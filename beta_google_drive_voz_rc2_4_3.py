# -*- coding: utf-8 -*-
# Beta v3.7.4 RC2.4.2 - Drive voz compacta + fallback plural PDF.

from __future__ import annotations

import re
import unicodedata

import beta_conexiones_rc2_3_drive as drive_api


def _normalizar(texto):
    t = (texto or "").strip().lower()
    t = unicodedata.normalize("NFD", t)
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = re.sub(r"[¿?¡!,;:]+", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"^(?:beta|veta|petra)\s+", "", t).strip()

    # Whisper observado: "buscacertificado.pdf ..."
    t = re.sub(r"^busca(?=\S)", "busca ", t)

    # Quitar solo punto final, conservando .pdf dentro de la frase.
    t = re.sub(r"[.]+$", "", t).strip()

    # Alias contextual de Drive SOLO al final de una orden Drive.
    # RC2.4.3: agrega deformaciones ASR observadas en aceptación v3.7.4
    # sin normalizar palabras fuera de un contexto final de Drive.
    t = re.sub(
        r"\b(?:google\s+)?(?:drive|driv|draiv|drivet|dribbe|adriven)\s*$",
        "drive",
        t,
    )

    return re.sub(r"\s+", " ", t).strip()


def _termino_busqueda(texto):
    t = _normalizar(texto)

    patrones = [
        r"^busca(?:me)?\s+(?:el\s+)?archivo\s+(.+?)\s+en\s+drive$",
        r"^busca(?:me)?\s+(.+?)\s+en\s+drive$",
        r"^buscar\s+(?:el\s+)?archivo\s+(.+?)\s+en\s+drive$",
        r"^buscar\s+(.+?)\s+en\s+drive$",
    ]

    for patron in patrones:
        m = re.fullmatch(patron, t)
        if not m:
            continue

        termino = m.group(1).strip()
        termino = re.sub(r"\s+punto\s+", ".", termino)
        termino = re.sub(r"\s+", " ", termino).strip()

        if termino:
            return termino

    return None


def _es_recientes(texto):
    t = _normalizar(texto)
    patrones = [
        # RC2.4.3: formas naturales de consulta observadas en aceptación.
        r"^(?:dime|muestrame|muestra|revisa|revisame)\s+(?:mis\s+)?archivos?\s+recientes\s+de\s+drive$",
        r"^cuales\s+son\s+(?:mis\s+)?archivos?\s+recientes\s+de\s+drive$",
        r"^(?:mis\s+)?archivos?\s+recientes\s+de\s+drive$",
    ]
    return any(re.fullmatch(p, t) for p in patrones)


def clasificar_consulta(texto):
    if _es_recientes(texto):
        return {"tipo": "recientes", "termino": None}

    termino = _termino_busqueda(texto)
    if termino:
        return {"tipo": "buscar", "termino": termino}

    return None


def drive_autorizado():
    return bool(drive_api.token_tiene_drive_metadata())


def _resumen_resultados(archivos, termino=None):
    # RC2.4.1: respuesta hablada compacta.
    # Máximo 3 nombres para reducir síntesis Piper y tiempo total de voz.
    if not archivos:
        if termino:
            return f"no encontré archivos que coincidan con {termino} en Google Drive."
        return "no encontré archivos recientes en Google Drive."

    cantidad = len(archivos)
    limite = 3
    nombres = [
        (a.get("nombre") or "(sin nombre)").strip()
        for a in archivos[:limite]
    ]

    if termino:
        texto = f"encontré {cantidad} resultado"
        if cantidad != 1:
            texto += "s"
        texto += f" para {termino}. "
        texto += "Los primeros son: "
    else:
        texto = f"encontré {cantidad} archivo"
        if cantidad != 1:
            texto += "s"
        texto += " reciente"
        if cantidad != 1:
            texto += "s"
        texto += ". Los primeros son: "

    texto += "; ".join(nombres) + "."

    restantes = cantidad - limite
    if restantes > 0:
        texto += f" Hay {restantes} resultado"
        if restantes != 1:
            texto += "s"
        texto += " adicional"
        if restantes != 1:
            texto += "es"
        texto += "."

    return texto


def _fallback_plural_pdf(termino):
    # RC2.4.2: corregir SOLO el caso observado por Whisper:
    # "certificados.pdf" -> "certificado.pdf".
    # Se usa únicamente como segundo intento si la búsqueda exacta no devuelve nada.
    import re

    t = (termino or "").strip()
    m = re.fullmatch(r"(.{4,})s(\.pdf)", t, flags=re.IGNORECASE)
    if not m:
        return None

    return m.group(1) + m.group(2)


def responder_consulta(consulta):
    tipo = consulta.get("tipo")

    if tipo == "recientes":
        return _resumen_resultados(drive_api.archivos_recientes(10))

    if tipo == "buscar":
        termino = consulta.get("termino") or ""
        archivos = drive_api.buscar_archivos(termino, 20)

        if not archivos:
            alternativo = _fallback_plural_pdf(termino)
            if alternativo:
                archivos = drive_api.buscar_archivos(alternativo, 20)
                if archivos:
                    termino = alternativo

        return _resumen_resultados(archivos, termino)

    raise ValueError("Consulta Drive no soportada.")
