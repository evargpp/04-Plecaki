import random
import timeit
import statistics
import os
import sys


def avg(data):
    """Oblicza średnią, pomijając najmniejszą i największą wartość."""
    if len(data) < 3:
        return sum(data) / len(data) if data else 0
    sorted_data = sorted(data)
    return sum(sorted_data[1:-1]) / (len(data) - 2)


def greedy_load_containers(capacity, containers):
    """Algorytm zachłanny maksymalizujący wartość załadunku kontenerów."""
    containers.sort(key=lambda x: x[1] / x[0], reverse=True)
    total_value, total_weight = 0, 0
    selected_containers = []
    for weight, value in containers:
        if total_weight + weight <= capacity:
            selected_containers.append((weight, value))
            total_weight += weight
            total_value += value
    return total_value, total_weight, selected_containers


def dynamic_load_containers(capacity, containers):
    """Algorytm programowania dynamicznego do rozwiązywania problemu plecakowego."""
    n = len(containers)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        weight, value = containers[i - 1]
        for w in range(capacity + 1):
            if weight <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weight] + value)
            else:
                dp[i][w] = dp[i - 1][w]
    total_value, total_weight = dp[n][capacity], 0
    selected_containers = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            weight, value = containers[i - 1]
            selected_containers.append((weight, value))
            total_weight += weight
            w -= weight
    return total_value, total_weight, selected_containers


def perform_measurements(base_containers):
    """Wykonuje pomiary i zapisuje wyniki algorytmów do załadunku kontenerów."""
    n = len(base_containers) - 1  # Dostosowanie, ponieważ base_containers zawiera n+1 elementów
    k = n // 15
    dynamic_times, greedy_times, errors = [], [], []
    results = []

    for b in range(k, n + 1, k):
        for _ in range(7):
            containers = base_containers.copy()
            dynamic_timer = timeit.Timer(lambda: dynamic_load_containers(b, containers))
            greedy_timer = timeit.Timer(lambda: greedy_load_containers(b, containers))

            dynamic_time = min(dynamic_timer.repeat(TIMEIT_REPEAT, TIMEIT_NUMBER))
            greedy_time = min(greedy_timer.repeat(TIMEIT_REPEAT, TIMEIT_NUMBER))

            dynamic_total_value, _, _ = dynamic_load_containers(b, containers)
            greedy_total_value, _, _ = greedy_load_containers(b, containers)

            measurement_error = (dynamic_total_value - greedy_total_value) / dynamic_total_value if dynamic_total_value != 0 else 0

            dynamic_times.append(dynamic_time)
            greedy_times.append(greedy_time)
            errors.append(measurement_error)

        result_line = f"Capacity: {b}, Dynamic avg time: {avg(dynamic_times):.8f}, Greedy avg time: {avg(greedy_times):.8f}, Average error: {avg(errors):.8f}"
        results.append(result_line + "\n")
        print(result_line)  # Wyświetla wyniki na konsoli w trakcie działania programu

    save_results_to_file(results)  # Zapisuje wszystkie wyniki do pliku na koniec

def save_results_to_file(results):
    """Zapisuje zebrane wyniki do pliku w katalogu 'results' z nazwami plików zwiększanymi numerycznie."""
    os.makedirs(RESULTS_DIR, exist_ok=True)  # Upewnij się, że katalog istnieje
    base_filename = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    filename = f"{base_filename}_results.txt"
    file_path = os.path.join(RESULTS_DIR, filename)

    counter = 1
    while os.path.exists(file_path):
        file_path = os.path.join(RESULTS_DIR, f"{base_filename}_results_{counter}.txt")
        counter += 1

    with open(file_path, 'w') as file:
        file.writelines(results)
    print(f"Wyniki zapisane w {file_path}")  # Informuje użytkownika o zapisaniu wyników


# Konfiguracja
NUM_CONTAINERS = 600
WEIGHT_MIN = 1
WEIGHT_MAX = 150
VALUE_MIN = 1
VALUE_MAX = 20
TIMEIT_REPEAT = 3
TIMEIT_NUMBER = 1
RESULTS_DIR = 'results'

# Generowanie kontenerów
base_containers = [(random.randint(WEIGHT_MIN, WEIGHT_MAX), random.randint(VALUE_MIN, VALUE_MAX)) for _ in
                   range(NUM_CONTAINERS + 1)]
perform_measurements(base_containers)
