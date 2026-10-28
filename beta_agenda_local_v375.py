from pathlib import Path
from datetime import datetime
import os
import sqlite3

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DB = BASE_DIR / "beta_agenda_v375.db"

def ruta_db():
    override = (os.environ.get("BETA_AGENDA_DB_PATH") or "").strip()
    return Path(override) if override else DEFAULT_DB

def conectar():
    db = ruta_db()
    db.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(db), timeout=15)
    con.row_factory = sqlite3.Row
    return con

def inicializar():
    with conectar() as con:
        con.execute(
            "CREATE TABLE IF NOT EXISTS agenda_eventos ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "titulo TEXT NOT NULL,"
            "fecha TEXT NOT NULL,"
            "hora TEXT NOT NULL,"
            "lugar TEXT NOT NULL DEFAULT '',"
            "notas TEXT NOT NULL DEFAULT '',"
            "recordatorio_minutos INTEGER NOT NULL DEFAULT 0,"
            "creado_en TEXT NOT NULL,"
            "google_event_id TEXT NOT NULL DEFAULT '',"
            "google_calendar_id TEXT NOT NULL DEFAULT '',"
            "google_html_link TEXT NOT NULL DEFAULT '',"
            "google_sync_state TEXT NOT NULL DEFAULT 'local',"
            "google_sync_error TEXT NOT NULL DEFAULT '',"
            "google_sync_actualizado_en TEXT NOT NULL DEFAULT '')"
        )
        columnas = {
            row["name"]
            for row in con.execute("PRAGMA table_info(agenda_eventos)").fetchall()
        }
        migraciones = [
            ("google_event_id", "TEXT NOT NULL DEFAULT ''"),
            ("google_calendar_id", "TEXT NOT NULL DEFAULT ''"),
            ("google_html_link", "TEXT NOT NULL DEFAULT ''"),
            ("google_sync_state", "TEXT NOT NULL DEFAULT 'local'"),
            ("google_sync_error", "TEXT NOT NULL DEFAULT ''"),
            ("google_sync_actualizado_en", "TEXT NOT NULL DEFAULT ''"),
        ]
        for nombre, definicion in migraciones:
            if nombre not in columnas:
                con.execute(
                    f"ALTER TABLE agenda_eventos ADD COLUMN {nombre} {definicion}"
                )
        con.execute(
            "CREATE INDEX IF NOT EXISTS idx_agenda_fecha_hora "
            "ON agenda_eventos(fecha, hora, id)"
        )
        con.execute(
            "CREATE INDEX IF NOT EXISTS idx_agenda_google_event_id "
            "ON agenda_eventos(google_event_id)"
        )
        con.commit()
    return ruta_db()

def _validar_payload(payload):
    titulo = str((payload or {}).get("titulo") or "").strip()
    fecha = str((payload or {}).get("fecha") or "").strip()
    hora = str((payload or {}).get("hora") or "").strip()
    lugar = str((payload or {}).get("lugar") or "").strip()
    notas = str((payload or {}).get("notas") or "").strip()

    if not titulo:
        raise ValueError("Falta el título del evento.")
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
    except Exception as exc:
        raise ValueError("Fecha inválida; use YYYY-MM-DD.") from exc
    try:
        datetime.strptime(hora, "%H:%M")
    except Exception as exc:
        raise ValueError("Hora inválida; use HH:MM.") from exc

    try:
        recordatorio = int((payload or {}).get("recordatorio_minutos") or 0)
    except Exception as exc:
        raise ValueError("recordatorio_minutos inválido.") from exc
    if recordatorio < 0:
        raise ValueError("recordatorio_minutos no puede ser negativo.")

    return {
        "titulo": titulo,
        "fecha": fecha,
        "hora": hora,
        "lugar": lugar,
        "notas": notas,
        "recordatorio_minutos": recordatorio,
    }

