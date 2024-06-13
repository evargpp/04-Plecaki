import random
import timeit
import os
import statistics

def avg(data):
    """Calculate the average excluding the smallest and largest values."""
    if len(data) < 3:
        return sum(data) / len(data) if data else 0
    sorted_data = sorted(data)
    return sum(sorted_data[1:-1]) / (len(data) - 2)

def greedy_load_containers(capacity, containers):
    """Greedy algorithm to maximize container loading value."""
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
    """Dynamic programming approach to solve the knapsack problem."""
    n = len(containers)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        weight, value = containers[i - 1]
        for w in range(capacity + 1):
            if weight <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weight] + value)
            else:
                dp[i][w] = dp[i - 1][w]
    total_value = dp[n][capacity]
    selected_containers = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            weight, value = containers[i - 1]
            selected_containers.append((weight, value))
            w -= weight
    return total_value, dp[n][capacity], selected_containers

import os

import os
import sys

def perform_measurements(capacity, min_weight, max_weight, min_value, max_value, k, repeat, number):
    """Function to perform and save the measurements of the container loading algorithms."""
    dynamic_times, greedy_times, errors = [], [], []
    results = []

    for n in range(k, capacity + 1, k):
        base_containers = [(random.randint(min_weight, max_weight), random.randint(min_value, max_value)) for _ in range(n + 1)]

        for _ in range(7):
            containers = base_containers.copy()
            dynamic_timer = timeit.Timer(lambda: dynamic_load_containers(capacity, containers))
            greedy_timer = timeit.Timer(lambda: greedy_load_containers(capacity, containers))

            dynamic_time = min(dynamic_timer.repeat(repeat, number))
            greedy_time = min(greedy_timer.repeat(repeat, number))

            dynamic_total_value, _, _ = dynamic_load_containers(capacity, containers)
            greedy_total_value, _, _ = greedy_load_containers(capacity, containers)

            measurement_error = (dynamic_total_value - greedy_total_value) / dynamic_total_value if dynamic_total_value != 0 else 0

            dynamic_times.append(dynamic_time)
            greedy_times.append(greedy_time)
            errors.append(measurement_error)

        result_line = f"Capacity: {n}, Dynamic avg time: {avg(dynamic_times):.8f}, Greedy avg time: {avg(greedy_times):.8f}, Average error: {avg(errors):.8f}\n"
        results.append(result_line)
        print(result_line.strip())

    # Save results to a file with a unique name based on the script name
    save_results_to_file(results)

def save_results_to_file(results):
    """Saves the collected results into a file in the 'results' directory with incremental filenames."""
    results_dir = 'results'
    os.makedirs(results_dir, exist_ok=True)  # Make sure the directory exists

    base_filename = os.path.splitext(os.path.basename(sys.argv[0]))[0]  # Get the name of the current script without extension
    filename = f"{base_filename}_results.txt"
    file_path = os.path.join(results_dir, filename)

    # If the file already exists, add a number to create a unique filename
    counter = 1
    while os.path.exists(file_path):
        file_path = os.path.join(results_dir, f"{base_filename}_results_{counter}.txt")
        counter += 1

    with open(file_path, 'w') as file:
        file.writelines(results)
    print(f"Results saved to {file_path}")

# Configurable parameters
min_weight = 1
max_weight = 150
min_value = 1
max_value = 20
capacity = 600  # Ship capacity
k = capacity // 15  # Interval increase for capacity
repeat = 3  # Number of repeats for time measurement
number = 1  # Number of executions for time measurement

perform_measurements(capacity, min_weight, max_weight, min_value, max_value, k, repeat, number)
