from utils.Tarea import get_key

def insertionsort(data, criterio):
    for i in range(1, len(data)):
        key_item = data[i]
        j = i - 1
        while j >= 0 and get_key(data[j], criterio) > get_key(key_item, criterio):
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = key_item