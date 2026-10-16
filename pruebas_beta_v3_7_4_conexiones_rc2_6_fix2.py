# -*- coding: utf-8 -*-
from pathlib import Path
import ast
import hashlib
import py_compile
import subprocess
import sys

BASE = Path(r"A:\Beta")
HEAD = "ea9e39529fcb52e0001e812629eff9be53a63ea9"
SHA = "774944526963A3D7EA1E5795CF4839C333CCDF1FD2A7872C1DB02514D1EE0C65"

stable = BASE / "beta.py"
cand = BASE / "beta_v3.7.4_conexiones_RC2_6_FIX2.py"
gmail_mod = BASE / "beta_google_gmail_voz_rc2_6_fix1.py"

pruebas = []

def ok(nombre, cond):
    pruebas.append((nombre, bool(cond)))

def git(*args):
    p = subprocess.run(
        ["git", "-C", str(BASE), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return p.returncode, p.stdout.strip()

for p in (cand, gmail_mod):
    try:
        py_compile.compile(str(p), doraise=True)
        ok(f"{p.name} compila", True)
    except Exception:
        ok(f"{p.name} compila", False)

rc, head = git("rev-parse", "HEAD")
ok("HEAD v3.7.3 intacto", rc == 0 and head == HEAD)
ok(
    "SHA beta.py intacto",
    hashlib.sha256(stable.read_bytes()).hexdigest().upper() == SHA,
)

ct = cand.read_text(encoding="utf-8")
mt = gmail_mod.read_text(encoding="utf-8")

ok("Log FIX2", "GMAIL v3.7.4 RC2.6 FIX2:" in ct)
ok("Gmail helper permanece", "def _google_gmail_manejar_voz_rc2_6" in ct)
ok("Gmail sigue temprano", "if self._google_gmail_manejar_voz_rc2_6(texto_original):" in ct)
ok("Calendar permanece", "_google_calendar_manejar_voz_rc2_2" in ct)
ok("Drive permanece", "_google_drive_manejar_voz_rc2_4" in ct)

ok(
    "Gmail usa contexto privado",
    ct.count('tipo_contexto="gmail_privado"') >= 3,
)
ok(
    "Responder tiene barrera Gmail",
    'if tipo_contexto == "gmail_privado":' in ct,
)
ok(
    "Streaming tiene barrera Gmail",
    'tipo_contexto not in {"proyecto", "gmail_privado"}' in ct,
)
ok(
    "Log privacidad existe",
    "PRIVACIDAD GMAIL RC2.6 FIX2:" in ct,
)

tree = ast.parse(ct)
funcs = [
    n for n in ast.walk(tree)
    if isinstance(n, ast.FunctionDef) and n.name == "responder"
]
ok("Una función responder", len(funcs) == 1)

if len(funcs) == 1:
    src = ast.get_source_segment(ct, funcs[0]) or ""
    ok(
        "Rama privada dentro de responder",
        'if tipo_contexto == "gmail_privado":' in src,
    )
    ok(
        "Persistencia normal se conserva",
        'self.memoria.guardar_conversacion("Beta", texto)' in src
        and 'self.actualizar_contexto_turno("Beta", texto)' in src
        and 'self.programar_memoria_inteligente(self.ultimo_mensaje_usuario, texto)' in src,
    )

ok("Gmail metadata-only", "gmail.readonly" not in mt.lower())
ok("Sin cuerpo Gmail", "payload(body" not in mt.replace(" ", "").lower())
ok("Sin adjuntos Gmail", "attachments" not in mt.lower())
ok(
    "Sin escritura Gmail",
    "messages.send" not in mt
    and "messages.modify" not in mt
    and "messages.delete" not in mt,
)

ok("Guardia recientes permanece", "RECIENTES_SIN_PERIODO" in mt)
ok("Tipo recientes_sin_periodo permanece", "recientes_sin_periodo" in mt)

for nombre, aguja in [
    ("Calendar voz", "_google_calendar_manejar_voz_rc2_2"),
    ("Drive voz", "_google_drive_manejar_voz_rc2_4"),
    ("WhatsApp apertura", "def _vosk_whatsapp_directo_seguro"),
    ("WhatsApp cierre", "def _vosk_whatsapp_cierre_seguro"),
    ("Gmail abrir u/0", "https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox"),
    ("Drive abrir u/0", "https://drive.google.com/drive/u/0/my-drive"),
    ("Agenda", "AGENDA_BETA_SERVICE"),
    ("Word", '"beta abre word"'),
    ("Spotify", "spotify"),
    ("Piper", "piper"),
    ("Whisper", "whisper"),
    ("Vosk", "vosk"),
    ("Acciones críticas Atlas", "_atlas_detectar_accion_sistema_critica"),
]:
    ok(nombre, aguja.lower() in ct.lower())

correctas = sum(1 for _, r in pruebas if r)

for nombre, resultado in pruebas:
    print(("[OK] " if resultado else "[ERROR] ") + nombre)

print()
print(f"RESULTADO: {correctas}/{len(pruebas)} pruebas correctas")

if correctas != len(pruebas):
    sys.exit(1)

print("Beta v3.7.4 RC2.6 FIX2: privacidad Gmail / no memoria validada estáticamente.")
