def insertionsort(n):
    for i in range(1, len(n)):
        u = n[i]
        j = i - 1
        while j >= 0 and u < n[j]:
            n[j + 1] = n[j]
            j -= 1
        n[j + 1] = u