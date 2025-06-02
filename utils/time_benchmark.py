import timeit
from sorting.bubble_sort import bubblesort
from sorting.insertion_sort import insertionsort
from sorting.selection_sort import selectionsort
from utils.Tarea import generate_list

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
    data = []
    
    if(str == "selectionsort"):   
        times = timeit.repeat(stmt=lambda: data.append(random_timed_selection_sort(size, criterio)), repeat=reps, number=num)
    elif(str == "insertionsort"):
        times = timeit.repeat(stmt=lambda: data.append(random_timed_insertion_sort(size, criterio)), repeat=reps, number=num)
    elif(str == "bubblesort"):
        times = timeit.repeat(stmt=lambda: data.append(random_timed_bubble_sort(size, criterio)), repeat=reps, number=num)

    tiempos = []
    mpm = []
    for i,t in enumerate(times,1):
        print(f"Repetición {i}: {t:.5f} s")
        tiempos.append(f"{t:.5f} s")  
    print(f"min: {min(times):.5f} s")
    mpm.append(f"{min(times):.5f} s")
    print(f"promedio: {sum(times)/len(times):.5f} s")
    mpm.append(f"{sum(times)/len(times):.5f} s")
    print(f"max: {max(times):.5f} s")
    mpm.append(f"{max(times):.5f} s")
    
    return data,tiempos, mpm