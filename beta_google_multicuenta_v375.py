from datetime import datetime, timedelta, time
import json
from urllib.parse import urlencode, quote
from urllib.request import Request as UrlRequest, urlopen
from urllib.error import HTTPError, URLError

import beta_conexiones_rc2_fix1 as base
import beta_conexiones_rc2_1_calendar as personal_calendar

TARGET_EMAIL = "betaasistenteatlas@gmail.com"
TARGET_CALENDAR_SUMMARY = "Agenda Beta"

SCOPE_OPENID = "openid"
SCOPE_EMAIL = "https://www.googleapis.com/auth/userinfo.email"
SCOPE_PROFILE = "https://www.googleapis.com/auth/userinfo.profile"
SCOPE_CALENDAR_READONLY = "https://www.googleapis.com/auth/calendar.readonly"
SCOPE_CALENDAR_EVENTS = "https://www.googleapis.com/auth/calendar.events"

SCOPES_BETA_ASISTENTE = [
    SCOPE_OPENID,
    SCOPE_EMAIL,
    SCOPE_PROFILE,
    SCOPE_CALENDAR_READONLY,
    SCOPE_CALENDAR_EVENTS,
]

CALENDAR_LIST_URL = "https://www.googleapis.com/calendar/v3/users/me/calendarList"


def ruta_token_beta_asistente():
    return base.carpeta_google() / "token_oauth_beta_asistente.dpapi"


def _estado_asistente(estado=None):
    if estado is None:
        estado = base.cargar_estado()
    proveedores = estado.setdefault("proveedores", {})
    asistente = proveedores.setdefault("google_beta_asistente", {})
    asistente.setdefault("conectado", False)
    asistente.setdefault("cuenta", None)
    asistente.setdefault("nombre", None)
    asistente.setdefault("sub", None)
    asistente.setdefault("permisos", [])
    asistente.setdefault("calendar_id", None)
    asistente.setdefault("calendar_summary", None)
    asistente.setdefault("ultima_actualizacion", None)
    asistente["conectado"] = ruta_token_beta_asistente().exists() and bool(asistente.get("cuenta"))
    return estado, asistente


def estado_beta_asistente():
    _, asistente = _estado_asistente()
    return dict(asistente)


def _leer_token_info_asistente():
    path = ruta_token_beta_asistente()
    if not path.exists():
        return None
    return json.loads(base.leer_cifrado(path))


def token_asistente_tiene_calendar():
    info = _leer_token_info_asistente()
    if not info:
        return False
    scopes = info.get("scopes") or []
    if isinstance(scopes, str):
        scopes = scopes.split()
    scopes = set(scopes)
    return (
        SCOPE_CALENDAR_READONLY in scopes
        and SCOPE_CALENDAR_EVENTS in scopes
    )


def _userinfo(token):
    req = UrlRequest(
        base.USERINFO_URL,
        headers={"Authorization": f"Bearer {token}"},
        method="GET",
    )
    try:
        with urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as exc:
        detalle = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"UserInfo devolvió HTTP {exc.code}: {detalle[:400]}") from exc
    except URLError as exc:
        raise RuntimeError(f"No pude consultar la identidad Google: {exc}") from exc


