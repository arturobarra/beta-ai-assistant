# -*- coding: utf-8 -*-
from __future__ import annotations

import ctypes
from ctypes import wintypes
import hashlib
import json
import os
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

VERSION = "v3.7.4 Conexiones RC2 FIX1"
SCOPES_GOOGLE = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]
USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"
CRYPTPROTECT_UI_FORBIDDEN = 0x1


class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_byte))]


crypt32 = ctypes.WinDLL("crypt32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
crypt32.CryptProtectData.argtypes = [
    ctypes.POINTER(DATA_BLOB), wintypes.LPCWSTR, ctypes.POINTER(DATA_BLOB),
    ctypes.c_void_p, ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(DATA_BLOB),
]
crypt32.CryptProtectData.restype = wintypes.BOOL
crypt32.CryptUnprotectData.argtypes = [
    ctypes.POINTER(DATA_BLOB), ctypes.POINTER(wintypes.LPWSTR), ctypes.POINTER(DATA_BLOB),
    ctypes.c_void_p, ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(DATA_BLOB),
]
crypt32.CryptUnprotectData.restype = wintypes.BOOL
kernel32.LocalFree.argtypes = [wintypes.HLOCAL]
kernel32.LocalFree.restype = wintypes.HLOCAL


def _blob(data: bytes):
    raw = bytes(data)
    if not raw:
        raise ValueError("Dato vacío")
    buf = ctypes.create_string_buffer(raw, len(raw))
    return DATA_BLOB(len(raw), ctypes.cast(buf, ctypes.POINTER(ctypes.c_byte))), buf


def proteger_bytes(data: bytes, descripcion: str) -> bytes:
    entrada, _buf = _blob(data)
    salida = DATA_BLOB()
    ok = crypt32.CryptProtectData(
        ctypes.byref(entrada), descripcion, None, None, None,
        CRYPTPROTECT_UI_FORBIDDEN, ctypes.byref(salida),
    )
    if not ok:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        return ctypes.string_at(salida.pbData, salida.cbData)
    finally:
        if salida.pbData:
            kernel32.LocalFree(ctypes.cast(salida.pbData, wintypes.HLOCAL))


def desproteger_bytes(data: bytes) -> bytes:
    entrada, _buf = _blob(data)
    salida = DATA_BLOB()
    descripcion = wintypes.LPWSTR()
    ok = crypt32.CryptUnprotectData(
        ctypes.byref(entrada), ctypes.byref(descripcion), None, None, None,
        CRYPTPROTECT_UI_FORBIDDEN, ctypes.byref(salida),
    )
    if not ok:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        return ctypes.string_at(salida.pbData, salida.cbData)
    finally:
        if salida.pbData:
            kernel32.LocalFree(ctypes.cast(salida.pbData, wintypes.HLOCAL))
        if descripcion:
            kernel32.LocalFree(ctypes.cast(descripcion, wintypes.HLOCAL))


def raiz_conexiones() -> Path:
    raiz = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
    p = Path(raiz) / "Beta" / "Conexiones"
    p.mkdir(parents=True, exist_ok=True)
    return p


def carpeta_google() -> Path:
    p = raiz_conexiones() / "google"
    p.mkdir(parents=True, exist_ok=True)
    return p


def ruta_cliente_google() -> Path:
    return carpeta_google() / "cliente_oauth.dpapi"


def ruta_token_google() -> Path:
    return carpeta_google() / "token_oauth.dpapi"


def ruta_estado() -> Path:
    return raiz_conexiones() / "estado.json"


ESTADO_BASE = {
    "version": 2,
    "proveedores": {
        "google": {
            "credencial_importada": False,
            "conectado": False,
            "cuenta": None,
            "nombre": None,
            "sub": None,
            "permisos": [],
            "ultima_actualizacion": None,
        },
        "github": {
            "conectado": False,
            "cuenta": None,
            "permisos": [],
            "ultima_actualizacion": None,
        },
    },
}


def _base():
    return json.loads(json.dumps(ESTADO_BASE))


def cargar_estado():
    p = ruta_estado()
    if not p.exists():
        data = _base()
        guardar_estado(data)
        return data
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        data = _base()
    data.setdefault("version", 2)
    prov = data.setdefault("proveedores", {})
    for nombre, base in ESTADO_BASE["proveedores"].items():
        actual = prov.setdefault(nombre, {})
        for clave, valor in base.items():
            actual.setdefault(clave, valor)
    prov["google"]["credencial_importada"] = ruta_cliente_google().exists()
    prov["google"]["conectado"] = ruta_token_google().exists() and bool(prov["google"].get("cuenta"))
    return data


def guardar_estado(data):
    p = ruta_estado()
    tmp = p.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(p)


def guardar_cifrado(path: Path, texto: str, descripcion: str):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(proteger_bytes(texto.encode("utf-8"), descripcion))
    tmp.replace(path)


def leer_cifrado(path: Path) -> str:
    return desproteger_bytes(path.read_bytes()).decode("utf-8")


def validar_json_cliente(data):
    if not isinstance(data, dict) or "installed" not in data:
        raise ValueError("El JSON no corresponde a una Aplicación de escritorio de Google OAuth.")
    inst = data.get("installed")
    if not isinstance(inst, dict):
        raise ValueError("Sección 'installed' inválida.")
    faltan = [k for k in ("client_id", "auth_uri", "token_uri") if not inst.get(k)]
    if faltan:
        raise ValueError("Faltan campos OAuth: " + ", ".join(faltan))
    if not str(inst.get("client_id", "")).endswith(".apps.googleusercontent.com"):
        raise ValueError("client_id no parece ser de Google OAuth.")
    return True


def importar_json_google(path_origen):
    bruto = Path(path_origen).read_text(encoding="utf-8")
    data = json.loads(bruto)
    validar_json_cliente(data)
    guardar_cifrado(
        ruta_cliente_google(),
        json.dumps(data, ensure_ascii=False),
        "Beta Google OAuth Client",
    )
    estado = cargar_estado()
    g = estado["proveedores"]["google"]
    g["credencial_importada"] = True
    g["ultima_actualizacion"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    guardar_estado(estado)
    huella = hashlib.sha256(data["installed"]["client_id"].encode("utf-8")).hexdigest()[:12]
    return huella


def cargar_config_cliente_google():
    p = ruta_cliente_google()
    if not p.exists():
        raise FileNotFoundError("Primero importe el JSON OAuth de Beta Desktop.")
    data = json.loads(leer_cifrado(p))
    validar_json_cliente(data)
    return data


def dependencia_google_disponible():
    try:
        import google_auth_oauthlib.flow  # noqa
        return True
    except Exception:
        return False


def conectar_google():
    if not dependencia_google_disponible():
        raise RuntimeError(
            r"Falta google-auth-oauthlib. Ejecute A:\Beta\INSTALAR_DEPENDENCIAS_GOOGLE_RC2.bat"
        )
    from google_auth_oauthlib.flow import InstalledAppFlow

    config = cargar_config_cliente_google()
    flow = InstalledAppFlow.from_client_config(config, SCOPES_GOOGLE)
    cred = flow.run_local_server(
        host="127.0.0.1",
        port=0,
        open_browser=True,
        authorization_prompt_message="Beta abrió el navegador para autorizar Google.",
        success_message="Autorización completada. Puede cerrar esta pestaña y volver a Beta.",
        access_type="offline",
        prompt="consent",
    )
    if not cred or not cred.token:
        raise RuntimeError("Google no devolvió un token de acceso.")

    req = Request(USERINFO_URL, headers={"Authorization": f"Bearer {cred.token}"})
    try:
        with urlopen(req, timeout=15) as resp:
            perfil = json.loads(resp.read().decode("utf-8"))
    except (URLError, HTTPError) as exc:
        raise RuntimeError(f"No pude consultar la identidad Google: {exc}") from exc

    email = perfil.get("email")
    if not email:
        raise RuntimeError("Google autorizó la cuenta, pero no devolvió el correo.")

    guardar_cifrado(ruta_token_google(), cred.to_json(), "Beta Google OAuth Token")
    estado = cargar_estado()
    g = estado["proveedores"]["google"]
    g.update({
        "credencial_importada": True,
        "conectado": True,
        "cuenta": email,
        "nombre": perfil.get("name"),
        "sub": perfil.get("sub"),
        "permisos": list(SCOPES_GOOGLE),
        "ultima_actualizacion": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    })
    guardar_estado(estado)
    return email, perfil.get("name")


def desconectar_google_local():
    p = ruta_token_google()
    if p.exists():
        p.unlink()
    estado = cargar_estado()
    g = estado["proveedores"]["google"]
    g.update({
        "conectado": False,
        "cuenta": None,
        "nombre": None,
        "sub": None,
        "permisos": [],
        "ultima_actualizacion": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    })
    guardar_estado(estado)


class CentroRC2(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"Beta — Centro de Conexiones — {VERSION}")
        self.geometry("760x500")
        self.minsize(690, 450)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        cab = ttk.Frame(self, padding=(20, 18, 20, 10))
        cab.grid(row=0, column=0, sticky="ew")
        ttk.Label(cab, text="Centro de Conexiones de Beta", font=("Segoe UI", 18, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(
            cab,
            text="RC2: Google OAuth real. Solo identidad; Gmail, Drive y Calendar siguen sin permisos.",
        ).grid(row=1, column=0, sticky="w", pady=(6, 0))

        self.cuerpo = ttk.Frame(self, padding=(20, 8, 20, 12))
        self.cuerpo.grid(row=1, column=0, sticky="nsew")
        self.cuerpo.columnconfigure(0, weight=1)

        pie = ttk.Frame(self, padding=(20, 8, 20, 18))
        pie.grid(row=2, column=0, sticky="ew")
        ttk.Label(
            pie,
            text="Beta no pide contraseñas. El JSON y el token se guardan cifrados con Windows DPAPI.",
        ).grid(row=0, column=0, sticky="w")
        self.refrescar()

    def refrescar(self):
        for w in self.cuerpo.winfo_children():
            w.destroy()
        estado = cargar_estado()
        g = estado["proveedores"]["google"]

        google = ttk.LabelFrame(self.cuerpo, text="Google", padding=16)
        google.grid(row=0, column=0, sticky="ew", pady=8)
        google.columnconfigure(1, weight=1)
        ttk.Label(google, text="Conectado" if g.get("conectado") else "No conectado", font=("Segoe UI", 11, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(google, text=g.get("cuenta") or "Sin cuenta enrolada").grid(row=0, column=1, sticky="w", padx=(18, 8))
        ttk.Label(
            google,
            text="Credencial OAuth importada" if g.get("credencial_importada") else "Falta importar el JSON de Beta Desktop",
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(8, 0))
        ttk.Label(google, text="Permisos RC2 FIX1: openid · userinfo.email · userinfo.profile").grid(row=2, column=0, columnspan=2, sticky="w", pady=(8, 0))

        botones = ttk.Frame(google)
        botones.grid(row=0, column=2, rowspan=3, sticky="e")
        ttk.Button(botones, text="Importar JSON OAuth", command=self.importar_ui).grid(row=0, column=0, sticky="ew", pady=2)
        b = ttk.Button(botones, text="Conectar Google", command=self.conectar_ui)
        b.grid(row=1, column=0, sticky="ew", pady=2)
        if not g.get("credencial_importada"):
            b.state(["disabled"])
        if g.get("conectado"):
            ttk.Button(botones, text="Desconectar localmente", command=self.desconectar_ui).grid(row=2, column=0, sticky="ew", pady=2)

        github = ttk.LabelFrame(self.cuerpo, text="GitHub", padding=16)
        github.grid(row=1, column=0, sticky="ew", pady=8)
        github.columnconfigure(1, weight=1)
        ttk.Label(github, text="No conectado", font=("Segoe UI", 11, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(github, text="RC3: GitHub App con permisos mínimos por repositorio.").grid(row=0, column=1, sticky="w", padx=(18, 8))
        ttk.Button(github, text="Conectar GitHub (RC3)", state="disabled").grid(row=0, column=2, sticky="e")

    def importar_ui(self):
        archivo = filedialog.askopenfilename(
            title="Seleccione el JSON OAuth descargado de Beta Desktop",
            filetypes=[("JSON OAuth", "*.json"), ("Todos los archivos", "*.*")],
        )
        if not archivo:
            return
        try:
            huella = importar_json_google(archivo)
        except Exception as exc:
            messagebox.showerror("Google OAuth", str(exc))
            return
        messagebox.showinfo(
            "Google OAuth",
            "Credencial importada y cifrada correctamente.\n\nHuella client_id: " + huella,
        )
        self.refrescar()

    def conectar_ui(self):
        if not dependencia_google_disponible():
            messagebox.showwarning(
                "Dependencia Google",
                r"Ejecute A:\Beta\INSTALAR_DEPENDENCIAS_GOOGLE_RC2.bat y luego vuelva a abrir RC2.",
            )
            return
        try:
            email, nombre = conectar_google()
        except Exception as exc:
            messagebox.showerror("Conectar Google", str(exc))
            return
        messagebox.showinfo(
            "Google conectado",
            f"Beta quedó enrolada con Google.\n\nCuenta: {email}\nNombre: {nombre or '(no informado)'}\n\nRC2 solo tiene identidad básica.",
        )
        self.refrescar()

    def desconectar_ui(self):
        if not messagebox.askyesno(
            "Desconectar Google",
            "Esto borrará solo el token OAuth local cifrado.\n\n¿Continuar?",
        ):
            return
        try:
            desconectar_google_local()
        except Exception as exc:
            messagebox.showerror("Desconectar Google", str(exc))
            return
        self.refrescar()


if __name__ == "__main__":
    CentroRC2().mainloop()
