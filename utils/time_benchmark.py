import random
import timeit
from sorting.bubble_sort import bubblesort
from sorting.insertion_sort import insertionsort
from sorting.selection_sort import selectionsort

def generate_list(size, n):
    return [random.randint(0,n) for _ in range(size)]

def random_timed_selection_sort(size, n):
    data = generate_list(size, n)
    print(f"Arreglo (Random Selection sort):{data}")
    print("======"*10)
    selectionsort(data)
    
def random_timed_insertion_sort(size, n):
    data = generate_list(size, n)
    print(f"Arreglo (Random Insertion sort):{data}")
    print("======"*10)
    insertionsort(data)
    
def random_timed_bubble_sort(size, n):
    data = generate_list(size, n)
    print(f"Arreglo (Random Bubble sort):{data}")
    print("======"*10)
    bubblesort(data)
    
def timed_selection_sort(data):
    print(f"Arreglo (Selection sort):{data}")
    print("======"*10)
    selectionsort(data)
    
def timed_insertion_sort(data):
    print(f"Arreglo (Insertion sort):{data}")
    print("======"*10)
    insertionsort(data)
    
def timed_bubble_sort(data):
    print(f"Arreglo (Bubble sort):{data}")
    print("======"*10)
    bubblesort(data)
    
def sortResults(str, data, reps, num):
    if(str == "selectionsort"):   
        times = timeit.repeat(stmt=lambda: timed_selection_sort(data), repeat=reps, number=num)
    elif(str == "insertionsort"):
        times = timeit.repeat(stmt=lambda: timed_insertion_sort(data), repeat=reps, number=num)
    elif(str == "bubblesort"):
        times = timeit.repeat(stmt=lambda: timed_bubble_sort(data), repeat=reps, number=num)

    tiempos = []
    mpm = []
    for i,t in enumerate(times,1):
        tiempos.append(f"{t:.5f} s")  
    mpm.append(f"{min(times):.5f} s")
    mpm.append(f"{sum(times)/len(times):.5f} s")
    mpm.append(f"{max(times):.5f} s")
    
    return tiempos, mpm

    
def sortRandomResults(str, size, n, reps, num):
    if(str == "selectionsort"):   
        times = timeit.repeat(stmt=lambda: random_timed_selection_sort(size, n), repeat=reps, number=num)
    elif(str == "insertionsort"):
        times = timeit.repeat(stmt=lambda: random_timed_insertion_sort(size, n), repeat=reps, number=num)
    elif(str == "bubblesort"):
        times = timeit.repeat(stmt=lambda: random_timed_bubble_sort(size, n), repeat=reps, number=num)

    tiempos = []
    mpm = []
    for i,t in enumerate(times,1):
        tiempos.append(f"{t:.5f} s")  
    mpm.append(f"{min(times):.5f} s")
    mpm.append(f"{sum(times)/len(times):.5f} s")
    mpm.append(f"{max(times):.5f} s")
    
    return tiempos, mpm