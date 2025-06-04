import tkinter as tk
from tkinter import ttk, messagebox
from utils.time_benchmark import sortResults, sortRandomResults, guardar_resultados_csv
from utils.Tarea import Tarea
from datetime import datetime
import os
import copy


class AplicacionOrdenamiento:
    def __init__(self, root):
        self.root = root
        self.root.title("Benchmarking de Ordenamiento de Tareas")
        self.root.state('zoomed')  # Maximizar ventana

        self.tipo_tarea = tk.StringVar(value="aleatorias")
        self.criterio = tk.StringVar(value="nombre")
        self.algoritmo = tk.StringVar(value="bubblesort")
        self.tipo_tarea.trace_add("write", lambda *args: self._actualizar_campos_visibles())

        self.entries_tareas = []
        self._crear_widgets()

    def _crear_widgets(self):
        fuente = ("Segoe UI", 12)

        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.frame, text="¿Deseas realizar pruebas con tareas aleatorias o específicas?", font=fuente).pack(anchor="w")
        tk.Radiobutton(self.frame, text="Aleatorias", variable=self.tipo_tarea, value="aleatorias", font=fuente).pack(anchor="w")
        tk.Radiobutton(self.frame, text="Específicas", variable=self.tipo_tarea, value="especificas", font=fuente).pack(anchor="w")

        self.lbl_tamano = tk.Label(self.frame, text="Tamaño del arreglo de tareas aleatorias:", font=fuente)
        self.entry_tamano = tk.Entry(self.frame, font=fuente)

        tk.Label(self.frame, text="Criterio de ordenamiento:", font=fuente).pack(anchor="w")
        self.combo_criterio = ttk.Combobox(self.frame, textvariable=self.criterio, values=["nombre", "fecha", "prioridad"], font=fuente)
        self.combo_criterio.pack(anchor="w", fill=tk.X)

        tk.Label(self.frame, text="Algoritmo de ordenamiento:", font=fuente).pack(anchor="w")
        self.combo_algoritmo = ttk.Combobox(self.frame, textvariable=self.algoritmo, values=["bubblesort", "selectionsort", "insertionsort"], font=fuente)
        self.combo_algoritmo.pack(anchor="w", fill=tk.X)

        tk.Label(self.frame, text="Número de repeticiones:", font=fuente).pack(anchor="w")
        self.entry_reps = tk.Entry(self.frame, font=fuente)
        self.entry_reps.pack(anchor="w", fill=tk.X)

        self.frame_tareas = tk.Frame(self.frame)
        self.frame_tareas.pack(fill=tk.BOTH, expand=False)

        self.lbl_tamano.pack(anchor="w")
        self.entry_tamano.pack(anchor="w", fill=tk.X)

        self.btn_ejecutar = tk.Button(self.frame, text="Iniciar prueba", command=self._iniciar_prueba, font=fuente)
        self.btn_ejecutar.pack(pady=10, side="bottom")

    def _actualizar_campos_visibles(self):
        for widget in self.frame_tareas.winfo_children():
            widget.destroy()
        self.entries_tareas.clear()

        if self.tipo_tarea.get() == "aleatorias":
            self.frame_tareas.pack_forget()
            self.lbl_tamano.pack(anchor="w")
            self.entry_tamano.pack(anchor="w", fill=tk.X)
        else:
            self.lbl_tamano.pack_forget()
            self.entry_tamano.pack_forget()
            self.frame_tareas.pack(fill=tk.BOTH, expand=False)

            tk.Label(self.frame_tareas, text="Ingrese los datos de las 10 tareas:", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, columnspan=3, sticky="w")
            tk.Label(self.frame_tareas, text="Nombre", font=("Segoe UI", 11)).grid(row=1, column=0)
            tk.Label(self.frame_tareas, text="Fecha (YYYY-MM-DD)", font=("Segoe UI", 11)).grid(row=1, column=1)
            tk.Label(self.frame_tareas, text="Prioridad(1-5)", font=("Segoe UI", 11)).grid(row=1, column=2)

            for i in range(10):
                fila = []
                for j in range(3):
                    e = tk.Entry(self.frame_tareas, width=20, font=("Segoe UI", 11))
                    e.grid(row=i+2, column=j, padx=4, pady=2)
                    fila.append(e)
                self.entries_tareas.append(fila)

    def _iniciar_prueba(self):
        tipo = self.tipo_tarea.get()
        criterio = self.criterio.get()
        algoritmo = self.algoritmo.get()

        try:
            reps = int(self.entry_reps.get())
        except ValueError:
            messagebox.showerror("Error", "Existen campos vacíos o inválidos")
            return

        if tipo == "aleatorias":
            try:
                size = int(self.entry_tamano.get())
            except ValueError:
                messagebox.showerror("Error", "Existen campos vacíos o inválidos")
                return

            tareas_ordenadas, tiempos, mpm, tareas_desordenadas = sortRandomResults(
                algoritmo, size, criterio, reps, 1
            )
        else:
            tareas = []
            try:
                for fila in self.entries_tareas:
                    nombre = fila[0].get()
                    fecha = fila[1].get()
                    prioridad = fila[2].get()
                    if not nombre or not fecha or not prioridad:
                        raise ValueError("Hay campos vacíos")
                    fecha_dt = datetime.strptime(fecha, "%Y-%m-%d")
                    prioridad_int = int(prioridad)
                    if not (1 <= prioridad_int <= 5):
                        raise ValueError("Prioridad fuera de rango")
                    tareas.append(Tarea(nombre, fecha_dt, prioridad_int))
            except Exception:
                messagebox.showerror("Error", "Hay campos vacíos o con formato incorrecto.")
                return

            tareas_desordenadas = [copy.deepcopy(tareas) for _ in range(reps)]
            tareas_ordenadas = []
            tiempos = []

            for i in range(reps):
                t = copy.deepcopy(tareas)
                tiempo_list, _ = sortResults(algoritmo, t, criterio, 1, 1)
                tiempo = float(tiempo_list[0].replace("s", "").strip())
                tareas_ordenadas.append(t)
                tiempos.append(tiempo)

            mpm = (
                f"{min(tiempos):.5f} s",
                f"{sum(tiempos) / len(tiempos):.5f} s",
                f"{max(tiempos):.5f} s"
            )

        # Guardar automáticamente en la carpeta 'data' con formato personalizado
        nombre_archivo = os.path.join("data", f"random_{algoritmo}_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx")
        guardar_resultados_csv(nombre_archivo, tareas_ordenadas, tiempos, criterio, algoritmo, mpm, tareas_desordenadas)
        messagebox.showinfo("Guardado", f"Resultados guardados en {nombre_archivo}")

        self.mostrar_resultados(tareas_ordenadas, tiempos, mpm, tareas_desordenadas, criterio, algoritmo)

    def mostrar_resultados(self, tareas_ordenadas, tiempos, mpm, tareas_desordenadas, criterio, algoritmo):
        ventana_resultados = tk.Toplevel(self.root)
        ventana_resultados.title("Resultados")
        ventana_resultados.geometry("1000x600")

        texto = tk.Text(ventana_resultados, font=("Consolas", 11))
        texto.pack(fill=tk.BOTH, expand=True)

        for i, (des, ord, tiempo) in enumerate(zip(tareas_desordenadas, tareas_ordenadas, tiempos), start=1):
            texto.insert(tk.END, f"\nIntento {i}\n")
            texto.insert(tk.END, "Tareas desordenadas:\n")
            for tarea in des:
                texto.insert(tk.END, f"  - {tarea.nombre}, {tarea.fecha_vencimiento.date()}, P{tarea.prioridad}\n")

            texto.insert(tk.END, "Tareas ordenadas:\n")
            for tarea in ord:
                texto.insert(tk.END, f"  - {tarea.nombre}, {tarea.fecha_vencimiento.date()}, P{tarea.prioridad}\n")

            texto.insert(tk.END, f"Tiempo: {tiempo}\n")

        texto.insert(tk.END, "\nResumen MPM:\n")
        texto.insert(tk.END, f"Mínimo: {mpm[0]}\n")
        texto.insert(tk.END, f"Promedio: {mpm[1]}\n")
        texto.insert(tk.END, f"Máximo: {mpm[2]}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionOrdenamiento(root)
    root.mainloop()
