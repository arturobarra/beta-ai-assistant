from pathlib import Path
import hashlib
import importlib.util
import py_compile
import subprocess
import sys

try:
    sys.stdout.reconfigure(errors="replace")
    sys.stderr.reconfigure(errors="replace")
except Exception:
    pass


BASE = Path(r"A:\Beta")
HEAD = "ea9e39529fcb52e0001e812629eff9be53a63ea9"
SHA_STABLE = "774944526963A3D7EA1E5795CF4839C333CCDF1FD2A7872C1DB02514D1EE0C65"

STABLE = BASE / "beta.py"
NEW_CAND = BASE / "beta_v3.7.4_conexiones_RC2_6_FIX3.py"
NEW_CAL = BASE / "beta_google_calendar_voz_rc2_2_fix1.py"
OLD_TEST = BASE / "pruebas_beta_v3_7_4_conexiones_rc2_6_fix2.py"

checks = 0
fails = 0

def ok(cond, nombre):
    global checks, fails
    checks += 1
    if cond:
        print("[OK]", nombre)
    else:
        fails += 1
        print("[FALLO]", nombre)

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def git(*args):
    p = subprocess.run(
        ["git", "-C", str(BASE), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return p.returncode, p.stdout.strip(), p.stderr.strip()

try:
    py_compile.compile(str(NEW_CAL), doraise=True)
    ok(True, "Calendar FIX1 compila")
except Exception as e:
    print(e)
    ok(False, "Calendar FIX1 compila")

try:
    py_compile.compile(str(NEW_CAND), doraise=True)
    ok(True, "Candidata FIX3 compila")
except Exception as e:
    print(e)
    ok(False, "Candidata FIX3 compila")

rc, head, _ = git("rev-parse", "HEAD")
ok(rc == 0 and head == HEAD, "HEAD v3.7.3 intacto")
ok(STABLE.exists() and sha256(STABLE) == SHA_STABLE, "SHA beta.py intacto")

p = subprocess.run(
    [sys.executable, str(OLD_TEST)],
    cwd=str(BASE),
    capture_output=True,
    text=True,
    encoding="utf-8",
    errors="replace",
)
print(p.stdout.rstrip())
if p.stderr.strip():
    print(p.stderr.rstrip())
ok(p.returncode == 0, "Regresión RC2.6 FIX2 original")

spec = importlib.util.spec_from_file_location("calendar_fix1_test", NEW_CAL)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

casos = [
    ("Beta, dime mis próximos eventos.", "proximo"),
    ("dime mis próximos eventos", "proximo"),
    ("Beta, cuáles son mis próximos eventos", "proximo"),
    ("Beta, dime mi próximo evento", "proximo"),
    ("Beta, cuál es mi próximo evento", "proximo"),
    ("Beta, qué tengo mañana", "manana"),
]

for frase, esperado in casos:
    obtenido = mod.clasificar_consulta(frase)
    ok(obtenido == esperado, f"Clasifica {frase!r} -> {esperado}")

for frase in [
    "Beta, dime mis correos recientes",
    "Beta, busca certificado.pdf en Drive",
    "Beta, abre WhatsApp",
]:
    ok(mod.clasificar_consulta(frase) is None, f"Calendar no invade: {frase!r}")

texto = NEW_CAND.read_text(encoding="utf-8", errors="replace")
ok("import beta_google_calendar_voz_rc2_2_fix1 as calendar_voz" in texto, "Import Calendar FIX1")
ok("GOOGLE CALENDAR v3.7.4 RC2.2 FIX1:" in texto, "Log Calendar FIX1")
ok("PRIVACIDAD GMAIL RC2.6 FIX2" in texto, "Privacidad Gmail permanece")
ok("_google_drive_manejar_voz_rc2_4" in texto, "Drive permanece")
ok("_google_gmail_manejar_voz_rc2_6" in texto, "Gmail permanece")
ok("CONTROL ATLAS" in texto, "Control Atlas permanece")

print()
print(f"RESULTADO: {checks - fails}/{checks} pruebas correctas")
if fails:
    raise SystemExit(1)

print("Beta v3.7.4 RC2.6 FIX3: Calendar 'próximos eventos' validado estáticamente.")
