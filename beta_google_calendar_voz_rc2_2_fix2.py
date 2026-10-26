# -*- coding: utf-8 -*-
# Beta v3.7.4 RC2.2 - Adaptador de voz para Google Calendar.
# Clasifica consultas acotadas, consulta RC2.1 directamente y no escribe eventos.

from __future__ import annotations

from datetime import datetime
import re
import unicodedata

import beta_conexiones_rc2_1_calendar as calendar_api


def _normalizar(texto):
    t = (texto or "").strip().lower()
    t = unicodedata.normalize("NFD", t)
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = re.sub(r"[¿?¡!.,;:]+", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    # No modifica el wake global. Solo limpia texto que ya llegó al cerebro.
    t = re.sub(r"^(?:beta|veta|petra)\s+", "", t).strip()
    return t


HOY = {
    "que tengo hoy",
    "que eventos tengo hoy",
    "que evento tengo hoy",
    "revisa mi calendario hoy",
    "revisar mi calendario hoy",
    "revisa mi calendario de hoy",
    "mi calendario hoy",
    "eventos de hoy",
    "agenda de hoy",
    # RC2.2 FIX2: variantes naturales observadas en aceptación v3.7.4.
    "que tengo hoy en mi calendario",
    "que tengo hoy en el calendario",
    "que tengo en mi calendario hoy",
    "que tengo en el calendario hoy",
    "que hay hoy en mi calendario",
    "que hay hoy en el calendario",
    "dime mis eventos de hoy",
    "cuales son mis eventos de hoy",
}

MANANA = {
    "que tengo manana",
    "que eventos tengo manana",
    "que evento tengo manana",
    "revisa mi calendario manana",
    "revisar mi calendario manana",
    "revisa mi calendario de manana",
    "mi calendario manana",
    "eventos de manana",
    "agenda de manana",
    # RC2.2 FIX2: variantes naturales observadas en aceptación v3.7.4.
    "que tengo manana en mi calendario",
    "que tengo manana en el calendario",
    "que tengo en mi calendario manana",
    "que tengo en el calendario manana",
    "que hay manana en mi calendario",
    "que hay manana en el calendario",
    "dime mis eventos de manana",
    "cuales son mis eventos de manana",
}

PROXIMO = {
    "cual es mi proximo evento",
    "cual es el proximo evento",
    "cual es mi siguiente evento",
    "mi proximo evento",
    "proximo evento",
    "siguiente evento",
}


def clasificar_consulta(texto):
    t = _normalizar(texto)
    if t in HOY:
        return "hoy"
    if t in MANANA:
        return "manana"
    if t in PROXIMO:
        return "proximo"
    if t in {
        "dime mis proximos eventos",
        "cuales son mis proximos eventos",
        "dime mi proximo evento",
        "cual es mi proximo evento",
    }:
        return "proximo"
    return None


def calendar_autorizado():
    return bool(calendar_api.token_tiene_calendar())


def _hora_legible(valor):
    if not valor:
        return "sin hora"

    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", valor):
        return "durante todo el día"

    try:
        dt = datetime.fromisoformat(valor.replace("Z", "+00:00"))
        if dt.tzinfo is not None:
            dt = dt.astimezone()
        return dt.strftime("%H:%M")
    except Exception:
        return valor


def _resumen_lista(eventos, referencia):
    if not eventos:
        if referencia == "hoy":
            return "hoy no registra eventos en su Google Calendar."
        return "mañana no registra eventos en su Google Calendar."

    cantidad = len(eventos)
    prefijo = (
        f"hoy tiene {cantidad} evento"
        if referencia == "hoy"
        else f"mañana tiene {cantidad} evento"
    )
    if cantidad != 1:
        prefijo += "s"

    partes = []
    limite = 4
    for evento in eventos[:limite]:
        titulo = (evento.get("titulo") or "(sin título)").strip()
        hora = _hora_legible(evento.get("inicio"))
        partes.append(f"{titulo}, {hora}")

    texto = prefijo + ". " + "; ".join(partes) + "."

    restantes = cantidad - limite
    if restantes > 0:
        texto += f" Además tiene {restantes} evento"
        if restantes != 1:
            texto += "s"
        texto += " adicional"
        if restantes != 1:
            texto += "es"
        texto += "."

    return texto


def _resumen_proximo(evento):
    if not evento:
        return "no encontré próximos eventos en su Google Calendar."

    titulo = (evento.get("titulo") or "(sin título)").strip()
    inicio = evento.get("inicio") or ""

    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", inicio):
        try:
            dt = datetime.strptime(inicio, "%Y-%m-%d")
            fecha = dt.strftime("%d/%m/%Y")
        except Exception:
            fecha = inicio
        return f"su próximo evento es {titulo}, programado para el {fecha}."

    try:
        dt = datetime.fromisoformat(inicio.replace("Z", "+00:00"))
        if dt.tzinfo is not None:
            dt = dt.astimezone()
        fecha = dt.strftime("%d/%m/%Y")
        hora = dt.strftime("%H:%M")
        return f"su próximo evento es {titulo}, el {fecha} a las {hora}."
    except Exception:
        return f"su próximo evento es {titulo}, con inicio {inicio}."


def responder_consulta(tipo):
    if tipo == "hoy":
        return _resumen_lista(calendar_api.eventos_hoy(), "hoy")
    if tipo == "manana":
        return _resumen_lista(calendar_api.eventos_manana(), "manana")
    if tipo == "proximo":
        return _resumen_proximo(calendar_api.proximo_evento())
    raise ValueError("Tipo de consulta Calendar no soportado.")