def autorizar_beta_asistente():
    # Autoriza SOLO la segunda cuenta. No reemplaza token_oauth.dpapi.
    if not base.dependencia_google_disponible():
        raise RuntimeError("Falta google-auth-oauthlib.")

    from google_auth_oauthlib.flow import InstalledAppFlow

    config = base.cargar_config_cliente_google()
    flow = InstalledAppFlow.from_client_config(config, SCOPES_BETA_ASISTENTE)
    cred = flow.run_local_server(
        host="127.0.0.1",
        port=0,
        open_browser=True,
        authorization_prompt_message=(
            "Beta abrió el navegador para autorizar la cuenta Beta Asistente. "
            "Seleccione betaasistenteatlas@gmail.com."
        ),
        success_message=(
            "Autorización de Beta Asistente completada. "
            "Puede cerrar esta pestaña y volver a Beta."
        ),
        access_type="offline",
        prompt="consent",
        login_hint=TARGET_EMAIL,
    )

    if not cred or not cred.token:
        raise RuntimeError("Google no devolvió un token de acceso.")

    perfil = _userinfo(cred.token)
    email = (perfil.get("email") or "").strip().lower()
    if email != TARGET_EMAIL.lower():
        raise RuntimeError(
            "Se autorizó una cuenta distinta. "
            f"Debe seleccionar exactamente {TARGET_EMAIL}. "
            "No se guardó ningún token."
        )

    base.guardar_cifrado(
        ruta_token_beta_asistente(),
        cred.to_json(),
        "Beta Google OAuth Token - Beta Asistente",
    )

    estado, asistente = _estado_asistente()
    asistente.update({
        "conectado": True,
        "cuenta": perfil.get("email"),
        "nombre": perfil.get("name"),
        "sub": perfil.get("sub"),
        "permisos": list(SCOPES_BETA_ASISTENTE),
        "ultima_actualizacion": datetime.now().astimezone().isoformat(timespec="seconds"),
    })
    base.guardar_estado(estado)

    calendar_id = resolver_calendar_id_agenda_beta(forzar=True)
    return {
        "email": perfil.get("email"),
        "nombre": perfil.get("name"),
        "calendar_id": calendar_id,
        "calendar_summary": TARGET_CALENDAR_SUMMARY,
    }


def _credenciales_asistente():
    info = _leer_token_info_asistente()
    if not info:
        raise RuntimeError("La cuenta Beta Asistente todavía no está autorizada.")

    scopes = info.get("scopes") or []
    if isinstance(scopes, str):
        scopes = scopes.split()
    scopes = list(dict.fromkeys(scopes))

    requeridos = {SCOPE_CALENDAR_READONLY, SCOPE_CALENDAR_EVENTS}
    if not requeridos.issubset(set(scopes)):
        raise RuntimeError(
            "La cuenta Beta Asistente no tiene todos los permisos Calendar requeridos."
        )

    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request as GoogleRequest

    cred = Credentials.from_authorized_user_info(info, scopes=scopes)
    if cred.expired and cred.refresh_token:
        cred.refresh(GoogleRequest())
        base.guardar_cifrado(
            ruta_token_beta_asistente(),
            cred.to_json(),
            "Beta Google OAuth Token - Beta Asistente",
        )

    if not cred.valid:
        raise RuntimeError("El token de Beta Asistente no es válido.")

    perfil = _userinfo(cred.token)
    email = (perfil.get("email") or "").strip().lower()
    if email != TARGET_EMAIL.lower():
        raise RuntimeError(
            "El token separado ya no corresponde a la cuenta Beta Asistente esperada."
        )
    return cred


def _calendar_list(cred):
    params = urlencode({"maxResults": "250"})
    req = UrlRequest(
        CALENDAR_LIST_URL + "?" + params,
        headers={"Authorization": f"Bearer {cred.token}"},
        method="GET",
    )
    try:
        with urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except HTTPError as exc:
        detalle = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"CalendarList devolvió HTTP {exc.code}: {detalle[:500]}") from exc
    except URLError as exc:
        raise RuntimeError(f"No pude consultar CalendarList: {exc}") from exc
    return data.get("items", [])


def resolver_calendar_id_agenda_beta(forzar=False):
    estado, asistente = _estado_asistente()
    guardado = (asistente.get("calendar_id") or "").strip()
    if guardado and not forzar:
        return guardado

    cred = _credenciales_asistente()
    candidatos = []
    for cal in _calendar_list(cred):
        summary = (cal.get("summary") or "").strip()
        if summary.casefold() == TARGET_CALENDAR_SUMMARY.casefold():
            candidatos.append(cal)

    if not candidatos:
        raise RuntimeError(
            f"No encontré el calendario '{TARGET_CALENDAR_SUMMARY}' en {TARGET_EMAIL}."
        )

    candidatos.sort(
        key=lambda c: (
            c.get("accessRole") not in ("owner", "writer"),
            c.get("id") or "",
        )
    )
    elegido = candidatos[0]
    calendar_id = elegido.get("id")
    if not calendar_id:
        raise RuntimeError("Agenda Beta no devolvió calendar id.")

    asistente["calendar_id"] = calendar_id
    asistente["calendar_summary"] = elegido.get("summary")
    asistente["ultima_actualizacion"] = datetime.now().astimezone().isoformat(timespec="seconds")
    base.guardar_estado(estado)
    return calendar_id


