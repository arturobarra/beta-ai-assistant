import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from pathlib import Path

import base64
from array import array
import ctypes
import difflib
import hashlib
import json
import math
import os
# Evita enlaces simbólicos de Hugging Face en Windows.
# En equipos sin Modo desarrollador, los symlinks pueden provocar WinError 1314.
os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS", "1")
os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
import queue
import random
import secrets
import http.server
import re
import sqlite3
import subprocess
import shutil
import threading
import time
import tempfile
import wave
import sys
import winsound
import zipfile
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime


# ==========================================================
# BETA v2.7.1 - RESPALDOS AUTOMÁTICOS + BIBLIOTECA TÉCNICA ESTABLE
# Mascota virtual + memoria + comandos aprendidos + clima
# + Ollama/Qwen3 Instruct + memoria evolutiva + personalidad adaptativa
# + voz híbrida: Vosk para activación y Faster-Whisper para dictado
# + investigación web con DDGS + Qwen local + fuentes + continuidad
# + iniciativa conversacional opcional (Modo compañera)
# + sincronización de boca con la amplitud real del WAV de Daniela
# + pronóstico meteorológico del día siguiente (temperatura, condición y lluvia)
# + memoria inteligente automática (hechos relevantes extraídos en segundo plano)
# + contexto conversacional persistente y resúmenes de conversación
# + preguntas de seguimiento y modo compañera mejorado
# + verificación biométrica local de hablante con SpeechBrain ECAPA-TDNN
# + múltiples voces autorizadas, registro local y bloqueo de voces desconocidas
# + biblioteca académica local de PDFs con búsqueda semántica (RAG)
# + prioridad a apuntes institucionales y complemento web opcional
# + fuentes académicas por PDF, ramo, módulo y página
# + OCR local con Tesseract para módulos escaneados o convertidos en imágenes
# + seguimiento académico robusto ante errores cortos de Whisper (ej. "perfumdiza")
# + prioridad al contexto académico activo para preguntas de continuación
# + streaming Ollama por frases: Daniela empieza a hablar antes de terminar toda la generación
# + precisión académica: todo seguimiento vuelve a consultar los apuntes con tema base estable
# + cierre seguro de streaming: nunca pronuncia una cola cortada a mitad de oración
# + prompt académico compacto + contexto reducido para bajar la latencia del primer audio
# + pipeline paralelo Qwen -> Piper -> audio para reducir la espera percibida
# + respuestas académicas más compactas por defecto y corte de contexto ante saludos
# + modo de escucha estricto por defecto: exige wake word + voz autorizada
# + modo conversación explícito y temporal para continuidad sin repetir "Beta"
# + modo silencio: ignora todo salvo "Beta, despierta"
# + filtro previo a biometría: conversaciones ambientales sin wake word se descartan
# + biometría obligatoria cuando existen voces autorizadas (no puede quedar desactivada por accidente)
# + sesión conversacional vinculada a una autenticación fuerte y umbral corto contextual seguro
# v2.6.0: aprendizaje curioso progresivo, preguntas naturales y memoria desde respuestas explícitas
# v2.6.1: instalación portable: toda la información propia de Beta sigue la carpeta donde vive beta.py
# v2.6.2: unidad de aprendizaje adaptativo con progreso por ramo/tema y evaluaciones desde los PDF
# v2.6.4: Spotify robusto: aliases fonéticos, controles contextuales, OAuth resistente y API 204
# v2.6.5: playlists personales: /me/playlists, coincidencia flexible, apertura y reproducción directa
# + reproducción por artista, controles de player y preferencias (top artists)
# + autoevaluación natural: "lo entendí" / "me cuesta" actualiza el progreso sin inventar dominio
# + preguntas académicas una por una, evaluación local con Qwen y evidencia guardada en beta.db
# + panel de progreso académico y recomendaciones de repaso basadas en evidencia real
# + personalización ligera usando preferencias aprendidas por curiosidad
# + migración automática de rutas absolutas antiguas de PDFs a rutas relativas portables
# + filtro de alucinaciones ASR típicas ("suscríbete", "subtítulos", etc.)
# + consolidación de comandos de privacidad y variantes naturales para cerrar conversación
# + seguimiento académico priorizado por ramo para evitar mezclar materias
# + memoria inteligente diferida mientras hay conversación activa
# + protección contra transcripciones parciales/duplicadas y colas de audio atrasadas
# v2.8.3: separación estricta de fuentes + uso inteligente de Internet
# + evita que un seguimiento corto arrastre Python cuando el Señor cambia claramente a RAM/hardware u otro dominio
# + reenvía cambios de dominio al enrutador global antes de heredar el contexto anterior
# + expande y reordena búsquedas de palabras clave como return, kwargs, xargs, elif, def y lambda
# + prioriza la pregunta de seguimiento actual para no repetir la definición del tema base
# + refuerzo adicional para que una mención incidental de RAM en Python no desplace apuntes de Arquitectura
# v2.8.1: enrutamiento semántico robusto + diccionario técnico de voz
# + compara evidencia académica y técnica por separado para que una categoría no oculte a la otra
# + puntúa grupos coherentes por ramo/colección en vez de decidir solo por el fragmento máximo
# + refuerzos de dominio conservadores (hardware, redes, seguridad, SQL, Docker, Linux, Python)
# + corrección contextual de términos técnicos mal transcritos por Whisper (return, kwargs, elif, etc.)
# + las consultas mixtas recuperan material de ambas bibliotecas de forma equilibrada
# v2.8.0: biblioteca inteligente y enrutamiento semántico de conocimiento
# + decide automáticamente entre apuntes académicos, libros técnicos, varias colecciones o Qwen
# + prioridad a documentos locales cuando existe evidencia semántica suficiente
# + soporte de consultas mixtas entre biblioteca académica y técnica
# + selección semántica de una o dos colecciones técnicas relevantes
# + estimación interna de confianza de las fuentes recuperadas
# + detección de nuevas versiones de PDF con opción de reemplazar la anterior sin borrar el archivo
# + panel de diagnóstico para ver la última decisión de enrutamiento
# v2.7.0: biblioteca técnica separada para libros/manuales de referencia
# + consultas de Python usan automáticamente libros técnicos locales antes que conocimiento general
# + las fuentes técnicas quedan ocultas en la explicación y solo se muestran si el Señor las solicita
# + contexto técnico persistente para seguimientos como "dame un ejemplo" o "profundiza"
# + índice vectorial persistente en SSD: carga vectores/metadatos sin levantar SentenceTransformer al iniciar
# + libros técnicos y apuntes académicos comparten motor semántico, pero no se mezclan por defecto
# v2.7.1: respaldos automáticos consistentes de beta.db usando SQLite Backup API
# + conserva beta.py, índice vectorial y manifiesto de biblioteca en archivos ZIP rotativos
# + respaldo diario configurable, retención automática y verificación de integridad
# + no duplica modelos ni PDFs en cada copia para evitar crecimiento innecesario del SSD
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent
CARPETA_MODELO = BASE_DIR / "modelo-es"
BASE_DATOS = BASE_DIR / "beta.db"
# No se fija una letra de unidad: si la carpeta Beta se mueve de C: a A:,
# todas las rutas internas siguen automáticamente la ubicación de beta.py.

# Voz neuronal local Piper / Daniela High.
# Los archivos deben estar dentro de: Beta\daniela\
PIPER_MODELO = BASE_DIR / "daniela" / "es_AR-daniela-high.onnx"
PIPER_CONFIG = BASE_DIR / "daniela" / "es_AR-daniela-high.onnx.json"

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
OLLAMA_MODEL = "qwen3:4b-instruct"
OLLAMA_TIMEOUT = 35
CLIMA_TIMEOUT = 6
CLIMA_CACHE_SEGUNDOS = 300
PRONOSTICO_CACHE_SEGUNDOS = 900
PROCESO_MAX_SEGUNDOS = 45

# Reconocimiento de voz híbrido.
# Vosk sigue escuchando de forma continua porque consume pocos recursos.
# Cuando detecta una frase dirigida a Beta, Faster-Whisper vuelve a
# transcribir ese mismo audio con mucha mayor precisión.
USAR_WHISPER = True
WHISPER_MODEL = "small"
WHISPER_REPO = "Systran/faster-whisper-small"
CARPETA_WHISPER = BASE_DIR / "modelo-whisper-small"
WHISPER_DEVICE = "cpu"
WHISPER_COMPUTE_TYPE = "int8"
WHISPER_LANGUAGE = "es"
WHISPER_BEAM_SIZE = 1

# Reconocimiento biométrico de hablante (speaker verification).
# El modelo se descarga una vez y luego funciona localmente.
USAR_RECONOCIMIENTO_HABLANTE = True
HABLANTE_REPO = "speechbrain/spkrec-ecapa-voxceleb"
CARPETA_HABLANTE = BASE_DIR / "modelo-hablante-ecapa"
HABLANTE_FRECUENCIA = 16000
HABLANTE_MUESTRAS_REGISTRO = 3
HABLANTE_SEGUNDOS_MUESTRA = 4
HABLANTE_UMBRAL_DEFECTO = 0.48
HABLANTE_MIN_SEGUNDOS = 0.30
HABLANTE_UMBRAL_SEGUIMIENTO_CORTO = 0.25
HABLANTE_SESION_CONFIABLE_SEGUNDOS = 90
HABLANTE_MAX_PALABRAS_SEGUIMIENTO_CORTO = 6
# La biometría de privacidad se fuerza si existe al menos una voz registrada.
HABLANTE_BIOMETRIA_PRIVACIDAD_OBLIGATORIA = True
# Evita procesar audio acumulado durante una transcripción Whisper lenta.
AUDIO_VACIAR_COLA_TRAS_WHISPER = True
# Filtro conservador de frases boilerplate que Whisper suele alucinar con TV/ruido.
ASR_FILTRAR_BOILERPLATE = True

# Ajustes de baja latencia.
OLLAMA_KEEP_ALIVE = "30m"
OLLAMA_NUM_CTX = 1536
OLLAMA_NUM_PREDICT = 90
PREFETCH_CLIMA_MS = 300000  # 5 minutos

# Investigación web. DDGS se importa de forma diferida para que Beta pueda
# iniciar incluso si el paquete todavía no está instalado.
WEB_REGION = "cl-es"
WEB_TIMEOUT = 8
WEB_MAX_RESULTADOS = 5
WEB_CACHE_SEGUNDOS = 600
WEB_CONTEXTO_SEGUNDOS = 600

# Spotify v2.6.4. Abrir y buscar funciona sin conectar la cuenta.
# Para controlar reproducción y leer preferencias, Beta usa la Web API con
# Authorization Code + PKCE; una app de escritorio no necesita Client Secret.
SPOTIFY_API_BASE = "https://api.spotify.com/v1"
SPOTIFY_ACCOUNTS_BASE = "https://accounts.spotify.com"
SPOTIFY_REDIRECT_URI = "http://127.0.0.1:8888/callback"
SPOTIFY_CALLBACK_HOST = "127.0.0.1"
SPOTIFY_CALLBACK_PORT = 8888
SPOTIFY_TIMEOUT = 10
SPOTIFY_SCOPES = (
    "user-read-playback-state "
    "user-modify-playback-state "
    "user-top-read "
    "playlist-read-private"
)

# Iniciativa conversacional. Beta habla muy ocasionalmente y solo cuando
# el modo compañera está activado.
INICIATIVA_MIN_SEGUNDOS = 30 * 60
INICIATIVA_MAX_SEGUNDOS = 55 * 60
INICIATIVA_SIN_VOZ_SEGUNDOS = 10 * 60
INICIATIVA_HORA_INICIO = 9
INICIATIVA_HORA_FIN = 22

# Aprendizaje curioso v2.6.0. Beta puede hacer preguntas breves para conocer
# mejor al Señor, pero sin convertir el escritorio en una entrevista constante.
# Las preguntas espontáneas son locales (Qwen) y nunca consultan Internet.
CURIOSIDAD_MIN_SEGUNDOS = 12 * 60
CURIOSIDAD_MAX_SEGUNDOS = 24 * 60
CURIOSIDAD_RESPUESTA_SEGUNDOS = 55
CURIOSIDAD_MAX_PREGUNTAS_DIA = 5
CURIOSIDAD_MIN_INTERACCIONES = 3
CURIOSIDAD_HORA_INICIO = 9
CURIOSIDAD_HORA_FIN = 22

# Unidad de aprendizaje adaptativo v2.6.2. El dominio no aumenta por el simple
# hecho de escuchar una explicación: solo cambia con autoevaluaciones explícitas
# o respuestas a preguntas de evaluación.
APRENDIZAJE_ADAPTATIVO_ACTIVO = True
EVALUACION_RESPUESTA_SEGUNDOS = 120
EVALUACION_FUENTES = 3
EVALUACION_TOKENS_PREGUNTA = 150
EVALUACION_TOKENS_CORRECCION = 180
APRENDIZAJE_MAX_EVENTOS_UI = 200

# Memoria inteligente. El análisis se ejecuta en segundo plano y solo cuando
# Beta lleva unos segundos sin recibir una nueva orden, para no aumentar la
# latencia de las respuestas principales.
MEMORIA_INTELIGENTE_ESPERA = 18
MEMORIA_INTELIGENTE_MIN_PALABRAS = 4
RESUMEN_CONVERSACION_CADA_TURNOS = 8
CONTEXTO_CONVERSACION_SEGUNDOS = 20 * 60

# Biblioteca académica local (RAG).
# El modelo de embeddings se descarga una sola vez y luego queda guardado
# dentro de la carpeta de Beta para consultas sin Internet.
BIBLIOTECA_DIR = BASE_DIR / "biblioteca"
BIBLIOTECA_DOCUMENTOS_DIR = BIBLIOTECA_DIR / "documentos"
BIBLIOTECA_TECNICA_DIR = BIBLIOTECA_DIR / "tecnica"
INDICES_DIR = BASE_DIR / "indices"
INDICE_MATRIZ_ARCHIVO = INDICES_DIR / "biblioteca_vectores.npy"
INDICE_META_ARCHIVO = INDICES_DIR / "biblioteca_meta.json"
INDICE_FIRMA_ARCHIVO = INDICES_DIR / "biblioteca_firma.json"

# Respaldos v2.7.1. Los ZIP automáticos protegen el estado vivo de Beta sin
# multiplicar el tamaño de los modelos o de todos los PDF en cada copia.
RESPALDOS_DIR = BASE_DIR / "respaldos"
RESPALDO_INTERVALO_SEGUNDOS = 24 * 60 * 60
RESPALDO_REVISION_MS = 60 * 60 * 1000
RESPALDO_INICIO_MS = 15 * 1000
RESPALDO_RETENCION = 10
RESPALDO_ESPACIO_MINIMO_MB = 300
RESPALDO_INCLUIR_INDICES = True
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
CARPETA_EMBEDDINGS = BASE_DIR / "modelo-embeddings-academico"
BIBLIOTECA_CHUNK_MAX = 1050
BIBLIOTECA_CHUNK_OVERLAP = 180
BIBLIOTECA_RESULTADOS = 5
BIBLIOTECA_UMBRAL_MIN = 0.27
BIBLIOTECA_UMBRAL_FUERTE = 0.38
BIBLIOTECA_CONTEXTO_SEGUNDOS = 20 * 60

# Biblioteca técnica / libros de referencia.
TECNICA_UMBRAL_MIN = 0.27
TECNICA_UMBRAL_FUERTE = 0.38
TECNICA_RESULTADOS = 5
TECNICA_FUENTES_BREVE = 3
TECNICA_FUENTES_PROFUNDO = 4
TECNICA_TOKENS_BREVE = 110
TECNICA_TOKENS_PROFUNDO = 230
TECNICA_NUM_CTX_BREVE = 1280
TECNICA_NUM_CTX_PROFUNDO = 1664
TECNICA_CONTEXTO_SEGUNDOS = 25 * 60

# Biblioteca inteligente v2.8. La decisión se apoya primero en similitud semántica
# y solo usa reglas léxicas como refuerzo. Los umbrales son conservadores para
# evitar que una conversación casual sea secuestrada por el RAG.
BIBLIOTECA_INTELIGENTE_ACTIVA = True
BIBLIOTECA_ROUTER_RESULTADOS = 10
BIBLIOTECA_ROUTER_UMBRAL_MIN = 0.30
BIBLIOTECA_ROUTER_UMBRAL_MEDIO = 0.36
BIBLIOTECA_ROUTER_UMBRAL_ALTO = 0.48
BIBLIOTECA_ROUTER_MARGEN_MIXTO = 0.045
BIBLIOTECA_ROUTER_MARGEN_COLECCION = 0.055
BIBLIOTECA_ROUTER_MAX_COLECCIONES = 2
# v2.8.1: cada biblioteca se consulta por separado durante el enrutamiento. Esto evita
# que, por ejemplo, varios fragmentos de Python desplacen por completo resultados de
# Arquitectura de Computadores antes de que Beta pueda compararlos.
BIBLIOTECA_ROUTER_RESULTADOS_POR_CATEGORIA = 8
BIBLIOTECA_ROUTER_MARGEN_MIXTO_ROBUSTO = 0.060
BIBLIOTECA_ROUTER_MAX_GRUPO = 4
BIBLIOTECA_INTELIGENTE_CONTEXTO_SEGUNDOS = 25 * 60

# Respuesta académica oral: breve por defecto para que Beta se sienta
# conversacional. El Señor puede decir "profundiza", "explícalo en detalle"
# o equivalentes para obtener una respuesta más extensa.
ACADEMICO_TOKENS_BREVE = 72
ACADEMICO_TOKENS_PROFUNDO = 210
ACADEMICO_FUENTES_BREVE = 2
ACADEMICO_FUENTES_PROFUNDO = 3
# Un contexto más pequeño reduce el prompt-eval de Qwen en consultas breves.
# Las respuestas profundas conservan más margen para no perder precisión.
ACADEMICO_NUM_CTX_BREVE = 1024
ACADEMICO_NUM_CTX_PROFUNDO = 1408

# Streaming local: Qwen entrega texto por fragmentos. Beta empieza a sintetizar
# la primera frase antes de que termine de generarse toda la respuesta.
STREAMING_OLLAMA_ACTIVO = True
STREAMING_MIN_CARACTERES_FRASE = 28
STREAMING_CORTE_LARGO = 190
# Para garantizar cierres naturales, v2.5.3 prioriza oraciones completas.
STREAMING_CORTE_INTERMEDIO = False
STREAMING_DESCARTAR_COLA_INCOMPLETA = True

# OCR académico para PDF sin capa de texto.
# Beta intenta primero extraer texto normalmente. Solo aplica OCR a las páginas
# que no contienen suficiente texto real, lo que reduce mucho el tiempo de proceso.
OCR_ACTIVO = True
OCR_DPI = 200
OCR_MIN_CARACTERES_DIRECTOS = 45
OCR_MIN_CARACTERES_VALIDOS = 25
OCR_IDIOMA_PREFERIDO = "spa"
OCR_CONFIG_PRINCIPAL = "--oem 3 --psm 3 -c preserve_interword_spaces=1"
OCR_CONFIG_REINTENTO = "--oem 3 --psm 6 -c preserve_interword_spaces=1"


TAMANO_INICIAL = 220
TAMANO_MINIMO = 120
TAMANO_MAXIMO = 420
PASO_TAMANO = 20

TIEMPO_IMPACIENCIA = 15
# Privacidad de escucha v2.5.4. En modo estricto NO se abren ventanas
# automáticas después de cada respuesta. "Beta" sola habilita únicamente una
# ventana corta para dictar la orden siguiente. El modo conversación debe
# activarse explícitamente y vuelve a estricto tras un periodo de silencio.
TIEMPO_CONVERSACION = 35  # compatibilidad interna; no abre escucha libre en modo estricto
TIEMPO_ORDEN_TRAS_WAKE = 15
TIEMPO_MODO_CONVERSACION_SILENCIO = 60
TIEMPO_CONVERSACION_POST_RESPUESTA = 55  # legado, no usado en modo estricto
TIEMPO_CONVERSACION_ACADEMICA = 90  # legado, no usado en modo estricto

COLOR_TRANSPARENTE = "#010101"
COLOR_BORDE_OSCURO = "#063C67"
COLOR_BORDE_MEDIO = "#075B88"
COLOR_CUERPO = "#0695C4"
COLOR_CUERPO_CLARO = "#19A9D0"
COLOR_LUZ = "#48C5E5"
COLOR_LUZ_SUAVE = "#87D9EE"
COLOR_REFLEJO = "#C4F2FF"
COLOR_REFLEJO_INFERIOR = "#66D5EB"
COLOR_SOMBRA_OJO = "#0780A5"
COLOR_BLANCO = "#FFFFFF"
COLOR_IRIS = "#2C2928"
COLOR_PUPILA = "#050505"
COLOR_REFLEJO_PUPILA = "#FFFFFF"
COLOR_REFLEJO_PUPILA_2 = "#AFC7D1"
COLOR_BOCA = "#092A37"
COLOR_BOCA_BRILLO = "#60D6E9"
COLOR_CEJA = "#07516E"


# ==========================================================
# UTILIDADES
# ==========================================================

def normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFD", (texto or "").lower().strip())
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = re.sub(r"[^\w\s]", "", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()


def buscar_modelo_vosk():
    if not CARPETA_MODELO.exists():
        return None

    if (CARPETA_MODELO / "am").exists() and (CARPETA_MODELO / "conf").exists():
        return CARPETA_MODELO

    for carpeta in CARPETA_MODELO.iterdir():
        if (
            carpeta.is_dir()
            and (carpeta / "am").exists()
            and (carpeta / "conf").exists()
        ):
            return carpeta

    return None


def obtener_escritorio():
    try:
        buffer = ctypes.create_unicode_buffer(260)
        ctypes.windll.shell32.SHGetFolderPathW(None, 0x10, None, 0, buffer)
        ruta = Path(buffer.value)
        if ruta.exists():
            return ruta
    except Exception:
        pass

    posibles = [
        Path.home() / "Desktop",
        Path.home() / "Escritorio",
        Path.home() / "OneDrive" / "Desktop",
        Path.home() / "OneDrive" / "Escritorio",
    ]

    for ruta in posibles:
        if ruta.exists():
            return ruta

    return Path.home()


# ==========================================================
# MEMORIA / BASE DE DATOS
# Cada operación abre su conexión para evitar problemas
# entre los hilos de voz, clima e IA.
# ==========================================================

class MemoriaBeta:
    def __init__(self):
        self.crear_tablas()
        self.crear_identidad()

    def conectar(self):
        return sqlite3.connect(BASE_DATOS, timeout=15)

    def crear_tablas(self):
        with self.conectar() as con:
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS recuerdos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    contenido TEXT NOT NULL,
                    contenido_normalizado TEXT NOT NULL,
                    fecha TEXT NOT NULL,
                    importancia INTEGER DEFAULT 1
                )
                """
            )

            con.execute(
                """
                CREATE TABLE IF NOT EXISTS conversaciones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    autor TEXT NOT NULL,
                    mensaje TEXT NOT NULL,
                    fecha TEXT NOT NULL
                )
                """
            )

            con.execute(
                """
                CREATE TABLE IF NOT EXISTS estado (
                    clave TEXT PRIMARY KEY,
                    valor TEXT
                )
                """
            )

            con.execute(
                """
                CREATE TABLE IF NOT EXISTS comandos_personalizados (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    frase TEXT NOT NULL UNIQUE,
                    frase_normalizada TEXT NOT NULL UNIQUE,
                    respuesta TEXT NOT NULL,
                    fecha TEXT NOT NULL
                )
                """
            )

            con.execute(
                """
                CREATE TABLE IF NOT EXISTS resumenes_conversacion (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    resumen TEXT NOT NULL,
                    tema TEXT DEFAULT '',
                    fecha TEXT NOT NULL,
                    turnos INTEGER DEFAULT 0,
                    activo INTEGER DEFAULT 1
                )
                """
            )

            con.execute(
                """
                CREATE TABLE IF NOT EXISTS voces_autorizadas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL UNIQUE,
                    embedding_json TEXT NOT NULL,
                    muestras INTEGER DEFAULT 1,
                    fecha TEXT NOT NULL,
                    activo INTEGER DEFAULT 1
                )
                """
            )

            con.execute(
                """
                CREATE TABLE IF NOT EXISTS curiosidad_historial (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pregunta TEXT NOT NULL,
                    pregunta_normalizada TEXT NOT NULL,
                    tema TEXT DEFAULT '',
                    tipo TEXT DEFAULT 'dato',
                    fecha TEXT NOT NULL,
                    respondida INTEGER DEFAULT 0,
                    respuesta TEXT DEFAULT '',
                    fecha_respuesta TEXT DEFAULT ''
                )
                """
            )

            con.execute(
                """
                CREATE TABLE IF NOT EXISTS aprendizaje_academico (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ramo TEXT NOT NULL,
                    ramo_normalizado TEXT NOT NULL,
                    tema TEXT NOT NULL,
                    tema_normalizado TEXT NOT NULL,
                    dominio REAL DEFAULT 0,
                    evidencias INTEGER DEFAULT 0,
                    exposiciones INTEGER DEFAULT 0,
                    aciertos INTEGER DEFAULT 0,
                    errores INTEGER DEFAULT 0,
                    ultima_fecha TEXT DEFAULT '',
                    ultima_evidencia TEXT DEFAULT '',
                    UNIQUE(ramo_normalizado, tema_normalizado)
                )
                """
            )
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS aprendizaje_eventos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ramo TEXT NOT NULL,
                    tema TEXT NOT NULL,
                    tipo TEXT NOT NULL,
                    puntuacion REAL,
                    detalle TEXT DEFAULT '',
                    fecha TEXT NOT NULL
                )
                """
            )
            con.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_aprendizaje_eventos_ramo_tema
                ON aprendizaje_eventos(ramo, tema)
                """
            )

            # Migración automática de memorias antiguas. No borra beta.db.
            columnas = {fila[1] for fila in con.execute("PRAGMA table_info(recuerdos)").fetchall()}
            migraciones = {
                "tipo": "TEXT DEFAULT 'dato'",
                "etiquetas": "TEXT DEFAULT ''",
                "veces_usado": "INTEGER DEFAULT 0",
                "ultima_consulta": "TEXT DEFAULT ''",
                "activo": "INTEGER DEFAULT 1",
                "fuente": "TEXT DEFAULT 'manual'",
                "confianza": "REAL DEFAULT 1.0",
                "tema": "TEXT DEFAULT ''",
                "actualizado": "TEXT DEFAULT ''",
            }
            for columna, definicion in migraciones.items():
                if columna not in columnas:
                    con.execute(f"ALTER TABLE recuerdos ADD COLUMN {columna} {definicion}")

    def crear_identidad(self):
        valores = {
            "nombre": "Beta",
            "tipo": "asistente personal local",
            "usuario": "Señor",
            "fecha_creacion": datetime.now().strftime("%d/%m/%Y"),
            "energia": "80",
            "curiosidad": "70",
            "confianza": "50",
            "humor": "62",
            "familiaridad": "25",
            "serenidad": "72",
            "interacciones": "0",
            "tamano_beta": str(TAMANO_INICIAL),
            "ciudad_clima": "",
            "clima_lat": "",
            "clima_lon": "",
            "clima_nombre": "",
            "clima_region": "",
            "clima_cache_texto": "",
            "clima_cache_ts": "0",
            "pronostico_manana_cache_texto": "",
            "pronostico_manana_cache_ts": "0",
            "modo_aprendizaje_natural": "1",
            "modo_biblioteca_academica": "si_falta",
            "modo_memoria_inteligente": "1",
            "preguntas_seguimiento": "1",
            "contexto_tema": "",
            "contexto_resumen": "",
            "turnos_desde_resumen": "0",
            "ultima_memoria_iniciativa_id": "0",
            "modo_curioso": "1",
            "modo_aprendizaje_adaptativo": "1",
            "curiosidad_fecha_contador": "",
            "curiosidad_preguntas_hoy": "0",
            "respaldos_automaticos": "1",
            "ultimo_respaldo_ok": "",
            "pos_x": "",
            "pos_y": "",
        }

        with self.conectar() as con:
            for clave, valor in valores.items():
                con.execute(
                    "INSERT OR IGNORE INTO estado (clave, valor) VALUES (?, ?)",
                    (clave, valor),
                )

            # Migración de tratamiento: aunque beta.db venga de una versión anterior
            # donde el usuario era "Jefe", desde esta versión Beta lo llama "Señor".
            con.execute(
                "INSERT OR REPLACE INTO estado (clave, valor) VALUES (?, ?)",
                ("usuario", "Señor"),
            )

    # -------------------- recuerdos --------------------

    def clasificar_recuerdo(self, contenido):
        texto = normalizar(contenido)

        if any(p in texto for p in [
            "me gusta ", "prefiero ", "mi favorito", "mi favorita",
            "me encanta ", "no me gusta ",
        ]):
            return "preferencia"

        if any(p in texto for p in [
            "mi objetivo", "quiero aprender", "quiero lograr",
            "quiero mejorar", "mi meta",
        ]):
            return "objetivo"

        if any(p in texto for p in [
            "tengo pendiente", "debo hacer", "me falta",
            "mañana quiero", "manana quiero", "tenemos pendiente",
        ]):
            return "pendiente"

        if any(p in texto for p in [
            "estoy estudiando", "estoy aprendiendo", "estoy practicando",
            "estudio ", "aprendo ",
        ]):
            return "aprendizaje"

        if any(p in texto for p in [
            "mi proyecto", "estoy construyendo", "estoy desarrollando",
        ]):
            return "proyecto"

        return "dato"

    def extraer_etiquetas(self, contenido, maximo=8):
        palabras = normalizar(contenido).split()
        ignoradas = {
            "que", "como", "cual", "quien", "cuando", "donde", "sobre",
            "de", "del", "la", "el", "los", "las", "un", "una", "mi",
            "mis", "es", "son", "y", "a", "por", "para", "me", "te",
            "tu", "tus", "lo", "se", "con", "sin", "en", "al", "le",
            "quiero", "estoy", "tengo", "muy", "mas", "pero", "esto",
        }
        etiquetas = []
        for palabra in palabras:
            if len(palabra) < 3 or palabra in ignoradas or palabra in etiquetas:
                continue
            etiquetas.append(palabra)
            if len(etiquetas) >= maximo:
                break
        return ",".join(etiquetas)

    def guardar_recuerdo(
        self,
        contenido,
        importancia=1,
        tipo=None,
        etiquetas=None,
        fuente="manual",
        confianza=1.0,
        tema="",
    ):
        contenido = (contenido or "").strip()
        if not contenido:
            return False

        contenido_normalizado = normalizar(contenido)
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tipo = (tipo or self.clasificar_recuerdo(contenido)).strip().lower()
        etiquetas = etiquetas if etiquetas is not None else self.extraer_etiquetas(contenido)
        fuente = (fuente or "manual").strip().lower()
        tema = (tema or "").strip()
        try:
            confianza = max(0.0, min(1.0, float(confianza)))
        except Exception:
            confianza = 1.0

        with self.conectar() as con:
            existente = con.execute(
                "SELECT id FROM recuerdos WHERE contenido_normalizado = ? AND activo = 1",
                (contenido_normalizado,),
            ).fetchone()

            if existente:
                # Si el mismo recuerdo reaparece en una conversación, elevamos
                # ligeramente su importancia/confianza en vez de duplicarlo.
                con.execute(
                    """
                    UPDATE recuerdos
                    SET importancia = MAX(importancia, ?),
                        confianza = MAX(COALESCE(confianza, 0), ?),
                        actualizado = ?,
                        tema = CASE WHEN COALESCE(tema, '') = '' THEN ? ELSE tema END
                    WHERE id = ?
                    """,
                    (importancia, confianza, fecha, tema, existente[0]),
                )
                return False

            con.execute(
                """
                INSERT INTO recuerdos
                (contenido, contenido_normalizado, fecha, importancia, tipo, etiquetas,
                 veces_usado, ultima_consulta, activo, fuente, confianza, tema, actualizado)
                VALUES (?, ?, ?, ?, ?, ?, 0, '', 1, ?, ?, ?, ?)
                """,
                (
                    contenido,
                    contenido_normalizado,
                    fecha,
                    importancia,
                    tipo,
                    etiquetas,
                    fuente,
                    confianza,
                    tema,
                    fecha,
                ),
            )

        return True

    def buscar_recuerdos(self, consulta, limite=5, tipo=None):
        consulta_normalizada = normalizar(consulta)
        palabras = set(consulta_normalizada.split())

        ignoradas = {
            "que", "como", "cual", "quien", "cuando", "donde", "sobre",
            "sabes", "recuerdas", "recuerdo", "de", "del", "la", "el",
            "los", "las", "un", "una", "mi", "mis", "es", "son", "y",
            "a", "por", "para", "me", "te", "tu", "tus", "lo", "se",
            "tengo", "tenemos", "pendiente", "pendientes",
        }
        palabras -= ignoradas

        with self.conectar() as con:
            if tipo:
                recuerdos = con.execute(
                    """
                    SELECT id, contenido, contenido_normalizado, fecha, importancia,
                           tipo, etiquetas, veces_usado, ultima_consulta
                    FROM recuerdos
                    WHERE activo = 1 AND tipo = ?
                    ORDER BY importancia DESC, id DESC
                    """,
                    (tipo,),
                ).fetchall()
            else:
                recuerdos = con.execute(
                    """
                    SELECT id, contenido, contenido_normalizado, fecha, importancia,
                           tipo, etiquetas, veces_usado, ultima_consulta
                    FROM recuerdos
                    WHERE activo = 1
                    ORDER BY importancia DESC, id DESC
                    """
                ).fetchall()

        resultados = []

        for recuerdo in recuerdos:
            palabras_recuerdo = set(recuerdo[2].split())
            etiquetas_recuerdo = set((recuerdo[6] or "").split(","))
            coincidencias = len(palabras & palabras_recuerdo)
            coincidencias_etiquetas = len(palabras & etiquetas_recuerdo)
            puntuacion = coincidencias * 2 + coincidencias_etiquetas * 2

            if consulta_normalizada and consulta_normalizada in recuerdo[2]:
                puntuacion += 6

            # Si se pidió un tipo concreto, todos los recuerdos de esa categoría son candidatos.
            if tipo:
                puntuacion += 3

            # La importancia solo desempata recuerdos que ya resultaron pertinentes.
            if puntuacion > 0:
                puntuacion += min(3, int(recuerdo[4] or 1))
                resultados.append((puntuacion, recuerdo))

        resultados.sort(key=lambda x: (x[0], x[1][0]), reverse=True)
        seleccionados = [resultado[1] for resultado in resultados[:limite]]

        if seleccionados:
            fecha_consulta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with self.conectar() as con:
                for recuerdo in seleccionados:
                    con.execute(
                        """
                        UPDATE recuerdos
                        SET veces_usado = COALESCE(veces_usado, 0) + 1,
                            ultima_consulta = ?
                        WHERE id = ?
                        """,
                        (fecha_consulta, recuerdo[0]),
                    )

        return seleccionados

    def listar_recuerdos(self, limite=500):
        with self.conectar() as con:
            return con.execute(
                """
                SELECT id, contenido, fecha, importancia, tipo, etiquetas
                FROM recuerdos
                WHERE activo = 1
                ORDER BY id DESC
                LIMIT ?
                """,
                (limite,),
            ).fetchall()

    def ultimos_recuerdos(self, limite=5):
        with self.conectar() as con:
            return con.execute(
                """
                SELECT id, contenido, fecha
                FROM recuerdos
                WHERE activo = 1
                ORDER BY id DESC
                LIMIT ?
                """,
                (limite,),
            ).fetchall()

    def eliminar_recuerdo_id(self, recuerdo_id):
        with self.conectar() as con:
            con.execute("DELETE FROM recuerdos WHERE id = ?", (recuerdo_id,))

    def olvidar(self, consulta):
        resultados = self.buscar_recuerdos(consulta, 1)
        if not resultados:
            return None

        recuerdo = resultados[0]
        self.eliminar_recuerdo_id(recuerdo[0])
        return recuerdo[1]

    def recuerdos_por_tipo(self, tipo, limite=8):
        with self.conectar() as con:
            return con.execute(
                """
                SELECT id, contenido, fecha, importancia, tipo
                FROM recuerdos
                WHERE activo = 1 AND tipo = ?
                ORDER BY importancia DESC, id DESC
                LIMIT ?
                """,
                (tipo, limite),
            ).fetchall()

    def contar_recuerdos_por_tipo(self):
        with self.conectar() as con:
            return dict(
                con.execute(
                    """
                    SELECT tipo, COUNT(*)
                    FROM recuerdos
                    WHERE activo = 1
                    GROUP BY tipo
                    """
                ).fetchall()
            )

    def completar_pendiente(self, consulta):
        candidatos = self.buscar_recuerdos(consulta, limite=3, tipo="pendiente")
        if not candidatos:
            return None
        recuerdo = candidatos[0]
        with self.conectar() as con:
            con.execute(
                "UPDATE recuerdos SET tipo = 'completado', importancia = 1 WHERE id = ?",
                (recuerdo[0],),
            )
        return recuerdo[1]

    # -------------------- conversaciones --------------------

    def guardar_conversacion(self, autor, mensaje):
        with self.conectar() as con:
            con.execute(
                """
                INSERT INTO conversaciones (autor, mensaje, fecha)
                VALUES (?, ?, ?)
                """,
                (
                    autor,
                    mensaje,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ),
            )

    def historial_reciente(self, limite=10):
        with self.conectar() as con:
            filas = con.execute(
                """
                SELECT autor, mensaje, fecha
                FROM conversaciones
                ORDER BY id DESC
                LIMIT ?
                """,
                (limite,),
            ).fetchall()

        filas.reverse()
        return filas

    def guardar_resumen_conversacion(self, resumen, tema="", turnos=0):
        resumen = (resumen or "").strip()
        tema = (tema or "").strip()
        if not resumen:
            return False

        # Evitar guardar dos resúmenes exactamente iguales.
        resumen_normal = normalizar(resumen)
        with self.conectar() as con:
            ultimo = con.execute(
                """
                SELECT resumen
                FROM resumenes_conversacion
                WHERE activo = 1
                ORDER BY id DESC
                LIMIT 1
                """
            ).fetchone()
            if ultimo and normalizar(ultimo[0]) == resumen_normal:
                return False

            con.execute(
                """
                INSERT INTO resumenes_conversacion (resumen, tema, fecha, turnos, activo)
                VALUES (?, ?, ?, ?, 1)
                """,
                (
                    resumen,
                    tema,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    int(turnos or 0),
                ),
            )
        return True

    def ultimo_resumen_conversacion(self):
        with self.conectar() as con:
            return con.execute(
                """
                SELECT id, resumen, tema, fecha, turnos
                FROM resumenes_conversacion
                WHERE activo = 1
                ORDER BY id DESC
                LIMIT 1
                """
            ).fetchone()

    def listar_resumenes_conversacion(self, limite=20):
        with self.conectar() as con:
            return con.execute(
                """
                SELECT id, resumen, tema, fecha, turnos
                FROM resumenes_conversacion
                WHERE activo = 1
                ORDER BY id DESC
                LIMIT ?
                """,
                (limite,),
            ).fetchall()

    def contar_conversaciones(self):
        with self.conectar() as con:
            fila = con.execute("SELECT COUNT(*) FROM conversaciones").fetchone()
        return int(fila[0]) if fila else 0

    def recuerdos_para_iniciativa(self, limite=8):
        """Recuerdos apropiados para retomar espontáneamente.

        Se priorizan objetivos, aprendizajes, pendientes, proyectos y preferencias.
        Los datos puramente administrativos quedan con menor prioridad.
        """
        prioridades = {
            "pendiente": 6,
            "objetivo": 5,
            "aprendizaje": 5,
            "proyecto": 4,
            "preferencia": 3,
            "dato": 1,
        }
        with self.conectar() as con:
            filas = con.execute(
                """
                SELECT id, contenido, fecha, importancia, tipo, tema,
                       COALESCE(veces_usado, 0), COALESCE(ultima_consulta, '')
                FROM recuerdos
                WHERE activo = 1 AND tipo != 'completado'
                ORDER BY id DESC
                LIMIT 80
                """
            ).fetchall()

        puntuados = []
        ultimo_id = 0
        try:
            ultimo_id = int(self.obtener_estado("ultima_memoria_iniciativa_id", "0") or 0)
        except Exception:
            ultimo_id = 0

        for fila in filas:
            rid, contenido, fecha, importancia, tipo, tema, veces_usado, ultima_consulta = fila
            if rid == ultimo_id:
                continue
            puntaje = prioridades.get((tipo or "dato").lower(), 1)
            puntaje += min(3, int(importancia or 1))
            # Los recuerdos menos usados tienen un poco más de oportunidad de reaparecer.
            puntaje -= min(2, int(veces_usado or 0) // 5)
            puntuados.append((puntaje, fila))

        puntuados.sort(key=lambda x: (x[0], x[1][0]), reverse=True)
        return [fila for _p, fila in puntuados[:limite]]

    # -------------------- curiosidad --------------------

    def registrar_pregunta_curiosa(self, pregunta, tema="", tipo="dato"):
        pregunta = (pregunta or "").strip()
        if not pregunta:
            return 0
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pn = normalizar(pregunta)
        with self.conectar() as con:
            cur = con.execute(
                """
                INSERT INTO curiosidad_historial
                (pregunta, pregunta_normalizada, tema, tipo, fecha, respondida, respuesta, fecha_respuesta)
                VALUES (?, ?, ?, ?, ?, 0, '', '')
                """,
                (pregunta, pn, (tema or "").strip(), (tipo or "dato").strip(), fecha),
            )
            return int(cur.lastrowid or 0)

    def marcar_pregunta_curiosa_respondida(self, pregunta_id, respuesta):
        if not pregunta_id:
            return
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.conectar() as con:
            con.execute(
                """
                UPDATE curiosidad_historial
                SET respondida = 1, respuesta = ?, fecha_respuesta = ?
                WHERE id = ?
                """,
                ((respuesta or "").strip(), fecha, int(pregunta_id)),
            )

    def ultimas_preguntas_curiosas(self, limite=20):
        with self.conectar() as con:
            return con.execute(
                """
                SELECT id, pregunta, tema, tipo, fecha, respondida, respuesta
                FROM curiosidad_historial
                ORDER BY id DESC
                LIMIT ?
                """,
                (int(limite),),
            ).fetchall()

    def recuerdos_por_fuente(self, fuente, limite=8):
        with self.conectar() as con:
            return con.execute(
                """
                SELECT id, contenido, contenido_normalizado, fecha, importancia, tipo,
                       etiquetas, tema, confianza
                FROM recuerdos
                WHERE activo = 1 AND fuente = ?
                ORDER BY importancia DESC, id DESC
                LIMIT ?
                """,
                ((fuente or "").strip().lower(), int(limite)),
            ).fetchall()

    # -------------------- unidad de aprendizaje adaptativo --------------------

    def registrar_evento_aprendizaje(self, ramo, tema, tipo, puntuacion=None, detalle=""):
        """Registra evidencia académica sin confundir exposición con dominio."""
        ramo = (ramo or "General").strip() or "General"
        tema = (tema or ramo).strip() or ramo
        rn, tn = normalizar(ramo), normalizar(tema)
        if not rn or not tn:
            return None
        tipo = (tipo or "exposicion").strip().lower()
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        muestra, peso = None, 0.0
        if tipo == "comprendido":
            muestra, peso = 80.0, 0.22
        elif tipo == "dificultad":
            muestra, peso = 35.0, 0.28
        elif tipo == "evaluacion" and puntuacion is not None:
            try:
                muestra = max(0.0, min(100.0, float(puntuacion)))
                peso = 0.38
            except Exception:
                muestra = None

        with self.conectar() as con:
            fila = con.execute(
                """SELECT id, dominio, evidencias, exposiciones, aciertos, errores
                   FROM aprendizaje_academico
                   WHERE ramo_normalizado = ? AND tema_normalizado = ?""",
                (rn, tn),
            ).fetchone()
            if fila:
                rid, dominio, evidencias, exposiciones, aciertos, errores = fila
                dominio = float(dominio or 0); evidencias = int(evidencias or 0)
                exposiciones = int(exposiciones or 0) + 1
                aciertos = int(aciertos or 0); errores = int(errores or 0)
                nuevo_dominio, nuevas_evidencias = dominio, evidencias
                if muestra is not None:
                    nuevo_dominio = muestra if evidencias <= 0 else dominio * (1.0-peso) + muestra * peso
                    nuevas_evidencias += 1
                    if muestra >= 70: aciertos += 1
                    elif muestra <= 45: errores += 1
                con.execute(
                    """UPDATE aprendizaje_academico
                       SET ramo=?, tema=?, dominio=?, evidencias=?, exposiciones=?, aciertos=?, errores=?,
                           ultima_fecha=?, ultima_evidencia=? WHERE id=?""",
                    (ramo, tema, float(nuevo_dominio), nuevas_evidencias, exposiciones,
                     aciertos, errores, fecha, (detalle or tipo)[:500], int(rid)),
                )
            else:
                dominio_inicial = float(muestra) if muestra is not None else 0.0
                evidencias_iniciales = 1 if muestra is not None else 0
                aciertos = 1 if muestra is not None and muestra >= 70 else 0
                errores = 1 if muestra is not None and muestra <= 45 else 0
                con.execute(
                    """INSERT INTO aprendizaje_academico
                       (ramo, ramo_normalizado, tema, tema_normalizado, dominio, evidencias,
                        exposiciones, aciertos, errores, ultima_fecha, ultima_evidencia)
                       VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?, ?, ?)""",
                    (ramo, rn, tema, tn, dominio_inicial, evidencias_iniciales,
                     aciertos, errores, fecha, (detalle or tipo)[:500]),
                )
            con.execute(
                """INSERT INTO aprendizaje_eventos
                   (ramo, tema, tipo, puntuacion, detalle, fecha) VALUES (?, ?, ?, ?, ?, ?)""",
                (ramo, tema, tipo, None if puntuacion is None else float(puntuacion),
                 (detalle or "")[:1200], fecha),
            )
        return self.obtener_progreso_tema(ramo, tema)

    def obtener_progreso_tema(self, ramo, tema):
        rn, tn = normalizar(ramo or "General"), normalizar(tema or ramo or "General")
        with self.conectar() as con:
            return con.execute(
                """SELECT ramo, tema, dominio, evidencias, exposiciones, aciertos, errores,
                          ultima_fecha, ultima_evidencia
                   FROM aprendizaje_academico
                   WHERE ramo_normalizado=? AND tema_normalizado=?""",
                (rn, tn),
            ).fetchone()

    def listar_progreso_academico(self, limite=200):
        with self.conectar() as con:
            return con.execute(
                """SELECT ramo, tema, dominio, evidencias, exposiciones, aciertos, errores,
                          ultima_fecha, ultima_evidencia
                   FROM aprendizaje_academico
                   ORDER BY ultima_fecha DESC, ramo COLLATE NOCASE, tema COLLATE NOCASE
                   LIMIT ?""", (int(limite),)
            ).fetchall()

    def resumen_progreso_por_ramo(self):
        with self.conectar() as con:
            return con.execute(
                """SELECT ramo, SUM(exposiciones), SUM(evidencias),
                          CASE WHEN SUM(evidencias)>0 THEN SUM(dominio*evidencias)/SUM(evidencias) ELSE 0 END,
                          MAX(ultima_fecha)
                   FROM aprendizaje_academico
                   GROUP BY ramo_normalizado
                   ORDER BY MAX(ultima_fecha) DESC"""
            ).fetchall()

    def temas_para_repasar(self, limite=5):
        with self.conectar() as con:
            return con.execute(
                """SELECT ramo, tema, dominio, evidencias, exposiciones, aciertos, errores, ultima_fecha
                   FROM aprendizaje_academico
                   WHERE evidencias > 0
                   ORDER BY dominio ASC, errores DESC, ultima_fecha ASC
                   LIMIT ?""", (int(limite),)
            ).fetchall()

    def ultimos_eventos_aprendizaje(self, limite=30):
        with self.conectar() as con:
            return con.execute(
                """SELECT ramo, tema, tipo, puntuacion, detalle, fecha
                   FROM aprendizaje_eventos ORDER BY id DESC LIMIT ?""", (int(limite),)
            ).fetchall()

    # -------------------- estado --------------------

    def obtener_estado(self, clave, defecto=None):
        with self.conectar() as con:
            resultado = con.execute(
                "SELECT valor FROM estado WHERE clave = ?",
                (clave,),
            ).fetchone()

        return resultado[0] if resultado else defecto

    def cambiar_estado(self, clave, valor):
        with self.conectar() as con:
            con.execute(
                "INSERT OR REPLACE INTO estado (clave, valor) VALUES (?, ?)",
                (clave, str(valor)),
            )

    def registrar_interaccion(self):
        actual = int(self.obtener_estado("interacciones", "0")) + 1
        self.cambiar_estado("interacciones", actual)

        # Estos valores son parámetros de comportamiento, no emociones reales.
        if actual % 4 == 0:
            familiaridad = min(100, int(self.obtener_estado("familiaridad", "25")) + 1)
            self.cambiar_estado("familiaridad", familiaridad)

        if actual % 5 == 0:
            confianza = min(100, int(self.obtener_estado("confianza", "50")) + 1)
            self.cambiar_estado("confianza", confianza)

        if actual % 8 == 0:
            curiosidad = min(100, int(self.obtener_estado("curiosidad", "70")) + 1)
            self.cambiar_estado("curiosidad", curiosidad)

    def obtener_perfil(self):
        claves = ["energia", "curiosidad", "confianza", "humor", "familiaridad", "serenidad"]
        perfil = {}
        for clave in claves:
            try:
                perfil[clave] = int(self.obtener_estado(clave, "50"))
            except Exception:
                perfil[clave] = 50
        perfil["interacciones"] = int(self.obtener_estado("interacciones", "0"))
        return perfil

    # -------------------- comandos personalizados --------------------

    def guardar_comando(self, frase, respuesta):
        frase = (frase or "").strip()
        respuesta = (respuesta or "").strip()

        if not frase or not respuesta:
            return False

        frase_normalizada = normalizar(frase)
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            with self.conectar() as con:
                con.execute(
                    """
                    INSERT INTO comandos_personalizados
                    (frase, frase_normalizada, respuesta, fecha)
                    VALUES (?, ?, ?, ?)
                    """,
                    (frase, frase_normalizada, respuesta, fecha),
                )
            return True
        except sqlite3.IntegrityError:
            with self.conectar() as con:
                con.execute(
                    """
                    UPDATE comandos_personalizados
                    SET frase = ?, respuesta = ?, fecha = ?
                    WHERE frase_normalizada = ?
                    """,
                    (frase, respuesta, fecha, frase_normalizada),
                )
            return True

    def listar_comandos(self):
        with self.conectar() as con:
            return con.execute(
                """
                SELECT id, frase, respuesta, fecha
                FROM comandos_personalizados
                ORDER BY id DESC
                """
            ).fetchall()

    def eliminar_comando_id(self, comando_id):
        with self.conectar() as con:
            con.execute(
                "DELETE FROM comandos_personalizados WHERE id = ?",
                (comando_id,),
            )

    def buscar_comando(self, frase):
        frase_norm = normalizar(frase)

        with self.conectar() as con:
            exacto = con.execute(
                """
                SELECT id, frase, respuesta
                FROM comandos_personalizados
                WHERE frase_normalizada = ?
                """,
                (frase_norm,),
            ).fetchone()

            if exacto:
                return exacto

            comandos = con.execute(
                """
                SELECT id, frase, frase_normalizada, respuesta
                FROM comandos_personalizados
                """
            ).fetchall()

        if len(frase_norm) < 5:
            return None

        mejor = None
        mejor_ratio = 0.0

        for comando in comandos:
            ratio = difflib.SequenceMatcher(
                None,
                frase_norm,
                comando[2],
            ).ratio()

            if ratio > mejor_ratio:
                mejor_ratio = ratio
                mejor = comando

        if mejor and mejor_ratio >= 0.86:
            return (mejor[0], mejor[1], mejor[3])

        return None

    # -------------------- voces autorizadas --------------------

    def guardar_voz_autorizada(self, nombre, embedding, muestras=1):
        nombre = (nombre or "").strip()
        if not nombre or embedding is None:
            return False

        try:
            valores = [float(x) for x in embedding]
        except Exception:
            return False

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        contenido = json.dumps(valores, separators=(",", ":"))

        with self.conectar() as con:
            existente = con.execute(
                "SELECT id FROM voces_autorizadas WHERE lower(nombre)=lower(?)",
                (nombre,),
            ).fetchone()

            if existente:
                con.execute(
                    """
                    UPDATE voces_autorizadas
                    SET nombre=?, embedding_json=?, muestras=?, fecha=?, activo=1
                    WHERE id=?
                    """,
                    (nombre, contenido, int(muestras), fecha, existente[0]),
                )
            else:
                con.execute(
                    """
                    INSERT INTO voces_autorizadas
                    (nombre, embedding_json, muestras, fecha, activo)
                    VALUES (?, ?, ?, ?, 1)
                    """,
                    (nombre, contenido, int(muestras), fecha),
                )

        return True

    def listar_voces_autorizadas(self, solo_activas=True):
        consulta = (
            "SELECT id, nombre, embedding_json, muestras, fecha, activo "
            "FROM voces_autorizadas"
        )
        if solo_activas:
            consulta += " WHERE activo=1"
        consulta += " ORDER BY nombre COLLATE NOCASE"

        with self.conectar() as con:
            filas = con.execute(consulta).fetchall()

        salida = []
        for fila in filas:
            try:
                embedding = [float(x) for x in json.loads(fila[2])]
            except Exception:
                embedding = []
            salida.append((fila[0], fila[1], embedding, fila[3], fila[4], fila[5]))
        return salida

    def eliminar_voz_autorizada(self, voz_id):
        with self.conectar() as con:
            con.execute("DELETE FROM voces_autorizadas WHERE id=?", (int(voz_id),))

    def cantidad_voces_autorizadas(self):
        with self.conectar() as con:
            fila = con.execute(
                "SELECT COUNT(*) FROM voces_autorizadas WHERE activo=1"
            ).fetchone()
        return int(fila[0] if fila else 0)


# ==========================================================
# BETA APP
# ==========================================================

# ==========================================================
# BIBLIOTECA ACADÉMICA LOCAL (RAG)
# Lee PDFs, los divide en fragmentos, crea embeddings y busca
# semánticamente sin enviar los documentos completos a Internet.
# ==========================================================

class BibliotecaAcademica:
    def __init__(self):
        self.modelo_embeddings = None
        self.modelo_cargando = False
        self.modelo_error = ""
        self.np = None
        self.indice_matriz = None
        self.indice_meta = []
        self.indice_lock = threading.Lock()
        self._ocr_componentes = None

        BIBLIOTECA_DIR.mkdir(parents=True, exist_ok=True)
        BIBLIOTECA_DOCUMENTOS_DIR.mkdir(parents=True, exist_ok=True)
        BIBLIOTECA_TECNICA_DIR.mkdir(parents=True, exist_ok=True)
        INDICES_DIR.mkdir(parents=True, exist_ok=True)
        self.crear_tablas()
        self.migrar_rutas_portables()

    def conectar(self):
        return sqlite3.connect(BASE_DATOS, timeout=30)

    def crear_tablas(self):
        with self.conectar() as con:
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS biblioteca_documentos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    ruta TEXT NOT NULL,
                    sha256 TEXT NOT NULL UNIQUE,
                    ramo TEXT DEFAULT '',
                    modulo TEXT DEFAULT '',
                    paginas INTEGER DEFAULT 0,
                    fragmentos INTEGER DEFAULT 0,
                    fecha TEXT NOT NULL,
                    activo INTEGER DEFAULT 1
                )
                """
            )
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS biblioteca_fragmentos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    documento_id INTEGER NOT NULL,
                    pagina INTEGER NOT NULL,
                    orden INTEGER NOT NULL,
                    texto TEXT NOT NULL,
                    embedding BLOB NOT NULL,
                    dim INTEGER NOT NULL,
                    FOREIGN KEY(documento_id) REFERENCES biblioteca_documentos(id)
                )
                """
            )
            con.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_biblioteca_fragmentos_documento
                ON biblioteca_fragmentos(documento_id)
                """
            )

            # v2.7.0: distinguimos apuntes académicos de libros/manuales técnicos.
            columnas_docs = {
                fila[1] for fila in con.execute(
                    "PRAGMA table_info(biblioteca_documentos)"
                ).fetchall()
            }
            if "categoria" not in columnas_docs:
                con.execute(
                    "ALTER TABLE biblioteca_documentos "
                    "ADD COLUMN categoria TEXT DEFAULT 'academica'"
                )
            if "coleccion" not in columnas_docs:
                con.execute(
                    "ALTER TABLE biblioteca_documentos "
                    "ADD COLUMN coleccion TEXT DEFAULT ''"
                )
            con.execute(
                "UPDATE biblioteca_documentos "
                "SET categoria='academica' "
                "WHERE categoria IS NULL OR TRIM(categoria)=''"
            )
            con.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_biblioteca_documentos_categoria
                ON biblioteca_documentos(categoria, coleccion, activo)
                """
            )

    def resolver_ruta_documento(self, ruta_guardada, ramo=""):
        """Resuelve una ruta guardada de forma portable.

        Desde v2.6.1 los documentos de la biblioteca se guardan con rutas
        relativas a BASE_DIR. Si beta.db viene de una ubicación anterior
        (por ejemplo C:/.../Beta) intentamos localizar automáticamente la
        copia equivalente dentro de la carpeta actual de Beta.
        """
        valor = str(ruta_guardada or "").strip()
        if not valor:
            return Path()

        ruta_original = Path(valor)
        candidatos = []

        # Las rutas relativas siempre se interpretan respecto a la carpeta
        # donde se encuentra beta.py (por ejemplo A:\Beta).
        if not ruta_original.is_absolute():
            candidatos.append(BASE_DIR / ruta_original)

        # Si la base venía de otro disco, preferimos la copia que exista
        # dentro de la biblioteca de la instalación actual.
        if ruta_original.name:
            candidatos.append(
                BIBLIOTECA_DOCUMENTOS_DIR
                / self.nombre_seguro(ramo)
                / ruta_original.name
            )

            # Respaldo para bibliotecas antiguas cuyo nombre de carpeta de
            # ramo haya cambiado ligeramente. Se ejecuta solo si hace falta.
            try:
                for encontrada in BIBLIOTECA_DOCUMENTOS_DIR.rglob(ruta_original.name):
                    candidatos.append(encontrada)
                    break
            except Exception:
                pass

        # Dejamos la ruta absoluta histórica como último recurso.
        if ruta_original.is_absolute():
            candidatos.append(ruta_original)

        vistos = set()
        for candidata in candidatos:
            try:
                clave = str(candidata)
                if clave in vistos:
                    continue
                vistos.add(clave)
                if candidata.exists():
                    return candidata
            except Exception:
                continue

        # Aunque el archivo no exista, devolvemos una ruta coherente para
        # poder mostrar el problema sin romper las consultas académicas.
        if ruta_original.is_absolute():
            return ruta_original
        return BASE_DIR / ruta_original

    def ruta_portable_para_bd(self, ruta):
        """Convierte una ruta interna de Beta a relativa antes de guardarla."""
        ruta = Path(ruta)
        try:
            return ruta.resolve().relative_to(BASE_DIR.resolve()).as_posix()
        except Exception:
            return str(ruta)

    def migrar_rutas_portables(self):
        """Migra sin borrar datos las rutas absolutas antiguas de la biblioteca."""
        cambios = 0
        with self.conectar() as con:
            filas = con.execute(
                "SELECT id, ruta, ramo FROM biblioteca_documentos"
            ).fetchall()
            for doc_id, ruta_guardada, ramo in filas:
                ruta_actual = self.resolver_ruta_documento(ruta_guardada, ramo or "")
                try:
                    if not ruta_actual.exists():
                        continue
                except Exception:
                    continue

                nueva = self.ruta_portable_para_bd(ruta_actual)
                if nueva != str(ruta_guardada or ""):
                    con.execute(
                        "UPDATE biblioteca_documentos SET ruta = ? WHERE id = ?",
                        (nueva, int(doc_id)),
                    )
                    cambios += 1

        if cambios:
            print(
                f"BIBLIOTECA PORTABLE: {cambios} ruta(s) migrada(s) "
                f"a la instalación actual: {BASE_DIR}"
            )

    def tiene_contenido(self):
        with self.conectar() as con:
            fila = con.execute(
                """
                SELECT COUNT(*)
                FROM biblioteca_fragmentos f
                JOIN biblioteca_documentos d ON d.id = f.documento_id
                WHERE d.activo = 1
                """
            ).fetchone()
        return bool(fila and int(fila[0] or 0) > 0)

    def estadisticas(self):
        with self.conectar() as con:
            docs = con.execute(
                "SELECT COUNT(*) FROM biblioteca_documentos WHERE activo = 1"
            ).fetchone()[0]
            frags = con.execute(
                """
                SELECT COUNT(*)
                FROM biblioteca_fragmentos f
                JOIN biblioteca_documentos d ON d.id=f.documento_id
                WHERE d.activo=1
                """
            ).fetchone()[0]
        return int(docs or 0), int(frags or 0)

    def tiene_contenido_categoria(self, categoria):
        categoria = normalizar(categoria)
        with self.conectar() as con:
            fila = con.execute(
                """
                SELECT COUNT(*)
                FROM biblioteca_fragmentos f
                JOIN biblioteca_documentos d ON d.id=f.documento_id
                WHERE d.activo=1 AND LOWER(TRIM(COALESCE(d.categoria,'academica'))) = ?
                """,
                (categoria,),
            ).fetchone()
        return bool(fila and int(fila[0] or 0) > 0)

    def estadisticas_categoria(self, categoria):
        categoria = normalizar(categoria)
        with self.conectar() as con:
            fila = con.execute(
                """
                SELECT COUNT(DISTINCT d.id), COUNT(f.id)
                FROM biblioteca_documentos d
                LEFT JOIN biblioteca_fragmentos f ON f.documento_id=d.id
                WHERE d.activo=1
                  AND LOWER(TRIM(COALESCE(d.categoria,'academica'))) = ?
                """,
                (categoria,),
            ).fetchone()
        return (int(fila[0] or 0), int(fila[1] or 0)) if fila else (0, 0)

    def listar_documentos_categoria(self, categoria):
        categoria = normalizar(categoria)
        with self.conectar() as con:
            filas = con.execute(
                """
                SELECT id, nombre, ruta, ramo, modulo, paginas, fragmentos, fecha,
                       COALESCE(categoria,'academica'), COALESCE(coleccion,'')
                FROM biblioteca_documentos
                WHERE activo=1
                  AND LOWER(TRIM(COALESCE(categoria,'academica'))) = ?
                ORDER BY coleccion COLLATE NOCASE, nombre COLLATE NOCASE
                """,
                (categoria,),
            ).fetchall()

        resultado = []
        for fila in filas:
            doc_id, nombre, ruta, ramo, modulo, paginas, fragmentos, fecha, cat, coleccion = fila
            ruta_resuelta = self.resolver_ruta_documento(ruta, ramo or coleccion or "")
            resultado.append(
                (doc_id, nombre, str(ruta_resuelta), ramo, modulo, paginas,
                 fragmentos, fecha, cat, coleccion)
            )
        return resultado

    def listar_colecciones_tecnicas(self):
        with self.conectar() as con:
            return con.execute(
                """
                SELECT COALESCE(NULLIF(TRIM(coleccion),''),'General') AS coleccion,
                       COUNT(*), COALESCE(SUM(fragmentos),0), COALESCE(SUM(paginas),0)
                FROM biblioteca_documentos
                WHERE activo=1
                  AND LOWER(TRIM(COALESCE(categoria,'academica')))='tecnica'
                GROUP BY LOWER(COALESCE(NULLIF(TRIM(coleccion),''),'General'))
                ORDER BY coleccion COLLATE NOCASE
                """
            ).fetchall()

    def buscar_versiones_mismo_nombre(
        self, ruta_pdf, categoria="", coleccion="", ramo=""
    ):
        """Busca documentos activos con el mismo nombre lógico.

        Sirve para detectar una nueva edición/versión del mismo PDF antes de
        importarla. No elimina nada automáticamente.
        """
        ruta_pdf = Path(ruta_pdf)
        objetivo = normalizar(ruta_pdf.stem)
        if not objetivo:
            return []
        categoria_n = normalizar(categoria or "")
        coleccion_n = normalizar(coleccion or "")
        ramo_n = normalizar(ramo or "")
        with self.conectar() as con:
            filas = con.execute(
                """
                SELECT id, nombre, sha256, categoria, coleccion, ramo, fecha
                FROM biblioteca_documentos
                WHERE activo=1
                ORDER BY id DESC
                """
            ).fetchall()
        salida = []
        for fila in filas:
            doc_id, nombre, sha, cat, col, ram, fecha = fila
            if normalizar(Path(nombre or "").stem) != objetivo:
                continue
            if categoria_n and normalizar(cat or "academica") != categoria_n:
                continue
            if categoria_n == "tecnica" and coleccion_n:
                if normalizar(col or "") != coleccion_n:
                    continue
            if categoria_n == "academica" and ramo_n:
                if normalizar(ram or "") != ramo_n:
                    continue
            salida.append({
                "id": int(doc_id), "nombre": nombre or "", "sha256": sha or "",
                "categoria": cat or "academica", "coleccion": col or "",
                "ramo": ram or "", "fecha": fecha or "",
            })
        return salida

    def _firma_indice_actual(self):
        with self.conectar() as con:
            fila = con.execute(
                """
                SELECT COUNT(f.id),
                       COALESCE(MAX(f.id),0),
                       COALESCE(SUM(f.id),0),
                       COUNT(DISTINCT d.id),
                       COALESCE(MAX(d.id),0)
                FROM biblioteca_fragmentos f
                JOIN biblioteca_documentos d ON d.id=f.documento_id
                WHERE d.activo=1
                """
            ).fetchone()
        if not fila:
            return {"fragmentos": 0, "max_fragmento": 0, "suma_fragmentos": 0,
                    "documentos": 0, "max_documento": 0}
        return {
            "fragmentos": int(fila[0] or 0),
            "max_fragmento": int(fila[1] or 0),
            "suma_fragmentos": int(fila[2] or 0),
            "documentos": int(fila[3] or 0),
            "max_documento": int(fila[4] or 0),
        }

    def _guardar_indice_persistente(self, matriz, meta, firma):
        try:
            INDICES_DIR.mkdir(parents=True, exist_ok=True)
            self.np.save(str(INDICE_MATRIZ_ARCHIVO), matriz)
            INDICE_META_ARCHIVO.write_text(
                json.dumps(meta, ensure_ascii=False, separators=(",", ":")),
                encoding="utf-8",
            )
            INDICE_FIRMA_ARCHIVO.write_text(
                json.dumps(firma, ensure_ascii=False, separators=(",", ":")),
                encoding="utf-8",
            )
        except Exception as error:
            print("ÍNDICE PERSISTENTE: no pude guardar caché:", error)

    def _cargar_indice_persistente(self, firma):
        try:
            if not (
                INDICE_MATRIZ_ARCHIVO.exists()
                and INDICE_META_ARCHIVO.exists()
                and INDICE_FIRMA_ARCHIVO.exists()
            ):
                return False
            firma_guardada = json.loads(
                INDICE_FIRMA_ARCHIVO.read_text(encoding="utf-8")
            )
            if firma_guardada != firma:
                return False
            meta = json.loads(INDICE_META_ARCHIVO.read_text(encoding="utf-8"))
            matriz = self.np.load(str(INDICE_MATRIZ_ARCHIVO), allow_pickle=False)
            if len(meta) != int(matriz.shape[0]):
                return False
            with self.indice_lock:
                self.indice_matriz = matriz.astype("float32", copy=False)
                self.indice_meta = meta
            print(
                f"ÍNDICE PERSISTENTE: {len(meta)} fragmentos cargados desde SSD."
            )
            return True
        except Exception as error:
            print("ÍNDICE PERSISTENTE: caché no utilizable, reconstruyendo:", error)
            return False

    def listar_ramos(self):
        with self.conectar() as con:
            return con.execute(
                """SELECT ramo, COUNT(*), COALESCE(SUM(fragmentos),0), COALESCE(SUM(paginas),0)
                   FROM biblioteca_documentos
                   WHERE activo=1 AND TRIM(ramo)!=''
                   GROUP BY LOWER(TRIM(ramo))
                   ORDER BY ramo COLLATE NOCASE"""
            ).fetchall()

    def listar_documentos(self):
        with self.conectar() as con:
            filas = con.execute(
                """
                SELECT id, nombre, ruta, ramo, modulo, paginas, fragmentos, fecha
                FROM biblioteca_documentos
                WHERE activo = 1
                ORDER BY ramo COLLATE NOCASE, modulo COLLATE NOCASE, nombre COLLATE NOCASE
                """
            ).fetchall()

        resultado = []
        for fila in filas:
            doc_id, nombre, ruta, ramo, modulo, paginas, fragmentos, fecha = fila
            ruta_resuelta = self.resolver_ruta_documento(ruta, ramo or "")
            resultado.append(
                (doc_id, nombre, str(ruta_resuelta), ramo, modulo, paginas, fragmentos, fecha)
            )
        return resultado

    def palabras_metadatos(self):
        palabras = set()
        with self.conectar() as con:
            filas = con.execute(
                """
                SELECT nombre, ramo, modulo, COALESCE(coleccion,'')
                FROM biblioteca_documentos
                WHERE activo=1
                """
            ).fetchall()
        for fila in filas:
            for valor in fila:
                for p in normalizar(valor or "").split():
                    if len(p) >= 4:
                        palabras.add(p)
        return palabras

    def hash_archivo(self, ruta):
        h = hashlib.sha256()
        with open(ruta, "rb") as f:
            while True:
                bloque = f.read(1024 * 1024)
                if not bloque:
                    break
                h.update(bloque)
        return h.hexdigest()

    def nombre_seguro(self, texto):
        texto = normalizar(texto or "general")
        texto = re.sub(r"[^a-z0-9_-]+", "_", texto)
        return texto.strip("_")[:60] or "general"

    def fragmentar_texto(self, texto):
        texto = (texto or "").replace("\x00", " ")
        texto = re.sub(r"[ \t]+", " ", texto)
        texto = re.sub(r"\n{3,}", "\n\n", texto)
        texto = texto.strip()
        if not texto:
            return []

        # Separamos en unidades naturales para no cortar ideas a mitad de frase.
        unidades = re.split(r"(?<=[.!?;:])\s+|\n+", texto)
        unidades = [u.strip() for u in unidades if u.strip()]
        fragmentos = []
        actual = ""

        for unidad in unidades:
            if len(unidad) > BIBLIOTECA_CHUNK_MAX:
                # Si una unidad es excepcionalmente larga, la dividimos con solape.
                inicio = 0
                while inicio < len(unidad):
                    fin = min(len(unidad), inicio + BIBLIOTECA_CHUNK_MAX)
                    parte = unidad[inicio:fin].strip()
                    if parte:
                        if actual:
                            fragmentos.append(actual.strip())
                            actual = ""
                        fragmentos.append(parte)
                    if fin >= len(unidad):
                        break
                    inicio = max(fin - BIBLIOTECA_CHUNK_OVERLAP, inicio + 1)
                continue

            candidato = (actual + " " + unidad).strip() if actual else unidad
            if len(candidato) <= BIBLIOTECA_CHUNK_MAX:
                actual = candidato
            else:
                if actual:
                    fragmentos.append(actual.strip())
                # Conservamos una pequeña cola del fragmento anterior para contexto.
                cola = ""
                if fragmentos:
                    cola = fragmentos[-1][-BIBLIOTECA_CHUNK_OVERLAP:].strip()
                actual = (cola + " " + unidad).strip() if cola else unidad

        if actual:
            fragmentos.append(actual.strip())

        # Eliminamos fragmentos demasiado pequeños salvo que sean el único contenido.
        utiles = [f for f in fragmentos if len(f) >= 90]
        return utiles if utiles else fragmentos

    def buscar_tesseract(self):
        """Localiza tesseract.exe en Windows sin exigir que esté en PATH."""
        encontrados = []

        desde_path = shutil.which("tesseract")
        if desde_path:
            encontrados.append(Path(desde_path))

        candidatos = [
            Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe"),
            Path(r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"),
            Path.home() / "AppData" / "Local" / "Programs" / "Tesseract-OCR" / "tesseract.exe",
        ]
        encontrados.extend(candidatos)

        for ruta in encontrados:
            try:
                if ruta and Path(ruta).exists():
                    return str(Path(ruta))
            except Exception:
                continue
        return ""

    def preparar_ocr(self, progreso=None):
        """Prepara pytesseract y devuelve (pytesseract, PIL helpers, idioma)."""
        if self._ocr_componentes is not None:
            return self._ocr_componentes

        try:
            import pytesseract
            from PIL import Image, ImageOps, ImageFilter
        except Exception as error:
            raise RuntimeError(
                "Falta el componente OCR de Python. Ejecute: "
                "python -m pip install -U pytesseract pillow"
            ) from error

        ejecutable = self.buscar_tesseract()
        if not ejecutable:
            raise RuntimeError(
                "El PDF parece estar escaneado, pero Tesseract OCR no está instalado. "
                "Instale Tesseract OCR para Windows y vuelva a agregar el PDF. "
                "Beta lo buscará automáticamente en C:\\Program Files\\Tesseract-OCR."
            )

        pytesseract.pytesseract.tesseract_cmd = ejecutable

        try:
            idiomas = set(pytesseract.get_languages(config=""))
        except Exception:
            idiomas = set()

        if OCR_IDIOMA_PREFERIDO in idiomas:
            idioma = OCR_IDIOMA_PREFERIDO
        elif "eng" in idiomas:
            idioma = "eng"
            if progreso:
                progreso(
                    "OCR: no encontré el paquete español 'spa'; usaré inglés como respaldo. "
                    "Conviene instalar spa.traineddata para mejorar los apuntes en español."
                )
        else:
            idioma = None

        if progreso:
            texto_idioma = idioma or "predeterminado"
            progreso(
                f"OCR listo: Tesseract encontrado en {ejecutable}. Idioma: {texto_idioma}."
            )

        self._ocr_componentes = (pytesseract, Image, ImageOps, ImageFilter, idioma)
        return self._ocr_componentes

    def limpiar_texto_ocr(self, texto):
        """Limpia ruido típico del OCR sin inventar contenido académico.

        La función corrige formato, palabras partidas al final de línea y
        descarta líneas que son casi puro ruido. No intenta adivinar palabras
        completas: la fuente original sigue siendo el PDF.
        """
        texto = unicodedata.normalize("NFKC", texto or "")
        texto = texto.replace("\x0c", " ").replace("\r", "\n")

        # Unir palabras que el escaneo cortó por salto de línea: progra-\nmación.
        texto = re.sub(
            r"([A-Za-zÁÉÍÓÚÜÑáéíóúüñ])-\s*\n\s*([a-záéíóúüñ])",
            r"\1\2",
            texto,
        )

        reemplazos = {
            "ﬁ": "fi", "ﬂ": "fl", "“": '"', "”": '"',
            "‘": "'", "’": "'", "…": "...", "•": " ",
        }
        for viejo, nuevo in reemplazos.items():
            texto = texto.replace(viejo, nuevo)

        lineas = []
        for linea in texto.splitlines():
            linea = re.sub(r"[ \t]+", " ", linea).strip()
            if not linea:
                if lineas and lineas[-1] != "":
                    lineas.append("")
                continue

            # Separadores, bordes y basura gráfica detectada como caracteres.
            if re.fullmatch(r"[^A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9]{4,}", linea):
                continue

            visibles = [c for c in linea if not c.isspace()]
            if len(visibles) >= 10:
                alfanumericos = sum(c.isalnum() for c in visibles)
                if alfanumericos / max(1, len(visibles)) < 0.32:
                    continue

            linea = re.sub(r"([!?.,;:])\1{2,}", r"\1", linea)
            linea = re.sub(r" {2,}", " ", linea)
            lineas.append(linea)

        texto = "\n".join(lineas)
        texto = re.sub(r"\n{3,}", "\n\n", texto)
        return texto.strip()

    def ocr_pagina(self, pagina, numero_pagina, progreso=None):
        """Convierte una página PDF a imagen y extrae texto localmente con Tesseract."""
        pytesseract, Image, ImageOps, ImageFilter, idioma = self.preparar_ocr(progreso=None)

        if progreso:
            progreso(f"OCR: leyendo página {numero_pagina}...")

        import pymupdf
        escala = max(1.0, float(OCR_DPI) / 72.0)
        pix = pagina.get_pixmap(
            matrix=pymupdf.Matrix(escala, escala),
            alpha=False,
            colorspace=pymupdf.csRGB,
        )

        imagen = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        imagen = ImageOps.grayscale(imagen)
        imagen = ImageOps.autocontrast(imagen)
        # Un enfoque muy suave ayuda con capturas o escaneos sin destruir letras finas.
        try:
            imagen = imagen.filter(ImageFilter.SHARPEN)
        except Exception:
            pass

        kwargs = {"config": OCR_CONFIG_PRINCIPAL}
        if idioma:
            kwargs["lang"] = idioma

        texto = pytesseract.image_to_string(imagen, **kwargs) or ""
        texto = texto.replace("\x0c", " ").strip()

        # Si la segmentación automática obtuvo muy poco, repetimos con bloque uniforme.
        if len(normalizar(texto)) < OCR_MIN_CARACTERES_VALIDOS:
            kwargs["config"] = OCR_CONFIG_REINTENTO
            texto2 = pytesseract.image_to_string(imagen, **kwargs) or ""
            texto2 = texto2.replace("\x0c", " ").strip()
            if len(normalizar(texto2)) > len(normalizar(texto)):
                texto = texto2

        return self.limpiar_texto_ocr(texto)

    def comprobar_ocr(self):
        """Devuelve un resumen simple para mostrar en la interfaz."""
        ejecutable = self.buscar_tesseract()
        if not ejecutable:
            return False, "Tesseract OCR no está instalado o Beta no pudo localizarlo."
        try:
            import pytesseract
            pytesseract.pytesseract.tesseract_cmd = ejecutable
            idiomas = pytesseract.get_languages(config="")
            idioma = "spa" if "spa" in idiomas else ("eng" if "eng" in idiomas else "predeterminado")
            return True, f"OCR disponible. Tesseract: {ejecutable} | Idioma: {idioma}"
        except Exception as error:
            return False, f"Tesseract fue localizado, pero pytesseract no pudo usarlo: {error}"

    def cargar_modelo(self, progreso=None):
        if self.modelo_embeddings is not None:
            return self.modelo_embeddings
        if self.modelo_cargando:
            # Otro hilo ya lo está preparando.
            limite = time.time() + 180
            while self.modelo_cargando and time.time() < limite:
                time.sleep(0.2)
            if self.modelo_embeddings is not None:
                return self.modelo_embeddings
            if self.modelo_error:
                raise RuntimeError(self.modelo_error)

        self.modelo_cargando = True
        self.modelo_error = ""
        try:
            try:
                import numpy as np
                from sentence_transformers import SentenceTransformer
            except Exception as error:
                raise RuntimeError(
                    "Faltan componentes de la biblioteca académica. "
                    "Ejecute: python -m pip install -U pymupdf sentence-transformers numpy"
                ) from error

            self.np = np

            marcador_local = CARPETA_EMBEDDINGS / "modules.json"
            if marcador_local.exists():
                if progreso:
                    progreso("Cargando modelo semántico local...")
                modelo = SentenceTransformer(str(CARPETA_EMBEDDINGS), device="cpu")
            else:
                if progreso:
                    progreso(
                        "Primera vez: descargando el modelo semántico multilingüe. "
                        "Después funcionará localmente."
                    )
                CARPETA_EMBEDDINGS.mkdir(parents=True, exist_ok=True)
                modelo = SentenceTransformer(EMBEDDING_MODEL, device="cpu")
                modelo.save(str(CARPETA_EMBEDDINGS))

            self.modelo_embeddings = modelo
            return modelo
        except Exception as error:
            self.modelo_error = str(error)
            raise
        finally:
            self.modelo_cargando = False

    def cargar_indice_memoria(self, forzar=False):
        """Carga el índice vectorial sin cargar SentenceTransformer.

        v2.7.0 guarda matriz + metadatos ligeros en el SSD. De este modo el
        arranque no necesita levantar el modelo semántico completo. El modelo
        se carga de forma perezosa cuando llega la primera consulta o durante
        el precalentamiento en segundo plano.
        """
        try:
            import numpy as np
        except Exception as error:
            raise RuntimeError(
                "Falta NumPy para cargar el índice semántico."
            ) from error

        self.np = np
        firma = self._firma_indice_actual()

        if not forzar and firma.get("fragmentos", 0) > 0:
            if self._cargar_indice_persistente(firma):
                return len(self.indice_meta)

        with self.conectar() as con:
            filas = con.execute(
                """
                SELECT
                    f.id, f.embedding, f.dim, f.pagina,
                    d.id, d.nombre, d.ruta, d.ramo, d.modulo,
                    COALESCE(d.categoria,'academica'),
                    COALESCE(d.coleccion,'')
                FROM biblioteca_fragmentos f
                JOIN biblioteca_documentos d ON d.id = f.documento_id
                WHERE d.activo = 1
                ORDER BY f.id
                """
            ).fetchall()

        vectores = []
        meta = []
        for fila in filas:
            vec = np.frombuffer(fila[1], dtype=np.float32)
            if vec.size != int(fila[2]):
                continue
            vectores.append(vec)
            meta.append(
                {
                    "fragmento_id": int(fila[0]),
                    "pagina": int(fila[3]),
                    "documento_id": int(fila[4]),
                    "documento": fila[5],
                    "ruta": fila[6],
                    "ramo": fila[7] or "",
                    "modulo": fila[8] or "",
                    "categoria": (fila[9] or "academica").strip().lower(),
                    "coleccion": fila[10] or "",
                }
            )

        with self.indice_lock:
            if vectores:
                matriz = np.vstack(vectores).astype("float32")
                self.indice_matriz = matriz
                self.indice_meta = meta
            else:
                matriz = np.empty((0, 0), dtype="float32")
                self.indice_matriz = None
                self.indice_meta = []

        if vectores:
            self._guardar_indice_persistente(matriz, meta, firma)
            print(
                f"ÍNDICE PERSISTENTE: reconstruido y guardado ({len(meta)} fragmentos)."
            )
        return len(meta)


    def importar_pdf(
        self, ruta_pdf, ramo="", modulo="", progreso=None,
        categoria="academica", coleccion="", reemplazar_documentos_ids=None
    ):
        ruta_pdf = Path(ruta_pdf)
        categoria = normalizar(categoria or "academica") or "academica"
        coleccion = (coleccion or "").strip()
        if categoria not in {"academica", "tecnica"}:
            categoria = "academica"
        reemplazar_documentos_ids = [
            int(x) for x in (reemplazar_documentos_ids or []) if str(x).isdigit()
        ]
        if not ruta_pdf.exists():
            return {"estado": "error", "mensaje": "El archivo ya no existe."}

        sha = self.hash_archivo(ruta_pdf)

        with self.conectar() as con:
            existente = con.execute(
                """
                SELECT id, activo, nombre
                FROM biblioteca_documentos
                WHERE sha256 = ?
                """,
                (sha,),
            ).fetchone()
            if existente and int(existente[1]) == 1:
                return {
                    "estado": "duplicado",
                    "mensaje": f"{existente[2]} ya forma parte de la biblioteca.",
                }
            if existente and int(existente[1]) == 0:
                con.execute(
                    "UPDATE biblioteca_documentos SET activo = 1, categoria = ?, coleccion = ? WHERE id = ?",
                    (categoria, coleccion, existente[0]),
                )
                self.cargar_indice_memoria()
                return {
                    "estado": "reactivado",
                    "mensaje": f"{existente[2]} fue reactivado.",
                }

        try:
            import pymupdf
        except Exception as error:
            raise RuntimeError(
                "Falta PyMuPDF. Ejecute: python -m pip install -U pymupdf"
            ) from error

        if progreso:
            progreso(f"Leyendo {ruta_pdf.name}...")

        doc = pymupdf.open(str(ruta_pdf))
        paginas = int(doc.page_count)
        registros = []
        paginas_texto = 0
        paginas_ocr = 0
        paginas_vacias = 0
        ocr_preparado = False

        try:
            for num_pagina in range(paginas):
                pagina = doc.load_page(num_pagina)
                texto = pagina.get_text("text") or ""
                texto_limpio = normalizar(texto)
                metodo = "texto"

                # Si la página no tiene una capa de texto útil, usamos OCR local.
                if OCR_ACTIVO and len(texto_limpio) < OCR_MIN_CARACTERES_DIRECTOS:
                    metodo = "ocr"
                    try:
                        if not ocr_preparado:
                            self.preparar_ocr(progreso=progreso)
                            ocr_preparado = True
                            if progreso:
                                progreso(
                                    f"{ruta_pdf.name} parece ser un PDF escaneado. "
                                    "Activando OCR local página por página..."
                                )
                        texto = self.ocr_pagina(
                            pagina,
                            num_pagina + 1,
                            progreso=progreso,
                        )
                        texto_limpio = normalizar(texto)
                    except Exception as error:
                        return {
                            "estado": "ocr_requerido",
                            "mensaje": f"{ruta_pdf.name}: {error}",
                            "error": str(error),
                        }

                if len(texto_limpio) < OCR_MIN_CARACTERES_VALIDOS:
                    paginas_vacias += 1
                    continue

                if metodo == "ocr":
                    paginas_ocr += 1
                else:
                    paginas_texto += 1

                trozos = self.fragmentar_texto(texto)
                for orden, trozo in enumerate(trozos):
                    registros.append((num_pagina + 1, orden, trozo))
        finally:
            doc.close()

        if not registros:
            return {
                "estado": "sin_texto",
                "mensaje": (
                    f"{ruta_pdf.name} no produjo texto utilizable incluso después del OCR. "
                    "Revise si las páginas son legibles o si Tesseract tiene instalado el idioma español."
                ),
            }

        # El modelo semántico solo se carga después de haber obtenido texto real.
        modelo = self.cargar_modelo(progreso)

        if progreso:
            detalle_ocr = (
                f" ({paginas_ocr} página(s) mediante OCR)" if paginas_ocr else ""
            )
            progreso(
                f"Creando {len(registros)} fragmentos semánticos de {ruta_pdf.name}{detalle_ocr}..."
            )

        textos = [r[2] for r in registros]
        embeddings = modelo.encode(
            textos,
            batch_size=24,
            show_progress_bar=False,
            normalize_embeddings=True,
            convert_to_numpy=True,
        ).astype("float32")

        if categoria == "tecnica":
            carpeta_ramo = (
                BIBLIOTECA_TECNICA_DIR
                / self.nombre_seguro(coleccion or "general")
            )
        else:
            carpeta_ramo = BIBLIOTECA_DOCUMENTOS_DIR / self.nombre_seguro(ramo)
        carpeta_ramo.mkdir(parents=True, exist_ok=True)
        nombre_copia = f"{sha[:12]}_{ruta_pdf.name}"
        ruta_copia = carpeta_ramo / nombre_copia
        if not ruta_copia.exists():
            shutil.copy2(ruta_pdf, ruta_copia)

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.conectar() as con:
            cur = con.execute(
                """
                INSERT INTO biblioteca_documentos
                (nombre, ruta, sha256, ramo, modulo, paginas, fragmentos, fecha, activo,
                 categoria, coleccion)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
                """,
                (
                    ruta_pdf.name,
                    self.ruta_portable_para_bd(ruta_copia),
                    sha,
                    (ramo or "").strip(),
                    (modulo or "").strip(),
                    paginas,
                    len(registros),
                    fecha,
                    categoria,
                    coleccion,
                ),
            )
            documento_id = cur.lastrowid

            datos = []
            for (pagina_num, orden, trozo), emb in zip(registros, embeddings):
                datos.append(
                    (
                        documento_id,
                        pagina_num,
                        orden,
                        trozo,
                        emb.tobytes(),
                        int(emb.shape[0]),
                    )
                )
            con.executemany(
                """
                INSERT INTO biblioteca_fragmentos
                (documento_id, pagina, orden, texto, embedding, dim)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                datos,
            )
            if reemplazar_documentos_ids:
                ids_validos = [i for i in reemplazar_documentos_ids if i != int(documento_id)]
                if ids_validos:
                    marcadores = ",".join("?" for _ in ids_validos)
                    con.execute(
                        f"UPDATE biblioteca_documentos SET activo=0 WHERE id IN ({marcadores})",
                        tuple(ids_validos),
                    )

        self.cargar_indice_memoria(forzar=True)
        return {
            "estado": "ok",
            "reemplazados": len(reemplazar_documentos_ids),
            "categoria": categoria,
            "coleccion": coleccion,
            "mensaje": (
                f"{ruta_pdf.name}: {paginas} páginas y {len(registros)} fragmentos incorporados. "
                f"Texto directo: {paginas_texto} página(s); OCR: {paginas_ocr}; "
                f"sin contenido útil: {paginas_vacias}."
            ),
            "paginas": paginas,
            "fragmentos": len(registros),
            "paginas_ocr": paginas_ocr,
            "paginas_texto": paginas_texto,
        }

    def eliminar_documento(self, documento_id):
        with self.conectar() as con:
            con.execute(
                "UPDATE biblioteca_documentos SET activo = 0 WHERE id = ?",
                (int(documento_id),),
            )
        try:
            self.cargar_indice_memoria(forzar=True)
        except Exception:
            pass

    def buscar(
        self, consulta, limite=BIBLIOTECA_RESULTADOS, ramo_preferido="",
        categoria_preferida="", coleccion_preferida="", colecciones_preferidas=None
    ):
        """Búsqueda semántica con filtros opcionales.

        categoria_preferida separa de forma estricta los apuntes académicos
        ('academica') de los libros/manuales técnicos ('tecnica').
        """
        consulta = (consulta or "").strip()
        if not consulta:
            return []

        modelo = self.cargar_modelo()

        if self.indice_matriz is None or not self.indice_meta:
            self.cargar_indice_memoria()

        with self.indice_lock:
            matriz = self.indice_matriz
            meta = list(self.indice_meta)

        if matriz is None or not meta:
            return []

        q = modelo.encode(
            [consulta],
            show_progress_bar=False,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )[0].astype("float32")

        scores = matriz @ q
        candidatos = list(range(len(meta)))

        categoria_n = normalizar(categoria_preferida)
        if categoria_n:
            filtrados = [
                i for i, item in enumerate(meta)
                if normalizar(item.get("categoria", "academica")) == categoria_n
            ]
            candidatos = filtrados

        coleccion_n = normalizar(coleccion_preferida)
        colecciones_n = [
            normalizar(c) for c in (colecciones_preferidas or []) if normalizar(c)
        ]
        if colecciones_n and candidatos:
            filtrados = []
            for i in candidatos:
                c = normalizar(meta[i].get("coleccion", ""))
                if c and any(
                    c == pref or c in pref or pref in c for pref in colecciones_n
                ):
                    filtrados.append(i)
            if filtrados:
                candidatos = filtrados
        elif coleccion_n and candidatos:
            filtrados = []
            for i in candidatos:
                c = normalizar(meta[i].get("coleccion", ""))
                if c and (c == coleccion_n or c in coleccion_n or coleccion_n in c):
                    filtrados.append(i)
            if filtrados:
                candidatos = filtrados

        ramo_n = normalizar(ramo_preferido)
        if ramo_n and candidatos:
            filtrados = []
            for i in candidatos:
                r = normalizar(meta[i].get("ramo", ""))
                if r and (r == ramo_n or r in ramo_n or ramo_n in r):
                    filtrados.append(i)
            if filtrados:
                candidatos = filtrados

        if not candidatos:
            return []

        cantidad = min(max(1, int(limite)), len(candidatos))
        indices = sorted(
            candidatos, key=lambda i: float(scores[i]), reverse=True
        )[:cantidad]

        fragmento_ids = [int(meta[int(idx)]["fragmento_id"]) for idx in indices]
        textos = {}
        if fragmento_ids:
            marcadores = ",".join("?" for _ in fragmento_ids)
            with self.conectar() as con:
                filas = con.execute(
                    f"SELECT id, texto FROM biblioteca_fragmentos "
                    f"WHERE id IN ({marcadores})",
                    tuple(fragmento_ids),
                ).fetchall()
            textos = {int(fid): texto for fid, texto in filas}

        resultados = []
        for idx in indices:
            item = dict(meta[int(idx)])
            fid = int(item["fragmento_id"])
            item["texto"] = textos.get(fid, "")
            item["ruta"] = str(
                self.resolver_ruta_documento(
                    item.get("ruta", ""),
                    item.get("ramo") or item.get("coleccion") or "",
                )
            )
            item["score"] = float(scores[int(idx)])
            resultados.append(item)
        return resultados



# ==========================================================
# RESPALDOS AUTOMÁTICOS v2.7.1
# ==========================================================

class GestorRespaldosBeta:
    """Crea copias consistentes y rotativas del estado de Beta.

    beta.db se copia con la API de respaldo de SQLite, por lo que la copia es
    coherente incluso si Beta está abierta. Los índices se incluyen como
    aceleradores opcionales; la base de datos sigue siendo la fuente canónica.
    """

    def __init__(self, memoria=None):
        self.memoria = memoria
        self.lock = threading.Lock()
        RESPALDOS_DIR.mkdir(parents=True, exist_ok=True)

    def _sha256_archivo(self, ruta):
        h = hashlib.sha256()
        with open(ruta, "rb") as f:
            while True:
                bloque = f.read(1024 * 1024)
                if not bloque:
                    break
                h.update(bloque)
        return h.hexdigest()

    def listar_respaldos(self):
        RESPALDOS_DIR.mkdir(parents=True, exist_ok=True)
        archivos = list(RESPALDOS_DIR.glob("Beta_respaldo_*.zip"))
        return sorted(archivos, key=lambda p: p.stat().st_mtime, reverse=True)

    def ultimo_respaldo(self):
        archivos = self.listar_respaldos()
        return archivos[0] if archivos else None

    def debe_crear_automatico(self):
        ultimo = self.ultimo_respaldo()
        if ultimo is None:
            return True
        try:
            edad = time.time() - ultimo.stat().st_mtime
            return edad >= RESPALDO_INTERVALO_SEGUNDOS
        except Exception:
            return True

    def espacio_libre_mb(self):
        try:
            return shutil.disk_usage(BASE_DIR).free / (1024 * 1024)
        except Exception:
            return 0.0

    def _crear_snapshot_sqlite(self, destino):
        if not BASE_DATOS.exists():
            raise RuntimeError("beta.db todavía no existe.")

        origen = sqlite3.connect(str(BASE_DATOS), timeout=30)
        destino_con = sqlite3.connect(str(destino), timeout=30)
        try:
            origen.backup(destino_con, pages=256, sleep=0.01)
            destino_con.commit()
        finally:
            try:
                destino_con.close()
            finally:
                origen.close()

        # Verificación real de la copia antes de empaquetarla.
        con = sqlite3.connect(str(destino), timeout=30)
        try:
            fila = con.execute("PRAGMA quick_check").fetchone()
            resultado = str(fila[0] if fila else "").strip().lower()
            if resultado != "ok":
                raise RuntimeError(f"SQLite quick_check devolvió: {resultado or 'sin respuesta'}")
        finally:
            con.close()

    def _resumen_base_datos(self, snapshot):
        resumen = {
            "quick_check": "ok",
            "documentos_biblioteca": [],
            "conteos": {},
        }
        con = sqlite3.connect(str(snapshot), timeout=30)
        try:
            tablas = [
                "recuerdos", "conversaciones", "resumenes_conversacion",
                "voces_autorizadas", "biblioteca_documentos",
                "biblioteca_fragmentos", "aprendizaje_academico",
                "aprendizaje_eventos",
            ]
            for tabla in tablas:
                try:
                    fila = con.execute(f"SELECT COUNT(*) FROM {tabla}").fetchone()
                    resumen["conteos"][tabla] = int(fila[0] if fila else 0)
                except Exception:
                    pass

            try:
                filas = con.execute(
                    """
                    SELECT nombre, sha256, ramo, modulo, paginas, fragmentos,
                           COALESCE(categoria,'academica'), COALESCE(coleccion,'')
                    FROM biblioteca_documentos
                    WHERE activo=1
                    ORDER BY id
                    """
                ).fetchall()
                resumen["documentos_biblioteca"] = [
                    {
                        "nombre": f[0],
                        "sha256": f[1],
                        "ramo": f[2] or "",
                        "modulo": f[3] or "",
                        "paginas": int(f[4] or 0),
                        "fragmentos": int(f[5] or 0),
                        "categoria": f[6] or "academica",
                        "coleccion": f[7] or "",
                    }
                    for f in filas
                ]
            except Exception:
                pass
        finally:
            con.close()
        return resumen

    def _podar_antiguos(self):
        archivos = self.listar_respaldos()
        eliminados = []
        for ruta in archivos[RESPALDO_RETENCION:]:
            try:
                ruta.unlink()
                eliminados.append(ruta.name)
            except Exception as error:
                print("RESPALDO: no pude eliminar copia antigua:", ruta.name, error)
        return eliminados

    def crear_respaldo(self, motivo="manual"):
        if self.espacio_libre_mb() < RESPALDO_ESPACIO_MINIMO_MB:
            raise RuntimeError(
                f"Quedan menos de {RESPALDO_ESPACIO_MINIMO_MB} MB libres en la unidad de Beta."
            )

        # Evita dos respaldos simultáneos desde el programador y el menú.
        if not self.lock.acquire(blocking=False):
            raise RuntimeError("Ya hay un respaldo de Beta en curso.")

        temporal_dir = None
        zip_parcial = None
        try:
            RESPALDOS_DIR.mkdir(parents=True, exist_ok=True)
            ahora = datetime.now()
            sello = ahora.strftime("%Y-%m-%d_%H-%M-%S")
            motivo_seguro = re.sub(r"[^a-z0-9_-]+", "_", normalizar(motivo)) or "manual"
            nombre = f"Beta_respaldo_{sello}_{motivo_seguro}.zip"
            destino_final = RESPALDOS_DIR / nombre
            zip_parcial = RESPALDOS_DIR / (nombre + ".partial")

            temporal_dir = Path(tempfile.mkdtemp(prefix="beta_backup_", dir=str(RESPALDOS_DIR)))
            snapshot = temporal_dir / "beta.db"
            self._crear_snapshot_sqlite(snapshot)

            script_actual = Path(__file__).resolve()
            copia_script = temporal_dir / "beta.py"
            shutil.copy2(script_actual, copia_script)

            incluidos = ["beta.db", "beta.py", "backup_info.json", "biblioteca_manifest.json"]
            indices_incluidos = []
            if RESPALDO_INCLUIR_INDICES:
                carpeta_indices_tmp = temporal_dir / "indices"
                for ruta in (INDICE_MATRIZ_ARCHIVO, INDICE_META_ARCHIVO, INDICE_FIRMA_ARCHIVO):
                    try:
                        if ruta.exists() and ruta.is_file():
                            carpeta_indices_tmp.mkdir(parents=True, exist_ok=True)
                            copia = carpeta_indices_tmp / ruta.name
                            shutil.copy2(ruta, copia)
                            indices_incluidos.append(f"indices/{ruta.name}")
                    except Exception as error:
                        print("RESPALDO: índice opcional omitido:", ruta.name, error)
            incluidos.extend(indices_incluidos)

            resumen_db = self._resumen_base_datos(snapshot)
            (temporal_dir / "biblioteca_manifest.json").write_text(
                json.dumps(
                    resumen_db.get("documentos_biblioteca", []),
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            info = {
                "beta_version": "2.7.1",
                "fecha": ahora.strftime("%Y-%m-%d %H:%M:%S"),
                "motivo": motivo,
                "base_dir": str(BASE_DIR),
                "database": {
                    "archivo": "beta.db",
                    "quick_check": "ok",
                    "tamano_bytes": snapshot.stat().st_size,
                    "sha256": self._sha256_archivo(snapshot),
                    "conteos": resumen_db.get("conteos", {}),
                },
                "codigo": {
                    "archivo": "beta.py",
                    "sha256": self._sha256_archivo(copia_script),
                },
                "indices_incluidos": indices_incluidos,
                "archivos_incluidos": incluidos,
                "nota": (
                    "Los PDF originales y los modelos de IA no se duplican en cada ZIP. "
                    "beta.db conserva textos, embeddings, memoria, progreso, preferencias y metadatos."
                ),
            }
            (temporal_dir / "backup_info.json").write_text(
                json.dumps(info, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

            with zipfile.ZipFile(
                zip_parcial,
                "w",
                compression=zipfile.ZIP_DEFLATED,
                compresslevel=6,
            ) as zf:
                for ruta in temporal_dir.rglob("*"):
                    if ruta.is_file():
                        zf.write(ruta, ruta.relative_to(temporal_dir).as_posix())

            # Validar CRC del ZIP antes de hacerlo visible como copia válida.
            with zipfile.ZipFile(zip_parcial, "r") as zf:
                malo = zf.testzip()
                if malo:
                    raise RuntimeError(f"El ZIP de respaldo falló la verificación CRC en {malo}.")
                nombres = set(zf.namelist())
                if "beta.db" not in nombres or "beta.py" not in nombres:
                    raise RuntimeError("El respaldo no contiene beta.db y beta.py.")

            os.replace(zip_parcial, destino_final)
            eliminados = self._podar_antiguos()

            try:
                if self.memoria is not None:
                    self.memoria.cambiar_estado(
                        "ultimo_respaldo_ok", ahora.strftime("%Y-%m-%d %H:%M:%S")
                    )
            except Exception:
                pass

            resultado = {
                "ruta": destino_final,
                "tamano": destino_final.stat().st_size,
                "fecha": ahora,
                "motivo": motivo,
                "eliminados": eliminados,
                "conteos": resumen_db.get("conteos", {}),
            }
            print(
                f"RESPALDO OK: {destino_final.name} | "
                f"{resultado['tamano'] / (1024 * 1024):.1f} MB"
            )
            if eliminados:
                print(f"RESPALDO: {len(eliminados)} copia(s) antigua(s) eliminada(s).")
            return resultado
        finally:
            try:
                if zip_parcial and Path(zip_parcial).exists():
                    Path(zip_parcial).unlink()
            except Exception:
                pass
            if temporal_dir:
                shutil.rmtree(temporal_dir, ignore_errors=True)
            self.lock.release()

    def verificar_respaldo(self, ruta=None):
        ruta = Path(ruta) if ruta else self.ultimo_respaldo()
        if not ruta or not ruta.exists():
            return False, "No hay respaldos para verificar."
        try:
            with zipfile.ZipFile(ruta, "r") as zf:
                malo = zf.testzip()
                if malo:
                    return False, f"Error CRC en {malo}."
                nombres = set(zf.namelist())
                if "beta.db" not in nombres or "backup_info.json" not in nombres:
                    return False, "Faltan archivos esenciales en el respaldo."

                with tempfile.TemporaryDirectory(prefix="beta_verify_") as td:
                    zf.extract("beta.db", td)
                    db = Path(td) / "beta.db"
                    con = sqlite3.connect(str(db), timeout=30)
                    try:
                        fila = con.execute("PRAGMA quick_check").fetchone()
                    finally:
                        con.close()
                    if not fila or str(fila[0]).strip().lower() != "ok":
                        return False, "La copia de beta.db no supera SQLite quick_check."
            return True, f"{ruta.name} está íntegro."
        except Exception as error:
            return False, str(error)



class BetaApp:
    def __init__(self, root):
        self.root = root
        self.memoria = MemoriaBeta()

        # Respaldos v2.7.1. Se ejecutan en segundo plano y nunca bloquean
        # el arranque de voz, Spotify o la biblioteca.
        self.gestor_respaldos = GestorRespaldosBeta(self.memoria)
        self.respaldos_automaticos = (
            self.memoria.obtener_estado("respaldos_automaticos", "1") == "1"
        )
        self.respaldo_en_curso = False

        # -------------------- tamaño --------------------
        try:
            self.tamano_beta = int(
                self.memoria.obtener_estado("tamano_beta", str(TAMANO_INICIAL))
            )
        except Exception:
            self.tamano_beta = TAMANO_INICIAL

        self.tamano_beta = max(
            TAMANO_MINIMO,
            min(TAMANO_MAXIMO, self.tamano_beta),
        )

        # -------------------- ventana flotante --------------------
        self.root.title("Beta")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg=COLOR_TRANSPARENTE)

        try:
            self.root.wm_attributes("-transparentcolor", COLOR_TRANSPARENTE)
        except Exception:
            pass

        pantalla_ancho = self.root.winfo_screenwidth()
        pantalla_alto = self.root.winfo_screenheight()

        try:
            posicion_x = int(self.memoria.obtener_estado("pos_x", ""))
            posicion_y = int(self.memoria.obtener_estado("pos_y", ""))
        except Exception:
            posicion_x = pantalla_ancho - self.tamano_beta - 40
            posicion_y = pantalla_alto - self.tamano_beta - 100

        posicion_x = max(0, min(posicion_x, pantalla_ancho - self.tamano_beta))
        posicion_y = max(0, min(posicion_y, pantalla_alto - self.tamano_beta))

        self.root.geometry(
            f"{self.tamano_beta}x{self.tamano_beta}+{posicion_x}+{posicion_y}"
        )

        # -------------------- estados generales --------------------
        self.escuchando = False
        self.hablando = False
        self.procesando = False
        self.procesando_desde = 0.0
        self.procesando_tipo = ""
        self.proceso_id = 0
        self.ojos_cerrados = False
        self.fase_habla = False

        # Sincronización de boca con el audio real de Daniela.
        # nivel_boca_habla: 0=cerrada, 1=suave, 2=media, 3=abierta.
        self.nivel_boca_habla = 0
        self.sincronizacion_boca_activa = False
        self.boca_audio_niveles = []
        self.boca_audio_indice = 0
        self.boca_audio_intervalo_ms = 45
        self.boca_audio_job = None

        self.audio_queue = queue.Queue()
        self.expresion_actual = "normal"
        self.modelo_vosk = None

        # Reconocimiento híbrido Vosk + Faster-Whisper.
        self.modelo_whisper = None
        self.whisper_listo = False
        self.whisper_cargando = False
        self.whisper_error = ""
        self.frecuencia_microfono = 16000

        # Verificación local de identidad por voz. La huella vocal se guarda
        # como embedding numérico en beta.db; las grabaciones de registro se
        # usan de forma temporal y se descartan.
        self.modelo_hablante = None
        self.hablante_listo = False
        self.hablante_cargando = False
        self.hablante_error = ""
        self.hablante_actual = ""
        # v2.5.2: una sesión de conversación explícita conserva quién la abrió.
        # Esto permite tolerar frases MUY cortas como "dame un ejemplo", que
        # producen embeddings menos estables, sin rebajar la seguridad del
        # modo estricto. El umbral reducido solo se usa para seguimientos
        # benignos, dentro de una sesión abierta por una voz fuertemente
        # autenticada.
        self.hablante_sesion_conversacion = ""
        self.ultima_autenticacion_fuerte_ts = 0.0
        self.registrando_voz = False
        self.reconocimiento_hablante_activo = (
            self.memoria.obtener_estado("reconocimiento_hablante", "0") == "1"
        )
        # v2.5.4: si ya existen voces autorizadas, el modo privado no puede
        # arrancar accidentalmente con la biometría desactivada por un estado
        # heredado de versiones anteriores.
        if (
            USAR_RECONOCIMIENTO_HABLANTE
            and HABLANTE_BIOMETRIA_PRIVACIDAD_OBLIGATORIA
            and self.memoria.cantidad_voces_autorizadas() > 0
            and not self.reconocimiento_hablante_activo
        ):
            print("PRIVACIDAD: hay voces autorizadas; activando verificación biométrica obligatoria.")
            self.reconocimiento_hablante_activo = True
            self.memoria.cambiar_estado("reconocimiento_hablante", "1")

        # Estado anti-duplicados/ASR. El hilo de audio puede acumular bloques
        # mientras Whisper tarda varios segundos; al finalizar limpiamos esa
        # cola para no procesar una segunda versión atrasada de la misma orden.
        self.ultimo_texto_asr_aceptado = ""
        self.ultimo_texto_asr_ts = 0.0
        self.transcribiendo_whisper = False
        try:
            self.umbral_hablante = float(
                self.memoria.obtener_estado(
                    "umbral_hablante", str(HABLANTE_UMBRAL_DEFECTO)
                )
            )
        except Exception:
            self.umbral_hablante = HABLANTE_UMBRAL_DEFECTO

        # v2.5.2: el modo privado vuelve a un umbral más estricto. Versiones
        # anteriores pudieron dejar valores cercanos a 0.338, demasiado
        # permisivos para un asistente que permanece escuchando en el escritorio.
        if self.umbral_hablante < HABLANTE_UMBRAL_DEFECTO:
            print(
                f"PRIVACIDAD: elevando umbral de voz de "
                f"{self.umbral_hablante:.3f} a {HABLANTE_UMBRAL_DEFECTO:.3f}."
            )
            self.umbral_hablante = HABLANTE_UMBRAL_DEFECTO
            self.memoria.cambiar_estado(
                "umbral_hablante", f"{self.umbral_hablante:.3f}"
            )

        # Piper se mantiene cargado en memoria para no levantar un proceso
        # nuevo y volver a cargar 114 MB en cada respuesta.
        self.piper_voice = None
        self.piper_listo = False
        self.piper_cargando = False
        self.piper_error = ""
        self.piper_lock = threading.Lock()

        # Marcas de tiempo para diagnosticar latencia real.
        self.ultima_frase_inicio = 0.0

        # Investigación web / continuidad de conversación.
        self.web_cache = {}
        self.ultima_investigacion_web = None
        self.ultima_investigacion_web_ts = 0.0
        self.ultimas_fuentes_web = []

        # Spotify. Los tokens OAuth son datos operativos locales y no se envían
        # a Qwen ni al sistema de memoria inteligente.
        self.spotify_client_id = (self.memoria.obtener_estado("spotify_client_id", "") or "").strip()
        self.spotify_access_token = self._spotify_desproteger_token(
            self.memoria.obtener_estado("spotify_access_token", "") or ""
        )
        self.spotify_refresh_token = self._spotify_desproteger_token(
            self.memoria.obtener_estado("spotify_refresh_token", "") or ""
        )
        try:
            self.spotify_token_expira = float(self.memoria.obtener_estado("spotify_token_expira", "0") or 0)
        except Exception:
            self.spotify_token_expira = 0.0
        self.spotify_autorizado_en = self.memoria.obtener_estado("spotify_autorizado_en", "") or ""
        self.spotify_lock = threading.Lock()
        # Contexto temporal del reproductor: permite órdenes naturales como
        # "siguiente canción" o "pausa la música" poco después de usar Spotify.
        self.spotify_contexto_hasta = 0.0
        # Vocabulario persistente de artistas para ayudar a Whisper con nombres
        # propios (Slipknot, Korn, Linkin Park, etc.) sin bajar la seguridad.
        try:
            vocab_guardado = self.memoria.obtener_estado("spotify_vocabulario", "") or ""
            vocab = json.loads(vocab_guardado) if vocab_guardado else []
            self.spotify_vocabulario = [str(x).strip() for x in vocab if str(x).strip()][:20]
        except Exception:
            self.spotify_vocabulario = []
        # Vocabulario inicial declarado por el Señor + artistas ya conocidos.
        for _nombre_spotify in [
            "Slipknot", "Korn", "Linkin Park", "Limp Bizkit",
            "Panda", "Rammstein", "Ska-P",
        ]:
            if normalizar(_nombre_spotify) not in {normalizar(x) for x in self.spotify_vocabulario}:
                self.spotify_vocabulario.append(_nombre_spotify)
        self.spotify_vocabulario = self.spotify_vocabulario[-20:]

        # Playlists personales de Spotify. Se guardan solo nombre/URI para
        # reconocimiento local de órdenes; no se envían a Qwen ni al sistema
        # de memoria inteligente. El listado vivo se actualiza con /me/playlists.
        self.spotify_playlists_cache = []
        self.spotify_playlists_cache_ts = 0.0
        try:
            bruto_playlists = self.memoria.obtener_estado("spotify_playlists_cache", "") or ""
            datos_playlists = json.loads(bruto_playlists) if bruto_playlists else []
            if isinstance(datos_playlists, list):
                self.spotify_playlists_cache = [
                    x for x in datos_playlists
                    if isinstance(x, dict) and x.get("name") and x.get("uri")
                ][:300]
            self.spotify_playlists_cache_ts = float(
                self.memoria.obtener_estado("spotify_playlists_cache_ts", "0") or 0
            )
        except Exception:
            self.spotify_playlists_cache = []
            self.spotify_playlists_cache_ts = 0.0

        # Si la cuenta ya estaba vinculada, refrescamos playlists en segundo plano
        # sin retrasar el arranque. Un token v2.6.4 puede requerir reautorización
        # porque todavía no incluía playlist-read-private.
        if self.spotify_client_id and (self.spotify_refresh_token or self.spotify_access_token):
            def _precargar_spotify_playlists():
                try:
                    self._spotify_obtener_mis_playlists(forzar=False)
                except Exception as error:
                    print("SPOTIFY: playlists personales pendientes de permiso/actualización:", error)
            threading.Thread(target=_precargar_spotify_playlists, daemon=True).start()

        # Biblioteca académica local: PDFs institucionales + búsqueda semántica.
        self.biblioteca = BibliotecaAcademica()
        self.ultimas_fuentes_academicas = []
        self.ultimo_contexto_academico = None
        self.ultimo_contexto_academico_ts = 0.0
        self.modo_biblioteca_academica = (
            self.memoria.obtener_estado("modo_biblioteca_academica", "si_falta")
            or "si_falta"
        )

        # Biblioteca técnica: libros y manuales de referencia. Se mantiene
        # separada de los apuntes institucionales para no mezclar fuentes.
        self.ultimas_fuentes_tecnicas = []
        self.ultimo_contexto_tecnico = None
        self.ultimo_contexto_tecnico_ts = 0.0
        # v2.8: contexto de consultas que mezclan más de una biblioteca.
        self.ultimo_contexto_inteligente = None
        self.ultimo_contexto_inteligente_ts = 0.0
        self.ultima_decision_biblioteca = {}

        # Modo compañera: iniciativa conversacional muy moderada.
        self.modo_companera = self.memoria.obtener_estado("modo_companera", "1") == "1"
        self.ultima_interaccion_voz = time.time()
        self.ultima_iniciativa_ts = time.time()
        self.proxima_iniciativa_ts = time.time() + random.randint(
            INICIATIVA_MIN_SEGUNDOS, INICIATIVA_MAX_SEGUNDOS
        )

        # Aprendizaje curioso: Beta pregunta poco a poco, una cosa cada vez,
        # y aprende únicamente de respuestas explícitas del Señor.
        self.modo_curioso = self.memoria.obtener_estado("modo_curioso", "1") == "1"
        self.pregunta_curiosa_pendiente = None
        self.pregunta_curiosa_id = 0
        self.pregunta_curiosa_hasta = 0.0
        self.pregunta_curiosa_tema = ""
        self.pregunta_curiosa_tipo = "dato"
        self.ultima_respuesta_curiosa_ts = 0.0
        self.interacciones_desde_curiosidad = 0
        self.proxima_pregunta_curiosa_ts = time.time() + random.randint(
            CURIOSIDAD_MIN_SEGUNDOS, CURIOSIDAD_MAX_SEGUNDOS
        )

        # Unidad de aprendizaje adaptativo. Las evaluaciones habilitan una única
        # respuesta natural, siempre protegida por la biometría de voz.
        self.modo_aprendizaje_adaptativo = (
            self.memoria.obtener_estado("modo_aprendizaje_adaptativo", "1") == "1"
        )
        self.evaluacion_academica_pendiente = None
        self.evaluacion_academica_hasta = 0.0
        self.ultimo_ramo_evaluacion = ""
        self.ultimo_tema_evaluacion = ""

        # Memoria inteligente y continuidad conversacional.
        self.modo_memoria_inteligente = (
            self.memoria.obtener_estado("modo_memoria_inteligente", "1") == "1"
        )
        self.preguntas_seguimiento = (
            self.memoria.obtener_estado("preguntas_seguimiento", "1") == "1"
        )
        self.contexto_tema = self.memoria.obtener_estado("contexto_tema", "") or ""
        self.contexto_resumen = self.memoria.obtener_estado("contexto_resumen", "") or ""
        self.contexto_actualizado_ts = 0.0
        self.contexto_turnos = []
        self.ultimo_mensaje_usuario = ""
        self.ultima_respuesta_beta = ""
        self.cola_memoria_inteligente = queue.Queue()
        self.memoria_inteligente_lock = threading.Lock()
        try:
            self.turnos_desde_resumen = int(
                self.memoria.obtener_estado("turnos_desde_resumen", "0") or 0
            )
        except Exception:
            self.turnos_desde_resumen = 0

        self.esperando_orden = False
        self.tiempo_limite_orden = 0
        # La escucha SIEMPRE inicia en modo estricto, incluso si una sesión
        # anterior terminó en conversación o silencio. Es la opción más segura.
        self.modo_escucha = "estricto"
        self.modo_conversacion_hasta = 0.0
        self.respuesta_actual_id = 0
        # Asociamos cada respuesta con su contexto para reabrir la ventana
        # conversacional exactamente cuando termina la voz de Daniela.
        self.respuesta_tipo_por_id = {}
        # Último tipo de respuesta que Daniela terminó de pronunciar. Se usa para
        # decidir si una orden corta y ambigua (por ejemplo, "profundiza") debe
        # heredar el contexto académico anterior en vez de caer al chat general.
        self.ultimo_tipo_respuesta_terminada = "general"
        # Mientras se pronuncia el informe de inicio, el micrófono permanece
        # apagado para que Beta no se escuche a sí misma.
        self.informe_inicio_en_curso = False

        # -------------------- arrastre --------------------
        self.arrastre_x = 0
        self.arrastre_y = 0

        # -------------------- ojos --------------------
        self.centro_ojo_izquierdo = (0, 0)
        self.centro_ojo_derecho = (0, 0)
        self.radio_movimiento_pupila = 10
        self.radio_iris = 8
        self.radio_pupila = 6
        self.radio_brillo_pupila = 2

        # -------------------- inactividad --------------------
        self.ultima_posicion_mouse = (
            self.root.winfo_pointerx(),
            self.root.winfo_pointery(),
        )
        self.ultimo_movimiento_mouse = time.time()
        self.impaciente = False

        # -------------------- comprensión --------------------
        self.ultimo_no_entendido = ""
        self.fallos_consecutivos = 0

        # -------------------- canvas --------------------
        self.canvas = tk.Canvas(
            self.root,
            width=self.tamano_beta,
            height=self.tamano_beta,
            bg=COLOR_TRANSPARENTE,
            highlightthickness=0,
            bd=0,
        )
        self.canvas.pack(fill="both", expand=True)

        # -------------------- cuerpo 3D --------------------
        self.cuerpo_sombra = self.canvas.create_oval(
            0, 0, 0, 0, fill=COLOR_BORDE_OSCURO, outline=""
        )
        self.cuerpo_borde = self.canvas.create_oval(
            0, 0, 0, 0, fill=COLOR_BORDE_MEDIO, outline=""
        )
        self.cuerpo = self.canvas.create_oval(
            0, 0, 0, 0, fill=COLOR_CUERPO, outline=""
        )
        self.cuerpo_claro = self.canvas.create_oval(
            0, 0, 0, 0, fill=COLOR_CUERPO_CLARO, outline=""
        )

        self.reflejo_grande = self.canvas.create_oval(
            0, 0, 0, 0, fill=COLOR_LUZ_SUAVE, outline=""
        )
        self.reflejo_medio = self.canvas.create_oval(
            0, 0, 0, 0, fill=COLOR_LUZ, outline=""
        )
        self.reflejo_pequeno = self.canvas.create_oval(
            0, 0, 0, 0, fill=COLOR_REFLEJO, outline=""
        )
        self.reflejo_inferior = self.canvas.create_line(
            0,
            0,
            0,
            0,
            fill=COLOR_REFLEJO_INFERIOR,
            width=4,
            smooth=True,
            capstyle=tk.ROUND,
        )

        # -------------------- ojos --------------------
        self.sombra_ojo_izquierdo = self.canvas.create_oval(
            0, 0, 0, 0, fill=COLOR_SOMBRA_OJO, outline=""
        )
        self.sombra_ojo_derecho = self.canvas.create_oval(
            0, 0, 0, 0, fill=COLOR_SOMBRA_OJO, outline=""
        )

        self.ojo_izquierdo = self.canvas.create_oval(
            0, 0, 0, 0, fill=COLOR_BLANCO, outline=""
        )
        self.ojo_derecho = self.canvas.create_oval(
            0, 0, 0, 0, fill=COLOR_BLANCO, outline=""
        )

        self.iris_izquierda = self.canvas.create_oval(
            0, 0, 0, 0, fill=COLOR_IRIS, outline=""
        )
        self.iris_derecha = self.canvas.create_oval(
            0, 0, 0, 0, fill=COLOR_IRIS, outline=""
        )

        self.pupila_izquierda = self.canvas.create_oval(
            0, 0, 0, 0, fill=COLOR_PUPILA, outline=""
        )
        self.pupila_derecha = self.canvas.create_oval(
            0, 0, 0, 0, fill=COLOR_PUPILA, outline=""
        )

        self.brillo_pupila_izq = self.canvas.create_oval(
            0, 0, 0, 0, fill=COLOR_REFLEJO_PUPILA, outline=""
        )
        self.brillo_pupila_der = self.canvas.create_oval(
            0, 0, 0, 0, fill=COLOR_REFLEJO_PUPILA, outline=""
        )
        self.brillo_pupila_izq_2 = self.canvas.create_oval(
            0, 0, 0, 0, fill=COLOR_REFLEJO_PUPILA_2, outline=""
        )
        self.brillo_pupila_der_2 = self.canvas.create_oval(
            0, 0, 0, 0, fill=COLOR_REFLEJO_PUPILA_2, outline=""
        )

        # -------------------- cejas --------------------
        self.ceja_izquierda = self.canvas.create_line(
            0,
            0,
            0,
            0,
            fill=COLOR_CEJA,
            width=4,
            smooth=True,
            capstyle=tk.ROUND,
        )
        self.ceja_derecha = self.canvas.create_line(
            0,
            0,
            0,
            0,
            fill=COLOR_CEJA,
            width=4,
            smooth=True,
            capstyle=tk.ROUND,
        )

        # -------------------- boca --------------------
        self.boca = self.canvas.create_line(
            0,
            0,
            0,
            0,
            fill=COLOR_BOCA,
            width=5,
            smooth=True,
            capstyle=tk.ROUND,
        )
        self.boca_brillo = self.canvas.create_line(
            0,
            0,
            0,
            0,
            fill=COLOR_BOCA_BRILLO,
            width=3,
            smooth=True,
            capstyle=tk.ROUND,
        )
        self.boca_abierta = self.canvas.create_oval(
            0, 0, 0, 0, fill=COLOR_BOCA, outline=""
        )
        self.boca_interior = self.canvas.create_oval(
            0, 0, 0, 0, fill=COLOR_BOCA_BRILLO, outline=""
        )

        # -------------------- eventos --------------------
        self.canvas.bind("<ButtonPress-1>", self.iniciar_arrastre)
        self.canvas.bind("<B1-Motion>", self.arrastrar_beta)
        self.canvas.bind("<ButtonRelease-1>", self.guardar_posicion)
        self.canvas.bind("<Button-3>", self.mostrar_menu)
        self.canvas.bind("<MouseWheel>", self.cambiar_tamano_rueda)
        self.canvas.bind("<Configure>", self.redibujar_beta)

        # -------------------- menú --------------------
        self.crear_menu()

        # -------------------- procesos --------------------
        self.root.after(300, self.redibujar_beta)
        self.root.after(1000, self.parpadear)
        self.root.after(100, self.actualizar_pupilas)
        self.root.after(500, self.vigilar_inactividad)
        self.root.after(1000, self.vigilar_procesamiento)
        self.root.after(500, self.mantener_siempre_visible)

        # Cargas pesadas en segundo plano. Piper primero para que la voz quede
        # lista; Whisper y Ollama se preparan después sin congelar la interfaz.
        threading.Thread(target=self.cargar_piper_en_memoria, daemon=True).start()
        if (
            USAR_RECONOCIMIENTO_HABLANTE
            and (
                self.reconocimiento_hablante_activo
                or self.memoria.cantidad_voces_autorizadas() > 0
            )
        ):
            threading.Thread(target=self.cargar_modelo_hablante, daemon=True).start()
        self.root.after(700, self.iniciar_beta)
        self.root.after(5000, self.calentar_ollama_en_segundo_plano)
        self.root.after(7000, self.precargar_clima_en_segundo_plano)
        self.root.after(9000, self.preparar_biblioteca_en_segundo_plano)
        self.root.after(60000, self.vigilar_iniciativa)
        self.root.after(45000, self.vigilar_curiosidad)
        self.root.after(RESPALDO_INICIO_MS, self.revisar_respaldo_automatico)
        threading.Thread(target=self.worker_memoria_inteligente, daemon=True).start()

    # ======================================================
    # MENÚ / INTERFACES DE APRENDIZAJE
    # ======================================================

    def crear_menu(self):
        self.menu = tk.Menu(self.root, tearoff=0)

        self.menu.add_command(
            label="Enseñar comando...",
            command=self.ventana_ensenar_comando,
        )
        self.menu.add_command(
            label="Enseñar información...",
            command=self.ventana_ensenar_informacion,
        )
        self.menu.add_command(
            label="Administrar memoria y comandos...",
            command=self.ventana_administrar,
        )
        self.menu.add_command(
            label="Estado y aprendizaje de Beta...",
            command=self.ventana_estado_beta,
        )

        self.menu_respaldos = tk.Menu(self.menu, tearoff=0)
        self.menu_respaldos.add_command(
            label="Crear respaldo ahora",
            command=self.crear_respaldo_manual,
        )
        self.menu_respaldos.add_command(
            label="Ver estado de respaldos...",
            command=self.ventana_estado_respaldos,
        )
        self.menu_respaldos.add_command(
            label="Comprobar último respaldo",
            command=self.comprobar_ultimo_respaldo,
        )
        self.menu_respaldos.add_command(
            label="Abrir carpeta de respaldos",
            command=self.abrir_carpeta_respaldos,
        )
        self.menu_respaldos.add_separator()
        self.var_respaldos_automaticos = tk.BooleanVar(value=self.respaldos_automaticos)
        self.menu_respaldos.add_checkbutton(
            label="Respaldos automáticos (cada 24 h)",
            variable=self.var_respaldos_automaticos,
            command=self.cambiar_respaldos_automaticos,
        )
        self.menu.add_cascade(label="Seguridad y respaldos", menu=self.menu_respaldos)

        self.menu_biblioteca = tk.Menu(self.menu, tearoff=0)
        self.menu_biblioteca.add_command(
            label="Agregar PDFs...",
            command=self.agregar_pdfs_biblioteca,
        )
        self.menu_biblioteca.add_command(
            label="Ver documentos...",
            command=self.ventana_biblioteca_documentos,
        )
        self.menu_biblioteca.add_command(
            label="Comprobar OCR...",
            command=self.comprobar_ocr_biblioteca,
        )
        self.menu_biblioteca.add_command(
            label="Buscar en mis apuntes...",
            command=self.buscar_biblioteca_manual,
        )
        self.menu_biblioteca.add_command(
            label="Ver últimas fuentes académicas...",
            command=self.ventana_fuentes_academicas,
        )
        self.menu_biblioteca.add_separator()
        self.menu_biblioteca.add_command(
            label="Configurar biblioteca...",
            command=self.configurar_biblioteca_academica,
        )
        self.menu.add_cascade(
            label="Biblioteca académica",
            menu=self.menu_biblioteca,
        )

        self.menu_biblioteca_tecnica = tk.Menu(self.menu, tearoff=0)
        self.menu_biblioteca_tecnica.add_command(
            label="Agregar libro / PDF técnico...",
            command=self.agregar_pdfs_biblioteca_tecnica,
        )
        self.menu_biblioteca_tecnica.add_command(
            label="Ver libros técnicos...",
            command=self.ventana_biblioteca_tecnica,
        )
        self.menu_biblioteca_tecnica.add_command(
            label="Buscar en libros técnicos...",
            command=self.buscar_biblioteca_tecnica_manual,
        )
        self.menu_biblioteca_tecnica.add_command(
            label="Ver últimas fuentes técnicas...",
            command=self.ventana_fuentes_tecnicas,
        )
        self.menu_biblioteca_tecnica.add_separator()
        self.menu_biblioteca_tecnica.add_command(
            label="Estado / reconstruir índice...",
            command=self.ventana_estado_indice_conocimiento,
        )
        self.menu_biblioteca_tecnica.add_command(
            label="Biblioteca inteligente / diagnóstico...",
            command=self.ventana_biblioteca_inteligente,
        )
        self.menu.add_cascade(
            label="Biblioteca técnica",
            menu=self.menu_biblioteca_tecnica,
        )

        self.menu_aprendizaje = tk.Menu(self.menu, tearoff=0)
        self.menu_aprendizaje.add_command(
            label="Ver progreso académico...", command=self.ventana_progreso_academico
        )
        self.menu_aprendizaje.add_command(
            label="Evaluarme con mis apuntes...", command=self.evaluacion_manual
        )
        self.menu_aprendizaje.add_command(
            label="Qué debería repasar", command=self.responder_recomendacion_repaso
        )
        self.menu_aprendizaje.add_separator()
        self.var_aprendizaje_adaptativo = tk.BooleanVar(value=self.modo_aprendizaje_adaptativo)
        self.menu_aprendizaje.add_checkbutton(
            label="Aprendizaje adaptativo", variable=self.var_aprendizaje_adaptativo,
            command=self.cambiar_aprendizaje_adaptativo
        )
        self.menu.add_cascade(label="Unidad de aprendizaje", menu=self.menu_aprendizaje)

        self.menu.add_separator()
        self.menu.add_command(
            label="Configurar clima...",
            command=self.configurar_clima,
        )
        self.menu.add_command(
            label="Buscar en Google...",
            command=self.buscar_google_manual,
        )
        self.menu.add_command(
            label="Reproducir en YouTube...",
            command=self.youtube_manual,
        )

        self.menu_spotify = tk.Menu(self.menu, tearoff=0)
        self.menu_spotify.add_command(label="Abrir Spotify", command=self.abrir_spotify_inicio)
        self.menu_spotify.add_command(label="Buscar en Spotify...", command=self.spotify_buscar_manual)
        self.menu_spotify.add_command(label="Reproducir artista en Spotify...", command=self.spotify_reproducir_manual)
        self.menu_spotify.add_command(label="Reproducir playlist en Spotify...", command=self.spotify_playlist_manual)
        self.menu_spotify.add_command(label="Mis playlists de Spotify", command=self.spotify_listar_playlists_async)
        self.menu_spotify.add_command(label="Mis preferencias de Spotify", command=self.spotify_preferencias_async)
        self.menu_spotify.add_separator()
        self.menu_spotify.add_command(label="Reconectar / actualizar permisos", command=self.spotify_reconectar_permisos)
        self.menu_spotify.add_command(label="Configurar / conectar cuenta...", command=self.configurar_spotify)
        self.menu_spotify.add_command(label="Desconectar cuenta", command=self.desconectar_spotify)
        self.menu.add_cascade(label="Spotify", menu=self.menu_spotify)

        self.menu.add_command(
            label="Investigar en Internet...",
            command=self.investigar_internet_manual,
        )
        self.menu.add_command(
            label="Ver últimas fuentes...",
            command=self.ventana_fuentes_web,
        )

        self.var_memoria_inteligente = tk.BooleanVar(value=self.modo_memoria_inteligente)
        self.menu.add_checkbutton(
            label="Memoria inteligente automática",
            variable=self.var_memoria_inteligente,
            command=self.cambiar_memoria_inteligente,
        )

        self.var_preguntas_seguimiento = tk.BooleanVar(value=self.preguntas_seguimiento)
        self.menu.add_checkbutton(
            label="Preguntas de seguimiento",
            variable=self.var_preguntas_seguimiento,
            command=self.cambiar_preguntas_seguimiento,
        )

        self.var_modo_companera = tk.BooleanVar(value=self.modo_companera)
        self.menu.add_checkbutton(
            label="Modo compañera (iniciativa espontánea)",
            variable=self.var_modo_companera,
            command=self.cambiar_modo_companera,
        )

        self.var_modo_curioso = tk.BooleanVar(value=self.modo_curioso)
        self.menu.add_checkbutton(
            label="Modo curioso (aprender del Señor)",
            variable=self.var_modo_curioso,
            command=self.cambiar_modo_curioso,
        )
        self.menu.add_command(
            label="Hazme una pregunta para conocerme",
            command=lambda: self.generar_pregunta_curiosa_async(forzada=True),
        )

        self.menu.add_separator()
        self.var_modo_escucha = tk.StringVar(value=self.modo_escucha)
        self.menu_escucha = tk.Menu(self.menu, tearoff=0)
        self.menu_escucha.add_radiobutton(
            label="Estricto (recomendado)",
            value="estricto",
            variable=self.var_modo_escucha,
            command=self.cambiar_modo_escucha_menu,
        )
        self.menu_escucha.add_radiobutton(
            label="Conversación (60 s de silencio)",
            value="conversacion",
            variable=self.var_modo_escucha,
            command=self.cambiar_modo_escucha_menu,
        )
        self.menu_escucha.add_radiobutton(
            label="Silencio",
            value="silencio",
            variable=self.var_modo_escucha,
            command=self.cambiar_modo_escucha_menu,
        )
        self.menu.add_cascade(label="Modo de escucha", menu=self.menu_escucha)

        self.menu.add_separator()
        self.var_reconocimiento_hablante = tk.BooleanVar(
            value=self.reconocimiento_hablante_activo
        )
        self.menu.add_checkbutton(
            label="Solo voces autorizadas",
            variable=self.var_reconocimiento_hablante,
            command=self.cambiar_reconocimiento_hablante,
        )
        self.menu.add_command(
            label="Registrar voz autorizada...",
            command=self.ventana_registrar_voz,
        )
        self.menu.add_command(
            label="Administrar voces autorizadas...",
            command=self.ventana_administrar_voces,
        )

        self.menu.add_separator()
        self.menu.add_command(
            label="Probar IA local (Ollama)",
            command=self.probar_ollama,
        )
        self.menu.add_command(
            label="Información IA local",
            command=self.informacion_ollama,
        )

        self.menu.add_separator()
        self.menu.add_command(label="Aumentar tamaño", command=self.aumentar_tamano)
        self.menu.add_command(label="Disminuir tamaño", command=self.disminuir_tamano)
        self.menu.add_command(label="Tamaño normal", command=self.tamano_normal)

        self.menu.add_separator()
        self.menu.add_command(label="Cerrar Beta", command=self.cerrar_beta)

    def mostrar_menu(self, event):
        self.registrar_actividad()
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def ventana_ensenar_comando(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Enseñar comando a Beta")
        ventana.geometry("560x430")
        ventana.attributes("-topmost", True)

        ttk.Label(
            ventana,
            text="Frases que activarán el comando (una por línea):",
        ).pack(anchor="w", padx=15, pady=(15, 5))

        texto_frases = tk.Text(ventana, height=7, wrap="word")
        texto_frases.pack(fill="x", padx=15)

        ttk.Label(
            ventana,
            text="Respuesta que Beta debe decir:",
        ).pack(anchor="w", padx=15, pady=(15, 5))

        texto_respuesta = tk.Text(ventana, height=8, wrap="word")
        texto_respuesta.pack(fill="both", expand=True, padx=15)

        def guardar():
            frases = [
                f.strip()
                for f in texto_frases.get("1.0", "end").splitlines()
                if f.strip()
            ]
            respuesta = texto_respuesta.get("1.0", "end").strip()

            if not frases or not respuesta:
                messagebox.showwarning(
                    "Beta",
                    "Escriba al menos una frase y una respuesta.",
                    parent=ventana,
                )
                return

            for frase in frases:
                self.memoria.guardar_comando(frase, respuesta)

            messagebox.showinfo(
                "Beta",
                f"Aprendí {len(frases)} frase(s) para ese comando.",
                parent=ventana,
            )
            ventana.destroy()

        ttk.Button(ventana, text="Guardar", command=guardar).pack(pady=15)

    def ventana_ensenar_informacion(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Enseñar información a Beta")
        ventana.geometry("560x360")
        ventana.attributes("-topmost", True)

        ttk.Label(
            ventana,
            text="Escriba la información que Beta debe recordar:",
        ).pack(anchor="w", padx=15, pady=(15, 5))

        texto = tk.Text(ventana, wrap="word")
        texto.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        def guardar():
            contenido = texto.get("1.0", "end").strip()
            if not contenido:
                return

            guardado = self.memoria.guardar_recuerdo(contenido, importancia=2)

            if guardado:
                messagebox.showinfo("Beta", "Información guardada.", parent=ventana)
            else:
                messagebox.showinfo(
                    "Beta",
                    "Esa información ya estaba en mi memoria.",
                    parent=ventana,
                )
            ventana.destroy()

        ttk.Button(ventana, text="Guardar", command=guardar).pack(pady=(0, 15))

    def ventana_administrar(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Memoria de Beta")
        ventana.geometry("850x560")
        ventana.attributes("-topmost", True)

        notebook = ttk.Notebook(ventana)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        marco_recuerdos = ttk.Frame(notebook)
        marco_comandos = ttk.Frame(notebook)
        notebook.add(marco_recuerdos, text="Recuerdos")
        notebook.add(marco_comandos, text="Comandos")

        # Recuerdos
        tabla_recuerdos = ttk.Treeview(
            marco_recuerdos,
            columns=("id", "tipo", "contenido", "fecha"),
            show="headings",
        )
        tabla_recuerdos.heading("id", text="ID")
        tabla_recuerdos.heading("tipo", text="Tipo")
        tabla_recuerdos.heading("contenido", text="Contenido")
        tabla_recuerdos.heading("fecha", text="Fecha")
        tabla_recuerdos.column("id", width=55, anchor="center")
        tabla_recuerdos.column("tipo", width=100, anchor="center")
        tabla_recuerdos.column("contenido", width=490)
        tabla_recuerdos.column("fecha", width=150)
        tabla_recuerdos.pack(fill="both", expand=True, padx=8, pady=8)

        for fila in self.memoria.listar_recuerdos():
            tabla_recuerdos.insert("", "end", values=(fila[0], fila[4], fila[1], fila[2]))

        def borrar_recuerdo():
            seleccion = tabla_recuerdos.selection()
            if not seleccion:
                return
            item = tabla_recuerdos.item(seleccion[0])
            recuerdo_id = item["values"][0]
            self.memoria.eliminar_recuerdo_id(recuerdo_id)
            tabla_recuerdos.delete(seleccion[0])

        ttk.Button(
            marco_recuerdos,
            text="Eliminar recuerdo seleccionado",
            command=borrar_recuerdo,
        ).pack(pady=(0, 8))

        # Comandos
        tabla_comandos = ttk.Treeview(
            marco_comandos,
            columns=("id", "frase", "respuesta"),
            show="headings",
        )
        tabla_comandos.heading("id", text="ID")
        tabla_comandos.heading("frase", text="Frase")
        tabla_comandos.heading("respuesta", text="Respuesta")
        tabla_comandos.column("id", width=55, anchor="center")
        tabla_comandos.column("frase", width=260)
        tabla_comandos.column("respuesta", width=470)
        tabla_comandos.pack(fill="both", expand=True, padx=8, pady=8)

        for fila in self.memoria.listar_comandos():
            tabla_comandos.insert("", "end", values=(fila[0], fila[1], fila[2]))

        def borrar_comando():
            seleccion = tabla_comandos.selection()
            if not seleccion:
                return
            item = tabla_comandos.item(seleccion[0])
            comando_id = item["values"][0]
            self.memoria.eliminar_comando_id(comando_id)
            tabla_comandos.delete(seleccion[0])

        ttk.Button(
            marco_comandos,
            text="Eliminar comando seleccionado",
            command=borrar_comando,
        ).pack(pady=(0, 8))

    def ventana_estado_beta(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Estado y aprendizaje de Beta")
        ventana.geometry("520x500")
        ventana.attributes("-topmost", True)

        ttk.Label(
            ventana,
            text="Parámetros de comportamiento de Beta",
            font=("Segoe UI", 12, "bold"),
        ).pack(pady=(15, 8))

        ttk.Label(
            ventana,
            text=(
                "Estos valores ajustan su forma de responder. No representan emociones "
                "o conciencia real."
            ),
            wraplength=460,
            justify="left",
        ).pack(padx=20, pady=(0, 12), anchor="w")

        perfil = self.memoria.obtener_perfil()
        marco = ttk.Frame(ventana)
        marco.pack(fill="x", padx=20)

        nombres = {
            "energia": "Energía",
            "curiosidad": "Curiosidad",
            "confianza": "Confianza",
            "humor": "Humor",
            "familiaridad": "Familiaridad",
            "serenidad": "Serenidad",
        }

        for clave, nombre in nombres.items():
            fila = ttk.Frame(marco)
            fila.pack(fill="x", pady=4)
            ttk.Label(fila, text=nombre, width=14).pack(side="left")
            barra = ttk.Progressbar(fila, maximum=100, value=perfil.get(clave, 50))
            barra.pack(side="left", fill="x", expand=True, padx=8)
            ttk.Label(fila, text=str(perfil.get(clave, 50)), width=4).pack(side="right")

        ttk.Separator(ventana).pack(fill="x", padx=20, pady=15)

        aprendizaje = tk.BooleanVar(
            value=self.memoria.obtener_estado("modo_aprendizaje_natural", "1") == "1"
        )

        def cambiar_aprendizaje():
            self.memoria.cambiar_estado(
                "modo_aprendizaje_natural",
                "1" if aprendizaje.get() else "0",
            )

        ttk.Checkbutton(
            ventana,
            text="Aprendizaje natural de preferencias, objetivos y pendientes",
            variable=aprendizaje,
            command=cambiar_aprendizaje,
        ).pack(anchor="w", padx=20, pady=4)

        conteos = self.memoria.contar_recuerdos_por_tipo()
        resumen = ", ".join(f"{k}: {v}" for k, v in sorted(conteos.items())) or "sin recuerdos"
        ttk.Label(
            ventana,
            text=f"Interacciones: {perfil.get('interacciones', 0)}\nMemoria: {resumen}",
            wraplength=460,
            justify="left",
        ).pack(anchor="w", padx=20, pady=15)

        ttk.Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=10)

    # ======================================================
    # SEGURIDAD / RESPALDOS v2.7.1
    # ======================================================

    def cambiar_respaldos_automaticos(self):
        try:
            self.respaldos_automaticos = bool(self.var_respaldos_automaticos.get())
        except Exception:
            self.respaldos_automaticos = not self.respaldos_automaticos
        self.memoria.cambiar_estado(
            "respaldos_automaticos", "1" if self.respaldos_automaticos else "0"
        )
        estado = "activados" if self.respaldos_automaticos else "desactivados"
        print(f"RESPALDOS AUTOMÁTICOS: {estado}.")

    def _lanzar_respaldo(self, motivo="manual", mostrar_resultado=False):
        if self.respaldo_en_curso:
            if mostrar_resultado:
                messagebox.showinfo(
                    "Respaldos de Beta",
                    "Ya hay un respaldo en curso.",
                    parent=self.root,
                )
            return

        self.respaldo_en_curso = True

        def trabajo():
            try:
                resultado = self.gestor_respaldos.crear_respaldo(motivo=motivo)
                if mostrar_resultado:
                    def ok():
                        try:
                            messagebox.showinfo(
                                "Respaldos de Beta",
                                "Respaldo creado correctamente.\n\n"
                                f"Archivo: {resultado['ruta'].name}\n"
                                f"Tamaño: {resultado['tamano'] / (1024 * 1024):.1f} MB\n"
                                f"Carpeta: {RESPALDOS_DIR}",
                                parent=self.root,
                            )
                        except tk.TclError:
                            pass
                    self.root.after(0, ok)
            except Exception as error:
                print("RESPALDO ERROR:", error)
                if mostrar_resultado:
                    def fallo(msg=str(error)):
                        try:
                            messagebox.showerror(
                                "Respaldos de Beta",
                                f"No pude crear el respaldo.\n\n{msg}",
                                parent=self.root,
                            )
                        except tk.TclError:
                            pass
                    self.root.after(0, fallo)
            finally:
                self.respaldo_en_curso = False

        threading.Thread(target=trabajo, daemon=True).start()

    def crear_respaldo_manual(self):
        self._lanzar_respaldo(motivo="manual", mostrar_resultado=True)

    def revisar_respaldo_automatico(self):
        try:
            if (
                self.respaldos_automaticos
                and not self.respaldo_en_curso
                and self.gestor_respaldos.debe_crear_automatico()
            ):
                print("RESPALDO AUTOMÁTICO: corresponde crear una nueva copia.")
                self._lanzar_respaldo(motivo="automatico", mostrar_resultado=False)
        except Exception as error:
            print("RESPALDO AUTOMÁTICO: no se pudo revisar:", error)
        finally:
            try:
                self.root.after(RESPALDO_REVISION_MS, self.revisar_respaldo_automatico)
            except tk.TclError:
                pass

    def abrir_carpeta_respaldos(self):
        try:
            RESPALDOS_DIR.mkdir(parents=True, exist_ok=True)
            if os.name == "nt":
                os.startfile(str(RESPALDOS_DIR))
            else:
                subprocess.Popen(["xdg-open", str(RESPALDOS_DIR)])
        except Exception as error:
            messagebox.showerror(
                "Respaldos de Beta",
                f"No pude abrir la carpeta.\n\n{error}",
                parent=self.root,
            )

    def comprobar_ultimo_respaldo(self):
        if self.respaldo_en_curso:
            messagebox.showinfo(
                "Respaldos de Beta",
                "Espere a que termine el respaldo que está en curso.",
                parent=self.root,
            )
            return

        def trabajo():
            ok, mensaje = self.gestor_respaldos.verificar_respaldo()
            def mostrar():
                try:
                    if ok:
                        messagebox.showinfo(
                            "Respaldos de Beta",
                            "Verificación correcta.\n\n" + mensaje,
                            parent=self.root,
                        )
                    else:
                        messagebox.showerror(
                            "Respaldos de Beta",
                            "El respaldo no pasó la verificación.\n\n" + mensaje,
                            parent=self.root,
                        )
                except tk.TclError:
                    pass
            self.root.after(0, mostrar)

        threading.Thread(target=trabajo, daemon=True).start()

    def ventana_estado_respaldos(self):
        RESPALDOS_DIR.mkdir(parents=True, exist_ok=True)
        archivos = self.gestor_respaldos.listar_respaldos()
        ultimo = archivos[0] if archivos else None
        libre_mb = self.gestor_respaldos.espacio_libre_mb()

        if ultimo:
            fecha = datetime.fromtimestamp(ultimo.stat().st_mtime)
            edad_seg = max(0, time.time() - ultimo.stat().st_mtime)
            horas = edad_seg / 3600
            ultimo_txt = (
                f"{ultimo.name}\n"
                f"{fecha.strftime('%d/%m/%Y %H:%M:%S')} | "
                f"{ultimo.stat().st_size / (1024 * 1024):.1f} MB | "
                f"hace {horas:.1f} h"
            )
        else:
            ultimo_txt = "Todavía no hay respaldos."

        ventana = tk.Toplevel(self.root)
        ventana.title("Seguridad y respaldos de Beta")
        ventana.geometry("680x510")
        ventana.attributes("-topmost", True)

        ttk.Label(
            ventana,
            text="Respaldos automáticos de Beta",
            font=("Segoe UI", 13, "bold"),
        ).pack(anchor="w", padx=18, pady=(16, 8))

        estado_auto = "Activados" if self.respaldos_automaticos else "Desactivados"
        texto = (
            f"Estado: {estado_auto}\n"
            f"Frecuencia: cada 24 horas\n"
            f"Retención: últimas {RESPALDO_RETENCION} copias\n"
            f"Copias disponibles: {len(archivos)}\n"
            f"Espacio libre en la unidad de Beta: {libre_mb / 1024:.1f} GB\n\n"
            f"Último respaldo:\n{ultimo_txt}\n\n"
            "Cada ZIP incluye una copia consistente de beta.db, el beta.py que la creó, "
            "el manifiesto de la biblioteca y, cuando están disponibles, los índices vectoriales.\n\n"
            "Para evitar llenar el SSD, los modelos de IA y los PDF originales no se duplican "
            "dentro de cada respaldo automático. El conocimiento procesado, memoria, progreso, "
            "preferencias y metadatos sí quedan dentro de beta.db."
        )
        ttk.Label(
            ventana,
            text=texto,
            wraplength=635,
            justify="left",
        ).pack(anchor="w", padx=18, pady=8)

        marco = ttk.Frame(ventana)
        marco.pack(fill="x", padx=18, pady=12)
        ttk.Button(
            marco, text="Crear respaldo ahora", command=self.crear_respaldo_manual
        ).pack(side="left", padx=(0, 8))
        ttk.Button(
            marco, text="Comprobar último", command=self.comprobar_ultimo_respaldo
        ).pack(side="left", padx=(0, 8))
        ttk.Button(
            marco, text="Abrir carpeta", command=self.abrir_carpeta_respaldos
        ).pack(side="left")

        ttk.Label(
            ventana,
            text=f"Carpeta: {RESPALDOS_DIR}",
            wraplength=635,
        ).pack(anchor="w", padx=18, pady=(8, 0))
        ttk.Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=18)

    # ======================================================
    # CONTROL DE PROCESAMIENTO / WATCHDOG
    # Evita que Beta quede bloqueada indefinidamente si una petición falla.
    # ======================================================

    def iniciar_proceso(self, tipo):
        ahora = time.time()

        # Si un proceso quedó bloqueado demasiado tiempo, lo liberamos.
        if self.procesando and self.procesando_desde:
            antiguedad = ahora - self.procesando_desde
            if antiguedad > PROCESO_MAX_SEGUNDOS:
                print(
                    f"WATCHDOG: liberando proceso bloqueado ({self.procesando_tipo}) "
                    f"después de {int(antiguedad)} s."
                )
                self.procesando = False
                self.procesando_tipo = ""
                self.procesando_desde = 0.0
                self.proceso_id += 1

        if self.procesando:
            return None

        self.proceso_id += 1
        token = self.proceso_id
        self.procesando = True
        self.procesando_desde = ahora
        self.procesando_tipo = tipo
        return token

    def terminar_proceso(self, token):
        # Solo libera el proceso si corresponde a la operación actual.
        if token == self.proceso_id:
            self.procesando = False
            self.procesando_desde = 0.0
            self.procesando_tipo = ""

    def vigilar_procesamiento(self):
        try:
            if self.procesando and self.procesando_desde:
                antiguedad = time.time() - self.procesando_desde
                if antiguedad > PROCESO_MAX_SEGUNDOS:
                    tipo = self.procesando_tipo or "desconocido"
                    print(
                        f"WATCHDOG: el proceso {tipo} superó "
                        f"{PROCESO_MAX_SEGUNDOS} segundos. Reiniciando estado."
                    )
                    self.proceso_id += 1
                    self.procesando = False
                    self.procesando_desde = 0.0
                    self.procesando_tipo = ""
                    if not self.hablando:
                        self.responder(
                            "la consulta anterior tardó demasiado y la cancelé para no quedar bloqueada. Puede preguntarme nuevamente.",
                            "confundida",
                        )
        except Exception as error:
            print("ERROR WATCHDOG:", error)

        try:
            self.root.after(1000, self.vigilar_procesamiento)
        except tk.TclError:
            pass

    # ======================================================
    # CLIMA (ÚNICO MÓDULO QUE USA INTERNET EXTERNO)
    # ======================================================

    def configurar_clima(self):
        actual = self.memoria.obtener_estado("ciudad_clima", "") or ""
        ciudad = simpledialog.askstring(
            "Clima de Beta",
            "Ciudad para las consultas meteorológicas:\nEjemplo: Santiago, Chile",
            initialvalue=actual,
            parent=self.root,
        )

        if ciudad is None:
            return

        ciudad = ciudad.strip()
        self.memoria.cambiar_estado("ciudad_clima", ciudad)

        # Al cambiar de ciudad invalidamos coordenadas y clima almacenados.
        for clave, valor in [
            ("clima_lat", ""),
            ("clima_lon", ""),
            ("clima_nombre", ""),
            ("clima_region", ""),
            ("clima_cache_texto", ""),
            ("clima_cache_ts", "0"),
            ("pronostico_manana_cache_texto", ""),
            ("pronostico_manana_cache_ts", "0"),
        ]:
            self.memoria.cambiar_estado(clave, valor)

        if ciudad:
            messagebox.showinfo(
                "Beta",
                f"Usaré {ciudad} para consultar el clima.",
                parent=self.root,
            )

    def obtener_clima(self):
        ciudad = (self.memoria.obtener_estado("ciudad_clima", "") or "").strip()
        if not ciudad:
            return None, "No tengo una ciudad configurada para el clima."

        # Caché breve: si consultamos hace menos de 5 minutos, responde sin red.
        try:
            cache_texto = self.memoria.obtener_estado("clima_cache_texto", "") or ""
            cache_ts = float(self.memoria.obtener_estado("clima_cache_ts", "0") or 0)
            if cache_texto and (time.time() - cache_ts) <= CLIMA_CACHE_SEGUNDOS:
                print("CLIMA: usando caché reciente.")
                return cache_texto, None
        except Exception:
            pass

        try:
            # Reutilizar coordenadas guardadas para evitar geocodificar en cada consulta.
            lat_txt = self.memoria.obtener_estado("clima_lat", "") or ""
            lon_txt = self.memoria.obtener_estado("clima_lon", "") or ""
            nombre = self.memoria.obtener_estado("clima_nombre", "") or ""
            region = self.memoria.obtener_estado("clima_region", "") or ""

            if lat_txt and lon_txt:
                lat = float(lat_txt)
                lon = float(lon_txt)
                nombre = nombre or ciudad
                print("CLIMA: usando coordenadas guardadas.")
            else:
                q = urllib.parse.quote(ciudad)
                url_geo = (
                    "https://geocoding-api.open-meteo.com/v1/search"
                    f"?name={q}&count=1&language=es&format=json"
                )

                with urllib.request.urlopen(url_geo, timeout=CLIMA_TIMEOUT) as r:
                    geo = json.loads(r.read().decode("utf-8"))

                resultados = geo.get("results") or []
                if not resultados:
                    return None, f"No pude encontrar la ubicación {ciudad}."

                lugar = resultados[0]
                lat = float(lugar["latitude"])
                lon = float(lugar["longitude"])
                nombre = lugar.get("name", ciudad)
                region = lugar.get("admin1") or lugar.get("country") or ""

                self.memoria.cambiar_estado("clima_lat", str(lat))
                self.memoria.cambiar_estado("clima_lon", str(lon))
                self.memoria.cambiar_estado("clima_nombre", nombre)
                self.memoria.cambiar_estado("clima_region", region)

            params = urllib.parse.urlencode(
                {
                    "latitude": lat,
                    "longitude": lon,
                    "current": (
                        "temperature_2m,apparent_temperature,weather_code,"
                        "wind_speed_10m"
                    ),
                    "timezone": "auto",
                }
            )

            url_clima = f"https://api.open-meteo.com/v1/forecast?{params}"

            with urllib.request.urlopen(url_clima, timeout=CLIMA_TIMEOUT) as r:
                datos = json.loads(r.read().decode("utf-8"))

            actual = datos.get("current") or {}
            temperatura = actual.get("temperature_2m")
            sensacion = actual.get("apparent_temperature")
            codigo = actual.get("weather_code")
            viento = actual.get("wind_speed_10m")

            condicion = self.descripcion_codigo_clima(codigo)

            ubicacion = nombre or ciudad
            if region and normalizar(region) not in normalizar(ubicacion):
                ubicacion += f", {region}"

            partes = [
                f"en {ubicacion} hay {self.formatear_numero(temperatura)} grados",
                f"con {condicion}",
            ]

            if sensacion is not None:
                partes.append(
                    f"la sensación térmica es de {self.formatear_numero(sensacion)} grados"
                )

            if viento is not None:
                partes.append(
                    f"y el viento es de aproximadamente {self.formatear_numero(viento)} kilómetros por hora"
                )

            respuesta = ", ".join(partes) + "."
            self.memoria.cambiar_estado("clima_cache_texto", respuesta)
            self.memoria.cambiar_estado("clima_cache_ts", str(time.time()))
            return respuesta, None

        except urllib.error.URLError as error:
            print("ERROR RED CLIMA:", error)
            return None, "No pude conectarme al servicio meteorológico. Revise la conexión a Internet."
        except TimeoutError:
            return None, "La consulta del clima tardó demasiado. Inténtelo nuevamente en unos segundos."
        except Exception as error:
            print("ERROR CLIMA:", error)
            return None, "Tuve un problema al consultar el clima."

    def obtener_pronostico_manana(self):
        """Consulta el pronóstico del día siguiente para la ciudad configurada."""
        ciudad = (self.memoria.obtener_estado("ciudad_clima", "") or "").strip()
        if not ciudad:
            return None, "No tengo una ciudad configurada para el clima."

        # El pronóstico de mañana cambia lentamente, por eso conservamos una
        # caché un poco más larga que la del tiempo actual.
        try:
            cache_texto = (
                self.memoria.obtener_estado("pronostico_manana_cache_texto", "") or ""
            )
            cache_ts = float(
                self.memoria.obtener_estado("pronostico_manana_cache_ts", "0") or 0
            )
            if cache_texto and (time.time() - cache_ts) <= PRONOSTICO_CACHE_SEGUNDOS:
                print("PRONÓSTICO MAÑANA: usando caché reciente.")
                return cache_texto, None
        except Exception:
            pass

        try:
            # Reutilizamos las coordenadas que ya usa el clima actual.
            lat_txt = self.memoria.obtener_estado("clima_lat", "") or ""
            lon_txt = self.memoria.obtener_estado("clima_lon", "") or ""
            nombre = self.memoria.obtener_estado("clima_nombre", "") or ""
            region = self.memoria.obtener_estado("clima_region", "") or ""

            if lat_txt and lon_txt:
                lat = float(lat_txt)
                lon = float(lon_txt)
                nombre = nombre or ciudad
                print("PRONÓSTICO MAÑANA: usando coordenadas guardadas.")
            else:
                q = urllib.parse.quote(ciudad)
                url_geo = (
                    "https://geocoding-api.open-meteo.com/v1/search"
                    f"?name={q}&count=1&language=es&format=json"
                )

                with urllib.request.urlopen(url_geo, timeout=CLIMA_TIMEOUT) as r:
                    geo = json.loads(r.read().decode("utf-8"))

                resultados = geo.get("results") or []
                if not resultados:
                    return None, f"No pude encontrar la ubicación {ciudad}."

                lugar = resultados[0]
                lat = float(lugar["latitude"])
                lon = float(lugar["longitude"])
                nombre = lugar.get("name", ciudad)
                region = lugar.get("admin1") or lugar.get("country") or ""

                self.memoria.cambiar_estado("clima_lat", str(lat))
                self.memoria.cambiar_estado("clima_lon", str(lon))
                self.memoria.cambiar_estado("clima_nombre", nombre)
                self.memoria.cambiar_estado("clima_region", region)

            params = urllib.parse.urlencode(
                {
                    "latitude": lat,
                    "longitude": lon,
                    "daily": (
                        "weather_code,temperature_2m_max,temperature_2m_min,"
                        "apparent_temperature_max,apparent_temperature_min,"
                        "precipitation_probability_max,wind_speed_10m_max"
                    ),
                    "forecast_days": 2,
                    "timezone": "auto",
                }
            )

            url_clima = f"https://api.open-meteo.com/v1/forecast?{params}"

            with urllib.request.urlopen(url_clima, timeout=CLIMA_TIMEOUT) as r:
                datos = json.loads(r.read().decode("utf-8"))

            diario = datos.get("daily") or {}
            fechas = diario.get("time") or []
            if len(fechas) < 2:
                return None, "El servicio meteorológico no entregó el pronóstico de mañana."

            indice = 1

            def valor_diario(clave):
                valores = diario.get(clave) or []
                return valores[indice] if len(valores) > indice else None

            codigo = valor_diario("weather_code")
            maxima = valor_diario("temperature_2m_max")
            minima = valor_diario("temperature_2m_min")
            sensacion_max = valor_diario("apparent_temperature_max")
            sensacion_min = valor_diario("apparent_temperature_min")
            prob_lluvia = valor_diario("precipitation_probability_max")
            viento_max = valor_diario("wind_speed_10m_max")

            condicion = self.descripcion_codigo_clima(codigo)

            ubicacion = nombre or ciudad
            if region and normalizar(region) not in normalizar(ubicacion):
                ubicacion += f", {region}"

            try:
                fecha_manana = datetime.strptime(fechas[indice], "%Y-%m-%d")
                dias = [
                    "lunes", "martes", "miércoles", "jueves",
                    "viernes", "sábado", "domingo",
                ]
                meses = [
                    "enero", "febrero", "marzo", "abril", "mayo", "junio",
                    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
                ]
                fecha_hablada = (
                    f"{dias[fecha_manana.weekday()]} {fecha_manana.day} "
                    f"de {meses[fecha_manana.month - 1]}"
                )
            except Exception:
                fecha_hablada = "mañana"

            partes = [
                f"para mañana, {fecha_hablada}, en {ubicacion} se espera {condicion}",
            ]

            if minima is not None and maxima is not None:
                partes.append(
                    f"con una temperatura mínima de {self.formatear_numero(minima)} grados "
                    f"y una máxima de {self.formatear_numero(maxima)} grados"
                )
            elif maxima is not None:
                partes.append(
                    f"con una temperatura máxima de {self.formatear_numero(maxima)} grados"
                )

            if sensacion_min is not None and sensacion_max is not None:
                partes.append(
                    f"la sensación térmica podría variar entre "
                    f"{self.formatear_numero(sensacion_min)} y "
                    f"{self.formatear_numero(sensacion_max)} grados"
                )

            if prob_lluvia is not None:
                partes.append(
                    f"la probabilidad máxima de precipitación es de "
                    f"{self.formatear_numero(prob_lluvia)} por ciento"
                )

            if viento_max is not None:
                partes.append(
                    f"y el viento podría alcanzar aproximadamente "
                    f"{self.formatear_numero(viento_max)} kilómetros por hora"
                )

            respuesta = ", ".join(partes) + "."
            self.memoria.cambiar_estado("pronostico_manana_cache_texto", respuesta)
            self.memoria.cambiar_estado("pronostico_manana_cache_ts", str(time.time()))
            return respuesta, None

        except urllib.error.URLError as error:
            print("ERROR RED PRONÓSTICO MAÑANA:", error)
            return None, "No pude conectarme al servicio meteorológico para consultar mañana."
        except TimeoutError:
            return None, "El pronóstico de mañana tardó demasiado. Inténtelo nuevamente en unos segundos."
        except Exception as error:
            print("ERROR PRONÓSTICO MAÑANA:", error)
            return None, "Tuve un problema al consultar el pronóstico de mañana."

    def precargar_clima_en_segundo_plano(self):
        """Mantiene una lectura meteorológica reciente para responder casi al instante."""
        def trabajo():
            try:
                ciudad = (self.memoria.obtener_estado("ciudad_clima", "") or "").strip()
                if ciudad:
                    inicio = time.perf_counter()
                    respuesta, error = self.obtener_clima()
                    if respuesta:
                        print(f"CLIMA PRECARGADO en {time.perf_counter() - inicio:.2f} s")
                    elif error:
                        print("CLIMA PRECARGA:", error)
            except Exception as error:
                print("ERROR PRECARGANDO CLIMA:", error)

        threading.Thread(target=trabajo, daemon=True).start()
        try:
            self.root.after(PREFETCH_CLIMA_MS, self.precargar_clima_en_segundo_plano)
        except tk.TclError:
            pass

    @staticmethod
    def formatear_numero(valor):
        if valor is None:
            return "sin dato"
        try:
            numero = float(valor)
            if abs(numero - round(numero)) < 0.05:
                return str(int(round(numero)))
            return f"{numero:.1f}".replace(".", ",")
        except Exception:
            return str(valor)

    @staticmethod
    def descripcion_codigo_clima(codigo):
        mapa = {
            0: "cielo despejado",
            1: "cielo mayormente despejado",
            2: "cielo parcialmente nublado",
            3: "cielo cubierto",
            45: "niebla",
            48: "niebla con escarcha",
            51: "llovizna ligera",
            53: "llovizna moderada",
            55: "llovizna intensa",
            56: "llovizna helada ligera",
            57: "llovizna helada intensa",
            61: "lluvia ligera",
            63: "lluvia moderada",
            65: "lluvia intensa",
            66: "lluvia helada ligera",
            67: "lluvia helada intensa",
            71: "nevada ligera",
            73: "nevada moderada",
            75: "nevada intensa",
            77: "granos de nieve",
            80: "chubascos ligeros",
            81: "chubascos moderados",
            82: "chubascos intensos",
            85: "chubascos de nieve ligeros",
            86: "chubascos de nieve intensos",
            95: "tormenta eléctrica",
            96: "tormenta con granizo ligero",
            99: "tormenta con granizo intenso",
        }
        return mapa.get(codigo, "condiciones meteorológicas variables")

    def consultar_clima_async(self):
        token = self.iniciar_proceso("clima")
        if token is None:
            # Nunca quedarse en silencio: informar al usuario.
            self.responder(
                "todavía estoy terminando la consulta anterior. Espere un momento y vuelva a preguntarme.",
                "pensando",
            )
            return

        self.expresion_pensando()

        def trabajo():
            respuesta = None
            error = None
            try:
                respuesta, error = self.obtener_clima()
            except Exception as exc:
                print("ERROR HILO CLIMA:", exc)
                error = "Tuve un problema al consultar el clima."
            finally:
                self.terminar_proceso(token)

            if token != self.proceso_id:
                return

            if error:
                self.root.after(0, lambda e=error: self.responder(e, "confundida"))
            elif respuesta:
                self.root.after(0, lambda r=respuesta: self.responder(r, "feliz"))
            else:
                self.root.after(
                    0,
                    lambda: self.responder(
                        "no obtuve una respuesta del servicio meteorológico.",
                        "confundida",
                    ),
                )

        threading.Thread(target=trabajo, daemon=True).start()

    def consultar_pronostico_manana_async(self):
        token = self.iniciar_proceso("pronostico_manana")
        if token is None:
            self.responder(
                "todavía estoy terminando la consulta anterior. Espere un momento y vuelva a preguntarme.",
                "pensando",
            )
            return

        self.expresion_pensando()

        def trabajo():
            respuesta = None
            error = None
            try:
                respuesta, error = self.obtener_pronostico_manana()
            except Exception as exc:
                print("ERROR HILO PRONÓSTICO MAÑANA:", exc)
                error = "Tuve un problema al consultar el pronóstico de mañana."
            finally:
                self.terminar_proceso(token)

            if token != self.proceso_id:
                return

            if error:
                self.root.after(0, lambda e=error: self.responder(e, "confundida"))
            elif respuesta:
                self.root.after(0, lambda r=respuesta: self.responder(r, "feliz"))
            else:
                self.root.after(
                    0,
                    lambda: self.responder(
                        "no obtuve el pronóstico de mañana del servicio meteorológico.",
                        "confundida",
                    ),
                )

        threading.Thread(target=trabajo, daemon=True).start()

    # ======================================================
    # UNIDAD DE APRENDIZAJE ADAPTATIVO v2.6.2
    # ======================================================

    def cambiar_aprendizaje_adaptativo(self):
        try: activo = bool(self.var_aprendizaje_adaptativo.get())
        except Exception: activo = True
        self.modo_aprendizaje_adaptativo = activo
        self.memoria.cambiar_estado("modo_aprendizaje_adaptativo", "1" if activo else "0")
        self.responder(
            "activé el aprendizaje adaptativo. Registraré únicamente evidencia real de estudio y evaluación."
            if activo else
            "desactivé el aprendizaje adaptativo. La biblioteca seguirá disponible, pero no actualizaré el progreso académico.",
            "feliz" if activo else "normal",
        )

    def nivel_texto_aprendizaje(self, dominio, evidencias):
        try: evidencias, dominio = int(evidencias or 0), float(dominio or 0)
        except Exception: evidencias, dominio = 0, 0.0
        if evidencias <= 0: return "Sin evaluar"
        if dominio < 45: return "Reforzar"
        if dominio < 65: return "En desarrollo"
        if dominio < 80: return "Buen avance"
        return "Sólido"

    def ventana_progreso_academico(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Unidad de aprendizaje de Beta")
        ventana.geometry("980x520")
        ventana.minsize(820, 420)
        marco = ttk.Frame(ventana, padding=10); marco.pack(fill="both", expand=True)
        ramos = self.biblioteca.listar_ramos()
        progreso = self.memoria.listar_progreso_academico(APRENDIZAJE_MAX_EVENTOS_UI)
        docs_total, frags_total = self.biblioteca.estadisticas()
        ttk.Label(marco, text=(
            f"Biblioteca: {docs_total} documentos, {frags_total} fragmentos. "
            f"Ramos cargados: {len(ramos)}. El dominio solo cambia con evidencia explícita."
        )).pack(anchor="w", pady=(0,8))
        columnas=("ramo","tema","nivel","dominio","evidencias","exposiciones","ultima")
        tabla=ttk.Treeview(marco, columns=columnas, show="headings", height=16)
        titulos={"ramo":"Ramo","tema":"Tema","nivel":"Estado","dominio":"Dominio","evidencias":"Evidencias","exposiciones":"Estudios","ultima":"Última actividad"}
        anchos={"ramo":190,"tema":240,"nivel":110,"dominio":75,"evidencias":75,"exposiciones":70,"ultima":135}
        for c in columnas:
            tabla.heading(c,text=titulos[c]); tabla.column(c,width=anchos[c],anchor="w")
        tabla.pack(fill="both",expand=True)
        for fila in progreso:
            ramo,tema,dominio,evidencias,exposiciones,aciertos,errores,ultima,detalle=fila
            nivel=self.nivel_texto_aprendizaje(dominio,evidencias)
            dominio_txt="—" if int(evidencias or 0)<=0 else f"{float(dominio or 0):.0f}%"
            tabla.insert("","end",values=(ramo,tema,nivel,dominio_txt,int(evidencias or 0),int(exposiciones or 0),ultima or "—"))
        if not progreso:
            tabla.insert("","end",values=("—","Todavía no hay temas evaluados","Sin evaluar","—",0,0,"—"))
        botones=ttk.Frame(marco); botones.pack(fill="x",pady=(8,0))
        def evaluar_seleccionado():
            sel=tabla.selection()
            if sel:
                vals=tabla.item(sel[0],"values")
                if vals and vals[0]!="—":
                    ventana.destroy(); self.generar_pregunta_evaluacion_async(str(vals[0]),str(vals[1])); return
            ventana.destroy(); self.evaluacion_manual()
        ttk.Button(botones,text="Evaluarme sobre seleccionado",command=evaluar_seleccionado).pack(side="left")
        ttk.Button(botones,text="Cerrar",command=ventana.destroy).pack(side="right")

    def inferir_ramo_academico(self, texto=""):
        texto_n=normalizar(texto or "")
        if self.ultimo_contexto_academico:
            ramo=(self.ultimo_contexto_academico.get("ramo_base") or "").strip()
            if ramo and (not texto_n or normalizar(ramo) in texto_n or len(texto_n.split())<=6):
                return ramo
        mejor,mejor_score="",0.0
        for ramo,_docs,_frags,_paginas in self.biblioteca.listar_ramos():
            rn=normalizar(ramo or "")
            if not rn: continue
            score=1.0 if (rn in texto_n or (texto_n and texto_n in rn)) else difflib.SequenceMatcher(None,rn,texto_n).ratio()
            if score>mejor_score: mejor_score,mejor=score,ramo
        return mejor if mejor_score>=0.45 else ""

    def inferir_tema_academico(self, texto="", ramo=""):
        limpio=self.limpiar_consulta_academica(texto or "").strip()
        if not limpio and self.ultimo_contexto_academico:
            limpio=(self.ultimo_contexto_academico.get("tema_base") or "").strip()
        limpio=re.sub(
            r"^(?:hablame|explicame|describe|dime|cuentame|ensename|muestrame|puedes hablarme|puedes explicarme|quiero saber)\\s+(?:mas\\s+)?(?:sobre\\s+|de\\s+)?",
            "", limpio, flags=re.IGNORECASE
        ).strip(" ,.;:-")
        if ramo:
            rn,ln=normalizar(ramo),normalizar(limpio)
            if ln==rn or (rn and rn in ln and len(ln.split())<=len(rn.split())+3): return ramo
        return limpio or ramo or "Tema general"

    def registrar_exposicion_academica(self, ramo, tema, detalle="consulta"):
        if not self.modo_aprendizaje_adaptativo: return
        try:
            self.memoria.registrar_evento_aprendizaje(ramo or "General",tema or ramo or "Tema general","exposicion",None,detalle)
        except Exception as error:
            print("APRENDIZAJE: no se pudo registrar exposición:",error)

    def registrar_autoevaluacion_academica(self, tipo):
        contexto=self.ultimo_contexto_academico or {}
        ramo=(contexto.get("ramo_base") or "").strip(); tema=(contexto.get("tema_base") or contexto.get("consulta") or "").strip()
        if not ramo and not tema:
            self.responder("todavía no tengo un tema académico activo para asociar esa autoevaluación.","normal"); return
        ramo=ramo or "General"; tema=self.inferir_tema_academico(tema,ramo)
        self.memoria.registrar_evento_aprendizaje(ramo,tema,tipo,None,"Autoevaluación explícita del Señor")
        if tipo=="comprendido":
            self.responder("perfecto. Lo registraré como una señal de comprensión, no como dominio definitivo. Más adelante puedo comprobarlo con una pregunta.","feliz",tipo_contexto="academico")
        else:
            self.responder("lo tendré en cuenta. Marqué este tema para reforzarlo; puedo explicarlo de otra forma o evaluarlo más adelante.","normal",tipo_contexto="academico")

    def responder_progreso_academico(self):
        ramos=self.memoria.resumen_progreso_por_ramo()
        if not ramos:
            self.responder("todavía no tengo evidencia suficiente para estimar su progreso. Podemos empezar con una evaluación breve usando sus apuntes.","normal"); return
        partes=[]
        for ramo,exposiciones,evidencias,dominio,ultima in ramos[:4]:
            if int(evidencias or 0)<=0: partes.append(f"en {ramo} hemos estudiado, pero aún no lo he evaluado")
            else: partes.append(f"en {ramo} estimo un {float(dominio or 0):.0f} por ciento de dominio con {int(evidencias)} evidencia(s)")
        self.responder("Señor, "+"; ".join(partes)+". Estos valores son estimaciones de estudio, no calificaciones oficiales.","normal")

    def responder_recomendacion_repaso(self):
        temas=self.memoria.temas_para_repasar(4)
        if not temas:
            self.responder("todavía no tengo suficientes evaluaciones para decir qué debería repasar. Puedo hacerle una pregunta de alguno de sus ramos cargados.","normal"); return
        frases=[f"{tema}, de {ramo}, con un dominio estimado de {float(dominio or 0):.0f} por ciento" for ramo,tema,dominio,evidencias,exposiciones,aciertos,errores,ultima in temas]
        self.responder("Señor, por la evidencia que tengo, priorizaría repasar "+"; ".join(frases)+".","normal")

    def evaluacion_manual(self):
        ramos=self.biblioteca.listar_ramos(); sugeridos=", ".join(r[0] for r in ramos[:8])
        ramo=simpledialog.askstring("Evaluación académica","¿Sobre qué ramo o tema desea que lo evalúe?\\n\\nRamos cargados: "+(sugeridos or "ninguno"),parent=self.root)
        if ramo: self.generar_pregunta_evaluacion_async(ramo.strip(),ramo.strip())

    def cancelar_evaluacion_academica(self, anunciar=False):
        self.evaluacion_academica_pendiente=None; self.evaluacion_academica_hasta=0.0
        if anunciar: self.responder("evaluación finalizada. Podemos retomarla cuando quiera.","normal")

    def generar_pregunta_evaluacion_async(self, ramo="", tema=""):
        if not self.modo_aprendizaje_adaptativo:
            self.responder("el aprendizaje adaptativo está desactivado.","normal"); return
        if self.evaluacion_academica_pendiente:
            self.responder("ya tengo una pregunta de evaluación pendiente. Respóndala o diga Beta, termina evaluación.","normal"); return
        ramo=(ramo or self.inferir_ramo_academico(tema) or "").strip(); tema=(tema or ramo or "").strip()
        if not ramo: self.evaluacion_manual(); return
        token=self.iniciar_proceso("evaluacion_academica")
        if token is None: self.responder("todavía estoy terminando otra consulta.","pensando"); return
        self.expresion_pensando()
        def trabajo():
            pregunta=respuesta_clave=""; tema_real=tema or ramo; fuentes=[]
            try:
                consulta=f"{ramo} {tema}".strip()
                fuentes=self.biblioteca.buscar(consulta,limite=max(EVALUACION_FUENTES,4),ramo_preferido=ramo)
                fuentes=[r for r in fuentes if float(r.get("score",0))>=BIBLIOTECA_UMBRAL_MIN][:EVALUACION_FUENTES]
                if not fuentes:
                    self.root.after(0,lambda:self.responder("no encontré suficiente material local de ese ramo para construir una evaluación confiable.","confundida")); return
                contexto=self.formatear_fuentes_academicas(fuentes,EVALUACION_FUENTES)
                mensajes=[
                    {"role":"system","content":"Eres Beta, tutora académica. Crea UNA pregunta breve usando exclusivamente los apuntes. No inventes. Devuelve solo JSON válido con claves: pregunta, respuesta_clave, tema. Debe poder responderse oralmente en 1 a 4 frases y no revelar la respuesta."},
                    {"role":"user","content":f"Ramo: {ramo}\\nTema solicitado: {tema}\\n\\nAPUNTES:\\n{contexto}"},
                ]
                bruto=self.enviar_ollama(mensajes,temperatura=0.18,num_predict=EVALUACION_TOKENS_PREGUNTA,num_ctx=1200)
                datos=self.extraer_json_de_texto(bruto or "") or {}
                pregunta=str(datos.get("pregunta","")).strip(); respuesta_clave=str(datos.get("respuesta_clave","")).strip(); tema_real=str(datos.get("tema","")).strip() or tema_real
                if not pregunta or not respuesta_clave:
                    pregunta=f"Señor, según sus apuntes de {ramo}, ¿qué concepto principal puede explicar sobre {tema_real}?"; respuesta_clave=fuentes[0].get("texto","")[:700]
            except Exception as error: print("ERROR GENERANDO EVALUACIÓN:",error)
            finally: self.terminar_proceso(token)
            if token!=self.proceso_id: return
            if not pregunta or not respuesta_clave:
                self.root.after(0,lambda:self.responder("no pude preparar la evaluación en este momento.","confundida")); return
            self.evaluacion_academica_pendiente={"ramo":ramo,"tema":tema_real,"pregunta":pregunta,"respuesta_clave":respuesta_clave,"fuentes":fuentes}
            self.evaluacion_academica_hasta=time.time()+EVALUACION_RESPUESTA_SEGUNDOS
            self.ultimo_ramo_evaluacion=ramo; self.ultimo_tema_evaluacion=tema_real
            self.root.after(0,lambda p=pregunta:self.responder(p,"escuchando",tipo_contexto="evaluacion"))
        threading.Thread(target=trabajo,daemon=True).start()

    def _puntuar_respuesta_evaluacion_respaldo(self, respuesta, clave):
        stop={"que","como","para","por","con","una","uno","unos","unas","del","las","los","este","esta","esto","son","ser","se","el","la","de","en","y","o","a","un"}
        a={p for p in normalizar(respuesta).split() if len(p)>=4 and p not in stop}; b={p for p in normalizar(clave).split() if len(p)>=4 and p not in stop}
        if not b: return 50.0
        cobertura=len(a & b)/max(1,min(len(b),12)); return max(15.0,min(90.0,25.0+cobertura*75.0))

    def procesar_respuesta_evaluacion(self, respuesta):
        pendiente=self.evaluacion_academica_pendiente
        if not pendiente: return
        self.evaluacion_academica_pendiente=None; self.evaluacion_academica_hasta=0.0
        respuesta=(respuesta or "").strip()
        if not respuesta: return
        ramo=pendiente.get("ramo","General"); tema=pendiente.get("tema",ramo); clave=pendiente.get("respuesta_clave",""); fuentes=pendiente.get("fuentes",[])
        token=self.iniciar_proceso("correccion_evaluacion")
        if token is None: return
        self.expresion_pensando()
        def trabajo():
            puntuacion=None; feedback=""
            try:
                fuentes_txt=self.formatear_fuentes_academicas(fuentes,EVALUACION_FUENTES)
                mensajes=[
                    {"role":"system","content":"Evalúa la respuesta del estudiante usando exclusivamente la respuesta clave y los apuntes. Sé justo con sinónimos. Devuelve solo JSON válido con puntuacion de 0 a 100 y feedback de máximo 45 palabras. No penalices estilo; evalúa comprensión conceptual."},
                    {"role":"user","content":f"Pregunta: {pendiente.get('pregunta','')}\\nRespuesta del Señor: {respuesta}\\nRespuesta clave: {clave}\\n\\nFuentes:\\n{fuentes_txt}"},
                ]
                bruto=self.enviar_ollama(mensajes,temperatura=0.05,num_predict=EVALUACION_TOKENS_CORRECCION,num_ctx=1300)
                datos=self.extraer_json_de_texto(bruto or "") or {}; puntuacion=max(0.0,min(100.0,float(datos.get("puntuacion")))); feedback=str(datos.get("feedback","")).strip()
            except Exception as error:
                print("EVALUACIÓN: usando corrección de respaldo:",error); puntuacion=self._puntuar_respuesta_evaluacion_respaldo(respuesta,clave); feedback="Comparé su respuesta con los conceptos principales de los apuntes."
            finally: self.terminar_proceso(token)
            self.memoria.registrar_evento_aprendizaje(ramo,tema,"evaluacion",puntuacion,f"Respuesta: {respuesta[:400]} | {feedback[:400]}")
            prog=self.memoria.obtener_progreso_tema(ramo,tema); nivel=self.nivel_texto_aprendizaje(prog[2] if prog else puntuacion, prog[3] if prog else 1)
            mensaje=f"Señor, su respuesta obtuvo aproximadamente {puntuacion:.0f} de 100. {feedback} Su estado estimado en este tema queda como {nivel}."
            self.root.after(0,lambda m=mensaje:self.responder(m,"feliz" if puntuacion>=70 else "normal",tipo_contexto="evaluacion"))
        threading.Thread(target=trabajo,daemon=True).start()

    def preferencias_aprendidas_para_prompt(self):
        try: recuerdos=self.memoria.recuerdos_por_fuente("curiosidad_usuario",limite=10)
        except Exception: return ""
        utiles=[]; claves=("prefiere","le gusta","aprende mejor","ejemplo","practico","práctico","teoria","teoría","explicacion","explicación","detall","breve")
        for r in recuerdos:
            contenido=str(r[1] or "").strip(); n=normalizar(contenido)
            if contenido and any(k in n for k in claves): utiles.append(contenido)
            if len(utiles)>=2: break
        return " | ".join(utiles)

    # ======================================================
    # OLLAMA / QWEN3 LOCAL
    # ======================================================


    def informacion_ollama(self):
        messagebox.showinfo(
            "IA local de Beta",
            f"Modelo: {OLLAMA_MODEL}\n"
            f"Dirección local: {OLLAMA_URL}\n\n"
            "Las conversaciones con la IA se procesan en este computador.\n"
            "Internet externo se usa únicamente para el clima.",
            parent=self.root,
        )

    def probar_ollama(self):
        token = self.iniciar_proceso("prueba_ollama")
        if token is None:
            messagebox.showinfo(
                "Beta",
                "Todavía estoy terminando otra consulta.",
                parent=self.root,
            )
            return

        self.expresion_pensando()

        def trabajo():
            mensajes = [
                {
                    "role": "system",
                    "content": (
                        "Responde únicamente en español. No muestres razonamiento. "
                        "Tu nombre es Beta."
                    ),
                },
                {
                    "role": "user",
                    "content": "Responde exactamente: conexión correcta.",
                },
            ]

            try:
                respuesta = self.enviar_ollama(mensajes)
            finally:
                self.terminar_proceso(token)

            if token != self.proceso_id:
                return

            if respuesta:
                respuesta = self.limpiar_respuesta_ollama(respuesta)
                self.root.after(
                    0,
                    lambda: messagebox.showinfo(
                        "Ollama",
                        f"Conexión correcta con {OLLAMA_MODEL}.\n\nRespuesta: {respuesta}",
                        parent=self.root,
                    ),
                )
                self.root.after(0, self.expresion_feliz)
            else:
                self.root.after(
                    0,
                    lambda: messagebox.showerror(
                        "Ollama",
                        "No pude comunicarme con Ollama.\n\n"
                        "Compruebe que Ollama esté iniciado y que qwen3:4b-instruct esté instalado.",
                        parent=self.root,
                    ),
                )
                self.root.after(0, self.expresion_confundida)

        threading.Thread(target=trabajo, daemon=True).start()

    def construir_prompt_sistema(self, pregunta):
        """Prompt compacto con memoria relevante y continuidad conversacional."""
        recuerdos = self.memoria.buscar_recuerdos(pregunta, limite=4)
        if recuerdos:
            recuerdos_texto = "\n".join(f"- {r[1]}" for r in recuerdos)
        else:
            recuerdos_texto = "- Sin recuerdos relevantes."

        perfil = self.memoria.obtener_perfil()
        familiaridad = perfil.get("familiaridad", 25)
        preferencias_aprendidas = self.preferencias_aprendidas_para_prompt()

        # Contexto de sesión: se usa solo mientras siga relativamente fresco.
        contexto_tema = ""
        contexto_resumen = ""
        if (
            self.contexto_actualizado_ts
            and time.time() - self.contexto_actualizado_ts <= CONTEXTO_CONVERSACION_SEGUNDOS
        ):
            contexto_tema = self.contexto_tema
            contexto_resumen = self.contexto_resumen
        else:
            # Al iniciar Beta podemos recuperar el último resumen persistente.
            ultimo_resumen = self.memoria.ultimo_resumen_conversacion()
            if ultimo_resumen:
                contexto_resumen = ultimo_resumen[1]
                contexto_tema = ultimo_resumen[2] or ""

        seguimiento = ""
        if self.debe_hacer_pregunta_seguimiento(pregunta):
            seguimiento = (
                "El Señor acaba de compartir algo personal o relacionado con un aprendizaje/proyecto. "
                "Después de responder, termina con UNA pregunta breve y natural que ayude a continuar "
                "la conversación. No interrogues ni hagas varias preguntas."
            )

        return f"""
Eres Beta, la asistente personal del Señor.
Responde SIEMPRE en español, de forma natural, cálida y breve.
Llama al usuario "Señor". No digas que eres Qwen u Ollama.
No muestres razonamiento interno. No inventes recuerdos ni acciones realizadas.
Si una memoria contradice lo que el Señor acaba de decir, da prioridad a la información nueva.
Normalmente responde en 1 a 3 frases.
Familiaridad actual: {familiaridad}/100.
Preferencias de interacción aprendidas: {preferencias_aprendidas or 'sin preferencias de estilo confirmadas'}.
Si una preferencia de estilo es relevante, adáptate discretamente sin decir que estás leyendo una base de datos.

Tema de conversación actual: {contexto_tema or 'sin tema definido'}
Resumen/contexto reciente: {contexto_resumen or 'sin resumen reciente'}

Recuerdos relevantes:
{recuerdos_texto}

{seguimiento}
""".strip()

    def preparar_historial_ollama(self, pregunta):
        """Prepara hasta tres turnos recientes para mantener continuidad natural."""
        # Preferimos el contexto de la sesión actual porque no contiene ruido de
        # conversaciones de días anteriores ni comandos antiguos.
        historial = list(self.contexto_turnos[-8:])
        if not historial:
            historial_db = self.memoria.historial_reciente(10)
            historial = [(autor, mensaje) for autor, mensaje, _fecha in historial_db]

        # El mensaje actual ya se enviará después como user; evitar duplicarlo.
        if historial:
            autor_ultimo, mensaje_ultimo = historial[-1]
            if (
                normalizar(autor_ultimo) in {"jefe", "senor"}
                and normalizar(mensaje_ultimo) == normalizar(pregunta)
            ):
                historial = historial[:-1]

        mensajes = []
        for autor, mensaje in historial[-6:]:
            if normalizar(autor) in {"jefe", "senor"}:
                mensajes.append({"role": "user", "content": mensaje})
                continue

            if self.respuesta_tiene_demasiado_ingles(mensaje):
                print("HISTORIAL OMITIDO POR IDIOMA:", mensaje[:120])
                continue
            mensajes.append({"role": "assistant", "content": mensaje})

        return mensajes

    def consultar_ollama(self, pregunta):
        """
        Genera la respuesta de Beta con tres barreras:
        1) prompt estricto en español,
        2) corrección automática si aparece inglés,
        3) regeneración sin historial si la corrección falla.
        """
        sistema = self.construir_prompt_sistema(pregunta)

        mensajes = [
            {
                "role": "system",
                "content": sistema,
            }
        ]

        mensajes.extend(self.preparar_historial_ollama(pregunta))

        mensajes.append(
            {
                "role": "user",
                "content": (
                    pregunta
                    + "\n\nResponde solo con la respuesta final en español."
                ),
            }
        )

        inicio_ollama = time.perf_counter()
        respuesta = self.enviar_ollama(
            mensajes,
            temperatura=0.22,
            num_predict=OLLAMA_NUM_PREDICT,
        )
        print(f"LATENCIA OLLAMA: {time.perf_counter() - inicio_ollama:.2f} s")

        if not respuesta:
            return None

        respuesta = self.limpiar_respuesta_ollama(respuesta)

        print("OLLAMA RESPUESTA ORIGINAL:", respuesta)

        # Primera barrera: corregir el texto ya generado.
        if self.respuesta_tiene_demasiado_ingles(respuesta):
            print("Beta detectó inglés. Intentando convertir la respuesta al español...")
            corregida = self.corregir_a_espanol(respuesta)

            if corregida and not self.respuesta_tiene_demasiado_ingles(corregida):
                respuesta = corregida
            else:
                # Segunda barrera: no reutilizar el texto contaminado ni el historial.
                print("La corrección no fue suficiente. Regenerando en español sin historial...")
                regenerada = self.regenerar_espanol_sin_historial(pregunta)

                if regenerada and not self.respuesta_tiene_demasiado_ingles(regenerada):
                    respuesta = regenerada
                else:
                    # Última barrera: Beta nunca pronuncia una respuesta claramente inglesa.
                    return (
                        "Señor, tuve un problema generando la respuesta completamente en español. "
                        "Intente formularme la pregunta nuevamente."
                    )

        return respuesta.strip()

    # ======================================================
    # BIBLIOTECA ACADÉMICA LOCAL
    # ======================================================

    def preparar_biblioteca_en_segundo_plano(self):
        if not self.biblioteca.tiene_contenido():
            return

        def trabajo():
            inicio = time.perf_counter()
            try:
                cantidad = self.biblioteca.cargar_indice_memoria()
                docs_a, frags_a = self.biblioteca.estadisticas_categoria("academica")
                docs_t, frags_t = self.biblioteca.estadisticas_categoria("tecnica")
                print(
                    f"BIBLIOTECA DE BETA LISTA: {cantidad} fragmentos en "
                    f"{time.perf_counter() - inicio:.2f} s | "
                    f"académica={frags_a} | técnica={frags_t}"
                )

                # El índice ya está disponible. El modelo semántico se precalienta
                # después, en el mismo hilo, sin impedir que Beta escuche.
                inicio_modelo = time.perf_counter()
                try:
                    self.biblioteca.cargar_modelo()
                    print(
                        f"MODELO SEMÁNTICO PRECALENTADO en "
                        f"{time.perf_counter() - inicio_modelo:.2f} s"
                    )
                except Exception as error_modelo:
                    print("MODELO SEMÁNTICO: precarga no disponible:", error_modelo)
            except Exception as error:
                print("BIBLIOTECA DE BETA: no se pudo precargar:", error)

        threading.Thread(target=trabajo, daemon=True).start()

    def agregar_pdfs_biblioteca(self):
        rutas = filedialog.askopenfilenames(
            parent=self.root,
            title="Seleccione los PDF que Beta estudiará",
            filetypes=[("Documentos PDF", "*.pdf")],
        )
        if not rutas:
            return

        ramo = simpledialog.askstring(
            "Biblioteca académica",
            "¿A qué ramo pertenecen estos documentos?\n"
            "Ejemplo: Seguridad de redes y periféricos",
            parent=self.root,
        )
        if ramo is None:
            return
        ramo = ramo.strip() or "General"

        modulo = simpledialog.askstring(
            "Biblioteca académica",
            "Módulo / unidad (opcional):\nEjemplo: Módulo 2",
            parent=self.root,
        )
        if modulo is None:
            modulo = ""
        modulo = modulo.strip()

        reemplazos_por_ruta = {}
        rutas_filtradas = []
        for ruta in rutas:
            anteriores = self.biblioteca.buscar_versiones_mismo_nombre(
                ruta, categoria="academica", ramo=ramo
            )
            if anteriores:
                try:
                    sha_nuevo = self.biblioteca.hash_archivo(ruta)
                except Exception:
                    sha_nuevo = ""
                distintos = [a for a in anteriores if a.get("sha256") != sha_nuevo]
                if distintos:
                    decision = messagebox.askyesnocancel(
                        "Posible actualización de PDF",
                        f"Ya existe una versión activa de '{Path(ruta).name}' en {ramo}.\n\n"
                        "Sí: incorporar la nueva y desactivar la anterior.\n"
                        "No: conservar ambas versiones.\n"
                        "Cancelar: omitir este archivo.",
                        parent=self.root,
                    )
                    if decision is None:
                        continue
                    if decision:
                        reemplazos_por_ruta[str(ruta)] = [a["id"] for a in distintos]
            rutas_filtradas.append(ruta)
        rutas = tuple(rutas_filtradas)
        if not rutas:
            return

        self.responder(
            f"recibí {len(rutas)} documento(s) de {ramo}. "
            "Voy a incorporarlos a mi biblioteca académica en segundo plano.",
            "feliz",
        )

        def progreso(mensaje):
            print("BIBLIOTECA:", mensaje)

        def trabajo():
            resultados = []
            errores = []
            inicio = time.perf_counter()

            for ruta in rutas:
                try:
                    resultado = self.biblioteca.importar_pdf(
                        ruta,
                        ramo=ramo,
                        modulo=modulo,
                        progreso=progreso,
                        reemplazar_documentos_ids=reemplazos_por_ruta.get(str(ruta), []),
                    )
                    resultados.append(resultado)
                    print("BIBLIOTECA:", resultado.get("mensaje", ""))
                except Exception as error:
                    print("ERROR IMPORTANDO PDF:", ruta, error)
                    errores.append(f"{Path(ruta).name}: {error}")

            ok = [r for r in resultados if r.get("estado") in {"ok", "reactivado"}]
            duplicados = [r for r in resultados if r.get("estado") == "duplicado"]
            sin_texto = [r for r in resultados if r.get("estado") == "sin_texto"]
            ocr_requeridos = [r for r in resultados if r.get("estado") == "ocr_requerido"]

            mensaje_partes = []
            if ok:
                total_frag = sum(int(r.get("fragmentos", 0)) for r in ok)
                mensaje_partes.append(
                    f"incorporé {len(ok)} documento(s) y {total_frag} fragmentos de conocimiento"
                )
            if duplicados:
                mensaje_partes.append(f"{len(duplicados)} ya estaban registrados")
            if sin_texto:
                mensaje_partes.append(
                    f"{len(sin_texto)} PDF no produjo texto utilizable ni con OCR"
                )
            if ocr_requeridos:
                mensaje_partes.append(
                    f"{len(ocr_requeridos)} PDF requiere instalar o configurar Tesseract OCR"
                )
            if errores:
                mensaje_partes.append(f"{len(errores)} presentó errores")

            mensaje = "; ".join(mensaje_partes) or "no pude incorporar documentos"
            print(
                f"BIBLIOTECA ACADÉMICA: proceso terminado en "
                f"{time.perf_counter() - inicio:.2f} s"
            )

            def finalizar():
                if ok:
                    mensaje_final = mensaje + ". Ya puede consultarme sobre ese material."
                else:
                    mensaje_final = (
                        mensaje
                        + ". Esos documentos no fueron incorporados todavía; "
                        "corrija el problema indicado y vuelva a agregarlos."
                    )
                self.responder(
                    mensaje_final,
                    "feliz" if ok else "confundida",
                )
                avisos = list(errores)
                avisos.extend(r.get("mensaje", "") for r in ocr_requeridos)
                avisos.extend(r.get("mensaje", "") for r in sin_texto)
                avisos = [a for a in avisos if a]
                if avisos:
                    messagebox.showwarning(
                        "Biblioteca académica",
                        "Algunos documentos necesitan atención:\n\n"
                        + "\n\n".join(avisos[:8]),
                        parent=self.root,
                    )

            self.root.after(0, finalizar)

        threading.Thread(target=trabajo, daemon=True).start()

    def ventana_biblioteca_documentos(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Biblioteca académica de Beta")
        ventana.geometry("1000x520")
        ventana.attributes("-topmost", True)

        docs, frags = self.biblioteca.estadisticas()
        encabezado = ttk.Label(
            ventana,
            text=f"Documentos activos: {docs}    Fragmentos de conocimiento: {frags}",
        )
        encabezado.pack(anchor="w", padx=12, pady=(12, 6))

        tabla = ttk.Treeview(
            ventana,
            columns=("id", "ramo", "modulo", "nombre", "paginas", "fragmentos", "fecha"),
            show="headings",
        )
        for clave, titulo in [
            ("id", "ID"),
            ("ramo", "Ramo"),
            ("modulo", "Módulo"),
            ("nombre", "Documento"),
            ("paginas", "Páginas"),
            ("fragmentos", "Fragmentos"),
            ("fecha", "Agregado"),
        ]:
            tabla.heading(clave, text=titulo)

        tabla.column("id", width=45, anchor="center")
        tabla.column("ramo", width=200)
        tabla.column("modulo", width=120)
        tabla.column("nombre", width=300)
        tabla.column("paginas", width=70, anchor="center")
        tabla.column("fragmentos", width=90, anchor="center")
        tabla.column("fecha", width=150)
        tabla.pack(fill="both", expand=True, padx=12, pady=(0, 10))

        rutas_por_id = {}

        def recargar():
            for item in tabla.get_children():
                tabla.delete(item)
            rutas_por_id.clear()
            for fila in self.biblioteca.listar_documentos():
                doc_id, nombre, ruta, ramo, modulo, paginas, fragmentos, fecha = fila
                rutas_por_id[str(doc_id)] = ruta
                tabla.insert(
                    "",
                    "end",
                    iid=str(doc_id),
                    values=(doc_id, ramo, modulo, nombre, paginas, fragmentos, fecha),
                )
            d, f = self.biblioteca.estadisticas()
            encabezado.config(
                text=f"Documentos activos: {d}    Fragmentos de conocimiento: {f}"
            )

        def abrir():
            seleccion = tabla.selection()
            if not seleccion:
                return
            ruta = rutas_por_id.get(seleccion[0], "")
            if ruta and Path(ruta).exists():
                try:
                    os.startfile(ruta)
                except Exception as error:
                    messagebox.showerror(
                        "Biblioteca académica",
                        f"No pude abrir el PDF:\n{error}",
                        parent=ventana,
                    )

        def eliminar():
            seleccion = tabla.selection()
            if not seleccion:
                return
            valores = tabla.item(seleccion[0]).get("values", [])
            nombre = valores[3] if len(valores) > 3 else "este documento"
            if not messagebox.askyesno(
                "Biblioteca académica",
                f"¿Quitar '{nombre}' del conocimiento activo de Beta?\n\n"
                "El PDF copiado no se elimina del disco; solo deja de usarse en las respuestas.",
                parent=ventana,
            ):
                return
            self.biblioteca.eliminar_documento(int(seleccion[0]))
            recargar()

        botones = ttk.Frame(ventana)
        botones.pack(fill="x", padx=12, pady=(0, 12))
        ttk.Button(botones, text="Abrir PDF", command=abrir).pack(side="left", padx=(0, 8))
        ttk.Button(botones, text="Quitar de la biblioteca", command=eliminar).pack(side="left")
        ttk.Button(botones, text="Agregar PDFs...", command=self.agregar_pdfs_biblioteca).pack(
            side="right"
        )

        tabla.bind("<Double-1>", lambda _e: abrir())
        recargar()

    def comprobar_ocr_biblioteca(self):
        correcto, detalle = self.biblioteca.comprobar_ocr()
        if correcto:
            messagebox.showinfo(
                "OCR de la biblioteca",
                detalle + "\n\nBeta puede leer PDF escaneados localmente.",
                parent=self.root,
            )
        else:
            messagebox.showwarning(
                "OCR de la biblioteca",
                detalle
                + "\n\nPara habilitar OCR:\n"
                + "1. Instale Tesseract OCR para Windows.\n"
                + "2. Instale: python -m pip install -U pytesseract pillow\n"
                + "3. Asegúrese de incluir el idioma español (spa).",
                parent=self.root,
            )

    def buscar_biblioteca_manual(self):
        consulta = simpledialog.askstring(
            "Buscar en mis apuntes",
            "¿Qué desea consultar en la biblioteca académica?",
            parent=self.root,
        )
        if consulta and consulta.strip():
            self.consultar_biblioteca_async(
                consulta.strip(),
                forzar=True,
                forzar_solo_local=False,
            )

    def agregar_pdfs_biblioteca_tecnica(self):
        rutas = filedialog.askopenfilenames(
            parent=self.root,
            title="Seleccione libros o PDF técnicos que Beta estudiará",
            filetypes=[("Documentos PDF", "*.pdf")],
        )
        if not rutas:
            return

        coleccion = simpledialog.askstring(
            "Biblioteca técnica",
            "¿A qué tecnología o colección pertenecen?\n"
            "Ejemplo: Python",
            initialvalue="Python",
            parent=self.root,
        )
        if coleccion is None:
            return
        coleccion = coleccion.strip() or "General"

        reemplazos_por_ruta = {}
        rutas_filtradas = []
        for ruta in rutas:
            anteriores = self.biblioteca.buscar_versiones_mismo_nombre(
                ruta, categoria="tecnica", coleccion=coleccion
            )
            if anteriores:
                try:
                    sha_nuevo = self.biblioteca.hash_archivo(ruta)
                except Exception:
                    sha_nuevo = ""
                distintos = [a for a in anteriores if a.get("sha256") != sha_nuevo]
                if distintos:
                    decision = messagebox.askyesnocancel(
                        "Posible actualización de libro",
                        f"Ya existe una versión activa de '{Path(ruta).name}' en {coleccion}.\n\n"
                        "Sí: incorporar la nueva y desactivar la anterior.\n"
                        "No: conservar ambas versiones.\n"
                        "Cancelar: omitir este archivo.",
                        parent=self.root,
                    )
                    if decision is None:
                        continue
                    if decision:
                        reemplazos_por_ruta[str(ruta)] = [a["id"] for a in distintos]
            rutas_filtradas.append(ruta)
        rutas = tuple(rutas_filtradas)
        if not rutas:
            return

        self.responder(
            f"recibí {len(rutas)} documento(s) técnicos de {coleccion}. "
            "Los estudiaré localmente en segundo plano.",
            "feliz",
        )

        def progreso(mensaje):
            print("BIBLIOTECA TÉCNICA:", mensaje)

        def trabajo():
            resultados = []
            errores = []
            inicio = time.perf_counter()
            for ruta in rutas:
                try:
                    resultado = self.biblioteca.importar_pdf(
                        ruta,
                        ramo="",
                        modulo="",
                        progreso=progreso,
                        categoria="tecnica",
                        coleccion=coleccion,
                        reemplazar_documentos_ids=reemplazos_por_ruta.get(str(ruta), []),
                    )
                    resultados.append(resultado)
                    print("BIBLIOTECA TÉCNICA:", resultado.get("mensaje", ""))
                except Exception as error:
                    errores.append(f"{Path(ruta).name}: {error}")
                    print("ERROR IMPORTANDO LIBRO TÉCNICO:", ruta, error)

            ok = [r for r in resultados if r.get("estado") in {"ok", "reactivado"}]
            duplicados = [r for r in resultados if r.get("estado") == "duplicado"]
            sin_texto = [r for r in resultados if r.get("estado") == "sin_texto"]
            ocr_req = [r for r in resultados if r.get("estado") == "ocr_requerido"]

            print(
                f"BIBLIOTECA TÉCNICA: proceso terminado en "
                f"{time.perf_counter() - inicio:.2f} s"
            )

            partes = []
            if ok:
                paginas = sum(int(r.get("paginas", 0) or 0) for r in ok)
                fragmentos = sum(int(r.get("fragmentos", 0) or 0) for r in ok)
                partes.append(
                    f"incorporé {len(ok)} documento(s), {paginas} páginas y "
                    f"{fragmentos} fragmentos de conocimiento técnico"
                )
            if duplicados:
                partes.append(f"{len(duplicados)} ya estaba en la biblioteca")
            if sin_texto:
                partes.append(f"{len(sin_texto)} no produjo texto utilizable")
            if ocr_req:
                partes.append(f"{len(ocr_req)} necesita revisar OCR")
            if errores:
                partes.append(f"{len(errores)} produjo un error")

            mensaje = ". ".join(partes) + "." if partes else "no pude incorporar esos documentos."
            self.root.after(
                0,
                lambda m=mensaje: self.responder(m, "feliz" if ok else "confundida"),
            )

        threading.Thread(target=trabajo, daemon=True).start()

    def ventana_biblioteca_tecnica(self):
        docs = self.biblioteca.listar_documentos_categoria("tecnica")
        ventana = tk.Toplevel(self.root)
        ventana.title("Biblioteca técnica de Beta")
        ventana.geometry("1050x540")
        ventana.attributes("-topmost", True)

        ttk.Label(
            ventana,
            text=(
                "Libros y manuales técnicos. Beta los usa como referencia interna "
                "y normalmente no menciona PDF ni página al explicarle un tema."
            ),
            wraplength=990,
        ).pack(anchor="w", padx=12, pady=(12, 8))

        tabla = ttk.Treeview(
            ventana,
            columns=("id", "coleccion", "documento", "paginas", "fragmentos", "fecha", "ruta"),
            show="headings",
        )
        for clave, titulo in [
            ("id", "ID"), ("coleccion", "Colección"), ("documento", "Documento"),
            ("paginas", "Páginas"), ("fragmentos", "Fragmentos"),
            ("fecha", "Agregado"), ("ruta", "Ruta"),
        ]:
            tabla.heading(clave, text=titulo)

        tabla.column("id", width=45, anchor="center")
        tabla.column("coleccion", width=130)
        tabla.column("documento", width=300)
        tabla.column("paginas", width=70, anchor="center")
        tabla.column("fragmentos", width=85, anchor="center")
        tabla.column("fecha", width=145)
        tabla.column("ruta", width=260)
        tabla.pack(fill="both", expand=True, padx=12, pady=(0, 8))

        for fila in docs:
            doc_id, nombre, ruta, ramo, modulo, paginas, fragmentos, fecha, categoria, coleccion = fila
            tabla.insert(
                "", "end",
                values=(doc_id, coleccion or "General", nombre, paginas, fragmentos, fecha, ruta),
            )

        def abrir_seleccion(_event=None):
            seleccion = tabla.selection()
            if not seleccion:
                return
            ruta = str(tabla.item(seleccion[0])["values"][6])
            try:
                os.startfile(ruta)
            except Exception as error:
                messagebox.showerror("Biblioteca técnica", str(error), parent=ventana)

        tabla.bind("<Double-1>", abrir_seleccion)
        ttk.Button(ventana, text="Abrir PDF", command=abrir_seleccion).pack(side="left", padx=12, pady=(0, 12))

    def buscar_biblioteca_tecnica_manual(self):
        consulta = simpledialog.askstring(
            "Biblioteca técnica",
            "¿Qué quiere que Beta le explique usando sus libros técnicos?",
            parent=self.root,
        )
        if consulta and consulta.strip():
            self.consultar_biblioteca_tecnica_async(consulta.strip(), forzar=True)

    def ventana_estado_indice_conocimiento(self):
        docs_a, frags_a = self.biblioteca.estadisticas_categoria("academica")
        docs_t, frags_t = self.biblioteca.estadisticas_categoria("tecnica")
        existe_cache = (
            INDICE_MATRIZ_ARCHIVO.exists()
            and INDICE_META_ARCHIVO.exists()
            and INDICE_FIRMA_ARCHIVO.exists()
        )

        respuesta = messagebox.askyesno(
            "Índice de conocimiento de Beta",
            (
                f"Biblioteca académica: {docs_a} documentos / {frags_a} fragmentos\n"
                f"Biblioteca técnica: {docs_t} documentos / {frags_t} fragmentos\n\n"
                f"Índice persistente en SSD: {'Sí' if existe_cache else 'No'}\n\n"
                "¿Desea reconstruir ahora el índice persistente?"
            ),
            parent=self.root,
        )
        if not respuesta:
            return

        def trabajo():
            inicio = time.perf_counter()
            try:
                cantidad = self.biblioteca.cargar_indice_memoria(forzar=True)
                texto = (
                    f"índice reconstruido correctamente con {cantidad} fragmentos "
                    f"en {time.perf_counter() - inicio:.2f} segundos."
                )
                self.root.after(0, lambda: self.responder(texto, "feliz"))
            except Exception as error:
                self.root.after(
                    0,
                    lambda e=str(error): self.responder(
                        f"no pude reconstruir el índice: {e}", "confundida"
                    ),
                )
        threading.Thread(target=trabajo, daemon=True).start()

    def configurar_biblioteca_academica(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Configurar biblioteca académica")
        ventana.geometry("560x330")
        ventana.attributes("-topmost", True)

        ttk.Label(
            ventana,
            text="¿Cómo debe usar Beta Internet al responder temas académicos?",
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w", padx=18, pady=(18, 12))

        variable = tk.StringVar(value=self.modo_biblioteca_academica)

        opciones = [
            (
                "solo_local",
                "Solo mis apuntes",
                "Beta responde únicamente con los PDF de su biblioteca.",
            ),
            (
                "si_falta",
                "Mis apuntes primero; Internet si falta información",
                "Es el modo recomendado. Los apuntes institucionales tienen prioridad.",
            ),
            (
                "siempre",
                "Apuntes + Internet siempre",
                "Beta complementa cada consulta académica con resultados actuales de Internet.",
            ),
        ]

        for valor, titulo, descripcion in opciones:
            marco = ttk.Frame(ventana)
            marco.pack(fill="x", padx=18, pady=5)
            ttk.Radiobutton(
                marco,
                text=titulo,
                variable=variable,
                value=valor,
            ).pack(anchor="w")
            ttk.Label(
                marco,
                text=descripcion,
                foreground="#555555",
                wraplength=500,
            ).pack(anchor="w", padx=(24, 0))

        def guardar():
            valor = variable.get()
            self.modo_biblioteca_academica = valor
            self.memoria.cambiar_estado("modo_biblioteca_academica", valor)
            ventana.destroy()
            messagebox.showinfo(
                "Biblioteca académica",
                "Configuración guardada.",
                parent=self.root,
            )

        ttk.Button(ventana, text="Guardar", command=guardar).pack(pady=16)

    def _contexto_python_activo(self):
        """Indica si la conversación reciente está claramente dentro de Python.

        Se usa únicamente para corregir errores fonéticos muy probables de ASR. No
        convierte dictado general en código si no existe señal suficiente.
        """
        try:
            contexto = self.ultimo_contexto_tecnico or {}
            if time.time() - float(self.ultimo_contexto_tecnico_ts or 0) > TECNICA_CONTEXTO_SEGUNDOS:
                return False
            colecciones = [
                normalizar(x) for x in (contexto.get("colecciones") or []) if normalizar(x)
            ]
            coleccion = normalizar(contexto.get("coleccion") or "")
            tema = normalizar(contexto.get("tema_base") or contexto.get("consulta") or "")
            return (
                "python" in coleccion
                or "python" in colecciones
                or "python" in tema
            )
        except Exception:
            return False

    def corregir_terminos_tecnicos_asr(self, texto, forzar_python=False):
        """Normaliza términos técnicos que Whisper suele escribir fonéticamente.

        La corrección es deliberadamente conservadora: las variantes ambiguas solo
        se sustituyen si la frase ya habla de Python/programación o si la conversación
        técnica activa pertenece a la colección Python.
        """
        original = (texto or "").strip()
        if not original:
            return original

        norm = normalizar(original)
        contexto_python = bool(
            forzar_python
            or self._contexto_python_activo()
            or "python" in norm
            or any(x in set(norm.split()) for x in {
                "programacion", "codigo", "funcion", "funciones", "variable", "variables",
                "string", "strings", "lista", "listas", "tupla", "diccionario", "clase",
                "metodo", "modulo", "excepcion", "repl", "pip", "pylint", "pep8",
            })
        )

        cambios = []
        corregido = original

        # Variantes bastante específicas que pueden corregirse cuando el contexto es Python.
        if contexto_python:
            reglas = [
                (r"\b(?:retur|returr|retun|riturn|ritern|returne)\b", "return"),
                (r"\b(?:kiuargs|kewargs|kwarcs|cuargs|kwars)\b", "kwargs"),
                (r"\b(?:exargs|x args|equis args)\b", "xargs"),
                (r"\b(?:el if|elifff|eliff)\b", "elif"),
                (r"\b(?:deff|defe)\b", "def"),
                (r"\b(?:lamda|lamb da)\b", "lambda"),
                (r"\b(?:pai ton|paiton|peiton|pyton)\b", "Python"),
                (r"\b(?:pi lint|pylin)\b", "Pylint"),
                (r"\b(?:pep ocho|pep 8)\b", "PEP8"),
            ]
            for patron, destino in reglas:
                nuevo, cantidad = re.subn(patron, destino, corregido, flags=re.IGNORECASE)
                if cantidad:
                    cambios.append(f"{patron}->{destino}")
                    corregido = nuevo

        # Términos no ambiguos de otras colecciones técnicas.
        reglas_generales = [
            (r"\bdocker compose\b", "Docker Compose"),
            (r"\bkuber netes\b", "Kubernetes"),
        ]
        for patron, destino in reglas_generales:
            nuevo, cantidad = re.subn(patron, destino, corregido, flags=re.IGNORECASE)
            if cantidad:
                cambios.append(f"{patron}->{destino}")
                corregido = nuevo

        corregido = re.sub(r"\s+", " ", corregido).strip()
        if cambios and normalizar(corregido) != normalizar(original):
            print(f"DICTADO TÉCNICO: interpretando '{original}' como '{corregido}'")
        return corregido

    def limpiar_consulta_tecnica(self, pregunta):
        texto = (pregunta or "").strip()
        texto = re.sub(
            r"^\s*(?:beta|veta|meta|metas|petra)[,\s:;-]*",
            "",
            texto,
            flags=re.IGNORECASE,
        )
        patrones = [
            r"^\s*segun\s+mi\s+libro(?:\s+de\s+python)?[,\s]+",
            r"^\s*segun\s+el\s+libro(?:\s+de\s+python)?[,\s]+",
            r"^\s*busca\s+en\s+mi\s+libro(?:\s+de\s+python)?\s+",
            r"^\s*busca\s+en\s+la\s+biblioteca\s+tecnica\s+",
            r"^\s*usando\s+mi\s+libro(?:\s+de\s+python)?[,\s]+",
        ]
        for patron in patrones:
            nuevo = re.sub(patron, "", texto, flags=re.IGNORECASE)
            if nuevo != texto:
                texto = nuevo.strip()
                break
        texto = texto.strip(" ,.;:-") or pregunta
        return self.corregir_terminos_tecnicos_asr(texto)

    def inferir_colecciones_tecnicas(self, pregunta, maximo=None):
        """Elige una o dos colecciones técnicas usando nombre + similitud semántica."""
        maximo = maximo or BIBLIOTECA_ROUTER_MAX_COLECCIONES
        texto = normalizar(pregunta)
        colecciones = self.biblioteca.listar_colecciones_tecnicas()
        nombres = [str(f[0] or "") for f in colecciones]
        if not nombres:
            return []

        # Una colección mencionada explícitamente siempre tiene prioridad.
        explicitas = []
        for nombre in nombres:
            n = normalizar(nombre)
            if n and (n in texto or (len(n.split()) == 1 and n in texto.split())):
                explicitas.append(nombre)
        if explicitas:
            return explicitas[:maximo]

        # Pistas de Python conservadas por compatibilidad con la primera colección.
        if any(x in texto for x in [
            "python", "pip", "pylint", "pep8", "repl", "pycharm", "vscode",
            "string", "strings", "lista", "listas", "tupla", "tuplas",
            "diccionario", "diccionarios", "kwargs", "xargs", "lambda",
        ]):
            for nombre in nombres:
                if "python" in normalizar(nombre):
                    return [nombre]

        if len(nombres) == 1:
            return [nombres[0]]

        # Cuando hay varias colecciones, dejamos que el índice semántico decida.
        try:
            resultados = self.biblioteca.buscar(
                pregunta, limite=max(8, BIBLIOTECA_ROUTER_RESULTADOS),
                categoria_preferida="tecnica"
            )
            mejores = {}
            for r in resultados:
                col = (r.get("coleccion") or "General").strip() or "General"
                score = float(r.get("score", 0) or 0)
                mejores[col] = max(mejores.get(col, 0.0), score)
            orden = sorted(mejores.items(), key=lambda x: x[1], reverse=True)
            if orden and orden[0][1] >= BIBLIOTECA_ROUTER_UMBRAL_MIN:
                top = orden[0][1]
                elegidas = [
                    nombre for nombre, score in orden
                    if score >= BIBLIOTECA_ROUTER_UMBRAL_MIN
                    and (top - score) <= BIBLIOTECA_ROUTER_MARGEN_COLECCION
                ]
                return elegidas[:maximo]
        except Exception as error:
            print("ROUTER TÉCNICO: no pude inferir colección semántica:", error)

        return []

    def inferir_coleccion_tecnica(self, pregunta):
        colecciones = self.inferir_colecciones_tecnicas(pregunta, maximo=1)
        return colecciones[0] if colecciones else ""

    def parece_consulta_tecnica_programacion(self, pregunta):
        if not self.biblioteca.tiene_contenido_categoria("tecnica"):
            return False

        texto = normalizar(pregunta)
        if not texto:
            return False

        # Si el Señor pide explícitamente sus apuntes o un ramo, respetamos
        # primero la biblioteca académica.
        if any(m in texto for m in [
            "mis apuntes", "mi material", "biblioteca academica",
            "segun el modulo", "segun mis modulos",
        ]):
            return False

        # Órdenes de navegación/Internet no deben convertirse en RAG técnico.
        if any(m in texto for m in [
            "youtube", "spotify", "google", "busca en internet",
            "investiga en internet", "abre chrome", "abre ",
        ]):
            return False

        # Evita usar el libro de Python para otro lenguaje explícitamente pedido.
        if any(m in texto for m in [
            "javascript", "typescript", "java ", "c sharp", "c#", "php ",
            "kotlin", "swift", "rust ", "golang", "sql ",
        ]) and "python" not in texto:
            return False

        explicita = any(m in texto for m in [
            "mi libro", "el libro de python", "biblioteca tecnica",
            "libro tecnico", "ultimate python",
        ])
        if explicita:
            return True

        tokens = set(texto.split())
        fuertes = {
            "python", "repl", "pip", "pylint", "pep8", "pycharm",
            "kwargs", "xargs", "lambda", "pathlib",
        }
        if tokens & fuertes:
            return True

        # Conceptos habituales del libro. Se usan cuando no se nombró otro lenguaje.
        conceptos = {
            "variable", "variables", "string", "strings", "funcion", "funciones",
            "lista", "listas", "tupla", "tuplas", "set", "sets",
            "diccionario", "diccionarios", "clase", "clases", "constructor",
            "herencia", "polimorfismo", "excepcion", "excepciones",
            "modulo", "modulos", "paquete", "paquetes", "iterable", "iterables",
            "while", "for", "if", "elif", "else", "archivo", "archivos",
            "json", "csv", "decorador", "decoradores", "metodo", "metodos",
        }
        if tokens & conceptos:
            return True

        if "programacion" in tokens and not any(
            x in texto for x in ["java", "javascript", "c#", "sql"]
        ):
            return True

        return False

    def _confianza_resultados_biblioteca(self, resultados):
        utiles = [r for r in (resultados or []) if float(r.get("score", 0) or 0) > 0]
        if not utiles:
            return "sin evidencia", 0.0
        top = float(utiles[0].get("score", 0) or 0)
        segundo = float(utiles[1].get("score", 0) or 0) if len(utiles) > 1 else 0.0
        if top >= BIBLIOTECA_ROUTER_UMBRAL_ALTO and (top - segundo >= 0.035 or segundo >= 0.40):
            return "alta", top
        if top >= BIBLIOTECA_ROUTER_UMBRAL_MEDIO:
            return "media", top
        if top >= BIBLIOTECA_ROUTER_UMBRAL_MIN:
            return "baja", top
        return "sin evidencia", top

    def _es_pregunta_candidata_biblioteca(self, pregunta):
        texto = normalizar(pregunta)
        if not texto or len(texto) < 4 or not self.biblioteca.tiene_contenido():
            return False
        # Acciones, multimedia, clima, memoria personal y búsquedas actuales tienen rutas propias.
        bloqueadas = [
            "spotify", "youtube", "clima", "temperatura", "hora es", "abre ",
            "cerrar ", "apaga", "reinicia", "crea carpeta", "borra ", "elimina ",
            "recuerda que", "aprende que", "olvida ", "que recuerdas de mi",
            "busca en google", "busca en internet", "investiga en internet",
            "noticias", "hoy ", "actualmente", "ultima version", "última version",
            "precio actual", "cotizacion", "resultado de hoy",
        ]
        if any(x in texto for x in bloqueadas):
            return False
        if any(x in texto for x in [
            "mis apuntes", "biblioteca academica", "mi material", "segun el modulo",
            "mi libro", "biblioteca tecnica", "ultimate python",
        ]):
            return True
        # Preguntas/órdenes de explicación. Evita enviar saludos y charla casual al índice.
        primeras = set(texto.split()[:3])
        marcas = {
            "que", "como", "cual", "cuales", "por", "explica", "explicame", "define",
            "dime", "ensename", "enseñame", "ayudame", "diferencia", "funciona",
            "sirve", "significa", "ejemplo", "hacer", "crear", "programar",
        }
        if primeras & marcas:
            return True
        # También aceptamos términos que coincidan con metadatos cargados.
        tokens = set(texto.split())
        return bool(tokens & self.biblioteca.palabras_metadatos())

    def _perfil_dominio_router(self, pregunta):
        """Detecta señales de dominio solo para desempatar evidencia local real."""
        texto = normalizar(pregunta)
        tokens = set(texto.split())
        perfiles = set()

        def contiene(frases):
            return any((" " in f and f in texto) or (" " not in f and f in tokens) for f in frases)

        python_fuerte = contiene({
            "python", "repl", "pip", "pylint", "pep8", "kwargs", "xargs", "lambda",
            "return", "def", "elif", "pycharm", "pathlib",
        })
        python_generico = contiene({
            "tupla", "diccionario", "lista", "listas", "clase", "clases", "herencia",
            "excepcion", "excepciones", "string", "strings",
        })
        # Palabras como "función" son demasiado generales para declarar Python por sí solas.
        # Los conceptos genéricos solo refuerzan Python si la conversación ya estaba allí.
        if python_fuerte or (python_generico and self._contexto_python_activo()):
            perfiles.add("python")
        if contiene({
            "memoria ram", "ram", "cache", "cpu", "procesador", "procesadores",
            "arquitectura", "alu", "registros", "memoria virtual",
            "memoria principal", "bus de datos", "placa madre", "hardware",
        }):
            perfiles.add("hardware")
        if contiene({
            "tcp", "udp", "vlan", "subred", "subnet", "router", "switch", "dns",
            "dhcp", "ethernet", "modelo osi", "direccion ip", "direcciones ip", "redes",
        }):
            perfiles.add("redes")
        if contiene({
            "ciberseguridad", "seguridad informatica", "malware", "ransomware", "phishing",
            "vulnerabilidad", "vulnerabilidades", "firewall", "cifrado", "criptografia",
            "autenticacion", "hardening", "pentesting",
        }):
            perfiles.add("seguridad")
        if contiene({
            "sql", "select", "insert", "update", "join", "base de datos", "bases de datos",
            "clave primaria", "foreign key",
        }):
            perfiles.add("sql")
        if contiene({"docker", "contenedor", "contenedores", "dockerfile", "docker compose", "imagen docker", "volumen docker"}):
            perfiles.add("docker")
        if contiene({"linux", "bash", "chmod", "systemd", "ubuntu", "debian", "shell", "apt"}):
            perfiles.add("linux")
        return perfiles

    def _consulta_router_categoria(self, pregunta, categoria, perfiles):
        """Añade contexto mínimo al embedding del router, sin alterar la pregunta final."""
        base = self.corregir_terminos_tecnicos_asr(self.limpiar_consulta_tecnica(pregunta))
        extras = []
        if categoria == "academica":
            if "hardware" in perfiles:
                extras += ["arquitectura de computadores", "memoria principal", "hardware"]
            if "redes" in perfiles:
                extras += ["redes de computadores", "protocolos de red"]
            if "seguridad" in perfiles:
                extras += ["ciberseguridad", "seguridad de redes"]
            if "sql" in perfiles:
                extras += ["bases de datos"]
            if "python" in perfiles:
                extras += ["programacion", "algoritmos"]
        else:
            if "python" in perfiles:
                extras += ["Python", "programacion"]
            if "docker" in perfiles:
                extras += ["Docker", "contenedores"]
            if "linux" in perfiles:
                extras += ["Linux"]
            if "redes" in perfiles:
                extras += ["redes"]
            if "seguridad" in perfiles:
                extras += ["ciberseguridad"]
            if "sql" in perfiles:
                extras += ["SQL", "bases de datos"]
            if "hardware" in perfiles:
                extras += ["hardware", "arquitectura de computadores"]
        return (base + " " + " ".join(extras)).strip()

    def _bonus_dominio_router(self, perfiles, categoria, etiqueta):
        """Pequeño refuerzo de dominio; nunca crea evidencia si el RAG no la encontró."""
        e = normalizar(etiqueta)
        bonus = 0.0
        if "python" in perfiles:
            if categoria == "tecnica" and "python" in e:
                bonus += 0.13
            elif categoria == "academica" and any(x in e for x in ["program", "algorit", "software"]):
                bonus += 0.045
        if "hardware" in perfiles:
            if any(x in e for x in ["arquitectura", "computador", "hardware", "sistema"]):
                bonus += 0.12 if categoria == "academica" else 0.08
            # Un libro de Python puede mencionar RAM como analogía sin ser la fuente principal.
            # v2.8.2: la penalización es mayor cuando la pregunta es claramente de
            # hardware y no contiene una señal Python explícita. Así una mención
            # incidental de RAM en un libro de programación no desplaza fácilmente
            # a un ramo completo de Arquitectura de Computadores.
            if categoria == "tecnica" and "python" in e and "python" not in perfiles:
                bonus -= 0.10
        if "redes" in perfiles and any(x in e for x in ["red", "network", "comunic"]):
            bonus += 0.105
        if "seguridad" in perfiles and any(x in e for x in ["seguridad", "ciber", "security"]):
            bonus += 0.105
        if "sql" in perfiles and any(x in e for x in ["base de datos", "sql", "database"]):
            bonus += 0.105
        if "docker" in perfiles and "docker" in e:
            bonus += 0.13
        if "linux" in perfiles and any(x in e for x in ["linux", "ubuntu", "sistema operativo"]):
            bonus += 0.11
        return bonus

    def _puntaje_grupo_router(self, resultados, perfiles, categoria, etiqueta):
        scores = sorted(
            [float(r.get("score", 0) or 0) for r in resultados if float(r.get("score", 0) or 0) >= BIBLIOTECA_ROUTER_UMBRAL_MIN],
            reverse=True,
        )[:BIBLIOTECA_ROUTER_MAX_GRUPO]
        if not scores:
            return 0.0
        top = scores[0]
        media3 = sum(scores[:3]) / min(3, len(scores))
        soporte = 0.020 * min(len(scores), BIBLIOTECA_ROUTER_MAX_GRUPO)
        valor = (0.68 * top) + (0.24 * media3) + soporte
        valor += self._bonus_dominio_router(perfiles, categoria, etiqueta)
        return max(0.0, valor)

    def _mejor_grupo_router(self, resultados, categoria, perfiles):
        grupos = {}
        for r in resultados or []:
            if float(r.get("score", 0) or 0) < BIBLIOTECA_ROUTER_UMBRAL_MIN:
                continue
            if categoria == "academica":
                etiqueta = (r.get("ramo") or r.get("modulo") or r.get("documento") or "General").strip()
            else:
                etiqueta = (r.get("coleccion") or r.get("documento") or "General").strip()
            grupos.setdefault(etiqueta or "General", []).append(r)

        candidatos = []
        for etiqueta, items in grupos.items():
            valor = self._puntaje_grupo_router(items, perfiles, categoria, etiqueta)
            candidatos.append((valor, etiqueta, items))
        candidatos.sort(key=lambda x: x[0], reverse=True)
        return candidatos[0] if candidatos else (0.0, "", [])

    def decidir_ruta_biblioteca(self, pregunta):
        """v2.8.3: compara evidencia coherente por ramo/colección y por categoría."""
        decision = {
            "ruta": "qwen", "confianza": "sin evidencia", "top_score": 0.0,
            "colecciones": [], "ramo": "", "resultados": [], "motivo": "",
            "score_academica": 0.0, "score_tecnica": 0.0,
            "grupo_academico": "", "grupo_tecnico": "", "perfiles": [],
        }
        if not BIBLIOTECA_INTELIGENTE_ACTIVA or not self._es_pregunta_candidata_biblioteca(pregunta):
            return decision

        pregunta_corregida = self.corregir_terminos_tecnicos_asr(pregunta)
        texto = normalizar(pregunta_corregida)
        explicita_academica = any(x in texto for x in [
            "mis apuntes", "mi material", "biblioteca academica", "segun el modulo",
            "segun mis modulos", "segun mis apuntes",
        ])
        explicita_tecnica = any(x in texto for x in [
            "mi libro", "biblioteca tecnica", "libro tecnico", "ultimate python",
        ])
        perfiles = self._perfil_dominio_router(pregunta_corregida)
        decision["perfiles"] = sorted(perfiles)

        try:
            qa = self._consulta_router_categoria(pregunta_corregida, "academica", perfiles)
            qt = self._consulta_router_categoria(pregunta_corregida, "tecnica", perfiles)
            resultados_a = self.biblioteca.buscar(
                qa,
                limite=BIBLIOTECA_ROUTER_RESULTADOS_POR_CATEGORIA,
                categoria_preferida="academica",
            ) if self.biblioteca.tiene_contenido_categoria("academica") else []
            resultados_t = self.biblioteca.buscar(
                qt,
                limite=BIBLIOTECA_ROUTER_RESULTADOS_POR_CATEGORIA,
                categoria_preferida="tecnica",
            ) if self.biblioteca.tiene_contenido_categoria("tecnica") else []
        except Exception as error:
            print("BIBLIOTECA INTELIGENTE: error de enrutamiento:", error)
            return decision

        va, ramo, grupo_a = self._mejor_grupo_router(resultados_a, "academica", perfiles)
        vt, coleccion_principal, grupo_t = self._mejor_grupo_router(resultados_t, "tecnica", perfiles)
        decision["score_academica"] = va
        decision["score_tecnica"] = vt
        decision["grupo_academico"] = ramo
        decision["grupo_tecnico"] = coleccion_principal

        todos = sorted(
            [r for r in (resultados_a + resultados_t) if float(r.get("score", 0) or 0) >= BIBLIOTECA_ROUTER_UMBRAL_MIN],
            key=lambda r: float(r.get("score", 0) or 0),
            reverse=True,
        )
        confianza, top_score = self._confianza_resultados_biblioteca(todos)
        decision.update({"confianza": confianza, "top_score": top_score, "resultados": todos})

        hay_a = va > 0 and bool(grupo_a)
        hay_t = vt > 0 and bool(grupo_t)

        if explicita_academica:
            decision["ruta"] = "academica"
            decision["motivo"] = "solicitud explícita de apuntes"
        elif explicita_tecnica:
            decision["ruta"] = "tecnica"
            decision["motivo"] = "solicitud explícita de libro técnico"
        elif not hay_a and not hay_t:
            decision["motivo"] = "sin evidencia local suficiente"
            self.ultima_decision_biblioteca = decision
            return decision
        elif hay_a and hay_t and abs(va - vt) <= BIBLIOTECA_ROUTER_MARGEN_MIXTO_ROBUSTO:
            decision["ruta"] = "mixta"
            decision["motivo"] = "evidencia coherente y comparable en ambas bibliotecas"
        elif vt > va:
            decision["ruta"] = "tecnica"
            decision["motivo"] = "grupo técnico más coherente para el tema"
        else:
            decision["ruta"] = "academica"
            decision["motivo"] = "ramo académico más coherente para el tema"

        if decision["ruta"] in {"tecnica", "mixta"} and grupo_t:
            mejores_col = {}
            for r in resultados_t:
                if float(r.get("score", 0) or 0) < BIBLIOTECA_ROUTER_UMBRAL_MIN:
                    continue
                col = (r.get("coleccion") or "General").strip() or "General"
                mejores_col[col] = max(mejores_col.get(col, 0.0), float(r.get("score", 0) or 0))
            orden = sorted(mejores_col.items(), key=lambda x: x[1], reverse=True)
            if orden:
                top = orden[0][1]
                decision["colecciones"] = [
                    n for n, s in orden
                    if s >= BIBLIOTECA_ROUTER_UMBRAL_MIN
                    and top - s <= BIBLIOTECA_ROUTER_MARGEN_COLECCION
                ][:BIBLIOTECA_ROUTER_MAX_COLECCIONES]
            if not decision["colecciones"]:
                decision["colecciones"] = [coleccion_principal]

        if decision["ruta"] in {"academica", "mixta"} and ramo:
            decision["ramo"] = ramo

        self.ultima_decision_biblioteca = decision
        print(
            "BIBLIOTECA INTELIGENTE v2.8.3: "
            f"ruta={decision['ruta']} confianza={decision['confianza']} "
            f"top={decision['top_score']:.3f} "
            f"scoreA={va:.3f} scoreT={vt:.3f} "
            f"ramo='{decision['ramo']}' colecciones={decision['colecciones']} "
            f"perfiles={decision['perfiles']} motivo={decision['motivo']}"
        )
        return decision

    def _formatear_contexto_inteligente(self, resultados, maximo=5):
        bloques = []
        for i, r in enumerate((resultados or [])[:maximo], 1):
            cat = normalizar(r.get("categoria", "academica")) or "academica"
            if cat == "tecnica":
                origen = f"Libro técnico / colección {r.get('coleccion') or 'General'}"
            else:
                origen = f"Apunte académico / ramo {r.get('ramo') or 'General'}"
            texto = (r.get("texto") or "").strip()
            if len(texto) > 520:
                texto = texto[:520].rsplit(" ", 1)[0] + "..."
            bloques.append(
                f"[CONTEXTO {i}] {origen} | documento {r.get('documento','')} | "
                f"página {r.get('pagina','')} | relevancia {float(r.get('score',0)):.3f}\n{texto}"
            )
        return "\n\n".join(bloques)

    def consultar_biblioteca_mixta_async(self, pregunta, decision=None):
        consulta = self.limpiar_consulta_academica(self.limpiar_consulta_tecnica(pregunta))
        decision = decision or self.decidir_ruta_biblioteca(consulta)
        profunda = self.es_pedido_academico_profundo(pregunta)
        token = self.iniciar_proceso("biblioteca_inteligente")
        if token is None:
            self.responder("todavía estoy terminando la consulta anterior.", "pensando")
            return
        self.expresion_pensando()

        def trabajo():
            respuesta = None
            uso_streaming = False
            try:
                # v2.8.1: una consulta mixta recupera por separado para que una
                # biblioteca no monopolice todos los puestos del top-K.
                limite_cat = 4 if profunda else 3
                resultados_a = self.biblioteca.buscar(
                    consulta, limite=limite_cat,
                    ramo_preferido=(decision.get("ramo") or ""),
                    categoria_preferida="academica",
                )
                resultados_t = self.biblioteca.buscar(
                    consulta, limite=limite_cat,
                    categoria_preferida="tecnica",
                    colecciones_preferidas=(decision.get("colecciones") or None),
                )
                utiles_a = [r for r in resultados_a if float(r.get("score", 0) or 0) >= BIBLIOTECA_ROUTER_UMBRAL_MIN]
                utiles_t = [r for r in resultados_t if float(r.get("score", 0) or 0) >= BIBLIOTECA_ROUTER_UMBRAL_MIN]
                # Intercalamos ambas fuentes para conservar equilibrio en el prompt.
                utiles = []
                for i in range(max(len(utiles_a), len(utiles_t))):
                    if i < len(utiles_a):
                        utiles.append(utiles_a[i])
                    if i < len(utiles_t):
                        utiles.append(utiles_t[i])
                resultados = utiles
                if not utiles:
                    self.terminar_proceso(token)
                    self.root.after(0, lambda: self.conversar_ollama_async(consulta))
                    return

                contexto = self._formatear_contexto_inteligente(utiles, 6 if profunda else 4)
                estilo = self.preferencias_aprendidas_para_prompt()
                instrucciones = (
                    "Eres Beta, tutora personal y académica del Señor. Responde en español. "
                    "La consulta necesita combinar conocimiento local de APUNTES ACADÉMICOS y "
                    "LIBROS TÉCNICOS. Prioriza estrictamente el contenido recuperado y no inventes "
                    "que un documento dice algo ausente. Integra las fuentes en una sola explicación "
                    "natural; no enumeres nombres de PDF ni páginas salvo que el Señor los pida. "
                    "Si hay diferencias entre fuentes, explícalas sin ocultarlas. No uses Internet. "
                    "Cuando sea programación, puedes incluir un ejemplo corto y correcto. "
                    "Sin Markdown extraño para voz y termina una oración completa. "
                    + ("Explica con detalle pedagógico en unas 140 a 190 palabras. " if profunda
                       else "Responde de manera directa en unas 70 a 110 palabras. ")
                    + (f"Adapta discretamente el estilo a estas preferencias: {estilo[:220]}." if estilo else "")
                )
                mensajes = [
                    {"role": "system", "content": instrucciones},
                    {"role": "user", "content": f"Pregunta: {consulta}\n\nCONOCIMIENTO LOCAL:\n{contexto}"},
                ]
                if STREAMING_OLLAMA_ACTIVO:
                    respuesta = self.generar_y_hablar_ollama_streaming(
                        mensajes, "biblioteca_inteligente", token,
                        temperatura=0.10,
                        num_predict=230 if profunda else 130,
                        num_ctx=1664 if profunda else 1350,
                    )
                    uso_streaming = bool(respuesta)
                else:
                    respuesta = self.enviar_ollama(
                        mensajes, temperatura=0.10,
                        num_predict=230 if profunda else 130,
                        num_ctx=1664 if profunda else 1350,
                    )
                    if respuesta:
                        respuesta = self.limpiar_respuesta_ollama(respuesta)

                self.ultimas_fuentes_tecnicas = [
                    r for r in utiles if normalizar(r.get("categoria", "")) == "tecnica"
                ][:4]
                self.ultimas_fuentes_academicas = [
                    r for r in utiles if normalizar(r.get("categoria", "academica")) == "academica"
                ][:4]
                self.ultimo_contexto_inteligente = {
                    "tema_base": consulta, "consulta": consulta,
                    "resultados": utiles[:6], "respuesta": respuesta or "",
                }
                self.ultimo_contexto_inteligente_ts = time.time()
                self.ultimo_contexto_tecnico_ts = 0.0
                self.ultimo_contexto_academico_ts = 0.0
            except Exception as error:
                print("ERROR BIBLIOTECA INTELIGENTE:", error)
            finally:
                self.terminar_proceso(token)

            if token != self.proceso_id:
                return
            if respuesta and not uso_streaming:
                self.root.after(0, lambda r=respuesta: self.responder(r, "hablando", "biblioteca_inteligente"))
            elif not respuesta:
                self.root.after(0, lambda: self.responder(
                    "no pude combinar mis bibliotecas en este momento.", "confundida"
                ))

        threading.Thread(target=trabajo, daemon=True).start()

    def es_seguimiento_biblioteca_inteligente(self, pregunta):
        if self.ultimo_tipo_respuesta_terminada != "biblioteca_inteligente":
            return False
        if not self.ultimo_contexto_inteligente:
            return False
        if time.time() - self.ultimo_contexto_inteligente_ts > BIBLIOTECA_INTELIGENTE_CONTEXTO_SEGUNDOS:
            return False
        if self._hay_cambio_dominio_contextual(
            pregunta, self.ultimo_contexto_inteligente, "inteligente"
        ):
            return False
        texto = self.corregir_seguimiento_academico_corto(pregunta)
        palabras = texto.split()
        marcas = [
            "profundiza", "explicame mas", "dame un ejemplo", "otro ejemplo",
            "como funciona", "por que", "cual es la diferencia", "paso a paso",
            "resumelo", "continua", "sigue", "explicame el codigo", "muestrame el codigo",
        ]
        return any(m in texto for m in marcas) or (len(palabras) <= 9 and bool(palabras))

    def conversar_contexto_inteligente_async(self, pregunta):
        contexto = self.ultimo_contexto_inteligente or {}
        base = (contexto.get("tema_base") or "").strip()
        seguimiento = self.corregir_seguimiento_academico_corto(pregunta) or pregunta
        seguimiento = self.corregir_terminos_tecnicos_asr(seguimiento)
        consulta = f"{base}. Seguimiento: {seguimiento}" if base else seguimiento
        self.consultar_biblioteca_mixta_async(consulta)

    def ventana_biblioteca_inteligente(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Biblioteca inteligente de Beta")
        ventana.geometry("700x520")
        ventana.attributes("-topmost", True)
        docs_a, frags_a = self.biblioteca.estadisticas_categoria("academica")
        docs_t, frags_t = self.biblioteca.estadisticas_categoria("tecnica")
        colecciones = self.biblioteca.listar_colecciones_tecnicas()
        ultima = self.ultima_decision_biblioteca or {}
        texto = tk.Text(ventana, wrap="word", font=("Segoe UI", 10))
        texto.pack(fill="both", expand=True, padx=12, pady=12)
        lineas = [
            "BIBLIOTECA INTELIGENTE v2.8.3",
            "",
            f"Estado: {'ACTIVA' if BIBLIOTECA_INTELIGENTE_ACTIVA else 'DESACTIVADA'}",
            f"Académica: {docs_a} documentos / {frags_a} fragmentos",
            f"Técnica: {docs_t} documentos / {frags_t} fragmentos",
            "",
            "Colecciones técnicas:",
        ]
        if colecciones:
            lineas.extend(
                f"  - {c[0]}: {c[1]} documento(s), {c[2]} fragmentos" for c in colecciones
            )
        else:
            lineas.append("  - Ninguna")
        lineas += [
            "", "Última decisión:",
            f"  Ruta: {ultima.get('ruta','Todavía sin consultas')}",
            f"  Confianza: {ultima.get('confianza','-')}",
            f"  Relevancia superior: {float(ultima.get('top_score',0) or 0):.3f}",
            f"  Evidencia académica: {float(ultima.get('score_academica',0) or 0):.3f}",
            f"  Evidencia técnica: {float(ultima.get('score_tecnica',0) or 0):.3f}",
            f"  Grupo académico: {ultima.get('grupo_academico') or '-'}",
            f"  Grupo técnico: {ultima.get('grupo_tecnico') or '-'}",
            f"  Perfiles detectados: {', '.join(ultima.get('perfiles') or []) or '-'}",
            f"  Colecciones: {', '.join(ultima.get('colecciones') or []) or '-'}",
            f"  Ramo: {ultima.get('ramo') or '-'}",
            f"  Motivo: {ultima.get('motivo') or '-'}",
            "",
            "Beta usa sus documentos locales cuando existe evidencia suficiente. Si no la hay, "
            "la consulta continúa hacia Qwen en vez de atribuir información inexistente a sus libros.",
        ]
        texto.insert("1.0", "\n".join(lineas))
        texto.configure(state="disabled")

        def probar():
            q = simpledialog.askstring(
                "Probar enrutamiento", "Escriba una pregunta para ver dónde buscaría Beta:",
                parent=ventana,
            )
            if not q:
                return
            d = self.decidir_ruta_biblioteca(q)
            messagebox.showinfo(
                "Decisión de Beta",
                f"Ruta: {d.get('ruta')}\nConfianza: {d.get('confianza')}\n"
                f"Top score: {d.get('top_score',0):.3f}\n"
                f"Evidencia académica: {d.get('score_academica',0):.3f}\n"
                f"Evidencia técnica: {d.get('score_tecnica',0):.3f}\n"
                f"Grupo académico: {d.get('grupo_academico') or '-'}\n"
                f"Grupo técnico: {d.get('grupo_tecnico') or '-'}\n"
                f"Colecciones: {', '.join(d.get('colecciones') or []) or '-'}\n"
                f"Ramo: {d.get('ramo') or '-'}\nMotivo: {d.get('motivo') or '-'}",
                parent=ventana,
            )

        ttk.Button(ventana, text="Probar enrutamiento...", command=probar).pack(pady=(0, 12))

    def _perfiles_contexto_guardado(self, contexto, tipo_contexto=""):
        """Obtiene dominios fuertes del contexto anterior sin depender solo del texto.

        Esto permite distinguir un seguimiento real (por ejemplo, ``return`` después
        de funciones en Python) de una nueva pregunta corta que cambia de materia
        (por ejemplo, ``qué es una memoria RAM`` después de hablar de Python).
        """
        contexto = contexto or {}
        partes = [
            str(contexto.get("tema_base") or ""),
            str(contexto.get("consulta") or ""),
            str(contexto.get("ramo") or ""),
            str(contexto.get("coleccion") or ""),
            " ".join(str(x) for x in (contexto.get("colecciones") or []) if x),
        ]
        for r in (contexto.get("resultados") or contexto.get("locales") or [])[:6]:
            if isinstance(r, dict):
                partes.extend([
                    str(r.get("ramo") or ""),
                    str(r.get("coleccion") or ""),
                ])
        perfiles = set(self._perfil_dominio_router(" ".join(partes)))

        # Los nombres de colección/ramo son evidencia más estable que una frase corta.
        etiquetas = normalizar(" ".join(partes))
        if "python" in etiquetas:
            perfiles.add("python")
        if "docker" in etiquetas:
            perfiles.add("docker")
        if any(x in etiquetas for x in ["arquitectura", "hardware", "computadores"]):
            perfiles.add("hardware")
        if any(x in etiquetas for x in ["redes", "network"]):
            perfiles.add("redes")
        if any(x in etiquetas for x in ["ciberseguridad", "seguridad"]):
            perfiles.add("seguridad")
        if any(x in etiquetas for x in ["base de datos", "sql"]):
            perfiles.add("sql")
        if "linux" in etiquetas:
            perfiles.add("linux")
        return perfiles

    def _hay_cambio_dominio_contextual(self, pregunta, contexto, tipo_contexto=""):
        """Devuelve True solo ante un cambio de dominio suficientemente claro.

        Las continuaciones deícticas como ``dame un ejemplo`` no tienen un dominio
        propio y conservan el contexto. En cambio, una pregunta que activa un perfil
        nuevo y disjunto (Python -> hardware, Python -> Docker, etc.) vuelve al
        enrutador global para evitar el efecto de contexto pegajoso.
        """
        texto = self.corregir_seguimiento_academico_corto(pregunta) or pregunta
        texto = self.corregir_terminos_tecnicos_asr(texto)
        perfiles_nuevos = set(self._perfil_dominio_router(texto))
        if not perfiles_nuevos:
            return False
        perfiles_previos = self._perfiles_contexto_guardado(contexto, tipo_contexto)
        if not perfiles_previos:
            return False
        if perfiles_nuevos.isdisjoint(perfiles_previos):
            print(
                "CAMBIO DE TEMA DETECTADO: "
                f"contexto={sorted(perfiles_previos)} -> pregunta={sorted(perfiles_nuevos)}. "
                "Se vuelve al enrutador global."
            )
            return True
        return False

    def _terminos_codigo_clave(self, consulta):
        texto = normalizar(consulta)
        tokens = set(texto.split())
        candidatos = {
            "return", "kwargs", "xargs", "elif", "def", "lambda", "yield",
            "import", "pip", "pylint", "pep8", "try", "except", "finally",
        }
        return [t for t in candidatos if t in tokens]

    def _expandir_consulta_codigo(self, consulta):
        """Añade sinónimos pedagógicos solo para recuperar mejor el fragmento correcto."""
        claves = self._terminos_codigo_clave(consulta)
        extras = []
        mapa = {
            "return": "palabra clave return devolver valor resultado de una funcion",
            "kwargs": "kwargs argumentos nombrados diccionario argumentos de funcion",
            "xargs": "xargs argumentos variables multiples argumentos de funcion",
            "elif": "elif condicion if else control de flujo",
            "def": "def definir declarar funcion python",
            "lambda": "lambda funcion anonima expresion lambda",
            "yield": "yield generador devolver valores iteracion",
            "import": "import importar modulo paquete python",
            "pip": "pip instalar paquetes indice de paquetes python",
            "pylint": "pylint linter errores advertencias codigo python",
            "pep8": "pep8 guia de estilo formato codigo python",
            "try": "try excepciones manejo de errores",
            "except": "except excepciones manejo de errores",
            "finally": "finally excepciones bloque final",
        }
        for clave in claves:
            extras.append(mapa.get(clave, clave))
        return (consulta + " " + " ".join(extras)).strip() if extras else consulta

    def buscar_tecnico_hibrido(
        self, consulta, limite=TECNICA_RESULTADOS, coleccion="", colecciones=None
    ):
        """Búsqueda semántica con refuerzo léxico para palabras clave de código.

        El texto original sigue siendo la pregunta que recibe Qwen. La expansión
        solo se usa para recuperar mejores fragmentos del libro. Cuando una palabra
        clave exacta aparece en un fragmento, recibe un pequeño bonus de ranking.
        """
        consulta_busqueda = self._expandir_consulta_codigo(consulta)
        claves = self._terminos_codigo_clave(consulta)
        limite_amplio = max(int(limite) * 4, 16) if claves else int(limite)
        resultados = self.biblioteca.buscar(
            consulta_busqueda,
            limite=limite_amplio,
            categoria_preferida="tecnica",
            coleccion_preferida=coleccion if not colecciones else "",
            colecciones_preferidas=colecciones or None,
        )
        if not claves:
            return resultados[:limite]

        reordenados = []
        for r in resultados:
            item = dict(r)
            sem = float(item.get("score", 0) or 0)
            contenido = normalizar(
                " ".join([
                    str(item.get("texto") or ""),
                    str(item.get("documento") or ""),
                    str(item.get("modulo") or ""),
                ])
            )
            tokens_contenido = set(contenido.split())
            coincidencias = sum(1 for clave in claves if clave in tokens_contenido)
            bonus = min(0.22, 0.14 * coincidencias)
            item["score_semantico"] = sem
            item["score"] = min(1.0, sem + bonus)
            item["coincidencia_lexica"] = coincidencias
            reordenados.append(item)

        reordenados.sort(
            key=lambda r: (
                int(r.get("coincidencia_lexica", 0) or 0),
                float(r.get("score", 0) or 0),
            ),
            reverse=True,
        )
        if reordenados and claves:
            print(
                "BÚSQUEDA TÉCNICA HÍBRIDA: "
                f"claves={claves} consulta='{consulta_busqueda}' "
                f"mejor_score={float(reordenados[0].get('score',0)):.3f}"
            )
        return reordenados[:limite]

    def formatear_fuentes_tecnicas(self, resultados, maximo=4):
        bloques = []
        for i, r in enumerate(resultados[:maximo], 1):
            encabezado = (
                f"[LIBRO {i}] Colección: {r.get('coleccion') or 'General'} | "
                f"PDF: {r.get('documento','')} | página {r.get('pagina','')}"
            )
            texto = (r.get("texto") or "").strip()
            limite = 560 if maximo > 3 else 420
            if len(texto) > limite:
                texto = texto[:limite].rsplit(" ", 1)[0] + "..."
            bloques.append(encabezado + "\nTexto: " + texto)
        return "\n\n".join(bloques)

    def es_seguimiento_tecnico(self, pregunta):
        if self.ultimo_tipo_respuesta_terminada != "tecnico":
            return False
        if not self.ultimo_contexto_tecnico:
            return False
        if time.time() - self.ultimo_contexto_tecnico_ts > TECNICA_CONTEXTO_SEGUNDOS:
            return False
        if self._hay_cambio_dominio_contextual(
            pregunta, self.ultimo_contexto_tecnico, "tecnico"
        ):
            return False

        texto = self.corregir_seguimiento_academico_corto(pregunta)
        palabras = texto.split()
        marcadores = [
            "explicame mas", "dime mas", "cuentame mas", "profundiza",
            "profundice", "amplia", "detalla", "continua", "sigue",
            "dame un ejemplo", "ponme un ejemplo", "hazme un ejemplo",
            "otro ejemplo", "dame otro", "que significa eso", "por que",
            "como funciona eso", "cual es la diferencia", "resumelo",
            "la primera", "la segunda", "la tercera", "el primero", "el segundo",
            "el tercero", "hazme un ejercicio", "dame un ejercicio",
            "muestrame el codigo", "explicame el codigo", "paso a paso",
        ]
        if any(m in texto for m in marcadores):
            return True
        if self.ultimo_tipo_respuesta_terminada == "tecnico" and len(palabras) <= 9:
            if palabras and palabras[0] in {
                "que", "cual", "cuales", "como", "por", "explica", "explicame",
                "dime", "muestra", "muestrame", "hazme", "dame",
            }:
                return True
        return False

    def consultar_biblioteca_tecnica_async(self, pregunta, forzar=False):
        consulta = self.limpiar_consulta_tecnica(pregunta)
        if not consulta:
            self.responder("necesito saber qué tema técnico desea revisar.", "confundida")
            return

        profunda = self.es_pedido_academico_profundo(pregunta)
        fuentes_max = TECNICA_FUENTES_PROFUNDO if profunda else TECNICA_FUENTES_BREVE
        tokens_max = TECNICA_TOKENS_PROFUNDO if profunda else TECNICA_TOKENS_BREVE
        num_ctx = TECNICA_NUM_CTX_PROFUNDO if profunda else TECNICA_NUM_CTX_BREVE
        colecciones = self.inferir_colecciones_tecnicas(consulta)
        coleccion = colecciones[0] if colecciones else ""

        token = self.iniciar_proceso("biblioteca_tecnica")
        if token is None:
            self.responder("todavía estoy terminando la consulta anterior.", "pensando")
            return
        self.expresion_pensando()

        def trabajo():
            respuesta = None
            uso_streaming = False
            locales_utiles = []
            error = ""
            try:
                inicio = time.perf_counter()
                locales = self.buscar_tecnico_hibrido(
                    consulta,
                    limite=TECNICA_RESULTADOS,
                    coleccion=coleccion if len(colecciones) <= 1 else "",
                    colecciones=colecciones if len(colecciones) > 1 else None,
                )
                print(
                    f"LATENCIA BIBLIOTECA TÉCNICA: "
                    f"{time.perf_counter() - inicio:.2f} s"
                )
                locales_utiles = [
                    r for r in locales
                    if float(r.get("score", 0)) >= TECNICA_UMBRAL_MIN
                ]
                top_score = float(locales[0].get("score", 0)) if locales else 0.0

                if not locales_utiles:
                    # No inventamos que el libro cubre algo que no recuperamos.
                    respuesta = (
                        "Señor, no encontré ese tema con suficiente claridad en mi "
                        "biblioteca técnica local. Puedo explicárselo con mi conocimiento "
                        "general o buscar información actual si usted me lo pide."
                    )
                else:
                    contexto = self.formatear_fuentes_tecnicas(
                        locales_utiles, fuentes_max
                    )
                    estilo = self.preferencias_aprendidas_para_prompt()
                    instrucciones = (
                        "Eres Beta, tutora técnica personal del Señor. "
                        "Responde en español de forma clara, práctica y pedagógica. "
                        "Usa LIBROS TÉCNICOS LOCALES como fuente principal y no inventes "
                        "contenido ausente. Puedes reorganizar y explicar con tus propias "
                        "palabras. NO menciones el nombre del PDF, libro, autor, número de "
                        "página ni la palabra fuente, salvo que el Señor lo pregunte. "
                        "No uses Internet. Si la pregunta pide cómo hacer algo, explica "
                        "el procedimiento directamente. Si el tema es programación, cuando sea "
                        "útil incluye un ejemplo de código corto y correcto seguido de una explicación. "
                        "No fuerces ejemplos Python en temas de redes, seguridad u otras colecciones. "
                        "Evita asteriscos y formato que suene extraño al leerlo en voz. "
                        + (
                            "Modo profundo: desarrolla el tema en unas 150 a 200 palabras. "
                            if profunda else
                            "Modo normal: explica en unas 60 a 100 palabras, priorizando lo práctico. "
                        )
                        + "Termina siempre una oración completa."
                        + (
                            f" Adapta discretamente el estilo a estas preferencias confirmadas: "
                            f"{estilo[:220]}."
                            if estilo else ""
                        )
                    )
                    contenido = (
                        f"Pregunta del Señor: {consulta}\n\n"
                        f"LIBROS TÉCNICOS LOCALES RECUPERADOS:\n{contexto}\n\n"
                        "Enseña el concepto directamente. Las referencias son internas."
                    )
                    mensajes = [
                        {"role": "system", "content": instrucciones},
                        {"role": "user", "content": contenido},
                    ]
                    if STREAMING_OLLAMA_ACTIVO:
                        respuesta = self.generar_y_hablar_ollama_streaming(
                            mensajes,
                            "tecnico",
                            token,
                            temperatura=0.10,
                            num_predict=tokens_max,
                            num_ctx=num_ctx,
                        )
                        uso_streaming = bool(respuesta)
                    else:
                        respuesta = self.enviar_ollama(
                            mensajes,
                            temperatura=0.10,
                            num_predict=tokens_max,
                            num_ctx=num_ctx,
                        )
                        if respuesta:
                            respuesta = self.limpiar_respuesta_ollama(respuesta)

                self.ultimas_fuentes_tecnicas = locales_utiles[:fuentes_max]
                self.ultimo_contexto_academico_ts = 0.0
                self.ultimo_contexto_tecnico = {
                    "tema_base": consulta,
                    "coleccion": coleccion,
                    "colecciones": colecciones,
                    "consulta": consulta,
                    "locales": locales_utiles[:fuentes_max],
                    "respuesta": respuesta or "",
                }
                self.ultimo_contexto_tecnico_ts = time.time()

                print(
                    f"BIBLIOTECA TÉCNICA: consulta='{consulta}' "
                    f"colecciones='{', '.join(colecciones) if colecciones else 'todas'}' "
                    f"top_score={top_score:.3f} locales={len(locales_utiles)}"
                )
                for i, r in enumerate(locales_utiles[:5], 1):
                    print(
                        f"  LIBRO {i}: {r.get('documento')} pág. {r.get('pagina')} "
                        f"score={r.get('score',0):.3f}"
                    )
            except Exception as exc:
                error = str(exc)
                print("ERROR BIBLIOTECA TÉCNICA:", exc)
            finally:
                self.terminar_proceso(token)

            if token != self.proceso_id:
                return
            if respuesta and not uso_streaming:
                self.root.after(
                    0,
                    lambda r=respuesta: self.responder(
                        r, "hablando", "tecnico"
                    ),
                )
            elif not respuesta:
                self.root.after(
                    0,
                    lambda: self.responder(
                        "no pude consultar la biblioteca técnica en este momento.",
                        "confundida",
                    ),
                )

        threading.Thread(target=trabajo, daemon=True).start()

    def conversar_contexto_tecnico_async(self, pregunta):
        contexto = self.ultimo_contexto_tecnico
        if not contexto:
            self.consultar_biblioteca_tecnica_async(pregunta, forzar=True)
            return

        interpretada = self.corregir_seguimiento_academico_corto(pregunta) or pregunta
        interpretada = self.corregir_terminos_tecnicos_asr(interpretada)
        profunda = self.es_pedido_academico_profundo(interpretada)
        fuentes_max = TECNICA_FUENTES_PROFUNDO if profunda else TECNICA_FUENTES_BREVE
        tokens_max = TECNICA_TOKENS_PROFUNDO if profunda else TECNICA_TOKENS_BREVE
        num_ctx = TECNICA_NUM_CTX_PROFUNDO if profunda else TECNICA_NUM_CTX_BREVE
        tema_base = (contexto.get("tema_base") or contexto.get("consulta") or "").strip()
        coleccion = (contexto.get("coleccion") or "").strip()
        colecciones = [c for c in (contexto.get("colecciones") or []) if c]
        consulta_expandida = f"{tema_base} {interpretada}".strip()

        token = self.iniciar_proceso("contexto_tecnico")
        if token is None:
            self.responder("todavía estoy terminando la respuesta anterior.", "pensando")
            return
        self.expresion_pensando()

        def trabajo():
            respuesta = None
            uso_streaming = False
            try:
                inicio = time.perf_counter()
                # La recuperación prioriza la pregunta actual. El tema base sirve
                # como contexto secundario, no como término dominante de búsqueda.
                consulta_recuperacion = (
                    f"{interpretada}. Contexto relacionado: {tema_base}"
                    if tema_base else interpretada
                )
                nuevos = self.buscar_tecnico_hibrido(
                    consulta_recuperacion,
                    limite=TECNICA_RESULTADOS,
                    coleccion=coleccion if len(colecciones) <= 1 else "",
                    colecciones=colecciones if len(colecciones) > 1 else None,
                )
                print(
                    f"LATENCIA BIBLIOTECA TÉCNICA SEGUIMIENTO: "
                    f"{time.perf_counter() - inicio:.2f} s"
                )
                utiles = [
                    r for r in nuevos
                    if float(r.get("score", 0)) >= TECNICA_UMBRAL_MIN
                ]
                fuentes = utiles[:fuentes_max] or (contexto.get("locales") or [])[:fuentes_max]
                contexto_libros = self.formatear_fuentes_tecnicas(fuentes, fuentes_max)

                instrucciones = (
                    "Eres Beta, tutora técnica personal. Responde PRINCIPALMENTE al "
                    "seguimiento actual del Señor usando los LIBROS TÉCNICOS LOCALES recuperados. "
                    "El tema anterior es contexto secundario: no vuelvas a definirlo salvo que sea "
                    "imprescindible para responder. Si el seguimiento nombra una palabra clave, "
                    "función u operador concreto (por ejemplo return), céntrate en esa pieza, su "
                    "sintaxis y su uso. Responde en español, de manera práctica. No menciones PDF, "
                    "libro, autor, páginas ni fuentes salvo que el Señor lo solicite. No inventes "
                    "sintaxis que no esté respaldada por el material local. Si pide un ejemplo o "
                    "código, entrégalo y explícalo con claridad. No uses Internet. Termina siempre "
                    "la última oración."
                )
                contenido = (
                    f"Tema base: {tema_base}\n"
                    f"Seguimiento del Señor: {interpretada}\n\n"
                    f"LIBROS TÉCNICOS LOCALES RECUPERADOS:\n{contexto_libros}"
                )
                mensajes = [
                    {"role": "system", "content": instrucciones},
                    {"role": "user", "content": contenido},
                ]
                if STREAMING_OLLAMA_ACTIVO:
                    respuesta = self.generar_y_hablar_ollama_streaming(
                        mensajes, "tecnico", token,
                        temperatura=0.10, num_predict=tokens_max, num_ctx=num_ctx,
                    )
                    uso_streaming = bool(respuesta)
                else:
                    respuesta = self.enviar_ollama(
                        mensajes, temperatura=0.10,
                        num_predict=tokens_max, num_ctx=num_ctx,
                    )
                    if respuesta:
                        respuesta = self.limpiar_respuesta_ollama(respuesta)

                self.ultimas_fuentes_tecnicas = fuentes
                self.ultimo_contexto_tecnico = {
                    "tema_base": tema_base,
                    "coleccion": coleccion,
                    "colecciones": colecciones,
                    "consulta": interpretada,
                    "locales": fuentes,
                    "respuesta": respuesta or "",
                }
                self.ultimo_contexto_tecnico_ts = time.time()
                top = float(nuevos[0].get("score", 0)) if nuevos else 0.0
                print(
                    f"BIBLIOTECA TÉCNICA SEGUIMIENTO: coleccion='{coleccion or 'todas'}' "
                    f"tema='{tema_base}' pregunta='{interpretada}' "
                    f"top_score={top:.3f} locales={len(utiles)}"
                )
            except Exception as error:
                print("ERROR SEGUIMIENTO TÉCNICO:", error)
            finally:
                self.terminar_proceso(token)

            if token != self.proceso_id:
                return
            if respuesta and not uso_streaming:
                self.root.after(
                    0,
                    lambda r=respuesta: self.responder(r, "hablando", "tecnico"),
                )
            elif not respuesta:
                self.root.after(
                    0,
                    lambda: self.responder(
                        "no pude continuar esa explicación técnica.", "confundida"
                    ),
                )

        threading.Thread(target=trabajo, daemon=True).start()

    def manejar_comando_fuentes_tecnicas(self, texto):
        texto_n = normalizar(texto)
        marcadores_especificos = [
            "muestrame las fuentes tecnicas", "muestra las fuentes tecnicas",
            "ver fuentes tecnicas", "de que libro sacaste eso",
            "de cual libro sacaste eso", "en que pagina del libro",
        ]
        generico = "de donde sacaste eso" in texto_n
        if not any(m in texto_n for m in marcadores_especificos) and not (
            generico and self.ultimo_tipo_respuesta_terminada == "tecnico"
        ):
            return False

        if not self.ultimas_fuentes_tecnicas:
            self.responder(
                "todavía no tengo referencias técnicas de una consulta reciente.",
                "confundida",
            )
            return True

        self.root.after(0, self.ventana_fuentes_tecnicas)
        self.responder(
            "le muestro el libro y las páginas que utilicé como referencia interna.",
            "feliz",
        )
        return True

    def ventana_fuentes_tecnicas(self):
        if not self.ultimas_fuentes_tecnicas:
            messagebox.showinfo(
                "Fuentes técnicas",
                "Beta todavía no tiene fuentes técnicas de una consulta reciente.",
                parent=self.root,
            )
            return

        ventana = tk.Toplevel(self.root)
        ventana.title("Referencias técnicas utilizadas por Beta")
        ventana.geometry("980x470")
        ventana.attributes("-topmost", True)

        tabla = ttk.Treeview(
            ventana,
            columns=("n", "coleccion", "documento", "pagina", "relevancia", "ruta"),
            show="headings",
        )
        for clave, titulo in [
            ("n", "#"), ("coleccion", "Colección"), ("documento", "PDF"),
            ("pagina", "Página"), ("relevancia", "Relevancia"), ("ruta", "Ruta"),
        ]:
            tabla.heading(clave, text=titulo)
        tabla.column("n", width=35, anchor="center")
        tabla.column("coleccion", width=130)
        tabla.column("documento", width=300)
        tabla.column("pagina", width=70, anchor="center")
        tabla.column("relevancia", width=90, anchor="center")
        tabla.column("ruta", width=300)
        tabla.pack(fill="both", expand=True, padx=12, pady=12)

        for i, r in enumerate(self.ultimas_fuentes_tecnicas, 1):
            tabla.insert(
                "", "end",
                values=(
                    i, r.get("coleccion") or "General",
                    r.get("documento") or "", r.get("pagina") or "",
                    f"{float(r.get('score',0)):.3f}", r.get("ruta") or "",
                ),
            )

        def abrir(_event=None):
            seleccion = tabla.selection()
            if not seleccion:
                return
            ruta = str(tabla.item(seleccion[0])["values"][5])
            try:
                os.startfile(ruta)
            except Exception:
                pass

        tabla.bind("<Double-1>", abrir)
        ttk.Button(ventana, text="Abrir PDF", command=abrir).pack(pady=(0, 12))

    def limpiar_consulta_academica(self, pregunta):
        texto = (pregunta or "").strip()
        texto = re.sub(
            r"^\s*(?:beta|veta|meta|metas|petra)[,\s:;-]*",
            "",
            texto,
            flags=re.IGNORECASE,
        )
        patrones = [
            r"^\s*busca\s+en\s+mis\s+apuntes\s+",
            r"^\s*busca\s+en\s+la\s+biblioteca\s+",
            r"^\s*que\s+dicen\s+mis\s+apuntes\s+(?:sobre\s+)?",
            r"^\s*segun\s+mis\s+apuntes[,\s]+",
            r"^\s*segun\s+mi\s+material[,\s]+",
        ]
        for patron in patrones:
            texto_nuevo = re.sub(patron, "", texto, flags=re.IGNORECASE)
            if texto_nuevo != texto:
                texto = texto_nuevo.strip()
                break
        return texto.strip(" ,.;:-") or pregunta

    def parece_consulta_academica(self, pregunta):
        texto = normalizar(pregunta)

        # Órdenes explícitas de navegación/investigación se respetan antes de RAG.
        if any(
            marca in texto
            for marca in [
                "youtube", "google chrome", "busca en google", "busca en internet",
                "investiga en internet", "investiga sobre", "ultimas noticias",
                "noticias de", "abre chrome",
            ]
        ):
            return False

        explicita = any(
            marca in texto
            for marca in [
                "mis apuntes", "mi material", "biblioteca academica",
                "biblioteca de beta", "segun el modulo", "segun mis modulos",
            ]
        )
        if explicita:
            return True

        if not self.biblioteca.tiene_contenido():
            return False

        palabras_academicas = {
            "programacion", "python", "java", "poo", "objeto", "objetos", "clase",
            "clases", "herencia", "polimorfismo", "encapsulamiento", "abstraccion",
            "algoritmo", "algoritmos", "sql", "base", "datos", "redes", "subred",
            "subnetting", "ip", "servidor", "servidores", "ciberseguridad",
            "seguridad", "perifericos", "arquitectura", "computadores", "computador",
            "procesador", "memoria", "hardware", "software", "sistema", "operativo",
            "centro", "computo", "iot", "internet", "cosas", "firewall", "vlan",
            "tcp", "udp", "dns", "dhcp", "virtualizacion", "backup", "respaldo",
            "confidencialidad", "integridad", "disponibilidad", "amenaza",
            "vulnerabilidad", "riesgo", "criptografia", "autenticacion",
        }

        tokens = set(texto.split())
        if tokens & palabras_academicas:
            return True

        metadatos = self.biblioteca.palabras_metadatos()
        if len(tokens & metadatos) >= 1:
            return True

        return False

    def formatear_fuentes_academicas(self, resultados, maximo=4):
        bloques = []
        for i, r in enumerate(resultados[:maximo], 1):
            encabezado = (
                f"[APUNTE {i}] Ramo: {r.get('ramo') or 'Sin ramo'} | "
                f"Módulo: {r.get('modulo') or 'Sin módulo'} | "
                f"PDF: {r.get('documento','')} | página {r.get('pagina','')}"
            )
            texto = (r.get("texto") or "").strip()
            limite_texto = 360 if maximo <= ACADEMICO_FUENTES_BREVE else 560
            if len(texto) > limite_texto:
                texto = texto[:limite_texto].rsplit(" ", 1)[0] + "..."
            bloques.append(encabezado + "\nTexto: " + texto)
        return "\n\n".join(bloques)

    def limpiar_wake_academico(self, pregunta):
        """Quita alias de activación para analizar una continuación académica corta."""
        texto = normalizar(pregunta)
        palabras = texto.split()
        activaciones = {"beta", "veta", "meta", "metas", "petra"}
        # Whisper/Vosk puede dejar el alias al principio de la frase.
        while palabras and palabras[0] in activaciones:
            palabras.pop(0)
        return " ".join(palabras).strip()

    def corregir_seguimiento_academico_corto(self, pregunta):
        """Corrige solo órdenes académicas cortas con errores obvios de ASR.

        No pretende corregir dictado libre. Se activa únicamente cuando existe
        contexto académico y la frase es breve. Así evitamos transformar palabras
        normales del Señor por coincidencias accidentales.
        """
        texto = self.limpiar_wake_academico(pregunta)
        palabras = texto.split()
        if not palabras or len(palabras) > 10:
            return texto

        objetivos = {
            "profundiza": 0.72,
            "profundice": 0.76,
            "amplia": 0.76,
            "detalla": 0.76,
            "continua": 0.77,
            "resume": 0.78,
        }

        corregidas = []
        cambios = []
        for palabra in palabras:
            mejor = palabra
            mejor_score = 0.0
            mejor_objetivo = None
            if len(palabra) >= 5:
                for objetivo, umbral in objetivos.items():
                    score = difflib.SequenceMatcher(None, palabra, objetivo).ratio()
                    if score >= umbral and score > mejor_score:
                        mejor_score = score
                        mejor_objetivo = objetivo
            if mejor_objetivo and mejor_objetivo != palabra:
                mejor = mejor_objetivo
                cambios.append(f"{palabra}->{mejor_objetivo} ({mejor_score:.2f})")
            corregidas.append(mejor)

        corregido = " ".join(corregidas).strip()
        if cambios:
            print("SEGUIMIENTO ACADÉMICO: corrección ASR:", ", ".join(cambios))
            print(f"SEGUIMIENTO ACADÉMICO: interpretando '{texto}' como '{corregido}'")
        return corregido

    def es_pedido_academico_profundo(self, pregunta):
        texto = self.corregir_seguimiento_academico_corto(pregunta)
        marcadores = [
            "profundiza", "profundice", "mas a fondo", "en profundidad",
            "en detalle", "detalladamente", "explicacion completa",
            "explicame completo", "explicamelo completo", "desarrolla el tema",
            "desarrollame", "amplia la explicacion", "amplia el tema",
            "amplia", "detalla", "respuesta larga", "todos los detalles",
            "paso a paso completo",
        ]
        return any(m in texto for m in marcadores)

    def es_seguimiento_academico(self, pregunta):
        if not self.ultimo_contexto_academico:
            return False
        if time.time() - self.ultimo_contexto_academico_ts > BIBLIOTECA_CONTEXTO_SEGUNDOS:
            return False
        if self._hay_cambio_dominio_contextual(
            pregunta, self.ultimo_contexto_academico, "academico"
        ):
            return False

        texto = self.corregir_seguimiento_academico_corto(pregunta)
        marcadores = [
            "explicame mas", "dime mas", "cuentame mas", "profundiza",
            "profundice", "amplia", "detalla", "continua", "sigue",
            "dame un ejemplo", "ponme un ejemplo", "hazme un ejemplo",
            "otro ejemplo", "dame otro", "que significa eso", "por que",
            "como funciona eso", "y eso", "y despues", "cual es la diferencia",
            "puedes explicarlo mejor", "resumelo", "resume", "hazme un resumen",
            "preguntame sobre eso", "cuales son las tres", "cuales son los tres",
            "cuales son esas tres", "cuales son esas partes", "menciona las tres",
            "las tres partes", "los tres elementos", "esas partes", "esos elementos",
            "la primera", "la segunda", "la tercera", "el primero", "el segundo",
            "el tercero", "a que se refiere", "que quiere decir",
        ]
        if any(m in texto for m in marcadores):
            return True

        palabras = texto.split()
        referencias = {
            "eso", "esa", "ese", "esas", "esos", "esto", "estas", "estos",
            "primera", "segunda", "tercera", "primero", "segundo", "tercero",
            "partes", "elementos", "caracteristicas", "pasos", "tipos",
            "ejemplo", "ejemplos", "diferencia", "diferencias",
        }
        if len(palabras) <= 11 and referencias.intersection(palabras):
            return True

        # Si Daniela acaba de terminar una respuesta académica, aceptamos también
        # interrogaciones de continuación muy cortas. Las rutas de clima, Windows,
        # YouTube, memoria, etc. se evalúan antes de llegar aquí, por lo que esas
        # órdenes explícitas conservan prioridad.
        if self.ultimo_tipo_respuesta_terminada == "academico" and len(palabras) <= 8:
            inicios = {
                "que", "cual", "cuales", "como", "cuando", "donde", "por",
                "explica", "explicame", "dime", "menciona", "describe",
            }
            if palabras and palabras[0] in inicios:
                return True

        return False

    def consultar_biblioteca_async(
        self,
        pregunta,
        forzar=False,
        forzar_solo_local=False,
        decision=None,
    ):
        consulta = self.limpiar_consulta_academica(pregunta)
        if not consulta:
            self.responder("necesito saber qué desea consultar en sus apuntes.", "confundida")
            return

        respuesta_profunda = self.es_pedido_academico_profundo(pregunta)
        limite_fuentes_respuesta = (
            ACADEMICO_FUENTES_PROFUNDO if respuesta_profunda else ACADEMICO_FUENTES_BREVE
        )
        max_tokens_respuesta = (
            ACADEMICO_TOKENS_PROFUNDO if respuesta_profunda else ACADEMICO_TOKENS_BREVE
        )

        token = self.iniciar_proceso("biblioteca_academica")
        if token is None:
            self.responder("todavía estoy terminando la consulta anterior.", "pensando")
            return

        self.expresion_pensando()

        def trabajo():
            respuesta = None
            uso_streaming = False
            locales = []
            web = []
            error = ""
            try:
                inicio = time.perf_counter()
                # v2.8.3: una ruta académica solo puede recuperar documentos
                # clasificados como académicos. Si el router ya identificó un
                # ramo, lo usamos también como preferencia para evitar que un
                # libro técnico con una mención incidental contamine el prompt.
                ramo_decision = (decision or {}).get("ramo", "") if decision else ""
                locales = self.biblioteca.buscar(
                    consulta,
                    limite=BIBLIOTECA_RESULTADOS,
                    ramo_preferido=ramo_decision,
                    categoria_preferida="academica",
                )
                print(
                    f"LATENCIA BIBLIOTECA: {time.perf_counter() - inicio:.2f} s"
                )
                if decision:
                    print(
                        "FUENTES ACADÉMICAS ESTRICTAS: "
                        f"categoria='academica' ramo='{ramo_decision or 'todos'}'"
                    )

                locales_utiles = [
                    r for r in locales if float(r.get("score", 0)) >= BIBLIOTECA_UMBRAL_MIN
                ]
                top_score = float(locales[0].get("score", 0)) if locales else 0.0
                local_fuerte = (
                    top_score >= BIBLIOTECA_UMBRAL_FUERTE
                    or len([r for r in locales if r.get("score", 0) >= 0.33]) >= 2
                )

                texto_n = normalizar(pregunta)
                pide_web = any(
                    m in texto_n
                    for m in [
                        "complementa con internet", "complementalo con internet",
                        "ademas busca en internet", "tambien busca en internet",
                    ]
                )
                pide_solo_local = forzar_solo_local or any(
                    m in texto_n
                    for m in [
                        "solo mis apuntes", "solo en mis apuntes",
                        "sin internet", "no uses internet",
                    ]
                )

                modo = "solo_local" if pide_solo_local else self.modo_biblioteca_academica

                # v2.8.3: si el enrutador inteligente ya encontró evidencia
                # académica alta (o media respaldada por varios fragmentos
                # locales), no salimos a Internet automáticamente. Una petición
                # explícita como "complementa con Internet" siempre conserva
                # prioridad. Las consultas manuales sin decisión del router
                # mantienen la configuración histórica de la biblioteca.
                decision_ruta = (decision or {}).get("ruta", "") if decision else ""
                decision_confianza = (decision or {}).get("confianza", "") if decision else ""
                try:
                    decision_score_a = float((decision or {}).get("score_academica", 0) or 0)
                except Exception:
                    decision_score_a = 0.0

                evidencia_local_suficiente = bool(
                    decision_ruta == "academica"
                    and (
                        decision_confianza == "alta"
                        or (decision_confianza == "media" and local_fuerte)
                    )
                    and decision_score_a > 0
                )

                if pide_solo_local:
                    usar_web = False
                elif pide_web:
                    usar_web = True
                elif evidencia_local_suficiente:
                    usar_web = False
                    print(
                        "INTERNET ACADÉMICO: omitido por evidencia local suficiente "
                        f"(confianza={decision_confianza}, scoreA={decision_score_a:.3f})."
                    )
                else:
                    usar_web = (
                        modo == "siempre"
                        or (modo == "si_falta" and not local_fuerte)
                    )

                if usar_web:
                    try:
                        inicio_web = time.perf_counter()
                        web = self.buscar_internet_ddgs(consulta)[:3]
                        print(
                            f"LATENCIA COMPLEMENTO WEB ACADÉMICO: "
                            f"{time.perf_counter() - inicio_web:.2f} s"
                        )
                    except Exception as web_error:
                        print("BIBLIOTECA: complemento web no disponible:", web_error)

                if not locales_utiles and not web:
                    respuesta = (
                        "Señor, no encontré información suficientemente relacionada "
                        "en sus apuntes"
                    )
                    if modo != "solo_local":
                        respuesta += " ni pude obtener un complemento útil de Internet"
                    respuesta += "."
                else:
                    contexto_local = self.formatear_fuentes_academicas(locales_utiles, limite_fuentes_respuesta)
                    contexto_web = self.formatear_resultados_web(web[:3]) if web else ""

                    estilo_aprendido = self.preferencias_aprendidas_para_prompt()
                    instrucciones = (
                        "Eres Beta, tutora académica del Señor. Responde solo en español y para voz. "
                        "Prioriza APUNTES LOCALES; no inventes ni atribuyas a los apuntes datos ausentes. "
                        "Si usas Internet, di claramente que es complemento externo. "
                        "Corrige solo errores OCR obvios y parafrasea texto dañado. "
                        "Sin Markdown, tablas, asteriscos, URLs ni razonamiento interno. "
                        + (
                            "Modo profundo: explica de forma pedagógica en unas 130 a 170 palabras. "
                            if respuesta_profunda
                            else "Modo breve: responde directamente en 1 a 3 frases y unas 40 a 55 palabras. "
                        )
                        + "Empieza por la respuesta útil. Termina siempre una oración completa; "
                          "no abras una idea nueva si no podrás cerrarla dentro del límite. "
                          "Puedes dar ejemplos propios, identificándolos como ejemplos."
                        + (f" Adapta discretamente el estilo a estas preferencias confirmadas: {estilo_aprendido[:220]}." if estilo_aprendido else "")
                    )

                    contenido = (
                        f"Pregunta del Señor: {consulta}\n\n"
                        f"APUNTES LOCALES RECUPERADOS:\n"
                        f"{contexto_local or 'No hubo fragmentos locales suficientemente relevantes.'}\n\n"
                    )
                    if contexto_web:
                        contenido += (
                            "COMPLEMENTO EXTERNO DE INTERNET:\n"
                            + contexto_web
                            + "\n\n"
                        )
                    contenido += (
                        "Responde ahora. Si aporta valor, menciona solo un PDF y una página principal."
                    )

                    mensajes_academicos = [
                        {"role": "system", "content": instrucciones},
                        {"role": "user", "content": contenido},
                    ]
                    if STREAMING_OLLAMA_ACTIVO:
                        respuesta = self.generar_y_hablar_ollama_streaming(
                            mensajes_academicos,
                            "academico",
                            token,
                            temperatura=0.12,
                            num_predict=max_tokens_respuesta,
                            num_ctx=(ACADEMICO_NUM_CTX_PROFUNDO if respuesta_profunda else ACADEMICO_NUM_CTX_BREVE),
                        )
                        uso_streaming = bool(respuesta)
                    else:
                        respuesta = self.enviar_ollama(
                            mensajes_academicos,
                            temperatura=0.12,
                            num_predict=max_tokens_respuesta,
                            num_ctx=(ACADEMICO_NUM_CTX_PROFUNDO if respuesta_profunda else ACADEMICO_NUM_CTX_BREVE),
                        )
                        if respuesta:
                            respuesta = self.limpiar_respuesta_ollama(respuesta)

                self.ultimas_fuentes_academicas = locales_utiles[:limite_fuentes_respuesta]
                self.ultimo_contexto_tecnico_ts = 0.0
                if web:
                    self.ultimas_fuentes_web = web
                ramo_base = ((decision or {}).get("ramo") or "").strip() if decision else ""
                if not ramo_base and locales_utiles:
                    ramo_base = (locales_utiles[0].get("ramo") or "").strip()
                self.ultimo_contexto_academico = {
                    # tema_base no se concatena indefinidamente: sirve como ancla
                    # para cada pregunta de seguimiento y evita deriva semántica.
                    "tema_base": consulta,
                    "ramo_base": ramo_base,
                    "consulta": consulta,
                    "ultima_consulta": consulta,
                    "locales": locales_utiles[:limite_fuentes_respuesta],
                    "web": web[:3],
                    "respuesta": respuesta or "",
                }
                self.ultimo_contexto_academico_ts = time.time()
                if ramo_base or consulta:
                    self.registrar_exposicion_academica(
                        ramo_base or "General",
                        self.inferir_tema_academico(consulta, ramo_base),
                        "Consulta académica basada en apuntes",
                    )

                print(
                    "MODO TUTOR ACADÉMICO:",
                    "PROFUNDO" if respuesta_profunda else "BREVE",
                )
                print(
                    f"BIBLIOTECA ACADÉMICA ESTRICTA: consulta='{consulta}' "
                    f"ramo='{ramo_base or 'todos'}' top_score={top_score:.3f} "
                    f"locales={len(locales_utiles)} web={len(web)}"
                )
                for i, r in enumerate(locales_utiles[:5], 1):
                    print(
                        f"  APUNTE {i}: {r.get('documento')} pág. {r.get('pagina')} "
                        f"score={r.get('score',0):.3f}"
                    )

            except Exception as exc:
                error = str(exc)
                print("ERROR BIBLIOTECA ACADÉMICA:", exc)
            finally:
                self.terminar_proceso(token)

            if token != self.proceso_id:
                return

            if respuesta and not uso_streaming:
                self.root.after(0, lambda r=respuesta: self.responder(r, "hablando", "academico"))
            elif not respuesta:
                if "pip install" in error:
                    mensaje = (
                        "para estudiar sus PDF me faltan componentes locales. "
                        "Instale PyMuPDF, Sentence Transformers y NumPy y vuelva a intentarlo."
                    )
                else:
                    mensaje = "no pude consultar la biblioteca académica en este momento."
                self.root.after(0, lambda m=mensaje: self.responder(m, "confundida"))

        threading.Thread(target=trabajo, daemon=True).start()

    def conversar_contexto_academico_async(self, pregunta):
        contexto = self.ultimo_contexto_academico
        if not contexto:
            self.consultar_biblioteca_async(pregunta, forzar=True)
            return

        # Normalizamos únicamente comandos cortos de seguimiento. Por ejemplo,
        # si Whisper entrega "perfumdiza", Beta lo interpreta como "profundiza"
        # y mantiene la consulta dentro de los apuntes locales.
        pregunta_interpretada = self.corregir_seguimiento_academico_corto(pregunta)
        if not pregunta_interpretada:
            pregunta_interpretada = pregunta

        respuesta_profunda = self.es_pedido_academico_profundo(pregunta_interpretada)
        limite_fuentes = (
            ACADEMICO_FUENTES_PROFUNDO if respuesta_profunda else ACADEMICO_FUENTES_BREVE
        )
        max_tokens = (
            ACADEMICO_TOKENS_PROFUNDO if respuesta_profunda else ACADEMICO_TOKENS_BREVE
        )

        token = self.iniciar_proceso("contexto_academico")
        if token is None:
            self.responder("todavía estoy terminando la respuesta anterior.", "pensando")
            return

        self.expresion_pensando()

        def trabajo():
            respuesta = None
            uso_streaming = False
            try:
                # v2.5.4: TODA continuación académica vuelve a consultar la biblioteca.
                # Usamos un tema base estable + la pregunta actual, en vez de concatenar
                # todas las preguntas anteriores; así evitamos deriva semántica.
                tema_base = (
                    contexto.get("tema_base")
                    or contexto.get("consulta")
                    or ""
                ).strip()
                consulta_expandida = f"{tema_base} {pregunta_interpretada}".strip()
                ramo_base = (contexto.get("ramo_base") or "").strip()
                inicio_busqueda = time.perf_counter()
                nuevos = self.biblioteca.buscar(
                    consulta_expandida,
                    limite=BIBLIOTECA_RESULTADOS,
                    ramo_preferido=ramo_base,
                    categoria_preferida="academica",
                )
                print(
                    f"LATENCIA BIBLIOTECA SEGUIMIENTO: "
                    f"{time.perf_counter() - inicio_busqueda:.2f} s"
                )
                nuevos_utiles = [
                    r for r in nuevos
                    if float(r.get("score", 0)) >= BIBLIOTECA_UMBRAL_MIN
                ]
                top_seguimiento = float(nuevos[0].get("score", 0)) if nuevos else 0.0
                print(
                    f"BIBLIOTECA SEGUIMIENTO: ramo='{ramo_base or 'todos'}' "
                    f"tema='{tema_base}' pregunta='{pregunta_interpretada}' "
                    f"top_score={top_seguimiento:.3f} locales={len(nuevos_utiles)}"
                )
                for i, r in enumerate(nuevos_utiles[:3], 1):
                    print(
                        f"  SEGUIMIENTO {i}: {r.get('documento')} pág. {r.get('pagina')} "
                        f"score={r.get('score',0):.3f}"
                    )

                locales = nuevos_utiles[:limite_fuentes] or (contexto.get("locales") or [])[:limite_fuentes]
                web = contexto.get("web") or []
                fuentes_locales = self.formatear_fuentes_academicas(locales, limite_fuentes)
                fuentes_web = self.formatear_resultados_web(web[:3]) if web else ""

                estilo_aprendido = self.preferencias_aprendidas_para_prompt()
                instrucciones = (
                    "Eres Beta, tutora académica del Señor. Continúa el tema usando primero los "
                    "APUNTES RECUPERADOS PARA ESTA PREGUNTA. No inventes ni extrapoles como si fuera "
                    "contenido institucional. Responde solo en español y para voz, sin Markdown. "
                    "Corrige solo OCR obvio. "
                    + (
                        "Modo profundo: desarrolla en unas 130 a 170 palabras. "
                        if respuesta_profunda
                        else "Modo breve: responde en 1 a 3 frases y unas 40 a 55 palabras. "
                    )
                    + "Termina siempre una oración completa y no abras una idea que no puedas cerrar."
                    + (f" Adapta discretamente el estilo a estas preferencias confirmadas: {estilo_aprendido[:220]}." if estilo_aprendido else "")
                )

                mensajes = [
                    {"role": "system", "content": instrucciones},
                    {
                        "role": "user",
                        "content": (
                            f"Tema base: {tema_base}\n"
                            f"Respuesta anterior (contexto breve): {contexto.get('respuesta','')[:420]}\n\n"
                            f"APUNTES RECUPERADOS PARA ESTA PREGUNTA:\n{fuentes_locales}\n\n"
                            f"INTERNET (solo si ya existía como complemento):\n{fuentes_web}\n\n"
                            f"Pregunta de seguimiento interpretada: {pregunta_interpretada}"
                        ),
                    },
                ]
                if STREAMING_OLLAMA_ACTIVO:
                    respuesta = self.generar_y_hablar_ollama_streaming(
                        mensajes,
                        "academico",
                        token,
                        temperatura=0.12,
                        num_predict=max_tokens,
                        num_ctx=(ACADEMICO_NUM_CTX_PROFUNDO if respuesta_profunda else ACADEMICO_NUM_CTX_BREVE),
                    )
                    uso_streaming = bool(respuesta)
                else:
                    respuesta = self.enviar_ollama(
                        mensajes,
                        temperatura=0.12,
                        num_predict=max_tokens,
                        num_ctx=(ACADEMICO_NUM_CTX_PROFUNDO if respuesta_profunda else ACADEMICO_NUM_CTX_BREVE),
                    )
                    if respuesta:
                        respuesta = self.limpiar_respuesta_ollama(respuesta)
                if respuesta:
                    contexto["respuesta"] = respuesta
                    contexto["locales"] = locales
                    contexto["tema_base"] = tema_base
                    contexto["ramo_base"] = ramo_base or (
                        (locales[0].get("ramo") or "").strip() if locales else ""
                    )
                    contexto["ultima_consulta"] = consulta_expandida
                    # consulta conserva el tema base para compatibilidad con el resto de Beta.
                    contexto["consulta"] = tema_base
                    self.ultimo_contexto_academico_ts = time.time()
                    self.ultimas_fuentes_academicas = locales
                    ramo_progreso = contexto.get("ramo_base") or ramo_base or "General"
                    tema_progreso = self.inferir_tema_academico(pregunta_interpretada, ramo_progreso)
                    if normalizar(tema_progreso) in {"profundiza", "profundice", "dame un ejemplo", "ejemplo"}:
                        tema_progreso = self.inferir_tema_academico(tema_base, ramo_progreso)
                    self.registrar_exposicion_academica(
                        ramo_progreso, tema_progreso, "Seguimiento académico basado en apuntes"
                    )
            except Exception as error:
                print("ERROR CONTEXTO ACADÉMICO:", error)
            finally:
                self.terminar_proceso(token)

            if token != self.proceso_id:
                return
            if respuesta and not uso_streaming:
                self.root.after(0, lambda r=respuesta: self.responder(r, "hablando", "academico"))
            elif not respuesta:
                self.root.after(
                    0,
                    lambda: self.responder(
                        "no pude continuar esa explicación académica.", "confundida"
                    ),
                )

        threading.Thread(target=trabajo, daemon=True).start()

    def manejar_comando_fuentes_academicas(self, texto):
        texto = normalizar(texto)
        if (
            "de donde sacaste eso" in texto
            and self.ultimo_tipo_respuesta_terminada == "tecnico"
        ):
            return False
        marcadores = [
            "muestrame las fuentes academicas",
            "muestra las fuentes academicas",
            "ver fuentes academicas",
            "fuentes de mis apuntes",
            "de que apunte sacaste eso",
            "de donde sacaste eso",
        ]
        if not any(m in texto for m in marcadores):
            return False

        if not self.ultimas_fuentes_academicas:
            self.responder(
                "todavía no tengo fuentes académicas de una consulta reciente.",
                "confundida",
            )
            return True

        self.root.after(0, self.ventana_fuentes_academicas)
        self.responder(
            "le muestro los documentos y páginas que utilicé.",
            "feliz",
        )
        return True

    def ventana_fuentes_academicas(self):
        if not self.ultimas_fuentes_academicas:
            messagebox.showinfo(
                "Fuentes académicas",
                "Beta todavía no tiene fuentes académicas de una consulta reciente.",
                parent=self.root,
            )
            return

        ventana = tk.Toplevel(self.root)
        ventana.title("Fuentes académicas utilizadas por Beta")
        ventana.geometry("1050x500")
        ventana.attributes("-topmost", True)

        ttk.Label(
            ventana,
            text=(
                "Estas son las páginas de sus PDF que Beta recuperó para la última respuesta. "
                "Doble clic para abrir el documento."
            ),
            wraplength=990,
        ).pack(anchor="w", padx=12, pady=(12, 8))

        tabla = ttk.Treeview(
            ventana,
            columns=("n", "ramo", "modulo", "documento", "pagina", "relevancia", "ruta"),
            show="headings",
        )
        for clave, titulo in [
            ("n", "#"),
            ("ramo", "Ramo"),
            ("modulo", "Módulo"),
            ("documento", "PDF"),
            ("pagina", "Página"),
            ("relevancia", "Relevancia"),
            ("ruta", "Ruta"),
        ]:
            tabla.heading(clave, text=titulo)

        tabla.column("n", width=35, anchor="center")
        tabla.column("ramo", width=180)
        tabla.column("modulo", width=110)
        tabla.column("documento", width=300)
        tabla.column("pagina", width=65, anchor="center")
        tabla.column("relevancia", width=85, anchor="center")
        tabla.column("ruta", width=250)
        tabla.pack(fill="both", expand=True, padx=12, pady=(0, 10))

        for i, r in enumerate(self.ultimas_fuentes_academicas, 1):
            tabla.insert(
                "",
                "end",
                values=(
                    i,
                    r.get("ramo", ""),
                    r.get("modulo", ""),
                    r.get("documento", ""),
                    r.get("pagina", ""),
                    f"{r.get('score',0):.3f}",
                    r.get("ruta", ""),
                ),
            )

        def abrir(_event=None):
            seleccion = tabla.selection()
            if not seleccion:
                return
            valores = tabla.item(seleccion[0]).get("values", [])
            if len(valores) >= 7:
                ruta = str(valores[6])
                if Path(ruta).exists():
                    try:
                        os.startfile(ruta)
                    except Exception as error:
                        messagebox.showerror(
                            "Fuentes académicas",
                            f"No pude abrir el PDF:\n{error}",
                            parent=ventana,
                        )

        tabla.bind("<Double-1>", abrir)
        ttk.Button(
            ventana,
            text="Abrir PDF seleccionado",
            command=abrir,
        ).pack(pady=(0, 12))

    def enviar_ollama(self, mensajes, temperatura=0.18, num_predict=240, num_ctx=None):
        datos = {
            "model": OLLAMA_MODEL,
            "messages": mensajes,
            "stream": False,
            "options": {
                "temperature": temperatura,
                "top_p": 0.80,
                "repeat_penalty": 1.08,
                "num_predict": num_predict,
                "num_ctx": int(num_ctx or OLLAMA_NUM_CTX),
            },
            "keep_alive": OLLAMA_KEEP_ALIVE,
        }

        def hacer_peticion(payload):
            cuerpo = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            solicitud = urllib.request.Request(
                OLLAMA_URL,
                data=cuerpo,
                headers={"Content-Type": "application/json; charset=utf-8"},
                method="POST",
            )

            with urllib.request.urlopen(solicitud, timeout=OLLAMA_TIMEOUT) as respuesta_http:
                contenido = respuesta_http.read().decode("utf-8")

            resultado = json.loads(contenido)

            # Solo usamos el contenido final devuelto por el modelo Instruct.
            mensaje = resultado.get("message", {})
            return mensaje.get("content", "").strip()

        try:
            return hacer_peticion(datos)

        except urllib.error.HTTPError as error:
            print("ERROR HTTP OLLAMA:", error)
            try:
                detalle = error.read().decode("utf-8", errors="replace")
                if detalle:
                    print("DETALLE OLLAMA:", detalle)
            except Exception:
                pass
            return None

        except urllib.error.URLError as error:
            print("ERROR CON OLLAMA:", error)
            return None

        except Exception as error:
            print("ERROR CONSULTANDO OLLAMA:", error)
            return None

    def extraer_fragmentos_streaming(self, buffer, forzar=False):
        """Separa texto incremental en frases naturales para la voz.

        El objetivo no es trocear cada token, sino entregar a Daniela unidades
        suficientemente largas para sonar fluidas y suficientemente cortas para
        empezar a hablar antes de que Qwen termine toda la respuesta.
        """
        texto = (buffer or "").replace("\r", " ")
        listos = []

        while texto.strip():
            corte = None
            for coincidencia in re.finditer(r'(?<=[.!?])(?:["”»])?\s+', texto):
                candidato = texto[:coincidencia.end()].strip()
                if len(candidato) >= STREAMING_MIN_CARACTERES_FRASE:
                    corte = coincidencia.end()
                    break

            # En versiones anteriores permitíamos cortar en comas para ganar algunos
            # segundos. Eso podía dejar la última locución suspendida si Qwen agotaba
            # el límite después de ese corte. v2.5.3 prioriza frases completas.
            if (
                STREAMING_CORTE_INTERMEDIO
                and corte is None
                and len(texto) >= STREAMING_CORTE_LARGO
            ):
                limite = min(len(texto), STREAMING_CORTE_LARGO)
                zona = texto[:limite]
                candidatos = [zona.rfind(", "), zona.rfind("; "), zona.rfind(": ")]
                pos = max(candidatos)
                if pos >= 90:
                    corte = pos + 1

            if corte is None:
                break

            fragmento = texto[:corte].strip()
            texto = texto[corte:].lstrip()
            if fragmento:
                listos.append(fragmento)

        if forzar and texto.strip():
            listos.append(texto.strip())
            texto = ""

        return listos, texto

    def enviar_ollama_streaming(
        self,
        mensajes,
        temperatura=0.16,
        num_predict=180,
        on_fragment=None,
        token_proceso=None,
        num_ctx=None,
    ):
        """Consulta Ollama por NDJSON y entrega frases a medida que se generan."""
        datos = {
            "model": OLLAMA_MODEL,
            "messages": mensajes,
            "stream": True,
            "options": {
                "temperature": temperatura,
                "top_p": 0.80,
                "repeat_penalty": 1.08,
                "num_predict": num_predict,
                "num_ctx": int(num_ctx or OLLAMA_NUM_CTX),
            },
            "keep_alive": OLLAMA_KEEP_ALIVE,
        }

        cuerpo = json.dumps(datos, ensure_ascii=False).encode("utf-8")
        solicitud = urllib.request.Request(
            OLLAMA_URL,
            data=cuerpo,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST",
        )

        texto_total = ""
        buffer = ""
        inicio = time.perf_counter()
        primer_token = False

        try:
            with urllib.request.urlopen(solicitud, timeout=OLLAMA_TIMEOUT) as respuesta_http:
                for linea in respuesta_http:
                    if token_proceso is not None and token_proceso != self.proceso_id:
                        print("STREAMING OLLAMA: respuesta cancelada por cambio de proceso.")
                        return None

                    linea = linea.decode("utf-8", errors="replace").strip()
                    if not linea:
                        continue

                    try:
                        evento = json.loads(linea)
                    except json.JSONDecodeError:
                        continue

                    pieza = ((evento.get("message") or {}).get("content") or "")
                    if pieza:
                        if not primer_token:
                            primer_token = True
                            print(
                                f"LATENCIA OLLAMA HASTA PRIMER TOKEN: "
                                f"{time.perf_counter() - inicio:.2f} s"
                            )
                        texto_total += pieza
                        buffer += pieza
                        fragmentos, buffer = self.extraer_fragmentos_streaming(buffer)
                        if on_fragment:
                            for fragmento in fragmentos:
                                on_fragment(fragmento)

                    if evento.get("done"):
                        break

            # Cierre seguro: emitimos únicamente oraciones completas. Si Qwen alcanza
            # num_predict a mitad de una idea, la cola incompleta NO se manda a Daniela.
            fragmentos, resto = self.extraer_fragmentos_streaming(buffer, forzar=False)
            if on_fragment:
                for fragmento in fragmentos:
                    on_fragment(fragmento)

            resto = (resto or "").strip()
            if resto:
                if re.search(r'[.!?][\"”»]?\s*$', resto):
                    if on_fragment:
                        on_fragment(resto)
                elif STREAMING_DESCARTAR_COLA_INCOMPLETA:
                    print(
                        "CIERRE STREAMING SEGURO: cola incompleta descartada para no "
                        f"cortar una oración ({len(resto)} caracteres)."
                    )
                else:
                    if on_fragment:
                        on_fragment(resto.rstrip(" ,;:") + ".")

            print(f"LATENCIA OLLAMA GENERACIÓN COMPLETA: {time.perf_counter() - inicio:.2f} s")
            return texto_total.strip()

        except urllib.error.HTTPError as error:
            print("ERROR HTTP OLLAMA STREAMING:", error)
            try:
                detalle = error.read().decode("utf-8", errors="replace")
                if detalle:
                    print("DETALLE OLLAMA STREAMING:", detalle)
            except Exception:
                pass
            return None
        except urllib.error.URLError as error:
            print("ERROR CON OLLAMA STREAMING:", error)
            return None
        except Exception as error:
            print("ERROR CONSULTANDO OLLAMA STREAMING:", error)
            return None

    def generar_wav_daniela_streaming(self, texto):
        """Sintetiza un fragmento sin reproducirlo todavía.

        En streaming, un hilo puede preparar el siguiente WAV mientras otro hilo
        reproduce el anterior. Así se reducen las pausas entre frases.
        """
        texto_voz = self.preparar_texto_para_voz(texto)
        if not texto_voz or not PIPER_MODELO.exists():
            return None, texto_voz

        ruta_wav = None
        try:
            fd, nombre_wav = tempfile.mkstemp(prefix="beta_stream_", suffix=".wav")
            os.close(fd)
            ruta_wav = Path(nombre_wav)

            if self.piper_listo and self.piper_voice is not None:
                inicio = time.perf_counter()
                with self.piper_lock:
                    with wave.open(str(ruta_wav), "wb") as wav_file:
                        self.piper_voice.synthesize_wav(texto_voz, wav_file)
                print(
                    f"LATENCIA PIPER STREAM (síntesis): "
                    f"{time.perf_counter() - inicio:.2f} s"
                )
            else:
                inicio = time.perf_counter()
                comando = [
                    sys.executable, "-m", "piper",
                    "-m", str(PIPER_MODELO),
                    "-f", str(ruta_wav),
                    "--", texto_voz,
                ]
                resultado = subprocess.run(
                    comando,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    check=False,
                )
                print(
                    f"LATENCIA PIPER STREAM (CLI): "
                    f"{time.perf_counter() - inicio:.2f} s"
                )
                if resultado.returncode != 0:
                    if resultado.stderr.strip():
                        print("ERROR PIPER STREAM:", resultado.stderr.strip())
                    ruta_wav.unlink(missing_ok=True)
                    return None, texto_voz

            if not ruta_wav.exists() or ruta_wav.stat().st_size < 100:
                ruta_wav.unlink(missing_ok=True)
                return None, texto_voz

            return ruta_wav, texto_voz
        except Exception as error:
            print("ERROR SINTETIZANDO PIPER STREAM:", error)
            if ruta_wav is not None:
                try:
                    ruta_wav.unlink(missing_ok=True)
                except Exception:
                    pass
            return None, texto_voz

    def reproducir_wav_daniela_streaming(self, ruta_wav, texto_respaldo=""):
        """Reproduce un WAV ya sintetizado y sincroniza la boca."""
        if ruta_wav is None:
            if texto_respaldo:
                self.reproducir_voz_windows_respaldo(texto_respaldo)
                return True
            return False

        try:
            intervalo_ms = 45
            niveles = self.analizar_wav_para_boca(ruta_wav, intervalo_ms)
            evento_visual_listo = threading.Event()
            try:
                self.root.after(
                    0,
                    lambda: self.preparar_sincronizacion_boca(
                        niveles,
                        intervalo_ms,
                        evento_visual_listo,
                    ),
                )
                evento_visual_listo.wait(timeout=0.40)
            except Exception:
                pass

            winsound.PlaySound(None, winsound.SND_PURGE)
            winsound.PlaySound(str(ruta_wav), winsound.SND_FILENAME)
            try:
                self.root.after(0, self.detener_sincronizacion_boca)
            except Exception:
                pass
            return True
        except Exception as error:
            print("ERROR REPRODUCIENDO WAV STREAM:", error)
            if texto_respaldo:
                self.reproducir_voz_windows_respaldo(texto_respaldo)
                return True
            return False
        finally:
            try:
                ruta_wav.unlink(missing_ok=True)
            except Exception:
                pass

    def iniciar_pipeline_respuesta_streaming(self, tipo_contexto="general", expresion_final="hablando"):
        """Crea el pipeline Qwen -> Piper -> audio para una sola respuesta."""
        self.respuesta_actual_id += 1
        respuesta_id = self.respuesta_actual_id
        self.respuesta_tipo_por_id[respuesta_id] = tipo_contexto or "general"

        sesion = {
            "id": respuesta_id,
            "tipo": tipo_contexto or "general",
            "expresion_final": expresion_final,
            "cola_texto": queue.Queue(),
            "cola_wav": queue.Queue(),
            "partes": [],
            "primer_fragmento": True,
            "texto_final": "",
            "cancelar_finalizacion": False,
            "inicio_peticion": self.ultima_frase_inicio or time.perf_counter(),
        }

        # Mientras Qwen todavía genera la primera frase, el micrófono sigue activo
        # para que el Señor pueda decir "Beta, deja de pensar" y cancelar.
        # self.hablando pasa a True justo cuando empieza el primer audio.
        try:
            self.root.after(0, lambda: self.cambiar_expresion("pensando"))
        except Exception:
            pass

        def sintetizador():
            while True:
                fragmento = sesion["cola_texto"].get()
                if fragmento is None:
                    break
                ruta, texto_voz = self.generar_wav_daniela_streaming(fragmento)
                sesion["cola_wav"].put((ruta, texto_voz))
            sesion["cola_wav"].put(None)

        def reproductor():
            primer_audio = True
            while True:
                item = sesion["cola_wav"].get()
                if item is None:
                    break
                ruta, texto_voz = item
                if primer_audio:
                    primer_audio = False
                    self.hablando = True
                    inicio_peticion = sesion.get("inicio_peticion")
                    if inicio_peticion:
                        print(
                            f"LATENCIA HASTA PRIMER AUDIO: "
                            f"{time.perf_counter() - inicio_peticion:.2f} s"
                        )
                self.reproducir_wav_daniela_streaming(ruta, texto_voz)

            self.hablando = False
            if sesion["cancelar_finalizacion"]:
                return

            texto_final = (sesion.get("texto_final") or " ".join(sesion["partes"])).strip()
            if texto_final:
                try:
                    self.root.after(
                        0,
                        lambda t=texto_final, sid=respuesta_id, exp=expresion_final: self.finalizar_respuesta_streaming(
                            t, sid, exp
                        ),
                    )
                except tk.TclError:
                    pass

        threading.Thread(target=sintetizador, daemon=True).start()
        threading.Thread(target=reproductor, daemon=True).start()
        return sesion

    def encolar_fragmento_streaming(self, sesion, fragmento):
        fragmento = self.limpiar_respuesta_ollama((fragmento or "").strip())
        if not fragmento:
            return

        if sesion.get("primer_fragmento"):
            sesion["primer_fragmento"] = False
            n = normalizar(fragmento)
            primeras = " ".join(n.split()[:6])
            if "senor" not in primeras:
                fragmento = (
                    "Señor, " + fragmento[0].lower() + fragmento[1:]
                    if len(fragmento) > 1
                    else "Señor, " + fragmento
                )
            inicio_peticion = sesion.get("inicio_peticion")
            if inicio_peticion:
                print(
                    f"LATENCIA HASTA PRIMERA FRASE LISTA: "
                    f"{time.perf_counter() - inicio_peticion:.2f} s"
                )

        sesion["partes"].append(fragmento)
        sesion["cola_texto"].put(fragmento)

    def cerrar_pipeline_respuesta_streaming(self, sesion, cancelar=False):
        sesion["cancelar_finalizacion"] = bool(cancelar)
        sesion["texto_final"] = " ".join(sesion.get("partes") or []).strip()
        inicio_peticion = sesion.get("inicio_peticion")
        if inicio_peticion:
            print(
                f"LATENCIA HASTA GENERACIÓN COMPLETA: "
                f"{time.perf_counter() - inicio_peticion:.2f} s"
            )
        # Una vez terminada la generación bloqueamos el micrófono mientras Piper
        # termina de preparar/reproducir los fragmentos pendientes.
        if not cancelar and sesion.get("partes"):
            self.hablando = True
        self.ultima_frase_inicio = 0.0
        sesion["cola_texto"].put(None)

    def finalizar_respuesta_streaming(self, texto, respuesta_id, expresion_final):
        """Guarda y cierra una respuesta que ya fue pronunciada por el pipeline."""
        texto = (texto or "").strip()
        if not texto:
            return

        print("RESPUESTA FINAL DE BETA [STREAMING]:", texto)
        self.memoria.guardar_conversacion("Beta", texto)
        self.ultima_respuesta_beta = texto
        self.actualizar_contexto_turno("Beta", texto)
        self.programar_memoria_inteligente(self.ultimo_mensaje_usuario, texto)

        if "?" in texto and self.modo_escucha == "conversacion":
            self.renovar_modo_conversacion()

        self.finalizar_respuesta(respuesta_id, expresion_final)

    def generar_y_hablar_ollama_streaming(
        self,
        mensajes,
        tipo_contexto,
        token_proceso,
        temperatura,
        num_predict,
        num_ctx=None,
    ):
        """Genera y habla en paralelo. Devuelve el texto completo ya encolado."""
        sesion = self.iniciar_pipeline_respuesta_streaming(tipo_contexto, "hablando")
        respuesta = self.enviar_ollama_streaming(
            mensajes,
            temperatura=temperatura,
            num_predict=num_predict,
            on_fragment=lambda frag: self.encolar_fragmento_streaming(sesion, frag),
            token_proceso=token_proceso,
            num_ctx=num_ctx,
        )

        if not respuesta or not sesion.get("partes"):
            self.cerrar_pipeline_respuesta_streaming(sesion, cancelar=True)
            return None

        self.cerrar_pipeline_respuesta_streaming(sesion, cancelar=False)
        return sesion.get("texto_final") or " ".join(sesion.get("partes") or [])

    def calentar_ollama_en_segundo_plano(self):
        """Carga Qwen en memoria antes de la primera conversación real."""
        def trabajo():
            inicio = time.perf_counter()
            try:
                datos = {
                    "model": OLLAMA_MODEL,
                    "messages": [
                        {"role": "system", "content": "Responde solo en español."},
                        {"role": "user", "content": "Responde únicamente: listo"},
                    ],
                    "stream": False,
                    "options": {"temperature": 0, "num_predict": 4, "num_ctx": ACADEMICO_NUM_CTX_BREVE},
                    "keep_alive": OLLAMA_KEEP_ALIVE,
                }
                cuerpo = json.dumps(datos, ensure_ascii=False).encode("utf-8")
                solicitud = urllib.request.Request(
                    OLLAMA_URL, data=cuerpo,
                    headers={"Content-Type": "application/json; charset=utf-8"},
                    method="POST",
                )
                with urllib.request.urlopen(solicitud, timeout=30) as respuesta_http:
                    respuesta_http.read()
                print(f"OLLAMA PRECALENTADO en {time.perf_counter() - inicio:.2f} s")
            except Exception as error:
                print("OLLAMA: no se pudo precalentar (no es fatal):", error)

        threading.Thread(target=trabajo, daemon=True).start()

    def limpiar_respuesta_ollama(self, texto):
        if not texto:
            return ""

        # Eliminar bloques de pensamiento etiquetados.
        texto = re.sub(
            r"<think>.*?</think>",
            "",
            texto,
            flags=re.DOTALL | re.IGNORECASE,
        )
        texto = re.sub(
            r"<analysis>.*?</analysis>",
            "",
            texto,
            flags=re.DOTALL | re.IGNORECASE,
        )
        texto = texto.replace("<think>", "").replace("</think>", "")
        texto = texto.replace("<analysis>", "").replace("</analysis>", "")

        lineas = [linea.strip() for linea in texto.splitlines() if linea.strip()]
        filtradas = []

        prefijos_internos = (
            "we need",
            "the user",
            "i need",
            "i should",
            "let me",
            "thinking",
            "analysis:",
            "reasoning:",
            "assistant should",
            "the answer",
            "final answer:",
            "response:",
        )

        for linea in lineas:
            linea_minuscula = linea.lower()
            if any(linea_minuscula.startswith(p) for p in prefijos_internos):
                continue
            filtradas.append(linea)

        texto = "\n".join(filtradas)
        texto = re.sub(r"\n{3,}", "\n\n", texto)
        texto = texto.strip().strip('"')

        return texto

    def puntuar_idioma(self, texto):
        """Devuelve (puntos_espanol, puntos_ingles) usando palabras funcionales."""
        texto_normal = normalizar(texto)
        palabras = texto_normal.split()

        palabras_espanol = {
            "el", "la", "los", "las", "un", "una", "unos", "unas", "de", "del",
            "que", "y", "o", "en", "con", "sin", "por", "para", "como", "porque",
            "es", "son", "soy", "eres", "esta", "estas", "estoy", "hay", "tiene",
            "puede", "puedo", "podemos", "ser", "si", "no", "pero", "tambien", "muy",
            "mas", "menos", "cuando", "donde", "quien", "cual", "su", "sus", "mi",
            "mis", "tu", "tus", "le", "lo", "se", "me", "te", "ya", "hoy", "jefe", "señor", "senor",
            "bien", "gracias", "claro", "creo", "recuerdo", "respuesta", "ayudar", "hacer",
            "esto", "eso", "este", "esta", "aqui", "algo", "todo", "cada", "desde",
        }

        palabras_ingles = {
            "the", "and", "you", "your", "are", "is", "was", "were", "this", "that",
            "with", "from", "have", "has", "had", "can", "could", "would", "should",
            "will", "what", "when", "where", "why", "how", "about", "because", "but",
            "not", "for", "into", "let", "think", "thinking", "answer", "response", "user",
            "assistant", "need", "needs", "make", "sure", "always", "only", "spanish",
            "english", "provide", "given", "context", "memory", "memories", "system", "prompt",
            "message", "reply", "final", "here", "there", "some", "more", "also", "then",
            "now", "dont", "doesnt", "did", "do", "does", "it", "its", "we", "they",
            "them", "our", "of", "to", "in", "on", "at", "as", "be", "been", "being",
            "if", "or", "so", "just", "really", "know", "want", "like", "good", "hello",
            "thanks", "please", "tell", "remember", "today", "computer", "local", "model",
        }

        puntos_es = sum(1 for p in palabras if p in palabras_espanol)
        puntos_en = sum(1 for p in palabras if p in palabras_ingles)

        frases_ingles = (
            "the user",
            "let me",
            "we need",
            "i need",
            "i think",
            "in english",
            "final answer",
            "the answer",
            "you can",
            "i can",
            "here is",
            "here are",
        )

        for frase in frases_ingles:
            if frase in texto_normal:
                puntos_en += 4

        return puntos_es, puntos_en

    def respuesta_tiene_demasiado_ingles(self, texto):
        if not texto:
            return False

        puntos_es, puntos_en = self.puntuar_idioma(texto)

        # Dos o más señales inglesas ya son sospechosas si no hay dominio claro del español.
        if puntos_en >= 2 and puntos_en >= max(2, puntos_es * 0.45):
            return True

        # Cuatro señales inglesas se consideran mezcla aunque haya bastante español.
        if puntos_en >= 4:
            return True

        return False

    def corregir_a_espanol(self, texto):
        """Intenta hasta dos veces traducir/reformular sin reutilizar historial."""
        texto_actual = texto

        for intento in range(2):
            mensajes = [
                {
                    "role": "system",
                    "content": (
                        "Eres un traductor y corrector profesional de español. "
                        "Devuelve exclusivamente una versión completamente en español natural del texto. "
                        "No expliques la traducción, no hagas comentarios, no añadas notas y no uses inglés. "
                        "Conserva únicamente nombres propios de marcas y tecnologías como Windows, Python, "
                        "Chrome, Ollama, Qwen, SQL o Visual Studio Code. "
                        "La salida será leída en voz alta, por lo que debe contener solo la respuesta final en español."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "TRADUCE Y REESCRIBE COMPLETAMENTE EN ESPAÑOL EL SIGUIENTE TEXTO:\n\n"
                        + texto_actual
                        + "\n\nSALIDA: solamente el texto final en español."
                    ),
                },
            ]

            respuesta = self.enviar_ollama(
                mensajes,
                temperatura=0.0,
                num_predict=260,
            )

            if not respuesta:
                return None

            respuesta = self.limpiar_respuesta_ollama(respuesta)
            print(f"CORRECCIÓN ESPAÑOL INTENTO {intento + 1}:", respuesta)

            if not self.respuesta_tiene_demasiado_ingles(respuesta):
                return respuesta

            texto_actual = respuesta

        return None

    def regenerar_espanol_sin_historial(self, pregunta):
        """Genera desde cero una respuesta breve en español, sin recuerdos ni historial."""
        mensajes = [
            {
                "role": "system",
                "content": (
                    "Tu nombre es Beta y hablas con el Señor. "
                    "Responde EXCLUSIVAMENTE EN ESPAÑOL. Está prohibido escribir frases en inglés. "
                    "No muestres razonamiento ni análisis. Responde de forma breve, natural y útil. "
                    "Conserva en inglés únicamente nombres propios de tecnologías o marcas."
                ),
            },
            {
                "role": "user",
                "content": pregunta + "\n\nRespuesta final exclusivamente en español:",
            },
        ]

        respuesta = self.enviar_ollama(
            mensajes,
            temperatura=0.0,
            num_predict=200,
        )

        if not respuesta:
            return None

        return self.limpiar_respuesta_ollama(respuesta)

    def conversar_ollama_async(self, pregunta):
        token = self.iniciar_proceso("ollama")
        if token is None:
            self.responder(
                "todavía estoy terminando la respuesta anterior. Espere un momento y vuelva a preguntarme.",
                "pensando",
            )
            return

        self.expresion_pensando()

        def trabajo():
            respuesta = None
            uso_streaming = False
            try:
                if STREAMING_OLLAMA_ACTIVO:
                    sistema = self.construir_prompt_sistema(pregunta)
                    mensajes = [{"role": "system", "content": sistema}]
                    mensajes.extend(self.preparar_historial_ollama(pregunta)[-4:])
                    mensajes.append(
                        {
                            "role": "user",
                            "content": (
                                pregunta
                                + "\n\nResponde únicamente en español. Para conversación oral, "
                                  "da primero la respuesta directa y normalmente usa entre 2 y 4 frases. "
                                  "No uses Markdown salvo que sea imprescindible."
                            ),
                        }
                    )
                    respuesta = self.generar_y_hablar_ollama_streaming(
                        mensajes,
                        "general",
                        token,
                        temperatura=0.20,
                        num_predict=OLLAMA_NUM_PREDICT,
                    )
                    uso_streaming = bool(respuesta)
                else:
                    respuesta = self.consultar_ollama(pregunta)
            except Exception as error:
                print("ERROR HILO OLLAMA:", error)
            finally:
                self.terminar_proceso(token)

            # Si el watchdog ya invalidó esta operación, ignorar respuesta tardía.
            if token != self.proceso_id:
                return

            if respuesta and not uso_streaming:
                self.root.after(0, lambda r=respuesta: self.responder(r, "hablando"))
            elif not respuesta:
                self.root.after(
                    0,
                    lambda: self.responder(
                        "no pude obtener una respuesta de mi modelo local. Revise que Ollama esté iniciado.",
                        "confundida",
                    ),
                )

        threading.Thread(target=trabajo, daemon=True).start()

    # ======================================================
    # TAMAÑO / ARRASTRE / TOPMOST
    # ======================================================

    def cambiar_tamano_rueda(self, event):
        self.registrar_actividad()
        nuevo = self.tamano_beta + PASO_TAMANO if event.delta > 0 else self.tamano_beta - PASO_TAMANO
        self.ajustar_tamano(nuevo)

    def aumentar_tamano(self):
        self.ajustar_tamano(self.tamano_beta + PASO_TAMANO)

    def disminuir_tamano(self):
        self.ajustar_tamano(self.tamano_beta - PASO_TAMANO)

    def tamano_normal(self):
        self.ajustar_tamano(TAMANO_INICIAL)

    def ajustar_tamano(self, nuevo_tamano):
        nuevo_tamano = max(TAMANO_MINIMO, min(TAMANO_MAXIMO, int(nuevo_tamano)))
        if nuevo_tamano == self.tamano_beta:
            return

        centro_x = self.root.winfo_x() + self.tamano_beta / 2
        centro_y = self.root.winfo_y() + self.tamano_beta / 2
        self.tamano_beta = nuevo_tamano

        nueva_x = int(centro_x - nuevo_tamano / 2)
        nueva_y = int(centro_y - nuevo_tamano / 2)
        pantalla_ancho = self.root.winfo_screenwidth()
        pantalla_alto = self.root.winfo_screenheight()

        nueva_x = max(0, min(nueva_x, pantalla_ancho - nuevo_tamano))
        nueva_y = max(0, min(nueva_y, pantalla_alto - nuevo_tamano))

        self.root.geometry(
            f"{nuevo_tamano}x{nuevo_tamano}+{nueva_x}+{nueva_y}"
        )
        self.memoria.cambiar_estado("tamano_beta", nuevo_tamano)
        self.root.after(20, self.redibujar_beta)

    def iniciar_arrastre(self, event):
        self.arrastre_x = event.x
        self.arrastre_y = event.y
        self.registrar_actividad()

    def arrastrar_beta(self, event):
        nueva_x = self.root.winfo_x() + event.x - self.arrastre_x
        nueva_y = self.root.winfo_y() + event.y - self.arrastre_y
        self.root.geometry(f"+{nueva_x}+{nueva_y}")
        self.registrar_actividad()

    def guardar_posicion(self, event=None):
        try:
            self.memoria.cambiar_estado("pos_x", self.root.winfo_x())
            self.memoria.cambiar_estado("pos_y", self.root.winfo_y())
        except Exception:
            pass

    def mantener_siempre_visible(self):
        try:
            self.root.attributes("-topmost", True)
            self.root.update_idletasks()
            hwnd = self.root.winfo_id()
            HWND_TOPMOST = -1
            SWP_NOSIZE = 0x0001
            SWP_NOMOVE = 0x0002
            SWP_NOACTIVATE = 0x0010

            ctypes.windll.user32.SetWindowPos(
                hwnd,
                HWND_TOPMOST,
                0,
                0,
                0,
                0,
                SWP_NOSIZE | SWP_NOMOVE | SWP_NOACTIVATE,
            )
        except Exception:
            pass

        try:
            self.root.after(1000, self.mantener_siempre_visible)
        except tk.TclError:
            pass

    # ======================================================
    # ACTIVIDAD / IMPACIENCIA
    # ======================================================

    def registrar_actividad(self):
        self.ultimo_movimiento_mouse = time.time()
        self.impaciente = False

    def vigilar_inactividad(self):
        try:
            posicion_actual = (
                self.root.winfo_pointerx(),
                self.root.winfo_pointery(),
            )

            if posicion_actual != self.ultima_posicion_mouse:
                self.ultima_posicion_mouse = posicion_actual
                self.ultimo_movimiento_mouse = time.time()

                if self.impaciente:
                    self.impaciente = False
                    if not self.hablando and not self.procesando:
                        self.expresion_sorprendida()
                        self.root.after(700, self.volver_despues_sorpresa)

            tiempo_inactivo = time.time() - self.ultimo_movimiento_mouse

            if (
                tiempo_inactivo >= TIEMPO_IMPACIENCIA
                and not self.impaciente
                and not self.hablando
                and not self.procesando
                and not self.esperando_orden
                and self.expresion_actual
                not in {"pensando", "confundida", "molesta", "sorprendida"}
            ):
                self.impaciente = True
                self.expresion_impaciente()

        except Exception:
            pass

        try:
            self.root.after(500, self.vigilar_inactividad)
        except tk.TclError:
            pass

    def volver_despues_sorpresa(self):
        if self.expresion_actual != "sorprendida":
            return
        if self.escuchando:
            self.expresion_escuchando()
        else:
            self.expresion_normal()

    # ======================================================
    # INICIO / VOZ VOSK
    # ======================================================

    def obtener_saludo_horario(self):
        """Devuelve un saludo acorde a la hora local del computador.

        05:00 a 11:59  -> Buenos días
        12:00 a 19:59  -> Buenas tardes
        20:00 a 04:59  -> Buenas noches
        """
        hora = datetime.now().hour

        if 5 <= hora < 12:
            return "Buenos días, Señor"
        elif 12 <= hora < 20:
            return "Buenas tardes, Señor"
        else:
            return "Buenas noches, Señor"

    def extraer_clima_para_informe_inicio(self, texto_clima):
        """Extrae ciudad, temperatura y condición del texto que ya genera obtener_clima().

        Se mantiene una única fuente meteorológica dentro de Beta: el informe de
        inicio reutiliza obtener_clima() y su caché, en vez de abrir una segunda
        consulta independiente.
        """
        texto_clima = (texto_clima or "").strip()
        if not texto_clima:
            return None

        patron = re.search(
            r"^en\s+(.+?)\s+hay\s+(.+?)\s+grados,\s+con\s+([^,.]+)",
            texto_clima,
            flags=re.IGNORECASE,
        )
        if not patron:
            return None

        ubicacion_texto = patron.group(1).strip()
        temperatura = patron.group(2).strip()
        condicion = patron.group(3).strip()

        # Para la locución preferimos el nombre corto guardado por el geocodificador
        # (por ejemplo "Santiago") y no "Santiago, Región Metropolitana...".
        ciudad = (self.memoria.obtener_estado("clima_nombre", "") or "").strip()
        if not ciudad:
            ciudad = (self.memoria.obtener_estado("ciudad_clima", "") or "").strip()
        if not ciudad:
            ciudad = ubicacion_texto.split(",", 1)[0].strip()

        if not ciudad or not temperatura or temperatura.lower() == "sin dato":
            return None

        return {
            "ciudad": ciudad,
            "temperatura": temperatura,
            "condicion": condicion or "condiciones meteorológicas variables",
        }

    def construir_informe_inicio(self):
        """Construye el saludo dinámico con hora local y clima actual.

        Si Internet falla, intenta reutilizar la última lectura meteorológica
        almacenada. Beta nunca queda bloqueada por el clima: como último recurso
        informa la hora y continúa el inicio normalmente.
        """
        datos_clima = None
        error_clima = None

        try:
            texto_clima, error_clima = self.obtener_clima()
            if texto_clima:
                datos_clima = self.extraer_clima_para_informe_inicio(texto_clima)

            # Si la actualización falló, una lectura anterior sigue siendo más útil
            # que omitir por completo el clima. Se identifica en consola como caché.
            if datos_clima is None:
                cache_anterior = (
                    self.memoria.obtener_estado("clima_cache_texto", "") or ""
                ).strip()
                if cache_anterior:
                    datos_clima = self.extraer_clima_para_informe_inicio(cache_anterior)
                    if datos_clima:
                        print("INFORME DE INICIO: usando última lectura meteorológica disponible.")
        except Exception as error:
            error_clima = str(error)
            print("ERROR PREPARANDO CLIMA DEL INFORME DE INICIO:", error)

        # La hora se toma justo antes de construir la frase, para que no quede
        # desfasada si la consulta meteorológica tardó algunos segundos.
        ahora = datetime.now()
        saludo = self.obtener_saludo_horario()
        hora_texto = ahora.strftime("%H:%M")

        if datos_clima:
            print(
                "INFORME DE INICIO: "
                f"{datos_clima['ciudad']} | {datos_clima['temperatura']} °C | "
                f"{datos_clima['condicion']}"
            )
            return (
                f"{saludo}. Le informo que son las {hora_texto} horas. "
                f"En estos momentos, la ciudad de {datos_clima['ciudad']} registra "
                f"una temperatura de {datos_clima['temperatura']} grados centígrados, "
                f"con condiciones de {datos_clima['condicion']}. "
                "Nos encontramos listos para comenzar."
            )

        if error_clima:
            print("INFORME DE INICIO: clima no disponible:", error_clima)
        else:
            print("INFORME DE INICIO: no hay una ciudad meteorológica configurada.")

        return (
            f"{saludo}. Le informo que son las {hora_texto} horas. "
            "En estos momentos no pude actualizar las condiciones meteorológicas. "
            "Nos encontramos listos para comenzar."
        )

    def emitir_informe_inicio(self, mensaje):
        self.informe_inicio_en_curso = True
        self.responder(mensaje, "feliz", tipo_contexto="inicio")

        # Respaldo de seguridad: normalmente la escucha se activa al terminar
        # Daniela. Si por una falla de audio no llegara ese callback, Beta no
        # quedará muda para siempre.
        try:
            self.root.after(45000, self.iniciar_escucha_si_necesario)
        except tk.TclError:
            pass

    def iniciar_escucha_si_necesario(self):
        if not self.escuchando and not self.hablando:
            self.iniciar_escucha()

    def iniciar_beta(self):
        # El clima puede requerir una consulta de red de algunos segundos. Se
        # prepara fuera del hilo de Tk para que la esfera nunca se congele.
        def trabajo_inicio():
            mensaje_inicio = self.construir_informe_inicio()
            try:
                self.root.after(
                    0,
                    lambda mensaje=mensaje_inicio: self.emitir_informe_inicio(mensaje),
                )
            except tk.TclError:
                pass

        threading.Thread(target=trabajo_inicio, daemon=True).start()

    # ======================================================
    # RECONOCIMIENTO DE HABLANTE / HUELLAS VOCALES
    # ======================================================

    def cargar_modelo_hablante(self):
        if not USAR_RECONOCIMIENTO_HABLANTE:
            return
        if self.hablante_listo or self.hablante_cargando:
            return

        self.hablante_cargando = True
        try:
            from speechbrain.inference.speaker import EncoderClassifier
            from speechbrain.utils.fetching import LocalStrategy

            CARPETA_HABLANTE.mkdir(parents=True, exist_ok=True)
            archivo_local = CARPETA_HABLANTE / "hyperparams.yaml"

            print()
            print("==============================")
            print("PREPARANDO IDENTIDAD DE VOZ")
            if not archivo_local.exists():
                print("Primera vez: descargando modelo ECAPA-TDNN.")
                print("Modo Windows: se copiarán los archivos sin crear enlaces simbólicos.")
                print("Después funcionará localmente.")
            else:
                print("Modelo ECAPA-TDNN encontrado localmente.")
            print("==============================")

            # SpeechBrain usa SYMLINK por defecto. En Windows eso puede fallar
            # con WinError 1314 si no está activo el Modo desarrollador.
            # COPY_SKIP_CACHE fuerza archivos normales en la carpeta de Beta.
            self.modelo_hablante = EncoderClassifier.from_hparams(
                source=HABLANTE_REPO,
                savedir=str(CARPETA_HABLANTE),
                run_opts={"device": "cpu"},
                local_strategy=LocalStrategy.COPY_SKIP_CACHE,
            )
            self.hablante_listo = True
            self.hablante_error = ""
            print("IDENTIDAD DE VOZ LISTA")
            print("Voces autorizadas:", self.memoria.cantidad_voces_autorizadas())
            print()

        except ImportError as error:
            self.hablante_error = (
                "Falta SpeechBrain/PyTorch. Instale los paquetes indicados."
            )
            print("RECONOCIMIENTO DE HABLANTE NO DISPONIBLE:", self.hablante_error)
            print("Detalle:", error)
        except Exception as error:
            self.hablante_error = str(error)
            print("ERROR CARGANDO MODELO DE HABLANTE:", error)
        finally:
            self.hablante_cargando = False

    # ======================================================
    # PRIVACIDAD / MODOS DE ESCUCHA
    # ======================================================

    def _wake_candidatos_vosk(self):
        # "meta/metas" se conservan SOLO como candidatos de Vosk para poder
        # enviar la frase a Whisper. Nunca bastan por sí solos para activar Beta
        # en modo estricto, porque son palabras demasiado comunes en español.
        return ("beta", "veta", "petra", "meta", "metas")

    def _wake_estrictos(self):
        return ("beta", "veta", "petra")

    def _wake_en_inicio(self, texto_normal, incluir_ambiguos=False):
        palabras = (texto_normal or "").split()
        if not palabras:
            return None
        permitidos = self._wake_candidatos_vosk() if incluir_ambiguos else self._wake_estrictos()
        # Forma normal: "Beta, ...". También permitimos "Hola Beta...",
        # "Oye Beta..." y "Hey Beta..." sin aceptar la palabra en cualquier
        # posición de una conversación ambiental.
        if palabras[0] in permitidos:
            return palabras[0]
        if len(palabras) >= 2 and palabras[0] in {"hola", "oye", "hey"} and palabras[1] in permitidos:
            return palabras[1]
        # Despedida natural: "gracias Beta". Solo para frases cortas.
        if len(palabras) <= 5 and palabras[-1] in permitidos and any(
            p in palabras for p in ("gracias", "agradezco")
        ):
            return palabras[-1]
        return None

    def _orden_despertar_silencio(self, texto_normal):
        t = texto_normal or ""
        wake = self._wake_en_inicio(t, incluir_ambiguos=False)
        if not wake:
            return False
        return any(frase in t for frase in (
            "despierta", "despertar", "reactiva", "reanuda escucha",
            "reanuda la escucha", "vuelve a escuchar", "sal del silencio",
        ))

    def _actualizar_expiracion_modo_conversacion(self):
        if self.modo_escucha != "conversacion":
            return
        if self.modo_conversacion_hasta and time.time() > self.modo_conversacion_hasta:
            self.modo_escucha = "estricto"
            self.modo_conversacion_hasta = 0.0
            self.hablante_sesion_conversacion = ""
            self.ultima_autenticacion_fuerte_ts = 0.0
            self.esperando_orden = False
            try:
                if hasattr(self, "var_modo_escucha"):
                    self.var_modo_escucha.set("estricto")
            except Exception:
                pass
            print("MODO CONVERSACIÓN: cerrado por 60 s de silencio. Vuelve a modo estricto.")

    def renovar_modo_conversacion(self):
        if self.modo_escucha == "conversacion":
            self.modo_conversacion_hasta = time.time() + TIEMPO_MODO_CONVERSACION_SILENCIO

    def establecer_modo_escucha(self, modo, anunciar=False, requiere_autenticacion=False):
        modo = (modo or "").strip().lower()
        if modo not in {"estricto", "conversacion", "silencio"}:
            return False

        self.modo_escucha = modo
        self.esperando_orden = False
        self.tiempo_limite_orden = 0.0

        if modo == "conversacion":
            # Si existen voces autorizadas y el cambio vino por voz, la sesión
            # solo queda confiable cuando hubo autenticación fuerte reciente.
            voces_registradas = self.memoria.cantidad_voces_autorizadas() > 0
            autenticacion_reciente = (
                bool(self.hablante_actual)
                and self.ultima_autenticacion_fuerte_ts > 0
                and (time.time() - self.ultima_autenticacion_fuerte_ts) <= 12
            )
            if requiere_autenticacion and voces_registradas and not autenticacion_reciente:
                self.modo_escucha = "estricto"
                self.modo_conversacion_hasta = 0.0
                self.hablante_sesion_conversacion = ""
                try:
                    if hasattr(self, "var_modo_escucha"):
                        self.var_modo_escucha.set("estricto")
                except Exception:
                    pass
                print("PRIVACIDAD: modo conversación rechazado; faltó autenticación fuerte reciente.")
                if anunciar:
                    self.responder(
                        "no pude confirmar suficientemente su identidad para abrir una conversación libre. "
                        "Repita Beta, activa modo conversación.",
                        "confundida",
                        tipo_contexto="general",
                    )
                return False

            self.modo_conversacion_hasta = time.time() + TIEMPO_MODO_CONVERSACION_SILENCIO
            if self.hablante_actual:
                self.hablante_sesion_conversacion = self.hablante_actual
                print(f"MODO CONVERSACIÓN: sesión vinculada a {self.hablante_sesion_conversacion}.")
            else:
                self.hablante_sesion_conversacion = ""
            respuesta = (
                "modo conversación activado. Durante el próximo minuto puede continuar "
                "hablándome sin repetir mi nombre; el tiempo se renueva con cada intervención."
            )
            print("MODO DE ESCUCHA: CONVERSACIÓN (60 s renovables).")
        elif modo == "silencio":
            self.modo_conversacion_hasta = 0.0
            self.hablante_sesion_conversacion = ""
            self.ultima_autenticacion_fuerte_ts = 0.0
            respuesta = (
                "modo silencio activado. Ignoraré las conversaciones y solo reaccionaré "
                "si dice Beta, despierta."
            )
            print("MODO DE ESCUCHA: SILENCIO. Solo 'Beta, despierta' puede reactivarme.")
        else:
            self.modo_conversacion_hasta = 0.0
            self.hablante_sesion_conversacion = ""
            self.ultima_autenticacion_fuerte_ts = 0.0
            respuesta = (
                "modo estricto activado. Solo responderé cuando diga mi nombre y la voz sea autorizada."
            )
            print("MODO DE ESCUCHA: ESTRICTO. Wake word + voz autorizada.")

        try:
            if hasattr(self, "var_modo_escucha"):
                self.var_modo_escucha.set(modo)
        except Exception:
            pass

        if anunciar:
            self.responder(respuesta, "normal", tipo_contexto="general")
        return True

    def cambiar_modo_escucha_menu(self):
        try:
            modo = self.var_modo_escucha.get()
        except Exception:
            modo = "estricto"
        self.establecer_modo_escucha(modo, anunciar=True)

    def frase_candidata_para_beta_vosk(self, texto_vosk):
        """Filtro barato ANTES de biometría y Whisper.

        En estricto, una charla ambiental sin wake word se descarta aquí.
        En silencio, ni siquiera se verifica la voz salvo ante un posible
        "Beta, despierta". En conversación, sí se valida cada intervención.
        """
        self._actualizar_expiracion_modo_conversacion()
        t = normalizar(texto_vosk)
        ahora = time.time()

        if self.modo_escucha == "conversacion":
            return ahora <= self.modo_conversacion_hasta

        if self.pregunta_curiosa_pendiente and ahora <= self.pregunta_curiosa_hasta:
            # Beta acaba de formular una pregunta explícita. Permitimos UNA
            # respuesta sin wake word, pero la biometría sigue siendo obligatoria.
            return True

        if self.evaluacion_academica_pendiente and ahora <= self.evaluacion_academica_hasta:
            return True

        if self.esperando_orden and ahora <= self.tiempo_limite_orden:
            return True

        wake = self._wake_en_inicio(t, incluir_ambiguos=True)
        if self.modo_escucha == "silencio":
            if not wake:
                return False
            return any(p in t for p in (
                "despierta", "despertar", "reactiva", "reanuda", "escucha", "silencio"
            ))

        return wake is not None

    def activacion_vosk_ambigua(self, texto_vosk):
        t = normalizar(texto_vosk)
        wake = self._wake_en_inicio(t, incluir_ambiguos=True)
        return wake in {"meta", "metas"}

    def vaciar_cola_audio_pendiente(self):
        """Descarta audio atrasado acumulado mientras Whisper estaba calculando."""
        if not AUDIO_VACIAR_COLA_TRAS_WHISPER:
            return 0
        descartados = 0
        try:
            while True:
                self.audio_queue.get_nowait()
                descartados += 1
        except queue.Empty:
            pass
        except Exception:
            pass
        if descartados:
            print(f"AUDIO: descartados {descartados} bloque(s) atrasados tras Whisper.")
        return descartados

    def transcripcion_asr_sospechosa(self, texto_vosk, texto_whisper):
        """Filtro conservador para alucinaciones típicas de Whisper/TV.

        Solo bloquea boilerplate corto o una expansión extrema desde una frase
        Vosk de 1-2 palabras a una transcripción no relacionada. No corrige dictado
        normal ni órdenes largas.
        """
        if not ASR_FILTRAR_BOILERPLATE:
            return False
        v = normalizar(texto_vosk)
        w = normalizar(texto_whisper)
        if not w:
            return False

        boilerplate = (
            "suscribete", "suscribete al canal", "gracias por ver",
            "gracias por mirar", "dale like", "activa la campana",
            "subtitulos", "subtitulos en espanol", "subtitulos realizados por",
            "nos vemos en el proximo video", "gracias por su atencion",
        )
        if len(w.split()) <= 6 and any(w == b or w.startswith(b + " ") for b in boilerplate):
            return True

        pv = v.split()
        pw = w.split()
        if len(pv) <= 2 and len(pw) >= 4:
            ratio = difflib.SequenceMatcher(None, v, w).ratio()
            if ratio < 0.22:
                return True
        return False

    def cambiar_reconocimiento_hablante(self):
        activo = bool(self.var_reconocimiento_hablante.get())
        cantidad_voces = self.memoria.cantidad_voces_autorizadas()

        if activo and cantidad_voces == 0:
            messagebox.showwarning(
                "Beta - Identidad de voz",
                "Primero registre al menos una voz autorizada.",
                parent=self.root,
            )
            self.var_reconocimiento_hablante.set(False)
            return

        # En v2.5.4, si hay voces registradas el modo privado exige biometría.
        # Evita que un clic accidental deje 'estricto' como solo wake word.
        if (
            not activo
            and cantidad_voces > 0
            and HABLANTE_BIOMETRIA_PRIVACIDAD_OBLIGATORIA
        ):
            messagebox.showwarning(
                "Beta - Privacidad",
                "Hay voces autorizadas registradas. Para conservar el modo privado, "
                "la verificación biométrica permanecerá activada.",
                parent=self.root,
            )
            self.var_reconocimiento_hablante.set(True)
            activo = True

        self.reconocimiento_hablante_activo = activo
        self.memoria.cambiar_estado("reconocimiento_hablante", "1" if activo else "0")

        if activo and not self.hablante_listo and not self.hablante_cargando:
            threading.Thread(target=self.cargar_modelo_hablante, daemon=True).start()

    def _pcm_a_16k(self, audio_pcm, frecuencia):
        try:
            import numpy as np
        except ImportError:
            return None

        if not audio_pcm:
            return None

        audio = np.frombuffer(audio_pcm, dtype=np.int16).astype(np.float32) / 32768.0
        if audio.size < 100:
            return None

        absoluto = np.abs(audio)
        p90 = float(np.percentile(absoluto, 90)) if absoluto.size else 0.0
        umbral = max(0.004, p90 * 0.12)
        indices = np.where(absoluto >= umbral)[0]
        if indices.size:
            margen = int(float(frecuencia) * 0.15)
            inicio = max(0, int(indices[0]) - margen)
            fin = min(audio.size, int(indices[-1]) + margen)
            audio = audio[inicio:fin]

        if frecuencia != HABLANTE_FRECUENCIA and audio.size > 1:
            duracion = audio.size / float(frecuencia)
            nueva_cantidad = max(1, int(duracion * HABLANTE_FRECUENCIA))
            x_origen = np.linspace(0.0, duracion, num=audio.size, endpoint=False)
            x_destino = np.linspace(0.0, duracion, num=nueva_cantidad, endpoint=False)
            audio = np.interp(x_destino, x_origen, audio).astype(np.float32)

        return audio

    def extraer_embedding_hablante(self, audio_pcm, frecuencia):
        if not self.hablante_listo or self.modelo_hablante is None:
            return None

        try:
            import numpy as np
            import torch

            audio = self._pcm_a_16k(audio_pcm, frecuencia)
            if audio is None or audio.size == 0:
                return None

            duracion = audio.size / float(HABLANTE_FRECUENCIA)
            if duracion < HABLANTE_MIN_SEGUNDOS:
                print(f"IDENTIDAD: audio demasiado corto ({duracion:.2f} s)")
                return None

            tensor = torch.from_numpy(audio).float().unsqueeze(0)
            with torch.no_grad():
                emb = self.modelo_hablante.encode_batch(tensor, normalize=True)

            vector = emb.squeeze().detach().cpu().numpy().astype(np.float32)
            norma = float(np.linalg.norm(vector))
            if norma <= 1e-8:
                return None
            return vector / norma

        except Exception as error:
            print("ERROR EXTRAER HUELLA VOCAL:", error)
            return None

    def es_seguimiento_corto_seguro(self, texto_vosk):
        """Permite una tolerancia biométrica limitada SOLO en conversación.

        Las frases breves dan embeddings más inestables. Para no volver a hacer
        permisivo el modo estricto, solo consideramos seguimiento contextual
        frases de hasta unas pocas palabras, sin wake word y sin órdenes de
        sistema/privacidad potencialmente sensibles.
        """
        t = normalizar(texto_vosk or "")
        palabras = t.split()
        if not palabras or len(palabras) > HABLANTE_MAX_PALABRAS_SEGUIMIENTO_CORTO:
            return False
        if self._wake_en_inicio(t, incluir_ambiguos=False) is not None:
            return False

        bloqueadas = {
            "abre", "abrir", "cierra", "cerrar", "apaga", "apagar",
            "reinicia", "reiniciar", "elimina", "eliminar", "borra", "borrar",
            "ejecuta", "ejecutar", "descarga", "descargar", "instala", "instalar",
            "registra", "registrar", "silencio", "despierta", "modo",
            "chrome", "youtube", "correo", "envia", "enviar", "archivo",
        }
        if any(p in bloqueadas for p in palabras):
            return False

        inicios_seguros = (
            "dame " , "dime " , "explica", "explicame", "profundiza",
            "continua", "sigue", "por que", "porque", "como " ,
            "cual " , "cuales " , "que " , "y " , "otro " , "otra " ,
            "repite", "resume", "resumelo", "un ejemplo", "otro ejemplo",
            "gracias", "muchas gracias", "perfecto", "entendido", "de acuerdo",
        )
        return any(t.startswith(pref) for pref in inicios_seguros) or t in {
            "profundiza", "continua", "sigue", "por que", "como",
            "cual", "cuales", "que significa", "otro ejemplo", "resumelo",
            "gracias", "gracias beta", "muchas gracias", "perfecto", "entendido",
            "de acuerdo", "ok", "esta bien",
        }

    def identificar_hablante(self, audio_pcm, frecuencia, texto_vosk=""):
        voces = self.memoria.listar_voces_autorizadas(solo_activas=True)
        if not voces:
            # Sin perfiles de voz no hay contra qué verificar. El wake word sigue
            # siendo obligatorio en modo estricto.
            return True, ""

        # Consolidación v2.5.4: una base con voces registradas nunca debe saltarse
        # biometría por un flag persistente antiguo o desactivado accidentalmente.
        if not self.reconocimiento_hablante_activo:
            if HABLANTE_BIOMETRIA_PRIVACIDAD_OBLIGATORIA:
                print("PRIVACIDAD: biometría obligatoria restaurada para esta sesión.")
                self.reconocimiento_hablante_activo = True
                self.memoria.cambiar_estado("reconocimiento_hablante", "1")
            else:
                return True, ""

        if not self.hablante_listo:
            if not self.hablante_cargando:
                threading.Thread(target=self.cargar_modelo_hablante, daemon=True).start()
            print("IDENTIDAD: modelo todavía no disponible; frase ignorada por seguridad.")
            return False, ""

        try:
            import numpy as np
            actual = self.extraer_embedding_hablante(audio_pcm, frecuencia)
            if actual is None:
                print("IDENTIDAD: no se pudo obtener huella; frase ignorada.")
                return False, ""

            mejor_nombre = ""
            mejor_score = -1.0

            for _id, nombre, embedding, _muestras, _fecha, _activo in voces:
                if not embedding:
                    continue
                referencia = np.asarray(embedding, dtype=np.float32)
                if referencia.size != actual.size:
                    continue
                norma = float(np.linalg.norm(referencia))
                if norma <= 1e-8:
                    continue
                referencia = referencia / norma
                score = float(np.dot(actual, referencia))
                if score > mejor_score:
                    mejor_score = score
                    mejor_nombre = nombre

            ahora = time.time()
            umbral_aplicado = self.umbral_hablante
            seguimiento_contextual = False

            # v2.5.2: ECAPA es muy fiable con frases normales, pero una frase de
            # uno a cuatro segundos puede bajar mucho de score aun siendo la
            # misma persona. Solo durante un modo conversación EXPLÍCITO, abierto
            # por una autenticación fuerte reciente, permitimos un umbral más
            # bajo para seguimientos benignos y cortos.
            sesion_confiable = (
                self.modo_escucha == "conversacion"
                and ahora <= self.modo_conversacion_hasta
                and bool(self.hablante_sesion_conversacion)
                and (ahora - self.ultima_autenticacion_fuerte_ts)
                    <= HABLANTE_SESION_CONFIABLE_SEGUNDOS
            )
            if (
                sesion_confiable
                and mejor_nombre
                and mejor_nombre.casefold() == self.hablante_sesion_conversacion.casefold()
                and self.es_seguimiento_corto_seguro(texto_vosk)
            ):
                umbral_aplicado = min(
                    self.umbral_hablante, HABLANTE_UMBRAL_SEGUIMIENTO_CORTO
                )
                seguimiento_contextual = True

            print(
                f"IDENTIDAD DE VOZ: mejor={mejor_nombre or 'desconocido'} "
                f"score={mejor_score:.3f} umbral={umbral_aplicado:.3f}"
                + (" (seguimiento corto seguro)" if seguimiento_contextual else "")
            )

            if mejor_nombre and mejor_score >= umbral_aplicado:
                self.hablante_actual = mejor_nombre
                if mejor_score >= self.umbral_hablante:
                    self.ultima_autenticacion_fuerte_ts = ahora
                    if self.modo_escucha == "conversacion":
                        self.hablante_sesion_conversacion = mejor_nombre
                elif seguimiento_contextual:
                    print(
                        "IDENTIDAD: seguimiento corto aceptado por sesión autenticada; "
                        "no renueva la autenticación fuerte."
                    )
                return True, mejor_nombre

            self.hablante_actual = ""
            return False, ""

        except Exception as error:
            print("ERROR IDENTIFICANDO HABLANTE:", error)
            return False, ""

    def ventana_registrar_voz(self):
        if self.registrando_voz:
            return

        ventana = tk.Toplevel(self.root)
        ventana.title("Registrar voz autorizada")
        ventana.geometry("500x360")
        ventana.attributes("-topmost", True)

        ttk.Label(
            ventana,
            text="Registrar una voz autorizada",
            font=("Segoe UI", 13, "bold"),
        ).pack(pady=(18, 8))

        ttk.Label(
            ventana,
            text=(
                "La huella de voz se guardará localmente en beta.db.\n"
                "Las grabaciones temporales se descartan después del registro.\n"
                "Registre a otras personas solo con su consentimiento."
            ),
            justify="center",
            wraplength=440,
        ).pack(padx=20, pady=(0, 15))

        marco = ttk.Frame(ventana)
        marco.pack(fill="x", padx=25)
        ttk.Label(marco, text="Nombre:").pack(side="left")
        entrada_nombre = ttk.Entry(marco)
        entrada_nombre.pack(side="left", fill="x", expand=True, padx=(8, 0))

        estado = ttk.Label(
            ventana,
            text="Se grabarán 3 muestras de 4 segundos.",
            justify="center",
        )
        estado.pack(pady=25)

        boton = ttk.Button(ventana, text="Grabar mi voz")
        boton.pack(pady=8)

        def actualizar_estado(texto_estado):
            if ventana.winfo_exists():
                estado.configure(text=texto_estado)

        def terminar_registro(exito, mensaje):
            self.registrando_voz = False
            if ventana.winfo_exists():
                boton.configure(state="normal")
                actualizar_estado(mensaje)
            if exito:
                self.reconocimiento_hablante_activo = True
                self.memoria.cambiar_estado("reconocimiento_hablante", "1")
                try:
                    self.var_reconocimiento_hablante.set(True)
                except Exception:
                    pass
                messagebox.showinfo(
                    "Beta - Identidad de voz",
                    mensaje,
                    parent=ventana if ventana.winfo_exists() else self.root,
                )
            else:
                messagebox.showerror(
                    "Beta - Identidad de voz",
                    mensaje,
                    parent=ventana if ventana.winfo_exists() else self.root,
                )

        def worker(nombre):
            try:
                import numpy as np
                import sounddevice as sd

                if not self.hablante_listo:
                    self.cargar_modelo_hablante()
                if not self.hablante_listo:
                    raise RuntimeError(
                        self.hablante_error or "No se pudo cargar el modelo de identidad de voz."
                    )

                self.escuchando = False
                time.sleep(0.8)
                while not self.audio_queue.empty():
                    try:
                        self.audio_queue.get_nowait()
                    except Exception:
                        break

                embeddings = []
                for indice in range(HABLANTE_MUESTRAS_REGISTRO):
                    self.root.after(
                        0,
                        lambda i=indice: actualizar_estado(
                            f"Muestra {i + 1} de {HABLANTE_MUESTRAS_REGISTRO}: "
                            "hable de forma natural durante 4 segundos..."
                        ),
                    )
                    grabacion = sd.rec(
                        int(HABLANTE_SEGUNDOS_MUESTRA * HABLANTE_FRECUENCIA),
                        samplerate=HABLANTE_FRECUENCIA,
                        channels=1,
                        dtype="int16",
                    )
                    sd.wait()
                    pcm = grabacion.reshape(-1).tobytes()
                    emb = self.extraer_embedding_hablante(pcm, HABLANTE_FRECUENCIA)
                    if emb is not None:
                        embeddings.append(emb)
                    time.sleep(0.4)

                if len(embeddings) < 2:
                    raise RuntimeError(
                        "No obtuve suficiente voz clara. Intente nuevamente hablando cerca del micrófono."
                    )

                promedio = np.mean(np.stack(embeddings), axis=0)
                norma = float(np.linalg.norm(promedio))
                if norma <= 1e-8:
                    raise RuntimeError("No pude crear la huella vocal.")
                promedio = (promedio / norma).astype(np.float32)

                if not self.memoria.guardar_voz_autorizada(
                    nombre, promedio.tolist(), len(embeddings)
                ):
                    raise RuntimeError("No pude guardar la huella vocal en beta.db.")

                self.root.after(
                    0,
                    lambda: terminar_registro(
                        True,
                        f"Voz de {nombre} registrada correctamente. Beta ya puede reconocerla.",
                    ),
                )

            except Exception as error:
                self.root.after(
                    0,
                    lambda e=str(error): terminar_registro(False, e),
                )
            finally:
                if not self.escuchando:
                    self.root.after(800, self.iniciar_escucha)

        def iniciar_registro():
            nombre = entrada_nombre.get().strip()
            if not nombre:
                messagebox.showwarning(
                    "Beta", "Escriba el nombre de la persona.", parent=ventana
                )
                return
            if self.registrando_voz:
                return

            self.registrando_voz = True
            boton.configure(state="disabled")
            actualizar_estado("Preparando el micrófono y el modelo de voz...")
            threading.Thread(target=worker, args=(nombre,), daemon=True).start()

        boton.configure(command=iniciar_registro)

    def ventana_administrar_voces(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Voces autorizadas")
        ventana.geometry("620x480")
        ventana.attributes("-topmost", True)

        ttk.Label(
            ventana,
            text="Voces autorizadas para hablar con Beta",
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w", padx=15, pady=(15, 8))

        columnas = ("nombre", "muestras", "fecha")
        tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=9)
        tabla.heading("nombre", text="Nombre")
        tabla.heading("muestras", text="Muestras")
        tabla.heading("fecha", text="Registrada")
        tabla.column("nombre", width=220)
        tabla.column("muestras", width=80, anchor="center")
        tabla.column("fecha", width=190)
        tabla.pack(fill="both", expand=True, padx=15, pady=5)

        def recargar():
            for item in tabla.get_children():
                tabla.delete(item)
            for voz_id, nombre, _emb, muestras, fecha, _activo in self.memoria.listar_voces_autorizadas(False):
                tabla.insert(
                    "", "end", iid=str(voz_id), values=(nombre, muestras, fecha)
                )

        def eliminar():
            seleccion = tabla.selection()
            if not seleccion:
                return
            voz_id = int(seleccion[0])
            valores = tabla.item(seleccion[0], "values")
            nombre = valores[0] if valores else "esta voz"
            if not messagebox.askyesno(
                "Beta",
                f"¿Eliminar la autorización de voz de {nombre}?",
                parent=ventana,
            ):
                return
            self.memoria.eliminar_voz_autorizada(voz_id)
            recargar()
            if self.memoria.cantidad_voces_autorizadas() == 0:
                self.reconocimiento_hablante_activo = False
                self.memoria.cambiar_estado("reconocimiento_hablante", "0")
                try:
                    self.var_reconocimiento_hablante.set(False)
                except Exception:
                    pass

        marco_botones = ttk.Frame(ventana)
        marco_botones.pack(fill="x", padx=15, pady=(4, 8))
        ttk.Button(
            marco_botones,
            text="Registrar otra voz",
            command=self.ventana_registrar_voz,
        ).pack(side="left")
        ttk.Button(
            marco_botones,
            text="Eliminar seleccionada",
            command=eliminar,
        ).pack(side="left", padx=8)

        marco_umbral = ttk.LabelFrame(ventana, text="Nivel de seguridad")
        marco_umbral.pack(fill="x", padx=15, pady=(4, 10))
        variable_umbral = tk.DoubleVar(value=float(self.umbral_hablante))
        etiqueta_umbral = ttk.Label(
            marco_umbral,
            text=f"Umbral: {self.umbral_hablante:.2f}  (más alto = más estricto)",
        )
        etiqueta_umbral.pack(anchor="w", padx=10, pady=(7, 2))

        def cambiar_umbral(valor):
            try:
                nuevo = max(0.30, min(0.75, float(valor)))
            except Exception:
                return
            self.umbral_hablante = nuevo
            self.memoria.cambiar_estado("umbral_hablante", f"{nuevo:.3f}")
            etiqueta_umbral.configure(
                text=f"Umbral: {nuevo:.2f}  (más alto = más estricto)"
            )

        ttk.Scale(
            marco_umbral,
            from_=0.30,
            to=0.75,
            variable=variable_umbral,
            command=cambiar_umbral,
        ).pack(fill="x", padx=10, pady=(0, 8))

        ttk.Label(
            ventana,
            text=(
                "La huella vocal es biométrica y se guarda localmente. "
                "No es una contraseña infalible: una grabación o una voz sintética "
                "podrían intentar imitar al usuario. Para acciones sensibles conviene "
                "mantener confirmaciones adicionales."
            ),
            wraplength=580,
            justify="left",
        ).pack(fill="x", padx=15, pady=(0, 12))

        recargar()

    def iniciar_escucha(self):
        # Protección contra dobles hilos de micrófono. El informe de inicio y su
        # respaldo pueden intentar activar la escucha casi al mismo tiempo.
        if self.escuchando:
            return

        modelo = buscar_modelo_vosk()

        if modelo is None:
            print("ERROR: Modelo Vosk no encontrado:", CARPETA_MODELO)
            self.expresion_confundida()
            return

        self.modelo_vosk = modelo
        self.escuchando = True
        self.expresion_escuchando()

        # Whisper se carga en segundo plano. Mientras termina de cargar,
        # Beta puede seguir funcionando con Vosk como respaldo.
        if USAR_WHISPER:
            threading.Thread(
                target=self.cargar_modelo_whisper,
                daemon=True,
            ).start()

        threading.Thread(
            target=self.escuchar_microfono,
            daemon=True,
        ).start()

    def cargar_modelo_whisper(self):
        if self.whisper_listo or self.whisper_cargando:
            return

        self.whisper_cargando = True

        try:
            from faster_whisper import WhisperModel

            CARPETA_WHISPER.mkdir(parents=True, exist_ok=True)

            # Si el modelo ya está descargado dentro del proyecto, se usa
            # exclusivamente desde disco. En el primer inicio se descarga
            # una sola vez y después ya no necesita Internet.
            archivo_modelo = CARPETA_WHISPER / "model.bin"

            if not archivo_modelo.exists():
                print()
                print("==============================")
                print("PREPARANDO WHISPER PARA BETA")
                print("Primera instalación: descargando el modelo", WHISPER_MODEL)
                print("Esto ocurre una sola vez. Después funciona localmente.")
                print("==============================")
                print()

                try:
                    from huggingface_hub import snapshot_download

                    snapshot_download(
                        repo_id=WHISPER_REPO,
                        local_dir=str(CARPETA_WHISPER),
                    )
                except Exception as error_descarga:
                    raise RuntimeError(
                        "No pude descargar el modelo Whisper. "
                        "Compruebe Internet durante esta primera instalación. "
                        f"Detalle: {error_descarga}"
                    )

            self.modelo_whisper = WhisperModel(
                str(CARPETA_WHISPER),
                device=WHISPER_DEVICE,
                compute_type=WHISPER_COMPUTE_TYPE,
            )

            self.whisper_listo = True
            self.whisper_error = ""

            print()
            print("==============================")
            print("WHISPER LISTO")
            print("Modelo:", WHISPER_MODEL)
            print("Idioma forzado: español")
            print("Modo: Vosk detecta wake word + voz autorizada; Whisper entiende el dictado")
            print("Curiosidad/evaluación: una pregunta explícita de Beta habilita una sola respuesta natural con voz autorizada")
            print("==============================")
            print()

        except ImportError:
            self.whisper_error = (
                "Falta faster-whisper. Ejecute: pip install faster-whisper"
            )
            print(self.whisper_error)
            print("Beta continuará usando Vosk hasta que lo instale.")

        except Exception as error:
            self.whisper_error = str(error)
            print("ERROR CARGANDO WHISPER:", error)
            print("Beta continuará usando Vosk como respaldo.")

        finally:
            self.whisper_cargando = False

    def debe_mejorar_con_whisper(self, texto_vosk):
        texto_normal = normalizar(texto_vosk)
        ahora = time.time()
        self._actualizar_expiracion_modo_conversacion()

        if self.modo_escucha == "conversacion" and ahora <= self.modo_conversacion_hasta:
            return True

        if self.pregunta_curiosa_pendiente and ahora <= self.pregunta_curiosa_hasta:
            return True

        if self.evaluacion_academica_pendiente and ahora <= self.evaluacion_academica_hasta:
            return True

        if self.esperando_orden and ahora <= self.tiempo_limite_orden:
            return True

        # En estricto/silencio solo llegamos a Whisper si Vosk detectó un posible
        # wake word al inicio. Esto evita transcribir conversaciones ambientales.
        return self._wake_en_inicio(texto_normal, incluir_ambiguos=True) is not None

    def transcribir_con_whisper(self, audio_pcm, frecuencia):
        if not self.whisper_listo or self.modelo_whisper is None:
            return ""

        if not audio_pcm:
            return ""

        ruta_temporal = None

        try:
            with tempfile.NamedTemporaryFile(
                suffix=".wav",
                delete=False,
            ) as temporal:
                ruta_temporal = temporal.name

            with wave.open(ruta_temporal, "wb") as wav:
                wav.setnchannels(1)
                wav.setsampwidth(2)
                wav.setframerate(int(frecuencia))
                wav.writeframes(audio_pcm)

            artistas_spotify = ", ".join(self.spotify_vocabulario[:12])
            extra_spotify = (
                " Spotify se pronuncia habitualmente como espótifai; si oye "
                "espotifai, spotifai, espotifay, es potifai o una variante fonética "
                "muy cercana, transcriba la palabra como Spotify. "
            )
            if artistas_spotify:
                extra_spotify += (
                    "Artistas frecuentes del usuario en Spotify: "
                    + artistas_spotify
                    + ". "
                )
            prompt = (
                "Conversación en español de Chile. "
                "El asistente se llama Beta y el usuario es el Señor. "
                "Términos frecuentes: Beta, Spotify, Python, SQL, Windows, Chrome, "
                "Ollama, Qwen, informática, programación, servidor, redes, REPL, PEP8, "
                "Pylint, variables, strings, funciones, listas, tuplas, diccionarios, "
                "clases, herencia, polimorfismo, excepciones, módulos, kwargs, xargs, lambda, "
                "return, def, elif, import, try, except, finally, async, await, Docker, Docker Compose. "
                "En programación Python, si oye algo parecido a 'retur', 'retun' o 'ritern', "
                "transcriba el término como return. "
                + extra_spotify +
                "Transcribe exactamente lo que dice el usuario en español, "
                "normalizando únicamente nombres propios conocidos como Spotify."
            )

            inicio_whisper = time.perf_counter()
            segmentos, info = self.modelo_whisper.transcribe(
                ruta_temporal,
                language=WHISPER_LANGUAGE,
                beam_size=WHISPER_BEAM_SIZE,
                best_of=1,
                temperature=0.0,
                vad_filter=False,
                condition_on_previous_text=False,
                without_timestamps=True,
                initial_prompt=prompt,
            )

            partes = []
            for segmento in segmentos:
                parte = (segmento.text or "").strip()
                if parte:
                    partes.append(parte)

            texto = " ".join(partes).strip()
            texto = re.sub(r"\s+", " ", texto).strip()
            texto = self.corregir_terminos_tecnicos_asr(texto)
            print(f"LATENCIA WHISPER: {time.perf_counter() - inicio_whisper:.2f} s")

            return texto

        except Exception as error:
            print("ERROR TRANSCRIBIENDO CON WHISPER:", error)
            return ""

        finally:
            if ruta_temporal:
                try:
                    os.remove(ruta_temporal)
                except Exception:
                    pass

    def es_comando_rapido_vosk(self, texto_vosk):
        """
        Para órdenes simples y bien reconocidas evitamos una segunda pasada por
        Whisper. Si Vosk no reconoce claramente la intención, Whisper sigue
        siendo el respaldo preciso.
        """
        # Spotify puede llegar como "espotifai"/"spotifai" por su pronunciación.
        t = self._spotify_normalizar_aliases(texto_vosk)
        palabras = set(t.split())

        # Consultas locales/directas que no necesitan análisis lingüístico complejo.
        if palabras & {"temperatura", "clima", "pronostico"}:
            return True
        if "tiempo" in palabras and palabras & {"dime", "esta", "hace", "actual", "manana", "siguiente"}:
            return True
        if "hora" in palabras:
            return True
        if ("hijos" in palabras or "hijo" in palabras or "hija" in palabras) and (
            "nombre" in palabras or "nombres" in palabras or "llaman" in palabras
        ):
            return True
        if palabras & {"calculadora", "explorador"}:
            return True
        # Spotify: si hay artista o búsqueda usamos Whisper para preservar
        # nombres propios. Abrir/pausar/reanudar sin consulta puede ser directo.
        if "spotify" in palabras:
            if palabras & {"busca", "buscar", "buscame", "reproduce", "reproducir", "pon", "toca", "musica", "cancion", "artista"}:
                return False
            return True
        if (palabras & {"reproduce", "pon", "toca"}) and "musica" in palabras:
            return False

        # Órdenes de YouTube con artista/tema usan Whisper para conservar
        # correctamente nombres propios como "Luli Pampín". Abrir YouTube sin
        # una búsqueda puede resolverse directamente con Vosk.
        if palabras & {"youtube", "yutube", "yutu"}:
            if palabras & {
                "busca", "buscar", "buscame", "reproduce", "reproducir",
                "reproduzca", "pon", "poner", "toca", "coloca", "video", "videos",
            }:
                return False
            return True

        # Abrir Chrome sin más es rápido. Si además hay una búsqueda, usamos
        # Whisper para conservar con precisión el tema dictado por el Señor.
        if "chrome" in palabras:
            if palabras & {"busca", "buscar", "buscame", "google", "internet", "imagenes", "fotos"}:
                return False
            return True
        if "bloc" in palabras and "notas" in palabras:
            return True
        if palabras & {"pendientes", "objetivos"}:
            return True
        if "nombre" in palabras and ("beta" in palabras or "veta" in palabras or "meta" in palabras or "metas" in palabras or "petra" in palabras):
            return True
        return False

    def escuchar_microfono(self):
        try:
            import sounddevice as sd
            from vosk import Model, KaldiRecognizer
        except ImportError:
            print("Faltan Vosk o sounddevice. Ejecute: pip install vosk sounddevice")
            self.root.after(0, self.expresion_confundida)
            return

        try:
            modelo = Model(str(self.modelo_vosk))
            dispositivo = sd.query_devices(kind="input")
            frecuencia = int(dispositivo["default_samplerate"])
            self.frecuencia_microfono = frecuencia

            print()
            print("==============================")
            print("BETA ESTÁ ESCUCHANDO")
            print("Micrófono:", dispositivo["name"])
            print("Frecuencia:", frecuencia)
            print("Reconocimiento rápido: Vosk")
            print("Dictado preciso: Faster-Whisper" if USAR_WHISPER else "Dictado preciso: desactivado")
            print("Modo de escucha: ESTRICTO (wake word + voz autorizada)" if self.modo_escucha == "estricto" else f"Modo de escucha: {self.modo_escucha.upper()}")
            print("==============================")
            print()

            reconocedor = KaldiRecognizer(modelo, frecuencia)
            audio_frase = bytearray()

            def callback(indata, frames, time_info, status):
                if status:
                    print("Audio:", status)

                if self.escuchando and not self.hablando:
                    self.audio_queue.put(bytes(indata))

            with sd.RawInputStream(
                samplerate=frecuencia,
                blocksize=4000,
                dtype="int16",
                channels=1,
                callback=callback,
            ):
                while self.escuchando:
                    try:
                        datos = self.audio_queue.get(timeout=0.5)
                    except queue.Empty:
                        continue

                    if self.hablando:
                        audio_frase.clear()
                        continue

                    audio_frase.extend(datos)

                    if reconocedor.AcceptWaveform(datos):
                        resultado = json.loads(reconocedor.Result())
                        texto_vosk = resultado.get("text", "").strip()
                        audio_actual = bytes(audio_frase)
                        audio_frase.clear()

                        if not texto_vosk:
                            continue

                        print("VOSK DETECTÓ:", texto_vosk)

                        # PRIVACIDAD v2.5.2: descartamos aquí cualquier conversación
                        # ambiental que no sea candidata a estar dirigida a Beta.
                        # Así ni Whisper ni la biometría trabajan sobre charlas ajenas.
                        if not self.frase_candidata_para_beta_vosk(texto_vosk):
                            if self.modo_escucha == "silencio":
                                print("MODO SILENCIO: frase ignorada.")
                            else:
                                print("MODO ESTRICTO: frase ambiental sin wake word; ignorada.")
                            continue

                        # Solo después del filtro de wake word verificamos la voz.
                        # En v2.5.4 la existencia de voces autorizadas vuelve esta
                        # verificación obligatoria, aunque un estado antiguo diga lo contrario.
                        debe_validar_voz = (
                            USAR_RECONOCIMIENTO_HABLANTE
                            and self.memoria.cantidad_voces_autorizadas() > 0
                        )
                        if debe_validar_voz:
                            autorizado, nombre_hablante = self.identificar_hablante(
                                audio_actual, frecuencia, texto_vosk
                            )
                            if not autorizado:
                                print("VOZ NO AUTORIZADA: frase ignorada.")
                                self.root.after(0, self.expresion_confundida)
                                continue
                            if nombre_hablante:
                                print("VOZ AUTORIZADA:", nombre_hablante)

                        texto_final = texto_vosk

                        # "meta/metas" son alias demasiado ambiguos para saltarse
                        # Whisper en modo estricto. Si Vosk oyó uno de ellos,
                        # obligamos a Whisper a confirmar y preferimos que la
                        # transcripción final contenga "Beta".
                        rapido_vosk = self.es_comando_rapido_vosk(texto_vosk)
                        if self.modo_escucha != "conversacion" and self.activacion_vosk_ambigua(texto_vosk):
                            rapido_vosk = False

                        if rapido_vosk:
                            print("MODO RÁPIDO: comando directo; se omite Whisper.")

                        # Vosk decide si la frase es candidata. Solo entonces usamos
                        # Whisper, evitando consumir CPU con conversaciones ambientales.
                        if USAR_WHISPER and self.debe_mejorar_con_whisper(texto_vosk) and not rapido_vosk:
                            if self.whisper_listo:
                                self.root.after(0, self.expresion_pensando)
                                texto_whisper = self.transcribir_con_whisper(
                                    audio_actual,
                                    frecuencia,
                                )

                                if texto_whisper:
                                    print("WHISPER ENTENDIÓ:", texto_whisper)
                                    if self.transcripcion_asr_sospechosa(texto_vosk, texto_whisper):
                                        print(
                                            "ASR FILTRO: transcripción sospechosa/boilerplate ignorada "
                                            f"(Vosk='{texto_vosk}' | Whisper='{texto_whisper}')."
                                        )
                                        # Conservamos una ventana abierta tras 'Beta' sola;
                                        # el usuario puede repetir la orden sin reactivar el wake.
                                        self.vaciar_cola_audio_pendiente()
                                        continue
                                    texto_final = texto_whisper

                                    # Si Vosk oyó claramente la palabra de
                                    # activación pero Whisper omitió solo ese
                                    # nombre, conservamos la activación.
                                    vosk_normal = normalizar(texto_vosk)
                                    whisper_normal = normalizar(texto_final)
                                    activaciones_fuertes = ("beta", "veta", "petra")
                                    vosk_tiene_beta_fuerte = self._wake_en_inicio(
                                        vosk_normal, incluir_ambiguos=False
                                    ) is not None
                                    whisper_tiene_beta_fuerte = self._wake_en_inicio(
                                        whisper_normal, incluir_ambiguos=False
                                    ) is not None

                                    # Solo restauramos el wake word si Vosk oyó una
                                    # variante fuerte. Nunca convertimos "meta/metas"
                                    # en Beta automáticamente: eso era una fuente de
                                    # activaciones durante conversaciones normales.
                                    if (
                                        vosk_tiene_beta_fuerte
                                        and not whisper_tiene_beta_fuerte
                                        and self.modo_escucha != "conversacion"
                                        and not self.esperando_orden
                                    ):
                                        texto_final = "Beta " + texto_final
                            elif self.whisper_cargando:
                                print("WHISPER: todavía se está cargando; usando Vosk temporalmente.")
                            elif self.whisper_error:
                                print("WHISPER NO DISPONIBLE:", self.whisper_error)

                        # Whisper tarda varios segundos en CPU y durante ese tiempo
                        # pueden acumularse bloques viejos de la misma frase. Los quitamos
                        # antes de volver al ciclo de escucha para evitar dobles órdenes.
                        if USAR_WHISPER and not rapido_vosk:
                            self.vaciar_cola_audio_pendiente()

                        print("BETA ENTENDIÓ FINALMENTE:", texto_final)
                        self.root.after(
                            0,
                            lambda t=texto_final: self.procesar_voz(t),
                        )

        except Exception as error:
            print("ERROR MICRÓFONO:", error)
            self.root.after(0, self.expresion_confundida)

    def aprender_de_frase_natural(self, frase):
        if self.memoria.obtener_estado("modo_aprendizaje_natural", "1") != "1":
            return False

        original = (frase or "").strip()
        texto = normalizar(original)
        if not texto or len(texto.split()) < 3:
            return False

        # Evitar guardar preguntas como hechos.
        if texto.startswith((
            "que ", "como ", "cual ", "quien ", "cuando ", "donde ",
            "por que ", "puedes ", "podrias ", "me puedes ",
        )):
            return False

        patrones = [
            ("me gusta ", "preferencia", 2),
            ("me encanta ", "preferencia", 2),
            ("prefiero ", "preferencia", 2),
            ("no me gusta ", "preferencia", 2),
            ("estoy estudiando ", "aprendizaje", 2),
            ("estoy aprendiendo ", "aprendizaje", 2),
            ("estoy practicando ", "aprendizaje", 2),
            ("quiero aprender ", "objetivo", 3),
            ("mi objetivo es ", "objetivo", 3),
            ("mi meta es ", "objetivo", 3),
            ("tengo pendiente ", "pendiente", 3),
            ("tenemos pendiente ", "pendiente", 3),
            ("mañana quiero ", "pendiente", 2),
            ("manana quiero ", "pendiente", 2),
            ("mi proyecto es ", "proyecto", 2),
            ("estoy construyendo ", "proyecto", 2),
            ("estoy desarrollando ", "proyecto", 2),
        ]

        for patron, tipo, importancia in patrones:
            if texto.startswith(patron):
                guardado = self.memoria.guardar_recuerdo(
                    original,
                    importancia=importancia,
                    tipo=tipo,
                )
                if guardado:
                    print(f"APRENDIZAJE NATURAL [{tipo}]: {original}")
                return guardado

        return False

    # ======================================================
    # MEMORIA INTELIGENTE / CONTEXTO CONVERSACIONAL
    # ======================================================

    def es_dato_sensible_para_no_guardar(self, texto):
        """Evita memorizar automáticamente credenciales o secretos evidentes.

        Los recuerdos explícitos mediante "recuerda que..." siguen bajo control
        del Señor; esta protección se aplica al aprendizaje automático.
        """
        t = normalizar(texto)
        patrones = [
            "contrasena", "password", "clave bancaria", "pin bancario",
            "codigo de seguridad", "cvv", "numero de tarjeta", "token de acceso",
            "api key", "clave api", "frase semilla", "seed phrase",
        ]
        return any(p in t for p in patrones)

    def es_mensaje_memorizable(self, texto):
        """Filtra comandos/ruido y deja pasar conversación personal útil."""
        original = (texto or "").strip()
        t = normalizar(original)
        if not t or len(t.split()) < MEMORIA_INTELIGENTE_MIN_PALABRAS:
            return False
        if self.es_dato_sensible_para_no_guardar(original):
            return False

        # Preguntas puras normalmente consultan información; no son un hecho nuevo.
        interrogativos = (
            "que ", "como ", "cual ", "quien ", "cuando ", "donde ",
            "por que ", "puedes ", "podrias ", "me puedes ", "cuanto ",
        )
        if t.startswith(interrogativos):
            return False

        # Comandos operativos no deben convertirse en recuerdos personales.
        comandos = (
            "abre ", "abrir ", "busca ", "buscar ", "reproduce ", "pon ",
            "crea ", "crear ", "borra ", "elimina ", "mueve ", "copia ",
            "renombra ", "ejecuta ", "inicia ", "apaga ", "reinicia ",
            "investiga ", "averigua ", "explicame ", "explica ", "define ",
            "defineme ", "dame ", "entregame ", "hablame ", "cuentame ",
            "resumeme ", "resume ", "muestrame ", "ensename ", "preguntame ",
            "compara ", "describeme ", "aclarame ", "ayudame ",
            "dime la temperatura", "dime el clima", "dime el tiempo",
            "muestrame las fuentes", "abre la primera fuente",
        )
        if t.startswith(comandos):
            return False

        # Las órdenes de tutoría describen una consulta, no una preferencia personal.
        # No guardamos "según mis apuntes...", "dame un ejemplo" o "profundiza"
        # como si fueran hechos sobre el Señor.
        if any(m in t for m in (
            "segun mis apuntes", "en base a mis apuntes", "busca en mis apuntes",
            "dame un ejemplo", "otro ejemplo", "profundiza", "explicame mas",
            "hablame sobre", "puedes hablarme sobre", "consulta mis apuntes",
        )):
            return False

        # Afirmaciones en primera persona y datos relacionales suelen ser útiles.
        indicadores = [
            "yo ", "mi ", "mis ", "me ", "estoy ", "tengo ", "quiero ",
            "prefiero ", "trabajo ", "estudio ", "aprendo ", "vivo ",
            "mi esposa", "mi hijo", "mi hija", "mis hijos", "mi perro",
            "mi gato", "mis gatos", "me gusta", "me encanta", "no me gusta",
            "mi objetivo", "mi meta", "mi proyecto", "tengo pendiente",
        ]
        return any(ind in (t + " ") for ind in indicadores)

    def programar_memoria_inteligente(self, mensaje_usuario, respuesta_beta=""):
        if not self.modo_memoria_inteligente:
            return
        if time.time() - getattr(self, "ultima_respuesta_curiosa_ts", 0.0) < 3.0:
            return
        mensaje_usuario = (mensaje_usuario or "").strip()
        if not self.es_mensaje_memorizable(mensaje_usuario):
            return

        self.turnos_desde_resumen += 1
        self.memoria.cambiar_estado("turnos_desde_resumen", self.turnos_desde_resumen)
        self.cola_memoria_inteligente.put(
            {
                "usuario": mensaje_usuario,
                "beta": (respuesta_beta or "").strip(),
                "ts": time.time(),
            }
        )

    def worker_memoria_inteligente(self):
        """Analiza conversación en baja prioridad sin retrasar la respuesta principal."""
        while True:
            try:
                item = self.cola_memoria_inteligente.get()
            except Exception:
                time.sleep(1)
                continue

            try:
                # Esperar a que el Señor deje de hablar y Beta termine la respuesta.
                # Si llega otra intervención, el contador vuelve a empezar de forma natural.
                while True:
                    inactividad = time.time() - self.ultima_interaccion_voz
                    conversacion_activa = (
                        self.modo_escucha == "conversacion"
                        and time.time() <= self.modo_conversacion_hasta
                    )
                    es_curiosidad = bool(item.get("pregunta_curiosa"))
                    espera_objetivo = 8 if es_curiosidad else MEMORIA_INTELIGENTE_ESPERA
                    # Las respuestas a preguntas curiosas son explícitas y pueden
                    # consolidarse antes; el resto espera a que termine la sesión.
                    if (
                        inactividad >= espera_objetivo
                        and not self.hablando
                        and not self.procesando
                        and (es_curiosidad or not conversacion_activa)
                    ):
                        break
                    time.sleep(1.0)

                with self.memoria_inteligente_lock:
                    self.analizar_turno_para_memoria(item)
                    if self.turnos_desde_resumen >= RESUMEN_CONVERSACION_CADA_TURNOS:
                        self.crear_resumen_conversacion_inteligente()
            except Exception as error:
                print("ERROR MEMORIA INTELIGENTE:", error)
            finally:
                try:
                    self.cola_memoria_inteligente.task_done()
                except Exception:
                    pass

    def extraer_json_de_texto(self, texto):
        if not texto:
            return None
        limpio = texto.strip()
        limpio = re.sub(r"^```(?:json)?\s*", "", limpio, flags=re.IGNORECASE)
        limpio = re.sub(r"\s*```$", "", limpio)
        inicio = limpio.find("{")
        fin = limpio.rfind("}")
        if inicio == -1 or fin == -1 or fin <= inicio:
            return None
        try:
            return json.loads(limpio[inicio:fin + 1])
        except Exception:
            return None

    def analizar_turno_para_memoria(self, item):
        usuario = (item.get("usuario") or "").strip()
        respuesta_beta = (item.get("beta") or "").strip()
        pregunta_curiosa = (item.get("pregunta_curiosa") or "").strip()
        tema_curioso = (item.get("tema_curioso") or "").strip()
        if not usuario:
            return

        contexto_usuario = usuario
        if pregunta_curiosa:
            contexto_usuario = (
                f"PREGUNTA QUE BETA HIZO AL SEÑOR:\n{pregunta_curiosa}\n\n"
                f"RESPUESTA EXPLÍCITA DEL SEÑOR:\n{usuario}"
            )

        mensajes = [
            {
                "role": "system",
                "content": (
                    "Eres el módulo local de memoria de Beta. Analiza SOLO lo que el usuario afirma explícitamente. "
                    "No inventes, no deduzcas datos no dichos y no conviertas preguntas, órdenes de explicación "
                    "o solicitudes académicas en hechos personales. "
                    "Nunca escribas que el Señor entendió, aprendió o comprendió algo salvo que él lo haya afirmado "
                    "de forma explícita con frases como 'entendí', 'aprendí' o 'ya comprendí'. "
                    "No guardes contraseñas, PIN, tokens, números de tarjeta ni secretos de acceso. "
                    "Devuelve SOLO JSON válido con esta forma: "
                    '{"tema":"tema breve","resumen_turno":"una frase breve","recuerdos":['
                    '{"contenido":"hecho autosuficiente","tipo":"dato|persona|preferencia|aprendizaje|objetivo|pendiente|proyecto",'
                    '"importancia":1,"confianza":0.0}]}. '
                    "Usa importancia 1 a 3. Confianza debe ser 0 a 1. "
                    "Si no hay nada útil para memoria a largo plazo, recuerdos debe ser []. "
                    "Escribe los recuerdos en español y preferentemente como 'El Señor...' para que sean autosuficientes."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"{contexto_usuario}\n\n"
                    "Extrae recuerdos únicamente de lo que el Señor respondió o afirmó explícitamente. "
                    "La pregunta de Beta solo aporta contexto y nunca debe convertirse por sí sola en un recuerdo."
                ),
            },
        ]

        inicio = time.perf_counter()
        respuesta = self.enviar_ollama(mensajes, temperatura=0.05, num_predict=220)
        if not respuesta:
            return
        datos = self.extraer_json_de_texto(self.limpiar_respuesta_ollama(respuesta))
        if not isinstance(datos, dict):
            print("MEMORIA INTELIGENTE: JSON no interpretable; se omite el turno.")
            return

        tema = str(datos.get("tema") or "").strip()
        resumen_turno = str(datos.get("resumen_turno") or "").strip()
        recuerdos = datos.get("recuerdos") or []
        guardados = 0

        tipos_validos = {
            "dato", "persona", "preferencia", "aprendizaje",
            "objetivo", "pendiente", "proyecto",
        }

        if isinstance(recuerdos, list):
            for candidato in recuerdos[:4]:
                if not isinstance(candidato, dict):
                    continue
                contenido = str(candidato.get("contenido") or "").strip()
                tipo = normalizar(str(candidato.get("tipo") or "dato")) or "dato"
                if tipo not in tipos_validos:
                    tipo = "dato"
                try:
                    importancia = max(1, min(3, int(candidato.get("importancia", 1))))
                except Exception:
                    importancia = 1
                try:
                    confianza = float(candidato.get("confianza", 0.8))
                except Exception:
                    confianza = 0.8

                # Exigimos una confianza razonable y una frase que tenga contenido real.
                if confianza < 0.72 or len(normalizar(contenido).split()) < 4:
                    continue
                if self.es_dato_sensible_para_no_guardar(contenido):
                    continue

                nuevo = self.memoria.guardar_recuerdo(
                    contenido,
                    importancia=importancia,
                    tipo=tipo,
                    fuente="curiosidad_usuario" if pregunta_curiosa else "conversacion_ia",
                    confianza=confianza,
                    tema=tema or tema_curioso,
                )
                if nuevo:
                    guardados += 1
                    print(f"MEMORIA INTELIGENTE [{tipo}] + {contenido}")

        if tema:
            self.contexto_tema = tema
            self.contexto_actualizado_ts = time.time()
            self.memoria.cambiar_estado("contexto_tema", tema)
        if resumen_turno:
            self.contexto_resumen = resumen_turno
            self.memoria.cambiar_estado("contexto_resumen", resumen_turno)

        print(
            f"MEMORIA INTELIGENTE: {guardados} recuerdo(s) nuevo(s) "
            f"en {time.perf_counter() - inicio:.2f} s. Tema: {tema or 'sin tema'}"
        )

    def crear_resumen_conversacion_inteligente(self):
        historial = self.memoria.historial_reciente(16)
        if len(historial) < 6:
            return

        lineas = []
        for autor, mensaje, _fecha in historial:
            # Limitar cada línea mantiene rápido el contexto para Qwen.
            lineas.append(f"{autor}: {mensaje[:500]}")
        transcripcion = "\n".join(lineas)

        mensajes = [
            {
                "role": "system",
                "content": (
                    "Resume una conversación entre el Señor y Beta para memoria de largo plazo. "
                    "Conserva hechos explícitos, temas, decisiones, objetivos, avances y pendientes. "
                    "No inventes. No copies saludos ni órdenes operativas irrelevantes. "
                    "Devuelve SOLO JSON válido: "
                    '{"tema":"tema principal","resumen":"resumen de 2 a 4 frases"}.'
                ),
            },
            {"role": "user", "content": transcripcion},
        ]
        respuesta = self.enviar_ollama(mensajes, temperatura=0.08, num_predict=180)
        datos = self.extraer_json_de_texto(self.limpiar_respuesta_ollama(respuesta or ""))
        if not isinstance(datos, dict):
            return

        tema = str(datos.get("tema") or self.contexto_tema or "").strip()
        resumen = str(datos.get("resumen") or "").strip()
        if resumen:
            if self.memoria.guardar_resumen_conversacion(
                resumen,
                tema=tema,
                turnos=self.turnos_desde_resumen,
            ):
                print("RESUMEN DE CONVERSACIÓN GUARDADO:", resumen[:180])
            self.contexto_resumen = resumen
            self.contexto_tema = tema
            self.memoria.cambiar_estado("contexto_resumen", resumen)
            self.memoria.cambiar_estado("contexto_tema", tema)

        self.turnos_desde_resumen = 0
        self.memoria.cambiar_estado("turnos_desde_resumen", "0")

    def debe_hacer_pregunta_seguimiento(self, mensaje):
        if not self.preguntas_seguimiento:
            return False
        t = normalizar(mensaje)
        if not t or len(t.split()) < 4:
            return False
        if "?" in (mensaje or ""):
            return False
        if t.startswith((
            "abre ", "busca ", "reproduce ", "pon ", "crea ", "borra ",
            "dime ", "investiga ", "averigua ", "recuerda ", "aprende ",
        )):
            return False
        return self.es_mensaje_memorizable(mensaje)

    def actualizar_contexto_turno(self, autor, mensaje):
        mensaje = (mensaje or "").strip()
        if not mensaje:
            return
        self.contexto_turnos.append((autor, mensaje))
        self.contexto_turnos = self.contexto_turnos[-8:]
        self.contexto_actualizado_ts = time.time()

    def _reiniciar_contador_curiosidad_si_corresponde(self):
        hoy = datetime.now().strftime("%Y-%m-%d")
        fecha = self.memoria.obtener_estado("curiosidad_fecha_contador", "") or ""
        if fecha != hoy:
            self.memoria.cambiar_estado("curiosidad_fecha_contador", hoy)
            self.memoria.cambiar_estado("curiosidad_preguntas_hoy", "0")

    def preguntas_curiosas_hoy(self):
        self._reiniciar_contador_curiosidad_si_corresponde()
        try:
            return int(self.memoria.obtener_estado("curiosidad_preguntas_hoy", "0") or 0)
        except Exception:
            return 0

    def incrementar_preguntas_curiosas_hoy(self):
        n = self.preguntas_curiosas_hoy() + 1
        self.memoria.cambiar_estado("curiosidad_preguntas_hoy", str(n))
        return n

    def cancelar_pregunta_curiosa(self, motivo=""):
        if self.pregunta_curiosa_pendiente and motivo:
            print(f"CURIOSIDAD: pregunta pendiente cerrada ({motivo}).")
        self.pregunta_curiosa_pendiente = None
        self.pregunta_curiosa_id = 0
        self.pregunta_curiosa_hasta = 0.0
        self.pregunta_curiosa_tema = ""
        self.pregunta_curiosa_tipo = "dato"

    def pregunta_curiosa_es_segura(self, pregunta):
        t = normalizar(pregunta)
        prohibidos = [
            "contrasena", "password", "pin", "tarjeta", "cvv", "rut", "documento de identidad",
            "direccion exacta", "cuenta bancaria", "sueldo", "ingresos", "deuda", "salud", "diagnostico",
            "enfermedad", "medicamento", "religion", "partido politico", "orientacion sexual", "vida sexual",
        ]
        if any(p in t for p in prohibidos):
            return False
        return 5 <= len(t.split()) <= 35 and "?" in pregunta

    def procesar_respuesta_curiosa(self, respuesta):
        respuesta = (respuesta or "").strip()
        if not self.pregunta_curiosa_pendiente or not respuesta:
            return

        pregunta = self.pregunta_curiosa_pendiente
        pregunta_id = self.pregunta_curiosa_id
        tema = self.pregunta_curiosa_tema
        self.cancelar_pregunta_curiosa()
        self.ultima_interaccion_voz = time.time()
        self.memoria.guardar_conversacion("Señor", respuesta)
        self.ultimo_mensaje_usuario = respuesta
        self.actualizar_contexto_turno("Señor", respuesta)
        self.memoria.marcar_pregunta_curiosa_respondida(pregunta_id, respuesta)
        self.ultima_respuesta_curiosa_ts = time.time()

        if self.es_dato_sensible_para_no_guardar(respuesta):
            self.responder(
                "entiendo. Por privacidad no guardaré esa respuesta en mi memoria automática.",
                "normal",
                tipo_contexto="curiosidad",
            )
            return

        self.cola_memoria_inteligente.put({
            "usuario": respuesta,
            "beta": "",
            "pregunta_curiosa": pregunta,
            "tema_curioso": tema,
            "ts": time.time(),
        })
        print(f"CURIOSIDAD: respuesta recibida para '{pregunta[:90]}'. Se consolidará en memoria.")
        self.responder(
            "entiendo, Señor. Gracias por contármelo; lo tendré en cuenta para conocerlo mejor.",
            "feliz",
            tipo_contexto="curiosidad",
        )

    def responder_aprendizajes_curiosos(self):
        recuerdos = self.memoria.recuerdos_por_fuente("curiosidad_usuario", limite=7)
        if not recuerdos:
            self.responder(
                "todavía no he consolidado recuerdos nacidos de mis propias preguntas. Podemos empezar cuando quiera.",
                "normal",
            )
            return
        textos = []
        for r in recuerdos:
            contenido = (r[1] or "").strip().rstrip(".")
            if contenido and contenido not in textos:
                textos.append(contenido)
        self.responder(
            "por nuestras conversaciones he aprendido que " + "; ".join(textos[:6]) + ".",
            "feliz",
        )

    def generar_pregunta_curiosa_async(self, forzada=False):
        if not forzada and not self.modo_curioso:
            return
        if self.pregunta_curiosa_pendiente and time.time() <= self.pregunta_curiosa_hasta:
            return
        if not forzada and self.preguntas_curiosas_hoy() >= CURIOSIDAD_MAX_PREGUNTAS_DIA:
            return
        if self.hablando or self.procesando or self.modo_escucha == "silencio":
            return

        token = self.iniciar_proceso("curiosidad")
        if token is None:
            return

        recuerdos = self.memoria.recuerdos_para_iniciativa(10)
        historial = self.memoria.ultimas_preguntas_curiosas(18)
        memoria_texto = "\n".join(f"- {r[1]}" for r in recuerdos[:8]) or "- Aún conozco pocas cosas."
        previas_texto = "\n".join(f"- {r[1]}" for r in historial[:12]) or "- Ninguna todavía."

        def trabajo():
            pregunta = ""
            tema = "conocer al Señor"
            tipo = "dato"
            try:
                mensajes = [
                    {
                        "role": "system",
                        "content": (
                            "Eres Beta. Tu objetivo es conocer gradualmente al Señor como una compañera curiosa, "
                            "sin invadir su privacidad. Haz UNA sola pregunta breve, natural y abierta. "
                            "Temas permitidos: estudios, informática, formas de aprender, proyectos, hobbies, "
                            "gustos culturales, rutinas de estudio, preferencias sobre cómo ayudarlo y metas. "
                            "No preguntes por salud, religión, política, finanzas, contraseñas, documentos, dirección exacta, "
                            "sexualidad ni otros datos sensibles. No repitas algo que ya esté en los recuerdos ni preguntas previas. "
                            "La pregunta debe invitar a responder con una frase, no solo sí/no. "
                            "Devuelve SOLO JSON: {\"pregunta\":\"... ?\",\"tema\":\"...\","
                            "\"tipo\":\"dato|preferencia|aprendizaje|objetivo|proyecto\"}."
                        ),
                    },
                    {
                        "role": "user",
                        "content": f"RECUERDOS YA CONOCIDOS:\n{memoria_texto}\n\nPREGUNTAS YA HECHAS:\n{previas_texto}",
                    },
                ]
                r = self.enviar_ollama(mensajes, temperatura=0.45, num_predict=100)
                datos = self.extraer_json_de_texto(self.limpiar_respuesta_ollama(r or ""))
                if isinstance(datos, dict):
                    pregunta = str(datos.get("pregunta") or "").strip()
                    tema = str(datos.get("tema") or tema).strip()
                    tipo = normalizar(str(datos.get("tipo") or tipo)) or "dato"
                if tipo not in {"dato", "preferencia", "aprendizaje", "objetivo", "proyecto"}:
                    tipo = "dato"
                if not self.pregunta_curiosa_es_segura(pregunta):
                    pregunta = "Señor, me dio curiosidad: ¿qué parte de la informática disfruta más aprender y qué es lo que le atrae de ella?"
                    tema = "intereses de informática"
                    tipo = "preferencia"
            except Exception as error:
                print("ERROR CURIOSIDAD:", error)
                pregunta = "Señor, me dio curiosidad: ¿qué parte de la informática disfruta más aprender y qué es lo que le atrae de ella?"
                tema = "intereses de informática"
                tipo = "preferencia"
            finally:
                self.terminar_proceso(token)

            if token != self.proceso_id or not pregunta:
                return

            def anunciar():
                self.pregunta_curiosa_pendiente = pregunta
                self.pregunta_curiosa_tema = tema
                self.pregunta_curiosa_tipo = tipo
                self.pregunta_curiosa_id = self.memoria.registrar_pregunta_curiosa(pregunta, tema, tipo)
                self.pregunta_curiosa_hasta = time.time() + CURIOSIDAD_RESPUESTA_SEGUNDOS
                self.interacciones_desde_curiosidad = 0
                self.proxima_pregunta_curiosa_ts = time.time() + random.randint(
                    CURIOSIDAD_MIN_SEGUNDOS, CURIOSIDAD_MAX_SEGUNDOS
                )
                self.incrementar_preguntas_curiosas_hoy()
                print(f"CURIOSIDAD: pregunta abierta por {CURIOSIDAD_RESPUESTA_SEGUNDOS} s | tema={tema}")
                self.responder(pregunta, "feliz", tipo_contexto="curiosidad")

            self.root.after(0, anunciar)

        threading.Thread(target=trabajo, daemon=True).start()

    def vigilar_curiosidad(self):
        try:
            ahora = time.time()
            hora = datetime.now().hour
            if self.pregunta_curiosa_pendiente and ahora > self.pregunta_curiosa_hasta:
                self.cancelar_pregunta_curiosa("sin respuesta")

            actividad_reciente = ahora - self.ultima_interaccion_voz <= 8 * 60
            condiciones = (
                self.modo_curioso
                and CURIOSIDAD_HORA_INICIO <= hora < CURIOSIDAD_HORA_FIN
                and ahora >= self.proxima_pregunta_curiosa_ts
                and self.interacciones_desde_curiosidad >= CURIOSIDAD_MIN_INTERACCIONES
                and self.preguntas_curiosas_hoy() < CURIOSIDAD_MAX_PREGUNTAS_DIA
                and actividad_reciente
                and not self.pregunta_curiosa_pendiente
                and not self.hablando
                and not self.procesando
                and not self.esperando_orden
                and self.modo_escucha != "silencio"
            )
            if condiciones:
                self.generar_pregunta_curiosa_async(forzada=False)
        except Exception as error:
            print("ERROR VIGILANDO CURIOSIDAD:", error)
        finally:
            self.root.after(60000, self.vigilar_curiosidad)

    def responder_pendientes(self):
        pendientes = self.memoria.recuerdos_por_tipo("pendiente", limite=6)
        if not pendientes:
            self.responder("no tengo pendientes guardados en mi memoria.", "normal")
            return

        textos = [p[1].strip().rstrip(".") for p in pendientes if p[1].strip()]
        if len(textos) == 1:
            respuesta = "tiene pendiente: " + textos[0] + "."
        else:
            respuesta = "tiene pendientes: " + "; ".join(textos) + "."
        self.responder(respuesta, "feliz")

    def responder_memoria_familiar(self, texto):
        """Ruta rápida para preguntas por los hijos, sin mezclar otros familiares."""
        patrones_hijos = [
            "nombre de mis hijos", "nombres de mis hijos", "como se llaman mis hijos",
            "como llaman mis hijos", "quienes son mis hijos", "quien son mis hijos",
        ]
        if not any(p in texto for p in patrones_hijos):
            return False

        candidatos = []
        ids = set()
        for consulta in ["mis hijos", "hijos se llaman", "hijo", "hija", "nombre hijos"]:
            for recuerdo in self.memoria.buscar_recuerdos(consulta, limite=10):
                contenido_norm = recuerdo[2] or ""
                # Regla estricta: una respuesta sobre hijos no puede provenir de
                # recuerdos que solo hablen de esposa, mascota u otra relación.
                if not re.search(r"\b(?:hijo|hijos|hija|hijas)\b", contenido_norm):
                    continue
                if recuerdo[0] not in ids:
                    ids.add(recuerdo[0])
                    candidatos.append(recuerdo)

        if not candidatos:
            self.responder(
                "no tengo guardados claramente los nombres de sus hijos. Puede enseñármelos diciendo: Beta, recuerda que mis hijos se llaman...",
                "confundida",
            )
            return True

        candidatos.sort(key=lambda r: (r[4], r[0]), reverse=True)
        textos = []
        for r in candidatos[:4]:
            contenido = r[1].strip().rstrip(".")
            if contenido and contenido not in textos:
                textos.append(contenido)

        if textos:
            self.responder("recuerdo que " + "; ".join(textos) + ".", "feliz")
        else:
            self.responder("no encontré los nombres de sus hijos en mi memoria.", "confundida")
        return True

    def responder_aprendizajes_directos(self):
        aprendizajes = self.memoria.recuerdos_por_tipo("aprendizaje", limite=6)
        if not aprendizajes:
            self.responder("todavía no tengo aprendizajes suyos guardados en mi memoria.", "normal")
            return
        textos = [r[1].strip().rstrip(".") for r in aprendizajes if r[1].strip()]
        self.responder("recuerdo que " + "; ".join(textos) + ".", "feliz")

    def responder_objetivos_directos(self):
        objetivos = self.memoria.recuerdos_por_tipo("objetivo", limite=6)
        if not objetivos:
            self.responder("todavía no tengo objetivos suyos guardados en mi memoria.", "normal")
            return
        textos = [r[1].strip().rstrip(".") for r in objetivos if r[1].strip()]
        self.responder("sus objetivos guardados son: " + "; ".join(textos) + ".", "feliz")

    # ======================================================
    # PROCESAR VOZ / CEREBRO
    # ======================================================

    def procesar_voz(self, texto):
        texto_original = (texto or "").strip()
        texto_normal = normalizar(texto_original)
        self.registrar_actividad()
        self._actualizar_expiracion_modo_conversacion()
        ahora = time.time()

        # SILENCIO: se ignora todo salvo una orden explícita de despertar con
        # wake word fuerte. El filtro de Vosk ya evita biometría/Whisper para
        # el resto, pero repetimos la regla aquí como segunda barrera.
        if self.modo_escucha == "silencio":
            if self._orden_despertar_silencio(texto_normal):
                self.establecer_modo_escucha("estricto", anunciar=True)
            else:
                print("MODO SILENCIO: orden no autorizada para despertar; ignorada.")
            return

        # RESPUESTA A UNA EVALUACIÓN ACADÉMICA. Se acepta una sola respuesta
        # natural sin wake word, siempre después de la validación biométrica.
        if self.evaluacion_academica_pendiente and ahora <= self.evaluacion_academica_hasta:
            wake_eval = self._wake_en_inicio(texto_normal, incluir_ambiguos=False)
            if wake_eval is None:
                self.procesar_respuesta_evaluacion(texto_original)
                return
        if self.evaluacion_academica_pendiente and ahora > self.evaluacion_academica_hasta:
            self.cancelar_evaluacion_academica(anunciar=False)

        # RESPUESTA A UNA PREGUNTA CURIOSA. Cuando Beta formula una pregunta
        # explícita, la siguiente respuesta puede llegar sin wake word. La capa
        # de audio ya exigió voz autorizada, por lo que aquí solo capturamos
        # una respuesta natural y cerramos inmediatamente esa ventana.
        if self.pregunta_curiosa_pendiente and ahora <= self.pregunta_curiosa_hasta:
            wake_curioso = self._wake_en_inicio(texto_normal, incluir_ambiguos=False)
            if wake_curioso is None:
                self.procesar_respuesta_curiosa(texto_original)
                return

        if self.pregunta_curiosa_pendiente and ahora > self.pregunta_curiosa_hasta:
            self.cancelar_pregunta_curiosa("tiempo agotado")

        # CONVERSACIÓN EXPLÍCITA: solo aquí se aceptan frases sin decir Beta.
        if self.modo_escucha == "conversacion" and ahora <= self.modo_conversacion_hasta:
            if (
                self.memoria.cantidad_voces_autorizadas() > 0
                and not self.hablante_sesion_conversacion
            ):
                print("PRIVACIDAD: sesión conversacional sin propietario; cerrando por seguridad.")
                self.establecer_modo_escucha("estricto", anunciar=False)
                return
            restante = max(0.0, self.modo_conversacion_hasta - ahora)
            print(
                f"MODO CONVERSACIÓN: aceptando frase sin wake word "
                f"({restante:.1f} s restantes)."
            )
            self.renovar_modo_conversacion()
            self.procesar_orden(texto_original)
            return

        # "Beta" sola abre una ventana MUY corta para la siguiente orden. Esta
        # ventana no se vuelve a abrir automáticamente tras las respuestas.
        if self.esperando_orden:
            if ahora <= self.tiempo_limite_orden:
                self.esperando_orden = False
                self.procesar_orden(texto_original)
                return
            self.esperando_orden = False
            self.tiempo_limite_orden = 0.0

        # ESTRICTO: exigimos una activación fuerte al inicio (o "gracias Beta"
        # al final). "meta/metas" sirven para despertar Whisper, pero si Whisper
        # no los confirma como Beta/veta/petra, aquí se descartan.
        wake = self._wake_en_inicio(texto_normal, incluir_ambiguos=False)
        if wake is None:
            print("MODO ESTRICTO: transcripción final sin wake word fuerte; ignorada.")
            return

        # "Gracias Beta" es una despedida breve, no una nueva sesión abierta.
        palabras_actuales = texto_normal.split()
        if any(x in texto_normal for x in ["gracias", "muchas gracias", "te agradezco"]):
            if len(palabras_actuales) <= 7:
                self.ultima_frase_inicio = time.perf_counter()
                self.responder("de nada. Me alegra poder ayudarle.", "feliz")
                return

        # Extraemos solo lo que viene después del wake word. Para "Hola Beta"
        # buscamos la posición real de la palabra dentro de la frase normalizada.
        palabras = texto_normal.split()
        try:
            indice = palabras.index(wake)
        except ValueError:
            indice = 0
        orden = " ".join(palabras[indice + 1:]).strip()

        if orden:
            self.procesar_orden(orden)
        else:
            self.esperando_orden = True
            self.tiempo_limite_orden = time.time() + TIEMPO_ORDEN_TRAS_WAKE
            self.ultima_frase_inicio = time.perf_counter()
            print(
                f"WAKE WORD CONFIRMADO: esperando orden durante "
                f"{TIEMPO_ORDEN_TRAS_WAKE} s."
            )
            self.responder("dígame.", "escuchando")

    def procesar_orden(self, comando):
        comando = (comando or "").strip()
        if not comando:
            return

        self.registrar_actividad()
        self.ultima_interaccion_voz = time.time()
        if self.modo_escucha == "conversacion":
            self.renovar_modo_conversacion()
        self.memoria.guardar_conversacion("Señor", comando)
        self.ultimo_mensaje_usuario = comando
        self.actualizar_contexto_turno("Señor", comando)
        self.memoria.registrar_interaccion()
        self.interacciones_desde_curiosidad += 1
        self.expresion_pensando()
        self.ultima_frase_inicio = time.perf_counter()

        # No agregamos demora artificial antes de enrutar la orden.
        self.root.after(0, lambda: self.ejecutar_comando(comando))

    def ejecutar_comando(self, comando):
        original = comando.strip()
        texto = normalizar(comando)
        print(f"RUTA DE RESPUESTA iniciada: {texto}")

        # 0) Curiosidad y aprendizaje activo. Son rutas locales de control;
        # nunca necesitan Internet ni deben caer al chat general.
        if any(frase in texto for frase in [
            "activa modo curioso", "activar modo curioso", "se mas curiosa",
            "quiero que seas curiosa", "quiero que me preguntes cosas",
        ]):
            self.modo_curioso = True
            self.memoria.cambiar_estado("modo_curioso", "1")
            try:
                self.var_modo_curioso.set(True)
            except Exception:
                pass
            self.responder(
                "activé el modo curioso. Iré conociéndolo poco a poco y recordaré sus respuestas explícitas.",
                "feliz",
            )
            return

        if any(frase in texto for frase in [
            "desactiva modo curioso", "desactivar modo curioso", "deja de preguntarme cosas",
            "no me hagas preguntas",
        ]):
            self.modo_curioso = False
            self.memoria.cambiar_estado("modo_curioso", "0")
            self.cancelar_pregunta_curiosa("modo curioso desactivado")
            try:
                self.var_modo_curioso.set(False)
            except Exception:
                pass
            self.responder(
                "desactivé el modo curioso. Seguiré recordando lo ya aprendido, pero no iniciaré nuevas preguntas.",
                "normal",
            )
            return

        if (
            texto in {"hazme una pregunta", "preguntame algo"}
            or "preguntame algo para conocerme" in texto
            or "quiero que me conozcas" in texto
            or "conoceme mejor" in texto
        ):
            self.generar_pregunta_curiosa_async(forzada=True)
            return

        if any(frase in texto for frase in [
            "que has aprendido de mi", "que aprendiste de mi", "que sabes de mi por tus preguntas",
        ]):
            self.responder_aprendizajes_curiosos()
            return

        # Unidad de aprendizaje adaptativo.
        if any(frase in texto for frase in ["activa aprendizaje adaptativo","activar aprendizaje adaptativo","activa modo aprendizaje","activar modo aprendizaje"]):
            self.modo_aprendizaje_adaptativo=True; self.memoria.cambiar_estado("modo_aprendizaje_adaptativo","1")
            try: self.var_aprendizaje_adaptativo.set(True)
            except Exception: pass
            self.responder("aprendizaje adaptativo activado. Registraré evidencia real de estudio y evaluación.","feliz"); return
        if any(frase in texto for frase in ["desactiva aprendizaje adaptativo","desactivar aprendizaje adaptativo","desactiva modo aprendizaje","desactivar modo aprendizaje"]):
            self.modo_aprendizaje_adaptativo=False; self.memoria.cambiar_estado("modo_aprendizaje_adaptativo","0")
            try: self.var_aprendizaje_adaptativo.set(False)
            except Exception: pass
            self.responder("aprendizaje adaptativo desactivado. Conservaré el progreso ya registrado.","normal"); return
        if any(frase in texto for frase in ["como voy en mis estudios","como voy estudiando","mi progreso academico","muestrame mi progreso","cual es mi progreso","como esta mi progreso"]):
            self.responder_progreso_academico(); return
        if any(frase in texto for frase in ["que deberia repasar","que tengo que repasar","que necesito reforzar","que tema debo reforzar","que me recomiendas repasar"]):
            self.responder_recomendacion_repaso(); return
        if any(frase in texto for frase in ["termina evaluacion","termina la evaluacion","termino evaluacion","termino la evaluacion","finaliza evaluacion","cancela evaluacion"]):
            self.cancelar_evaluacion_academica(anunciar=True); return
        if any(frase in texto for frase in ["ya entendi","lo entendi","esto lo entendi","me quedo claro","ya lo comprendi","lo comprendi","ahora lo entiendo"]):
            self.registrar_autoevaluacion_academica("comprendido"); return
        if any(frase in texto for frase in ["no entendi","no lo entendi","esto me cuesta","me cuesta este tema","no me queda claro","todavia no lo entiendo","me cuesta entenderlo"]):
            self.registrar_autoevaluacion_academica("dificultad"); return
        if any(frase in texto for frase in ["evaluame sobre","evaluame en","ponme a prueba sobre","ponme a prueba en","hazme una pregunta de","hazme una pregunta sobre","preguntame sobre"]):
            objetivo=texto
            for prefijo in ["evaluame sobre","evaluame en","ponme a prueba sobre","ponme a prueba en","hazme una pregunta de","hazme una pregunta sobre","preguntame sobre"]:
                objetivo=objetivo.replace(prefijo," ")
            objetivo=objetivo.strip(); ramo=self.inferir_ramo_academico(objetivo) or objetivo; tema=objetivo or ramo
            self.generar_pregunta_evaluacion_async(ramo,tema); return
        if texto in {"otra pregunta","hazme otra pregunta","otra de evaluacion","otra evaluacion"}:
            ramo=self.ultimo_ramo_evaluacion or self.inferir_ramo_academico(""); tema=self.ultimo_tema_evaluacion or ramo
            if ramo: self.generar_pregunta_evaluacion_async(ramo,tema)
            else: self.evaluacion_manual()
            return

        # 1) Privacidad / modos de escucha. Estas órdenes tienen prioridad
        # porque cambian inmediatamente cuánto audio acepta Beta.
        # Una transcripción parcial como "activa modo" no se manda a Ollama:
        # esperamos la frase completa para evitar dos respuestas superpuestas.
        if (
            texto in {"activa modo", "activar modo", "modo conversacion...", "activa modo..."}
            or (
                texto.startswith(("activa modo", "activar modo"))
                and not any(m in texto for m in ("conversacion", "estricto", "silencio"))
            )
        ):
            print("COMANDO PARCIAL: esperando que termine la orden de modo; no se envía a Ollama.")
            return

        if any(frase in texto for frase in [
            "activa modo conversacion", "activar modo conversacion",
            "modo conversacion", "conversemos", "hablemos sin repetir beta",
        ]):
            self.establecer_modo_escucha(
                "conversacion", anunciar=True, requiere_autenticacion=True
            )
            return

        if any(frase in texto for frase in [
            "termina la conversacion", "termina conversacion",
            "termino la conversacion", "termine la conversacion",
            "terminar la conversacion", "termina modo conversacion",
            "finaliza la conversacion", "finalizo la conversacion",
            "cierra la conversacion", "cierro la conversacion",
            "cierra modo conversacion", "sal del modo conversacion",
            "sal de modo conversacion", "vuelve al modo estricto",
            "regresa al modo estricto", "modo estricto", "activa modo estricto",
        ]):
            self.establecer_modo_escucha("estricto", anunciar=True)
            return

        if any(frase in texto for frase in [
            "modo silencio", "activa modo silencio", "activar modo silencio",
            "silencio", "queda en silencio", "quedate en silencio",
        ]):
            self.establecer_modo_escucha("silencio", anunciar=True)
            return

        if any(frase in texto for frase in [
            "despierta", "reactiva la escucha", "reanuda la escucha",
            "vuelve a escuchar",
        ]):
            self.establecer_modo_escucha("estricto", anunciar=True)
            return

        if any(frase in texto for frase in [
            "que modo de escucha tienes", "cual es tu modo de escucha",
            "en que modo estas",
        ]):
            nombres = {
                "estricto": "modo estricto",
                "conversacion": "modo conversación",
                "silencio": "modo silencio",
            }
            self.responder(
                f"actualmente estoy en {nombres.get(self.modo_escucha, self.modo_escucha)}.",
                "normal",
            )
            return

        # 1) Comandos que el Señor enseñó: máxima prioridad.
        comando_aprendido = self.memoria.buscar_comando(texto)
        if comando_aprendido:
            self.fallos_consecutivos = 0
            self.responder(comando_aprendido[2], "feliz")
            return

        # 2) Enseñar información por voz.
        for prefijo in [
            "aprende que ",
            "recuerda que ",
            "quiero que recuerdes que ",
            "quiero que aprendas que ",
        ]:
            if texto.startswith(prefijo):
                contenido = texto[len(prefijo):].strip()
                if contenido:
                    guardado = self.memoria.guardar_recuerdo(contenido, importancia=2)
                    self.fallos_consecutivos = 0
                    if guardado:
                        self.responder("lo recordaré.", "feliz")
                    else:
                        self.responder("eso ya estaba en mi memoria.", "feliz")
                return

        # Aprendizaje natural: solo frases declarativas claras. No interrumpe la conversación.
        self.aprender_de_frase_natural(original)

        # 3) Nombre / identidad.
        if any(
            frase in texto
            for frase in [
                "como te llamas",
                "cual es tu nombre",
                "dime tu nombre",
                "quien eres",
                "que eres",
                "hablame de ti",
            ]
        ):
            self.fallos_consecutivos = 0
            self.responder(
                "me llamo Beta. Soy su asistente personal local y vivo en este computador.",
                "feliz",
            )
            return

        # 3.4) Saludos, presencia y agradecimientos: respuesta inmediata.
        # También cortan la continuidad académica activa para evitar que un
        # simple "¿estás ahí?" herede por accidente el tema anterior.
        texto_sin_wake = re.sub(
            r"^(beta|veta|meta|metas|petra)\s+", "", texto
        ).strip()
        palabras_breves = texto_sin_wake.split()
        if len(palabras_breves) <= 8 and any(
            frase in texto_sin_wake
            for frase in [
                "hola", "estas ahi", "sigues ahi", "estas alli",
                "me escuchas", "estas disponible", "sigues disponible",
            ]
        ):
            self.ultimo_contexto_academico_ts = 0.0
            self.ultimo_tipo_respuesta_terminada = "general"
            self.fallos_consecutivos = 0
            self.responder("sí, Señor. Aquí estoy y estoy disponible.", "feliz")
            return

        if len(palabras_breves) <= 6 and any(
            texto_sin_wake.startswith(frase)
            for frase in ["gracias", "muchas gracias", "te agradezco"]
        ):
            self.ultimo_tipo_respuesta_terminada = "general"
            self.fallos_consecutivos = 0
            self.responder("de nada, Señor.", "feliz")
            return

        # 3.5) Memoria familiar: respuesta directa y rápida, sin Ollama.
        if self.responder_memoria_familiar(texto):
            self.fallos_consecutivos = 0
            return

        # 3.6) Fuentes de libros técnicos o apuntes académicos.
        if self.manejar_comando_fuentes_tecnicas(texto):
            return
        if self.manejar_comando_fuentes_academicas(texto):
            return

        # La consulta académica genérica se decide más abajo, después de
        # clima/web/acciones explícitas. Así una continuación como "explícame más
        # sobre la memoria" puede heredar el ramo activo antes de abrir una búsqueda
        # global por todas las asignaturas.

        # 4) Pronóstico de mañana / día siguiente.
        # Esta ruta debe evaluarse antes del clima actual para que una frase como
        # "dime la temperatura de mañana" no termine devolviendo el tiempo de hoy.
        palabras_manana = [
            "manana",
            "dia de manana",
            "dia siguiente",
            "siguiente dia",
            "proximo dia",
            "pronostico de manana",
            "tiempo de manana",
        ]
        palabras_meteo = [
            "clima",
            "temperatura",
            "meteorologico",
            "meteorologica",
            "tiempo",
            "pronostico",
        ]
        if (
            any(frase in texto for frase in palabras_manana)
            and any(palabra in texto for palabra in palabras_meteo)
        ):
            self.fallos_consecutivos = 0
            self.consultar_pronostico_manana_async()
            return

        # 4.1) Clima / temperatura actual.
        if any(
            palabra in texto
            for palabra in [
                "clima",
                "temperatura",
                "meteorologico",
                "meteorologica",
                "como esta el tiempo",
                "dime el tiempo",
                "que tiempo hace",
            ]
        ):
            self.fallos_consecutivos = 0
            self.consultar_clima_async()
            return

        # 5) Pendientes y objetivos guardados.
        if any(frase in texto for frase in [
            "que tengo pendiente", "que teniamos pendiente", "que tenemos pendiente",
            "cuales son mis pendientes", "dime mis pendientes", "que me falta hacer",
        ]):
            self.responder_pendientes()
            return

        if texto.startswith(("ya termine ", "ya complete ", "ya hice ")):
            consulta = re.sub(r"^(ya termine|ya complete|ya hice)\s+", "", texto).strip()
            completado = self.memoria.completar_pendiente(consulta)
            if completado:
                self.responder("marqué ese pendiente como completado.", "feliz")
            else:
                self.responder("no encontré un pendiente relacionado para marcarlo como completado.", "confundida")
            return

        if any(frase in texto for frase in [
            "cuales son mis objetivos", "que objetivos tengo", "cual es mi objetivo",
            "que metas tengo", "cuales son mis metas",
        ]):
            self.responder_objetivos_directos()
            return

        if any(frase in texto for frase in [
            "que estoy aprendiendo", "que estoy estudiando", "que estoy practicando",
            "que he estado aprendiendo", "que estoy aprendiendo ahora",
        ]):
            self.responder_aprendizajes_directos()
            return

        # 6) Consultas explícitas de recuerdos.
        for prefijo in [
            "que sabes de ",
            "que sabes sobre ",
            "que recuerdas de ",
            "que recuerdas sobre ",
        ]:
            if texto.startswith(prefijo):
                consulta = texto[len(prefijo):].strip()
                recuerdos = self.memoria.buscar_recuerdos(consulta, 5)
                if recuerdos:
                    contenido = "; ".join(r[1].strip().rstrip(".") for r in recuerdos)
                    self.responder("recuerdo que " + contenido + ".", "feliz")
                else:
                    self.responder("no encontré un recuerdo relacionado con eso.", "confundida")
                return

        if texto in {"que recuerdas", "que has aprendido", "que sabes"}:
            recuerdos = self.memoria.ultimos_recuerdos(5)
            if not recuerdos:
                self.responder("todavía tengo pocos recuerdos.", "confundida")
            else:
                contenido = "; ".join(r[1] for r in recuerdos[:4])
                self.responder("entre otras cosas, recuerdo que " + contenido + ".", "feliz")
            return

        if texto.startswith("olvida "):
            eliminado = self.memoria.olvidar(texto.replace("olvida ", "", 1).strip())
            if eliminado:
                self.responder("he eliminado ese recuerdo.", "normal")
            else:
                self.responder("no encontré ese recuerdo.", "confundida")
            return

        # Comando de recuperación manual por si alguna consulta externa quedó atascada.
        if (
            any(frase in texto for frase in [
                "cancela la consulta", "cancela lo anterior", "reinicia la respuesta",
                "deja de pensar", "dejas de pensar", "deje de pensar", "cancela respuesta",
                "para de pensar", "pare de pensar", "deten la respuesta",
            ])
            or ("pensar" in texto and any(v in texto for v in ["deja", "dejas", "para", "pare", "deten"]))
        ):
            self.proceso_id += 1
            self.procesando = False
            self.procesando_desde = 0.0
            self.procesando_tipo = ""
            self.responder("cancelé el procesamiento anterior y ya estoy disponible.", "normal")
            return

        # 5.8) Spotify: abrir, buscar y controlar reproducción. Las órdenes
        # "reproduce música de X" sin plataforma explícita usan Spotify.
        orden_spotify = self.extraer_orden_spotify(original)
        if orden_spotify:
            accion_spotify, consulta_spotify = orden_spotify
            if accion_spotify == "abrir":
                self.abrir_spotify_inicio()
            elif accion_spotify == "buscar":
                self.buscar_en_spotify(consulta_spotify)
            elif accion_spotify == "reproducir":
                self.reproducir_spotify_async(consulta_spotify)
            elif accion_spotify == "reproducir_playlist":
                self.reproducir_playlist_spotify_async(consulta_spotify)
            elif accion_spotify == "abrir_playlist":
                self.abrir_playlist_spotify_async(consulta_spotify)
            elif accion_spotify == "listar_playlists":
                self.spotify_listar_playlists_async()
            elif accion_spotify == "reanudar":
                self.spotify_control_async("reanudar")
            elif accion_spotify == "pausar":
                self.spotify_control_async("pausar")
            elif accion_spotify == "siguiente":
                self.spotify_control_async("siguiente")
            elif accion_spotify == "anterior":
                self.spotify_control_async("anterior")
            elif accion_spotify == "preferencias":
                self.spotify_preferencias_async()
            elif accion_spotify == "reproducir_preferencias":
                self.reproducir_preferencias_spotify_async()
            return

        # 5.9) YouTube: abrir el sitio, buscar o reproducir el primer resultado.
        # Esta ruta va antes de Google y Ollama para evitar que una frase como
        # "busca en YouTube Luli Pampín" termine convertida en una búsqueda web
        # genérica o en una conversación con el modelo local.
        orden_youtube = self.extraer_orden_youtube(original)
        if orden_youtube:
            consulta_youtube, reproducir_youtube, solo_abrir_youtube = orden_youtube
            if solo_abrir_youtube:
                self.abrir_youtube_inicio()
            elif reproducir_youtube:
                self.reproducir_youtube_async(consulta_youtube)
            else:
                self.buscar_en_youtube(consulta_youtube)
            return

        # 6) Investigación web: Beta busca información actual y la conversa
        # utilizando Qwen local. Esto es distinto de abrir Google visualmente.
        consulta_investigacion = self.extraer_investigacion_web(original)
        if consulta_investigacion:
            self.investigar_internet_async(consulta_investigacion)
            return

        # Abrir una fuente de la última investigación.
        if self.manejar_comando_fuentes(texto):
            return

        # 6.5) Acciones locales seguras / navegación visual en Internet.
        # Una orden como "abre Google Chrome y busca diseños de muebles de madera"
        # abre directamente los resultados en pantalla. El contenido buscado se
        # codifica como URL; nunca se ejecuta como comando del sistema.
        busqueda_web = self.extraer_busqueda_web(original)
        if busqueda_web:
            consulta, modo_imagenes = busqueda_web
            self.buscar_en_chrome(consulta, modo_imagenes=modo_imagenes)
            return

        if "chrome" in texto and any(v in texto for v in ["abre", "abrir", "inicia"]):
            self.abrir_chrome()
            return

        if "calculadora" in texto and any(v in texto for v in ["abre", "abrir", "inicia"]):
            try:
                subprocess.Popen("calc.exe")
                self.responder("abriendo la calculadora.", "feliz")
            except Exception:
                self.responder("no pude abrir la calculadora.", "molesta")
            return

        if (
            ("bloc de notas" in texto or "notepad" in texto)
            and any(v in texto for v in ["abre", "abrir", "inicia"])
        ):
            try:
                subprocess.Popen("notepad.exe")
                self.responder("abriendo el bloc de notas.", "feliz")
            except Exception:
                self.responder("no pude abrirlo.", "molesta")
            return

        if "explorador" in texto and any(v in texto for v in ["abre", "abrir", "inicia"]):
            try:
                subprocess.Popen("explorer.exe")
                self.responder("abriendo el explorador.", "feliz")
            except Exception:
                self.responder("no pude abrir el explorador.", "molesta")
            return

        if any(frase in texto for frase in ["abre inicio", "menu inicio", "abrir inicio"]):
            self.abrir_inicio()
            return

        if texto.startswith("crea carpeta ") or texto.startswith("crear carpeta "):
            nombre = re.sub(
                r"^(crea|crear)\s+carpeta\s+",
                "",
                original,
                flags=re.IGNORECASE,
            )
            self.crear_carpeta(nombre)
            return

        # 7) Hora local del computador.
        if (
            "hora" in texto
            and not any(p in texto for p in ["temperatura", "clima", "tiempo"])
        ):
            self.responder(f"son las {time.strftime('%H:%M')}.", "normal")
            return

        # 8) Si parece una acción desconocida, NO dejamos que el modelo invente
        # comandos de Windows. Se muestra confusión.
        if any(
            texto.startswith(prefijo)
            for prefijo in [
                "abre ",
                "borra ",
                "elimina ",
                "mueve ",
                "copia ",
                "renombra ",
                "ejecuta ",
                "inicia ",
                "apaga ",
                "reinicia ",
            ]
        ):
            self.no_entendi(texto, "no sé realizar esa acción todavía.")
            return

        # 8.7) Seguimiento de una respuesta que combinó varias bibliotecas.
        if self.es_seguimiento_biblioteca_inteligente(original):
            self.fallos_consecutivos = 0
            self.conversar_contexto_inteligente_async(original)
            return

        # 8.8) Seguimiento técnico: si la respuesta anterior vino de un libro
        # técnico, mantenemos ese contexto antes de evaluar el RAG académico.
        if self.es_seguimiento_tecnico(original):
            self.fallos_consecutivos = 0
            self.conversar_contexto_tecnico_async(original)
            return

        # 8.9) Seguimiento robusto de una explicación basada en la biblioteca académica.
        if self.es_seguimiento_academico(original):
            self.fallos_consecutivos = 0
            self.conversar_contexto_academico_async(original)
            return

        # 8.10) Biblioteca inteligente: decide automáticamente entre libros
        # técnicos, apuntes académicos o una combinación de ambos.
        decision_biblioteca = self.decidir_ruta_biblioteca(original)
        ruta_biblioteca = decision_biblioteca.get("ruta", "qwen")
        if ruta_biblioteca == "tecnica":
            self.fallos_consecutivos = 0
            self.consultar_biblioteca_tecnica_async(original)
            return
        if ruta_biblioteca == "academica":
            self.fallos_consecutivos = 0
            self.consultar_biblioteca_async(original, decision=decision_biblioteca)
            return
        if ruta_biblioteca == "mixta":
            self.fallos_consecutivos = 0
            self.consultar_biblioteca_mixta_async(original, decision_biblioteca)
            return

        # Compatibilidad: una solicitud local explícita siempre se respeta, incluso
        # si por alguna razón el enrutador no pudo cargar el índice en ese instante.
        if self.parece_consulta_tecnica_programacion(original):
            self.fallos_consecutivos = 0
            self.consultar_biblioteca_tecnica_async(original)
            return
        if self.parece_consulta_academica(original) and any(
            x in normalizar(original) for x in [
                "mis apuntes", "mi material", "biblioteca academica", "segun el modulo"
            ]
        ):
            self.fallos_consecutivos = 0
            self.consultar_biblioteca_async(original)
            return

        # 9) Si venimos de una investigación reciente y el Señor hace una
        # pregunta de seguimiento, Qwen recibe ese contexto sin volver a buscar.
        if self.es_seguimiento_web(original):
            self.fallos_consecutivos = 0
            self.conversar_web_contexto_async(original)
            return

        # 10) Todo lo demás pasa al modelo local para conversación natural.
        self.fallos_consecutivos = 0
        self.conversar_ollama_async(original)

    def no_entendi(self, texto, mensaje):
        if texto == self.ultimo_no_entendido:
            self.fallos_consecutivos += 1
        else:
            self.ultimo_no_entendido = texto
            self.fallos_consecutivos = 1

        if self.fallos_consecutivos < 2:
            self.responder(mensaje, "confundida")
        else:
            self.responder("sigo sin entender esa petición.", "molesta")

    # ======================================================
    # ACCIONES WINDOWS
    # ======================================================

    def buscar_google_manual(self):
        consulta = simpledialog.askstring(
            "Buscar en Google",
            "¿Qué quiere que busque, Señor?",
            parent=self.root,
        )
        if consulta and consulta.strip():
            self.buscar_en_chrome(consulta.strip())

    def spotify_buscar_manual(self):
        consulta = simpledialog.askstring(
            "Buscar en Spotify",
            "¿Qué quiere buscar en Spotify, Señor?",
            parent=self.root,
        )
        if consulta and consulta.strip():
            self.buscar_en_spotify(consulta.strip())

    def spotify_reproducir_manual(self):
        consulta = simpledialog.askstring(
            "Reproducir en Spotify",
            "¿Qué artista quiere reproducir en Spotify, Señor?",
            parent=self.root,
        )
        if consulta and consulta.strip():
            self.reproducir_spotify_async(consulta.strip())

    def spotify_playlist_manual(self):
        consulta = simpledialog.askstring(
            "Reproducir playlist en Spotify",
            "¿Qué playlist quiere reproducir en Spotify, Señor?",
            parent=self.root,
        )
        if consulta and consulta.strip():
            self.reproducir_playlist_spotify_async(consulta.strip())

    def spotify_reconectar_permisos(self):
        """Reautoriza la cuenta con los scopes actuales sin pedir otro Client ID."""
        if not self.spotify_client_id:
            self.configurar_spotify()
            return
        self.conectar_spotify_async()

    def youtube_manual(self):
        consulta = simpledialog.askstring(
            "Reproducir en YouTube",
            "¿Qué quiere que reproduzca en YouTube, Señor?",
            parent=self.root,
        )
        if consulta and consulta.strip():
            self.reproducir_youtube_async(consulta.strip())

    def investigar_internet_manual(self):
        consulta = simpledialog.askstring(
            "Investigar en Internet",
            "¿Qué quiere que investigue, Señor?",
            parent=self.root,
        )
        if consulta and consulta.strip():
            self.investigar_internet_async(consulta.strip())

    def cambiar_memoria_inteligente(self):
        self.modo_memoria_inteligente = bool(self.var_memoria_inteligente.get())
        self.memoria.cambiar_estado(
            "modo_memoria_inteligente",
            "1" if self.modo_memoria_inteligente else "0",
        )
        if self.modo_memoria_inteligente:
            self.responder(
                "activé la memoria inteligente. Guardaré en segundo plano la información personal y los temas importantes que usted me cuente.",
                "feliz",
            )
        else:
            self.responder(
                "desactivé la memoria inteligente automática. Seguiré guardando solamente lo que usted me pida recordar de forma explícita.",
                "normal",
            )

    def cambiar_preguntas_seguimiento(self):
        self.preguntas_seguimiento = bool(self.var_preguntas_seguimiento.get())
        self.memoria.cambiar_estado(
            "preguntas_seguimiento",
            "1" if self.preguntas_seguimiento else "0",
        )
        if self.preguntas_seguimiento:
            self.responder(
                "activé las preguntas de seguimiento. Cuando corresponda, intentaré continuar la conversación con una pregunta natural.",
                "feliz",
            )
        else:
            self.responder(
                "desactivé las preguntas de seguimiento. Responderé sin intentar prolongar la conversación.",
                "normal",
            )

    def cambiar_modo_companera(self):
        self.modo_companera = bool(self.var_modo_companera.get())
        self.memoria.cambiar_estado(
            "modo_companera",
            "1" if self.modo_companera else "0",
        )
        self.proxima_iniciativa_ts = time.time() + random.randint(
            INICIATIVA_MIN_SEGUNDOS,
            INICIATIVA_MAX_SEGUNDOS,
        )
        if self.modo_companera:
            self.responder(
                "activé el modo compañera. Iniciaré alguna conversación de vez en cuando, sin interrumpirlo demasiado.",
                "feliz",
            )
        else:
            self.responder(
                "desactivé el modo compañera. Esperaré a que usted inicie las conversaciones.",
                "normal",
            )

    def cambiar_modo_curioso(self):
        self.modo_curioso = bool(self.var_modo_curioso.get())
        self.memoria.cambiar_estado("modo_curioso", "1" if self.modo_curioso else "0")
        self.pregunta_curiosa_pendiente = None
        self.pregunta_curiosa_id = 0
        self.pregunta_curiosa_hasta = 0.0
        self.proxima_pregunta_curiosa_ts = time.time() + random.randint(
            CURIOSIDAD_MIN_SEGUNDOS, CURIOSIDAD_MAX_SEGUNDOS
        )
        if self.modo_curioso:
            self.responder(
                "activé el modo curioso. De vez en cuando le haré una pregunta breve para conocerlo mejor, y recordaré únicamente lo que usted me responda explícitamente.",
                "feliz",
            )
        else:
            self.responder(
                "desactivé el modo curioso. No iniciaré preguntas para aprender datos nuevos sobre usted.",
                "normal",
            )

    def extraer_investigacion_web(self, comando):
        """Detecta cuando el Señor quiere que Beta investigue y converse.

        Diferencia dos comportamientos:
        - "abre Chrome / busca en Google..." -> búsqueda visual.
        - "investiga / averigua / busca en Internet información..." ->
          Beta recupera fuentes y después Qwen las explica.
        """
        original = (comando or "").strip()
        if not original:
            return None

        # Trabajamos con la versión normalizada para tolerar signos de pregunta,
        # acentos y pequeñas variaciones de Whisper/Vosk.
        texto = normalizar(original)
        # Si el Señor nombró explícitamente YouTube, esa plataforma tiene prioridad.
        if any(x in texto for x in ["youtube", "yutube", "yutu"]) and "spotify" not in texto:
            return None
        texto = re.sub(r"^(?:beta|veta|meta|metas|petra)\s+", "", texto).strip()
        texto = re.sub(
            r"^(?:por favor )?(?:me )?(?:puedes|podrias)\s+",
            "",
            texto,
        ).strip()

        # No secuestrar clima: esa ruta tiene su servicio dedicado.
        if any(p in texto for p in ["clima", "temperatura", "meteorologico", "tiempo hace"]):
            return None

        # Si la orden dice explícitamente abrir/mostrar Chrome, se considera visual.
        if any(x in texto for x in [
            "abre chrome", "abre google chrome", "abrir chrome",
            "muestrame en chrome", "visualiza en chrome",
        ]):
            return None

        patrones = [
            r"^(?:investiga|investigar|averigua|averiguar)\s+(?:sobre\s+|acerca\s+de\s+)?(.+)$",
            r"^(?:consulta|consultar)\s+(?:en\s+)?internet\s+(?:sobre\s+|acerca\s+de\s+)?(.+)$",
            r"^(?:busca|buscar|buscame)\s+informacion\s+(?:en\s+internet\s+)?(?:sobre\s+|acerca\s+de\s+|de\s+)?(.+)$",
            # Frases naturales como: "busca en internet algo relacionado con el sistema nervioso"
            r"^(?:busca|buscar|buscame)\s+(?:en\s+)?internet(?:\s+o\s+(?:en\s+)?google)?\s+(?:algo\s+)?(?:relacionado\s+con\s+|sobre\s+|acerca\s+de\s+|informacion\s+(?:sobre\s+|de\s+)?)?(.+)$",
            r"^(?:que\s+hay\s+de\s+nuevo\s+sobre)\s+(.+)$",
            r"^(?:ultimas?\s+noticias\s+(?:sobre|de))\s+(.+)$",
            r"^(?:novedades\s+(?:sobre|de))\s+(.+)$",
            r"^(?:que\s+esta\s+pasando\s+con)\s+(.+)$",
            r"^(?:cual\s+es\s+la\s+ultima\s+version\s+de)\s+(.+)$",
            r"^(?:cual\s+es\s+la\s+version\s+actual\s+de)\s+(.+)$",
        ]

        for patron in patrones:
            m = re.match(patron, texto, flags=re.IGNORECASE)
            if m:
                consulta = m.group(1).strip(" .,:;-\t\n")
                consulta = re.sub(
                    r"^(?:algo\s+)?(?:relacionado\s+con|sobre|acerca\s+de|informacion\s+(?:sobre|de))\s+",
                    "",
                    consulta,
                    flags=re.IGNORECASE,
                ).strip()
                if len(consulta) >= 2:
                    print(f"INVESTIGACIÓN WEB DETECTADA: {consulta}")
                    return consulta

        # Preguntas inequívocamente temporales: mejor consultar la web que
        # responder con conocimiento potencialmente desactualizado del modelo.
        marcadores_actualidad = [
            "hoy", "actualmente", "actual", "reciente", "recientes",
            "ultima noticia", "ultimas noticias", "ultima version",
            "ultima actualizacion", "este mes", "esta semana",
        ]
        if any(m in texto for m in marcadores_actualidad) and any(
            q in texto for q in ["que ", "cual ", "como ", "dime ", "cuentame "]
        ):
            return texto

        return None

    def buscar_internet_ddgs(self, consulta):
        clave = normalizar(consulta)
        ahora = time.time()
        cache = self.web_cache.get(clave)
        if cache and ahora - cache[0] <= WEB_CACHE_SEGUNDOS:
            print("INTERNET: usando resultados recientes en caché.")
            return cache[1]

        try:
            from ddgs import DDGS
        except Exception as error:
            print("DDGS NO DISPONIBLE:", error)
            raise RuntimeError(
                "Falta instalar el paquete ddgs. Ejecute: python -m pip install -U ddgs"
            ) from error

        texto = normalizar(consulta)
        es_noticia = any(p in texto for p in [
            "noticia", "noticias", "novedad", "novedades", "hoy", "esta semana",
        ])
        timelimit = "w" if es_noticia else None

        def ejecutar(region):
            buscador = DDGS(timeout=WEB_TIMEOUT)
            if es_noticia:
                resultados = buscador.news(
                    consulta,
                    region=region,
                    safesearch="moderate",
                    timelimit=timelimit,
                    max_results=WEB_MAX_RESULTADOS,
                    backend="auto",
                )
                if resultados:
                    return resultados
            return buscador.text(
                consulta,
                region=region,
                safesearch="moderate",
                timelimit=timelimit,
                max_results=WEB_MAX_RESULTADOS,
                backend="auto",
            )

        try:
            crudos = ejecutar(WEB_REGION)
        except Exception as primero:
            print("INTERNET: falló región CL, reintentando global:", primero)
            crudos = ejecutar("wt-wt")

        resultados = []
        for item in crudos or []:
            titulo = str(item.get("title") or "").strip()
            url = str(item.get("href") or item.get("url") or "").strip()
            cuerpo = str(item.get("body") or item.get("description") or "").strip()
            fecha = str(item.get("date") or "").strip()
            fuente = str(item.get("source") or "").strip()
            if not titulo and not cuerpo:
                continue
            resultados.append({
                "titulo": titulo,
                "url": url,
                "cuerpo": cuerpo[:900],
                "fecha": fecha,
                "fuente": fuente,
            })

        self.web_cache[clave] = (ahora, resultados)
        return resultados

    def formatear_resultados_web(self, resultados):
        bloques = []
        for i, r in enumerate(resultados[:WEB_MAX_RESULTADOS], 1):
            fuente = r.get("fuente") or urllib.parse.urlparse(r.get("url", "")).netloc
            partes = [f"FUENTE {i}: {r.get('titulo', '')}"]
            if fuente:
                partes.append(f"Sitio: {fuente}")
            if r.get("fecha"):
                partes.append(f"Fecha: {r['fecha']}")
            if r.get("cuerpo"):
                partes.append(f"Resumen del buscador: {r['cuerpo']}")
            bloques.append("\n".join(partes))
        return "\n\n".join(bloques)

    def resumir_resultados_web(self, consulta, resultados):
        contexto = self.formatear_resultados_web(resultados)
        recuerdos = self.memoria.buscar_recuerdos(consulta, limite=2)
        recuerdos_texto = "\n".join(f"- {r[1]}" for r in recuerdos) if recuerdos else "Sin recuerdos relevantes."

        mensajes = [
            {
                "role": "system",
                "content": (
                    "Eres Beta, la asistente del Señor. Responde exclusivamente en español. "
                    "Estás analizando resultados RECIENTES obtenidos de Internet. "
                    "Usa solamente los datos incluidos en FUENTES para las afirmaciones actuales; "
                    "no inventes hechos, fechas ni cifras que no aparezcan allí. Si las fuentes no "
                    "alcanzan para responder con seguridad, dilo. Resume de forma conversacional "
                    "en 2 a 5 frases. Puedes mencionar brevemente el nombre del sitio o título de "
                    "las fuentes más útiles, pero no leas URLs completas. No muestres razonamiento interno."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Consulta del Señor: {consulta}\n\n"
                    f"FUENTES DE INTERNET:\n{contexto}\n\n"
                    f"RECUERDOS LOCALES RELEVANTES (solo para personalizar, no como fuente de actualidad):\n"
                    f"{recuerdos_texto}\n\n"
                    "Explique lo encontrado de forma natural y útil."
                ),
            },
        ]
        return self.enviar_ollama(mensajes, temperatura=0.15, num_predict=170)

    def investigar_internet_async(self, consulta):
        consulta = (consulta or "").strip()
        if not consulta:
            self.responder("necesito saber qué desea que investigue.", "confundida")
            return

        token = self.iniciar_proceso("internet")
        if token is None:
            self.responder(
                "todavía estoy terminando la consulta anterior. Espere un momento.",
                "pensando",
            )
            return

        self.expresion_pensando()

        def trabajo():
            respuesta = None
            resultados = []
            error_texto = ""
            try:
                inicio = time.perf_counter()
                resultados = self.buscar_internet_ddgs(consulta)
                print(f"LATENCIA BÚSQUEDA INTERNET: {time.perf_counter() - inicio:.2f} s")

                if resultados:
                    inicio_ia = time.perf_counter()
                    respuesta = self.resumir_resultados_web(consulta, resultados)
                    print(f"LATENCIA RESUMEN WEB QWEN: {time.perf_counter() - inicio_ia:.2f} s")
                else:
                    error_texto = "no encontré resultados suficientes en Internet para esa consulta."
            except Exception as error:
                print("ERROR INVESTIGACIÓN INTERNET:", error)
                error_texto = str(error)
            finally:
                self.terminar_proceso(token)

            if token != self.proceso_id:
                return

            if resultados and respuesta:
                resumen = self.limpiar_respuesta_ollama(respuesta)
                self.ultimas_fuentes_web = resultados
                self.ultima_investigacion_web = {
                    "consulta": consulta,
                    "resultados": resultados,
                    "resumen": resumen,
                }
                self.ultima_investigacion_web_ts = time.time()
                print("INVESTIGACIÓN WEB:", consulta)
                for i, r in enumerate(resultados[:5], 1):
                    print(f"  FUENTE {i}: {r.get('titulo','')} | {r.get('url','')}")
                self.root.after(0, lambda r=resumen: self.responder(r, "hablando"))
            else:
                if "Falta instalar el paquete ddgs" in error_texto:
                    mensaje = (
                        "para investigar Internet me falta un componente. "
                        "Instale el paquete DDGS y vuelva a intentarlo."
                    )
                elif error_texto:
                    mensaje = "no pude completar la investigación en Internet en este momento."
                else:
                    mensaje = "no encontré información suficiente en Internet sobre ese tema."
                self.root.after(0, lambda m=mensaje: self.responder(m, "confundida"))

        threading.Thread(target=trabajo, daemon=True).start()

    def es_seguimiento_web(self, pregunta):
        """Detecta preguntas que se refieren a la última búsqueda/investigación."""
        if not self.ultima_investigacion_web:
            return False
        if time.time() - self.ultima_investigacion_web_ts > WEB_CONTEXTO_SEGUNDOS:
            return False

        texto = normalizar(pregunta)
        marcadores = [
            "dime mas", "cuentame mas", "explicame mas", "por que es importante",
            "por que", "que significa eso", "que significa", "cual de esas",
            "cual de ellos", "de esas", "de esos", "esa noticia", "esas noticias",
            "sobre eso", "y eso", "y cual", "y que", "me conviene", "que opinas de eso",
            # Seguimiento después de una búsqueda visual en Google/Chrome.
            "explicame lo que encontraste", "explica lo que encontraste",
            "me puedes explicar lo que encontraste", "puedes explicar lo que encontraste",
            "que encontraste", "que encontraste en google", "que encontraste en chrome",
            "lo que encontraste en google", "lo que encontraste en chrome",
            "explicame los resultados", "explica los resultados", "resumeme los resultados",
            "resumeme lo que encontraste", "hablame de lo que encontraste",
        ]
        return any(m in texto for m in marcadores)

    def conversar_web_contexto_async(self, pregunta):
        contexto_web = self.ultima_investigacion_web
        if not contexto_web:
            self.conversar_ollama_async(pregunta)
            return

        token = self.iniciar_proceso("web_contexto")
        if token is None:
            self.responder("todavía estoy terminando la respuesta anterior.", "pensando")
            return

        self.expresion_pensando()

        def trabajo():
            respuesta = None
            try:
                # Una búsqueda visual puede haberse abierto hace apenas unos segundos.
                # Si el contexto todavía no terminó de descargarse, lo recuperamos aquí.
                resultados = contexto_web.get("resultados") or []
                if not resultados:
                    inicio_web = time.perf_counter()
                    resultados = self.buscar_internet_ddgs(contexto_web.get("consulta", ""))
                    print(f"LATENCIA CONTEXTO GOOGLE: {time.perf_counter() - inicio_web:.2f} s")
                    if resultados:
                        contexto_web["resultados"] = resultados
                        self.ultimas_fuentes_web = resultados

                if not resultados:
                    raise RuntimeError("No hay resultados web disponibles para explicar.")

                fuentes = self.formatear_resultados_web(resultados)
                resumen_anterior = contexto_web.get("resumen") or ""
                origen = contexto_web.get("origen", "investigacion")

                mensajes = [
                    {
                        "role": "system",
                        "content": (
                            "Eres Beta y hablas con el Señor en español. Estás continuando una conversación "
                            "sobre información que Beta recuperó de Internet. No afirmes que puedes ver la "
                            "pantalla ni leer directamente Google Chrome. Explica los resultados web que se "
                            "te proporcionan. Para hechos actuales usa únicamente las fuentes suministradas. "
                            "Si las fuentes no bastan, dilo con claridad. Responde de forma breve, natural y útil."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Tema buscado: {contexto_web.get('consulta','')}\n"
                            f"Origen: {origen}\n"
                            f"Resumen anterior: {resumen_anterior}\n\n"
                            f"Resultados recuperados de Internet:\n{fuentes}\n\n"
                            f"Pregunta de seguimiento del Señor: {pregunta}"
                        ),
                    },
                ]
                respuesta = self.enviar_ollama(mensajes, temperatura=0.18, num_predict=170)
                if respuesta:
                    respuesta = self.limpiar_respuesta_ollama(respuesta)
                    contexto_web["resumen"] = respuesta
            except Exception as error:
                print("ERROR SEGUIMIENTO WEB:", error)
            finally:
                self.terminar_proceso(token)

            if token != self.proceso_id:
                return
            if respuesta:
                self.root.after(0, lambda r=respuesta: self.responder(r, "hablando"))
            else:
                self.root.after(0, lambda: self.responder(
                    "no pude recuperar información suficiente de esa búsqueda para explicársela.", "confundida"
                ))

        threading.Thread(target=trabajo, daemon=True).start()

    def manejar_comando_fuentes(self, texto):
        texto = normalizar(texto)
        if not self.ultimas_fuentes_web:
            if any(x in texto for x in ["abre la fuente", "muestra las fuentes", "ver fuentes"]):
                self.responder("todavía no tengo fuentes de una investigación reciente.", "confundida")
                return True
            return False

        if any(x in texto for x in ["muestrame las fuentes", "muestra las fuentes", "ver las fuentes", "ver fuentes"]):
            self.root.after(0, self.ventana_fuentes_web)
            self.responder("le muestro las fuentes de la última investigación.", "feliz")
            return True

        indices = {
            "primera fuente": 0, "fuente uno": 0,
            "segunda fuente": 1, "fuente dos": 1,
            "tercera fuente": 2, "fuente tres": 2,
            "cuarta fuente": 3, "fuente cuatro": 3,
            "quinta fuente": 4, "fuente cinco": 4,
        }
        for frase, indice in indices.items():
            if frase in texto and any(v in texto for v in ["abre", "abrir", "muestra", "ver"]):
                if indice < len(self.ultimas_fuentes_web):
                    self.abrir_url_fuente(self.ultimas_fuentes_web[indice].get("url", ""))
                    self.responder(f"abriendo la {frase}.", "feliz")
                else:
                    self.responder("esa fuente no está disponible en la última investigación.", "confundida")
                return True
        return False

    def abrir_url_fuente(self, url):
        if not url:
            return
        try:
            chrome = self.obtener_ruta_chrome()
            if chrome:
                subprocess.Popen([chrome, url])
            else:
                os.startfile(url)
        except Exception as error:
            print("ERROR ABRIENDO FUENTE:", error)

    def ventana_fuentes_web(self):
        if not self.ultimas_fuentes_web:
            messagebox.showinfo(
                "Fuentes de Internet",
                "Beta todavía no tiene fuentes de una investigación reciente.",
                parent=self.root,
            )
            return

        ventana = tk.Toplevel(self.root)
        ventana.title("Fuentes de la última investigación de Beta")
        ventana.geometry("900x460")
        ventana.attributes("-topmost", True)

        ttk.Label(
            ventana,
            text="Doble clic en una fuente para abrirla en Chrome.",
        ).pack(anchor="w", padx=12, pady=(12, 6))

        tabla = ttk.Treeview(
            ventana,
            columns=("n", "titulo", "sitio", "url"),
            show="headings",
        )
        tabla.heading("n", text="#")
        tabla.heading("titulo", text="Título")
        tabla.heading("sitio", text="Sitio")
        tabla.heading("url", text="URL")
        tabla.column("n", width=40, anchor="center")
        tabla.column("titulo", width=390)
        tabla.column("sitio", width=150)
        tabla.column("url", width=300)
        tabla.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        for i, r in enumerate(self.ultimas_fuentes_web, 1):
            sitio = r.get("fuente") or urllib.parse.urlparse(r.get("url", "")).netloc
            tabla.insert("", "end", values=(i, r.get("titulo", ""), sitio, r.get("url", "")))

        def abrir_seleccion(_event=None):
            seleccion = tabla.selection()
            if not seleccion:
                return
            valores = tabla.item(seleccion[0]).get("values", [])
            if len(valores) >= 4:
                self.abrir_url_fuente(str(valores[3]))

        tabla.bind("<Double-1>", abrir_seleccion)
        ttk.Button(ventana, text="Abrir fuente seleccionada", command=abrir_seleccion).pack(pady=(0, 12))

    def vigilar_iniciativa(self):
        """Permite que Beta inicie una conversación muy ocasionalmente.

        No usa Internet automáticamente: solo memoria local + Qwen. Así no
        genera tráfico web ni interrupciones frecuentes sin que el Señor lo pida.
        """
        try:
            ahora = time.time()
            hora = datetime.now().hour
            activa_recientemente = ahora - self.ultimo_movimiento_mouse < 120
            silencio_suficiente = ahora - self.ultima_interaccion_voz >= INICIATIVA_SIN_VOZ_SEGUNDOS

            condiciones = (
                self.modo_companera
                and INICIATIVA_HORA_INICIO <= hora < INICIATIVA_HORA_FIN
                and ahora >= self.proxima_iniciativa_ts
                and activa_recientemente
                and silencio_suficiente
                and not self.hablando
                and not self.procesando
                and not self.esperando_orden
                and self.modo_escucha != "silencio"
            )

            if condiciones:
                recuerdos = self.memoria.ultimos_recuerdos(4)
                if recuerdos:
                    self.generar_iniciativa_async(recuerdos)
                self.proxima_iniciativa_ts = ahora + random.randint(
                    INICIATIVA_MIN_SEGUNDOS,
                    INICIATIVA_MAX_SEGUNDOS,
                )
        except Exception as error:
            print("ERROR MODO COMPAÑERA:", error)
        finally:
            self.root.after(60000, self.vigilar_iniciativa)

    def generar_iniciativa_async(self, recuerdos):
        token = self.iniciar_proceso("iniciativa")
        if token is None:
            return

        contexto = "\n".join(f"- {r[1]}" for r in recuerdos[:4])

        def trabajo():
            respuesta = None
            try:
                mensajes = [
                    {
                        "role": "system",
                        "content": (
                            "Eres Beta, asistente personal del Señor. Inicia una conversación breve y natural "
                            "basándote en uno de los recuerdos suministrados. Haz una sola observación o pregunta "
                            "amable. No inventes recuerdos, no seas insistente y no menciones que recibiste un prompt. "
                            "Responde solo en español y en una o dos frases."
                        ),
                    },
                    {
                        "role": "user",
                        "content": f"Recuerdos disponibles:\n{contexto}",
                    },
                ]
                respuesta = self.enviar_ollama(mensajes, temperatura=0.35, num_predict=80)
                if respuesta:
                    respuesta = self.limpiar_respuesta_ollama(respuesta)
            except Exception as error:
                print("ERROR GENERANDO INICIATIVA:", error)
            finally:
                self.terminar_proceso(token)

            if token != self.proceso_id or not respuesta:
                return
            self.ultima_iniciativa_ts = time.time()
            self.ultima_interaccion_voz = time.time()
            self.root.after(0, lambda r=respuesta: self.responder(r, "feliz"))

        threading.Thread(target=trabajo, daemon=True).start()

    # ======================================================
    # SPOTIFY
    # ======================================================

    def _spotify_normalizar_aliases(self, texto):
        """Normaliza variantes fonéticas de Spotify detectadas por ASR.

        El usuario puede pronunciar el nombre como "espótifai". Vosk/Whisper
        pueden escribirlo de muchas formas; internamente todas se convierten a
        la palabra canónica "spotify" sin obligar al usuario a pronunciarla
        como se escribe.
        """
        t = normalizar(texto or "")
        # Variantes frecuentes y suficientemente específicas para no secuestrar
        # frases corrientes. normalizar() ya elimina tildes.
        patrones = [
            r"\bes\s+potifai\b", r"\bes\s+potifay\b", r"\bes\s+potify\b",
            r"\bes\s+potifi\b", r"\bes\s+potifai\b",
            r"\bespotifai\b", r"\bespotifay\b", r"\bespotify\b",
            r"\bespotifi\b", r"\bspotifai\b", r"\bspotifay\b",
            r"\bspotifi\b", r"\bspodifai\b", r"\bspodifay\b",
            r"\bspodify\b", r"\bspotifly\b", r"\bspotify\b",
        ]
        for patron in patrones:
            t = re.sub(patron, "spotify", t)
        t = re.sub(r"\s+", " ", t).strip()
        return t

    def _spotify_marcar_contexto(self, minutos=45):
        self.spotify_contexto_hasta = max(
            float(getattr(self, "spotify_contexto_hasta", 0.0) or 0.0),
            time.time() + max(1, int(minutos)) * 60,
        )

    def _spotify_contexto_vigente(self):
        return time.time() < float(getattr(self, "spotify_contexto_hasta", 0.0) or 0.0)

    def _spotify_guardar_vocabulario(self, nombres):
        """Conserva nombres de artistas para ayudar al prompt de Whisper."""
        actuales = list(getattr(self, "spotify_vocabulario", []) or [])
        vistos = {normalizar(x) for x in actuales}
        for nombre in nombres or []:
            nombre = str(nombre or "").strip()
            if not nombre:
                continue
            n = normalizar(nombre)
            if n and n not in vistos:
                actuales.append(nombre)
                vistos.add(n)
        self.spotify_vocabulario = actuales[-20:]
        try:
            self.memoria.cambiar_estado(
                "spotify_vocabulario",
                json.dumps(self.spotify_vocabulario, ensure_ascii=False),
            )
        except Exception:
            pass

    def extraer_orden_spotify(self, comando):
        """Devuelve (accion, consulta) para órdenes de Spotify.

        v2.6.5 entiende playlists personales incluso cuando su nombre no lleva
        la palabra "playlist" en la orden: "Beta, reproduce Gold Black" puede
        resolverse contra la biblioteca personal cacheada antes de tratar el
        nombre como artista.
        """
        original = (comando or "").strip()
        if not original:
            return None

        texto = self._spotify_normalizar_aliases(original)
        texto = re.sub(r"^(?:beta|veta|meta|metas|petra)\s+", "", texto).strip()
        texto = re.sub(
            r"^(?:por favor\s+)?(?:me\s+)?(?:puedes|podrias)\s+",
            "",
            texto,
        ).strip()

        spotify_explicito = "spotify" in texto
        contexto_player = self._spotify_contexto_vigente()

        # Listar playlists propias/seguidas.
        if any(x in texto for x in [
            "mis playlists", "mis playlist", "mis listas de reproduccion",
            "que playlists tengo", "cuales son mis playlists",
            "cuales son mis listas de reproduccion",
        ]):
            return "listar_playlists", ""

        # Preferencias / gustos de la cuenta.
        if spotify_explicito and any(
            x in texto
            for x in [
                "mis preferencias", "mis gustos", "que escucho mas", "que escucho",
                "artistas favoritos", "artistas mas escuchados", "top artistas",
            ]
        ):
            if any(v in texto for v in ["reproduce", "pon", "toca", "escuchar"]):
                return "reproducir_preferencias", ""
            return "preferencias", ""

        # Controles explícitos o contextuales del reproductor.
        if spotify_explicito or contexto_player:
            if any(x in texto for x in [
                "pausa spotify", "pausar spotify", "pausa la musica", "pausa musica",
                "deten la musica", "para la musica", "pausa reproduccion",
            ]):
                return "pausar", ""
            if any(x in texto for x in [
                "siguiente cancion", "proxima cancion", "siguiente tema",
                "proximo tema", "pasa a la siguiente", "salta la cancion",
            ]) or (spotify_explicito and texto in {"siguiente spotify", "siguiente"}):
                return "siguiente", ""
            if any(x in texto for x in [
                "cancion anterior", "tema anterior", "pista anterior",
                "vuelve a la anterior", "anterior cancion",
            ]) or (spotify_explicito and texto in {"anterior spotify", "anterior"}):
                return "anterior", ""
            if any(x in texto for x in [
                "reanuda spotify", "continua spotify", "reanuda la musica",
                "continua la musica", "sigue reproduciendo", "continua reproduccion",
            ]):
                return "reanudar", ""

        # Abrir Spotify sin otra intención.
        if spotify_explicito and any(v in texto for v in ["abre", "abrir", "inicia", "iniciar"]):
            if not any(v in texto for v in ["busca", "buscar", "reproduce", "reproducir", "pon", "toca", "playlist", "lista"]):
                return "abrir", ""

        # Abrir/buscar específicamente una playlist personal.
        if any(x in texto for x in ["playlist", "lista de reproduccion"]):
            if any(v in texto for v in ["abre", "abrir", "busca", "buscar", "encuentra", "muestra"]):
                t = texto
                t = re.sub(r"^(?:abre|abrir|busca|buscar|encuentra|muestra)\s+", "", t).strip()
                t = re.sub(r"^(?:en\s+)?spotify\s+", "", t).strip()
                t = re.sub(r"^(?:mi\s+|mis\s+|la\s+)?(?:playlists?|lista de reproduccion)\s+(?:de\s+|llamada\s+)?", "", t).strip()
                t = re.sub(r"\s+(?:en\s+)?spotify$", "", t).strip(" .,:;-")
                if t:
                    return "abrir_playlist", t

        # Búsqueda visual genérica en Spotify.
        if spotify_explicito and any(v in texto for v in ["busca", "buscar", "buscame", "encuentra"]):
            patrones = [
                r"^(?:abre|abrir|inicia)\s+spotify(?:\s+y)?\s+(?:busca|buscar|buscame|encuentra)\s+(.+)$",
                r"^(?:busca|buscar|buscame|encuentra)\s+(?:en\s+)?spotify\s+(.+)$",
                r"^(?:busca|buscar|buscame|encuentra)\s+(.+?)\s+(?:en\s+)?spotify$",
            ]
            for patron in patrones:
                coincidencia = re.match(patron, texto)
                if coincidencia:
                    consulta = coincidencia.group(1).strip(" .,:;-")
                    return ("buscar", consulta) if consulta else ("abrir", "")
            t = re.sub(r"^(?:abre|abrir|inicia)\s+spotify(?:\s+y)?\s*", "", texto).strip()
            t = re.sub(r"^(?:busca|buscar|buscame|encuentra)\s+", "", t).strip()
            t = re.sub(r"^(?:en\s+)?spotify\s+", "", t).strip()
            t = re.sub(r"\s+(?:en\s+)?spotify$", "", t).strip()
            if t:
                return "buscar", t

        quiere_reproducir = any(v in texto for v in [
            "reproduce", "reproducir", "reproduzca", "pon", "ponme", "toca",
            "tocame", "escucha",
        ])

        # Playlist explícita.
        if quiere_reproducir and any(x in texto for x in ["playlist", "playlists", "lista de reproduccion", "listas de reproduccion"]):
            t = texto
            t = re.sub(r"^(?:abre|abrir|inicia)\s+spotify(?:\s+y)?\s*", "", t).strip()
            t = re.sub(r"^(?:reproduce|reproducir|reproduzca|pon|ponme|toca|tocame|escucha)\s+", "", t).strip()
            t = re.sub(r"^(?:en\s+)?spotify\s+", "", t).strip()
            t = re.sub(r"^(?:mi\s+|mis\s+|la\s+)?(?:playlists?|listas? de reproduccion)\s+(?:de\s+|llamada\s+)?", "", t).strip()
            t = re.sub(r"\s+(?:en\s+)?spotify$", "", t).strip(" .,:;-")
            if t:
                return "reproducir_playlist", t

        # Reproducción genérica. Primero conservamos la semántica explícita
        # "música de X" como artista, salvo que X sea una playlist personal
        # con coincidencia prácticamente exacta.
        es_musica_generica = bool(re.search(
            r"\b(?:reproduce|pon|ponme|toca|tocame)\s+(?:algo\s+de\s+)?musica\b",
            texto,
        ))
        if quiere_reproducir and "youtube" not in texto:
            t = texto
            t = re.sub(r"^(?:abre|abrir|inicia)\s+spotify(?:\s+y)?\s*", "", t).strip()
            t = re.sub(r"^(?:reproduce|reproducir|reproduzca|pon|ponme|toca|tocame|escucha)\s+", "", t).strip()
            t = re.sub(r"^(?:en\s+)?spotify\s+", "", t).strip()
            t = re.sub(r"\s+(?:en\s+)?spotify$", "", t).strip()
            tenia_musica_de = bool(re.match(r"^(?:musica|canciones|temas)\s+(?:de\s+)?", t))
            t = re.sub(r"^(?:musica|canciones|temas)\s+(?:de\s+)?", "", t).strip()
            t = t.strip(" .,:;-")

            if not t or t in {"musica", "algo de musica"}:
                return "reanudar", ""

            # Si el nombre coincide con una playlist personal ya cacheada,
            # reproducimos la playlist aun cuando el usuario no diga la palabra.
            # Para "música de X" exigimos coincidencia muy alta para no romper
            # órdenes normales de artistas.
            umbral = 0.94 if tenia_musica_de else 0.84
            if self._spotify_coincide_playlist_cache(t, umbral=umbral):
                return "reproducir_playlist", t

            if spotify_explicito or es_musica_generica or tenia_musica_de or contexto_player:
                return "reproducir", t

        if texto in {"abre spotify", "abrir spotify", "spotify"}:
            return "abrir", ""
        return None

    def _spotify_proteger_token(self, valor):
        """Protege un token con Windows DPAPI antes de guardarlo en beta.db."""
        valor = (valor or "").strip()
        if not valor:
            return ""
        if os.name != "nt":
            return valor
        try:
            class DATA_BLOB(ctypes.Structure):
                _fields_ = [
                    ("cbData", ctypes.c_ulong),
                    ("pbData", ctypes.POINTER(ctypes.c_byte)),
                ]

            datos = valor.encode("utf-8")
            buffer_entrada = ctypes.create_string_buffer(datos)
            entrada = DATA_BLOB(
                len(datos),
                ctypes.cast(buffer_entrada, ctypes.POINTER(ctypes.c_byte)),
            )
            salida = DATA_BLOB()
            ok = ctypes.windll.crypt32.CryptProtectData(
                ctypes.byref(entrada),
                None,
                None,
                None,
                None,
                0,
                ctypes.byref(salida),
            )
            if not ok:
                raise ctypes.WinError()
            try:
                cifrado = ctypes.string_at(salida.pbData, salida.cbData)
            finally:
                ctypes.windll.kernel32.LocalFree(salida.pbData)
            return "dpapi:" + base64.b64encode(cifrado).decode("ascii")
        except Exception as error:
            print("SPOTIFY: no se pudo proteger un token con DPAPI:", error)
            # No guardamos el secreto si Windows no pudo cifrarlo.
            return ""

    def _spotify_desproteger_token(self, valor_guardado):
        """Descifra tokens DPAPI; admite valores antiguos en texto para migrarlos."""
        valor_guardado = (valor_guardado or "").strip()
        if not valor_guardado:
            return ""
        if not valor_guardado.startswith("dpapi:"):
            return valor_guardado
        if os.name != "nt":
            return ""
        try:
            class DATA_BLOB(ctypes.Structure):
                _fields_ = [
                    ("cbData", ctypes.c_ulong),
                    ("pbData", ctypes.POINTER(ctypes.c_byte)),
                ]

            cifrado = base64.b64decode(valor_guardado[6:])
            buffer_entrada = ctypes.create_string_buffer(cifrado)
            entrada = DATA_BLOB(
                len(cifrado),
                ctypes.cast(buffer_entrada, ctypes.POINTER(ctypes.c_byte)),
            )
            salida = DATA_BLOB()
            ok = ctypes.windll.crypt32.CryptUnprotectData(
                ctypes.byref(entrada),
                None,
                None,
                None,
                None,
                0,
                ctypes.byref(salida),
            )
            if not ok:
                raise ctypes.WinError()
            try:
                plano = ctypes.string_at(salida.pbData, salida.cbData)
            finally:
                ctypes.windll.kernel32.LocalFree(salida.pbData)
            return plano.decode("utf-8")
        except Exception as error:
            print("SPOTIFY: no se pudo descifrar token DPAPI:", error)
            return ""

    def _spotify_guardar_tokens(self, datos, conservar_refresh=True):
        """Guarda tokens operativos cifrados con DPAPI en beta.db."""
        access = (datos.get("access_token") or "").strip()
        refresh = (datos.get("refresh_token") or "").strip()
        expires = int(datos.get("expires_in") or 3600)

        if access:
            self.spotify_access_token = access
            self.spotify_token_expira = time.time() + max(60, expires - 30)
            protegido = self._spotify_proteger_token(access)
            if protegido:
                self.memoria.cambiar_estado("spotify_access_token", protegido)
            self.memoria.cambiar_estado(
                "spotify_token_expira", str(self.spotify_token_expira)
            )

        if refresh:
            self.spotify_refresh_token = refresh
            protegido = self._spotify_proteger_token(refresh)
            if protegido:
                self.memoria.cambiar_estado("spotify_refresh_token", protegido)
        elif not conservar_refresh:
            self.spotify_refresh_token = ""
            self.memoria.cambiar_estado("spotify_refresh_token", "")

    def _spotify_form_post(self, url, campos):
        datos = urllib.parse.urlencode(campos).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=datos,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=SPOTIFY_TIMEOUT) as respuesta:
            return json.loads(respuesta.read().decode("utf-8"))

    def _spotify_api(
        self, metodo, endpoint, params=None, cuerpo=None, reintentar=True
    ):
        token = self._spotify_token_valido()
        if not token:
            raise RuntimeError("Spotify no está conectado a Beta.")

        url = SPOTIFY_API_BASE + endpoint
        if params:
            url += "?" + urllib.parse.urlencode(params)

        data = None
        headers = {"Authorization": f"Bearer {token}"}
        if cuerpo is not None:
            data = json.dumps(cuerpo).encode("utf-8")
            headers["Content-Type"] = "application/json"

        req = urllib.request.Request(
            url, data=data, headers=headers, method=metodo.upper()
        )

        try:
            with urllib.request.urlopen(req, timeout=SPOTIFY_TIMEOUT) as respuesta:
                raw = respuesta.read()
                estado = getattr(respuesta, "status", None) or respuesta.getcode()
                # Spotify devuelve 204 No Content en varias acciones de player
                # (pausa, play, next, previous). Eso es éxito, no un JSON vacío.
                if estado == 204:
                    return {}
                if not raw or not raw.strip():
                    return {}
                texto_raw = raw.decode("utf-8", errors="replace").strip()
                if not texto_raw:
                    return {}
                content_type = str(respuesta.headers.get("Content-Type", "")).lower()
                if "json" not in content_type:
                    # Algunas respuestas exitosas no incluyen JSON. No intentamos
                    # decodificarlas para evitar "Expecting value...".
                    return {}
                return json.loads(texto_raw)

        except urllib.error.HTTPError as error:
            body = ""
            try:
                body = error.read().decode("utf-8", errors="replace")
            except Exception:
                pass

            if error.code == 401 and reintentar and self.spotify_refresh_token:
                self.spotify_token_expira = 0
                if self._spotify_refrescar_token():
                    return self._spotify_api(
                        metodo, endpoint, params, cuerpo, reintentar=False
                    )

            if error.code == 403:
                raise RuntimeError(
                    "Spotify rechazó el control de reproducción. Verifique que "
                    "la cuenta sea Premium y que Beta tenga permisos."
                )
            if error.code == 404:
                raise RuntimeError(
                    "Spotify no encontró un dispositivo de reproducción activo."
                )
            if error.code == 429:
                raise RuntimeError(
                    "Spotify está limitando temporalmente las solicitudes. "
                    "Inténtelo nuevamente en unos segundos."
                )
            raise RuntimeError(
                f"Spotify API respondió {error.code}: {body[:220]}"
            ) from error

    def _spotify_refrescar_token(self):
        if not self.spotify_client_id or not self.spotify_refresh_token:
            return False
        try:
            datos = self._spotify_form_post(
                SPOTIFY_ACCOUNTS_BASE + "/api/token",
                {
                    "grant_type": "refresh_token",
                    "refresh_token": self.spotify_refresh_token,
                    "client_id": self.spotify_client_id,
                },
            )
            self._spotify_guardar_tokens(datos, conservar_refresh=True)
            print("SPOTIFY: token renovado correctamente.")
            return True

        except urllib.error.HTTPError as error:
            detalle = ""
            try:
                detalle = error.read().decode("utf-8", errors="replace")
            except Exception:
                pass
            print("SPOTIFY: no se pudo renovar token:", detalle or error)
            if "invalid_grant" in detalle:
                self.spotify_access_token = ""
                self.spotify_refresh_token = ""
                self.spotify_token_expira = 0
                self.memoria.cambiar_estado("spotify_access_token", "")
                self.memoria.cambiar_estado("spotify_refresh_token", "")
                self.memoria.cambiar_estado("spotify_token_expira", "0")
            return False

        except Exception as error:
            print("SPOTIFY: error renovando token:", error)
            return False

    def _spotify_token_valido(self):
        # Lock reentrante no es necesario porque el refresco no vuelve a llamar
        # a esta función; evita dos renovaciones simultáneas.
        with self.spotify_lock:
            if (
                self.spotify_access_token
                and time.time() < self.spotify_token_expira - 20
            ):
                return self.spotify_access_token
            if self.spotify_refresh_token and self._spotify_refrescar_token():
                return self.spotify_access_token
            return ""

    def configurar_spotify(self):
        mensaje = (
            "Para que Beta reproduzca música automáticamente necesita conectar "
            "su cuenta de Spotify.\n\n"
            "1. Cree una aplicación en Spotify for Developers.\n"
            f"2. Agregue exactamente esta Redirect URI: {SPOTIFY_REDIRECT_URI}\n"
            "3. Copie el Client ID y péguelo en la siguiente ventana.\n\n"
            "Beta usa PKCE, por lo que NO necesita guardar Client Secret."
        )
        abrir = messagebox.askyesno(
            "Conectar Spotify",
            mensaje + "\n\n¿Desea abrir Spotify for Developers ahora?",
            parent=self.root,
        )
        if abrir:
            try:
                self.abrir_url_en_chrome("https://developer.spotify.com/dashboard")
            except Exception:
                pass

        client_id = simpledialog.askstring(
            "Spotify - Client ID",
            "Pegue el Client ID de su aplicación de Spotify:",
            initialvalue=self.spotify_client_id,
            parent=self.root,
        )
        if not client_id or not client_id.strip():
            return

        self.spotify_client_id = client_id.strip()
        self.memoria.cambiar_estado("spotify_client_id", self.spotify_client_id)
        self.conectar_spotify_async()

    def conectar_spotify_async(self):
        if not self.spotify_client_id:
            self.configurar_spotify()
            return

        def trabajo():
            verifier = secrets.token_urlsafe(64)[:96]
            challenge = (
                base64.urlsafe_b64encode(
                    hashlib.sha256(verifier.encode("ascii")).digest()
                )
                .decode("ascii")
                .rstrip("=")
            )
            state = secrets.token_urlsafe(24)
            resultado = {}

            class CallbackHandler(http.server.BaseHTTPRequestHandler):
                def do_GET(self_h):
                    parsed = urllib.parse.urlparse(self_h.path)
                    qs = urllib.parse.parse_qs(parsed.query)
                    code = (qs.get("code") or [""])[0]
                    estado = (qs.get("state") or [""])[0]
                    error_oauth = (qs.get("error") or [""])[0]

                    # Navegadores pueden pedir favicon u otros recursos antes o
                    # después del callback. Solo damos por terminada la espera si
                    # realmente llegó code=... o error=... desde Spotify.
                    if parsed.path == "/callback" and (code or error_oauth):
                        resultado["code"] = code
                        resultado["state"] = estado
                        resultado["error"] = error_oauth
                        pagina = (
                            "<html><body style='font-family:Segoe UI;padding:40px'>"
                            "<h2>Beta + Spotify</h2>"
                            "<p>Autorización recibida. Ya puede cerrar esta ventana "
                            "y volver a Beta.</p></body></html>"
                        ).encode("utf-8")
                        self_h.send_response(200)
                        self_h.send_header("Content-Type", "text/html; charset=utf-8")
                        self_h.send_header("Content-Length", str(len(pagina)))
                        self_h.end_headers()
                        self_h.wfile.write(pagina)
                    else:
                        self_h.send_response(204)
                        self_h.end_headers()

                def log_message(self_h, fmt, *args):
                    return

            try:
                server = http.server.HTTPServer(
                    (SPOTIFY_CALLBACK_HOST, SPOTIFY_CALLBACK_PORT),
                    CallbackHandler,
                )
                server.timeout = 180
            except OSError as error:
                detalle = str(error)
                self.root.after(
                    0,
                    lambda d=detalle: messagebox.showerror(
                        "Spotify",
                        f"No pude abrir el puerto {SPOTIFY_CALLBACK_PORT} para "
                        f"recibir la autorización.\n\n{d}",
                        parent=self.root,
                    ),
                )
                return

            params = {
                "client_id": self.spotify_client_id,
                "response_type": "code",
                "redirect_uri": SPOTIFY_REDIRECT_URI,
                "scope": SPOTIFY_SCOPES,
                "code_challenge_method": "S256",
                "code_challenge": challenge,
                "state": state,
            }
            auth_url = (
                SPOTIFY_ACCOUNTS_BASE
                + "/authorize?"
                + urllib.parse.urlencode(params)
            )
            self.root.after(0, lambda u=auth_url: self.abrir_url_en_chrome(u))
            print("SPOTIFY: esperando autorización en el navegador...")

            limite = time.time() + 180
            try:
                # Espera hasta tres minutos, ignorando peticiones auxiliares del
                # navegador que no contengan el código OAuth válido.
                while time.time() < limite and not (resultado.get("code") or resultado.get("error")):
                    server.timeout = min(2.0, max(0.2, limite - time.time()))
                    server.handle_request()
            finally:
                server.server_close()

            if resultado.get("error"):
                self.root.after(
                    0,
                    lambda: self.responder(
                        "la autorización de Spotify fue cancelada.", "normal"
                    ),
                )
                return

            if not resultado.get("code") or resultado.get("state") != state:
                self.root.after(
                    0,
                    lambda: self.responder(
                        "no pude completar la autorización de Spotify.",
                        "confundida",
                    ),
                )
                return

            try:
                datos = self._spotify_form_post(
                    SPOTIFY_ACCOUNTS_BASE + "/api/token",
                    {
                        "client_id": self.spotify_client_id,
                        "grant_type": "authorization_code",
                        "code": resultado["code"],
                        "redirect_uri": SPOTIFY_REDIRECT_URI,
                        "code_verifier": verifier,
                    },
                )
                self._spotify_guardar_tokens(datos, conservar_refresh=False)
                self.spotify_autorizado_en = datetime.now().isoformat(
                    timespec="seconds"
                )
                self.memoria.cambiar_estado(
                    "spotify_autorizado_en", self.spotify_autorizado_en
                )
                print("SPOTIFY: cuenta conectada correctamente.")
                try:
                    self._spotify_obtener_mis_playlists(forzar=True)
                except Exception as error_playlists:
                    print("SPOTIFY: cuenta conectada, pero no pude precargar playlists:", error_playlists)
                self.root.after(
                    0,
                    lambda: self.responder(
                        "Spotify quedó conectado. Ya puedo controlar la reproducción y consultar sus playlists personales.",
                        "feliz",
                    ),
                )
            except Exception as error:
                print("SPOTIFY: error intercambiando autorización:", error)
                self.root.after(
                    0,
                    lambda: self.responder(
                        "no pude terminar de conectar Spotify. Revise el "
                        "Client ID y la Redirect URI.",
                        "confundida",
                    ),
                )

        threading.Thread(target=trabajo, daemon=True).start()

    def desconectar_spotify(self):
        self.spotify_access_token = ""
        self.spotify_refresh_token = ""
        self.spotify_token_expira = 0.0
        self.spotify_autorizado_en = ""
        for clave in [
            "spotify_access_token",
            "spotify_refresh_token",
            "spotify_token_expira",
            "spotify_autorizado_en",
        ]:
            self.memoria.cambiar_estado(clave, "")
        self.responder("desconecté la cuenta de Spotify de Beta.", "normal")

    def abrir_spotify_sin_respuesta(self):
        try:
            os.startfile("spotify:")
            return True
        except Exception:
            try:
                self.abrir_url_en_chrome("https://open.spotify.com/")
                return True
            except Exception:
                return False

    def abrir_spotify_inicio(self):
        if self.abrir_spotify_sin_respuesta():
            self._spotify_marcar_contexto()
            self.responder("abriendo Spotify.", "feliz")
        else:
            self.responder(
                "no pude abrir Spotify en este computador.", "molesta"
            )

    def buscar_en_spotify(self, consulta):
        consulta = (consulta or "").strip()
        if not consulta:
            self.abrir_spotify_inicio()
            return

        try:
            uri = "spotify:search:" + urllib.parse.quote(consulta, safe="")
            try:
                os.startfile(uri)
            except Exception:
                self.abrir_url_en_chrome(
                    "https://open.spotify.com/search/"
                    + urllib.parse.quote(consulta, safe="")
                )
            self._spotify_marcar_contexto()
            self.responder(f"buscando {consulta} en Spotify.", "feliz")
        except Exception as error:
            print("SPOTIFY: error buscando:", error)
            self.responder(
                "no pude abrir la búsqueda en Spotify.", "molesta"
            )

    def _spotify_dispositivo(self):
        datos = self._spotify_api("GET", "/me/player/devices")
        devices = [
            d
            for d in datos.get("devices", [])
            if d.get("id") and not d.get("is_restricted")
        ]
        if not devices:
            return None

        for device in devices:
            if device.get("is_active"):
                return device
        for device in devices:
            if str(device.get("type", "")).lower() == "computer":
                return device
        return devices[0]

    def _spotify_asegurar_dispositivo(self):
        # Abrir el cliente ayuda a que el PC aparezca como dispositivo Connect.
        self.abrir_spotify_sin_respuesta()
        for espera in [0.4, 1.2, 2.0]:
            time.sleep(espera)
            try:
                dispositivo = self._spotify_dispositivo()
            except Exception:
                dispositivo = None
            if dispositivo:
                return dispositivo
        return None

    def _spotify_buscar_artista(self, consulta):
        datos = self._spotify_api(
            "GET",
            "/search",
            params={
                "q": f"artist:{consulta}",
                "type": "artist",
                "limit": 5,
            },
        )
        items = (datos.get("artists") or {}).get("items") or []
        if not items:
            return None

        consulta_normalizada = normalizar(consulta)
        elegido = None
        for item in items:
            if normalizar(item.get("name", "")) == consulta_normalizada:
                elegido = item
                break
        if elegido is None:
            elegido = items[0]
        if elegido and elegido.get("name"):
            self._spotify_guardar_vocabulario([elegido.get("name")])
        return elegido

    def _spotify_normalizar_nombre_playlist(self, texto):
        t = normalizar(texto or "")
        t = t.replace("_", " ").replace("-", " ")
        t = re.sub(r"[^a-z0-9 ]+", " ", t)
        t = re.sub(r"\b(?:mi|mis|la|el|playlist|playlists)\b", " ", t)
        t = re.sub(r"\blista(?:s)? de reproduccion\b", " ", t)
        return re.sub(r"\s+", " ", t).strip()

    def _spotify_guardar_cache_playlists(self, items):
        limpios = []
        for item in items or []:
            if not isinstance(item, dict):
                continue
            nombre = str(item.get("name") or "").strip()
            uri = str(item.get("uri") or "").strip()
            if not nombre or not uri:
                continue
            owner = item.get("owner") or {}
            limpios.append({
                "id": item.get("id") or "",
                "name": nombre,
                "uri": uri,
                "url": ((item.get("external_urls") or {}).get("spotify") or ""),
                "owner": owner.get("display_name") or owner.get("id") or "",
                "public": item.get("public"),
            })
        self.spotify_playlists_cache = limpios[:300]
        self.spotify_playlists_cache_ts = time.time()
        try:
            self.memoria.cambiar_estado(
                "spotify_playlists_cache",
                json.dumps(self.spotify_playlists_cache, ensure_ascii=False),
            )
            self.memoria.cambiar_estado(
                "spotify_playlists_cache_ts", str(self.spotify_playlists_cache_ts)
            )
        except Exception:
            pass

    def _spotify_obtener_mis_playlists(self, forzar=False):
        # Caché breve para no consultar la API en cada frase de voz.
        if (
            not forzar
            and self.spotify_playlists_cache
            and time.time() - self.spotify_playlists_cache_ts < 300
        ):
            return list(self.spotify_playlists_cache)

        items = []
        offset = 0
        limit = 50
        try:
            while offset < 300:
                datos = self._spotify_api(
                    "GET", "/me/playlists",
                    params={"limit": limit, "offset": offset},
                )
                lote = [x for x in (datos.get("items") or []) if isinstance(x, dict)]
                items.extend(lote)
                total = int(datos.get("total") or len(items))
                if not lote or len(items) >= total or len(lote) < limit:
                    break
                offset += len(lote)
        except Exception as error:
            # Los tokens creados con v2.6.4 no incluían playlist-read-private.
            # Si existe una caché vieja, aún podemos usarla; si no, guiamos a
            # reautorizar una sola vez desde el menú de Spotify.
            if self.spotify_playlists_cache:
                print("SPOTIFY: no pude refrescar playlists; usando caché local:", error)
                return list(self.spotify_playlists_cache)
            raise RuntimeError(
                "necesito actualizar los permisos de Spotify para leer sus playlists. "
                "Use clic derecho, Spotify, Reconectar o actualizar permisos y autorice nuevamente la cuenta."
            ) from error

        self._spotify_guardar_cache_playlists(items)
        if items:
            print(f"SPOTIFY: {len(items)} playlist(s) personales disponibles.")
        return list(self.spotify_playlists_cache)

    def _spotify_score_playlist(self, consulta, nombre):
        q = self._spotify_normalizar_nombre_playlist(consulta)
        n = self._spotify_normalizar_nombre_playlist(nombre)
        if not q or not n:
            return 0.0
        if q == n:
            return 1.0
        if q in n or n in q:
            base = 0.92 if min(len(q), len(n)) >= 4 else 0.82
        else:
            base = difflib.SequenceMatcher(None, q, n).ratio()
        pq, pn = set(q.split()), set(n.split())
        if pq and pn:
            overlap = len(pq & pn) / max(len(pq), len(pn))
            base = max(base, 0.55 + 0.40 * overlap)
        return min(1.0, base)

    def _spotify_coincide_playlist_cache(self, consulta, umbral=0.84):
        if not self.spotify_playlists_cache:
            return False
        mejor = max(
            (self._spotify_score_playlist(consulta, p.get("name", "")) for p in self.spotify_playlists_cache),
            default=0.0,
        )
        return mejor >= float(umbral)

    def _spotify_buscar_playlist_personal(self, consulta, forzar=False):
        items = self._spotify_obtener_mis_playlists(forzar=forzar)
        if not items:
            return None
        puntuados = [
            (self._spotify_score_playlist(consulta, item.get("name", "")), item)
            for item in items
        ]
        puntuados.sort(key=lambda x: x[0], reverse=True)
        score, mejor = puntuados[0]
        print(
            "SPOTIFY PLAYLIST PERSONAL:",
            f"consulta='{consulta}' mejor='{mejor.get('name')}' score={score:.3f}"
        )
        if score >= 0.72:
            return mejor
        return None

    def _spotify_buscar_playlist(self, consulta):
        # Primero se consulta /me/playlists. El endpoint global /search no es
        # fiable para playlists privadas o personales, por eso queda de respaldo.
        try:
            personal = self._spotify_buscar_playlist_personal(consulta)
            if personal:
                return personal
        except Exception as error:
            print("SPOTIFY: búsqueda personal de playlist:", error)
            # Propagamos errores de permisos para que el usuario sepa que debe
            # reautorizar; otros casos todavía pueden intentar búsqueda global.
            if "actualizar los permisos" in str(error).lower():
                raise

        datos = self._spotify_api(
            "GET",
            "/search",
            params={"q": consulta, "type": "playlist", "limit": 8},
        )
        items = [x for x in ((datos.get("playlists") or {}).get("items") or []) if x]
        if not items:
            return None
        q = self._spotify_normalizar_nombre_playlist(consulta)
        puntuados = [
            (self._spotify_score_playlist(q, item.get("name", "")), item)
            for item in items
        ]
        puntuados.sort(key=lambda x: x[0], reverse=True)
        return puntuados[0][1] if puntuados else items[0]

    def spotify_listar_playlists_async(self):
        if not self.spotify_client_id or not (self.spotify_refresh_token or self.spotify_access_token):
            self.responder(
                "para consultar sus playlists, primero conecte Spotify desde mi menú.",
                "confundida",
            )
            return

        def trabajo():
            try:
                playlists = self._spotify_obtener_mis_playlists(forzar=True)
                nombres = [p.get("name") for p in playlists if p.get("name")]
                if not nombres:
                    texto = "no encontré playlists en su biblioteca de Spotify."
                else:
                    visibles = nombres[:8]
                    texto = "entre sus playlists de Spotify están " + ", ".join(visibles)
                    if len(nombres) > len(visibles):
                        texto += f", y {len(nombres) - len(visibles)} más"
                    texto += "."
                self.root.after(0, lambda t=texto: self.responder(t, "feliz"))
            except Exception as error:
                detalle = self._spotify_error_amigable(error)
                self.root.after(0, lambda d=detalle: self.responder(d, "confundida"))

        threading.Thread(target=trabajo, daemon=True).start()

    def abrir_playlist_spotify_async(self, consulta):
        consulta = (consulta or "").strip()
        if not consulta:
            self.responder("necesito el nombre de la playlist que desea abrir.", "confundida")
            return

        def trabajo():
            try:
                playlist = self._spotify_buscar_playlist(consulta)
                if not playlist:
                    raise RuntimeError(f"no encontré la playlist {consulta} en su biblioteca de Spotify.")
                nombre = playlist.get("name") or consulta
                uri = playlist.get("uri") or ""
                url = ((playlist.get("external_urls") or {}).get("spotify") or playlist.get("url") or "")

                def abrir_y_responder():
                    try:
                        if uri:
                            os.startfile(uri)
                        elif url:
                            self.abrir_url_en_chrome(url)
                        else:
                            raise RuntimeError("playlist sin enlace")
                        self._spotify_marcar_contexto()
                        self.responder(f"abriendo su playlist {nombre} en Spotify.", "feliz")
                    except Exception:
                        if url:
                            self.abrir_url_en_chrome(url)
                            self.responder(f"abriendo su playlist {nombre} en Spotify.", "feliz")
                        else:
                            self.responder("no pude abrir esa playlist en Spotify.", "confundida")
                self.root.after(0, abrir_y_responder)
            except Exception as error:
                detalle = self._spotify_error_amigable(error)
                print("SPOTIFY: error abriendo playlist:", error)
                self.root.after(0, lambda d=detalle: self.responder(d, "confundida"))

        threading.Thread(target=trabajo, daemon=True).start()

    def _spotify_error_amigable(self, error):
        detalle = str(error or "").strip()
        bajo = detalle.lower()
        if not detalle:
            return "Spotify no pudo completar esa acción."
        if "expecting value" in bajo or "json" in bajo and "decode" in bajo:
            return "Spotify recibió la orden, pero no devolvió una respuesta interpretable. Inténtelo nuevamente."
        if "no encontré un dispositivo" in bajo or "dispositivo" in bajo and "activo" in bajo:
            return "no encontré un dispositivo Spotify activo. Abra Spotify y reproduzca una canción manualmente una vez."
        if "actualizar los permisos" in bajo or "playlist-read-private" in bajo:
            return (
                "necesito que vuelva a autorizar Spotify una vez para poder leer sus playlists. "
                "Use clic derecho, Spotify, Reconectar o actualizar permisos."
            )
        if "premium" in bajo:
            return "Spotify rechazó el control de reproducción. Verifique que la cuenta Premium siga conectada."
        if detalle.startswith("Spotify API respondió"):
            return "Spotify no pudo completar esa acción en este momento."
        return detalle

    def _spotify_esperar_fin_voz_y_ejecutar(self, funcion):
        """Evita que Daniela y Spotify empiecen a sonar a la vez."""

        def trabajo():
            inicio = time.time()
            vio_habla = False
            while time.time() - inicio < 12:
                if self.hablando:
                    vio_habla = True
                elif vio_habla:
                    break
                elif time.time() - inicio > 2.0:
                    break
                time.sleep(0.05)

            try:
                funcion()
            except Exception as error:
                detalle = self._spotify_error_amigable(error)
                print("SPOTIFY: error ejecutando tras voz:", error)
                self.root.after(
                    0,
                    lambda d=detalle: self.responder(d, "confundida"),
                )

        threading.Thread(target=trabajo, daemon=True).start()

    def _spotify_reproducir_contexto(self, uri, device_id=None):
        params = {"device_id": device_id} if device_id else None
        self._spotify_api(
            "PUT",
            "/me/player/play",
            params=params,
            cuerpo={"context_uri": uri},
        )

    def reproducir_spotify_async(self, consulta):
        consulta = (consulta or "").strip()
        if not consulta:
            self.spotify_control_async("reanudar")
            return

        if not self.spotify_client_id or not (
            self.spotify_refresh_token or self.spotify_access_token
        ):
            self.buscar_en_spotify(consulta)
            self.root.after(
                100,
                lambda: messagebox.showinfo(
                    "Spotify",
                    "Abrí la búsqueda en Spotify. Para que Beta pueda iniciar "
                    "la reproducción automáticamente, conecte su cuenta desde: "
                    "clic derecho > Spotify > Configurar / conectar cuenta.\n\n"
                    "El control de reproducción mediante la Web API requiere "
                    "Spotify Premium.",
                    parent=self.root,
                ),
            )
            return

        token_proceso = self.iniciar_proceso("spotify")
        if token_proceso is None:
            self.responder(
                "estoy terminando la operación anterior. Inténtelo nuevamente "
                "en unos segundos.",
                "confundida",
            )
            return

        def trabajo():
            try:
                artista = self._spotify_buscar_artista(consulta)
                if not artista:
                    raise RuntimeError(
                        f"no encontré el artista {consulta} en Spotify."
                    )

                dispositivo = self._spotify_asegurar_dispositivo()
                if not dispositivo:
                    raise RuntimeError(
                        "abrí Spotify, pero todavía no aparece un dispositivo "
                        "disponible. Reproduzca una canción manualmente una vez "
                        "y vuelva a intentarlo."
                    )

                nombre = artista.get("name") or consulta
                uri = artista.get("uri")
                device_id = dispositivo.get("id")
                self.terminar_proceso(token_proceso)

                def confirmar():
                    self._spotify_marcar_contexto()
                    self.responder(
                        f"reproduciendo música de {nombre} en Spotify.",
                        "feliz",
                    )
                    self._spotify_esperar_fin_voz_y_ejecutar(
                        lambda: self._spotify_reproducir_contexto(
                            uri, device_id
                        )
                    )

                self.root.after(0, confirmar)

            except Exception as error:
                self.terminar_proceso(token_proceso)
                detalle = str(error)
                print("SPOTIFY: error reproduciendo artista:", detalle)
                self.root.after(
                    0,
                    lambda d=detalle: self.responder(d, "confundida"),
                )

        threading.Thread(target=trabajo, daemon=True).start()

    def reproducir_playlist_spotify_async(self, consulta):
        consulta = (consulta or "").strip()
        if not consulta:
            self.responder("necesito el nombre de la playlist que desea reproducir.", "confundida")
            return

        if not self.spotify_client_id or not (
            self.spotify_refresh_token or self.spotify_access_token
        ):
            self.buscar_en_spotify(consulta)
            return

        token_proceso = self.iniciar_proceso("spotify_playlist")
        if token_proceso is None:
            self.responder("estoy terminando la operación anterior. Inténtelo nuevamente en unos segundos.", "confundida")
            return

        def trabajo():
            try:
                playlist = self._spotify_buscar_playlist(consulta)
                if not playlist:
                    raise RuntimeError(f"no encontré la playlist {consulta} en Spotify.")
                dispositivo = self._spotify_asegurar_dispositivo()
                if not dispositivo:
                    raise RuntimeError("no encontré un dispositivo Spotify disponible.")
                nombre = playlist.get("name") or consulta
                uri = playlist.get("uri")
                device_id = dispositivo.get("id")
                print(f"SPOTIFY: playlist resuelta '{consulta}' -> '{nombre}'.")
                self.terminar_proceso(token_proceso)

                def confirmar():
                    self._spotify_marcar_contexto()
                    self.responder(f"reproduciendo la playlist {nombre} en Spotify.", "feliz")
                    self._spotify_esperar_fin_voz_y_ejecutar(
                        lambda: self._spotify_reproducir_contexto(uri, device_id)
                    )
                self.root.after(0, confirmar)
            except Exception as error:
                self.terminar_proceso(token_proceso)
                detalle = self._spotify_error_amigable(error)
                print("SPOTIFY: error reproduciendo playlist:", error)
                self.root.after(0, lambda d=detalle: self.responder(d, "confundida"))

        threading.Thread(target=trabajo, daemon=True).start()

    def spotify_control_async(self, accion):
        if not self.spotify_client_id or not (
            self.spotify_refresh_token or self.spotify_access_token
        ):
            if accion == "reanudar":
                self.abrir_spotify_inicio()
            else:
                self.responder(
                    "primero debe conectar Spotify desde el menú de Beta.",
                    "confundida",
                )
            return

        def trabajo():
            try:
                dispositivo = self._spotify_asegurar_dispositivo()
                if not dispositivo:
                    raise RuntimeError(
                        "no encontré un dispositivo Spotify disponible."
                    )
                device_id = dispositivo.get("id")

                if accion == "reanudar":
                    frase = "reanudando Spotify."
                    funcion = lambda: self._spotify_api(
                        "PUT",
                        "/me/player/play",
                        params={"device_id": device_id},
                    )
                elif accion == "pausar":
                    frase = "pausando Spotify."
                    funcion = lambda: self._spotify_api(
                        "PUT",
                        "/me/player/pause",
                        params={"device_id": device_id},
                    )
                elif accion == "siguiente":
                    frase = "pasando a la siguiente canción."
                    funcion = lambda: self._spotify_api(
                        "POST",
                        "/me/player/next",
                        params={"device_id": device_id},
                    )
                else:
                    frase = "volviendo a la canción anterior."
                    funcion = lambda: self._spotify_api(
                        "POST",
                        "/me/player/previous",
                        params={"device_id": device_id},
                    )

                def confirmar():
                    self._spotify_marcar_contexto()
                    self.responder(frase, "feliz")
                    self._spotify_esperar_fin_voz_y_ejecutar(funcion)

                self.root.after(0, confirmar)

            except Exception as error:
                detalle = self._spotify_error_amigable(error)
                print("SPOTIFY: error de control:", error)
                self.root.after(
                    0,
                    lambda d=detalle: self.responder(d, "confundida"),
                )

        threading.Thread(target=trabajo, daemon=True).start()

    def spotify_preferencias_async(self):
        if not self.spotify_client_id or not (
            self.spotify_refresh_token or self.spotify_access_token
        ):
            self.responder(
                "para consultar sus preferencias de Spotify, primero conecte "
                "la cuenta desde mi menú.",
                "confundida",
            )
            return

        def trabajo():
            try:
                datos = self._spotify_api(
                    "GET",
                    "/me/top/artists",
                    params={"time_range": "medium_term", "limit": 5},
                )
                nombres = [
                    item.get("name", "").strip()
                    for item in datos.get("items", [])
                    if item.get("name")
                ]

                if nombres:
                    self._spotify_guardar_vocabulario(nombres)

                if not nombres:
                    texto = (
                        "Spotify todavía no me devolvió suficientes "
                        "preferencias para mostrar."
                    )
                elif len(nombres) == 1:
                    texto = (
                        "Según Spotify, entre sus artistas más escuchados está "
                        + nombres[0]
                        + "."
                    )
                else:
                    texto = (
                        "Según Spotify, entre sus artistas más escuchados están "
                        + ", ".join(nombres[:-1])
                        + " y "
                        + nombres[-1]
                        + "."
                    )

                # Los metadatos de Spotify se formatean directamente y no se
                # pasan a Qwen ni se usan para entrenamiento/aprendizaje del LLM.
                self.root.after(
                    0, lambda t=texto: self.responder(t, "feliz")
                )

            except Exception as error:
                detalle = str(error)
                print("SPOTIFY: error leyendo preferencias:", detalle)
                self.root.after(
                    0,
                    lambda d=detalle: self.responder(d, "confundida"),
                )

        threading.Thread(target=trabajo, daemon=True).start()

    def reproducir_preferencias_spotify_async(self):
        if not self.spotify_client_id or not (
            self.spotify_refresh_token or self.spotify_access_token
        ):
            self.responder(
                "para reproducir sus preferencias de Spotify, primero conecte "
                "la cuenta desde mi menú.",
                "confundida",
            )
            return

        def trabajo():
            try:
                datos = self._spotify_api(
                    "GET",
                    "/me/top/artists",
                    params={"time_range": "medium_term", "limit": 10},
                )
                items = [
                    item
                    for item in datos.get("items", [])
                    if item.get("uri")
                ]
                self._spotify_guardar_vocabulario([item.get("name") for item in items if item.get("name")])
                if not items:
                    raise RuntimeError(
                        "Spotify todavía no me entregó preferencias suficientes "
                        "para elegir música."
                    )

                candidatos = items[:5] if len(items) >= 5 else items
                artista = random.choice(candidatos)
                dispositivo = self._spotify_asegurar_dispositivo()
                if not dispositivo:
                    raise RuntimeError(
                        "no encontré un dispositivo Spotify disponible."
                    )

                nombre = artista.get(
                    "name", "uno de sus artistas preferidos"
                )
                uri = artista.get("uri")
                device_id = dispositivo.get("id")

                def confirmar():
                    self._spotify_marcar_contexto()
                    self.responder(
                        f"elegí {nombre} según sus preferencias de Spotify. "
                        "Comenzaré a reproducirlo.",
                        "feliz",
                    )
                    self._spotify_esperar_fin_voz_y_ejecutar(
                        lambda: self._spotify_reproducir_contexto(
                            uri, device_id
                        )
                    )

                self.root.after(0, confirmar)

            except Exception as error:
                detalle = str(error)
                print("SPOTIFY: error reproduciendo preferencias:", detalle)
                self.root.after(
                    0,
                    lambda d=detalle: self.responder(d, "confundida"),
                )

        threading.Thread(target=trabajo, daemon=True).start()


    def extraer_orden_youtube(self, comando):
        """Detecta órdenes específicas para YouTube.

        Devuelve una tupla:
            (consulta, reproducir_primero, solo_abrir_youtube)

        Ejemplos aceptados:
        - "Beta, abre YouTube"
        - "Beta, busca en YouTube Luli Pampín"
        - "Beta, abre YouTube y reproduce Luli Pampín"
        - "Beta, reproduce en YouTube música de Luli Pampín"
        - "Beta, pon un video de Dragon Ball Z en YouTube"
        - "Beta, abre Google Chrome, ve a YouTube y reproduce Luli Pampín"
        """
        original = (comando or "").strip()
        if not original:
            return None

        texto = normalizar(original)
        texto = re.sub(
            r"^(?:beta|veta|meta|metas|petra)\s+",
            "",
            texto,
        ).strip()

        # Toleramos variantes pequeñas que pueden aparecer en Whisper/Vosk.
        contiene_youtube = any(
            palabra in texto
            for palabra in ["youtube", "yutube", "yutu"]
        )
        if not contiene_youtube:
            return None

        # Quitar fórmulas de cortesía al principio.
        texto = re.sub(
            r"^(?:por favor\s+)?(?:me\s+)?(?:puedes|podrias|podrias)\s+",
            "",
            texto,
        ).strip()

        verbos_reproducir = [
            "reproduce", "reproducir", "reproduzca", "reproduceme",
            "pon", "poner", "ponme", "toca", "tocame", "coloca",
            "quiero escuchar", "quiero ver",
        ]
        verbos_buscar = ["busca", "buscar", "buscame", "encuentra"]

        quiere_reproducir = any(v in texto for v in verbos_reproducir)
        quiere_buscar = any(v in texto for v in verbos_buscar)

        # Si solo pide abrir YouTube, no hace falta extraer ninguna consulta.
        if not quiere_reproducir and not quiere_buscar:
            if any(v in texto for v in ["abre", "abrir", "entra", "ve a", "inicia"]):
                return "", False, True
            return None

        patrones_reproducir = [
            # abre Google Chrome y ve a YouTube y reproduce X
            r"^(?:abre|abrir|inicia)\s+(?:google\s+)?chrome(?:\s+y)?(?:\s+ve\s+a|\s+entra\s+a)?\s+youtube(?:\s+y)?\s+(?:reproduce|reproducir|reproduzca|pon|ponme|toca|coloca)\s+(.+)$",
            # abre YouTube y reproduce X
            r"^(?:abre|abrir|entra\s+a|ve\s+a|inicia)\s+youtube(?:\s+y)?\s+(?:reproduce|reproducir|reproduzca|pon|ponme|toca|coloca)\s+(.+)$",
            # reproduce/pon X en YouTube
            r"^(?:reproduce|reproducir|reproduzca|reproduceme|pon|ponme|poner|toca|tocame|coloca)\s+(.+?)\s+(?:en\s+)?youtube$",
            # reproduce/pon en YouTube X
            r"^(?:reproduce|reproducir|reproduzca|reproduceme|pon|ponme|poner|toca|tocame|coloca)\s+(?:en\s+)?youtube\s+(.+)$",
            # quiero escuchar/ver X en YouTube
            r"^(?:quiero\s+escuchar|quiero\s+ver)\s+(.+?)\s+(?:en\s+)?youtube$",
        ]

        patrones_buscar = [
            r"^(?:abre|abrir)\s+(?:google\s+)?chrome(?:\s+y)?\s+(?:ve\s+a\s+)?youtube(?:\s+y)?\s+(?:busca|buscar|buscame|encuentra)\s+(.+)$",
            r"^(?:abre|abrir|entra\s+a|ve\s+a)\s+youtube(?:\s+y)?\s+(?:busca|buscar|buscame|encuentra)\s+(.+)$",
            r"^(?:busca|buscar|buscame|encuentra)\s+(?:en\s+)?youtube\s+(.+)$",
            r"^(?:busca|buscar|buscame|encuentra)\s+(.+?)\s+(?:en\s+)?youtube$",
        ]

        consulta = ""
        patrones = patrones_reproducir if quiere_reproducir else patrones_buscar
        for patron in patrones:
            coincidencia = re.match(patron, texto, flags=re.IGNORECASE)
            if coincidencia:
                consulta = coincidencia.group(1).strip()
                break

        # Respaldo tolerante para frases naturales más largas.
        if not consulta:
            t = texto
            t = re.sub(
                r"^(?:abre|abrir|inicia)\s+(?:google\s+)?chrome(?:\s+y)?\s*",
                "",
                t,
            ).strip()
            t = re.sub(
                r"^(?:ve|vaya|ir|entra)(?:\s+especificamente)?\s+a\s+youtube(?:\s+y)?\s*",
                "",
                t,
            ).strip()
            t = re.sub(r"^youtube(?:\s+y)?\s*", "", t).strip()
            t = re.sub(
                r"^(?:reproduce|reproducir|reproduzca|reproduceme|pon|ponme|poner|toca|tocame|coloca|busca|buscar|buscame|encuentra)\s+",
                "",
                t,
            ).strip()
            t = re.sub(r"^(?:en\s+)?youtube\s+", "", t).strip()
            t = re.sub(r"\s+(?:en\s+)?youtube$", "", t).strip()
            consulta = t

        consulta = re.sub(
            r"^(?:algun|alguna|un|una)\s+(?:video|videos|cancion|canciones|musica)\s+(?:de|sobre|relacionado\s+con|relacionada\s+con)?\s*",
            "",
            consulta,
            flags=re.IGNORECASE,
        ).strip()
        consulta = re.sub(
            r"^(?:algo\s+)?(?:relacionado\s+con|sobre|acerca\s+de)\s+",
            "",
            consulta,
            flags=re.IGNORECASE,
        ).strip()
        consulta = consulta.strip(" .,:;-\t\n")

        if len(consulta) < 2:
            return "", False, True

        print(
            "YOUTUBE DETECTADO:",
            "reproducir" if quiere_reproducir else "buscar",
            "->",
            consulta,
        )
        return consulta, bool(quiere_reproducir), False

    def abrir_url_en_chrome(self, url):
        """Abre una URL en Google Chrome cuando está instalado."""
        chrome = self.obtener_ruta_chrome()
        if chrome:
            subprocess.Popen([chrome, url])
        else:
            os.startfile(url)

    def abrir_youtube_inicio(self):
        try:
            self.abrir_url_en_chrome("https://www.youtube.com/")
            self.responder("abriendo YouTube en Google Chrome.", "feliz")
        except Exception as error:
            print("ERROR ABRIENDO YOUTUBE:", error)
            self.responder("no pude abrir YouTube.", "molesta")

    def buscar_en_youtube(self, consulta):
        consulta = (consulta or "").strip()
        if not consulta:
            self.abrir_youtube_inicio()
            return

        try:
            consulta_url = urllib.parse.quote_plus(consulta)
            url = f"https://www.youtube.com/results?search_query={consulta_url}"
            self.abrir_url_en_chrome(url)
            consulta_hablada = consulta if len(consulta) <= 80 else consulta[:77] + "..."
            self.responder(
                f"abriendo YouTube. Le muestro resultados sobre {consulta_hablada}.",
                "feliz",
            )
        except Exception as error:
            print("ERROR BUSCANDO EN YOUTUBE:", error)
            self.responder("no pude abrir la búsqueda en YouTube.", "molesta")

    def obtener_primer_video_youtube(self, consulta):
        """Usa yt-dlp solo como buscador y devuelve la URL del primer resultado.

        No descarga ningún video. Se utiliza ``ytsearch1`` + ``--flat-playlist``
        para obtener rápidamente el identificador del primer resultado relevante.
        """
        comando = [
            sys.executable,
            "-m",
            "yt_dlp",
            f"ytsearch1:{consulta}",
            "--flat-playlist",
            "--skip-download",
            "--no-warnings",
            "--quiet",
            "--print",
            "%(id)s",
        ]

        try:
            resultado = subprocess.run(
                comando,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=30,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
        except subprocess.TimeoutExpired as error:
            raise RuntimeError("La búsqueda de YouTube tardó demasiado.") from error

        if resultado.returncode != 0:
            detalle = (resultado.stderr or "").strip()
            if "No module named yt_dlp" in detalle:
                raise RuntimeError(
                    "Falta yt-dlp. Ejecute: python -m pip install -U yt-dlp"
                )
            raise RuntimeError(detalle or "yt-dlp no pudo consultar YouTube.")

        lineas = [linea.strip() for linea in (resultado.stdout or "").splitlines() if linea.strip()]
        if not lineas:
            return None

        video_id = lineas[0]
        if video_id.startswith("http://") or video_id.startswith("https://"):
            url = video_id
        else:
            url = f"https://www.youtube.com/watch?v={video_id}"

        separador = "&" if "?" in url else "?"
        return f"{url}{separador}autoplay=1"

    def abrir_youtube_despues_de_voz(self, url):
        """Evita que Daniela y el video de YouTube hablen al mismo tiempo."""
        def trabajo():
            inicio = time.time()
            vio_habla = False

            # Esperamos a que Piper comience y termine la confirmación. Si por
            # cualquier razón no inicia, no dejamos el video bloqueado para siempre.
            while time.time() - inicio < 12:
                if self.hablando:
                    vio_habla = True
                elif vio_habla:
                    break
                elif time.time() - inicio > 2.5:
                    break
                time.sleep(0.05)

            try:
                self.abrir_url_en_chrome(url)
                print("YOUTUBE: video abierto ->", url)
            except Exception as error:
                print("ERROR ABRIENDO VIDEO YOUTUBE:", error)

        threading.Thread(target=trabajo, daemon=True).start()

    def reproducir_youtube_async(self, consulta):
        consulta = (consulta or "").strip()
        if not consulta:
            self.abrir_youtube_inicio()
            return

        token = self.iniciar_proceso("youtube")
        if token is None:
            self.responder(
                "estoy terminando la operación anterior. Inténtelo nuevamente en unos segundos.",
                "confundida",
            )
            return

        self.cambiar_expresion("pensando")

        def trabajo():
            inicio = time.perf_counter()
            try:
                url = self.obtener_primer_video_youtube(consulta)
                print(f"LATENCIA YOUTUBE: {time.perf_counter() - inicio:.2f} s")
            except Exception as error:
                print("ERROR RESOLVIENDO YOUTUBE:", error)
                self.terminar_proceso(token)

                # Si yt-dlp no está instalado o YouTube cambia su sistema,
                # todavía abrimos los resultados para que la orden no se pierda.
                def respaldo():
                    self.buscar_en_youtube(consulta)
                    messagebox.showinfo(
                        "YouTube",
                        "Beta pudo abrir la búsqueda, pero no seleccionar automáticamente "
                        "el primer video.\n\nSi falta yt-dlp, instálelo con:\n"
                        "python -m pip install -U yt-dlp",
                        parent=self.root,
                    )

                self.root.after(0, respaldo)
                return

            self.terminar_proceso(token)

            if not url:
                self.root.after(
                    0,
                    lambda: self.buscar_en_youtube(consulta),
                )
                return

            consulta_hablada = consulta if len(consulta) <= 70 else consulta[:67] + "..."

            def confirmar_y_abrir():
                # Primero habla Daniela. El navegador se abre cuando termina esa
                # frase para evitar que ambas voces se superpongan.
                self.responder(
                    f"encontré un video relacionado con {consulta_hablada}. Lo reproduciré en YouTube.",
                    "feliz",
                )
                self.abrir_youtube_despues_de_voz(url)

            self.root.after(0, confirmar_y_abrir)

        threading.Thread(target=trabajo, daemon=True).start()

    def extraer_busqueda_web(self, comando):
        """Detecta órdenes de búsqueda visual y devuelve (consulta, imágenes).

        Acepta frases como:
        - abre Google Chrome y busca muebles de madera
        - busca en Google muebles de madera
        - busca muebles de madera en Chrome
        - busca imágenes de Dragon Ball Z
        """
        original = (comando or "").strip()
        if not original:
            return None

        texto = normalizar(original)
        palabras = set(texto.split())
        verbos_busqueda = {"busca", "buscar", "buscame", "encuentra", "buscarme"}
        if not (palabras & verbos_busqueda):
            return None

        if any(frase in texto for frase in [
            "que recuerdas", "que sabes", "buscar recuerdo", "busca recuerdo",
            "buscar memoria", "busca memoria",
        ]):
            return None

        modo_imagenes = any(frase in texto for frase in [
            "busca imagenes", "buscar imagenes", "buscame imagenes",
            "imagenes de", "busca fotos", "buscar fotos", "fotos de",
        ])

        patrones = [
            r"^(?:abre|abrir|inicia)\s+(?:google\s+)?chrome\s+(?:y\s+)?(?:busca|buscar|búscame|buscame|encuentra)\s+(.+)$",
            r"^(?:busca|buscar|búscame|buscame|encuentra)\s+(?:en\s+)?(?:google\s+chrome|google|chrome|internet)\s+(.+)$",
            r"^(?:busca|buscar|búscame|buscame|encuentra)\s+(.+?)\s+(?:en|con)\s+(?:google\s+chrome|google|chrome|internet)$",
            r"^(?:busca|buscar|búscame|buscame|encuentra)\s+(.+)$",
        ]

        consulta = ""
        for patron in patrones:
            coincidencia = re.match(patron, original, flags=re.IGNORECASE)
            if coincidencia:
                consulta = coincidencia.group(1).strip()
                break

        if not consulta:
            # Respaldo tolerante para pequeñas variaciones de Whisper.
            t = texto
            t = re.sub(r"^(?:beta|veta|meta|metas|petra)\s+", "", t).strip()
            t = re.sub(r"^(?:abre|abrir|inicia)\s+(?:google\s+)?chrome\s+(?:y\s+)?", "", t).strip()
            t = re.sub(r"^(?:busca|buscar|buscame|encuentra|buscarme)\s+", "", t).strip()
            t = re.sub(r"^(?:en\s+)?(?:google\s+chrome|google|chrome|internet)\s+", "", t).strip()
            t = re.sub(r"\s+(?:en|con)\s+(?:google\s+chrome|google|chrome|internet)$", "", t).strip()
            consulta = t

        consulta = re.sub(
            r"^(?:algo\s+)?(?:relacionado\s+con|sobre|acerca\s+de|informaci[oó]n\s+(?:sobre|de)|cosas\s+(?:sobre|de))\s+",
            "",
            consulta,
            flags=re.IGNORECASE,
        ).strip()

        # Quitamos puntuación final antes de detectar sufijos como "en Chrome.".
        consulta = consulta.strip(" .,:;-\t\n")
        consulta = re.sub(
            r"\s+(?:en|con)\s+(?:google\s+chrome|google|chrome|internet)$",
            "",
            consulta,
            flags=re.IGNORECASE,
        ).strip()

        if modo_imagenes:
            # Limpia tanto "imágenes de X" como "imágenes en Google de X".
            consulta = re.sub(
                r"^(?:im[aá]genes|fotos)\s+(?:(?:en\s+)?(?:google\s+chrome|google|chrome|internet)\s+)?(?:de|sobre)?\s*",
                "",
                consulta,
                flags=re.IGNORECASE,
            ).strip()

        consulta = consulta.strip(" .,:;-\t\n")
        if len(consulta) < 2:
            return None

        print(f"BÚSQUEDA WEB DETECTADA: {consulta}")
        return consulta, modo_imagenes

    def preparar_contexto_busqueda_visual_async(self, consulta):
        """Guarda contexto web de una búsqueda abierta en Chrome sin bloquear la UI.

        Beta no intenta leer el DOM de Chrome. En paralelo recupera resultados web
        equivalentes con DDGS para poder responder después a frases como
        "explícame lo que encontraste".
        """
        consulta = (consulta or "").strip()
        if not consulta:
            return

        # Registramos de inmediato el tema; así un seguimiento muy rápido ya sabe
        # a qué búsqueda se refiere, aunque DDGS siga trabajando en segundo plano.
        contexto = {
            "consulta": consulta,
            "resultados": [],
            "resumen": "",
            "origen": "busqueda_visual_google",
        }
        self.ultima_investigacion_web = contexto
        self.ultima_investigacion_web_ts = time.time()

        def trabajo():
            try:
                inicio = time.perf_counter()
                resultados = self.buscar_internet_ddgs(consulta)
                print(f"LATENCIA CONTEXTO BÚSQUEDA VISUAL: {time.perf_counter() - inicio:.2f} s")
                if resultados:
                    # Solo reemplazamos si sigue siendo la misma búsqueda activa.
                    if self.ultima_investigacion_web is contexto:
                        contexto["resultados"] = resultados
                        self.ultimas_fuentes_web = resultados
                        self.ultima_investigacion_web_ts = time.time()
                        print(f"CONTEXTO WEB PREPARADO: {consulta} ({len(resultados)} fuentes)")
            except Exception as error:
                print("CONTEXTO WEB VISUAL NO DISPONIBLE:", error)

        threading.Thread(target=trabajo, daemon=True).start()

    def obtener_ruta_chrome(self):
        rutas = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
        ]
        for ruta in rutas:
            if os.path.exists(ruta):
                return ruta
        return None

    def buscar_en_chrome(self, consulta, modo_imagenes=False):
        consulta = (consulta or "").strip()
        if not consulta:
            self.responder("necesito saber qué desea que busque.", "confundida")
            return

        consulta_url = urllib.parse.quote_plus(consulta)
        if modo_imagenes:
            url = f"https://www.google.com/search?tbm=isch&q={consulta_url}"
        else:
            url = f"https://www.google.com/search?q={consulta_url}"

        try:
            chrome = self.obtener_ruta_chrome()
            if chrome:
                subprocess.Popen([chrome, url])
            else:
                os.startfile(url)

            # En paralelo Beta recupera resultados textuales equivalentes para
            # poder conversar después sobre lo buscado. Esto NO bloquea Chrome.
            self.preparar_contexto_busqueda_visual_async(consulta)

            tipo = "imágenes" if modo_imagenes else "resultados"
            consulta_hablada = consulta if len(consulta) <= 85 else consulta[:82] + "..."
            self.responder(
                f"abriendo Google Chrome. Le muestro {tipo} sobre {consulta_hablada}.",
                "feliz",
            )
        except Exception as error:
            print("ERROR ABRIENDO BÚSQUEDA WEB:", error)
            self.responder("no pude abrir la búsqueda en Google.", "molesta")

    def abrir_chrome(self):
        ruta = self.obtener_ruta_chrome()
        if ruta:
            subprocess.Popen([ruta])
            self.responder("abriendo Google Chrome.", "feliz")
            return

        self.responder("no pude encontrar Google Chrome.", "molesta")

    def abrir_inicio(self):
        try:
            ctypes.windll.user32.keybd_event(0x5B, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0x5B, 0, 0x0002, 0)
            self.responder("abriendo el menú Inicio.", "feliz")
        except Exception:
            self.responder("no pude abrir el menú Inicio.", "molesta")

    def crear_carpeta(self, nombre):
        nombre = re.sub(r'[<>:"/\\|?*]', "", (nombre or "")).strip()
        if not nombre:
            self.responder("necesito un nombre válido.", "confundida")
            return

        ruta = obtener_escritorio() / nombre
        if ruta.exists():
            self.responder(f"la carpeta {nombre} ya existe.", "confundida")
            return

        try:
            ruta.mkdir(parents=True)
            self.responder(f"la carpeta {nombre} fue creada.", "feliz")
        except Exception:
            self.responder("no pude crear la carpeta.", "molesta")

    # ======================================================
    # VOZ DE BETA: PIPER / DANIELA + RESPALDO WINDOWS
    # ======================================================

    def cargar_piper_en_memoria(self):
        """Carga Daniela una sola vez. Si falla, la CLI anterior sigue como respaldo."""
        if self.piper_listo or self.piper_cargando:
            return
        self.piper_cargando = True
        inicio = time.perf_counter()
        try:
            if not PIPER_MODELO.exists():
                raise FileNotFoundError(f"No existe {PIPER_MODELO}")
            from piper import PiperVoice
            self.piper_voice = PiperVoice.load(str(PIPER_MODELO), str(PIPER_CONFIG))
            self.piper_listo = True
            self.piper_error = ""
            print(f"PIPER DANIELA CARGADA EN MEMORIA en {time.perf_counter() - inicio:.2f} s")
        except Exception as error:
            self.piper_voice = None
            self.piper_listo = False
            self.piper_error = str(error)
            print("PIPER API: no pude precargar Daniela; usaré la CLI estable:", error)
        finally:
            self.piper_cargando = False

    def reproducir_voz_windows_respaldo(self, texto):
        """Voz anterior de Windows, usada solo si Piper falla."""
        try:
            texto_b64 = base64.b64encode(texto.encode("utf-8")).decode("ascii")

            comando_ps = f"""
Add-Type -AssemblyName System.Speech
$voz = New-Object System.Speech.Synthesis.SpeechSynthesizer
$voz.Rate = 0
$voz.Volume = 100
$es = $voz.GetInstalledVoices() | Where-Object {{ $_.VoiceInfo.Culture.Name -like 'es-*' }} | Select-Object -First 1
if ($es) {{ $voz.SelectVoice($es.VoiceInfo.Name) }}
$bytes = [Convert]::FromBase64String('{texto_b64}')
$texto = [Text.Encoding]::UTF8.GetString($bytes)
$voz.Speak($texto)
"""
            encoded = base64.b64encode(comando_ps.encode("utf-16le")).decode("ascii")
            subprocess.run(
                ["powershell", "-NoProfile", "-EncodedCommand", encoded],
                creationflags=subprocess.CREATE_NO_WINDOW,
                check=False,
            )
            return True
        except Exception as error:
            print("ERROR VOZ WINDOWS:", error)
            return False

    def analizar_wav_para_boca(self, ruta_wav, intervalo_ms=45):
        """
        Convierte la intensidad real del WAV de Daniela en niveles de boca.

        Devuelve una lista de enteros:
            0 = boca casi cerrada
            1 = apertura suave
            2 = apertura media
            3 = apertura amplia

        No intenta adivinar fonemas. Sigue la energía real de la voz, que para
        una mascota de escritorio produce una sincronización mucho más natural
        que abrir/cerrar la boca con un temporizador fijo.
        """
        try:
            niveles_rms = []
            with wave.open(str(ruta_wav), "rb") as wav_file:
                frecuencia = wav_file.getframerate()
                canales = wav_file.getnchannels()
                ancho_muestra = wav_file.getsampwidth()

                # Piper/Daniela genera PCM de 16 bits. Si algún día se cambia el
                # formato, devolvemos una secuencia vacía y usamos la animación
                # de respaldo en vez de arriesgar una lectura incorrecta.
                if ancho_muestra != 2 or frecuencia <= 0:
                    print(
                        "SINCRONIZACIÓN BOCA: formato WAV no compatible; "
                        "usaré animación de respaldo."
                    )
                    return []

                frames_por_bloque = max(
                    1,
                    int(frecuencia * (intervalo_ms / 1000.0)),
                )

                while True:
                    datos = wav_file.readframes(frames_por_bloque)
                    if not datos:
                        break

                    muestras = array("h")
                    muestras.frombytes(datos)
                    if sys.byteorder == "big":
                        muestras.byteswap()

                    if not muestras:
                        niveles_rms.append(0.0)
                        continue

                    # En estéreo basta con considerar todas las muestras: para
                    # la amplitud visual no necesitamos separar canales.
                    suma_cuadrados = 0.0
                    for muestra in muestras:
                        suma_cuadrados += float(muestra) * float(muestra)

                    rms = math.sqrt(suma_cuadrados / len(muestras))
                    niveles_rms.append(rms)

            if not niveles_rms:
                return []

            positivos = sorted(v for v in niveles_rms if v > 0)
            if not positivos:
                return [0] * len(niveles_rms)

            # Referencia robusta: percentil 90. Así un pico aislado no hace que
            # todo el resto de la frase parezca demasiado silencioso.
            indice_90 = min(
                len(positivos) - 1,
                max(0, int(len(positivos) * 0.90)),
            )
            referencia = max(positivos[indice_90], 1.0)

            # Umbral de ruido dinámico + mínimo práctico para Daniela.
            indice_15 = min(
                len(positivos) - 1,
                max(0, int(len(positivos) * 0.15)),
            )
            piso_ruido = max(120.0, positivos[indice_15] * 0.75)

            niveles = []
            for rms in niveles_rms:
                if rms <= piso_ruido:
                    nivel = 0
                else:
                    proporcion = (rms - piso_ruido) / max(
                        1.0,
                        referencia - piso_ruido,
                    )
                    proporcion = max(0.0, min(1.25, proporcion))

                    if proporcion < 0.16:
                        nivel = 1
                    elif proporcion < 0.44:
                        nivel = 2
                    else:
                        nivel = 3

                niveles.append(nivel)

            # Suavizado mínimo: evita parpadeos de 0->3->0 en 90 ms sin borrar
            # las pausas reales entre palabras.
            suavizados = []
            anterior = 0
            for nivel in niveles:
                if nivel == 0:
                    valor = 0
                elif anterior == 0 and nivel == 3:
                    valor = 2
                elif abs(nivel - anterior) > 1:
                    valor = anterior + (1 if nivel > anterior else -1)
                else:
                    valor = nivel
                suavizados.append(valor)
                anterior = valor

            duracion = len(suavizados) * intervalo_ms / 1000.0
            print(
                f"SINCRONIZACIÓN BOCA: {len(suavizados)} cuadros, "
                f"{duracion:.2f} s de audio"
            )
            return suavizados

        except Exception as error:
            print("ERROR ANALIZANDO AUDIO PARA BOCA:", error)
            return []

    def preparar_sincronizacion_boca(self, niveles, intervalo_ms, evento_listo=None):
        """Se ejecuta en el hilo de Tkinter justo antes de iniciar el audio."""
        try:
            self.detener_sincronizacion_boca(redibujar=False)
            self.sincronizacion_boca_activa = bool(niveles)
            self.boca_audio_niveles = list(niveles or [])
            self.boca_audio_indice = 0
            self.boca_audio_intervalo_ms = max(25, int(intervalo_ms))
            self.nivel_boca_habla = (
                self.boca_audio_niveles[0]
                if self.boca_audio_niveles
                else 1
            )

            self.cambiar_expresion("hablando")
            self.redibujar_beta()

            if self.sincronizacion_boca_activa:
                self.boca_audio_job = self.root.after(
                    self.boca_audio_intervalo_ms,
                    self.actualizar_boca_desde_audio,
                )
            else:
                # Respaldo si no pudimos analizar el WAV.
                self.fase_habla = False
                self.root.after(80, self.iniciar_animacion_habla)
        finally:
            if evento_listo is not None:
                evento_listo.set()

    def actualizar_boca_desde_audio(self):
        """Avanza un cuadro de boca siguiendo la amplitud del WAV."""
        self.boca_audio_job = None

        if not self.hablando or not self.sincronizacion_boca_activa:
            return

        self.boca_audio_indice += 1

        if self.boca_audio_indice >= len(self.boca_audio_niveles):
            self.nivel_boca_habla = 0
            self.redibujar_beta()
            return

        self.nivel_boca_habla = self.boca_audio_niveles[self.boca_audio_indice]
        self.redibujar_beta()

        try:
            self.boca_audio_job = self.root.after(
                self.boca_audio_intervalo_ms,
                self.actualizar_boca_desde_audio,
            )
        except tk.TclError:
            self.boca_audio_job = None

    def detener_sincronizacion_boca(self, redibujar=True):
        """Detiene la animación y deja la boca cerrada al terminar Daniela."""
        if self.boca_audio_job is not None:
            try:
                self.root.after_cancel(self.boca_audio_job)
            except Exception:
                pass
            self.boca_audio_job = None

        self.sincronizacion_boca_activa = False
        self.boca_audio_niveles = []
        self.boca_audio_indice = 0
        self.nivel_boca_habla = 0
        self.fase_habla = False

        if redibujar:
            try:
                self.redibujar_beta()
            except Exception:
                pass

    def reproducir_voz_daniela(self, texto):
        """
        Genera el WAV de Daniela, analiza su amplitud y SOLO entonces inicia
        boca + audio. Esto elimina el desfase donde Beta movía la boca mientras
        Piper todavía estaba generando la frase.
        """
        if not PIPER_MODELO.exists():
            print("PIPER: no encuentro el modelo:", PIPER_MODELO)
            return False

        ruta_wav = None
        try:
            fd, nombre_wav = tempfile.mkstemp(prefix="beta_daniela_", suffix=".wav")
            os.close(fd)
            ruta_wav = Path(nombre_wav)

            # -------- Ruta rápida: modelo persistente --------
            if self.piper_listo and self.piper_voice is not None:
                inicio = time.perf_counter()
                try:
                    with self.piper_lock:
                        with wave.open(str(ruta_wav), "wb") as wav_file:
                            self.piper_voice.synthesize_wav(texto, wav_file)
                    print(f"LATENCIA PIPER (memoria): {time.perf_counter() - inicio:.2f} s")
                except Exception as error_api:
                    print("PIPER API falló; usando CLI estable:", error_api)
                    self.piper_listo = False
                    self.piper_voice = None
                    try:
                        ruta_wav.unlink(missing_ok=True)
                    except Exception:
                        pass
                    fd, nombre_wav = tempfile.mkstemp(prefix="beta_daniela_", suffix=".wav")
                    os.close(fd)
                    ruta_wav = Path(nombre_wav)

            # -------- Respaldo: CLI estable --------
            if not self.piper_listo or self.piper_voice is None:
                inicio = time.perf_counter()
                comando = [
                    sys.executable, "-m", "piper",
                    "-m", str(PIPER_MODELO),
                    "-f", str(ruta_wav),
                    "--", texto,
                ]
                resultado = subprocess.run(
                    comando,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    check=False,
                )
                print(f"LATENCIA PIPER (CLI): {time.perf_counter() - inicio:.2f} s")
                if resultado.returncode != 0:
                    print("ERROR PIPER (código", resultado.returncode, "):")
                    if resultado.stderr.strip():
                        print(resultado.stderr.strip())
                    return False

            if not ruta_wav.exists() or ruta_wav.stat().st_size < 100:
                print("ERROR PIPER: no se generó un WAV válido.")
                return False

            # Analizamos el WAV ANTES de mover la boca.
            intervalo_ms = 45
            niveles = self.analizar_wav_para_boca(ruta_wav, intervalo_ms)

            # Coordinación entre el hilo de voz y Tkinter: preparamos la primera
            # posición de la boca y, cuando está dibujada, arrancamos el audio.
            evento_visual_listo = threading.Event()
            try:
                self.root.after(
                    0,
                    lambda: self.preparar_sincronizacion_boca(
                        niveles,
                        intervalo_ms,
                        evento_visual_listo,
                    ),
                )
                evento_visual_listo.wait(timeout=0.40)
            except Exception:
                pass

            winsound.PlaySound(None, winsound.SND_PURGE)
            winsound.PlaySound(str(ruta_wav), winsound.SND_FILENAME)

            try:
                self.root.after(0, self.detener_sincronizacion_boca)
            except Exception:
                pass

            return True

        except Exception as error:
            print("ERROR VOZ DANIELA:", error)
            try:
                self.root.after(0, self.detener_sincronizacion_boca)
            except Exception:
                pass
            return False
        finally:
            if ruta_wav is not None:
                try:
                    ruta_wav.unlink(missing_ok=True)
                except Exception:
                    pass

    def preparar_texto_para_voz(self, texto):
        """Convierte una respuesta escrita en texto natural para Daniela.

        Qwen puede devolver Markdown (**, #, viñetas, `código`, etc.).
        Esos símbolos son útiles en pantalla, pero Piper puede pronunciarlos
        literalmente. Aquí conservamos el contenido y eliminamos solamente
        marcas de formato antes de sintetizar la voz.
        """
        texto = (texto or "").strip()
        if not texto:
            return ""

        # Enlaces Markdown: [texto](url) -> texto.
        texto = re.sub(r"\[([^\]]+)\]\((?:https?://)?[^)]+\)", r"\1", texto)

        # URLs sueltas no aportan a una explicación oral y pueden sonar muy mal.
        texto = re.sub(r"https?://\S+", "", texto)

        # En respuestas de programación, el código completo queda visible en
        # terminal. Daniela no debe leer símbolos, sangrías y operadores como si
        # fueran una frase natural.
        if "```" in texto:
            texto = re.sub(
                r"```(?:[A-Za-z0-9_+.#-]+)?\s*.*?```",
                " Le dejé el ejemplo de código en pantalla. ",
                texto,
                flags=re.DOTALL,
            )
        texto = texto.replace("```", "")
        texto = texto.replace("`", "")

        # Encabezados Markdown y citas.
        texto = re.sub(r"(?m)^\s{0,3}#{1,6}\s*", "", texto)
        texto = re.sub(r"(?m)^\s*>+\s*", "", texto)

        # Viñetas: las convertimos en pausas naturales, no en símbolos leídos.
        texto = re.sub(r"(?m)^\s*[-+*•▪◦]\s+", "", texto)

        # Separadores horizontales de Markdown.
        texto = re.sub(r"(?m)^\s*[-*_]{3,}\s*$", "", texto)

        # Énfasis Markdown. El contenido permanece.
        texto = texto.replace("**", "")
        texto = texto.replace("__", "")
        texto = texto.replace("~~", "")
        texto = texto.replace("*", "")

        # Guiones bajos usados como énfasis, pero respetamos palabras técnicas.
        texto = re.sub(r"(?<!\w)_(?=\S)|(?<=\S)_(?!\w)", "", texto)

        # Caracteres estructurales que Piper puede verbalizar.
        texto = texto.translate(str.maketrans({
            "[": "", "]": "", "{": "", "}": "",
            "|": ", ", "<": "", ">": "",
        }))

        # Emojis y símbolos pictográficos: se omiten en la voz.
        texto = re.sub(
            "["
            "\U0001F300-\U0001FAFF"
            "\U00002700-\U000027BF"
            "\U00002600-\U000026FF"
            "]+",
            "",
            texto,
        )

        # Si Qwen creó una lista numerada, usamos conectores más conversacionales.
        conectores = {
            "1": "Primero, ",
            "2": "Segundo, ",
            "3": "Tercero, ",
            "4": "Cuarto, ",
            "5": "Quinto, ",
            "6": "Sexto, ",
            "7": "Séptimo, ",
            "8": "Octavo, ",
            "9": "Noveno, ",
            "10": "Décimo, ",
        }
        lineas_limpias = []
        for linea in texto.splitlines():
            linea = linea.strip()
            if not linea:
                continue
            m = re.match(r"^(\d{1,2})[.)]\s+(.*)$", linea)
            if m and m.group(1) in conectores:
                linea = conectores[m.group(1)] + m.group(2)
            lineas_limpias.append(linea)

        # Los saltos de línea se transforman en pausas naturales.
        texto = ". ".join(lineas_limpias)

        # Evitar dobles signos provocados por la conversión de líneas.
        texto = re.sub(r"\.\s*[.;:]", ".", texto)
        texto = re.sub(r"\s+([,.;:?!])", r"\1", texto)
        texto = re.sub(r"([,;:]){2,}", r"\1", texto)
        texto = re.sub(r"\.{2,}", ".", texto)
        texto = re.sub(r"\s{2,}", " ", texto)

        return texto.strip()

    def hablar(self, texto, respuesta_id, expresion_final):
        # Guardamos y mostramos la respuesta original, pero Daniela recibe una
        # versión oral sin Markdown ni símbolos de formato.
        texto_voz = self.preparar_texto_para_voz(texto)
        if not texto_voz:
            texto_voz = texto

        self.hablando = True

        def reproducir():
            try:
                print("VOZ: intentando Piper / Daniela High...")
                funciono = self.reproducir_voz_daniela(texto_voz)

                if funciono:
                    print("VOZ: Daniela High OK")
                else:
                    print("VOZ: Piper falló. Usando respaldo de Windows.")
                    # Para la voz de Windows no tenemos un WAV de Daniela que
                    # analizar, así que usamos la animación antigua como respaldo.
                    try:
                        self.root.after(
                            0,
                            lambda: self.preparar_sincronizacion_boca([], 90),
                        )
                    except Exception:
                        pass
                    self.reproducir_voz_windows_respaldo(texto_voz)
                    try:
                        self.root.after(0, self.detener_sincronizacion_boca)
                    except Exception:
                        pass

            except Exception as error:
                print("ERROR VOZ:", error)
                try:
                    self.root.after(
                        0,
                        lambda: self.preparar_sincronizacion_boca([], 90),
                    )
                except Exception:
                    pass
                self.reproducir_voz_windows_respaldo(texto_voz)
                try:
                    self.root.after(0, self.detener_sincronizacion_boca)
                except Exception:
                    pass

            finally:
                try:
                    while not self.audio_queue.empty():
                        self.audio_queue.get_nowait()
                except Exception:
                    pass

                self.hablando = False

                try:
                    self.root.after(
                        0,
                        lambda: self.finalizar_respuesta(
                            respuesta_id,
                            expresion_final,
                        ),
                    )
                except tk.TclError:
                    pass

        threading.Thread(target=reproducir, daemon=True).start()

    def iniciar_animacion_habla(self):
        """Animación de respaldo cuando no existe un WAV analizable."""
        if not self.hablando or self.sincronizacion_boca_activa:
            return

        self.fase_habla = not self.fase_habla
        self.nivel_boca_habla = 2 if self.fase_habla else 1
        self.redibujar_beta()

        try:
            self.root.after(140, self.iniciar_animacion_habla)
        except tk.TclError:
            pass

    def responder(self, texto, expresion="hablando", tipo_contexto="general"):
        texto = (texto or "").strip()
        if not texto:
            return

        # El prompt ya suele incluir "Señor", pero esta protección evita respuestas
        # sin tratamiento incluso si el modelo lo omite.
        texto_normalizado_inicio = normalizar(texto)

        # Los saludos de inicio ya incluyen el tratamiento "Señor" después
        # de "Buenos días / Buenas tardes / Buenas noches". Evitamos
        # duplicarlo como "Señor, buenos días, Señor...".
        prefijos_con_tratamiento = (
            "senor",
            "buenos dias senor",
            "buenas tardes senor",
            "buenas noches senor",
        )
        if not any(texto_normalizado_inicio.startswith(p) for p in prefijos_con_tratamiento):
            # Si el modelo ya incluyó "Señor" en las primeras palabras (por ejemplo
            # "¡Qué gusto, Señor!"), no lo duplicamos como "Señor, ¡Qué gusto, Señor!".
            primeras = " ".join(texto_normalizado_inicio.split()[:6])
            if "senor" not in primeras:
                texto = "Señor, " + texto[0].lower() + texto[1:] if len(texto) > 1 else "Señor, " + texto

        if self.ultima_frase_inicio:
            print(f"LATENCIA HASTA TEXTO FINAL: {time.perf_counter() - self.ultima_frase_inicio:.2f} s")
            self.ultima_frase_inicio = 0.0
        print("RESPUESTA FINAL DE BETA:", texto)

        self.memoria.guardar_conversacion("Beta", texto)
        self.ultima_respuesta_beta = texto
        self.actualizar_contexto_turno("Beta", texto)
        self.programar_memoria_inteligente(self.ultimo_mensaje_usuario, texto)

        # En modo estricto, ni siquiera una pregunta de Beta abre escucha libre.
        # Solo el modo conversación explícito conserva continuidad sin wake word.
        if "?" in texto and self.modo_escucha == "conversacion":
            self.renovar_modo_conversacion()

        self.respuesta_actual_id += 1
        respuesta_id = self.respuesta_actual_id
        self.respuesta_tipo_por_id[respuesta_id] = tipo_contexto or "general"

        # No ponemos la expresión "hablando" todavía: Piper debe generar el
        # WAV primero. La boca pasa a "hablando" justo cuando el audio está
        # listo para reproducirse, evitando que se mueva antes que Daniela.
        if expresion == "hablando":
            self.cambiar_expresion("pensando")
        else:
            self.cambiar_expresion(expresion)

        self.hablar(texto, respuesta_id, expresion)

    def finalizar_respuesta(self, respuesta_id, expresion_final):
        if respuesta_id != self.respuesta_actual_id:
            self.respuesta_tipo_por_id.pop(respuesta_id, None)
            return

        # MUY IMPORTANTE: la ventana de conversación comienza al TERMINAR la voz,
        # no cuando el Señor hizo la pregunta. Antes una respuesta académica podía
        # tardar 15-25 s en generarse + 20 s en hablarse y consumir por completo
        # una ventana de 30 s. Por eso una frase como "¿cuáles son las tres partes?"
        # se reconocía pero quedaba ignorada.
        tipo_contexto = self.respuesta_tipo_por_id.pop(respuesta_id, "general")
        self.ultimo_tipo_respuesta_terminada = tipo_contexto or "general"

        # En el arranque, el micrófono se habilita DESPUÉS de que Daniela termina
        # el informe de hora y clima. Esto evita que Vosk/Whisper capturen la voz
        # de la propia Beta durante el saludo.
        if tipo_contexto == "curiosidad" and self.pregunta_curiosa_pendiente:
            self.pregunta_curiosa_hasta = time.time() + CURIOSIDAD_RESPUESTA_SEGUNDOS
            print(
                f"CURIOSIDAD: esperando respuesta autorizada durante "
                f"{CURIOSIDAD_RESPUESTA_SEGUNDOS} s después de la voz."
            )

        if tipo_contexto == "inicio":
            self.informe_inicio_en_curso = False
            if not self.escuchando:
                try:
                    self.root.after(350, self.iniciar_escucha_si_necesario)
                except tk.TclError:
                    pass

        if self.ultimo_mensaje_usuario:
            if self.modo_escucha == "conversacion":
                self.renovar_modo_conversacion()
                print(
                    f"MODO CONVERSACIÓN: ventana renovada por "
                    f"{TIEMPO_MODO_CONVERSACION_SILENCIO} s después de la voz."
                )
            elif self.modo_escucha == "estricto":
                # No se abre ninguna ventana automática. La siguiente orden
                # deberá comenzar nuevamente por "Beta".
                self.modo_conversacion_hasta = 0.0
                print("MODO ESTRICTO: se requiere 'Beta' para la siguiente orden.")
            else:
                self.modo_conversacion_hasta = 0.0

        if expresion_final not in {"hablando", "escuchando"}:
            self.cambiar_expresion(expresion_final)
            self.root.after(
                700,
                lambda: self.volver_escucha_si_corresponde(respuesta_id),
            )
        else:
            self.volver_escucha_si_corresponde(respuesta_id)

    def volver_escucha_si_corresponde(self, respuesta_id):
        if respuesta_id != self.respuesta_actual_id:
            return

        if self.escuchando:
            self.expresion_escuchando()
        else:
            self.expresion_normal()

    # ======================================================
    # DIBUJO DE BETA
    # ======================================================

    def redibujar_beta(self, event=None):
        ancho = self.canvas.winfo_width()
        alto = self.canvas.winfo_height()

        if ancho < 50 or alto < 50:
            return

        cx = ancho / 2
        cy = alto / 2
        radio = min(ancho, alto) * 0.455

        if self.expresion_actual == "pensando":
            color_centro = "#0886B7"
        elif self.expresion_actual == "molesta":
            color_centro = "#087CB1"
        elif self.expresion_actual == "sorprendida":
            color_centro = "#12A4CC"
        elif self.expresion_actual == "escuchando":
            color_centro = "#08A1CB"
        else:
            color_centro = COLOR_CUERPO

        self.canvas.coords(
            self.cuerpo_sombra,
            cx - radio,
            cy - radio,
            cx + radio,
            cy + radio,
        )

        radio_borde = radio * 0.965
        self.canvas.coords(
            self.cuerpo_borde,
            cx - radio_borde,
            cy - radio_borde,
            cx + radio_borde,
            cy + radio_borde,
        )

        radio_cuerpo = radio * 0.91
        self.canvas.coords(
            self.cuerpo,
            cx - radio_cuerpo,
            cy - radio_cuerpo,
            cx + radio_cuerpo,
            cy + radio_cuerpo,
        )
        self.canvas.itemconfig(self.cuerpo, fill=color_centro)

        radio_claro = radio * 0.79
        luz_x = cx - radio * 0.055
        luz_y = cy - radio * 0.065
        self.canvas.coords(
            self.cuerpo_claro,
            luz_x - radio_claro,
            luz_y - radio_claro,
            luz_x + radio_claro,
            luz_y + radio_claro,
        )

        self.canvas.coords(
            self.reflejo_grande,
            cx - radio * 0.57,
            cy - radio * 0.72,
            cx + radio * 0.07,
            cy - radio * 0.38,
        )
        self.canvas.coords(
            self.reflejo_medio,
            cx - radio * 0.47,
            cy - radio * 0.66,
            cx - radio * 0.05,
            cy - radio * 0.46,
        )
        self.canvas.coords(
            self.reflejo_pequeno,
            cx - radio * 0.36,
            cy - radio * 0.63,
            cx - radio * 0.24,
            cy - radio * 0.55,
        )
        self.canvas.coords(
            self.reflejo_inferior,
            cx - radio * 0.24,
            cy + radio * 0.46,
            cx,
            cy + radio * 0.52,
            cx + radio * 0.23,
            cy + radio * 0.43,
        )
        self.canvas.itemconfig(
            self.reflejo_inferior,
            width=max(2, int(radio * 0.035)),
        )

        self.dibujar_ojos(cx, cy, radio)
        self.dibujar_cejas(cx, cy, radio)
        self.dibujar_boca(cx, cy, radio)

    def dibujar_ojos(self, cx, cy, radio):
        separacion = radio * 0.285
        ancho_ojo = radio * 0.19
        alto_ojo = radio * 0.255
        y_ojo = cy - radio * 0.17

        if self.expresion_actual == "feliz":
            alto_ojo = radio * 0.19
        elif self.expresion_actual == "impaciente":
            alto_ojo = radio * 0.17
        elif self.expresion_actual == "molesta":
            alto_ojo = radio * 0.18
        elif self.expresion_actual == "sorprendida":
            ancho_ojo = radio * 0.205
            alto_ojo = radio * 0.29
        elif self.expresion_actual == "escuchando":
            alto_ojo = radio * 0.27

        ojo_izq_x = cx - separacion
        ojo_der_x = cx + separacion

        if self.ojos_cerrados:
            grosor = max(3, int(radio * 0.04))

            self.canvas.coords(self.sombra_ojo_izquierdo, 0, 0, 0, 0)
            self.canvas.coords(self.sombra_ojo_derecho, 0, 0, 0, 0)

            self.canvas.coords(
                self.ojo_izquierdo,
                ojo_izq_x - ancho_ojo,
                y_ojo,
                ojo_izq_x + ancho_ojo,
                y_ojo + grosor,
            )
            self.canvas.coords(
                self.ojo_derecho,
                ojo_der_x - ancho_ojo,
                y_ojo,
                ojo_der_x + ancho_ojo,
                y_ojo + grosor,
            )

            self.ocultar_pupilas()
            return

        self.mostrar_pupilas()

        sombra_x = radio * 0.035
        sombra_y = radio * 0.035

        self.canvas.coords(
            self.sombra_ojo_izquierdo,
            ojo_izq_x - ancho_ojo - sombra_x,
            y_ojo - alto_ojo - sombra_y,
            ojo_izq_x + ancho_ojo + sombra_x,
            y_ojo + alto_ojo + sombra_y,
        )
        self.canvas.coords(
            self.sombra_ojo_derecho,
            ojo_der_x - ancho_ojo - sombra_x,
            y_ojo - alto_ojo - sombra_y,
            ojo_der_x + ancho_ojo + sombra_x,
            y_ojo + alto_ojo + sombra_y,
        )

        self.canvas.coords(
            self.ojo_izquierdo,
            ojo_izq_x - ancho_ojo,
            y_ojo - alto_ojo,
            ojo_izq_x + ancho_ojo,
            y_ojo + alto_ojo,
        )

        if self.expresion_actual == "confundida":
            self.canvas.coords(
                self.ojo_derecho,
                ojo_der_x - ancho_ojo * 0.84,
                y_ojo - alto_ojo * 0.79,
                ojo_der_x + ancho_ojo * 0.84,
                y_ojo + alto_ojo * 0.79,
            )
        else:
            self.canvas.coords(
                self.ojo_derecho,
                ojo_der_x - ancho_ojo,
                y_ojo - alto_ojo,
                ojo_der_x + ancho_ojo,
                y_ojo + alto_ojo,
            )

        self.centro_ojo_izquierdo = (ojo_izq_x, y_ojo)
        self.centro_ojo_derecho = (ojo_der_x, y_ojo)

        menor_dimension = min(ancho_ojo, alto_ojo)
        self.radio_iris = menor_dimension * 0.66
        self.radio_pupila = self.radio_iris * 0.72
        self.radio_movimiento_pupila = menor_dimension * 0.30
        self.radio_brillo_pupila = max(2, self.radio_pupila * 0.24)

    def ocultar_pupilas(self):
        for item in [
            self.iris_izquierda,
            self.iris_derecha,
            self.pupila_izquierda,
            self.pupila_derecha,
            self.brillo_pupila_izq,
            self.brillo_pupila_der,
            self.brillo_pupila_izq_2,
            self.brillo_pupila_der_2,
        ]:
            self.canvas.itemconfigure(item, state="hidden")

    def mostrar_pupilas(self):
        for item in [
            self.iris_izquierda,
            self.iris_derecha,
            self.pupila_izquierda,
            self.pupila_derecha,
            self.brillo_pupila_izq,
            self.brillo_pupila_der,
            self.brillo_pupila_izq_2,
            self.brillo_pupila_der_2,
        ]:
            self.canvas.itemconfigure(item, state="normal")

    def dibujar_cejas(self, cx, cy, radio):
        separacion = radio * 0.285
        largo = radio * 0.16
        y = cy - radio * 0.51
        izq_x = cx - separacion
        der_x = cx + separacion
        grosor = max(2, int(radio * 0.035))

        self.canvas.itemconfig(self.ceja_izquierda, width=grosor)
        self.canvas.itemconfig(self.ceja_derecha, width=grosor)

        expresion = self.expresion_actual

        if expresion in {"normal", "escuchando", "feliz", "hablando"}:
            self.canvas.itemconfigure(self.ceja_izquierda, state="hidden")
            self.canvas.itemconfigure(self.ceja_derecha, state="hidden")
            return

        self.canvas.itemconfigure(self.ceja_izquierda, state="normal")
        self.canvas.itemconfigure(self.ceja_derecha, state="normal")

        if expresion == "confundida":
            izq = (izq_x - largo, y + radio * 0.04, izq_x + largo, y - radio * 0.07)
            der = (der_x - largo, y - radio * 0.07, der_x + largo, y - radio * 0.07)
        elif expresion == "impaciente":
            izq = (izq_x - largo, y, izq_x + largo, y + radio * 0.04)
            der = (der_x - largo, y + radio * 0.04, der_x + largo, y)
        elif expresion == "molesta":
            izq = (izq_x - largo, y - radio * 0.07, izq_x + largo, y + radio * 0.07)
            der = (der_x - largo, y + radio * 0.07, der_x + largo, y - radio * 0.07)
        elif expresion == "sorprendida":
            izq = (izq_x - largo, y - radio * 0.09, izq_x + largo, y - radio * 0.09)
            der = (der_x - largo, y - radio * 0.09, der_x + largo, y - radio * 0.09)
        elif expresion == "pensando":
            izq = (izq_x - largo, y, izq_x + largo, y - radio * 0.03)
            der = (der_x - largo, y - radio * 0.05, der_x + largo, y)
        else:
            izq = (izq_x - largo, y, izq_x + largo, y)
            der = (der_x - largo, y, der_x + largo, y)

        self.canvas.coords(self.ceja_izquierda, *izq)
        self.canvas.coords(self.ceja_derecha, *der)

    def dibujar_boca(self, cx, cy, radio):
        expresion = self.expresion_actual
        y = cy + radio * 0.30
        ancho = radio * 0.30
        grosor = max(3, int(radio * 0.045))

        self.canvas.itemconfig(self.boca, width=grosor)
        self.canvas.itemconfig(
            self.boca_brillo,
            width=max(2, int(radio * 0.028)),
        )

        self.canvas.itemconfigure(self.boca_abierta, state="hidden")
        self.canvas.itemconfigure(self.boca_interior, state="hidden")
        self.canvas.itemconfigure(self.boca, state="normal")
        self.canvas.itemconfigure(self.boca_brillo, state="normal")

        if expresion == "normal":
            coords = (
                cx - ancho,
                y - radio * 0.04,
                cx - ancho * 0.45,
                y + radio * 0.035,
                cx,
                y + radio * 0.07,
                cx + ancho * 0.48,
                y + radio * 0.02,
                cx + ancho,
                y - radio * 0.12,
            )
            brillo = (
                cx - ancho * 0.58,
                y + radio * 0.055,
                cx,
                y + radio * 0.12,
                cx + ancho * 0.48,
                y + radio * 0.06,
            )

        elif expresion == "escuchando":
            coords = (
                cx - ancho * 0.75,
                y,
                cx,
                y + radio * 0.055,
                cx + ancho * 0.75,
                y - radio * 0.035,
            )
            brillo = (
                cx - ancho * 0.40,
                y + radio * 0.06,
                cx,
                y + radio * 0.09,
                cx + ancho * 0.36,
                y + radio * 0.05,
            )

        elif expresion == "feliz":
            coords = (
                cx - ancho,
                y - radio * 0.10,
                cx - ancho * 0.55,
                y + radio * 0.04,
                cx,
                y + radio * 0.12,
                cx + ancho * 0.55,
                y + radio * 0.04,
                cx + ancho,
                y - radio * 0.10,
            )
            brillo = (
                cx - ancho * 0.58,
                y + radio * 0.08,
                cx,
                y + radio * 0.16,
                cx + ancho * 0.58,
                y + radio * 0.08,
            )

        elif expresion == "pensando":
            coords = (cx - ancho * 0.36, y, cx + ancho * 0.22, y - radio * 0.02)
            brillo = coords

        elif expresion == "confundida":
            coords = (
                cx - ancho * 0.70,
                y + radio * 0.04,
                cx - ancho * 0.15,
                y - radio * 0.035,
                cx + ancho * 0.30,
                y + radio * 0.035,
                cx + ancho * 0.70,
                y,
            )
            brillo = (
                cx - ancho * 0.28,
                y + radio * 0.06,
                cx + ancho * 0.18,
                y + radio * 0.08,
            )

        elif expresion == "impaciente":
            coords = (cx - ancho * 0.58, y + radio * 0.02, cx + ancho * 0.20, y + radio * 0.02)
            brillo = coords

        elif expresion == "molesta":
            coords = (
                cx - ancho * 0.80,
                y + radio * 0.09,
                cx,
                y - radio * 0.035,
                cx + ancho * 0.80,
                y + radio * 0.09,
            )
            brillo = (
                cx - ancho * 0.40,
                y + radio * 0.08,
                cx,
                y + radio * 0.02,
                cx + ancho * 0.40,
                y + radio * 0.08,
            )

        elif expresion == "hablando":
            # La apertura ya no depende de un parpadeo fijo. Cuando Daniela
            # habla, nivel_boca_habla sigue la amplitud real del WAV.
            nivel = max(0, min(3, int(self.nivel_boca_habla)))

            if nivel == 0:
                # Pausa o silencio: boca pequeña, casi cerrada.
                self.canvas.itemconfigure(self.boca_abierta, state="hidden")
                self.canvas.itemconfigure(self.boca_interior, state="hidden")
                self.canvas.itemconfigure(self.boca, state="normal")
                self.canvas.itemconfigure(self.boca_brillo, state="normal")

                coords = (
                    cx - ancho * 0.50,
                    y + radio * 0.01,
                    cx,
                    y + radio * 0.025,
                    cx + ancho * 0.50,
                    y + radio * 0.005,
                )
                brillo = (
                    cx - ancho * 0.24,
                    y + radio * 0.035,
                    cx + ancho * 0.22,
                    y + radio * 0.030,
                )
                self.canvas.coords(self.boca, *coords)
                self.canvas.coords(self.boca_brillo, *brillo)
                return

            self.canvas.itemconfigure(self.boca, state="hidden")
            self.canvas.itemconfigure(self.boca_brillo, state="hidden")
            self.canvas.itemconfigure(self.boca_abierta, state="normal")
            self.canvas.itemconfigure(self.boca_interior, state="normal")

            if nivel == 1:
                boca_ancho = radio * 0.075
                boca_alto = radio * 0.055
            elif nivel == 2:
                boca_ancho = radio * 0.095
                boca_alto = radio * 0.100
            else:
                boca_ancho = radio * 0.115
                boca_alto = radio * 0.155

            self.canvas.coords(
                self.boca_abierta,
                cx - boca_ancho,
                y - boca_alto,
                cx + boca_ancho,
                y + boca_alto,
            )

            # El interior/"labio" inferior también crece con la apertura.
            interior_factor = 0.32 if nivel == 1 else (0.40 if nivel == 2 else 0.46)
            self.canvas.coords(
                self.boca_interior,
                cx - boca_ancho * interior_factor,
                y + boca_alto * 0.18,
                cx + boca_ancho * interior_factor,
                y + boca_alto * 0.72,
            )
            return

        elif expresion == "sorprendida":
            self.canvas.itemconfigure(self.boca, state="hidden")
            self.canvas.itemconfigure(self.boca_brillo, state="hidden")
            self.canvas.itemconfigure(self.boca_abierta, state="normal")
            self.canvas.itemconfigure(self.boca_interior, state="hidden")

            boca_ancho = radio * 0.10
            boca_alto = radio * 0.14
            self.canvas.coords(
                self.boca_abierta,
                cx - boca_ancho,
                y - boca_alto,
                cx + boca_ancho,
                y + boca_alto,
            )
            return

        else:
            coords = (cx - ancho, y, cx + ancho, y)
            brillo = coords

        self.canvas.coords(self.boca, *coords)
        self.canvas.coords(self.boca_brillo, *brillo)

    # ======================================================
    # PUPILAS SIGUEN CURSOR
    # ======================================================

    def actualizar_pupilas(self):
        if not self.ojos_cerrados:
            try:
                mouse_x = self.root.winfo_pointerx() - self.canvas.winfo_rootx()
                mouse_y = self.root.winfo_pointery() - self.canvas.winfo_rooty()

                if self.expresion_actual == "impaciente":
                    mouse_x = 0
                    mouse_y = self.canvas.winfo_height() / 2
                elif self.expresion_actual == "pensando":
                    mouse_x = self.canvas.winfo_width() * 0.85
                    mouse_y = self.canvas.winfo_height() * 0.08

                self.mover_pupila(
                    "izquierda",
                    self.centro_ojo_izquierdo,
                    mouse_x,
                    mouse_y,
                )
                self.mover_pupila(
                    "derecha",
                    self.centro_ojo_derecho,
                    mouse_x,
                    mouse_y,
                )

            except Exception:
                pass

        try:
            self.root.after(33, self.actualizar_pupilas)
        except tk.TclError:
            pass

    def mover_pupila(self, lado, centro_ojo, mouse_x, mouse_y):
        ojo_x, ojo_y = centro_ojo
        if ojo_x == 0 and ojo_y == 0:
            return

        dx = mouse_x - ojo_x
        dy = mouse_y - ojo_y
        distancia = math.sqrt(dx * dx + dy * dy)

        if distancia == 0:
            offset_x = 0
            offset_y = 0
        else:
            escala = min(self.radio_movimiento_pupila / distancia, 1)
            offset_x = dx * escala
            offset_y = dy * escala

        nuevo_x = ojo_x + offset_x
        nuevo_y = ojo_y + offset_y

        if lado == "izquierda":
            iris = self.iris_izquierda
            pupila = self.pupila_izquierda
            brillo_1 = self.brillo_pupila_izq
            brillo_2 = self.brillo_pupila_izq_2
        else:
            iris = self.iris_derecha
            pupila = self.pupila_derecha
            brillo_1 = self.brillo_pupila_der
            brillo_2 = self.brillo_pupila_der_2

        r_iris = self.radio_iris
        self.canvas.coords(
            iris,
            nuevo_x - r_iris,
            nuevo_y - r_iris,
            nuevo_x + r_iris,
            nuevo_y + r_iris,
        )

        r_pupila = self.radio_pupila
        self.canvas.coords(
            pupila,
            nuevo_x - r_pupila,
            nuevo_y - r_pupila,
            nuevo_x + r_pupila,
            nuevo_y + r_pupila,
        )

        r_brillo = self.radio_brillo_pupila
        brillo_x = nuevo_x - r_pupila * 0.40
        brillo_y = nuevo_y - r_pupila * 0.42
        self.canvas.coords(
            brillo_1,
            brillo_x - r_brillo,
            brillo_y - r_brillo,
            brillo_x + r_brillo,
            brillo_y + r_brillo,
        )

        r_brillo_2 = max(1, r_brillo * 0.42)
        brillo2_x = nuevo_x + r_pupila * 0.27
        brillo2_y = nuevo_y + r_pupila * 0.25
        self.canvas.coords(
            brillo_2,
            brillo2_x - r_brillo_2,
            brillo2_y - r_brillo_2,
            brillo2_x + r_brillo_2,
            brillo2_y + r_brillo_2,
        )

    # ======================================================
    # EXPRESIONES / PARPADEO
    # ======================================================

    def cambiar_expresion(self, expresion):
        self.expresion_actual = expresion
        self.redibujar_beta()

    def expresion_normal(self):
        self.cambiar_expresion("normal")

    def expresion_escuchando(self):
        self.cambiar_expresion("escuchando")

    def expresion_pensando(self):
        self.cambiar_expresion("pensando")

    def expresion_hablando(self):
        self.cambiar_expresion("hablando")

    def expresion_feliz(self):
        self.cambiar_expresion("feliz")

    def expresion_confundida(self):
        self.cambiar_expresion("confundida")

    def expresion_impaciente(self):
        self.cambiar_expresion("impaciente")

    def expresion_molesta(self):
        self.cambiar_expresion("molesta")

    def expresion_sorprendida(self):
        self.cambiar_expresion("sorprendida")

    def parpadear(self):
        if self.expresion_actual not in {"hablando", "sorprendida"}:
            self.ojos_cerrados = True
            self.redibujar_beta()
            self.root.after(130, self.abrir_ojos)

        try:
            self.root.after(random.randint(3000, 6500), self.parpadear)
        except tk.TclError:
            pass

    def abrir_ojos(self):
        self.ojos_cerrados = False
        self.redibujar_beta()

    # ======================================================
    # CERRAR
    # ======================================================

    def cerrar_beta(self):
        self.escuchando = False
        try:
            self.memoria.cambiar_estado("tamano_beta", self.tamano_beta)
            self.guardar_posicion()
        except Exception:
            pass
        self.root.destroy()


# ==========================================================
# EJECUTAR
# ==========================================================

if __name__ == "__main__":
    print("=" * 62)
    print(f"BETA PORTABLE - RUTA BASE: {BASE_DIR}")
    print(f"BASE DE DATOS: {BASE_DATOS}")
    print(f"BIBLIOTECA: {BIBLIOTECA_DIR}")
    print(f"RESPALDOS: {RESPALDOS_DIR}")
    print(f"MODELO WHISPER: {CARPETA_WHISPER}")
    print(f"MODELO DE VOZ: {PIPER_MODELO}")
    print("Las rutas propias de Beta siguen automáticamente a beta.py.")
    print("=" * 62)
    ventana = tk.Tk()
    beta = BetaApp(ventana)
    ventana.mainloop()
