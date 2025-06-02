from utils.time_benchmark import sortRandomResults, sortResults
import pandas as pd
from datetime import datetime
import os
import platform
import psutil
import winreg
from utils.Tarea import ingresar_diez_tareas

# Función para obtener el nombre exacto (porque os lo agarra mal) del sistema operativo
def get_sistema_operativo_real():
    try:
        clave = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
        )
        product_name, _ = winreg.QueryValueEx(clave, "ProductName")
        build, _ = winreg.QueryValueEx(clave, "CurrentBuildNumber")
        if int(build) >= 22000:
            return product_name.replace("Windows 10", "Windows 11")
        return product_name
    except Exception as e:
        return f"No disponible ({e})"
    
# DataFrame con información del sistema donde se haran las pruebas
def get_sistema_df():
    try:
        usuario = os.getlogin()
    except:
        usuario = "Desconocido"

    info = {
        "Elemento": [
            "Sistema Operativo",
            "Versión del OS",
            "Nombre del Equipo",
            "Tipo de sistema",
            "Arquitectura",
            "Procesador",
            "Núcleos físicos",
            "Núcleos lógicos",
            "RAM Total (GB)",
            "Memoria ROM / Disco (GB)",
            "Usuario actual"
        ],
        "Valor": [
            get_sistema_operativo_real(), 
            platform.version(),
            platform.node(),
            platform.architecture()[0],
            platform.machine(),
            platform.processor(),
            psutil.cpu_count(logical=False),
            psutil.cpu_count(logical=True),
            f"{psutil.virtual_memory().total / (1024**3):.2f}",
            f"{psutil.disk_usage('/').total / (1024**3):.2f}",
            usuario
        ]
    }

    return pd.DataFrame(info)

def guardar_resultados_csv(nombre_archivo, tareas, tiempos, criterio, algoritmo, mpm):
    intentos_data = []

    for i, tiempo in enumerate(tiempos):
        tareas_en_intento = tareas[i]

        # Verificamos si es una lista de listas y la aplanamos
        if tareas_en_intento and isinstance(tareas_en_intento[0], list):
            tareas_en_intento = tareas_en_intento[0]

        for tarea in tareas_en_intento:
            intentos_data.append({
                "Intento": i + 1,
                "Nombre de tarea": tarea.nombre,
                "Fecha": tarea.fecha_vencimiento.strftime("%Y-%m-%d"),
                "Prioridad": tarea.prioridad,
                "Tiempo (s)": round(float(str(tiempo).replace("s", "").strip()), 6),
                "Criterio": criterio,
                "Algoritmo": algoritmo
            })

    df_intentos = pd.DataFrame(intentos_data)
    df_mpm = pd.DataFrame({
        "Métrica": ["Mínimo", "Promedio", "Máximo"],
        "Tiempo (s)": [
            round(float(str(mpm[0]).replace("s", "").strip()), 6),
            round(float(str(mpm[1]).replace("s", "").strip()), 6),
            round(float(str(mpm[2]).replace("s", "").strip()), 6),
        ]
    })

    with pd.ExcelWriter(nombre_archivo) as writer:
        df_intentos.to_excel(writer, sheet_name="Resultados", index=False)
        df_mpm.to_excel(writer, sheet_name="Resumen MPM", index=False)

def main():

    df_sistema = get_sistema_df()

    x = input("\n¿Deseas realizar pruebas con tareas aleatorias, específicas o salir del programa? (a/e/s): ").strip().lower()
    while(True):
        if x == "a":
            size = int(input("Ingresa el tamaño del arreglo de tareas aleatorias: "))
            criterio = input("Ingresa el criterio de ordenamiento (nombre/fecha/prioridad): ").strip().lower()
            algorithm = input("Ingresa el algoritmo de ordenamiento (bubblesort/selectionsort/insertionsort): ").strip().lower()
            reps = int(input("Ingresa el número de repeticiones para la prueba: "))
            num = int(input("Ingresa el número de veces que se ejecutará cada repetición: "))
            tareas,tiempos,mpm = sortRandomResults(algorithm, size, criterio, reps, num)
            filename = "data/" + f"random_{algorithm}_{datetime.now().strftime('%Y%m%d%H%M%S')}" + ".xlsx"
            guardar_resultados_csv(filename, tareas, tiempos, criterio, algorithm, mpm)
            if os.path.exists(filename):
                print(f"\nResultados guardados en {filename}\n")
            else:
                print("\nError al guardar los resultados. Por favor, intente nuevamente.\n")
        elif x == "e":
            print("Ingresa 10 tareas:")
            tareas = ingresar_diez_tareas()
            criterio = input("Ingresa el criterio de ordenamiento (nombre/fecha/prioridad): ").strip().lower()
            algorithm = input("Ingresa el algoritmo de ordenamiento (bubblesort/selectionsort/insertionsort): ").strip().lower()
            reps = int(input("Ingresa el número de repeticiones para la prueba: "))
            num = int(input("Ingresa el número de veces que se ejecutará cada repetición: "))
            tiempos, mpm = sortResults(algorithm, tareas, criterio, reps, num)
            filename = "data/" + f"random_{algorithm}_{datetime.now().strftime('%Y%m%d%H%M%S')}" + ".xlsx"
            guardar_resultados_csv(filename, tareas, tiempos, criterio, algorithm, mpm)
            if os.path.exists(filename):
                print(f"\nResultados guardados en {filename}\n")
            else:
                print("\nError al guardar los resultados. Por favor, intente nuevamente.\n")
        elif x == "s":
            print("Saliendo del programa.")
            return
        else:
            print("Opción no válida. Inténtalo de nuevo.")
        x = input("\n¿Deseas realizar pruebas con tareas aleatorias, específicas o salir del programa? (a/e/s): ").strip().lower()    
        
if __name__ == "__main__":
    main()