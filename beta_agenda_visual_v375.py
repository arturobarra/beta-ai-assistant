import calendar
from datetime import date, datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

import beta_agenda_local_v375 as agenda
import beta_google_calendar_escritura_fix9 as calendar_write

BASE_DIR = Path(__file__).resolve().parent
AGENDA_ICON_ICO = BASE_DIR / "assets" / "agenda" / "cara_agendando.ico"
AGENDA_ICON_PNG = BASE_DIR / "assets" / "agenda" / "cara_agendando.png"

MESES = [
    "",
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]
DIAS = ["Lu", "Ma", "Mi", "Ju", "Vi", "Sa", "Do"]


class AgendaBetaCalendario(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Agenda Beta")
        self.geometry("1080x700")
        self.minsize(940, 620)

        # Identidad visual propia de Agenda Beta.
        try:
            if AGENDA_ICON_ICO.exists():
                self.iconbitmap(default=str(AGENDA_ICON_ICO))
        except Exception as exc:
            print("AGENDA BETA v3.7.5: no pude aplicar iconbitmap:", exc)

        self.logo_agenda = None

        agenda.inicializar()

        hoy = date.today()
        self.anio = hoy.year
        self.mes = hoy.month
        self.fecha_seleccionada = hoy.isoformat()
        self.evento_seleccionado_id = None

        self._crear_ui()
        self.refrescar()

    def _crear_ui(self):
        raiz = ttk.Frame(self, padding=10)
        raiz.pack(fill="both", expand=True)

        # Cabecera
        cab = ttk.Frame(raiz)
        cab.pack(fill="x", pady=(0, 8))

        ttk.Button(cab, text="< Mes", command=self.mes_anterior).pack(side="left")
        ttk.Button(cab, text="Hoy", command=self.ir_hoy).pack(side="left", padx=(6, 0))
        ttk.Button(cab, text="Mes >", command=self.mes_siguiente).pack(side="left", padx=(6, 0))

        self.lbl_mes = ttk.Label(cab, text="", font=("Segoe UI", 16, "bold"))
        self.lbl_mes.pack(side="left", padx=(18, 0))

        # Logo de Beta Agenda: siempre visible arriba a la derecha.
        marca = ttk.Frame(cab)
        marca.pack(side="right")

        ttk.Label(
            marca,
            text="Agenda local propia de Beta v3.7.5",
        ).pack(side="left", padx=(0, 10))

        try:
            if AGENDA_ICON_PNG.exists():
                self.logo_agenda = tk.PhotoImage(file=str(AGENDA_ICON_PNG))
                ttk.Label(
                    marca,
                    image=self.logo_agenda,
                ).pack(side="right")
        except Exception as exc:
            print("AGENDA BETA v3.7.5: no pude mostrar logo de Agenda:", exc)

        # Zona principal
        principal = ttk.Panedwindow(raiz, orient="horizontal")
        principal.pack(fill="both", expand=True)

        marco_cal = ttk.LabelFrame(principal, text="Calendario mensual", padding=8)
        marco_dia = ttk.LabelFrame(principal, text="Eventos del día", padding=8)
        principal.add(marco_cal, weight=2)
        principal.add(marco_dia, weight=3)

        # Encabezados de días
        cab_dias = ttk.Frame(marco_cal)
        cab_dias.pack(fill="x")
        for col, nombre in enumerate(DIAS):
            ttk.Label(cab_dias, text=nombre, anchor="center").grid(
                row=0, column=col, sticky="nsew", padx=1, pady=(0, 2)
            )
            cab_dias.grid_columnconfigure(col, weight=1)

        self.marco_dias = ttk.Frame(marco_cal)
        self.marco_dias.pack(fill="both", expand=True)
        for col in range(7):
            self.marco_dias.grid_columnconfigure(col, weight=1)
        for fila in range(6):
            self.marco_dias.grid_rowconfigure(fila, weight=1)

        # Eventos del día
        self.lbl_fecha = ttk.Label(marco_dia, text="", font=("Segoe UI", 12, "bold"))
        self.lbl_fecha.pack(anchor="w", pady=(0, 6))

        self.tabla_dia = ttk.Treeview(
            marco_dia,
            columns=("hora", "evento", "lugar"),
            show="headings",
            selectmode="browse",
            height=12,
        )
        self.tabla_dia.heading("hora", text="Hora")
        self.tabla_dia.heading("evento", text="Evento")
        self.tabla_dia.heading("lugar", text="Lugar")
        self.tabla_dia.column("hora", width=70, anchor="center", stretch=False)
        self.tabla_dia.column("evento", width=320, anchor="w")
        self.tabla_dia.column("lugar", width=180, anchor="w")
        self.tabla_dia.pack(fill="both", expand=True)
        self.tabla_dia.bind("<<TreeviewSelect>>", self._seleccionar_evento)

        # Próximos compromisos
        prox = ttk.LabelFrame(raiz, text="Próximos compromisos", padding=8)
        prox.pack(fill="x", pady=(10, 8))

        self.tabla_prox = ttk.Treeview(
            prox,
            columns=("fecha", "hora", "evento"),
            show="headings",
            selectmode="browse",
            height=5,
        )
        self.tabla_prox.heading("fecha", text="Fecha")
        self.tabla_prox.heading("hora", text="Hora")
        self.tabla_prox.heading("evento", text="Compromiso")
        self.tabla_prox.column("fecha", width=110, anchor="center", stretch=False)
        self.tabla_prox.column("hora", width=80, anchor="center", stretch=False)
        self.tabla_prox.column("evento", width=700, anchor="w")
        self.tabla_prox.pack(fill="x")
        self.tabla_prox.bind("<<TreeviewSelect>>", self._seleccionar_proximo)

        # Detalle
        detalle = ttk.LabelFrame(raiz, text="Crear / editar evento local", padding=8)
        detalle.pack(fill="x")

        ttk.Label(detalle, text="Título").grid(row=0, column=0, sticky="w")
        self.var_titulo = tk.StringVar()
        ttk.Entry(detalle, textvariable=self.var_titulo).grid(
            row=0, column=1, columnspan=5, sticky="ew", padx=(6, 0)
        )

        ttk.Label(detalle, text="Fecha").grid(row=1, column=0, sticky="w", pady=(6, 0))
        self.var_fecha = tk.StringVar(value=self.fecha_seleccionada)
        ttk.Entry(detalle, textvariable=self.var_fecha, width=14).grid(
            row=1, column=1, sticky="w", padx=(6, 12), pady=(6, 0)
        )

        ttk.Label(detalle, text="Hora").grid(row=1, column=2, sticky="w", pady=(6, 0))
        self.var_hora = tk.StringVar(value="09:00")
        ttk.Entry(detalle, textvariable=self.var_hora, width=10).grid(
            row=1, column=3, sticky="w", padx=(6, 12), pady=(6, 0)
        )

        ttk.Label(detalle, text="Aviso").grid(row=1, column=4, sticky="w", pady=(6, 0))
        self.var_aviso = tk.StringVar(value="24 horas antes")
        self.combo_aviso = ttk.Combobox(
            detalle,
            textvariable=self.var_aviso,
            state="readonly",
            values=(
                "Sin aviso",
                "15 minutos antes",
                "30 minutos antes",
                "1 hora antes",
                "24 horas antes",
            ),
            width=20,
        )
        self.combo_aviso.grid(
            row=1, column=5, sticky="w", padx=(6, 0), pady=(6, 0)
        )

        ttk.Label(detalle, text="Lugar").grid(row=2, column=0, sticky="w", pady=(6, 0))
        self.var_lugar = tk.StringVar()
        ttk.Entry(detalle, textvariable=self.var_lugar).grid(
            row=2, column=1, columnspan=5, sticky="ew", padx=(6, 0), pady=(6, 0)
        )

        ttk.Label(detalle, text="Notas").grid(row=3, column=0, sticky="nw", pady=(6, 0))
        self.txt_notas = tk.Text(detalle, height=3, wrap="word")
        self.txt_notas.grid(
            row=3, column=1, columnspan=5, sticky="ew", padx=(6, 0), pady=(6, 0)
        )

        botones = ttk.Frame(detalle)
        botones.grid(row=4, column=1, columnspan=5, sticky="w", pady=(8, 0))

        ttk.Button(botones, text="Nuevo", command=self.nuevo_evento).pack(side="left")
        ttk.Button(
            botones, text="Guardar local", command=self.guardar_evento
        ).pack(side="left", padx=(6, 0))
        ttk.Button(
            botones, text="Eliminar local", command=self.eliminar_evento
        ).pack(side="left", padx=(6, 0))
        ttk.Button(botones, text="Actualizar", command=self.refrescar).pack(
            side="left", padx=(6, 0)
        )
        ttk.Button(botones, text="Cerrar", command=self.destroy).pack(
            side="left", padx=(6, 0)
        )

        self.lbl_estado = ttk.Label(detalle, text="")
        self.lbl_estado.grid(row=4, column=5, sticky="e", pady=(8, 0))

        for col in range(6):
            detalle.grid_columnconfigure(col, weight=1 if col in (1, 5) else 0)

    def eventos(self):
        return agenda.listar_eventos()

    def refrescar(self):
        self._dibujar_calendario()
        self._cargar_eventos_dia()
        self._cargar_proximos()
        self.lbl_estado.configure(text=f"{len(self.eventos())} evento(s) local(es)")

    def _dibujar_calendario(self):
        for widget in self.marco_dias.winfo_children():
            widget.destroy()

        self.lbl_mes.configure(text=f"{MESES[self.mes]} {self.anio}")

        eventos_por_fecha = {}
        for ev in self.eventos():
            eventos_por_fecha[ev["fecha"]] = eventos_por_fecha.get(ev["fecha"], 0) + 1

        semanas = calendar.monthcalendar(self.anio, self.mes)
        while len(semanas) < 6:
            semanas.append([0] * 7)

        hoy = date.today().isoformat()

        for fila, semana in enumerate(semanas):
            for col, dia in enumerate(semana):
                if dia == 0:
                    ttk.Label(self.marco_dias, text="").grid(
                        row=fila, column=col, sticky="nsew", padx=1, pady=1
                    )
                    continue

                fecha = f"{self.anio:04d}-{self.mes:02d}-{dia:02d}"
                cantidad = eventos_por_fecha.get(fecha, 0)
                texto = str(dia)
                if cantidad:
                    texto += f"\n• {cantidad}"

                boton = tk.Button(
                    self.marco_dias,
                    text=texto,
                    justify="center",
                    relief="sunken" if fecha == self.fecha_seleccionada else "raised",
                    command=lambda f=fecha: self.seleccionar_fecha(f),
                )
                if fecha == hoy:
                    boton.configure(font=("Segoe UI", 9, "bold"))

                boton.grid(row=fila, column=col, sticky="nsew", padx=1, pady=1)

    def seleccionar_fecha(self, fecha):
        self.fecha_seleccionada = fecha
        self.evento_seleccionado_id = None
        self._limpiar_detalle()
        self._dibujar_calendario()
        self._cargar_eventos_dia()

    def _cargar_eventos_dia(self):
        for item in self.tabla_dia.get_children():
            self.tabla_dia.delete(item)

        try:
            dt = datetime.strptime(self.fecha_seleccionada, "%Y-%m-%d")
            self.lbl_fecha.configure(
                text=f"{dt.day} de {MESES[dt.month].lower()} de {dt.year}"
            )
        except Exception:
            self.lbl_fecha.configure(text=self.fecha_seleccionada)

        for ev in self.eventos():
            if ev["fecha"] == self.fecha_seleccionada:
                self.tabla_dia.insert(
                    "",
                    "end",
                    iid=str(ev["id"]),
                    values=(ev["hora"], ev["titulo"], ev["lugar"]),
                )

    def _cargar_proximos(self):
        for item in self.tabla_prox.get_children():
            self.tabla_prox.delete(item)

        ahora = datetime.now()
        futuros = []

        for ev in self.eventos():
            try:
                cuando = datetime.strptime(
                    f"{ev['fecha']} {ev['hora']}", "%Y-%m-%d %H:%M"
                )
            except Exception:
                continue
            if cuando >= ahora:
                futuros.append((cuando, ev))

        futuros.sort(key=lambda par: par[0])

        for _, ev in futuros[:12]:
            self.tabla_prox.insert(
                "",
                "end",
                iid=f"p{ev['id']}",
                values=(ev["fecha"], ev["hora"], ev["titulo"]),
            )

    def _seleccionar_evento(self, _event=None):
        seleccion = self.tabla_dia.selection()
        if seleccion:
            self._mostrar_evento(int(seleccion[0]))

    def _seleccionar_proximo(self, _event=None):
        seleccion = self.tabla_prox.selection()
        if not seleccion:
            return
        iid = seleccion[0]
        if iid.startswith("p"):
            self._mostrar_evento(int(iid[1:]))

    def _mostrar_evento(self, local_id):
        ev = agenda.obtener_evento(local_id)
        if not ev:
            return

        self.evento_seleccionado_id = local_id
        self.fecha_seleccionada = ev["fecha"]

        dt = datetime.strptime(ev["fecha"], "%Y-%m-%d")
        self.anio = dt.year
        self.mes = dt.month

        self.var_titulo.set(ev["titulo"])
        self.var_fecha.set(ev["fecha"])
        self.var_hora.set(ev["hora"])
        self.var_lugar.set(ev["lugar"])
        self.var_aviso.set(self._texto_aviso(ev["recordatorio_minutos"]))

        self.txt_notas.delete("1.0", "end")
        self.txt_notas.insert("1.0", ev["notas"])

        self._dibujar_calendario()
        self._cargar_eventos_dia()

    def _limpiar_detalle(self):
        self.var_titulo.set("")
        self.var_fecha.set(self.fecha_seleccionada)
        self.var_hora.set("09:00")
        self.var_lugar.set("")
        self.var_aviso.set("24 horas antes")
        self.txt_notas.delete("1.0", "end")

    def _texto_aviso(self, minutos):
        try:
            minutos = int(minutos)
        except Exception:
            minutos = 0

        if minutos == 1440:
            return "24 horas antes"
        if minutos == 60:
            return "1 hora antes"
        if minutos == 30:
            return "30 minutos antes"
        if minutos == 15:
            return "15 minutos antes"
        if minutos <= 0:
            return "Sin aviso"
        return f"{minutos} minutos antes"

    def _recordatorio_a_minutos(self):
        mapa = {
            "Sin aviso": 0,
            "15 minutos antes": 15,
            "30 minutos antes": 30,
            "1 hora antes": 60,
            "24 horas antes": 1440,
        }
        return mapa.get(self.var_aviso.get(), 1440)

    def nuevo_evento(self):
        self.evento_seleccionado_id = None
        self._limpiar_detalle()

    def _payload_formulario(self):
        return {
            "titulo": self.var_titulo.get().strip(),
            "fecha": self.var_fecha.get().strip(),
            "hora": self.var_hora.get().strip(),
            "lugar": self.var_lugar.get().strip(),
            "notas": self.txt_notas.get("1.0", "end").strip(),
            "recordatorio_minutos": self._recordatorio_a_minutos(),
        }

    def guardar_evento(self):
        payload = self._payload_formulario()

        if not payload["titulo"]:
            messagebox.showerror("Agenda Beta", "Escriba un título para el evento.")
            return

        try:
            datetime.strptime(payload["fecha"], "%Y-%m-%d")
            datetime.strptime(payload["hora"], "%H:%M")
        except Exception:
            messagebox.showerror(
                "Agenda Beta",
                "Revise la fecha (YYYY-MM-DD) y la hora (HH:MM).",
            )
            return

        try:
            if self.evento_seleccionado_id is None:
                ev = agenda.crear_evento(payload)
                self.evento_seleccionado_id = ev["id"]
            else:
                actualizado = agenda.actualizar_evento(
                    self.evento_seleccionado_id,
                    payload,
                )
                if not actualizado:
                    raise RuntimeError("No se encontró el evento local a actualizar.")
        except Exception as exc:
            messagebox.showerror(
                "Agenda Beta",
                f"No pude guardar el evento local.\n\n{exc}",
            )
            return

        try:
            ev = agenda.obtener_evento(self.evento_seleccionado_id)
            google_event_id = str((ev or {}).get("google_event_id") or "").strip()
            google_calendar_id = str((ev or {}).get("google_calendar_id") or "").strip()

            if google_event_id:
                sync_google = calendar_write.actualizar_evento(
                    google_event_id,
                    payload,
                    calendar_id=google_calendar_id,
                )
            else:
                sync_google = calendar_write.crear_evento(payload)

            agenda.vincular_google(self.evento_seleccionado_id, sync_google)

        except Exception as exc:
            agenda.marcar_sync_error(self.evento_seleccionado_id, exc)
            messagebox.showwarning(
                "Agenda Beta",
                "El evento quedó guardado localmente, pero la sincronización "
                f"con Google Calendar falló.\n\n{exc}",
            )
        else:
            messagebox.showinfo(
                "Agenda Beta",
                "Evento guardado localmente y sincronizado con Google Calendar.",
            )

        self.fecha_seleccionada = payload["fecha"]
        dt = datetime.strptime(payload["fecha"], "%Y-%m-%d")
        self.anio = dt.year
        self.mes = dt.month
        self.refrescar()

    def eliminar_evento(self):
        if self.evento_seleccionado_id is None:
            messagebox.showinfo("Agenda Beta", "Seleccione un evento local.")
            return

        ev = agenda.obtener_evento(self.evento_seleccionado_id)
        if not ev:
            self.refrescar()
            return

        google_event_id = str(ev.get("google_event_id") or "").strip()
        google_calendar_id = str(ev.get("google_calendar_id") or "").strip()

        if google_event_id:
            texto = (
                f"¿Eliminar este evento de la Agenda local y de Google Calendar?\n\n"
                f"{ev['titulo']}\n"
                f"{ev['fecha']} a las {ev['hora']}\n\n"
                "La eliminación se hará sobre el mismo evento Google vinculado."
            )
        else:
            texto = (
                f"¿Eliminar este evento de la Agenda local?\n\n"
                f"{ev['titulo']}\n"
                f"{ev['fecha']} a las {ev['hora']}\n\n"
                "Este evento no tiene un identificador Google vinculado."
            )

        if not messagebox.askyesno("Agenda Beta", texto):
            return

        if google_event_id:
            try:
                calendar_write.eliminar_evento(
                    google_event_id,
                    calendar_id=google_calendar_id,
                )
            except Exception as exc:
                agenda.marcar_sync_error(self.evento_seleccionado_id, exc)
                messagebox.showerror(
                    "Agenda Beta",
                    "No eliminé la copia local porque primero falló la eliminación "
                    f"del evento Google vinculado.\n\n{exc}",
                )
                self.refrescar()
                return

        if agenda.eliminar_evento(self.evento_seleccionado_id):
            self.evento_seleccionado_id = None
            self._limpiar_detalle()
            self.refrescar()
            messagebox.showinfo("Agenda Beta", "Evento eliminado correctamente.")
        else:
            messagebox.showerror("Agenda Beta", "No pude eliminar el evento local.")

    def mes_anterior(self):
        if self.mes == 1:
            self.mes = 12
            self.anio -= 1
        else:
            self.mes -= 1
        self.fecha_seleccionada = f"{self.anio:04d}-{self.mes:02d}-01"
        self.evento_seleccionado_id = None
        self._limpiar_detalle()
        self.refrescar()

    def mes_siguiente(self):
        if self.mes == 12:
            self.mes = 1
            self.anio += 1
        else:
            self.mes += 1
        self.fecha_seleccionada = f"{self.anio:04d}-{self.mes:02d}-01"
        self.evento_seleccionado_id = None
        self._limpiar_detalle()
        self.refrescar()

    def ir_hoy(self):
        hoy = date.today()
        self.anio = hoy.year
        self.mes = hoy.month
        self.fecha_seleccionada = hoy.isoformat()
        self.evento_seleccionado_id = None
        self._limpiar_detalle()
        self.refrescar()


if __name__ == "__main__":
    AgendaBetaCalendario().mainloop()
