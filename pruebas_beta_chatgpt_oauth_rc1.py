
from pathlib import Path
import hashlib, subprocess
BASE=Path(r"A:\Beta"); MOD=BASE/"beta_chatgpt_oauth_rc1.py"; ST=BASE/"beta.py"
HEAD="5293daa3d2cb226d836256a0953e2495a2d5750b"
SHA="774944526963A3D7EA1E5795CF4839C333CCDF1FD2A7872C1DB02514D1EE0C65"
ok=0; total=0
def c(x,n):
    global ok,total; total+=1
    if x: ok+=1; print("[OK]",n)
    else: print("[FALLO]",n)
txt=MOD.read_text(encoding="utf-8")
compile(txt,str(MOD),"exec")
head=subprocess.run(["git","-C",str(BASE),"rev-parse","HEAD"],capture_output=True,text=True).stdout.strip()
staged=subprocess.run(["git","-C",str(BASE),"diff","--cached","--name-only"],capture_output=True,text=True).stdout.strip()
c(head==HEAD,"HEAD v3.7.4 FIX3 intacto")
c(hashlib.sha256(ST.read_bytes()).hexdigest().upper()==SHA,"beta.py estable intacto")
c(not staged,"Sin staged")
c("dynamic_agent_client" in txt,"dynamic_agent_client")
c("ext_agent_host_id" in txt,"host ID")
c("127.0.0.1" in txt and "/auth/callback" in txt,"callback loopback")
c("code_challenge_method" in txt and "S256" in txt,"PKCE S256")
c("chatgpt.tokens.use.direct" in txt and "resource.invoke" in txt,"scopes plan ChatGPT")
c("PyJWKClient" in txt and "audience=client_id" in txt and "issuer=ISSUER" in txt,"validacion ID token")
c("CryptProtectData" in txt and "CryptUnprotectData" in txt,"DPAPI")
c('"Beta"/"Conexiones"/"chatgpt"' in txt,"almacen fuera de A:\\Beta")
c("perfil_activo" in txt and "perfiles" in txt,"multi-cuenta")
c('grant_type":"refresh_token"' in txt,"refresh token")
c("revocation_endpoint" in txt,"revocacion")
c("store=False" in txt and "stream=True" in txt,"Responses store false + stream")
c("response.completed" in txt,"stream completado")
c("guardar_conversacion" not in txt,"RC1 no toca beta.db")
print(f"\nRESULTADO: {ok}/{total} pruebas correctas")
raise SystemExit(0 if ok==total else 1)