def crear_evento(payload):
    datos = _validar_payload(payload)
    inicializar()
    creado_en = datetime.now().astimezone().isoformat(timespec="seconds")
    with conectar() as con:
        cur = con.execute(
            "INSERT INTO agenda_eventos "
            "(titulo, fecha, hora, lugar, notas, recordatorio_minutos, creado_en) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                datos["titulo"], datos["fecha"], datos["hora"], datos["lugar"],
                datos["notas"], datos["recordatorio_minutos"], creado_en,
            ),
        )
        con.commit()
        local_id = int(cur.lastrowid)
    return {"id": local_id, **datos, "creado_en": creado_en}

def listar_eventos():
    inicializar()
    with conectar() as con:
        rows = con.execute(
            "SELECT id, titulo, fecha, hora, lugar, notas, "
            "recordatorio_minutos, creado_en, "
            "google_event_id, google_calendar_id, google_html_link, "
            "google_sync_state, google_sync_error, google_sync_actualizado_en "
            "FROM agenda_eventos "
            "ORDER BY fecha ASC, hora ASC, id ASC"
        ).fetchall()
    return [dict(row) for row in rows]

def obtener_evento(local_id):
    inicializar()
    with conectar() as con:
        row = con.execute(
            "SELECT id, titulo, fecha, hora, lugar, notas, "
            "recordatorio_minutos, creado_en, "
            "google_event_id, google_calendar_id, google_html_link, "
            "google_sync_state, google_sync_error, google_sync_actualizado_en "
            "FROM agenda_eventos WHERE id = ?",
            (int(local_id),),
        ).fetchone()
    return dict(row) if row else None

def actualizar_evento(local_id, payload):
    datos = _validar_payload(payload)
    inicializar()
    with conectar() as con:
        cur = con.execute(
            "UPDATE agenda_eventos SET "
            "titulo = ?, fecha = ?, hora = ?, lugar = ?, notas = ?, "
            "recordatorio_minutos = ? "
            "WHERE id = ?",
            (
                datos["titulo"],
                datos["fecha"],
                datos["hora"],
                datos["lugar"],
                datos["notas"],
                datos["recordatorio_minutos"],
                int(local_id),
            ),
        )
        con.commit()
        return cur.rowcount == 1

def vincular_google(local_id, resultado):
    resultado = resultado or {}
    google_event_id = str(resultado.get("google_event_id") or "").strip()
    google_calendar_id = str(resultado.get("google_calendar_id") or "").strip()
    google_html_link = str(resultado.get("html_link") or "").strip()
    if not google_event_id:
        raise ValueError("Falta google_event_id para vincular el evento local.")

    actualizado_en = datetime.now().astimezone().isoformat(timespec="seconds")
    inicializar()
    with conectar() as con:
        cur = con.execute(
            "UPDATE agenda_eventos SET "
            "google_event_id = ?, google_calendar_id = ?, google_html_link = ?, "
            "google_sync_state = 'sincronizado', google_sync_error = '', "
            "google_sync_actualizado_en = ? "
            "WHERE id = ?",
            (
                google_event_id,
                google_calendar_id,
                google_html_link,
                actualizado_en,
                int(local_id),
            ),
        )
        con.commit()
        return cur.rowcount == 1

def marcar_sync_error(local_id, error):
    actualizado_en = datetime.now().astimezone().isoformat(timespec="seconds")
    inicializar()
    with conectar() as con:
        cur = con.execute(
            "UPDATE agenda_eventos SET "
            "google_sync_state = 'error', google_sync_error = ?, "
            "google_sync_actualizado_en = ? "
            "WHERE id = ?",
            (str(error or "")[:1000], actualizado_en, int(local_id)),
        )
        con.commit()
        return cur.rowcount == 1

def eliminar_evento(local_id):
    inicializar()
    with conectar() as con:
        cur = con.execute(
            "DELETE FROM agenda_eventos WHERE id = ?",
            (int(local_id),),
        )
        con.commit()
        return cur.rowcount == 1
