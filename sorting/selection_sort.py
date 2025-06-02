from utils.Tarea import get_key

def selectionsort(data, criterio):
    n = len(data)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if get_key(data[j], criterio) < get_key(data[min_idx], criterio):
                min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]