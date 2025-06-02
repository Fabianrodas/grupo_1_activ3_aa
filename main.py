from utils.time_benchmark import sortRandomResults, sortResults
import pandas as pd
from datetime import datetime
import os
import platform
import psutil
import winreg

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

df_sistema = get_sistema_df()

# Parámetros de entrada
size = 10  # Tamaño del arreglo
n = 100    # Rango de elementos a generar aleatoriamente
reps = 5   # Número de repeticiones para medir el tiempo
num = 1    # Número de veces que se ejecuta cada sort

x = input("\n¿Deseas realizar pruebas con arreglos aleatorios o específicos o salir del programa? (a/e/s): ").strip().lower()
while(True):
    if x == "a":
        size = int(input("Ingrese el tamaño del arreglo: "))
        n = int(input("Ingrese el rango de elementos a generar aleatoriamente: "))
        reps = int(input("Ingrese el número de repeticiones para medir el tiempo: "))
        num = int(input("Ingrese el número de veces que se ejecuta cada sort: "))
        algorithm = input("Ingrese el algoritmo a utilizar (selectionsort, insertionsort, bubblesort): ").strip().lower()
        
        while algorithm not in ["selectionsort", "insertionsort", "bubblesort"]:
            print("\nAlgoritmo no válido. Por favor, elija uno de los siguientes: selectionsort, insertionsort, bubblesort.\n")
            algorithm = input("Ingrese el algoritmo a utilizar: ").strip().lower()
        
        tiempos,mpm = sortRandomResults(algorithm, size, n, reps, num)
        
        df_tiempos = pd.DataFrame({
            "Repetición": list(range(1, len(tiempos)+1)),
            "Tiempo": tiempos
        })

        df_mpm = pd.DataFrame({
            "Métrica": ["Mínimo", "Promedio", "Máximo"],
            "Valor": mpm
        })
        
        filename = "data/" + f"random_{algorithm}_{datetime.now().strftime('%Y%m%d%H%M%S')}" + ".xlsx"
        
        with pd.ExcelWriter(filename) as writer:
            df_tiempos.to_excel(writer, sheet_name="Tiempos", index=False)
            df_mpm.to_excel(writer, sheet_name="Resumen", index=False)
            df_sistema.to_excel(writer, sheet_name="Sistema", index=False)
        
        if os.path.exists(filename):
            print(f"\nResultados guardados en {filename}\n")
        else:
            print("\nError al guardar los resultados. Por favor, intente nuevamente.\n")
            
    elif x == "e":
        data_input = input("Ingrese los elementos del arreglo separados por comas: ")
        data = list(map(int, data_input.split(',')))
        reps = int(input("Ingrese el número de repeticiones para medir el tiempo: "))
        num = int(input("Ingrese el número de veces que se ejecuta cada sort: "))
        algorithm = input("Ingrese el algoritmo a utilizar (selectionsort, insertionsort, bubblesort): ").strip().lower()
        
        while algorithm not in ["selectionsort", "insertionsort", "bubblesort"]:
            print("\nAlgoritmo no válido. Por favor, elija uno de los siguientes: selectionsort, insertionsort, bubblesort.\n")
            algorithm = input("Ingrese el algoritmo a utilizar: ").strip().lower()
        
        tiempos,mpm = sortResults(algorithm, data, reps, num)
        
        df_tiempos = pd.DataFrame({
            "Repetición": list(range(1, len(tiempos)+1)),
            "Tiempo": tiempos
        })

        df_mpm = pd.DataFrame({
            "Métrica": ["Mínimo", "Promedio", "Máximo"],
            "Valor": mpm
        })
        
        filename = "data/" + f"{algorithm}_{datetime.now().strftime('%Y%m%d%H%M%S')}" + ".xlsx"
        
        with pd.ExcelWriter(filename) as writer:
            df_tiempos.to_excel(writer, sheet_name="Tiempos", index=False)
            df_mpm.to_excel(writer, sheet_name="Resumen", index=False)
            df_sistema.to_excel(writer, sheet_name="Sistema", index=False)
            
        if os.path.exists(filename):
            print(f"\nResultados guardados en {filename}\n")
        else:
            print("\nError al guardar los resultados. Por favor, intente nuevamente.\n")
            
    elif x == "s":
        print("\nSaliendo del programa.\n")
        exit()
    else:
        print("\nOpción no válida. Intente nuevamente.\n")
    x = input("¿Deseas realizar pruebas con arreglos aleatorios o específicos o salir del programa? (a/e/s): ").strip().lower()