
from __future__ import annotations
import base64, ctypes, hashlib, json, os, queue, secrets, threading, time, uuid, webbrowser
from ctypes import wintypes
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse
import requests
import tkinter as tk
from tkinter import ttk, messagebox

APP_NAME = "Beta"
AUTH_URL = "https://auth.openai.com/api/accounts/authorize"
TOKEN_URL = "https://auth.openai.com/api/accounts/oauth/token"
JWKS_URL = "https://auth.openai.com/.well-known/jwks.json"
DISCOVERY_URL = "https://auth.openai.com/.well-known/openid-configuration"
ISSUER = "https://auth.openai.com"
RESOURCE = "https://api.openai.com/v1"
SCOPES = "openid profile email offline_access resource.invoke chatgpt.tokens.use.direct"
DYNAMIC_CLIENT = "dynamic_agent_client"
CALLBACK_PATH = "/auth/callback"
CRYPTPROTECT_UI_FORBIDDEN = 0x1

class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_byte))]

crypt32 = ctypes.WinDLL("crypt32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
crypt32.CryptProtectData.argtypes = [ctypes.POINTER(DATA_BLOB), wintypes.LPCWSTR, ctypes.POINTER(DATA_BLOB), ctypes.c_void_p, ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(DATA_BLOB)]
crypt32.CryptProtectData.restype = wintypes.BOOL
crypt32.CryptUnprotectData.argtypes = [ctypes.POINTER(DATA_BLOB), ctypes.POINTER(wintypes.LPWSTR), ctypes.POINTER(DATA_BLOB), ctypes.c_void_p, ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(DATA_BLOB)]
crypt32.CryptUnprotectData.restype = wintypes.BOOL
kernel32.LocalFree.argtypes = [wintypes.HLOCAL]

def _blob(data: bytes):
    b = ctypes.create_string_buffer(data)
    return DATA_BLOB(len(data), ctypes.cast(b, ctypes.POINTER(ctypes.c_byte))), b

def proteger(data: bytes, desc: str) -> bytes:
    entrada, _ = _blob(data); salida = DATA_BLOB()
    if not crypt32.CryptProtectData(ctypes.byref(entrada), desc, None, None, None, CRYPTPROTECT_UI_FORBIDDEN, ctypes.byref(salida)):
        raise ctypes.WinError(ctypes.get_last_error())
    try: return ctypes.string_at(salida.pbData, salida.cbData)
    finally:
        if salida.pbData: kernel32.LocalFree(ctypes.cast(salida.pbData, wintypes.HLOCAL))

def desproteger(data: bytes) -> bytes:
    entrada, _ = _blob(data); salida = DATA_BLOB(); desc = wintypes.LPWSTR()
    if not crypt32.CryptUnprotectData(ctypes.byref(entrada), ctypes.byref(desc), None, None, None, CRYPTPROTECT_UI_FORBIDDEN, ctypes.byref(salida)):
        raise ctypes.WinError(ctypes.get_last_error())
    try: return ctypes.string_at(salida.pbData, salida.cbData)
    finally:
        if salida.pbData: kernel32.LocalFree(ctypes.cast(salida.pbData, wintypes.HLOCAL))
        if desc: kernel32.LocalFree(ctypes.cast(desc, wintypes.HLOCAL))

def raiz():
    base = os.environ.get("LOCALAPPDATA") or str(Path.home()/"AppData"/"Local")
    p = Path(base)/"Beta"/"Conexiones"/"chatgpt"
    (p/"perfiles").mkdir(parents=True, exist_ok=True)
    return p

def _leer_json(p, defecto):
    try: return json.loads(p.read_text(encoding="utf-8"))
    except Exception: return defecto

def _guardar_json(p, data):
    tmp = p.with_suffix(p.suffix+".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, p)

def host_id():
    p = raiz()/"host.json"; d = _leer_json(p,{})
    h = str(d.get("ext_agent_host_id") or "")
    if not h.startswith("urn:uuid:"):
        h = "urn:uuid:"+str(uuid.uuid4())
        _guardar_json(p, {"ext_agent_host_id":h,"creado":datetime.now(timezone.utc).isoformat()})
    return h

def estado():
    p = raiz()/"estado.json"; d = _leer_json(p,{"perfil_activo":"","perfiles":{}})
    d.setdefault("perfil_activo",""); d.setdefault("perfiles",{})
    return d

def guardar_estado(d): _guardar_json(raiz()/"estado.json", d)
def ruta_cred(pid): return raiz()/"perfiles"/f"{pid}.dpapi"

def guardar_cred(pid, d):
    tmp = ruta_cred(pid).with_suffix(".tmp")
    tmp.write_bytes(proteger(json.dumps(d,ensure_ascii=False).encode(), f"Beta ChatGPT {pid}"))
    os.replace(tmp, ruta_cred(pid))

def cargar_cred(pid):
    p = ruta_cred(pid)
    if not p.exists(): return {}
    return json.loads(desproteger(p.read_bytes()).decode("utf-8"))

def b64u(b): return base64.urlsafe_b64encode(b).decode().rstrip("=")

def pkce():
    v=b64u(secrets.token_bytes(48))
    return v, b64u(hashlib.sha256(v.encode()).digest())

class Callback:
    def __init__(self): self.q=queue.Queue(1); self.server=None
    def iniciar(self):
        owner=self
        class H(BaseHTTPRequestHandler):
            def log_message(self,*a): pass
            def do_GET(self):
                u=urlparse(self.path)
                if u.path != CALLBACK_PATH: self.send_response(404); self.end_headers(); return
                data={k:v[-1] for k,v in parse_qs(u.query).items() if v}
                try: owner.q.put_nowait(data)
                except queue.Full: pass
                body=b"<html><body><h2>Beta</h2><p>Autorizacion recibida. Puede cerrar esta pestana.</p></body></html>"
                self.send_response(200); self.send_header("Content-Type","text/html; charset=utf-8"); self.send_header("Content-Length",str(len(body))); self.end_headers(); self.wfile.write(body)
        self.server=ThreadingHTTPServer(("127.0.0.1",0),H)
        port=self.server.server_address[1]
        threading.Thread(target=self.server.serve_forever,daemon=True).start()
        return f"http://127.0.0.1:{port}{CALLBACK_PATH}"
    def esperar(self):
        try: return self.q.get(timeout=240)
        finally: self.server.shutdown(); self.server.server_close()

def validar_id_token(token, client_id, nonce):
    try:
        import jwt
        from jwt import PyJWKClient
    except ImportError as e:
        raise RuntimeError("Falta PyJWT. Ejecute INSTALAR_DEPENDENCIAS_CHATGPT_RC1.bat.") from e
    key=PyJWKClient(JWKS_URL).get_signing_key_from_jwt(token).key
    claims=jwt.decode(token,key,algorithms=["RS256","ES256"],audience=client_id,issuer=ISSUER,options={"require":["exp","iss","sub"]},leeway=120)
    if str(claims.get("nonce") or "") != nonce: raise RuntimeError("Nonce OAuth invalido.")
    return claims

def scope_set(d):
    s=d.get("scope") or d.get("scopes") or ""
    return set(s if isinstance(s,list) else str(s).split())

def registrar(reusar_pid=None):
    e=estado(); h=host_id(); old={}; meta={}; cid=DYNAMIC_CLIENT
    if reusar_pid:
        meta=e["perfiles"].get(reusar_pid) or {}; old=cargar_cred(reusar_pid)
        cid=str(old.get("client_id") or meta.get("client_id") or "")
        if not cid: raise RuntimeError("Perfil guardado sin client_id.")
    cb=Callback(); redirect=cb.iniciar()
    st=secrets.token_urlsafe(32); nonce=secrets.token_urlsafe(32); verifier,challenge=pkce()
    p={"client_id":cid,"response_type":"code","redirect_uri":redirect,"scope":SCOPES,"resource":RESOURCE,"state":st,"nonce":nonce,"code_challenge_method":"S256","code_challenge":challenge,"ext_agent_host_id":h}
    if cid==DYNAMIC_CLIENT: p["agent_name_hint"]=APP_NAME
    else:
        if old.get("id_token"): p["id_token_hint"]=old["id_token"]
        if old.get("email") or meta.get("email"): p["login_hint"]=old.get("email") or meta.get("email")
    webbrowser.open(AUTH_URL+"?"+urlencode(p))
    r=cb.esperar()
    if r.get("state")!=st: raise RuntimeError("State OAuth invalido.")
    if r.get("error"): raise RuntimeError(r.get("error_description") or r["error"])
    code=str(r.get("code") or "")
    if not code: raise RuntimeError("Callback sin codigo.")
    issued=str(r.get("client_id") or "") if cid==DYNAMIC_CLIENT else cid
    if cid==DYNAMIC_CLIENT and (not issued or issued==DYNAMIC_CLIENT): raise RuntimeError("OpenAI no devolvio client_id emitido.")
    if cid!=DYNAMIC_CLIENT and r.get("client_id") and r["client_id"]!=cid: raise RuntimeError("client_id inesperado.")
    x=requests.post(TOKEN_URL,data={"grant_type":"authorization_code","client_id":issued,"code":code,"code_verifier":verifier,"redirect_uri":redirect,"resource":RESOURCE},timeout=25)
    if x.status_code>=400: raise RuntimeError(f"Intercambio OAuth {x.status_code}: {x.text[:500]}")
    td=x.json(); idt=str(td.get("id_token") or "")
    if not idt: raise RuntimeError("Sin ID token.")
    c=validar_id_token(idt,issued,nonce); sub=str(c.get("sub") or "")
    if reusar_pid:
        esperado=str(old.get("subject") or meta.get("subject") or "")
        if esperado and esperado!=sub: raise RuntimeError("La identidad no coincide con el perfil guardado.")
    pid=hashlib.sha256(f"{issued}|{sub}".encode()).hexdigest()[:20]
    scopes=scope_set(td)
    cred={"client_id":issued,"subject":sub,"email":str(c.get("email") or ""),"name":str(c.get("name") or ""),"ext_agent_host_id":h,"id_token":idt,"access_token":td.get("access_token"),"refresh_token":td.get("refresh_token"),"token_type":td.get("token_type","Bearer"),"expires_in":int(td.get("expires_in") or 0),"scope":td.get("scope",""),"scopes":sorted(scopes),"saved_at":datetime.now(timezone.utc).isoformat()}
    if not cred["access_token"]: raise RuntimeError("Sin access token.")
    guardar_cred(pid,cred)
    e=estado(); e["perfiles"][pid]={"client_id":issued,"subject":sub,"email":cred["email"],"name":cred["name"],"conectado":True,"plan_habilitado":"chatgpt.tokens.use.direct" in scopes}; e["perfil_activo"]=pid; guardar_estado(e)
    _depurar_duplicados(pid)
    e=estado()
    return pid,e["perfiles"][pid]

def expira_pronto(d):
    try:
        t=datetime.fromisoformat(d["saved_at"]); exp=int(d.get("expires_in") or 0)
        return time.time() >= t.timestamp()+exp-90
    except Exception: return True

def refrescar(pid):
    d=cargar_cred(pid)
    if not expira_pronto(d): return d
    if not d.get("refresh_token"): raise RuntimeError("La cuenta necesita reconectarse.")
    x=requests.post(TOKEN_URL,data={"grant_type":"refresh_token","client_id":d["client_id"],"refresh_token":d["refresh_token"],"resource":RESOURCE},timeout=25)
    if x.status_code>=400: raise RuntimeError(f"Refresh {x.status_code}: {x.text[:500]}")
    n=x.json()
    for k in ("access_token","refresh_token","id_token","token_type","expires_in","scope"):
        if n.get(k) is not None: d[k]=n[k]
    d["scopes"]=sorted(scope_set(n) or scope_set(d)); d["saved_at"]=datetime.now(timezone.utc).isoformat()
    guardar_cred(pid,d); return d

def seleccionar(pid):
    e=estado()
    if pid not in e["perfiles"]: raise RuntimeError("Perfil no encontrado.")
    d=cargar_cred(pid)
    if not d.get("access_token") and not d.get("refresh_token"): raise RuntimeError("Perfil desconectado.")
    e["perfil_activo"]=pid; guardar_estado(e)

def modelos(pid):
    d=refrescar(pid)
    if "chatgpt.tokens.use.direct" not in scope_set(d): raise RuntimeError("Uso del plan ChatGPT no habilitado.")
    x=requests.get(RESOURCE+"/models",headers={"Authorization":f"Bearer {d['access_token']}"},timeout=25)
    if x.status_code>=400: raise RuntimeError(f"Modelos {x.status_code}: {x.text[:500]}")
    o=x.json(); arr=o.get("models") if isinstance(o,dict) else None
    if arr is None and isinstance(o,dict): arr=o.get("data")
    out=[]
    for m in arr or []:
        if isinstance(m,dict) and m.get("visibility") in (None,"list"):
            slug=str(m.get("slug") or m.get("id") or "")
            if slug: out.append((slug,str(m.get("display_name") or slug)))
    return out

def probar(pid):
    from openai import OpenAI
    d=refrescar(pid); ms=modelos(pid)
    if not ms: raise RuntimeError("Sin modelos disponibles.")
    model=ms[0][0]; cli=OpenAI(api_key=d["access_token"],base_url=RESOURCE,max_retries=0)
    partes=[]; completed=False; t0=time.perf_counter()
    with cli.responses.create(model=model,input=[{"role":"user","content":"Responde unicamente: conexion correcta"}],store=False,stream=True) as s:
        for ev in s:
            if ev.type=="response.output_text.delta": partes.append(ev.delta or "")
            elif ev.type=="response.failed": raise RuntimeError("Responses API fallo.")
            elif ev.type=="response.completed": completed=True
    if not completed: raise RuntimeError("Stream sin response.completed.")
    return model,"".join(partes).strip(),time.perf_counter()-t0

def desconectar(pid):
    e=estado(); m=e["perfiles"].get(pid) or {}; d=cargar_cred(pid); remoto="no confirmado"
    if d.get("refresh_token") and d.get("client_id"):
        try:
            cfg=requests.get(DISCOVERY_URL,timeout=15).json(); ep=str(cfg.get("revocation_endpoint") or "")
            if ep:
                rr=requests.post(ep,data={"token":d["refresh_token"],"token_type_hint":"refresh_token","client_id":d["client_id"]},timeout=15)
                remoto="confirmado" if rr.status_code==200 else f"HTTP {rr.status_code}"
        except Exception: pass
    for k in ("access_token","refresh_token","id_token","expires_in","scope","scopes","saved_at","token_type"): d.pop(k,None)
    guardar_cred(pid,d); m["conectado"]=False; m["plan_habilitado"]=False; e["perfiles"][pid]=m
    if e.get("perfil_activo")==pid: e["perfil_activo"]=""
    guardar_estado(e); return remoto

def _misma_identidad(a, b):
    ea = str((a or {}).get("email") or "").strip().casefold()
    eb = str((b or {}).get("email") or "").strip().casefold()
    if ea and eb:
        return ea == eb
    sa = str((a or {}).get("subject") or "").strip()
    sb = str((b or {}).get("subject") or "").strip()
    return bool(sa and sb and sa == sb)


def _elegir_perfil_activo(perfiles):
    items = sorted(
        (perfiles or {}).items(),
        key=lambda kv: str((kv[1] or {}).get("email") or kv[0]).casefold(),
    )
    for pid, meta in items:
        if (meta or {}).get("conectado") and (meta or {}).get("plan_habilitado"):
            return pid
    for pid, meta in items:
        if (meta or {}).get("conectado"):
            return pid
    return ""


def eliminar_perfil(pid, revocar=True):
    e = estado()
    if pid not in e["perfiles"]:
        raise RuntimeError("Perfil no encontrado.")

    remoto = "no solicitado"
    if revocar:
        try:
            remoto = desconectar(pid)
        except Exception:
            remoto = "no confirmado"

    p = ruta_cred(pid)
    try:
        if p.exists():
            p.unlink()
    except Exception as ex:
        raise RuntimeError(f"No pude eliminar las credenciales locales del perfil: {ex}")

    e = estado()
    e["perfiles"].pop(pid, None)
    if e.get("perfil_activo") == pid or e.get("perfil_activo") not in e["perfiles"]:
        e["perfil_activo"] = _elegir_perfil_activo(e["perfiles"])
    guardar_estado(e)
    return remoto


def _depurar_duplicados(pid_nuevo):
    e = estado()
    nuevo = e["perfiles"].get(pid_nuevo) or {}
    duplicados = [
        pid
        for pid, meta in list(e["perfiles"].items())
        if pid != pid_nuevo and _misma_identidad(nuevo, meta)
    ]

    for pid in duplicados:
        try:
            eliminar_perfil(pid, revocar=False)
        except Exception as ex:
            print(
                "CHATGPT OAUTH RC2: no pude retirar perfil duplicado:",
                type(ex).__name__,
            )

    e = estado()
    if pid_nuevo in e["perfiles"]:
        e["perfil_activo"] = pid_nuevo
        guardar_estado(e)
    return duplicados


class App(tk.Tk):
    def __init__(self):
        super().__init__(); self.title("Beta — ChatGPT RC1"); self.geometry("820x560"); self.minsize(760,500)
        self.columnconfigure(0,weight=1); self.rowconfigure(1,weight=1)
        h=ttk.Frame(self,padding=18); h.grid(row=0,column=0,sticky="ew")
        ttk.Label(h,text="ChatGPT en Beta",font=("Segoe UI",18,"bold")).pack(anchor="w")
        ttk.Label(h,text="OAuth, varias cuentas y credenciales cifradas con Windows DPAPI. Beta no pide contrasena ni API key.").pack(anchor="w",pady=(5,0))
        self.body=ttk.Frame(self,padding=(18,5,18,10)); self.body.grid(row=1,column=0,sticky="nsew"); self.body.columnconfigure(0,weight=1)
        self.msg=tk.StringVar(value="Listo."); ttk.Label(self,textvariable=self.msg,padding=18).grid(row=2,column=0,sticky="w")
        self.render()

    def job(self,fn,ok=None):
        def run():
            try:r=fn()
            except Exception as ex:self.after(0,lambda e=str(ex):messagebox.showerror("ChatGPT",e)); return
            if ok:self.after(0,lambda:ok(r))
            self.after(0,self.render)
        threading.Thread(target=run,daemon=True).start()

    def nueva(self): self.msg.set("Abriendo ChatGPT en el navegador..."); self.job(lambda:registrar(),lambda r:messagebox.showinfo("ChatGPT","Cuenta conectada." if r[1].get("plan_habilitado") else "Cuenta conectada, pero el uso del plan no fue concedido."))
    def recon(self,pid): self.job(lambda:registrar(pid),lambda r:messagebox.showinfo("ChatGPT","Cuenta reconectada."))
    def usar(self,pid):
        try: seleccionar(pid); self.msg.set("Cuenta activa cambiada."); self.render()
        except Exception as ex: messagebox.showerror("ChatGPT",str(ex))
    def test(self,pid): self.msg.set("Probando ChatGPT..."); self.job(lambda:probar(pid),lambda r:messagebox.showinfo("Prueba",f"Modelo: {r[0]}\nRespuesta: {r[1]}\nLatencia: {r[2]:.2f} s"))
    def off(self,pid):
        if messagebox.askyesno("Desconectar","Se borraran los tokens locales, pero se conservara el perfil para reconectarlo facilmente."):
            self.job(lambda:desconectar(pid),lambda r:messagebox.showinfo("ChatGPT",f"Desconectado. Revocacion remota: {r}"))

    def render(self):
        for w in self.body.winfo_children(): w.destroy()
        e=estado(); activo=e.get("perfil_activo","")
        ttk.Button(self.body,text="Continuar con ChatGPT / Agregar otra cuenta",command=self.nueva).grid(row=0,column=0,sticky="w",pady=(0,12))
        row=1
        for pid,m in sorted(e["perfiles"].items(),key=lambda kv:(kv[1].get("email") or kv[0]).lower()):
            f=ttk.LabelFrame(self.body,padding=10); f.grid(row=row,column=0,sticky="ew",pady=5); f.columnconfigure(0,weight=1)
            titulo=m.get("name") or m.get("email") or f"Cuenta {pid[:8]}"
            ttk.Label(f,text=titulo+("  • ACTIVA" if pid==activo else ""),font=("Segoe UI",11,"bold")).grid(row=0,column=0,sticky="w")
            if m.get("email") and m.get("email")!=titulo: ttk.Label(f,text=m["email"]).grid(row=1,column=0,sticky="w")
            est="Conectada" if m.get("conectado") else "Desconectada"
            if m.get("conectado"): est += " • plan habilitado" if m.get("plan_habilitado") else " • solo identidad"
            ttk.Label(f,text=est).grid(row=2,column=0,sticky="w",pady=(3,7))
            b=ttk.Frame(f); b.grid(row=3,column=0,sticky="w")
            if m.get("conectado"):
                ttk.Button(b,text="Usar esta cuenta",command=lambda p=pid:self.usar(p)).pack(side="left",padx=(0,5))
                if m.get("plan_habilitado"): ttk.Button(b,text="Probar ChatGPT",command=lambda p=pid:self.test(p)).pack(side="left",padx=(0,5))
                ttk.Button(b,text="Reconectar",command=lambda p=pid:self.recon(p)).pack(side="left",padx=(0,5))
                ttk.Button(b,text="Desconectar",command=lambda p=pid:self.off(p)).pack(side="left")
            else: ttk.Button(b,text="Reconectar",command=lambda p=pid:self.recon(p)).pack(side="left")
            row+=1

if __name__=="__main__":
    host_id()
    App().mainloop()
