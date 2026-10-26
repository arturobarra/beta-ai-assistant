from pathlib import Path
import ast, hashlib, re

BASE = Path(r"A:\Beta")
SRC = BASE / "beta_v3.7.4_CHATGPT_RC4_CONVERSACIONES_BETA_RC1_FIX13_MEMORIA_JSON.py"
DST = BASE / "beta_v3.7.4_CHATGPT_RC4_CONVERSACIONES_BETA_RC1_FIX14_MEMORIA_RELEVANCIA.py"

EXPECTED_SRC_SHA = "FA748A764B73DF10B4C78E5E0497713AAE10E1E4311EEE11E025185823C7DCE5"
EXPECTED_DST_SHA = "C35B2965B27DAAF13A65F1FA2E6B29E407112F7C83CFF4C3039CC65821D481E1"

ok = 0
total = 0

def c(cond, name):
    global ok, total
    total += 1
    if cond:
        ok += 1
        print("[OK]", name)
    else:
        print("[FALLO]", name)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest().upper()

c(sha(SRC) == EXPECTED_SRC_SHA, "FIX13 base intacta")
c(sha(DST) == EXPECTED_DST_SHA, "FIX14 exacta")

txt = DST.read_text(encoding="utf-8")
tree = ast.parse(txt)
compile(txt, str(DST), "exec")
c(True, "Sintaxis FIX14 válida")

# Verificar que el stopword 'en' quedó dentro de buscar_recuerdos y no como cambio global accidental.
funcs = {n.name: n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
buscar = funcs.get("buscar_recuerdos")
c(buscar is not None, "Existe buscar_recuerdos")

if buscar is not None:
    src_lines = txt.splitlines()
    body = "\n".join(src_lines[buscar.lineno-1:buscar.end_lineno])
    c('"a", "en", "por"' in body, "'en' ignorado en búsqueda de recuerdos")
else:
    c(False, "'en' ignorado en búsqueda de recuerdos")

# Simulación del scoring observado en runtime.
def normalizar(s):
    s = str(s or "").lower()
    s = (
        s.replace("á","a").replace("é","e").replace("í","i")
         .replace("ó","o").replace("ú","u").replace("ü","u").replace("ñ","n")
    )
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()

ignoradas = {
    "que", "como", "cual", "quien", "cuando", "donde", "sobre",
    "sabes", "recuerdas", "recuerdo", "de", "del", "la", "el",
    "los", "las", "un", "una", "mi", "mis", "es", "son", "y",
    "a", "en", "por", "para", "me", "te", "tu", "tus", "lo", "se",
    "tengo", "tenemos", "pendiente", "pendientes",
}

consulta = normalizar("que recuerdas sobre mis gustos en motocicletas")
tokens = set(consulta.split()) - ignoradas
c(tokens == {"gustos", "motocicletas"}, "Consulta elimina stopword 'en'")

target = normalizar("El Señor me gustaria especialmente el estilo caferacer en las motocicletas clasicas")
irrelevante = normalizar("El Señor tiene un encuentro con Rafael el día 17 de octubre en el hospital La Florida")

def score(texto, etiquetas="", importancia=3):
    palabras = set(texto.split())
    tags = set((etiquetas or "").split(","))
    s = len(tokens & palabras) * 2 + len(tokens & tags) * 2
    if consulta and consulta in texto:
        s += 6
    if s > 0:
        s += min(3, int(importancia or 1))
    return s

c(score(target, "senor,gustaria,especialmente,estilo,caferacer,motocicletas,clasicas", 3) > 0,
  "Recuerdo de motocicletas sigue siendo relevante")
c(score(irrelevante, "", 3) == 0,
  "Recuerdo médico ya no entra por la preposición 'en'")

# Regresiones clave.
for marker, label in [
    ("formato_json=True", "FIX13 memoria JSON preservado"),
    ("beta_google_calendar_escritura_fix9", "Google FIX9 preservado"),
    ("agenda_aclaracion_pendiente", "Agenda FIX10 preservada"),
    ("_atlas_clasificar_referencia_eliminar", "Atlas FIX12 preservado"),
    ("beta_google_drive_voz_rc2_4_3", "Drive preservado"),
    ('"gmail_privado"', "Privacidad Gmail preservada"),
    ("continua con spotify", "Spotify preservado"),
    ("store=False", "ChatGPT store:false preservado"),
    ("conversaciones_beta_mensajes", "Conversaciones Beta preservadas"),
]:
    c(marker in txt, label)

print()
print(f"RESULTADO FIX14 MEMORIA RELEVANCIA: {ok}/{total} pruebas correctas")
raise SystemExit(0 if ok == total else 1)
