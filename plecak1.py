import random
import timeit
import statistics
import os
import sys

def read_data_from_file(filename):
    # Odczytuje dane z pliku
    input_folder = 'input'
    filepath = os.path.join(input_folder, filename)
    with open(filepath, 'r') as file:
        lines = file.readlines()
        num_items = int(lines[0].strip())
        weights = list(map(int, lines[1].strip().split()))
        values = list(map(int, lines[2].strip().split()))
        capacity = int(lines[3].strip())

        # Debugowanie - sprawdzenie, czy wartości są poprawnie odczytane
        print("Liczba elementów:", num_items)
        print("Wagi:", weights)
        print("Wartości:", values)
        print("Pojemność:", capacity)

    return weights, values, capacity


def generate_random_data(num_items, min_weight, max_weight, min_value, max_value, capacity):
    # Generuje losowe dane
    weights = [random.randint(min_weight, max_weight) for _ in range(num_items)]
    values = [random.randint(min_value, max_value) for _ in range(num_items)]
    return weights, values, capacity


def avg(data):
    # Oblicza średnią bez najmniejszej i największej wartości
    if len(data) < 3:
        return sum(data) / len(data)
    sorted_data = sorted(data)
    return sum(sorted_data[1:-1]) / (len(data) - 2)


def greedy_load_containers(capacity, weights, values):
    # Algorytm zachłanny do ładowania kontenerów
    containers = sorted(zip(weights, values), key=lambda x: x[1] / x[0], reverse=True)
    total_value, total_weight = 0, 0
    selected_containers = []
    for weight, value in containers:
        if total_weight + weight <= capacity:
            selected_containers.append((weight, value))
            total_weight += weight
            total_value += value
    return total_value, total_weight, selected_containers


def dynamic_load_containers(capacity, weights, values):
    # Algorytm dynamicznego programowania do ładowania kontenerów
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]
    return dp[n][capacity], dp


def save_results_to_file(results, filename_suffix):
    # Zapisuje wyniki do pliku w folderze 'results' z unikalnymi nazwami plików
    results_dir = 'results'
    os.makedirs(results_dir, exist_ok=True)
    base_filename = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    filename = f"{base_filename}_{filename_suffix}.txt"
    file_path = os.path.join(results_dir, filename)
    counter = 1
    while os.path.exists(file_path):
        file_path = os.path.join(results_dir, f"{base_filename}_{filename_suffix}_{counter}.txt")
        counter += 1
    with open(file_path, 'w') as file:
        file.writelines(results)
    print(f"Wyniki zapisane do {file_path}")


def perform_measurements():
    global capacity  # Używa globalnej pojemności zdefiniowanej wcześniej
    dynamic_times, greedy_times, errors = [], [], []
    results = []

    # Generuje losowe dane na podstawie domyślnych lub zmodyfikowanych globalnych ustawień
    num_items = capacity // 15
    weights, values, capacity = generate_random_data(num_items, min_weight, max_weight, min_value, max_value, capacity)

    for n in range(k, capacity + 1, k):
        dynamic_timer = timeit.Timer(lambda: dynamic_load_containers(n, weights, values))
        greedy_timer = timeit.Timer(lambda: greedy_load_containers(n, weights, values))

        dynamic_time = min(dynamic_timer.repeat(repeat, number))
        greedy_time = min(greedy_timer.repeat(repeat, number))

        dynamic_value, _ = dynamic_load_containers(n, weights, values)
        greedy_value, greedy_weight, _ = greedy_load_containers(n, weights, values)

        measurement_error = (dynamic_value - greedy_value) / dynamic_value if dynamic_value != 0 else 0

        dynamic_times.append(dynamic_time)
        greedy_times.append(greedy_time)
        errors.append(measurement_error)

        result_line = f"Pojemność: {n}, Średni czas dynamiczny: {avg(dynamic_times):.8f}, Średni czas zachłanny: {avg(greedy_times):.8f}, Średni błąd: {avg(errors):.8f}\n"
        results.append(result_line)
        print(result_line.strip())

    save_results_to_file(results, 'range_of_capacities')


def process_file_data():
    weights, values, capacity = read_data_from_file(filename)
    results = []

    dynamic_value, dp = dynamic_load_containers(capacity, weights, values)

    results.append("Tabela dynamicznego programowania:\n")
    for row in dp:
        results.append(" ".join(map(str, row)) + "\n")

    for line in results:
        print(line.strip())

# Konfigurowalne parametry
min_weight = 1  # minimalna waga
max_weight = 150  # maksymalna waga
min_value = 1  # minimalna wartość
max_value = 20  # maksymalna wartość
capacity = 6000  # Pojemność statku
k = capacity // 15  # Interwał zwiększenia pojemności
repeat = 3  # Liczba powtórzeń pomiaru czasu
number = 1  # Liczba wykonań pomiaru czasu

# Ustaw tutaj nazwę pliku, 'none' dla losowych danych lub podaj nazwę pliku do odczytu z folderu 'input'
# filename = "none"  # Odkomentuj tę linię, aby użyć losowych danych


filename = "plecak.txt"  # Odkomentuj i ustaw właściwą nazwę pliku, aby odczytać z pliku

# Odkomentuj odpowiednią funkcję do uruchomienia
if filename == "none":
    perform_measurements()
else:
    process_file_data()


