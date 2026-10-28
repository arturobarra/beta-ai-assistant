import json
import sys

import beta_agenda_local_v375 as agenda

def responder(obj):
    print(json.dumps(obj, ensure_ascii=False))

def main():
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
        accion = str(payload.get("accion") or "crear").strip().lower()

        if accion == "ping":
            db = agenda.inicializar()
            responder({"ok": True, "servicio": "beta_agenda_local_v375", "db": str(db)})
            return

        if accion == "crear":
            evento = agenda.crear_evento(payload)
            responder({
                "ok": True,
                "sincronizado": False,
                "local_id": evento["id"],
                "evento": evento,
            })
            return

        if accion == "listar":
            responder({"ok": True, "eventos": agenda.listar_eventos()})
            return

        if accion == "eliminar":
            local_id = payload.get("id")
            if local_id is None:
                raise ValueError("Falta id para eliminar.")
            eliminado = agenda.eliminar_evento(local_id)
            responder({"ok": eliminado, "eliminado": eliminado, "id": int(local_id)})
            return

        raise ValueError(f"Acción no soportada: {accion}")

    except Exception as exc:
        responder({"ok": False, "error": str(exc), "tipo": type(exc).__name__})

if __name__ == "__main__":
    main()
