# -*- coding: utf-8 -*-
# Beta v3.7.4 RC2.5 - Gmail metadata SOLO LECTURA.
#
# Permite:
# - reautorizar Google conservando identidad + Calendar + Drive metadata;
# - añadir gmail.metadata;
# - listar correos recientes de INBOX;
# - listar correos no leídos de INBOX;
# - leer únicamente encabezados From / Subject / Date.
#
# NO lee cuerpo del correo.
# NO usa snippet.
# NO envía, responde, archiva, elimina, mueve ni modifica mensajes.
# NO usa el parámetro q de Gmail porque gmail.metadata no lo permite.

from __future__ import annotations

import json
from datetime import datetime, timezone
from urllib.parse import urlencode, quote
from urllib.request import Request as UrlRequest, urlopen
from urllib.error import HTTPError, URLError
import tkinter as tk
from tkinter import ttk, messagebox

import beta_conexiones_rc2_fix1 as base
import beta_conexiones_rc2_1_calendar as calendar_base
import beta_conexiones_rc2_3_drive as drive_base

VERSION = "v3.7.4 Conexiones RC2.5 Gmail Metadata"
SCOPE_GMAIL_METADATA = "https://www.googleapis.com/auth/gmail.metadata"

SCOPES_GOOGLE_GMAIL = list(dict.fromkeys(
    drive_base.SCOPES_GOOGLE_DRIVE + [SCOPE_GMAIL_METADATA]
))

GMAIL_MESSAGES_URL = "https://gmail.googleapis.com/gmail/v1/users/me/messages"


def _ahora_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _leer_token_info():
    p = base.ruta_token_google()
    if not p.exists():
        return None
    return json.loads(base.leer_cifrado(p))


def _scopes_token():
    info = _leer_token_info()
    if not info:
        return set()

    scopes = info.get("scopes") or []
    if isinstance(scopes, str):
        scopes = scopes.split()

    return set(scopes)


def token_tiene_gmail_metadata():
    return SCOPE_GMAIL_METADATA in _scopes_token()


def token_conserva_calendar():
    return calendar_base.SCOPE_CALENDAR_READONLY in _scopes_token()


def token_conserva_drive():
    return drive_base.SCOPE_DRIVE_METADATA in _scopes_token()


def autorizar_google_gmail_metadata():
    if not base.dependencia_google_disponible():
        raise RuntimeError("Falta google-auth-oauthlib.")

    from google_auth_oauthlib.flow import InstalledAppFlow

    config = base.cargar_config_cliente_google()
    flow = InstalledAppFlow.from_client_config(
        config,
        SCOPES_GOOGLE_GMAIL,
    )

    cred = flow.run_local_server(
        host="127.0.0.1",
        port=0,
        open_browser=True,
        authorization_prompt_message=(
            "Beta abrió el navegador para autorizar Gmail "
            "en modo metadatos de solo lectura."
        ),
        success_message=(
            "Autorización Gmail completada. "
            "Puede cerrar esta pestaña y volver a Beta."
        ),
        access_type="offline",
        prompt="consent",
    )

    if not cred or not cred.token:
        raise RuntimeError("Google no devolvió un token de acceso.")

    req = UrlRequest(
        base.USERINFO_URL,
        headers={"Authorization": f"Bearer {cred.token}"},
        method="GET",
    )

    try:
        with urlopen(req, timeout=15) as resp:
            perfil = json.loads(resp.read().decode("utf-8"))
    except (HTTPError, URLError) as exc:
        raise RuntimeError(
            f"No pude consultar la identidad Google: {exc}"
        ) from exc

    email = perfil.get("email")
    if not email:
        raise RuntimeError("Google no devolvió el correo.")

    # Sustituir el token cifrado solo después de OAuth exitoso.
    base.guardar_cifrado(
        base.ruta_token_google(),
        cred.to_json(),
        "Beta Google OAuth Token",
    )

    estado = base.cargar_estado()
    g = estado["proveedores"]["google"]
    g["credencial_importada"] = True
    g["conectado"] = True
    g["cuenta"] = email
    g["nombre"] = perfil.get("name")
    g["sub"] = perfil.get("sub")
    g["permisos"] = list(SCOPES_GOOGLE_GMAIL)
    g["ultima_actualizacion"] = _ahora_iso()
    estado["version"] = max(int(estado.get("version", 2)), 5)
    base.guardar_estado(estado)

    return {
        "email": email,
        "calendar_readonly": True,
        "drive_metadata_readonly": True,
        "gmail_metadata": True,
    }


