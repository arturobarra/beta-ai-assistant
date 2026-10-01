"""Lanzador visual aditivo para Beta.

NO modifica beta.py. Importa el núcleo estable y permite elegir entre:
  - Orbe JARVIS transparente (predeterminado)
  - Esfera clásica de Beta (interfaz Tk original)

Colocar en la misma carpeta que beta.py, orbe_jarvis.py y beta_orbe_integrado.py.
"""
from __future__ import annotations

import importlib.util
import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
BETA_CORE = BASE_DIR / "beta.py"
ORBE_APP = BASE_DIR / "beta_orbe_integrado.py"
CONFIG_PATH = BASE_DIR / "beta_apariencia.json"

CONFIG_DEFECTO = {
    "apariencia": "jarvis",
    "tam_orbe": 760,
    "tema": "oro",
    "modo": "fijo",
    "siempre_encima": True,
}


def _leer_config() -> dict:
    data = dict(CONFIG_DEFECTO)
    try:
        if CONFIG_PATH.exists():
            cargado = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            if isinstance(cargado, dict):
                data.update(cargado)
    except Exception as exc:
        print(f"APARIENCIA BETA: no pude leer configuración; uso valores por defecto. {exc}")
    if data.get("apariencia") not in {"jarvis", "esfera"}:
        data["apariencia"] = "jarvis"
    return data


def _guardar_config(data: dict) -> None:
    try:
        tmp = CONFIG_PATH.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(tmp, CONFIG_PATH)
    except Exception as exc:
        print(f"APARIENCIA BETA: no pude guardar configuración. {exc}")


def _puerto_libre() -> int:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])
    finally:
        s.close()


def _cargar_beta_core():
    if not BETA_CORE.exists():
        raise FileNotFoundError(f"No encontré el núcleo estable: {BETA_CORE}")
    spec = importlib.util.spec_from_file_location("beta_core_estable", str(BETA_CORE))
    if spec is None or spec.loader is None:
        raise RuntimeError("No pude preparar la importación de beta.py")
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = modulo
    spec.loader.exec_module(modulo)
    return modulo


