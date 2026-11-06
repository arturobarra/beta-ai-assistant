# -*- coding: utf-8 -*-
"""
Beta v3.7.8 - Recuperacion segura de servicios RC1

IMPORTANTE:
- Este modulo NO reemplaza al diagnostico.
- Solo ejecuta acciones incluidas explicitamente en una lista blanca.
- No renueva Spotify.
- No refresca ChatGPT.
- No modifica Google/OAuth.
- No reinicia el microfono.
- No instala dependencias.
- No descarga modelos.
"""

from pathlib import Path
import importlib.util


BASE_DIR = Path(__file__).resolve().parent
MODELO_WHISPER_LOCAL = (
    BASE_DIR
    / "modelo-whisper-small"
    / "model.bin"
)

RECUPERADO = "RECUPERADO"
SIN_CAMBIOS = "SIN CAMBIOS"
EN_PROCESO = "EN PROCESO"
REQUIERE_INTERVENCION = "REQUIERE INTERVENCION"


def resultado(servicio, estado, detalle, accion=""):
    return {
        "servicio": str(servicio),
        "estado": str(estado),
        "detalle": str(detalle),
        "accion": str(accion),
    }


def plan_recuperacion_whisper(app):
    listo = bool(
        getattr(app, "whisper_listo", False)
    )
    cargando = bool(
        getattr(app, "whisper_cargando", False)
    )
    modelo = getattr(
        app,
        "modelo_whisper",
        None,
    )

    if listo and modelo is not None:
        return resultado(
            "Whisper",
            SIN_CAMBIOS,
            "Whisper ya esta cargado y operativo.",
        )

    if cargando:
        return resultado(
            "Whisper",
            EN_PROCESO,
            "Whisper ya se esta cargando. No se iniciara una segunda carga.",
        )

    if not MODELO_WHISPER_LOCAL.exists():
        return resultado(
            "Whisper",
            REQUIERE_INTERVENCION,
            "No encontre model.bin local. La recuperacion segura no descargara modelos.",
        )

    try:
        disponible = (
            importlib.util.find_spec(
                "faster_whisper"
            )
            is not None
        )
    except Exception:
        disponible = False

    if not disponible:
        return resultado(
            "Whisper",
            REQUIERE_INTERVENCION,
            "Falta faster-whisper. La recuperacion segura no instalara dependencias.",
        )

    return resultado(
        "Whisper",
        "LISTO PARA RECUPERAR",
        "El modelo y la dependencia existen localmente.",
        accion="cargar_whisper_local",
    )


def recuperar_whisper(app):
    plan = plan_recuperacion_whisper(app)

    if plan.get("accion") != "cargar_whisper_local":
        return plan

    try:
        app.cargar_modelo_whisper()
    except Exception as exc:
        return resultado(
            "Whisper",
            REQUIERE_INTERVENCION,
            "El reintento local produjo un error: "
            + str(exc),
        )

    listo = bool(
        getattr(app, "whisper_listo", False)
    )
    modelo = getattr(
        app,
        "modelo_whisper",
        None,
    )

    if listo and modelo is not None:
        return resultado(
            "Whisper",
            RECUPERADO,
            "Whisper volvio a quedar cargado y operativo.",
        )

    if bool(
        getattr(app, "whisper_cargando", False)
    ):
        return resultado(
            "Whisper",
            EN_PROCESO,
            "Whisper continua cargandose.",
        )

    error = str(
        getattr(app, "whisper_error", "")
        or ""
    ).strip()

    detalle = (
        "Whisper no quedo operativo despues del reintento."
    )

    if error:
        detalle += " Detalle: " + error

    return resultado(
        "Whisper",
        REQUIERE_INTERVENCION,
        detalle,
    )


def ejecutar_recuperacion_segura(app):
    resultados = [
        recuperar_whisper(app),
    ]

    return {
        "resultados": resultados,
        "recuperados": sum(
            1
            for item in resultados
            if item.get("estado") == RECUPERADO
        ),
        "bloqueados_por_seguridad": [
            "Microfono / Vosk",
            "Spotify",
            "ChatGPT",
            "Google / OAuth",
        ],
    }


def imprimir_informe(informe):
    print("=" * 78)
    print(
        "BETA - RECUPERACION SEGURA "
        "v3.7.8 RC1"
    )
    print("=" * 78)

    for item in informe.get(
        "resultados",
        [],
    ):
        print(
            f"[{item['estado']}] "
            f"{item['servicio']}: "
            f"{item['detalle']}"
        )

    print(
        "SERVICIOS NO MODIFICADOS POR SEGURIDAD: "
        + ", ".join(
            informe.get(
                "bloqueados_por_seguridad",
                [],
            )
        )
    )

    print("=" * 78)
