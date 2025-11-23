import tkinter as tk
from tkinter import ttk, messagebox
import calendar
from datetime import datetime, timedelta
import json
import os

# Variables
ARCHIVO_DATOS = "Turnos de trabajo.json"

MESES_ES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]
DIAS_ES = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
DIAS_COMPLETOS_ES = {
    "Monday": "Lunes",
    "Tuesday": "Martes",
    "Wednesday": "Miércoles",
    "Thursday": "Jueves",
    "Friday": "Viernes",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
}

# Configuración ventana
class PlanificadorTurnos:
    def __init__(self, root):
        self.root = root
        self.root.title("Planificador jornada laboral")
        ancho, alto = 820, 620
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        x = (sw - ancho) // 2
        y = (sh - alto) // 2
        root.geometry(f"{ancho}x{alto}+{x}+{y}")
        root.resizable(False, False)
        root.configure(bg="#f6f6f6")

        self.mes = datetime.now().month
        self.año = datetime.now().year
        self.config_turno = None
        self.dias_trabajo = set()
        self.dias_descanso = set()
        self.dia_seleccionado = None

        # Barra lateral izquierda
        left = tk.Frame(root, bg="#f6f6f6")
        left.pack(side="left", anchor="n", padx=(8, 4), pady=8)

        tk.Label(left, text="Configuración del turno", font=("Arial", 12, "bold"), bg="#f6f6f6").pack(anchor="w", pady=(0, 6))

        tk.Label(left, text="Días de trabajo:", bg="#f6f6f6").pack(anchor="w")
        self.entry_trabajo = ttk.Entry(left, width=14)
        self.entry_trabajo.pack(anchor="w", pady=(0, 6))

        tk.Label(left, text="Días de descanso:", bg="#f6f6f6").pack(anchor="w")
        self.entry_descanso = ttk.Entry(left, width=14)
        self.entry_descanso.pack(anchor="w", pady=(0, 6))

        tk.Label(left, text="Fecha de inicio (dd/mm/aa):", bg="#f6f6f6").pack(anchor="w")
        self.entry_inicio = ttk.Entry(left, width=14)
        self.entry_inicio.pack(anchor="w", pady=(0, 6))

        tk.Label(left, text="Fecha de término (opcional):", bg="#f6f6f6").pack(anchor="w")
        self.entry_termino = ttk.Entry(left, width=14)
        self.entry_termino.pack(anchor="w", pady=(0, 8))

        tk.Label(left, text="Tipo de jornada:", bg="#f6f6f6").pack(anchor="w")
        self.jornada_var = tk.StringVar(value="Mañana")
        ttk.Radiobutton(left, text="Mañana", variable=self.jornada_var, value="Mañana").pack(anchor="w", padx=6)
        ttk.Radiobutton(left, text="Tarde", variable=self.jornada_var, value="Tarde").pack(anchor="w", padx=6)
        ttk.Radiobutton(left, text="Noche", variable=self.jornada_var, value="Noche").pack(anchor="w", padx=6)

        ttk.Button(left, text="Aplicar Jornada", command=self.aplicar_rotacion).pack(fill="x", pady=(10, 6))
        ttk.Button(left, text="Vaciar Día Seleccionado", command=self.limpiar_dia_seleccionado).pack(fill="x", pady=3)
        ttk.Button(left, text="Limpiar Calendario", command=self.limpiar_calendario).pack(fill="x", pady=(6, 4))
        ttk.Button(left, text="Vaciar Campos", command=self.limpiar_campos).pack(fill="x", pady=(4, 8))

        simbologia = tk.LabelFrame(left, text="Simbología", padx=6, pady=6)
        simbologia.pack(anchor="w", pady=(4, 0))
        fila1 = tk.Frame(simbologia)
        fila1.pack(anchor="w", pady=2)
        tk.Label(fila1, bg="#FF6666", width=3, height=1, bd=1, relief="groove").pack(side="left")
        tk.Label(fila1, text="  Día de trabajo").pack(side="left", padx=(6, 0))
        fila2 = tk.Frame(simbologia)
        fila2.pack(anchor="w", pady=2)
        tk.Label(fila2, bg="#8BE78B", width=3, height=1, bd=1, relief="groove").pack(side="left")
        tk.Label(fila2, text="  Día libre").pack(side="left", padx=(6, 0))

        # Interfaz calendario
        right = tk.Frame(root, bg="#f6f6f6")
        right.pack(side="left", fill="both", expand=True, padx=(4, 8), pady=8)

        header = tk.Frame(right, bg="#f6f6f6")
        header.pack(anchor="n", pady=(0, 2))
        ttk.Button(header, text="Anterior", width=10, command=self.mes_anterior).pack(side="left", padx=(0, 2))
        self.label_mes = tk.Label(header, text="", font=("Arial", 14, "bold"), bg="#f6f6f6")
        self.label_mes.pack(side="left", padx=6)
        ttk.Button(header, text="Siguiente", width=10, command=self.mes_siguiente).pack(side="left", padx=(2, 0))

        cal_frame = tk.Frame(right, bg="#ffffff", bd=0)
        cal_frame.pack(anchor="n", pady=(2, 2))

        header_row = tk.Frame(cal_frame, bg="#ffffff")
        header_row.pack(anchor="n", pady=(6, 0))
        for i, d in enumerate(DIAS_ES):
            lbl = tk.Label(header_row, text=d, font=("Arial", 10, "bold"), bg="#ffffff", width=8)
            lbl.grid(row=0, column=i, padx=1)

        self.grid_frame = tk.Frame(cal_frame, bg="#ffffff")
        self.grid_frame.pack(anchor="n", pady=(2, 6))

        self.label_jornada = tk.Label(right, text="", font=("Arial", 11, "bold"), bg="#f6f6f6")
        self.label_jornada.pack(anchor="n", pady=(2, 6))

        self.label_reloj = tk.Label(right, text="", font=("Arial", 10), bg="#f6f6f6")
        self.label_reloj.pack(side="bottom", anchor="e", pady=(0, 4), padx=(0, 6))

        self.botones_dias = []

        self.cargar_datos_guardados()
        self.mostrar_calendario()
        self.actualizar_reloj()

    # Funcionalidad principal
    def mostrar_calendario(self):
        for w in self.grid_frame.winfo_children():
            w.destroy()
        self.botones_dias = []
        self.label_mes.config(text=f"{MESES_ES[self.mes - 1]} {self.año}")

        cal = calendar.Calendar(firstweekday=0)
        semanas = cal.monthdayscalendar(self.año, self.mes)

        for r, semana in enumerate(semanas):
            for c, dia in enumerate(semana):
                if dia == 0:
                    tk.Label(self.grid_frame, text="", bg="#ffffff", width=8, height=4).grid(row=r, column=c, padx=1, pady=1)
                else:
                    btn = tk.Button(self.grid_frame, text=str(dia), bg="#ffffff", width=8, height=4,
                                    relief="raised", bd=1,
                                    command=lambda d=dia: self.seleccionar_dia(d))
                    btn.grid(row=r, column=c, padx=1, pady=1)
                    self.botones_dias.append((dia, btn))

        self._calcular_dias_para_mes_actual()
        self.colorear_dias()
        self.actualizar_seleccion_visual()

        if self.config_turno:
            jornada = self.config_turno.get("jornada", "")
            self.label_jornada.config(text=f"Jornada: {jornada}")
        else:
            self.label_jornada.config(text="")

    def colorear_dias(self):
        for dia, widget in self.botones_dias:
            if dia in self.dias_trabajo:
                widget.config(bg="#FF6666")
            elif dia in self.dias_descanso:
                widget.config(bg="#8BE78B")
            else:
                widget.config(bg="white")

    def actualizar_seleccion_visual(self):
        for dia, widget in self.botones_dias:
            if self.dia_seleccionado and dia == self.dia_seleccionado:
                widget.config(relief="sunken", bd=2)
            else:
                widget.config(relief="raised", bd=1)

    def seleccionar_dia(self, dia):
        self.dia_seleccionado = dia
        self.actualizar_seleccion_visual()

    def limpiar_dia_seleccionado(self):
        if not self.dia_seleccionado:
            messagebox.showinfo("Aviso", "Selecciona un día del calendario para limpiar.")
            return

        dia = self.dia_seleccionado
        if dia in self.dias_trabajo or dia in self.dias_descanso:
            self.dias_trabajo.discard(dia)
            self.dias_descanso.discard(dia)
            self.colorear_dias()
            self.actualizar_seleccion_visual()
            messagebox.showinfo("Listo", f"Se limpió el día {dia}.")
        else:
            messagebox.showinfo("Aviso", f"El día {dia} no tiene turno.")

    def aplicar_rotacion(self):
        try:
            dias_trabajo = int(self.entry_trabajo.get())
            dias_descanso = int(self.entry_descanso.get())
            inicio_str = self.entry_inicio.get()
            termino_str = self.entry_termino.get().strip()
            jornada = self.jornada_var.get()

            inicio = datetime.strptime(inicio_str, "%d/%m/%y")
            termino = datetime.strptime(termino_str, "%d/%m/%y") if termino_str else None

            self.config_turno = {
                "trabajo": dias_trabajo,
                "descanso": dias_descanso,
                "inicio": inicio.strftime("%Y-%m-%d"),
                "termino": termino.strftime("%Y-%m-%d") if termino else None,
                "jornada": jornada
            }

            self.guardar_datos()
            self.mostrar_calendario()

        except ValueError:
            messagebox.showerror("Error", "Verifica que las fechas (dd/mm/aa) y días de turno sean válidos.")

    def _calcular_dias_para_mes_actual(self):
        self.dias_trabajo.clear()
        self.dias_descanso.clear()

        if not self.config_turno:
            return

        dias_trabajo = self.config_turno["trabajo"]
        dias_descanso = self.config_turno["descanso"]
        inicio = datetime.strptime(self.config_turno["inicio"], "%Y-%m-%d")
        termino = datetime.strptime(self.config_turno["termino"], "%Y-%m-%d") if self.config_turno["termino"] else None

        dia_actual = inicio
        ciclo = dias_trabajo + dias_descanso
        contador = 0

        while True:
            if termino and dia_actual > termino:
                break
            if dia_actual.year > self.año + 1:
                break

            mes_act = dia_actual.month == self.mes and dia_actual.year == self.año
            if contador < dias_trabajo:
                if mes_act:
                    self.dias_trabajo.add(dia_actual.day)
            else:
                if mes_act:
                    self.dias_descanso.add(dia_actual.day)

            contador = (contador + 1) % ciclo
            dia_actual += timedelta(days=1)

            if not termino and dia_actual.year > self.año + 1:
                break

    # Definiciones
    def limpiar_calendario(self):
        confirmar = messagebox.askyesno("AVISO", "¿Seguro que quieres eliminar el turno?")
        if not confirmar:
            return

        self.dias_trabajo.clear()
        self.dias_descanso.clear()
        self.config_turno = None
        self.colorear_dias()

        if os.path.exists(ARCHIVO_DATOS):
            os.remove(ARCHIVO_DATOS)

        messagebox.showinfo("Listo", "Se eliminó el turno")

    def limpiar_campos(self):
        for e in [self.entry_trabajo, self.entry_descanso, self.entry_inicio, self.entry_termino]:
            e.delete(0, tk.END)
        self.jornada_var.set("Mañana")
        messagebox.showinfo("Listo", "Calendario vaciado")

    def mes_anterior(self):
        self.mes -= 1
        if self.mes == 0:
            self.mes = 12
            self.año -= 1
        self.mostrar_calendario()

    def mes_siguiente(self):
        self.mes += 1
        if self.mes == 13:
            self.mes = 1
            self.año += 1
        self.mostrar_calendario()

    def actualizar_reloj(self):
        ahora = datetime.now()
        dia_semana = DIAS_COMPLETOS_ES[ahora.strftime("%A")]
        texto = f"{dia_semana} - {ahora.day}/{ahora.month}/{ahora.year}, {ahora.strftime('%H:%M:%S')}"
        self.label_reloj.config(text=texto)
        self.root.after(1000, self.actualizar_reloj)

    # Archivo .JSON
    def guardar_datos(self):
        datos = {"config_turno": self.config_turno}
        with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)

    def cargar_datos_guardados(self):
        if os.path.exists(ARCHIVO_DATOS):
            with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
                datos = json.load(f)
                self.config_turno = datos.get("config_turno")
        if self.config_turno:
            self._calcular_dias_para_mes_actual()


if __name__ == "__main__":
    root = tk.Tk()
    app = PlanificadorTurnos(root)
    root.mainloop()