class GestorApariencia:
    def __init__(self, root, beta_app):
        self.root = root
        self.beta = beta_app
        self.config = _leer_config()
        self.apariencia = self.config.get("apariencia", "jarvis")
        self.orbe_proc: subprocess.Popen | None = None
        self.sock_estado = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_control = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_control.bind(("127.0.0.1", 0))
        self.sock_control.setblocking(False)
        self.control_port = int(self.sock_control.getsockname()[1])
        self.state_port = _puerto_libre()
        self._cerrando = False
        self._ultima_advertencia_dependencias = 0.0

        self._instalar_menu_clasico()
        self.root.bind("<Destroy>", self._al_destruir_root, add="+")

        if self.apariencia == "jarvis":
            self._activar_jarvis(inicial=True)
        else:
            self._activar_esfera(inicial=True)

        self.root.after(50, self._enviar_estado)
        self.root.after(100, self._leer_control)
        self.root.after(700, self._vigilar_orbe)

    # -------------------- configuración / menú --------------------
    def _instalar_menu_clasico(self):
        """Añade el selector al menú existente en tiempo de ejecución.

        No modifica el archivo beta.py.
        """
        try:
            import tkinter as tk
            self.var_apariencia = tk.StringVar(master=self.root, value=self.apariencia)
            submenu = tk.Menu(self.beta.menu, tearoff=0)
            submenu.add_radiobutton(
                label="Orbe JARVIS (predeterminado)",
                value="jarvis",
                variable=self.var_apariencia,
                command=lambda: self.cambiar("jarvis"),
            )
            submenu.add_radiobutton(
                label="Esfera clásica",
                value="esfera",
                variable=self.var_apariencia,
                command=lambda: self.cambiar("esfera"),
            )

            insertar = None
            fin = self.beta.menu.index("end")
            if fin is not None:
                for i in range(int(fin) + 1):
                    try:
                        if self.beta.menu.entrycget(i, "label") == "Cerrar Beta":
                            insertar = i
                            break
                    except Exception:
                        continue
            if insertar is None:
                self.beta.menu.add_separator()
                self.beta.menu.add_cascade(label="Apariencia", menu=submenu)
            else:
                self.beta.menu.insert_separator(insertar)
                self.beta.menu.insert_cascade(insertar + 1, label="Apariencia", menu=submenu)
        except Exception as exc:
            print(f"APARIENCIA BETA: no pude añadir selector al menú clásico. {exc}")

    def _persistir(self):
        self.config["apariencia"] = self.apariencia
        _guardar_config(self.config)
        try:
            self.var_apariencia.set(self.apariencia)
        except Exception:
            pass

    # -------------------- cambio de apariencia --------------------
    def cambiar(self, apariencia: str):
        if apariencia not in {"jarvis", "esfera"}:
            return
        if apariencia == self.apariencia:
            return
        self.apariencia = apariencia
        self._persistir()
        if apariencia == "jarvis":
            self._activar_jarvis()
        else:
            self._activar_esfera()

    def _dependencias_orbe_disponibles(self) -> tuple[bool, str]:
        faltan = []
        for nombre in ("PySide6", "pygame", "numpy"):
            if importlib.util.find_spec(nombre) is None:
                faltan.append(nombre)
        if faltan:
            return False, ", ".join(faltan)
        if not ORBE_APP.exists():
            return False, ORBE_APP.name
        if not (BASE_DIR / "orbe_jarvis.py").exists():
            return False, "orbe_jarvis.py"
        return True, ""

    def _activar_jarvis(self, inicial=False):
        ok, faltan = self._dependencias_orbe_disponibles()
        if not ok:
            print(
                "APARIENCIA BETA: no puedo iniciar el Orbe JARVIS; falta: " + faltan
            )
            print(
                "Instale las dependencias con: python -m pip install PySide6 pygame numpy"
            )
            self.apariencia = "esfera"
            self._persistir()
            self._activar_esfera(inicial=inicial)
            try:
                from tkinter import messagebox
                messagebox.showwarning(
                    "Beta - Apariencia",
                    "No pude iniciar el Orbe JARVIS porque faltan componentes:\n"
                    + faltan
                    + "\n\nEjecute INSTALAR_APARIENCIA_BETA.bat y vuelva a iniciar Beta.",
                    parent=self.root,
                )
            except Exception:
                pass
            return

        self._detener_orbe()
        self.state_port = _puerto_libre()
        args = [
            sys.executable,
            str(ORBE_APP),
            "--state-port", str(self.state_port),
            "--control-port", str(self.control_port),
            "--config", str(CONFIG_PATH),
            "--tam", str(int(self.config.get("tam_orbe", 760))),
            "--tema", str(self.config.get("tema", "oro")),
            "--modo", str(self.config.get("modo", "fijo")),
        ]
        try:
            self.orbe_proc = subprocess.Popen(args, cwd=str(BASE_DIR))
            # El cerebro sigue vivo en Tk; solamente ocultamos su rostro clásico.
            self.root.withdraw()
            print("APARIENCIA BETA: Orbe JARVIS activo (beta.py permanece intacto).")
        except Exception as exc:
            print(f"APARIENCIA BETA: fallo al iniciar orbe: {exc}")
            self.apariencia = "esfera"
            self._persistir()
            self._activar_esfera(inicial=inicial)

    def _activar_esfera(self, inicial=False):
        self._detener_orbe()
        try:
            self.root.deiconify()
            self.root.lift()
            self.root.attributes("-topmost", True)
            print("APARIENCIA BETA: esfera clásica activa.")
        except Exception as exc:
            if not inicial:
                print(f"APARIENCIA BETA: no pude mostrar esfera clásica. {exc}")

    def _detener_orbe(self):
        proc = self.orbe_proc
        self.orbe_proc = None
        if proc is None:
            return
        try:
            self.sock_estado.sendto(
                json.dumps({"cerrar": True}).encode("utf-8"),
                ("127.0.0.1", self.state_port),
            )
        except Exception:
            pass
        try:
            proc.wait(timeout=1.2)
        except Exception:
            try:
                proc.terminate()
            except Exception:
                pass

    # -------------------- sincronización visual --------------------
    def _estado_beta(self) -> dict:
        b = self.beta
        nivel = int(getattr(b, "nivel_boca_habla", 0) or 0)
        hablando = bool(getattr(b, "hablando", False))
        procesando = bool(getattr(b, "procesando", False))
        escuchando = bool(getattr(b, "escuchando", False))
        expresion = str(getattr(b, "expresion_actual", "normal") or "normal")
        sincronizada = bool(getattr(b, "sincronizacion_boca_activa", False))

        if hablando:
            if sincronizada:
                energia = max(0.30, min(1.0, nivel / 3.0))
            else:
                energia = 0.58
        elif procesando:
            # Energía discreta; el propio orbe conserva su respiración visual.
            energia = 0.18
        elif escuchando:
            energia = 0.10
        else:
            energia = 0.035

        return {
            "ts": time.time(),
            "hablando": hablando,
            "procesando": procesando,
            "escuchando": escuchando,
            "nivel_boca": nivel,
            "energia": energia,
            "expresion": expresion,
            "mirada_frontal": bool(getattr(b, "mirada_frontal_voz", False)),
        }

    def _enviar_estado(self):
        if self._cerrando:
            return
        if self.apariencia == "jarvis" and self.orbe_proc is not None:
            try:
                payload = json.dumps(self._estado_beta(), ensure_ascii=False).encode("utf-8")
                self.sock_estado.sendto(payload, ("127.0.0.1", self.state_port))
            except Exception:
                pass
        try:
            self.root.after(50, self._enviar_estado)
        except Exception:
            pass

    def _leer_control(self):
        if self._cerrando:
            return
        while True:
            try:
                data, _ = self.sock_control.recvfrom(4096)
            except BlockingIOError:
                break
            except Exception:
                break
            try:
                msg = json.loads(data.decode("utf-8", errors="replace"))
            except Exception:
                continue
            cmd = str(msg.get("cmd", "")).strip().lower()
            if cmd == "apariencia_esfera":
                self.cambiar("esfera")
            elif cmd == "apariencia_jarvis":
                self.cambiar("jarvis")
            elif cmd == "cerrar_beta":
                try:
                    self.beta.cerrar_beta()
                except Exception:
                    try:
                        self.root.destroy()
                    except Exception:
                        pass
            elif cmd == "config":
                cambios = msg.get("data")
                if isinstance(cambios, dict):
                    for k in ("tam_orbe", "tema", "modo", "siempre_encima"):
                        if k in cambios:
                            self.config[k] = cambios[k]
                    _guardar_config(self.config)
        try:
            self.root.after(100, self._leer_control)
        except Exception:
            pass

    def _vigilar_orbe(self):
        if self._cerrando:
            return
        if self.apariencia == "jarvis" and self.orbe_proc is not None:
            codigo = self.orbe_proc.poll()
            if codigo is not None:
                print(f"APARIENCIA BETA: el orbe terminó (código {codigo}); vuelvo a esfera clásica.")
                self.orbe_proc = None
                self.apariencia = "esfera"
                self._persistir()
                self._activar_esfera()
        try:
            self.root.after(700, self._vigilar_orbe)
        except Exception:
            pass

    def _al_destruir_root(self, event):
        if event.widget is not self.root or self._cerrando:
            return
        self._cerrando = True
        self._detener_orbe()
        try:
            self.sock_estado.close()
            self.sock_control.close()
        except Exception:
            pass


def main():
    beta_core = _cargar_beta_core()

    print("=" * 62)
    print(f"BETA PORTABLE - RUTA BASE: {getattr(beta_core, 'BASE_DIR', BASE_DIR)}")
    print(f"BASE DE DATOS: {getattr(beta_core, 'BASE_DATOS', '')}")
    print(f"BIBLIOTECA: {getattr(beta_core, 'BIBLIOTECA_DIR', '')}")
    print(f"RESPALDOS: {getattr(beta_core, 'RESPALDOS_DIR', '')}")
    print(f"MODELO WHISPER: {getattr(beta_core, 'CARPETA_WHISPER', '')}")
    print(f"MODELO DE VOZ: {getattr(beta_core, 'PIPER_MODELO', '')}")
    print("NÚCLEO: beta.py cargado sin modificar.")
    print("APARIENCIA: Orbe JARVIS predeterminado; esfera clásica disponible.")
    print("=" * 62)

    ventana = beta_core.tk.Tk()
    beta = beta_core.BetaApp(ventana)
    gestor = GestorApariencia(ventana, beta)
    # Mantener referencia viva durante toda la sesión.
    beta._gestor_apariencia_externo = gestor
    ventana.mainloop()


if __name__ == "__main__":
    main()
