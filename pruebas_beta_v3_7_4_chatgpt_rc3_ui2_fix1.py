from pathlib import Path
import ast
import hashlib
import subprocess

BASE=Path(r"A:\Beta")
UI=BASE/"beta_v3.7.4_CHATGPT_RC3_UI2_FIX1.py"
OAUTH=BASE/"beta_chatgpt_oauth_rc2_fix1.py"
UI2=BASE/"beta_v3.7.4_CHATGPT_RC3_UI2.py"
OAUTH2=BASE/"beta_chatgpt_oauth_rc2.py"
OAUTH1=BASE/"beta_chatgpt_oauth_rc1.py"
STABLE=BASE/"beta.py"

HEAD="8d2342e8962048c4d32c90365ecaec4c2af5350a"
SHA_UI="4EACDCDD3568FD5F50C4B2887A38227AC590CA857387C436C10FA171A9380456"
SHA_OAUTH="1666AEAD3ADDAB026B6FDC23B949852E1D44719D8EDB2581E1DE7377236A8516"
SHA_UI2="29B522D50B685CC98F747EA0D88B6A2333D51EB0DC62EE206253C6A4BED90BB2"
SHA_OAUTH2="A2BDD9A3B1B52832ABF3DDCE548AD21F44CB99C15AC3E23D4D42ACD9E336C08E"
SHA_OAUTH1="C042FE0AB2ECCCB4AA36D5ED153C8AB04BD29C4A1FA0A6A795C19ADFDA8AEABF"
SHA_STABLE="774944526963A3D7EA1E5795CF4839C333CCDF1FD2A7872C1DB02514D1EE0C65"

ok=0
total=0

def c(cond,n):
    global ok,total
    total+=1
    if cond:
        ok+=1
        print("[OK]",n)
    else:
        print("[FALLO]",n)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest().upper()

def git(*args):
    p=subprocess.run(["git","-C",str(BASE),*args],capture_output=True,text=True,errors="replace")
    return p.stdout.strip()

def bloque(text,nombre):
    tree=ast.parse(text)
    ns=[n for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name==nombre]
    if len(ns)!=1:
        return ""
    n=ns[0]
    ls=text.splitlines()
    return "\n".join(ls[n.lineno-1:n.end_lineno])

ui=UI.read_text(encoding="utf-8")
oauth=OAUTH.read_text(encoding="utf-8")
compile(ui,str(UI),"exec")
compile(oauth,str(OAUTH),"exec")

estado=bloque(ui,"_chatgpt_estado_rc2")
admin=bloque(ui,"abrir_chatgpt_cuentas_rc2")
dedup=bloque(oauth,"_depurar_duplicados")
elim=bloque(oauth,"eliminar_perfil")

c(git("branch","--show-current")=="beta-v3.7.4-chatgpt-rc1","Rama correcta")
c(git("rev-parse","HEAD")==HEAD,"HEAD correcto")
c(not git("diff","--cached","--name-only"),"Sin staged")
c(sha(STABLE)==SHA_STABLE,"beta.py estable intacto")
c(sha(OAUTH1)==SHA_OAUTH1,"OAuth RC1 intacto")
c(sha(UI2)==SHA_UI2,"RC3 UI2 base intacta")
c(sha(OAUTH2)==SHA_OAUTH2,"OAuth RC2 base intacto")
c(sha(UI)==SHA_UI,"RC3 UI2 FIX1 exacta")
c(sha(OAUTH)==SHA_OAUTH,"OAuth RC2 FIX1 exacto")

c("import beta_chatgpt_oauth_rc1 as chatgpt_oauth" in estado,
  "Cerebro general sigue usando OAuth RC1")
c("beta_chatgpt_oauth_rc2" not in estado,
  "Cerebro general no fue migrado accidentalmente")
c("import beta_chatgpt_oauth_rc2_fix1 as chatgpt_oauth" in admin,
  "Administrador integrado usa OAuth RC2 FIX1")
c("beta_chatgpt_oauth_rc1 as chatgpt_oauth" not in admin,
  "Administrador ya no usa OAuth RC1")
c("chatgpt_oauth.eliminar_perfil" in admin,
  "Eliminar cuenta llama API disponible")
c('text="Eliminar cuenta"' in admin,
  "Botón Eliminar cuenta preservado")
c("chatgpt_oauth.desconectar" in admin,"Desconectar preservado")
c("chatgpt_oauth.registrar()" in admin,"Agregar cuenta preservado")
c("chatgpt_oauth.registrar(p)" in admin,"Reconectar preservado")
c("chatgpt_oauth.seleccionar(pid)" in admin,"Cambiar cuenta preservado")
c("chatgpt_oauth.probar(p)" in admin,"Probar ChatGPT preservado")

c("eliminar_perfil(pid, revocar=False)" in dedup,
  "Deduplicación automática no revoca perfil viejo")
c("eliminar_perfil(pid, revocar=True)" not in dedup,
  "Deduplicación automática evita revocación remota")
c("p.unlink()" in elim,"Eliminación manual borra credencial local")
c("revocar=True" in elim,"Eliminación manual conserva revocación")

c("store=False" in ui and "stream=True" in ui,"Responses store=false + stream=true")
c("self._chatgpt_rc2_candidata_biblioteca_rapida(original)" in ui,"FIX2 preservado")
c("ACADEMICO_TOKENS_BREVE = 120" in ui,"ACAD1 preservado")
c("self.conversar_chatgpt_async(original)" in ui,"ChatGPT general preservado")
c("self.conversar_ollama_async(pregunta)" in ui,"Ollama respaldo preservado")
c('"gmail_privado"' in ui,"Privacidad Gmail preservada")
c("self._google_gmail_manejar_voz_rc2_6" in ui,"Gmail directo preservado")
c("self._google_drive_manejar_voz_rc2_4" in ui,"Drive directo preservado")
c("self._google_calendar_manejar_voz_rc2_2" in ui,"Calendar directo preservado")
c("client_secret" not in oauth,"OAuth FIX1 sigue sin client_secret")

print()
print(f"RESULTADO: {ok}/{total} pruebas correctas")
raise SystemExit(0 if ok==total else 1)