def _credenciales_gmail():
    info = _leer_token_info()
    if not info:
        raise RuntimeError("Google no está conectado.")

    scopes = info.get("scopes") or []
    if isinstance(scopes, str):
        scopes = scopes.split()
    scopes = set(scopes)

    requeridos = {
        SCOPE_GMAIL_METADATA,
        calendar_base.SCOPE_CALENDAR_READONLY,
        drive_base.SCOPE_DRIVE_METADATA,
    }

    faltantes = requeridos - scopes
    if faltantes:
        raise RuntimeError(
            "El token Google no contiene todos los permisos esperados. "
            "Autorice Gmail nuevamente desde RC2.5."
        )

    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request as GoogleRequest

    cred = Credentials.from_authorized_user_info(
        info,
        scopes=SCOPES_GOOGLE_GMAIL,
    )

    if cred.expired and cred.refresh_token:
        cred.refresh(GoogleRequest())
        base.guardar_cifrado(
            base.ruta_token_google(),
            cred.to_json(),
            "Beta Google OAuth Token",
        )

    if not cred.valid:
        raise RuntimeError(
            "El token Google no es válido. Autorice Gmail nuevamente."
        )

    return cred


def _gmail_get_json(url):
    cred = _credenciales_gmail()

    req = UrlRequest(
        url,
        headers={"Authorization": f"Bearer {cred.token}"},
        method="GET",
    )

    try:
        with urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as exc:
        detalle = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Gmail API devolvió HTTP {exc.code}: {detalle[:600]}"
        ) from exc
    except URLError as exc:
        raise RuntimeError(
            f"No pude conectar con Gmail API: {exc}"
        ) from exc


def _listar_ids(label_ids, limite=10):
    limite = max(1, min(int(limite), 20))

    params = [
        ("maxResults", str(limite)),
    ]
    for label in label_ids:
        params.append(("labelIds", label))

    # Deliberadamente NO usamos q: gmail.metadata no admite ese parámetro.
    url = GMAIL_MESSAGES_URL + "?" + urlencode(params)
    data = _gmail_get_json(url)

    return [x.get("id") for x in data.get("messages", []) if x.get("id")]


def _mensaje_metadata(message_id):
    safe_id = quote(str(message_id), safe="")
    params = [
        ("format", "metadata"),
        ("metadataHeaders", "From"),
        ("metadataHeaders", "Subject"),
        ("metadataHeaders", "Date"),
        (
            "fields",
            "id,threadId,labelIds,internalDate,"
            "payload(headers(name,value))",
        ),
    ]

    url = (
        GMAIL_MESSAGES_URL
        + "/"
        + safe_id
        + "?"
        + urlencode(params)
    )

    data = _gmail_get_json(url)

    headers = {}
    for h in (data.get("payload") or {}).get("headers", []):
        nombre = (h.get("name") or "").strip().lower()
        if nombre in {"from", "subject", "date"}:
            headers[nombre] = (h.get("value") or "").strip()

    return {
        "id": data.get("id"),
        "threadId": data.get("threadId"),
        "labelIds": data.get("labelIds") or [],
        "internalDate": data.get("internalDate"),
        "de": headers.get("from") or "(Remitente sin nombre)",
        "asunto": headers.get("subject") or "(Sin asunto)",
        "fecha": headers.get("date") or "(Sin fecha)",
    }


def _obtener_mensajes(label_ids, limite=10):
    ids = _listar_ids(label_ids, limite)
    return [_mensaje_metadata(mid) for mid in ids]


def correos_recientes(limite=10):
    return _obtener_mensajes(["INBOX"], limite)


def correos_no_leidos(limite=10):
    return _obtener_mensajes(["INBOX", "UNREAD"], limite)


def _texto_correos(titulo, mensajes):
    if not mensajes:
        return titulo + "\n\nNo encontré mensajes."

    lineas = [titulo, ""]
    for i, msg in enumerate(mensajes, 1):
        lineas.append(
            f"{i}. {msg['asunto']}\n"
            f"   De: {msg['de']}\n"
            f"   Fecha: {msg['fecha']}"
        )
    return "\n".join(lineas)