def _consultar_eventos_asistente(time_min, time_max=None, max_results=50):
    cred = _credenciales_asistente()
    calendar_id = resolver_calendar_id_agenda_beta()
    params = {
        "timeMin": time_min.isoformat(),
        "singleEvents": "true",
        "orderBy": "startTime",
        "maxResults": str(max_results),
    }
    if time_max is not None:
        params["timeMax"] = time_max.isoformat()

    url = (
        "https://www.googleapis.com/calendar/v3/calendars/"
        + quote(calendar_id, safe="")
        + "/events?"
        + urlencode(params)
    )
    req = UrlRequest(
        url,
        headers={"Authorization": f"Bearer {cred.token}"},
        method="GET",
    )
    try:
        with urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except HTTPError as exc:
        detalle = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Agenda Beta devolvió HTTP {exc.code}: {detalle[:500]}") from exc
    except URLError as exc:
        raise RuntimeError(f"No pude consultar Agenda Beta: {exc}") from exc
    return data.get("items", [])


def _resumir_evento_asistente(evento):
    start = evento.get("start") or {}
    return {
        "inicio": start.get("dateTime") or start.get("date") or "",
        "titulo": evento.get("summary") or "(Sin título)",
        "ubicacion": evento.get("location"),
        "estado": evento.get("status"),
        "origen": "Agenda Beta",
    }


def _eventos_asistente_en_rango(inicio, fin=None, max_results=50):
    return [
        _resumir_evento_asistente(e)
        for e in _consultar_eventos_asistente(inicio, fin, max_results=max_results)
    ]


def _clave_evento(evento):
    return (
        str(evento.get("inicio") or "").strip(),
        str(evento.get("titulo") or "").strip().casefold(),
        str(evento.get("ubicacion") or "").strip().casefold(),
    )


def _combinar(personales, asistentes):
    resultado = []
    vistos = set()
    for evento in list(personales or []) + list(asistentes or []):
        clave = _clave_evento(evento)
        if clave in vistos:
            continue
        vistos.add(clave)
        resultado.append(evento)
    resultado.sort(key=lambda e: str(e.get("inicio") or ""))
    return resultado


def lectura_asistente_disponible():
    try:
        return token_asistente_tiene_calendar() and bool(resolver_calendar_id_agenda_beta())
    except Exception:
        return False


def calendar_autorizado():
    return bool(personal_calendar.token_tiene_calendar() or token_asistente_tiene_calendar())


def eventos_hoy():
    personales = []
    asistentes = []

    if personal_calendar.token_tiene_calendar():
        personales = personal_calendar.eventos_hoy()

    if token_asistente_tiene_calendar():
        ahora = datetime.now().astimezone()
        inicio = datetime.combine(ahora.date(), time.min, tzinfo=ahora.tzinfo)
        fin = inicio + timedelta(days=1)
        asistentes = _eventos_asistente_en_rango(inicio, fin)

    return _combinar(personales, asistentes)


def eventos_manana():
    personales = []
    asistentes = []

    if personal_calendar.token_tiene_calendar():
        personales = personal_calendar.eventos_manana()

    if token_asistente_tiene_calendar():
        ahora = datetime.now().astimezone()
        inicio = datetime.combine(
            ahora.date() + timedelta(days=1),
            time.min,
            tzinfo=ahora.tzinfo,
        )
        fin = inicio + timedelta(days=1)
        asistentes = _eventos_asistente_en_rango(inicio, fin)

    return _combinar(personales, asistentes)


def proximo_evento():
    candidatos = []

    if personal_calendar.token_tiene_calendar():
        p = personal_calendar.proximo_evento()
        if p:
            candidatos.append(p)

    if token_asistente_tiene_calendar():
        ahora = datetime.now().astimezone()
        a = _eventos_asistente_en_rango(ahora, None, max_results=1)
        if a:
            candidatos.append(a[0])

    if not candidatos:
        return None

    candidatos.sort(key=lambda e: str(e.get("inicio") or ""))
    return candidatos[0]
