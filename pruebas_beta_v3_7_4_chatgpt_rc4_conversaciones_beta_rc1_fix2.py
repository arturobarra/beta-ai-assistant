from pathlib import Path
import ast
import hashlib
import subprocess
import textwrap
import re

BASE = Path(r"A:\Beta")
SRC = BASE / "beta_v3.7.4_CHATGPT_RC4_CONVERSACIONES_BETA_RC1_FIX1.py"
DST = BASE / "beta_v3.7.4_CHATGPT_RC4_CONVERSACIONES_BETA_RC1_FIX2.py"
TEST_RC1 = BASE / "pruebas_beta_v3_7_4_chatgpt_rc4_conversaciones_beta_rc1.py"
TEST_FIX1 = BASE / "pruebas_beta_v3_7_4_chatgpt_rc4_conversaciones_beta_rc1_fix1.py"

EXPECTED_HEAD = "c605ac5cb6a06b4f15462b04b603ca5e59daf11e"
EXPECTED_SRC_SHA = "4F4F3FA0D537877FCDBF6A61C906F7CAD540A55E6BE7AE3CA880AF5F338804EB"
EXPECTED_DST_SHA = "344B866CEA9BB7DE9069DA3ADAA49BA017D1C0218950047DB4B8CB032DE148AF"

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

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def git(*args):
    p = subprocess.run(
        ["git", "-C", str(BASE), *args],
        capture_output=True, text=True, errors="replace"
    )
    return p.stdout.strip()

def function_source(text, name):
    tree = ast.parse(text)
    nodes = [
        n for n in ast.walk(tree)
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
        and n.name == name
    ]
    if len(nodes) != 1:
        return ""
    n = nodes[0]
    lines = text.splitlines()
    return "\n".join(lines[n.lineno-1:n.end_lineno])

def run_old(path, marker, label):
    p = subprocess.run(
        ["py", "-3", str(path)],
        cwd=str(BASE),
        capture_output=True,
        text=True,
        errors="replace",
    )
    print(f"----- {label} -----")
    print((p.stdout or "").rstrip())
    if p.stderr.strip():
        print(p.stderr.rstrip())
    c(p.returncode == 0 and marker in p.stdout, label + " sigue correcta")

run_old(TEST_RC1, "RESULTADO: 41/41 pruebas correctas", "Batería base 41/41")
run_old(TEST_FIX1, "RESULTADO FIX1: 35/35 pruebas correctas", "Batería FIX1 35/35")

src = SRC.read_text(encoding="utf-8")
dst = DST.read_text(encoding="utf-8")
compile(dst, str(DST), "exec")

c(git("branch", "--show-current") == "beta-v3.7.4-chatgpt-rc1", "Rama correcta")
c(git("rev-parse", "HEAD") == EXPECTED_HEAD, "HEAD correcto")
c(not git("diff", "--cached", "--name-only"), "Sin staged")
c(sha(SRC) == EXPECTED_SRC_SHA, "FIX1 base intacta")
c(sha(DST) == EXPECTED_DST_SHA, "Candidata FIX2 exacta")

mem_src = function_source(dst, "es_mensaje_memorizable")
clear_src = function_source(dst, "_conversaciones_beta_limpiar_contexto_rc1")
prompt_src = function_source(dst, "construir_prompt_sistema")

c("t_pregunta = re.sub" in mem_src, "Normalización de conectores para preguntas presente")
c('"repite ", "repiteme "' in mem_src, "Repite/repíteme filtrados como consulta")
c("self.contexto_actualizado_ts = time.time()" in clear_src,
  "Nueva conversación marca contexto vacío como fresco")
c("self.contexto_actualizado_ts = 0.0" not in clear_src,
  "Nueva conversación ya no fuerza fallback global")
c("ultimo_resumen_conversacion()" in prompt_src,
  "Fallback legacy al iniciar Beta se preserva")

func = textwrap.dedent(mem_src)
class_code = "class Dummy:\n" + textwrap.indent(func, "    ")

def normalizar_min(s):
    tabla = str.maketrans("áéíóúüñÁÉÍÓÚÜÑ", "aeiouunAEIOUUN")
    return " ".join(str(s or "").translate(tabla).lower().split())

ns = {
    "normalizar": normalizar_min,
    "re": re,
    "MEMORIA_INTELIGENTE_MIN_PALABRAS": 4,
}
exec(class_code, ns)
d = ns["Dummy"]()
d.tutor_python_tema_actual = ""
d.es_dato_sensible_para_no_guardar = lambda x: False
d._atlas_normalizar_orden_operativa = lambda x: x
d._orq_normalizar_hardware_contextual = lambda x: x

no_mem = [
    "y cual era la decimo tercera que me mencionaste",
    "como se llamaba lo que me dijiste antes",
    "repiteme lo anterior por favor",
    "cual era el nombre que mencionaste",
    "que dijiste sobre eso anteriormente",
]
for frase in no_mem:
    c(not d.es_mensaje_memorizable(frase), f"No memoriza consulta: {frase}")

si_mem = [
    "y me gusta mucho el cafe por las mañanas",
    "pero mi objetivo es terminar este proyecto este mes",
    "entonces prefiero respuestas breves cuando estoy estudiando",
]
for frase in si_mem:
    c(d.es_mensaje_memorizable(frase), f"Conserva afirmación personal: {frase}")

c("CREATE TABLE IF NOT EXISTS conversaciones_beta (" in dst,
  "Conversaciones Beta preservada")
c("CREATE TABLE IF NOT EXISTS conversaciones_beta_mensajes (" in dst,
  "Mensajes Conversaciones Beta preservados")
c('"gmail_privado"' in dst and '"proyecto"' in dst,
  "Privacidad Gmail/proyecto preservada")
c("store=False" in dst and "stream=True" in dst,
  "ChatGPT mantiene store=false + stream=true")
c("CONTROL ATLAS RC1 FIX1: consulta conceptual de RAM" in dst,
  "FIX1 RAM preservado")
c('label="Conversaciones Beta..."' in dst,
  "Menú Conversaciones Beta preservado")

print()
print(f"RESULTADO FIX2: {ok}/{total} pruebas correctas")
raise SystemExit(0 if ok == total else 1)
