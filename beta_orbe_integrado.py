"""Orbe transparente integrado con Beta mediante UDP local.

Este archivo NO importa ni modifica beta.py. Solo representa visualmente el estado
que beta_inicio_visual.py le envía (hablando/procesando/escuchando/energía).
"""
from __future__ import annotations

import argparse
import json
import socket
import sys
import time
from pathlib import Path

import numpy as np
import pygame
from PySide6.QtCore import Qt, QTimer, QElapsedTimer, QPoint
from PySide6.QtGui import QImage, QPainter, QCursor, QColor
from PySide6.QtWidgets import QApplication, QWidget, QMenu, QColorDialog

from orbe_jarvis import Orbe, TEMAS, MODOS, anadir_args_color, configurar_color


def superficie_a_qimage(surf):
    rgb = np.ascontiguousarray(pygame.surfarray.array3d(surf).transpose(1, 0, 2))
    h, w, _ = rgb.shape
    out = np.empty((h, w, 4), dtype=np.uint8)
    out[..., :3] = rgb
    out[..., 3] = rgb.max(axis=2)
    img = QImage(out.data, w, h, w * 4, QImage.Format_RGBA8888_Premultiplied)
    return img.copy()


class VentanaOrbeBeta(QWidget):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.tam = int(args.tam)
        self.config_path = Path(args.config) if args.config else None
        self.control_addr = ("127.0.0.1", int(args.control_port))

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowTitle("Beta - Orbe JARVIS")
        self.resize(self.tam, self.tam)

        pygame.init()
        self.superficie = pygame.Surface((self.tam, self.tam))
        self.orbe = Orbe(radio=int(self.tam * 0.23))
        configurar_color(self.orbe, args)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("127.0.0.1", int(args.state_port)))
        self.sock.setblocking(False)
        self.sock_control = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.estado = {
            "energia": 0.035,
            "hablando": False,
            "procesando": False,
            "escuchando": False,
            "expresion": "normal",
        }
        self.ultimo_estado_ts = time.time()
        self.energia_visual = 0.035
        self.imagen = None
        self._arrastre = None
        self._movido = False

        self.reloj = QElapsedTimer()
        self.reloj.start()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar)
        self.timer.start(16)

        c = self.screen().availableGeometry().center()
        self.move(c - QPoint(self.tam // 2, self.tam // 2))

    # -------------------- comunicación --------------------
    def _enviar_control(self, cmd, data=None):
        payload = {"cmd": cmd}
        if data is not None:
            payload["data"] = data
        try:
            self.sock_control.sendto(
                json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                self.control_addr,
            )
        except Exception:
            pass

    def _leer_estado(self):
        cerrar = False
        while True:
            try:
                data, _ = self.sock.recvfrom(8192)
            except BlockingIOError:
                break
            except Exception:
                break
            try:
                msg = json.loads(data.decode("utf-8", errors="replace"))
            except Exception:
                continue
            if msg.get("cerrar"):
                cerrar = True
                continue
            if isinstance(msg, dict):
                self.estado.update(msg)
                self.ultimo_estado_ts = time.time()
        return cerrar

    # -------------------- animación --------------------
    def actualizar(self):
        if self._leer_estado():
            self.close()
            return
        # Si el núcleo desaparece abruptamente, el orbe no queda huérfano.
        if time.time() - self.ultimo_estado_ts > 5.0:
            self.close()
            return

        t = self.reloj.elapsed() / 1000.0
        objetivo = float(np.clip(self.estado.get("energia", 0.035), 0.0, 1.0))
        k = 0.42 if objetivo > self.energia_visual else 0.10
        self.energia_visual += (objetivo - self.energia_visual) * k

        p = self.mapFromGlobal(QCursor.pos())
        self.superficie.fill((0, 0, 0))
        self.orbe.dibujar(
            self.superficie,
            (self.tam / 2, self.tam / 2),
            t,
            self.energia_visual,
            mouse=(p.x(), p.y()),
        )
        self.imagen = superficie_a_qimage(self.superficie)
        self.update()

    def paintEvent(self, _):
        if self.imagen is None:
            return
        pintor = QPainter(self)
        pintor.setCompositionMode(QPainter.CompositionMode_Source)
        pintor.drawImage(0, 0, self.imagen)

    # -------------------- ratón --------------------
    def mousePressEvent(self, ev):
        if ev.button() == Qt.LeftButton:
            self._arrastre = ev.globalPosition().toPoint() - self.frameGeometry().topLeft()
            self._movido = False

    def mouseMoveEvent(self, ev):
        if ev.buttons() & Qt.LeftButton and self._arrastre is not None:
            destino = ev.globalPosition().toPoint() - self._arrastre
            if (destino - self.frameGeometry().topLeft()).manhattanLength() > 3:
                self._movido = True
            self.move(destino)

    def mouseReleaseEvent(self, ev):
        if ev.button() == Qt.LeftButton:
            if not self._movido:
                self.orbe.impulso(1.0)
            self._arrastre = None
        elif ev.button() == Qt.RightButton:
            self.menu(ev.globalPosition().toPoint())

    def wheelEvent(self, ev):
        paso = 1.06 if ev.angleDelta().y() > 0 else 1 / 1.06
        self.orbe.R = int(np.clip(self.orbe.R * paso, 35, self.tam * 0.30))

    def keyPressEvent(self, ev):
        k = ev.key()
        nombres = list(TEMAS)
        if k == Qt.Key_Escape:
            self._enviar_control("cerrar_beta")
        elif k == Qt.Key_Tab:
            self.orbe.siguiente_tema()
            self._notificar_config()
        elif k == Qt.Key_C:
            self.orbe.siguiente_modo()
            self._notificar_config()
        elif Qt.Key_1 <= k < Qt.Key_1 + len(nombres):
            self.orbe.set_tema(nombres[k - Qt.Key_1])
            self._notificar_config()

    def elegir_color(self, clave, titulo):
        t = self.orbe.tema
        c = QColorDialog.getColor(QColor(*[int(x) for x in t[clave]]), self, titulo)
        if not c.isValid():
            return
        rgb = (c.red(), c.green(), c.blue())
        if clave == "p":
            self.orbe.set_colores(rgb)
        elif clave == "s":
            self.orbe.set_colores(t["p"], rgb, t["r"])
        else:
            self.orbe.set_colores(t["p"], t["s"], rgb)
            self.orbe.set_modo("reactivo")
        self._notificar_config()

    def _notificar_config(self):
        nombre_tema = self.orbe.tema.get("nombre", "oro")
        # Los colores personalizados funcionan durante la sesión. Para el próximo
        # arranque conservamos un tema válido del motor; así nunca pasamos
        # "personalizado" a --tema (que solo admite TEMAS predefinidos).
        if nombre_tema not in TEMAS:
            nombre_tema = "oro"
        self._enviar_control(
            "config",
            {
                "tema": nombre_tema,
                "modo": self.orbe.modo,
                "tam_orbe": self.tam,
                "siempre_encima": bool(self.windowFlags() & Qt.WindowStaysOnTopHint),
            },
        )

    def menu(self, pos):
        m = QMenu(self)

        # Apariencia general de Beta
        m_ap = m.addMenu("Apariencia de Beta")
        a_jarvis = m_ap.addAction("Orbe JARVIS (predeterminado)")
        a_jarvis.setCheckable(True)
        a_jarvis.setChecked(True)
        a_esfera = m_ap.addAction("Esfera clásica")

        m.addSeparator()
        m_tema = m.addMenu("Tema de color")
        acc_tema = {}
        for nombre in TEMAS:
            a = m_tema.addAction(nombre.capitalize())
            a.setCheckable(True)
            a.setChecked(self.orbe.tema["nombre"] == nombre)
            acc_tema[a] = nombre

        m_modo = m.addMenu("Modo de color")
        etiquetas = {
            "fijo": "Fijo",
            "reactivo": "Reactivo (estado/voz/mouse)",
            "arcoiris": "Arcoíris",
        }
        acc_modo = {}
        for k, txt in etiquetas.items():
            a = m_modo.addAction(txt)
            a.setCheckable(True)
            a.setChecked(self.orbe.modo == k)
            acc_modo[a] = k

        m_pers = m.addMenu("Colores personalizados")
        a_cp = m_pers.addAction("Color principal…")
        a_cs = m_pers.addAction("Color secundario (borde)…")
        a_cr = m_pers.addAction("Color de reacción…")

        m.addSeparator()
        a_top = m.addAction("Siempre encima")
        a_top.setCheckable(True)
        a_top.setChecked(bool(self.windowFlags() & Qt.WindowStaysOnTopHint))
        m.addSeparator()
        a_salir = m.addAction("Cerrar Beta")

        sel = m.exec(pos)
        if sel == a_esfera:
            self._enviar_control("apariencia_esfera")
        elif sel == a_jarvis:
            pass
        elif sel in acc_tema:
            self.orbe.set_tema(acc_tema[sel])
            self._notificar_config()
        elif sel in acc_modo:
            self.orbe.set_modo(acc_modo[sel])
            self._notificar_config()
        elif sel == a_cp:
            self.elegir_color("p", "Color principal")
        elif sel == a_cs:
            self.elegir_color("s", "Color secundario (borde)")
        elif sel == a_cr:
            self.elegir_color("r", "Color de reacción")
        elif sel == a_top:
            self.setWindowFlag(Qt.WindowStaysOnTopHint, a_top.isChecked())
            self.show()
            self._notificar_config()
        elif sel == a_salir:
            self._enviar_control("cerrar_beta")

    def closeEvent(self, ev):
        try:
            self.timer.stop()
            self.sock.close()
            self.sock_control.close()
            pygame.quit()
        except Exception:
            pass
        ev.accept()


def main():
    ap = argparse.ArgumentParser(description="Apariencia Orbe JARVIS integrada con Beta")
    ap.add_argument("--state-port", required=True, type=int)
    ap.add_argument("--control-port", required=True, type=int)
    ap.add_argument("--config", default="")
    ap.add_argument("--tam", type=int, default=760)
    anadir_args_color(ap)
    args = ap.parse_args()

    app = QApplication(sys.argv)
    v = VentanaOrbeBeta(args)
    v.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
