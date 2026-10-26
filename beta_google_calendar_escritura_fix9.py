from datetime import datetime, timedelta
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request as UrlRequest, urlopen

import beta_conexiones_rc2_1_calendar as calendar_base

SCOPE_CALENDAR_EVENTS = "https://www.googleapis.com/auth/calendar.events"
CALENDAR_EVENTS_URL = "https://www.googleapis.com/calendar/v3/calendars/primary/events"


def _credenciales_escritura():
    info = calendar_base._leer_token_info()
    if not info:
        raise RuntimeError("Google no está conectado.")

    scopes = info.get("scopes") or []
    if isinstance(scopes, str):
        scopes = scopes.split()
    scopes = list(dict.fromkeys(scopes))

    if SCOPE_CALENDAR_EVENTS not in set(scopes):
        raise RuntimeError(
            "Falta el permiso calendar.events. Reautorice Google Calendar escritura."
        )

    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request as GoogleRequest

    # Usamos los scopes realmente guardados en el token para no perder
    # Calendar lectura, Drive metadata ni Gmail metadata al refrescarlo.
    cred = Credentials.from_authorized_user_info(info, scopes=scopes)
    if cred.expired and cred.refresh_token:
        cred.refresh(GoogleRequest())
        calendar_base.base.guardar_cifrado(
            calendar_base.base.ruta_token_google(),
            cred.to_json(),
            "Beta Google OAuth Token",
        )

    if not cred.valid:
        raise RuntimeError("El token Google no es válido para Calendar.")
    return cred


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
    cuerpo = _evento_desde_payload(payload)

    req = UrlRequest(
        CALENDAR_EVENTS_URL,
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
    }
