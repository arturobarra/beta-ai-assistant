"""
Orbe amarillo/naranja estilo JARVIS (partículas + malla + anillos + rayos + núcleo brillante).

Requisitos:
    pip install pygame numpy
    (opcional, para reaccionar al micrófono)  pip install sounddevice

Uso rápido:
    python orbe_jarvis.py            -> ventana; usa el micrófono si está disponible
    python orbe_jarvis.py --sim      -> energía simulada (sin micrófono)
    python orbe_jarvis.py --tema azul --modo reactivo
    python orbe_jarvis.py --color "#00ff99" --color2 "#0044ff" --reaccion "#ff0066"
    python orbe_jarvis.py --frame salida.png   -> guarda un solo fotograma

Controles en la ventana:
    Mouse        -> el orbe se inclina hacia el cursor, las partículas se apartan
                    y, si mueves el mouse rápido, el orbe se agita
    Clic         -> onda de choque (pulso fuerte)
    Voz          -> el orbe se expande al hablar y se encoge al callar
    1-8          -> cambiar de tema de color (oro, azul, rojo, verde, cian, violeta, rosa, plata)
    TAB          -> siguiente tema
    C            -> cambiar modo de color: fijo / reactivo / arcoíris
    M            -> alternar micrófono / simulación
    Flecha arriba/abajo -> sensibilidad del micrófono
    ESC          -> salir

Para integrarlo en tu proyecto:
    from orbe_jarvis import Orbe
    orbe = Orbe(radio=200)
    ...
    # dentro de tu bucle pygame:
    orbe.dibujar(pantalla, (ancho//2, alto//2), t, energia, mouse=pygame.mouse.get_pos())
    # energia: 0.0 a 1.0 (volumen de voz). Con un clic: orbe.impulso(1.0)
"""
import math
import sys
import argparse
import colorsys
import numpy as np
import pygame

# --------------------------- PARÁMETROS AJUSTABLES ---------------------------
N_PARTICULAS = 14000      # puntos de la nube exterior
N_MALLA = 520            # vértices de la esfera de malla interior
VECINOS_MALLA = 3        # conexiones por vértice
N_ANILLOS = 7            # arcos giratorios
N_RAYOS = 40             # rayos que salen del centro
VELOCIDAD_GIRO = 0.35
PERSPECTIVA = 3.2        # menor = más perspectiva
# ------------------------------------------------------------------------------


# ------------------------------ COLORES ------------------------------------------
# p = color principal (cuerpo brillante), s = color secundario (borde / partículas
# exteriores), r = color de reacción (hacia el que se mezcla en modo "reactivo").
TEMAS = {
    "oro":     {"p": (255, 185, 40),  "s": (255, 70, 8),    "r": (255, 60, 40)},
    "azul":    {"p": (70, 170, 255),  "s": (20, 60, 255),   "r": (255, 70, 130)},
    "rojo":    {"p": (255, 95, 70),   "s": (210, 10, 10),   "r": (255, 225, 90)},
    "verde":   {"p": (90, 255, 150),  "s": (0, 150, 70),    "r": (255, 240, 90)},
    "cian":    {"p": (70, 255, 240),  "s": (0, 110, 210),   "r": (255, 80, 220)},
    "violeta": {"p": (195, 125, 255), "s": (95, 30, 225),   "r": (255, 130, 60)},
    "rosa":    {"p": (255, 115, 225), "s": (185, 20, 165),  "r": (90, 225, 255)},
    "plata":   {"p": (225, 238, 255), "s": (110, 140, 200), "r": (255, 200, 100)},
}
MODOS = ("fijo", "reactivo", "arcoiris")


def _a_rgb(c):
    """Acepta (r, g, b) o '#rrggbb' y devuelve un array float."""
    if isinstance(c, str):
        c = c.strip().lstrip("#")
        return np.array([int(c[i:i + 2], 16) for i in (0, 2, 4)], dtype=float)
    return np.array(c[:3], dtype=float)


def _sec_de(p):
    """Versión más profunda y saturada de un color (para el borde)."""
    return 255.0 * (np.clip(p, 0, 255) / 255.0) ** 1.8


def _complementario(p):
    h, s, v = colorsys.rgb_to_hsv(*(np.clip(p, 0, 255) / 255.0))
    r = colorsys.hsv_to_rgb((h + 0.45) % 1.0, max(s, 0.6), 1.0)
    return np.array(r) * 255.0


