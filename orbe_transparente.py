"""
Orbe JARVIS flotando sobre el escritorio: SIN fondo negro y SIN marco de ventana.

Requisitos:
    pip install PySide6 pygame numpy sounddevice
    (deja este archivo en la misma carpeta que orbe_jarvis.py)

Uso:
    python orbe_transparente.py             # con micrófono (si hay)
    python orbe_transparente.py --sim       # sin micrófono
    python orbe_transparente.py --tam 900   # ventana más grande
    python orbe_transparente.py --tema azul --modo reactivo
    python orbe_transparente.py --color "#00ff99" --color2 "#0044ff" --reaccion "#ff0066"

Controles:
    Arrastrar con clic izquierdo  -> mover el orbe por la pantalla
    Clic izquierdo (sin arrastrar)-> onda de choque
    Rueda del mouse               -> agrandar / achicar el orbe
    Clic derecho                  -> menú: temas, modo de color, colores propios,
                                     micrófono, siempre encima, salir
    Teclas 1-8 / TAB              -> cambiar de tema   |   C -> cambiar de modo de color

Modos de color:
    Fijo      -> siempre el mismo color
    Reactivo  -> el color se mezcla hacia el "color de reacción" cuando hablas,
                 haces clic o mueves el mouse rápido, y vuelve al calmarse
    Arcoíris  -> el color va cambiando solo
    El orbe sigue al cursor en TODA la pantalla, aunque esté fuera de su ventana.
    Voz -> se expande al hablar y se encoge al callar.
"""
import sys
import argparse
import numpy as np
import pygame
from PySide6.QtCore import Qt, QTimer, QElapsedTimer, QPoint
from PySide6.QtGui import QImage, QPainter, QCursor, QColor
from PySide6.QtWidgets import QApplication, QWidget, QMenu, QColorDialog

from orbe_jarvis import (Orbe, EnergiaSimulada, EnergiaMicrofono, TEMAS, MODOS,
                         anadir_args_color, configurar_color)


def superficie_a_qimage(surf):
    """
    Convierte la superficie de pygame (luz sobre negro) en una imagen con transparencia.
    El orbe es luz aditiva, así que: alfa = canal más brillante del píxel, y el color ya
    queda 'premultiplicado'. Resultado: el negro desaparece y el resplandor se funde con
    lo que haya detrás de la ventana, sin halos oscuros.
    """
    rgb = np.ascontiguousarray(pygame.surfarray.array3d(surf).transpose(1, 0, 2))  # (alto, ancho, 3)
    h, w, _ = rgb.shape
    out = np.empty((h, w, 4), dtype=np.uint8)
    out[..., :3] = rgb
    out[..., 3] = rgb.max(axis=2)
    img = QImage(out.data, w, h, w * 4, QImage.Format_RGBA8888_Premultiplied)
    return img.copy()          # copia: el buffer de numpy se libera al salir de la función


