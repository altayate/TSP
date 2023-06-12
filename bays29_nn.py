import math
import random
import matplotlib.pyplot as plt
import time

bays29_coords = [
    (1150, 1760), (630, 1660), (40, 2090), (750, 1100), (750, 2030),
    (1030, 2070), (1650, 650), (1490, 1630), (790, 2260), (710, 1310),
    (840, 550), (1170, 2300), (970, 1340), (510, 700), (750, 900),
    (1280, 1200), (230, 590), (460, 860), (1040, 950), (590, 1390),
    (830, 1770), (490, 500), (1840, 1240), (1260, 1500), (1280, 790),
    (490, 2130), (1460, 1420), (1260, 1910), (360, 1980)
]

start_time = time.time()
elapsed_time = 0
times = []

def compute_distance(city1, city2):
    x1, y1 = city1
    x2, y2 = city2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def nearest_neighbor_tsp(coords, start_city):
    num_cities = len(coords)
    unvisited_cities = set(range(num_cities))
    current_city = start_city
    tsp_tour = []

    while unvisited_cities:
        nearest_city = min(unvisited_cities, key=lambda city: compute_distance(coords[current_city], coords[city]))
        tsp_tour.append(nearest_city)
        unvisited_cities.remove(nearest_city)
        current_city = nearest_city
    tsp_tour.append(start_city)
    return tsp_tour

#Nearest Neighbor algorithm with different permutations
best = 0
iteration = 0
best_tour = []
total_time = 0
total_objective_value = 0
found_optimal = 0

num_iterations = 10000
time_limit = 10.0

for i in range(num_iterations):
    current_time = time.time()
    start_city = i % len(bays29_coords)
    tsp_tour = nearest_neighbor_tsp(bays29_coords, start_city)
    end_time = time.time()

    total_distance = sum(compute_distance(bays29_coords[tsp_tour[i]], bays29_coords[tsp_tour[i+1]]) for i in range(len(tsp_tour) - 1))

    total_time += end_time - start_time
    total_objective_value += total_distance

    if total_distance < best or best == 0:
        elapsed_time = current_time - start_time
        times.append(elapsed_time)
        best = total_distance
        iteration = i
        best_tour = tsp_tour
        found_optimal += 1
        print("New optimal time found: ", elapsed_time, " Current tour distance: ", best)


average_runtime = total_time / num_iterations
success_rate = found_optimal / num_iterations
average_objective_value = total_objective_value / num_iterations

print("Average Runtime:", average_runtime)
print("Success Rate:", success_rate)
print("Average Objective Value:", average_objective_value)
print("Best: ", best)

ordered_coords = [bays29_coords[i] for i in best_tour]

x = [coord[0] for coord in ordered_coords]
y = [coord[1] for coord in ordered_coords]

# Plot the cities
plt.plot(x, y, 'o-')
plt.title("TSP Tour")
plt.xlabel("X-coordinate")
plt.ylabel("Y-coordinate")
plt.grid(True)
plt.show()
