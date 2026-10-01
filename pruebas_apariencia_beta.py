from pathlib import Path
import ast
import json
import py_compile
import zipfile

BASE = Path(__file__).resolve().parent
archivos = [
    BASE / "beta_inicio_visual.py",
    BASE / "beta_orbe_integrado.py",
    BASE / "orbe_jarvis.py",
    BASE / "orbe_transparente.py",
]

ok = 0
pruebas = []

def check(cond, nombre):
    global ok
    pruebas.append((bool(cond), nombre))
    if cond:
        ok += 1

for f in archivos:
    try:
        py_compile.compile(str(f), doraise=True)
        check(True, f"compila {f.name}")
    except Exception:
        check(False, f"compila {f.name}")

lanzador = (BASE / "beta_inicio_visual.py").read_text(encoding="utf-8")
orbe = (BASE / "beta_orbe_integrado.py").read_text(encoding="utf-8")
config = json.loads((BASE / "beta_apariencia.json").read_text(encoding="utf-8"))

check(config.get("apariencia") == "jarvis", "JARVIS es apariencia predeterminada")
check('"jarvis", "esfera"' in lanzador or '{"jarvis", "esfera"}' in lanzador, "dos apariencias permitidas")
check("Orbe JARVIS (predeterminado)" in lanzador, "selector clásico contiene JARVIS")
check("Esfera clásica" in lanzador, "selector clásico conserva esfera")
check("root.withdraw()" in lanzador and "root.deiconify()" in lanzador, "solo oculta/muestra la UI clásica")
check("spec_from_file_location" in lanzador and 'BETA_CORE = BASE_DIR / "beta.py"' in lanzador, "beta.py se importa como núcleo externo")
check("BETA_CORE.write" not in lanzador and "BETA_CORE.open" not in lanzador, "lanzador no escribe beta.py")
check("127.0.0.1" in lanzador and "127.0.0.1" in orbe, "sincronización limitada a localhost")
check("EnergiaMicrofono" not in orbe and "sounddevice" not in orbe, "orbe integrado no abre segundo micrófono")
check('self.estado.get("energia"' in orbe, "orbe usa energía enviada por Beta")
check("apariencia_esfera" in orbe and "apariencia_jarvis" in lanzador, "cambio de apariencia bidireccional preparado")
check("el orbe terminó" in lanzador and "esfera clásica" in lanzador, "fallback a esfera si el orbe termina")
check("cerrar_beta" in orbe and "self.beta.cerrar_beta" in lanzador, "cerrar desde orbe cierra Beta completa")
check("personalizado" in orbe and "nombre_tema not in TEMAS" in orbe, "tema personalizado no rompe siguiente arranque")

for estado, nombre in pruebas:
    print(("OK" if estado else "FALLO") + " - " + nombre)
print(f"RESULTADO: {ok}/{len(pruebas)}")
raise SystemExit(0 if ok == len(pruebas) else 1)
