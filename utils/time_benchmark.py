import timeit
import pandas as pd
from sorting.bubble_sort import bubblesort
from sorting.insertion_sort import insertionsort
from sorting.selection_sort import selectionsort
from utils.Tarea import generate_list
import psutil
import winreg
import os
import platform

def random_timed_selection_sort(size, criterio):
    data = generate_list(size)
    print(f"Arreglo (Random Selection sort):{data}")
    print("======"*10)
    selectionsort(data, criterio)
    return data
    
def random_timed_insertion_sort(size, criterio):
    data = generate_list(size)
    print(f"Arreglo (Random Insertion sort):{data}")
    print("======"*10)
    insertionsort(data, criterio)
    return data
    
def random_timed_bubble_sort(size, criterio):
    data = generate_list(size)
    print(f"Arreglo (Random Bubble sort):{data}")
    print("======"*10)
    bubblesort(data, criterio)
    return data
    
def timed_selection_sort(data, criterio):
    print(f"Arreglo (Selection sort):{data}")
    print("======"*10)
    selectionsort(data, criterio)
    
def timed_insertion_sort(data, criterio):
    print(f"Arreglo (Insertion sort):{data}")
    print("======"*10)
    insertionsort(data, criterio)
    
def timed_bubble_sort(data, criterio):
    print(f"Arreglo (Bubble sort):{data}")
    print("======"*10)
    bubblesort(data, criterio)
    
def sortResults(str, data, criterio, reps, num):
    if(str == "selectionsort"):   
        times = timeit.repeat(stmt=lambda: timed_selection_sort(data, criterio), repeat=reps, number=num)
    elif(str == "insertionsort"):
        times = timeit.repeat(stmt=lambda: timed_insertion_sort(data, criterio), repeat=reps, number=num)
    elif(str == "bubblesort"):
        times = timeit.repeat(stmt=lambda: timed_bubble_sort(data, criterio), repeat=reps, number=num)

    tiempos = []
    mpm = []
    for i,t in enumerate(times,1):
        tiempos.append(f"{t:.5f} s")  
    mpm.append(f"{min(times):.5f} s")
    mpm.append(f"{sum(times)/len(times):.5f} s")
    mpm.append(f"{max(times):.5f} s")
    
    return tiempos, mpm

    
def sortRandomResults(str, size, criterio, reps, num):
    ordenados = []
    desordenados = []
    tiempos_crudos = []

    def wrap_sort(sort_func):
        def inner():
            lista = generate_list(size)
            desordenados.append(lista.copy())
            sort_func(lista, criterio)
            ordenados.append(lista.copy())
        return inner

    if str == "selectionsort":
        func = wrap_sort(selectionsort)
    elif str == "insertionsort":
        func = wrap_sort(insertionsort)
    elif str == "bubblesort":
        func = wrap_sort(bubblesort)

    tiempos_crudos = timeit.repeat(stmt=func, repeat=reps, number=num)

    tiempos = [f"{t:.5f} s" for t in tiempos_crudos]
    mpm = [
        f"{min(tiempos_crudos):.5f} s",
        f"{sum(tiempos_crudos) / len(tiempos_crudos):.5f} s",
        f"{max(tiempos_crudos):.5f} s"
    ]

    return ordenados, tiempos, mpm, desordenados

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


def guardar_resultados_csv(nombre_archivo, tareas, tiempos, criterio, algoritmo, mpm, tareas_desordenadas):
    resumen_data = []
    tareas_desordenadas_data = []
    tareas_ordenadas_data = []
    resumen_mpm = []

    for i, tiempo in enumerate(tiempos):
        tareas_en_intento = tareas[i]
        if tareas_en_intento and isinstance(tareas_en_intento[0], list):
            tareas_en_intento = tareas_en_intento[0]

        resumen_data.append({
            "Intento": i + 1,
            "Tiempo (s)": round(float(str(tiempo).replace("s", "").strip()), 6),
            "Criterio": criterio,
            "Algoritmo": algoritmo,
            "Tipo" : "random" if ("random" in nombre_archivo) else "specific",
            "Input Size": len(tareas_en_intento)
        })

        tiempo_valor = round(float(str(tiempo).replace("s", "").strip()), 6)

        # Agregar tareas ordenadas
        for tarea in tareas_en_intento:
            tareas_ordenadas_data.append({
                "Intento": i + 1,
                "Nombre de tarea": tarea.nombre,
                "Fecha": tarea.fecha_vencimiento.strftime("%Y-%m-%d"),
                "Prioridad": tarea.prioridad,
                "Tiempo (s)": tiempo_valor,
                "Criterio": criterio,
                "Algoritmo": algoritmo
            })

        # Agregar tareas desordenadas (si existen)
        if i < len(tareas_desordenadas):
            des = tareas_desordenadas[i]
            if des and isinstance(des[0], list):
                des = des[0]

            for tarea in des:
                tareas_desordenadas_data.append({
                    "Intento": i + 1,
                    "Nombre de tarea": tarea.nombre,
                    "Fecha": tarea.fecha_vencimiento.strftime("%Y-%m-%d"),
                    "Prioridad": tarea.prioridad,
                    "Tiempo (s)": tiempo_valor,
                    "Criterio": criterio,
                    "Algoritmo": algoritmo
                })



    df_resumen = pd.DataFrame(resumen_data)
    df_tareas_desordenadas = pd.DataFrame(tareas_desordenadas_data)
    df_tareas_ordenadas = pd.DataFrame(tareas_ordenadas_data)
    resumen_mpm.append({
        "Mínimo (s)" : round(float(str(mpm[0]).replace("s", "").strip()), 6),
        "Promedio (s)" : round(float(str(mpm[1]).replace("s", "").strip()), 6),
        "Máximo (s)" : round(float(str(mpm[2]).replace("s", "").strip()), 6),
        "Criterio": criterio,
        "Algoritmo": algoritmo,
        "Tipo" : "random" if ("random" in nombre_archivo) else "specific",
        "Input Size": len(tareas_en_intento)
    })
    df_sistema = get_sistema_df()
    df_mpm = pd.DataFrame(resumen_mpm)

    with pd.ExcelWriter(nombre_archivo) as writer:
        df_resumen.to_excel(writer, sheet_name="Resumen", index=False)
        df_tareas_desordenadas.to_excel(writer, sheet_name="Tareas Desordenadas", index=False)
        df_tareas_ordenadas.to_excel(writer, sheet_name="Tareas Ordenadas", index=False)
        df_mpm.to_excel(writer, sheet_name="Resumen MPM", index=False)
        df_sistema.to_excel(writer, sheet_name="Sistema", index=False)