class CentroGmailRC25(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"Beta — Centro de Conexiones — {VERSION}")
        self.geometry("900x650")
        self.minsize(800, 560)
        self.columnconfigure(0, weight=1)

        cab = ttk.Frame(self, padding=20)
        cab.grid(row=0, column=0, sticky="ew")

        ttk.Label(
            cab,
            text="Centro de Conexiones de Beta",
            font=("Segoe UI", 18, "bold"),
        ).grid(row=0, column=0, sticky="w")

        ttk.Label(
            cab,
            text=(
                "RC2.5: Gmail solo metadatos. "
                "Lee remitente, asunto, fecha y etiquetas; NO el cuerpo."
            ),
        ).grid(row=1, column=0, sticky="w", pady=(6, 0))

        self.cuerpo = ttk.Frame(self, padding=(20, 0, 20, 20))
        self.cuerpo.grid(row=1, column=0, sticky="nsew")
        self.cuerpo.columnconfigure(0, weight=1)

        self.refrescar()

    def _limpiar(self):
        for w in self.cuerpo.winfo_children():
            w.destroy()

    def refrescar(self):
        self._limpiar()

        estado = base.cargar_estado()
        g = estado["proveedores"]["google"]

        cal_ok = token_conserva_calendar()
        drive_ok = token_conserva_drive()
        gmail_ok = token_tiene_gmail_metadata()

        box = ttk.LabelFrame(self.cuerpo, text="Google", padding=16)
        box.grid(row=0, column=0, sticky="ew", pady=8)
        box.columnconfigure(1, weight=1)

        ttk.Label(
            box,
            text="Conectado" if g.get("conectado") else "No conectado",
            font=("Segoe UI", 11, "bold"),
        ).grid(row=0, column=0, sticky="w")

        ttk.Label(
            box,
            text=g.get("cuenta") or "Sin cuenta",
        ).grid(row=0, column=1, sticky="w", padx=(16, 8))

        ttk.Label(
            box,
            text="Calendar lectura: OK" if cal_ok else "Calendar lectura: pendiente",
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(8, 0))

        ttk.Label(
            box,
            text="Drive metadatos: OK" if drive_ok else "Drive metadatos: pendiente",
        ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(5, 0))

        ttk.Label(
            box,
            text="Gmail metadatos: autorizado" if gmail_ok else "Gmail metadatos: pendiente",
            font=("Segoe UI", 10, "bold"),
        ).grid(row=3, column=0, columnspan=2, sticky="w", pady=(5, 0))

        ttk.Button(
            box,
            text="Autorizar Gmail metadatos",
            command=self.autorizar,
        ).grid(row=0, column=2, rowspan=4, sticky="e")

        pruebas = ttk.LabelFrame(
            self.cuerpo,
            text="Pruebas reales de Gmail",
            padding=16,
        )
        pruebas.grid(row=1, column=0, sticky="ew", pady=8)

        b_recientes = ttk.Button(
            pruebas,
            text="Ver correos recientes",
            command=self.recientes,
        )
        b_recientes.grid(row=0, column=0, sticky="w")

        b_no_leidos = ttk.Button(
            pruebas,
            text="Ver correos no leídos",
            command=self.no_leidos,
        )
        b_no_leidos.grid(row=0, column=1, sticky="w", padx=(12, 0))

        if not gmail_ok:
            b_recientes.state(["disabled"])
            b_no_leidos.state(["disabled"])

        ttk.Label(
            pruebas,
            text=(
                "RC2.5 muestra solo De, Asunto y Fecha. "
                "No lee contenido, adjuntos ni snippet."
            ),
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(14, 0))

    def autorizar(self):
        try:
            info = autorizar_google_gmail_metadata()
        except Exception as exc:
            messagebox.showerror("Gmail", str(exc))
            return

        messagebox.showinfo(
            "Gmail autorizado",
            (
                "Gmail quedó autorizado en modo metadatos de solo lectura.\n\n"
                f"Cuenta: {info['email']}\n\n"
                "Calendar readonly y Drive metadata fueron conservados.\n"
                "Beta todavía no puede leer el cuerpo ni modificar correos."
            ),
        )
        self.refrescar()

    def recientes(self):
        try:
            mensajes = correos_recientes(10)
        except Exception as exc:
            messagebox.showerror("Gmail — Recientes", str(exc))
            return

        messagebox.showinfo(
            "Gmail — Recientes",
            _texto_correos("Correos recientes de Recibidos", mensajes),
        )

    def no_leidos(self):
        try:
            mensajes = correos_no_leidos(10)
        except Exception as exc:
            messagebox.showerror("Gmail — No leídos", str(exc))
            return

        messagebox.showinfo(
            "Gmail — No leídos",
            _texto_correos("Correos no leídos de Recibidos", mensajes),
        )


if __name__ == "__main__":
    CentroGmailRC25().mainloop()
