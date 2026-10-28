from datetime import datetime, timedelta
import json
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request as UrlRequest, urlopen

import beta_conexiones_rc2_1_calendar as calendar_base
import beta_google_multicuenta_v375 as calendar_multi

SCOPE_CALENDAR_EVENTS = "https://www.googleapis.com/auth/calendar.events"
CALENDAR_EVENTS_URL = "https://www.googleapis.com/calendar/v3/calendars/primary/events"


def _credenciales_escritura():
    return calendar_multi._credenciales_asistente()


def _evento_desde_payload(payload):
    titulo = str((payload or {}).get("titulo") or "").strip()
    fecha = str((payload or {}).get("fecha") or "").strip()
    hora = str((payload or {}).get("hora") or "").strip()
    lugar = str((payload or {}).get("lugar") or "").strip()
    notas = str((payload or {}).get("notas") or "").strip()

    if not titulo:
        raise ValueError("Falta el título del evento.")
    if not fecha:
        raise ValueError("Falta la fecha del evento.")
    if not hora:
        raise ValueError("Falta la hora del evento.")

    try:
        inicio_naive = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
    except ValueError as exc:
        raise ValueError("Fecha u hora inválida para Google Calendar.") from exc

    tz = datetime.now().astimezone().tzinfo
    inicio = inicio_naive.replace(tzinfo=tz)

    # Agenda Beta todavía no solicita duración por voz.
    # Usamos 60 minutos como duración predeterminada y no alteramos el payload local.
    fin = inicio + timedelta(minutes=60)

    cuerpo = {
        "summary": titulo,
        "start": {"dateTime": inicio.isoformat()},
        "end": {"dateTime": fin.isoformat()},
    }

    if lugar:
        cuerpo["location"] = lugar
    if notas:
        cuerpo["description"] = notas

    minutos = (payload or {}).get("recordatorio_minutos")
    try:
        minutos = int(minutos)
    except Exception:
        minutos = 0
    if minutos > 0:
        cuerpo["reminders"] = {
            "useDefault": False,
            "overrides": [{"method": "email", "minutes": minutos}],
        }

    return cuerpo


def crear_evento(payload):
    cred = _credenciales_escritura()
    calendar_id = calendar_multi.resolver_calendar_id_agenda_beta()
    cuerpo = _evento_desde_payload(payload)

    url = (
        "https://www.googleapis.com/calendar/v3/calendars/"
        + quote(calendar_id, safe="")
        + "/events"
    )

    req = UrlRequest(
        url,
        data=json.dumps(cuerpo, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {cred.token}",
            "Content-Type": "application/json; charset=utf-8",
        },
        method="POST",
    )

    try:
        with urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except HTTPError as exc:
        detalle = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Calendar API devolvió HTTP {exc.code}: {detalle[:500]}"
        ) from exc
    except URLError as exc:
        raise RuntimeError(f"No pude conectar con Google Calendar: {exc}") from exc

    if not data.get("id"):
        raise RuntimeError("Google Calendar no devolvió un identificador de evento.")

    return {
        "ok": True,
        "sincronizado": True,
        "google_event_id": data.get("id"),
        "html_link": data.get("htmlLink"),
        "google_cuenta": calendar_multi.TARGET_EMAIL,
        "google_calendar": calendar_multi.TARGET_CALENDAR_SUMMARY,
        "google_calendar_id": calendar_id,
    }

def actualizar_evento(google_event_id, payload, calendar_id=None):
    google_event_id = str(google_event_id or "").strip()
    if not google_event_id:
        raise ValueError("Falta google_event_id para actualizar Google Calendar.")

    cred = _credenciales_escritura()
    calendar_id = str(calendar_id or "").strip() or calendar_multi.resolver_calendar_id_agenda_beta()
    cuerpo = _evento_desde_payload(payload)

    url = (
        "https://www.googleapis.com/calendar/v3/calendars/"
        + quote(calendar_id, safe="")
        + "/events/"
        + quote(google_event_id, safe="")
    )

    req = UrlRequest(
        url,
        data=json.dumps(cuerpo, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {cred.token}",
            "Content-Type": "application/json; charset=utf-8",
        },
        method="PATCH",
    )

    try:
        with urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except HTTPError as exc:
        detalle = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Calendar API devolvió HTTP {exc.code} al actualizar: {detalle[:500]}"
        ) from exc
    except URLError as exc:
        raise RuntimeError(f"No pude conectar con Google Calendar al actualizar: {exc}") from exc

    if data.get("id") != google_event_id:
        raise RuntimeError("Google Calendar devolvió un evento distinto al esperado.")

    return {
        "ok": True,
        "sincronizado": True,
        "google_event_id": data.get("id"),
        "html_link": data.get("htmlLink"),
        "google_cuenta": calendar_multi.TARGET_EMAIL,
        "google_calendar": calendar_multi.TARGET_CALENDAR_SUMMARY,
        "google_calendar_id": calendar_id,
    }


def eliminar_evento(google_event_id, calendar_id=None):
    google_event_id = str(google_event_id or "").strip()
    if not google_event_id:
        raise ValueError("Falta google_event_id para eliminar en Google Calendar.")

    cred = _credenciales_escritura()
    calendar_id = str(calendar_id or "").strip() or calendar_multi.resolver_calendar_id_agenda_beta()

    url = (
        "https://www.googleapis.com/calendar/v3/calendars/"
        + quote(calendar_id, safe="")
        + "/events/"
        + quote(google_event_id, safe="")
    )

    req = UrlRequest(
        url,
        headers={"Authorization": f"Bearer {cred.token}"},
        method="DELETE",
    )

    try:
        with urlopen(req, timeout=20) as resp:
            resp.read()
    except HTTPError as exc:
        if exc.code in (404, 410):
            return {
                "ok": True,
                "eliminado": True,
                "ya_ausente": True,
                "google_event_id": google_event_id,
                "google_calendar_id": calendar_id,
            }
        detalle = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Calendar API devolvió HTTP {exc.code} al eliminar: {detalle[:500]}"
        ) from exc
    except URLError as exc:
        raise RuntimeError(f"No pude conectar con Google Calendar al eliminar: {exc}") from exc

    return {
        "ok": True,
        "eliminado": True,
        "ya_ausente": False,
        "google_event_id": google_event_id,
        "google_calendar_id": calendar_id,
    }