def _paleta_de(p, s=None):
    """Paleta (3x3): [borde, principal, brillo/núcleo]."""
    p = _a_rgb(p)
    s = _sec_de(p) if s is None else _a_rgb(s)
    c2 = p + (255 - p) * 0.75
    return np.stack([s, p, c2])


def _esfera_aleatoria(n, rng):
    v = rng.normal(size=(n, 3))
    return v / np.linalg.norm(v, axis=1, keepdims=True)


def _rot(ax, ay, az):
    """Matriz de rotación 3D a partir de tres ángulos."""
    cx, sx, cy, sy, cz, sz = math.cos(ax), math.sin(ax), math.cos(ay), math.sin(ay), math.cos(az), math.sin(az)
    rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    return rz @ ry @ rx


def _color(prof, base, pal):
    """Color de partículas: borde -> principal -> núcleo según brillo (0..1) y profundidad."""
    b = np.clip(base, 0, 1)[:, None]
    c0, c1, c2 = pal
    c = np.where(b < 0.6, c0 + (c1 - c0) * (b / 0.6), c1 + (c2 - c1) * ((b - 0.6) / 0.4))
    return np.clip(c * np.clip(prof, 0.25, 1.0)[:, None], 0, 255).astype(np.uint8)


class Orbe:
    def __init__(self, radio=220, semilla=7):
        self.R = radio
        rng = np.random.default_rng(semilla)
        self.rng = rng

        # Nube de partículas: más densas hacia el borde, con dispersión radial
        self.dir_p = _esfera_aleatoria(N_PARTICULAS, rng)
        self.rad_p = 0.45 + 0.60 * rng.beta(5.0, 1.8, N_PARTICULAS)
        self.fase_p = rng.uniform(0, 6.28, N_PARTICULAS)
        self.vel_p = rng.uniform(0.5, 1.5, N_PARTICULAS)

        # Malla interior (esfera con líneas entre vecinos)
        self.pts_m = _esfera_aleatoria(N_MALLA, rng)
        d = np.linalg.norm(self.pts_m[:, None] - self.pts_m[None], axis=2)
        idx = np.argsort(d, axis=1)[:, 1:VECINOS_MALLA + 1]
        self.aristas = np.array([(i, j) for i in range(N_MALLA) for j in idx[i]])

        # Anillos (arcos) con eje, velocidad y longitud propios
        self.anillos = []
        for _ in range(N_ANILLOS):
            self.anillos.append({
                "eje": rng.uniform(0, 6.28, 3),
                "vel": rng.uniform(-1, 1, 3) * 0.8,
                "r": rng.uniform(0.7, 1.12),
                "ini": rng.uniform(0, 6.28),
                "vel_ini": rng.uniform(-1.5, 1.5),
                "largo": rng.uniform(1.6, 6.0),
                "ancho": int(rng.integers(2, 5)),
            })

        # Rayos radiales
        self.dir_r = _esfera_aleatoria(N_RAYOS, rng)
        self.fase_r = rng.uniform(0, 6.28, N_RAYOS)
        self.long_r = rng.uniform(0.75, 1.25, N_RAYOS)

        # Estado de interacción (mouse / voz)
        self.tilt = np.zeros(2)          # inclinación suavizada hacia el mouse
        self.desp = np.zeros(2)          # desplazamiento suave del centro
        self.mpos_prev = None
        self.t_prev = None
        self.mvel = 0.0                  # velocidad del mouse suavizada (0..1)
        self.escala = 1.0                # expansión/encogimiento suavizado
        self._imp = 0.0                  # impulso por clic

        # Color
        self.tema = {"nombre": "oro", **TEMAS["oro"]}
        self.modo = "fijo"
        self.mix = 0.0                   # cuánto se ha mezclado hacia el color de reacción
        self.pal = _paleta_de(self.tema["p"], self.tema["s"])

        # Superficies auxiliares (se crean según el tamaño de la pantalla)
        self._tam = None
        self._nucleo = None

    # ------------------------------ color ------------------------------
    def set_tema(self, nombre, inmediato=False):
        t = TEMAS[nombre]
        self.tema = {"nombre": nombre, "p": t["p"], "s": t["s"], "r": t["r"]}
        if inmediato:
            self.pal = self._paleta_objetivo(0.0).copy()

    def set_colores(self, principal, secundario=None, reaccion=None, inmediato=False):
        """Colores propios: (r,g,b) o '#rrggbb'. Los que no des se derivan del principal."""
        p = _a_rgb(principal)
        s = _sec_de(p) if secundario is None else _a_rgb(secundario)
        r = _complementario(p) if reaccion is None else _a_rgb(reaccion)
        self.tema = {"nombre": "personalizado", "p": tuple(p), "s": tuple(s), "r": tuple(r)}
        if inmediato:
            self.pal = self._paleta_objetivo(0.0).copy()

    def set_modo(self, modo, inmediato=False):
        """'fijo' | 'reactivo' (cambia con voz y mouse) | 'arcoiris' (cicla de color)."""
        assert modo in MODOS, "modo debe ser uno de %s" % (MODOS,)
        self.modo = modo
        if inmediato:
            self.pal = self._paleta_objetivo(0.0).copy()

    def siguiente_tema(self):
        nombres = list(TEMAS)
        i = nombres.index(self.tema["nombre"]) if self.tema["nombre"] in nombres else -1
        self.set_tema(nombres[(i + 1) % len(nombres)])

    def siguiente_modo(self):
        self.set_modo(MODOS[(MODOS.index(self.modo) + 1) % len(MODOS)])

    def _paleta_objetivo(self, t):
        if self.modo == "arcoiris":
            h = (t * 0.05) % 1.0
            p = np.array(colorsys.hsv_to_rgb(h, 0.70, 1.0)) * 255
            sc = np.array(colorsys.hsv_to_rgb((h + 0.09) % 1.0, 1.0, 0.90)) * 255
            return _paleta_de(p, sc)
        base = _paleta_de(self.tema["p"], self.tema["s"])
        if self.modo == "reactivo":
            react = _paleta_de(self.tema["r"])
            return base + (react - base) * self.mix
        return base

    def impulso(self, fuerza=1.0):
        """Onda de choque: el orbe se expande de golpe y vuelve a su tamaño."""
        self._imp = max(self._imp, fuerza)

    # ---------------------------- utilidades ----------------------------
    def _proyectar(self, p, centro):
        """p: (N,3) en unidades de radio -> (x, y, profundidad 0..1)."""
        z = p[:, 2]
        f = PERSPECTIVA / (PERSPECTIVA - z)
        x = centro[0] + p[:, 0] * self.R * f
        y = centro[1] + p[:, 1] * self.R * f
        prof = (z + 1.3) / 2.6
        return x, y, prof

    def _ruido(self, p, t):
        """Deformación orgánica tipo 'humo' del borde."""
        return (np.sin(2.1 * p[:, 0] + 0.9 * t) * np.sin(1.7 * p[:, 1] - 0.7 * t)
                + np.sin(2.6 * p[:, 2] + 1.1 * t + 3.0 * p[:, 0]) * 0.8) * 0.5

    def _crear_nucleo(self, r, pal):
        s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        c0, c1, c2 = pal
        borde = c0 + (c1 - c0) * 0.6
        for i in range(r, 0, -2):
            a = (1 - i / r) ** 2.2
            m = min(1.0, a ** 0.8 * 1.15)
            col = np.clip(borde + (c2 - borde) * m, 0, 255)
            pygame.draw.circle(s, (int(col[0]), int(col[1]), int(col[2]), int(255 * min(1, a * 1.3))), (r, r), i)
        return s

    @staticmethod
    def _bloom(surf, intensidad=1.0, esc=1.0):
        """Resplandor: reduce, amplía y suma. El radio del brillo se adapta al tamaño del orbe."""
        w, h = surf.get_size()
        out = surf.copy()
        k = min(1.5, max(0.2, esc))
        for div in (max(2, int(round(4 * k))), max(3, int(round(10 * k)))):
            peq_ = pygame.transform.smoothscale(surf, (max(1, w // div), max(1, h // div)))
            gr = pygame.transform.smoothscale(peq_, (w, h))
            if intensidad != 1.0:
                gr.fill((int(255 * min(1, intensidad)),) * 3, special_flags=pygame.BLEND_RGB_MULT)
            out.blit(gr, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
            out.blit(gr, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
        return out

    # ------------------------------ dibujo ------------------------------
    def dibujar(self, pantalla, centro, t, energia=0.4, mouse=None):
        """Dibuja el orbe. energia en [0,1] (volumen de voz). mouse=(x, y) activa la interacción."""
        w, h = pantalla.get_size()
        if self._tam != (w, h):
            self._tam = (w, h)
            self._capa = pygame.Surface((w, h))
        capa = self._capa
        capa.fill((0, 0, 0))
        R = self.R
        esc = R / 252.0                  # 1.0 = tamaño de referencia; <1 = orbe pequeño
        peq = min(1.0, esc)

        # --- Interacción con el mouse -----------------------------------------
        if mouse is not None:
            dxn = float(np.clip((mouse[0] - centro[0]) / (w / 2), -1, 1))
            dyn = float(np.clip((mouse[1] - centro[1]) / (h / 2), -1, 1))
            self.tilt += (np.array([-dyn * 0.7, dxn * 0.7]) - self.tilt) * 0.08
            self.desp += (np.array([dxn, dyn]) * R * 0.12 - self.desp) * 0.06
            if self.mpos_prev is not None and self.t_prev is not None and t > self.t_prev:
                v = math.hypot(mouse[0] - self.mpos_prev[0], mouse[1] - self.mpos_prev[1]) / (t - self.t_prev) / (R * 5)
                self.mvel = max(min(1.0, v), self.mvel * 0.93)
            self.mpos_prev = mouse
        else:
            self.tilt *= 0.95
            self.desp *= 0.95
            self.mvel *= 0.93
        self.t_prev = t
        extra = _rot(self.tilt[0], self.tilt[1], 0.0)          # rotación extra por el mouse
        centro = (centro[0] + self.desp[0], centro[1] + self.desp[1])
        self._imp *= 0.90

        # Energía total: voz + agitación del mouse + impulso del clic
        e = float(np.clip(energia + 0.6 * self.mvel + self._imp, 0, 1))

        # Expansión / encogimiento: sube rápido al hablar, baja lento al callar
        objetivo = 1.0 + 0.38 * e + 0.25 * self._imp
        k = 0.45 if objetivo > self.escala else 0.10
        self.escala += (objetivo - self.escala) * k
        pulso = self.escala * (1 + 0.025 * math.sin(t * 2.0))
        giro = t * (VELOCIDAD_GIRO + 0.5 * self.mvel)

        # Color: tema + modo (fijo / reactivo / arcoíris), con transición suave
        m_obj = min(1.0, e * 1.4)
        self.mix += (m_obj - self.mix) * (0.35 if m_obj > self.mix else 0.05)
        self.pal += (self._paleta_objetivo(t) - self.pal) * 0.12
        pal = self.pal
        c0, c1, c2 = pal

        # 1) Malla interior -------------------------------------------------
        rot = _rot(giro * 0.9, giro * 1.3, giro * 0.4)
        pm = (self.pts_m @ (extra @ rot).T) * (0.78 * pulso)
        xm, ym, profm = self._proyectar(pm, centro)
        col = tuple(int(x) for x in np.clip(c0 * (0.45 + 0.2 * e) * (0.55 + 0.45 * peq), 0, 255))
        n_ar = int(len(self.aristas) * float(np.clip(esc ** 2.0, 0.05, 1.0)))
        for a, b in self.aristas[:n_ar]:
            pygame.draw.line(capa, col, (xm[a], ym[a]), (xm[b], ym[b]), 1)

        # 2) Nube de partículas ----------------------------------------------
        rot_p = _rot(giro * 0.5, giro, giro * 0.2)
        nv = int(N_PARTICULAS * float(np.clip(esc ** 1.8, 0.05, 1.0)))   # menos partículas si es pequeño
        dirs = self.dir_p[:nv] @ (extra @ rot_p).T
        n = self._ruido(dirs, t * 0.9)
        # las partículas "respiran" y se desplazan hacia fuera con la energía
        resp = 1 + 0.05 * np.sin(t * 1.5 * self.vel_p[:nv] + self.fase_p[:nv])
        rad = self.rad_p[:nv] * (1 + 0.16 * n + 0.10 * self.mvel) * resp * pulso * (1 + 0.10 * e * np.sin(self.fase_p[:nv] * 3 + t * 6))
        pp = dirs * rad[:, None]
        xp, yp, profp = self._proyectar(pp, centro)
        if mouse is not None:                      # las partículas se apartan del cursor
            ddx, ddy = xp - mouse[0], yp - mouse[1]
            dist = np.hypot(ddx, ddy) + 1e-6
            fuerza = np.clip(1 - dist / (R * 0.6), 0, 1) ** 2 * R * 0.30
            xp = xp + ddx / dist * fuerza
            yp = yp + ddy / dist * fuerza
        ix, iy = xp.astype(int), yp.astype(int)
        ok = (ix >= 1) & (ix < w - 1) & (iy >= 1) & (iy < h - 1)
        brillo = np.clip(rad / 1.1, 0, 1) ** 0.8
        cols = _color(profp, 0.0 + 0.36 * brillo + 0.10 * e, pal)
        px = pygame.surfarray.pixels3d(capa)
        puntos = ((0, 0), (1, 0), (0, 1), (1, 1)) if esc >= 0.65 else ((0, 0),)   # 2x2 px, o 1 px si es pequeño
        for dx, dy in puntos:
            px[ix[ok] + dx, iy[ok] + dy] = cols[ok]
        del px

        # 3) Anillos / arcos giratorios --------------------------------------
        for an in self.anillos:
            ang = an["ini"] + an["vel_ini"] * t
            largo = an["largo"] * (0.75 + 0.25 * math.sin(t * 0.8 + an["ini"]))
            m = _rot(*(an["eje"] + an["vel"] * t))
            k = max(20, int(largo * 14))
            th = ang + np.linspace(0, largo, k)
            circ = np.stack([np.cos(th), np.sin(th), np.zeros(k)], axis=1)
            circ = (circ @ (extra @ m).T) * (an["r"] * pulso)
            x, y, prof = self._proyectar(circ, centro)
            for i in range(k - 1):
                f = 0.45 + 0.55 * (i / k)                   # la cola se desvanece
                c = tuple(int(x) for x in np.clip(c1 * f * (0.6 + 0.4 * prof[i]), 0, 255))
                pygame.draw.line(capa, c, (x[i], y[i]), (x[i + 1], y[i + 1]), (1 if esc < 0.6 else max(1, int(round(an["ancho"] * peq * 0.8)))))

        # 4) Rayos radiales ---------------------------------------------------
        rot_r = _rot(-giro * 0.7, giro * 0.6, giro * 0.3)
        dr = self.dir_r @ (extra @ rot_r).T
        nr = int(max(8, N_RAYOS * min(1.0, esc * 1.1)))
        ancho_r = 2 if esc >= 0.9 else 1
        for i in range(nr):
            parpadeo = 0.6 + 0.4 * math.sin(t * 3 + self.fase_r[i] * 2)
            largo = self.long_r[i] * (0.55 + 0.45 * e * parpadeo + 0.15 * parpadeo) * pulso
            a = dr[i] * 0.12
            b = dr[i] * largo
            (xa, xb), (ya, yb), prof = self._proyectar(np.array([a, b]), centro)
            g = 0.55 + 0.45 * parpadeo
            c = tuple(int(x) for x in np.clip(c0 + (c1 - c0) * min(1.0, 0.8 * g + 0.2 * prof[1]), 0, 255))
            pygame.draw.line(capa, c, (xa, ya), (xb, yb), ancho_r)

        # 5) Núcleo brillante ---------------------------------------------------
        rn = max(3, int(R * (0.75 + 0.25 * peq) * (0.14 + 0.10 * e + 0.015 * math.sin(t * 3))))
        clave = (rn, tuple(int(x) // 5 for x in pal.flatten()))
        if self._nucleo is None or self._nucleo[0] != clave:
            self._nucleo = (clave, self._crear_nucleo(rn, pal))
        capa.blit(self._nucleo[1], (centro[0] - rn, centro[1] - rn), special_flags=pygame.BLEND_RGB_ADD)

        # 6) Resplandor (bloom) y composición ------------------------------------
        final = self._bloom(capa, (0.55 + 0.25 * e) * (0.5 + 0.5 * peq), esc)
        pantalla.blit(final, (0, 0))


# --------------------------- ENERGÍA DE ENTRADA ---------------------------
class EnergiaSimulada:
    """Simula 'habla': ráfagas aleatorias suaves."""
    def __init__(self):
        self.v = 0.3

    def __call__(self, t):
        obj = 0.35 + 0.35 * math.sin(t * 1.3) * math.sin(t * 0.37) + 0.25 * math.sin(t * 7.0) ** 2
        self.v += (obj - self.v) * 0.15
        return float(np.clip(self.v, 0, 1))


class EnergiaMicrofono:
    """Nivel de voz del micrófono (requiere sounddevice). Calibra el ruido de fondo solo."""
    def __init__(self, sensibilidad=18.0):
        import sounddevice as sd
        self.nivel = 0.0
        self.suelo = 0.01          # ruido de fondo estimado
        self.sens = sensibilidad
        def cb(datos, frames, tiempo, estado):
            rms = float(np.sqrt(np.mean(datos ** 2)))
            if rms < self.suelo:
                self.suelo = rms
            else:
                self.suelo += (rms - self.suelo) * 0.002
            obj = float(np.clip((rms - self.suelo * 1.5) * self.sens, 0, 1))
            k = 0.6 if obj > self.nivel else 0.12      # ataque rápido, caída suave
            self.nivel += (obj - self.nivel) * k
        self.stream = sd.InputStream(channels=1, blocksize=1024, callback=cb)
        self.stream.start()

    def __call__(self, t):
        return self.nivel


# ---------------------------------- MAIN ----------------------------------
def anadir_args_color(ap):
    ap.add_argument("--tema", default="oro", choices=list(TEMAS), help="tema de color")
    ap.add_argument("--modo", default="fijo", choices=MODOS, help="fijo | reactivo | arcoiris")
    ap.add_argument("--color", help='color principal propio, ej. "#00ff99"')
    ap.add_argument("--color2", help="color secundario (borde)")
    ap.add_argument("--reaccion", help="color al que se mezcla en modo reactivo")


def configurar_color(orbe, args):
    if args.color:
        orbe.set_colores(args.color, args.color2, args.reaccion, inmediato=True)
    else:
        orbe.set_tema(args.tema, inmediato=True)
    orbe.set_modo(args.modo, inmediato=True)


def main():
    ap = argparse.ArgumentParser(description="Orbe JARVIS")
    ap.add_argument("--sim", action="store_true", help="energía simulada, sin micrófono")
    ap.add_argument("--frame", help="guardar un fotograma en este archivo y salir")
    anadir_args_color(ap)
    args = ap.parse_args()
    guardar = args.frame

    pygame.init()
    W, H = 900, 900
    pantalla = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Orbe JARVIS")
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("consolas,menlo,monospace", 16)
    orbe = Orbe(radio=int(H * 0.28))
    configurar_color(orbe, args)

    sim = EnergiaSimulada()
    mic = None
    if guardar is None and not args.sim:
        try:
            mic = EnergiaMicrofono()
        except Exception as ex:
            print("No se pudo abrir el micrófono (pip install sounddevice). Uso simulación.", ex)
    usar_mic = mic is not None

    if guardar:
        t = 6.0
        pantalla.fill((2, 2, 8))
        for i in range(30):
            orbe.dibujar(pantalla, (W // 2, H // 2), t + i / 30, 0.7)
        pygame.image.save(pantalla, guardar)
        return

    nombres_tema = list(TEMAS)
    teclas_tema = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8]
    t0 = pygame.time.get_ticks()
    corriendo = True
    while corriendo:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT or (ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE):
                corriendo = False
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                orbe.impulso(1.0)
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_m and mic is not None:
                    usar_mic = not usar_mic
                elif ev.key == pygame.K_UP and mic is not None:
                    mic.sens *= 1.25
                elif ev.key == pygame.K_DOWN and mic is not None:
                    mic.sens /= 1.25
                elif ev.key == pygame.K_TAB:
                    orbe.siguiente_tema()
                elif ev.key == pygame.K_c:
                    orbe.siguiente_modo()
                elif ev.key in teclas_tema:
                    orbe.set_tema(nombres_tema[teclas_tema.index(ev.key)])
        t = (pygame.time.get_ticks() - t0) / 1000
        energia = mic(t) if usar_mic else sim(t)
        pantalla.fill((2, 2, 8))
        orbe.dibujar(pantalla, (W // 2, H // 2), t, energia, mouse=pygame.mouse.get_pos())

        # Indicadores
        l1 = "Tema: %s   Modo: %s   [1-8/TAB] tema  [C] modo" % (orbe.tema["nombre"], orbe.modo)
        l2 = "Mic: %s  sens x%.1f   [M] mic  [↑/↓] sensibilidad" % (
            "ON" if usar_mic else "SIM", mic.sens / 18 if mic else 1)
        pantalla.blit(fuente.render(l1, True, (170, 110, 40)), (14, H - 52))
        pantalla.blit(fuente.render(l2, True, (170, 110, 40)), (14, H - 28))
        pygame.draw.rect(pantalla, (60, 35, 8), (14, H - 68, 160, 8))
        pygame.draw.rect(pantalla, tuple(int(x) for x in orbe.pal[1]), (14, H - 68, int(160 * energia), 8))

        pygame.display.flip()
        reloj.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
