# -*- coding: utf-8 -*-
# Beta v3.7.4 RC2.6 FIX1 - Gmail metadata por voz + guardia de recientes ambiguos.
#
# Permite:
# - correos recientes de Recibidos;
# - correos no leídos de Recibidos;
# - contar correos no leídos de Recibidos.
#
# NO lee el cuerpo, snippet ni adjuntos.
# NO usa q.
# NO envía, responde, archiva, elimina ni modifica mensajes.

from __future__ import annotations

from email.utils import parseaddr
import re
import unicodedata

import beta_conexiones_rc2_5_gmail_metadata as gmail_api


GMAIL_INBOX_LABEL_URL = (
    "https://gmail.googleapis.com/gmail/v1/users/me/labels/INBOX"
    "?fields=messagesUnread"
)


def _normalizar(texto):
    t = (texto or "").strip().lower()
    t = unicodedata.normalize("NFD", t)
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = re.sub(r"[¿?¡!,;:.]+", " ", t)
    t = re.sub(r"\s+", " ", t).strip()

    # Solo dentro del adaptador de intención, sin tocar el wake global.
    t = re.sub(r"^(?:beta|veta|petra)\s+", "", t).strip()
    return t


RECIENTES = {
    "dime mis correos recientes",
    "muestrame mis correos recientes",
    "muestra mis correos recientes",
    "cuales son mis correos recientes",
    "que correos recientes tengo",
    "revisa mis correos recientes",
    "dime los correos recientes",
    "muestrame los correos recientes",
}

NO_LEIDOS = {
    "dime mis correos no leidos",
    "muestrame mis correos no leidos",
    "muestra mis correos no leidos",
    "cuales son mis correos no leidos",
    "que correos no leidos tengo",
    "revisa mis correos no leidos",
}

NUEVOS = {
    "tengo correos nuevos",
    "hay correos nuevos",
    "tengo correos no leidos",
    "hay correos no leidos",
}

CONTAR_NO_LEIDOS = {
    "cuantos correos no leidos tengo",
    "cuantos correos nuevos tengo",
    "cuantos correos sin leer tengo",
    "cuantos mensajes no leidos tengo",
}

RECIENTES_SIN_PERIODO = {
    "dime cuantos correos recientes",
    "cuantos correos recientes tengo",
    "cuantos correos recientes hay",
    "dime cuantos correos recientes tengo",
}


def clasificar_consulta(texto):
    t = _normalizar(texto)

    if t in RECIENTES_SIN_PERIODO:
        return {"tipo": "recientes_sin_periodo"}

    if t in CONTAR_NO_LEIDOS:
        return {"tipo": "contar_no_leidos"}

    if t in NUEVOS:
        return {"tipo": "contar_no_leidos"}

    if t in NO_LEIDOS:
        return {"tipo": "no_leidos"}

    if t in RECIENTES:
        return {"tipo": "recientes"}

    return None


def gmail_autorizado():
    return bool(gmail_api.token_tiene_gmail_metadata())


def contar_no_leidos():
    data = gmail_api._gmail_get_json(GMAIL_INBOX_LABEL_URL)
    return int(data.get("messagesUnread") or 0)


def _nombre_remitente(valor):
    nombre, correo = parseaddr(valor or "")
    nombre = (nombre or "").strip().strip('"')

    if nombre:
        return nombre

    if correo:
        local = correo.split("@", 1)[0].strip()
        return local or "remitente desconocido"

    return "remitente desconocido"


def _resumen_mensajes(mensajes, titulo):
    if not mensajes:
        return titulo + " No encontré mensajes."

    # Máximo 3 para que Piper responda rápido.
    limite = 3
    partes = []

    for msg in mensajes[:limite]:
        asunto = (msg.get("asunto") or "(Sin asunto)").strip()
        remitente = _nombre_remitente(msg.get("de"))
        partes.append(f"{asunto}, de {remitente}")

    texto = titulo + " " + "; ".join(partes) + "."

    restantes = len(mensajes) - limite
    if restantes > 0:
        texto += f" Hay {restantes} resultado"
        if restantes != 1:
            texto += "s"
        texto += " adicional"
        if restantes != 1:
            texto += "es"
        texto += "."

    return texto


def responder_consulta(consulta):
    tipo = consulta.get("tipo")

    if tipo == "recientes_sin_periodo":
        return (
            "para contar correos recientes necesito un período definido. "
            "Puede pedirme sus correos recientes, o preguntar cuántos correos no leídos tiene."
        )

    if tipo == "contar_no_leidos":
        cantidad = contar_no_leidos()

        if cantidad == 0:
            return "no tiene correos no leídos en Recibidos."

        if cantidad == 1:
            return "tiene 1 correo no leído en Recibidos."

        return f"tiene {cantidad} correos no leídos en Recibidos."

    if tipo == "recientes":
        mensajes = gmail_api.correos_recientes(5)
        return _resumen_mensajes(
            mensajes,
            "sus correos recientes son:",
        )

    if tipo == "no_leidos":
        total = contar_no_leidos()

        if total == 0:
            return "no tiene correos no leídos en Recibidos."

        mensajes = gmail_api.correos_no_leidos(5)
        texto = _resumen_mensajes(
            mensajes,
            f"tiene {total} correos no leídos. Los primeros son:",
        )
        return texto

    raise ValueError("Consulta Gmail no soportada.")
