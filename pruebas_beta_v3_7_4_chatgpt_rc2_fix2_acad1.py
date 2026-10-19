from pathlib import Path
import hashlib
import subprocess

BASE=Path(r"A:\Beta")
FIX2=BASE/"beta_v3.7.4_CHATGPT_RC2_FIX2.py"
ACAD1=BASE/"beta_v3.7.4_CHATGPT_RC2_FIX2_ACAD1.py"
OAUTH=BASE/"beta_chatgpt_oauth_rc1.py"
ST=BASE/"beta.py"

HEAD="5293daa3d2cb226d836256a0953e2495a2d5750b"
SHA_ST="774944526963A3D7EA1E5795CF4839C333CCDF1FD2A7872C1DB02514D1EE0C65"
SHA_FIX2="61F5E5779D7FDDBA963F048ED92B5ECD1DCF7D47FBA563AAB262894B0EA6D5CF"
SHA_ACAD1="AF17531B446B281B944F7AEFD4B8FACE014E2B6C6226B51EB54D098903693FB5"
SHA_OAUTH="C042FE0AB2ECCCB4AA36D5ED153C8AB04BD29C4A1FA0A6A795C19ADFDA8AEABF"

ok=0
total=0

def c(cond,nombre):
    global ok,total
    total+=1
    if cond:
        ok+=1
        print("[OK]",nombre)
    else:
        print("[FALLO]",nombre)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest().upper()

txt=ACAD1.read_text(encoding="utf-8")
base=FIX2.read_text(encoding="utf-8")
compile(txt,str(ACAD1),"exec")

head=subprocess.run(
    ["git","-C",str(BASE),"rev-parse","HEAD"],
    capture_output=True,text=True,errors="replace"
).stdout.strip()
staged=subprocess.run(
    ["git","-C",str(BASE),"diff","--cached","--name-only"],
    capture_output=True,text=True,errors="replace"
).stdout.strip()

c(head==HEAD,"HEAD respaldo FIX3 Google intacto")
c(sha(ST)==SHA_ST,"beta.py estable intacto")
c(sha(FIX2)==SHA_FIX2,"FIX2 base intacta")
c(sha(ACAD1)==SHA_ACAD1,"ACAD1 sin cambios inesperados")
c(sha(OAUTH)==SHA_OAUTH,"OAuth RC1 intacto")
c(not staged,"Sin staged")

c("ACADEMICO_TOKENS_BREVE = 120" in txt,"Límite académico breve ampliado a 120")
c("ACADEMICO_TOKENS_BREVE = 72" not in txt,"Límite antiguo 72 reemplazado")
c("ACADEMICO_TOKENS_PROFUNDO = 210" in txt,"Modo profundo intacto")
c("STREAMING_DESCARTAR_COLA_INCOMPLETA = True" in txt,"Cierre seguro intacto")
c("STREAMING_CORTE_INTERMEDIO = False" in txt,"Corte intermedio sigue desactivado")
c("Modo breve: responde directamente en 1 a 3 frases y unas 40 a 55 palabras." in txt,"Prompt académico breve intacto")
c("Termina siempre una oración completa" in txt,"Instrucción de cierre intacta")
c("self.generar_y_hablar_ollama_streaming" in txt,"Streaming Ollama académico intacto")
c("self._chatgpt_rc2_candidata_biblioteca_rapida(original)" in txt,"FIX2 router rápido intacto")
c("self.conversar_chatgpt_async(original)" in txt,"ChatGPT general intacto")
c("self.conversar_ollama_async(pregunta)" in txt,"Ollama respaldo intacto")
c("self._google_gmail_manejar_voz_rc2_6" in txt,"Gmail directo intacto")
c("self._google_drive_manejar_voz_rc2_4" in txt,"Drive directo intacto")
c("self._google_calendar_manejar_voz_rc2_2" in txt,"Calendar directo intacto")
c('"gmail_privado"' in txt,"Privacidad Gmail intacta")
c("store=False" in txt and "stream=True" in txt,"Responses store=false + stream=true")

# Confirmación de parche mínimo: sólo cambia la constante objetivo.
esperado = base.replace("ACADEMICO_TOKENS_BREVE = 72","ACADEMICO_TOKENS_BREVE = 120",1)
c(txt==esperado,"Parche mínimo: sólo cambió ACADEMICO_TOKENS_BREVE")

print()
print(f"RESULTADO: {ok}/{total} pruebas correctas")
raise SystemExit(0 if ok==total else 1)
