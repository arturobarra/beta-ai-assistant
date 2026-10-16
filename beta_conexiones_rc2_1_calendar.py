# -*- coding: utf-8 -*-
"""Beta v3.7.4 Conexiones RC2.1 - Google Calendar SOLO LECTURA."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, time, timezone
from urllib.parse import urlencode
from urllib.request import Request as UrlRequest, urlopen
from urllib.error import HTTPError, URLError
import tkinter as tk
from tkinter import ttk, messagebox

import beta_conexiones_rc2_fix1 as base

VERSION = "v3.7.4 Conexiones RC2.1 Calendar Lectura"
SCOPE_CALENDAR_READONLY = "https://www.googleapis.com/auth/calendar.readonly"
SCOPES_GOOGLE_CALENDAR = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    SCOPE_CALENDAR_READONLY,
]
CALENDAR_EVENTS_URL = "https://www.googleapis.com/calendar/v3/calendars/primary/events"


def _ahora_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _leer_token_info():
    path = base.ruta_token_google()
    if not path.exists():
        return None
    return json.loads(base.leer_cifrado(path))


def token_tiene_calendar():
    info = _leer_token_info()
    if not info:
        return False
    scopes = info.get("scopes") or []
    if isinstance(scopes, str):
        scopes = scopes.split()
    return SCOPE_CALENDAR_READONLY in set(scopes)


def autorizar_google_calendar():
    if not base.dependencia_google_disponible():
        raise RuntimeError("Falta google-auth-oauthlib. Use el instalador de dependencias de RC2.")

    from google_auth_oauthlib.flow import InstalledAppFlow

    config = base.cargar_config_cliente_google()
    flow = InstalledAppFlow.from_client_config(config, SCOPES_GOOGLE_CALENDAR)
    credenciales = flow.run_local_server(
        host="127.0.0.1",
        port=0,
        open_browser=True,
        authorization_prompt_message=(
            "Beta abrió el navegador para autorizar Google Calendar en modo lectura."
        ),
        success_message=(
            "Autorización Calendar completada. Puede cerrar esta pestaña y volver a Beta."
        ),
        access_type="offline",
        prompt="consent",
    )

    if not credenciales or not credenciales.token:
        raise RuntimeError("Google no devolvió un token de acceso.")

    req = UrlRequest(
        base.USERINFO_URL,
        headers={"Authorization": f"Bearer {credenciales.token}"},
        method="GET",
    )
    try:
        with urlopen(req, timeout=15) as resp:
            perfil = json.loads(resp.read().decode("utf-8"))
    except (HTTPError, URLError) as exc:
        raise RuntimeError(f"No pude consultar la identidad Google: {exc}") from exc

    email = perfil.get("email")
    if not email:
        raise RuntimeError("Google autorizó la cuenta, pero no devolvió el correo.")

    base.guardar_cifrado(
        base.ruta_token_google(),
        credenciales.to_json(),
        "Beta Google OAuth Token",
    )

    estado = base.cargar_estado()
    g = estado["proveedores"]["google"]
    g["credencial_importada"] = True
    g["conectado"] = True
    g["cuenta"] = email
    g["nombre"] = perfil.get("name")
    g["sub"] = perfil.get("sub")
    g["permisos"] = list(SCOPES_GOOGLE_CALENDAR)
    g["ultima_actualizacion"] = _ahora_iso()
    estado["version"] = max(int(estado.get("version", 2)), 3)
    base.guardar_estado(estado)

    return {"email": email, "nombre": perfil.get("name"), "calendar_readonly": True}


def _credenciales_calendar():
    info = _leer_token_info()
    if not info:
        raise RuntimeError("Google no está conectado.")

    scopes = info.get("scopes") or []
    if isinstance(scopes, str):
        scopes = scopes.split()
    if SCOPE_CALENDAR_READONLY not in set(scopes):
        raise RuntimeError("Falta autorizar Calendar. Pulse 'Autorizar Calendar lectura'.")

    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request as GoogleRequest

    cred = Credentials.from_authorized_user_info(info, scopes=SCOPES_GOOGLE_CALENDAR)
    if cred.expired and cred.refresh_token:
        cred.refresh(GoogleRequest())
        base.guardar_cifrado(
            base.ruta_token_google(),
            cred.to_json(),
            "Beta Google OAuth Token",
        )

    if not cred.valid:
        raise RuntimeError("El token Google no es válido. Autorice Calendar nuevamente.")
    return cred


def _consultar_eventos(time_min, time_max=None, max_results=50):
    cred = _credenciales_calendar()
    params = {
        "timeMin": time_min.isoformat(),
        "singleEvents": "true",
        "orderBy": "startTime",
        "maxResults": str(max_results),
    }
    if time_max is not None:
        params["timeMax"] = time_max.isoformat()

    url = CALENDAR_EVENTS_URL + "?" + urlencode(params)
    req = UrlRequest(url, headers={"Authorization": f"Bearer {cred.token}"}, method="GET")
    try:
        with urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except HTTPError as exc:
        detalle = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Calendar API devolvió HTTP {exc.code}: {detalle[:500]}") from exc
    except URLError as exc:
        raise RuntimeError(f"No pude conectar con Google Calendar: {exc}") from exc
    return data.get("items", [])


def _inicio_evento(evento):
    start = evento.get("start") or {}
    return start.get("dateTime") or start.get("date") or ""


def _resumir_evento(evento):
    return {
        "inicio": _inicio_evento(evento),
        "titulo": evento.get("summary") or "(Sin título)",
        "ubicacion": evento.get("location"),
        "estado": evento.get("status"),
    }


def eventos_hoy():
    ahora = datetime.now().astimezone()
    inicio = datetime.combine(ahora.date(), time.min, tzinfo=ahora.tzinfo)
    fin = inicio + timedelta(days=1)
    return [_resumir_evento(e) for e in _consultar_eventos(inicio, fin)]


def eventos_manana():
    ahora = datetime.now().astimezone()
    inicio = datetime.combine(ahora.date() + timedelta(days=1), time.min, tzinfo=ahora.tzinfo)
    fin = inicio + timedelta(days=1)
    return [_resumir_evento(e) for e in _consultar_eventos(inicio, fin)]


def proximo_evento():
    ahora = datetime.now().astimezone()
    eventos = _consultar_eventos(ahora, None, max_results=1)
    return _resumir_evento(eventos[0]) if eventos else None


def _texto_eventos(titulo, eventos):
    if not eventos:
        return titulo + "\n\nNo encontré eventos."
    lineas = [titulo, ""]
    for i, evento in enumerate(eventos, 1):
        linea = f"{i}. {evento['inicio']} — {evento['titulo']}"
        if evento.get("ubicacion"):
            linea += f"\n   Ubicación: {evento['ubicacion']}"
        lineas.append(linea)
    return "\n".join(lineas)


class CentroCalendarRC21(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"Beta — Centro de Conexiones — {VERSION}")
        self.geometry("820x560")
        self.minsize(740, 500)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        cab = ttk.Frame(self, padding=(20, 18, 20, 10))
        cab.grid(row=0, column=0, sticky="ew")
        cab.columnconfigure(0, weight=1)
        ttk.Label(cab, text="Centro de Conexiones de Beta", font=("Segoe UI", 18, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(
            cab,
            text="RC2.1: Google Calendar solo lectura. No puede crear, modificar ni borrar eventos.",
            font=("Segoe UI", 10),
        ).grid(row=1, column=0, sticky="w", pady=(6, 0))

        self.cuerpo = ttk.Frame(self, padding=(20, 8, 20, 12))
        self.cuerpo.grid(row=1, column=0, sticky="nsew")
        self.cuerpo.columnconfigure(0, weight=1)

        pie = ttk.Frame(self, padding=(20, 8, 20, 18))
        pie.grid(row=2, column=0, sticky="ew")
        ttk.Label(
            pie,
            text="El token OAuth permanece cifrado con Windows DPAPI. Calendar se consulta exclusivamente por GET.",
            font=("Segoe UI", 9),
        ).grid(row=0, column=0, sticky="w")

        self.refrescar()

    def _limpiar(self):
        for w in self.cuerpo.winfo_children():
            w.destroy()

    def refrescar(self):
        self._limpiar()
        estado = base.cargar_estado()
        g = estado["proveedores"]["google"]
        conectado = bool(g.get("conectado"))
        calendar_ok = token_tiene_calendar()

        google = ttk.LabelFrame(self.cuerpo, text="Google", padding=16)
        google.grid(row=0, column=0, sticky="ew", pady=8)
        google.columnconfigure(1, weight=1)
        ttk.Label(google, text="Conectado" if conectado else "No conectado", font=("Segoe UI", 11, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(google, text=g.get("cuenta") or "Sin cuenta enrolada").grid(row=0, column=1, sticky="w", padx=(18, 8))
        ttk.Label(
            google,
            text="Calendar lectura autorizado" if calendar_ok else "Calendar pendiente de autorización",
            font=("Segoe UI", 10, "bold"),
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(10, 0))
        ttk.Label(google, text="Permiso: calendar.readonly").grid(row=2, column=0, columnspan=2, sticky="w", pady=(5, 0))
        ttk.Button(google, text="Autorizar Calendar lectura", command=self.autorizar_calendar_ui).grid(row=0, column=2, sticky="e", padx=(10, 0))

        pruebas = ttk.LabelFrame(self.cuerpo, text="Pruebas reales de Calendar", padding=16)
        pruebas.grid(row=1, column=0, sticky="ew", pady=8)
        b_hoy = ttk.Button(pruebas, text="Ver eventos de hoy", command=self.ver_hoy)
        b_manana = ttk.Button(pruebas, text="Ver eventos de mañana", command=self.ver_manana)
        b_prox = ttk.Button(pruebas, text="Ver próximo evento", command=self.ver_proximo)
        b_hoy.grid(row=0, column=0, padx=(0, 8))
        b_manana.grid(row=0, column=1, padx=8)
        b_prox.grid(row=0, column=2, padx=8)
        if not calendar_ok:
            b_hoy.state(["disabled"])
            b_manana.state(["disabled"])
            b_prox.state(["disabled"])
        ttk.Label(
            pruebas,
            text="Estas pruebas solo leen el calendario principal. No hay código de escritura en RC2.1.",
            font=("Segoe UI", 9),
        ).grid(row=1, column=0, columnspan=3, sticky="w", pady=(12, 0))

        github = ttk.LabelFrame(self.cuerpo, text="GitHub", padding=16)
        github.grid(row=2, column=0, sticky="ew", pady=8)
        github.columnconfigure(1, weight=1)
        ttk.Label(github, text="No conectado", font=("Segoe UI", 11, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(github, text="RC3: GitHub App con permisos mínimos por repositorio.").grid(row=0, column=1, sticky="w", padx=(18, 8))
        ttk.Button(github, text="Conectar GitHub (RC3)", state="disabled").grid(row=0, column=2, sticky="e")

    def autorizar_calendar_ui(self):
        try:
            info = autorizar_google_calendar()
        except Exception as exc:
            messagebox.showerror("Google Calendar", str(exc))
            return
        messagebox.showinfo(
            "Calendar autorizado",
            "Google Calendar quedó autorizado en modo solo lectura.\n\n"
            f"Cuenta: {info['email']}\n\n"
            "Beta todavía no puede crear, editar ni borrar eventos.",
        )
        self.refrescar()

    def ver_hoy(self):
        try:
            eventos = eventos_hoy()
        except Exception as exc:
            messagebox.showerror("Calendar — Hoy", str(exc))
            return
        messagebox.showinfo("Calendar — Hoy", _texto_eventos("Eventos de hoy", eventos))

    def ver_manana(self):
        try:
            eventos = eventos_manana()
        except Exception as exc:
            messagebox.showerror("Calendar — Mañana", str(exc))
            return
        messagebox.showinfo("Calendar — Mañana", _texto_eventos("Eventos de mañana", eventos))

    def ver_proximo(self):
        try:
            evento = proximo_evento()
        except Exception as exc:
            messagebox.showerror("Calendar — Próximo", str(exc))
            return
        if not evento:
            texto = "No encontré próximos eventos."
        else:
            texto = f"{evento['inicio']} — {evento['titulo']}"
            if evento.get("ubicacion"):
                texto += f"\nUbicación: {evento['ubicacion']}"
        messagebox.showinfo("Calendar — Próximo evento", texto)


if __name__ == "__main__":
    app = CentroCalendarRC21()
    app.mainloop()
