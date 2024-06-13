import random
from time import time

def avg(tablica):
    avg = []
    tablica.sort()
    suma = 0
    for j in range(7):
        if (j > 0) and (j < 6):
            suma += tablica[j]
    avg.append(suma / 5)
    return avg
def greedy_load_containers(capacity, containers):
    # Oblicz wartość jednostkową i sortuj kontenery według tej wartości malejąco
    containers.sort(key=lambda x: x[1] / x[0], reverse=True)
    #print(containers)
    total_value = 0
    total_weight = 0
    selected_containers = []

    for weight, value in containers:
        if total_weight + weight <= capacity:
            selected_containers.append((weight, value))
            total_weight += weight
            total_value += value

    return total_value, total_weight, selected_containers
def dynamic_load_containers(capacity, containers):
    n = len(containers)
    # Tworzenie tabeli DP o wymiarach (n+1) x (capacity+1)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    # Przetwarzanie tabeli DP
    for i in range(1, n + 1):
        weight, value = containers[i - 1]
        for w in range(capacity + 1):
            if weight <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weight] + value)
            else:
                dp[i][w] = dp[i - 1][w]

    # Wyznaczenie maksymalnej wartości
    total_value = dp[n][capacity]

    #for i in range(n+1):
    #    print(dp[i], end="\n")

    # Wyznaczenie, które kontenery zostały wybrane
    total_weight = 0
    selected_containers = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            weight, value = containers[i - 1]
            selected_containers.append((weight, value))
            total_weight += weight
            w -= weight

    return total_value, total_weight, selected_containers


# generowanie kontenerów
n = 6000  # liczba kontenerów
base_containers = []
for _ in range(n+1):
    base_containers.append((random.randint(1, 150), random.randint(1, 20)))  # (waga, wartość)

k = n//15  # wzrost ładowności

for b in range(k, n+1, k):

    time_error = []  # (0: dynamic, 1: greedy, 2: błąd pomiaru)
    czasy_dynamic = []
    czasy_greedy = []
    errors = []

    # pomiary
    for i in range(7):

        containers = base_containers.copy()
        t0 = time()
        dynamic_total_value, dynamic_total_weight, dynamic_selected_containers = dynamic_load_containers(b, containers)
        t1 = time()
        greedy_total_value, greedy_total_weight, greedy_selected_containers = greedy_load_containers(b, containers)
        t2 = time()
        # błąd pomiaru
        measurement_error = (dynamic_total_value - greedy_total_value) / dynamic_total_value

        czasy_dynamic.append(t1 - t0)
        czasy_greedy.append(t2 - t1)
        errors.append(measurement_error)

    time_error = (avg(czasy_dynamic), avg(czasy_greedy), avg(errors))
    print(*time_error[0], *time_error[1], *time_error[2], sep=" ")



"""# Przykładowe dane wejściowe
capacity = 10
containers = [
    (1,10),  # kontener o wadze 10 i wartości 60
    (2,20),
    (3,30),
    (1,15),
    (2,25),
    (3,5),
    (1,10),
    (1,5),
"""