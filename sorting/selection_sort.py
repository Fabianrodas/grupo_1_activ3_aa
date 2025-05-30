def selectionsort(n):
    for i in range(len(n)):
        min = i
        for j in range(i+1, len(n)):
            if n[j] < n[min]:
                min = j
        n[i], n[min] = n[min], n[i]