class VentanaOrbe(QWidget):
    def __init__(self, tam=760, usar_mic=True, args=None):
        super().__init__()
        self.tam = tam
        # Sin marco + siempre encima + fondo totalmente transparente
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowTitle("Orbe JARVIS")
        self.resize(tam, tam)

        self.superficie = pygame.Surface((tam, tam))
        self.orbe = Orbe(radio=int(tam * 0.23))
        if args is not None:
            configurar_color(self.orbe, args)

        self.sim = EnergiaSimulada()
        self.mic = None
        if usar_mic:
            try:
                self.mic = EnergiaMicrofono()
            except Exception as ex:
                print("No se pudo abrir el micrófono; uso simulación.", ex)
        self.usar_mic = self.mic is not None

        self.imagen = None
        self._arrastre = None
        self._movido = False

        self.reloj = QElapsedTimer()
        self.reloj.start()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar)
        self.timer.start(16)   # ~60 fps (lo real depende de tu equipo)

        # Centrar en la pantalla
        c = self.screen().availableGeometry().center()
        self.move(c - QPoint(tam // 2, tam // 2))

    # ------------------------------ animación ------------------------------
    def actualizar(self):
        t = self.reloj.elapsed() / 1000.0
        energia = self.mic(t) if self.usar_mic else self.sim(t)

        # Posición del cursor en coordenadas de esta ventana (funciona aunque esté fuera)
        p = self.mapFromGlobal(QCursor.pos())

        self.superficie.fill((0, 0, 0))
        self.orbe.dibujar(self.superficie, (self.tam / 2, self.tam / 2), t, energia, mouse=(p.x(), p.y()))
        self.imagen = superficie_a_qimage(self.superficie)
        self.update()

    def paintEvent(self, _):
        if self.imagen is None:
            return
        pintor = QPainter(self)
        pintor.setCompositionMode(QPainter.CompositionMode_Source)   # reemplaza, no mezcla con negro
        pintor.drawImage(0, 0, self.imagen)

    # ------------------------------- ratón ---------------------------------
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
                self.orbe.impulso(1.0)       # clic simple = onda de choque
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
            self.close()
        elif k == Qt.Key_Tab:
            self.orbe.siguiente_tema()
        elif k == Qt.Key_C:
            self.orbe.siguiente_modo()
        elif Qt.Key_1 <= k < Qt.Key_1 + len(nombres):
            self.orbe.set_tema(nombres[k - Qt.Key_1])

    def elegir_color(self, clave, titulo):
        """Abre el selector de color. 'p' = principal (deriva el resto), 's' = borde, 'r' = reacción."""
        t = self.orbe.tema
        c = QColorDialog.getColor(QColor(*[int(x) for x in t[clave]]), self, titulo)
        if not c.isValid():
            return
        rgb = (c.red(), c.green(), c.blue())
        if clave == "p":
            self.orbe.set_colores(rgb)                         # secundario y reacción se derivan solos
        elif clave == "s":
            self.orbe.set_colores(t["p"], rgb, t["r"])
        else:
            self.orbe.set_colores(t["p"], t["s"], rgb)
            self.orbe.set_modo("reactivo")                     # para que veas el efecto enseguida

    def menu(self, pos):
        m = QMenu(self)
        a_mic = m.addAction("Micrófono: " + ("activado" if self.usar_mic else "desactivado (simulación)"))
        a_mic.setEnabled(self.mic is not None)
        m.addSeparator()
        m_tema = m.addMenu("Tema de color")
        acc_tema = {}
        for nombre in TEMAS:
            a = m_tema.addAction(nombre.capitalize())
            a.setCheckable(True)
            a.setChecked(self.orbe.tema["nombre"] == nombre)
            acc_tema[a] = nombre
        m_modo = m.addMenu("Modo de color")
        etiquetas = {"fijo": "Fijo", "reactivo": "Reactivo (cambia con voz y mouse)", "arcoiris": "Arcoíris"}
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
        a_salir = m.addAction("Salir")
        sel = m.exec(pos)
        if sel == a_mic:
            self.usar_mic = not self.usar_mic
        elif sel in acc_tema:
            self.orbe.set_tema(acc_tema[sel])
        elif sel in acc_modo:
            self.orbe.set_modo(acc_modo[sel])
        elif sel == a_cp:
            self.elegir_color("p", "Color principal")
        elif sel == a_cs:
            self.elegir_color("s", "Color secundario (borde)")
        elif sel == a_cr:
            self.elegir_color("r", "Color de reacción")
        elif sel == a_top:
            self.setWindowFlag(Qt.WindowStaysOnTopHint, a_top.isChecked())
            self.show()
        elif sel == a_salir:
            self.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sim", action="store_true", help="no usar micrófono")
    ap.add_argument("--tam", type=int, default=760, help="tamaño de la ventana en píxeles")
    anadir_args_color(ap)
    args = ap.parse_args()

    app = QApplication(sys.argv)
    v = VentanaOrbe(args.tam, usar_mic=not args.sim, args=args)
    v.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
