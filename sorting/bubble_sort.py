from utils.Tarea import get_key

def bubblesort(data, criterio):
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if get_key(data[j], criterio) > get_key(data[j + 1], criterio):
                data[j], data[j + 1] = data[j + 1], data[j]