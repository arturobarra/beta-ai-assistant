# -*- coding: utf-8 -*-
# Beta v3.7.4 RC2.3 - Google Drive metadata readonly

from __future__ import annotations

import json
from datetime import datetime, timezone
from urllib.parse import urlencode
from urllib.request import Request as UrlRequest, urlopen
from urllib.error import HTTPError, URLError
import tkinter as tk
from tkinter import ttk, messagebox

import beta_conexiones_rc2_fix1 as base
import beta_conexiones_rc2_1_calendar as calendar_base

VERSION = "v3.7.4 Conexiones RC2.3 Drive Metadata"
SCOPE_DRIVE_METADATA = "https://www.googleapis.com/auth/drive.metadata.readonly"

SCOPES_GOOGLE_DRIVE = list(dict.fromkeys(
    list(calendar_base.SCOPES_GOOGLE_CALENDAR) + [SCOPE_DRIVE_METADATA]
))

DRIVE_FILES_URL = "https://www.googleapis.com/drive/v3/files"

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

def token_tiene_drive_metadata():
    return SCOPE_DRIVE_METADATA in _scopes_token()

def token_conserva_calendar():
    return calendar_base.SCOPE_CALENDAR_READONLY in _scopes_token()

def autorizar_google_drive_metadata():
    if not base.dependencia_google_disponible():
        raise RuntimeError("Falta google-auth-oauthlib.")

    from google_auth_oauthlib.flow import InstalledAppFlow

    config = base.cargar_config_cliente_google()
    flow = InstalledAppFlow.from_client_config(config, SCOPES_GOOGLE_DRIVE)

    cred = flow.run_local_server(
        host="127.0.0.1",
        port=0,
        open_browser=True,
        authorization_prompt_message=(
            "Beta abrió el navegador para autorizar Google Drive conservando los permisos Google de Beta "
            "en modo metadatos de solo lectura."
        ),
        success_message=(
            "Autorización Drive completada. Puede cerrar esta pestaña y volver a Beta."
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
        raise RuntimeError(f"No pude consultar la identidad Google: {exc}") from exc

    email = perfil.get("email")
    if not email:
        raise RuntimeError("Google no devolvió el correo.")

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
    g["permisos"] = list(SCOPES_GOOGLE_DRIVE)
    g["ultima_actualizacion"] = _ahora_iso()
    estado["version"] = max(int(estado.get("version", 2)), 4)
    base.guardar_estado(estado)

    return {
        "email": email,
        "drive_metadata_readonly": True,
        "calendar_readonly": True,
    }

def _credenciales_drive():
    info = _leer_token_info()
    if not info:
        raise RuntimeError("Google no está conectado.")

    scopes = info.get("scopes") or []
    if isinstance(scopes, str):
        scopes = scopes.split()
    scopes = set(scopes)

    if SCOPE_DRIVE_METADATA not in scopes:
        raise RuntimeError("Falta autorizar Drive.")
    if calendar_base.SCOPE_CALENDAR_READONLY not in scopes:
        raise RuntimeError("El token actual no conserva Calendar readonly.")

    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request as GoogleRequest

    cred = Credentials.from_authorized_user_info(
        info,
        scopes=SCOPES_GOOGLE_DRIVE,
    )

    if cred.expired and cred.refresh_token:
        cred.refresh(GoogleRequest())
        base.guardar_cifrado(
            base.ruta_token_google(),
            cred.to_json(),
            "Beta Google OAuth Token",
        )

    if not cred.valid:
        raise RuntimeError("El token Google no es válido.")

    return cred

def _escape_drive_q(texto):
    return (texto or "").replace("\\", "\\\\").replace("'", "\\'")

def _drive_list(params):
    cred = _credenciales_drive()

    base_params = {
        "fields": (
            "nextPageToken,"
            "files(id,name,mimeType,modifiedTime,createdTime,"
            "webViewLink,parents,trashed)"
        ),
        "pageSize": "20",
        "spaces": "drive",
    }
    base_params.update(params)

    url = DRIVE_FILES_URL + "?" + urlencode(base_params)

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
        raise RuntimeError(
            f"Drive API HTTP {exc.code}: {detalle[:500]}"
        ) from exc
    except URLError as exc:
        raise RuntimeError(f"No pude conectar con Google Drive: {exc}") from exc

    return data.get("files", [])

def _resumir(item):
    return {
        "id": item.get("id"),
        "nombre": item.get("name") or "(Sin nombre)",
        "mimeType": item.get("mimeType"),
        "modificado": item.get("modifiedTime"),
        "creado": item.get("createdTime"),
        "webViewLink": item.get("webViewLink"),
        "parents": item.get("parents") or [],
    }

def archivos_recientes(limite=10):
    limite = max(1, min(int(limite), 20))
    items = _drive_list({
        "q": "trashed = false",
        "orderBy": "modifiedTime desc",
        "pageSize": str(limite),
    })
    return [_resumir(x) for x in items]

def buscar_archivos(nombre, limite=20):
    nombre = (nombre or "").strip()
    if not nombre:
        raise ValueError("Escriba un nombre o fragmento para buscar.")

    seguro = _escape_drive_q(nombre)

    items = _drive_list({
        "q": f"name contains '{seguro}' and trashed = false",
        "orderBy": "modifiedTime desc",
        "pageSize": str(max(1, min(int(limite), 20))),
    })
    return [_resumir(x) for x in items]

def _texto(titulo, archivos):
    if not archivos:
        return titulo + "\n\nNo encontré archivos."

    lineas = [titulo, ""]
    for i, a in enumerate(archivos, 1):
        lineas.append(
            f"{i}. {a['nombre']}\n"
            f"   Tipo: {a.get('mimeType') or 'desconocido'}\n"
            f"   Modificado: {a.get('modificado') or 'sin fecha'}"
        )
    return "\n".join(lineas)

class CentroDriveRC23(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"Beta — Centro de Conexiones — {VERSION}")
        self.geometry("860x600")
        self.minsize(760, 520)
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
                "RC2.3: Drive solo metadatos. "
                "No descarga contenido ni modifica archivos."
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
        drive_ok = token_tiene_drive_metadata()
        cal_ok = token_conserva_calendar()

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
            text=(
                "Drive metadatos: autorizado"
                if drive_ok
                else "Drive metadatos: pendiente"
            ),
            font=("Segoe UI", 10, "bold"),
        ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(5, 0))

        ttk.Button(
            box,
            text="Autorizar Drive metadatos",
            command=self.autorizar,
        ).grid(row=0, column=2, rowspan=3, sticky="e")

        pruebas = ttk.LabelFrame(
            self.cuerpo,
            text="Pruebas reales de Drive",
            padding=16,
        )
        pruebas.grid(row=1, column=0, sticky="ew", pady=8)
        pruebas.columnconfigure(1, weight=1)

        ttk.Label(
            pruebas,
            text="Buscar por nombre:",
        ).grid(row=0, column=0, sticky="w")

        self.busqueda = ttk.Entry(pruebas)
        self.busqueda.grid(row=0, column=1, sticky="ew", padx=8)

        b_buscar = ttk.Button(
            pruebas,
            text="Buscar",
            command=self.buscar,
        )
        b_buscar.grid(row=0, column=2)

        b_recientes = ttk.Button(
            pruebas,
            text="Ver archivos recientes",
            command=self.recientes,
        )
        b_recientes.grid(
            row=1,
            column=0,
            columnspan=3,
            sticky="w",
            pady=(12, 0),
        )

        if not drive_ok:
            b_buscar.state(["disabled"])
            b_recientes.state(["disabled"])

        ttk.Label(
            pruebas,
            text=(
                "Solo nombre, tipo, fechas, padres y enlace web. "
                "No se descargan bytes del archivo."
            ),
        ).grid(row=2, column=0, columnspan=3, sticky="w", pady=(12, 0))

    def autorizar(self):
        try:
            info = autorizar_google_drive_metadata()
        except Exception as exc:
            messagebox.showerror("Google Drive", str(exc))
            return

        messagebox.showinfo(
            "Drive autorizado",
            (
                "Drive quedó autorizado en modo metadatos de solo lectura.\n\n"
                f"Cuenta: {info['email']}\n\n"
                "Calendar readonly fue conservado."
            ),
        )
        self.refrescar()

    def buscar(self):
        try:
            resultado = buscar_archivos(self.busqueda.get())
        except Exception as exc:
            messagebox.showerror("Drive — Buscar", str(exc))
            return

        messagebox.showinfo(
            "Drive — Buscar",
            _texto("Resultados de búsqueda", resultado),
        )

    def recientes(self):
        try:
            resultado = archivos_recientes(10)
        except Exception as exc:
            messagebox.showerror("Drive — Recientes", str(exc))
            return

        messagebox.showinfo(
            "Drive — Recientes",
            _texto("Archivos recientes", resultado),
        )

if __name__ == "__main__":
    CentroDriveRC23().mainloop()
