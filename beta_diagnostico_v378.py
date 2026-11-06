# -*- coding: utf-8 -*-
"""
Beta v3.7.8 - Diagnostico seguro de servicios RC1

Principios:
- Solo lectura.
- No refresca tokens.
- No abre navegadores.
- No inicia autorizaciones OAuth.
- No escribe eventos ni bases de datos.
- No reproduce Spotify.
- No llama a APIs autenticadas.
"""

from pathlib import Path
from collections import Counter
import importlib.util
import socket
import time


BASE_DIR = Path(__file__).resolve().parent
DIAGNOSTICO_VERSION = "v3.7.8 RC1"

OK = "OK"
AVISO = "AVISO"
ERROR = "ERROR"
NO_CONFIGURADO = "NO CONFIGURADO"


def resultado(servicio, estado, detalle):
    return {
        "servicio": str(servicio),
        "estado": str(estado),
        "detalle": str(detalle),
    }


def modulo_disponible(nombre):
    try:
        return importlib.util.find_spec(nombre) is not None
    except Exception:
        return False


def diagnosticar_nucleo():
    requeridos = [
        "beta.py",
        "beta_apariencia.json",
        "beta_agenda_local_v375.py",
        "beta_agenda_servicio_v375.py",
        "beta_agenda_visual_v375.py",
        "beta_chatgpt_oauth_rc1.py",
        "beta_google_multicuenta_v375.py",
    ]

    faltan = [
        nombre
        for nombre in requeridos
        if not (BASE_DIR / nombre).exists()
    ]

    if faltan:
        return resultado(
            "Nucleo Beta",
            ERROR,
            "Faltan archivos esenciales: " + ", ".join(faltan),
        )

    return resultado(
        "Nucleo Beta",
        OK,
        "Archivos esenciales presentes.",
    )


def diagnosticar_dependencias_voz():
    faltan = []

    for modulo in ("sounddevice", "vosk"):
        if not modulo_disponible(modulo):
            faltan.append(modulo)

    if faltan:
        return resultado(
            "Voz base / Vosk",
            ERROR,
            "Faltan dependencias: " + ", ".join(faltan),
        )

    return resultado(
        "Voz base / Vosk",
        OK,
        "Vosk y sounddevice estan instalados.",
    )


def diagnosticar_microfono():
    if not modulo_disponible("sounddevice"):
        return resultado(
            "Microfono",
            ERROR,
            "sounddevice no esta instalado.",
        )

    try:
        import sounddevice as sd

        dispositivo = sd.query_devices(kind="input")
        nombre = str(dispositivo.get("name") or "sin nombre")
        canales = int(dispositivo.get("max_input_channels") or 0)
        frecuencia = dispositivo.get("default_samplerate")

        if canales < 1:
            return resultado(
                "Microfono",
                ERROR,
                "Windows no informa canales de entrada disponibles.",
            )

        frecuencia_txt = ""
        if frecuencia:
            frecuencia_txt = f", {int(float(frecuencia))} Hz"

        return resultado(
            "Microfono",
            OK,
            f"Entrada disponible: {nombre} ({canales} canal(es){frecuencia_txt}).",
        )

    except Exception as exc:
        return resultado(
            "Microfono",
            ERROR,
            f"No pude consultar el dispositivo de entrada: {exc}",
        )


