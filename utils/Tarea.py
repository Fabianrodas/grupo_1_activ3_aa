from datetime import datetime, timedelta
import random

class Tarea:
    def __init__(self, nombre, fecha_vencimiento, prioridad):
        self.nombre = nombre
        self.fecha_vencimiento = fecha_vencimiento
        self.prioridad = prioridad

    def __repr__(self):
        return f"{self.nombre} | Vence: {self.fecha_vencimiento.date()} | Prioridad: {self.prioridad}"
    
def generate_list(size):
    tareas = []
    for i in range(size):
        nombre = f"Tarea_{i+1}"
        fecha = datetime.now() + timedelta(days=random.randint(1, 30))
        prioridad = random.randint(1, 5)
        tareas.append(Tarea(nombre, fecha, prioridad))
    return tareas

def ingresar_diez_tareas():
    tareas = []
    for i in range(10):
        nombre = input("Nombre de la tarea: ").strip()
        fecha = input("Fecha de vencimiento (YYYY-MM-DD): ").strip()
        prioridad = input("Prioridad (1 a 5): ").strip()
        tareas.append(Tarea(nombre, fecha, prioridad))
    return tareas

def ingresar_tareas():
    tareas = []
    while True:
        nombre = input("Nombre de la tarea (o 'fin' para terminar): ").strip()
        if nombre.lower() == 'fin':
            break
        fecha = input("Fecha de vencimiento (YYYY-MM-DD): ").strip()
        prioridad = input("Prioridad (1 a 5): ").strip()
        tareas.append(Tarea(nombre, fecha, prioridad))
    return tareas

def get_key(item, criterio):
    if criterio == "fecha":
        return item.fecha_vencimiento
    elif criterio == "prioridad":
        return int(item.prioridad)
    elif criterio == "nombre":
        return item.nombre.lower()
    else:
        raise ValueError("Criterio no válido. Usa 'fecha', 'prioridad' o 'nombre'.")