def diagnosticar_whisper(app=None):
    if app is not None:
        listo = bool(getattr(app, "whisper_listo", False))
        cargando = bool(getattr(app, "whisper_cargando", False))
        error = str(getattr(app, "whisper_error", "") or "").strip()
        modelo = getattr(app, "modelo_whisper", None)

        if listo and modelo is not None:
            return resultado(
                "Whisper",
                OK,
                "Modelo cargado y disponible en Beta.",
            )

        if cargando:
            return resultado(
                "Whisper",
                AVISO,
                "El modelo se esta cargando.",
            )

        if error:
            return resultado(
                "Whisper",
                ERROR,
                f"Beta registro un error de Whisper: {error}",
            )

    if not modulo_disponible("faster_whisper"):
        return resultado(
            "Whisper",
            ERROR,
            "La dependencia faster-whisper no esta instalada.",
        )

    archivo_modelo = (
        BASE_DIR
        / "modelo-whisper-small"
        / "model.bin"
    )

    if not archivo_modelo.exists():
        return resultado(
            "Whisper",
            AVISO,
            "faster-whisper esta instalado, pero no encontre model.bin.",
        )

    return resultado(
        "Whisper",
        OK,
        "Modelo local presente. La carga en memoria se comprobara dentro de Beta.",
    )


def diagnosticar_chatgpt():
    try:
        import beta_chatgpt_oauth_rc1 as chatgpt_oauth

        estado = chatgpt_oauth.estado()
        perfil_id = str(
            estado.get("perfil_activo") or ""
        ).strip()

        if not perfil_id:
            return resultado(
                "ChatGPT",
                NO_CONFIGURADO,
                "No hay un perfil activo.",
            )

        perfiles = estado.get("perfiles") or {}
        meta = perfiles.get(perfil_id) or {}

        if not meta.get("conectado"):
            return resultado(
                "ChatGPT",
                AVISO,
                "Existe un perfil activo, pero esta marcado como desconectado.",
            )

        if not meta.get("plan_habilitado"):
            return resultado(
                "ChatGPT",
                AVISO,
                "La cuenta esta registrada, pero el uso del plan no figura habilitado.",
            )

        return resultado(
            "ChatGPT",
            OK,
            "Perfil activo configurado. El diagnostico no refresco ni valido el token remotamente.",
        )

    except Exception as exc:
        return resultado(
            "ChatGPT",
            ERROR,
            f"No pude leer el estado local de ChatGPT: {exc}",
        )


def diagnosticar_spotify(app=None):
    if app is None:
        return resultado(
            "Spotify",
            NO_CONFIGURADO,
            "La comprobacion completa requiere Beta en ejecucion. No se tocaron tokens.",
        )

    access_token = str(
        getattr(app, "spotify_access_token", "") or ""
    ).strip()

    refresh_token = str(
        getattr(app, "spotify_refresh_token", "") or ""
    ).strip()

    try:
        expira = float(
            getattr(app, "spotify_token_expira", 0) or 0
        )
    except Exception:
        expira = 0

    ahora = time.time()

    if access_token and expira > ahora + 20:
        segundos = max(0, int(expira - ahora))

        return resultado(
            "Spotify",
            OK,
            f"Token de acceso presente y vigente localmente por aproximadamente {segundos} s.",
        )

    if refresh_token:
        return resultado(
            "Spotify",
            AVISO,
            "Hay token de renovacion, pero el token de acceso esta vencido o proximo a vencer. No fue renovado.",
        )

    if access_token:
        return resultado(
            "Spotify",
            AVISO,
            "Hay token de acceso, pero no pude confirmar una vigencia util.",
        )

    return resultado(
        "Spotify",
        NO_CONFIGURADO,
        "No detecto tokens de Spotify en la instancia actual.",
    )


def diagnosticar_internet():
    destino = ("www.google.com", 443)

    inicio = time.perf_counter()

    try:
        with socket.create_connection(
            destino,
            timeout=2.5,
        ):
            pass

        ms = (
            time.perf_counter() - inicio
        ) * 1000.0

        return resultado(
            "Internet",
            OK,
            f"Conexion TCP disponible. Prueba aproximada: {ms:.0f} ms.",
        )

    except Exception as exc:
        return resultado(
            "Internet",
            AVISO,
            f"No pude confirmar salida a Internet: {exc}",
        )


def diagnosticar_agenda_local():
    archivos = [
        "beta_agenda_local_v375.py",
        "beta_agenda_servicio_v375.py",
        "beta_agenda_visual_v375.py",
        "beta_google_calendar_escritura_fix9.py",
    ]

    faltan = [
        nombre
        for nombre in archivos
        if not (BASE_DIR / nombre).exists()
    ]

    if faltan:
        return resultado(
            "Agenda local",
            ERROR,
            "Faltan componentes: " + ", ".join(faltan),
        )

    return resultado(
        "Agenda local",
        OK,
        "Componentes presentes. No se abrio ni modifico la base de eventos.",
    )


def diagnosticar_google():
    try:
        import beta_google_multicuenta_v375 as multi

        estado = multi.estado_beta_asistente() or {}

        cuenta = str(
            estado.get("cuenta") or ""
        ).strip()

        token_presente = False

        ruta_token = getattr(
            multi,
            "ruta_token_beta_asistente",
            None,
        )

        if callable(ruta_token):
            try:
                token_presente = bool(
                    ruta_token().exists()
                )
            except Exception:
                token_presente = False

        if cuenta or token_presente:
            return resultado(
                "Google / Agenda Beta",
                AVISO,
                "Configuracion local detectada. La conexion remota no se comprobo porque Agenda/OAuth esta congelado en esta rama.",
            )

        return resultado(
            "Google / Agenda Beta",
            NO_CONFIGURADO,
            "No detecto configuracion local de la cuenta Beta Asistente.",
        )

    except Exception as exc:
        return resultado(
            "Google / Agenda Beta",
            AVISO,
            f"No pude leer el estado local de Google: {exc}",
        )


def diagnosticar_sistema():
    if not modulo_disponible("psutil"):
        return resultado(
            "Sistema Atlas",
            AVISO,
            "psutil no esta instalado.",
        )

    try:
        import psutil

        ram = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=0.15)

        return resultado(
            "Sistema Atlas",
            OK,
            f"CPU {cpu:.0f}%, RAM {ram.percent:.0f}% en uso.",
        )

    except Exception as exc:
        return resultado(
            "Sistema Atlas",
            AVISO,
            f"No pude leer recursos del sistema: {exc}",
        )


def ejecutar_diagnostico(app=None):
    resultados = [
        diagnosticar_nucleo(),
        diagnosticar_dependencias_voz(),
        diagnosticar_microfono(),
        diagnosticar_whisper(app),
        diagnosticar_chatgpt(),
        diagnosticar_spotify(app),
        diagnosticar_internet(),
        diagnosticar_agenda_local(),
        diagnosticar_google(),
        diagnosticar_sistema(),
    ]

    conteo = Counter(
        item["estado"]
        for item in resultados
    )

    if conteo.get(ERROR, 0):
        estado_general = ERROR
    elif conteo.get(AVISO, 0):
        estado_general = AVISO
    elif conteo.get(NO_CONFIGURADO, 0):
        estado_general = AVISO
    else:
        estado_general = OK

    return {
        "version": DIAGNOSTICO_VERSION,
        "estado_general": estado_general,
        "resultados": resultados,
        "conteo": dict(conteo),
    }


def imprimir_informe(informe):
    print("=" * 78)
    print(
        "BETA - DIAGNOSTICO GENERAL "
        + informe["version"]
    )
    print("=" * 78)

    for item in informe["resultados"]:
        print(
            f"[{item['estado']}] "
            f"{item['servicio']}: "
            f"{item['detalle']}"
        )

    print("-" * 78)

    conteo = informe["conteo"]

    print(
        "RESULTADO GENERAL:",
        informe["estado_general"],
    )

    print(
        "OK:",
        conteo.get(OK, 0),
        "| AVISOS:",
        conteo.get(AVISO, 0),
        "| ERRORES:",
        conteo.get(ERROR, 0),
        "| NO CONFIGURADOS:",
        conteo.get(NO_CONFIGURADO, 0),
    )

    print("=" * 78)


if __name__ == "__main__":
    informe = ejecutar_diagnostico()
    imprimir_informe(informe)
