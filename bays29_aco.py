import numpy as np
import random
import math
import matplotlib.pyplot as plt

bays29_coords = [
    (1150, 1760), (630, 1660), (40, 2090), (750, 1100), (750, 2030),
    (1030, 2070), (1650, 650), (1490, 1630), (790, 2260), (710, 1310),
    (840, 550), (1170, 2300), (970, 1340), (510, 700), (750, 900),
    (1280, 1200), (230, 590), (460, 860), (1040, 950), (590, 1390),
    (830, 1770), (490, 500), (1840, 1240), (1260, 1500), (1280, 790),
    (490, 2130), (1460, 1420), (1260, 1910), (360, 1980)
]
def compute_distance(city1, city2):
    x1, y1 = city1
    x2, y2 = city2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
num_cities = len(bays29_coords)
distance_matrix = np.zeros((num_cities, num_cities))
for i in range(num_cities):
    for j in range(i + 1, num_cities):
        distance_matrix[i, j] = distance_matrix[j, i] = compute_distance(bays29_coords[i], bays29_coords[j])

#ACO parameters
num_ants = 50
num_iterations = 1000
pheromone_decay = 0.2
pheromone_constant = 1.0
alpha = 1.0
beta = 1.0
pheromone_matrix = np.ones((num_cities, num_cities))

# ACO algorithm
best_tour = None
best_distance = float('inf')

for iteration in range(num_iterations):
    ant_tours = []

    for ant in range(num_ants):
        current_city = random.randint(0, num_cities - 1)
        unvisited_cities = set(range(num_cities))
        unvisited_cities.remove(current_city)
        tour = [current_city]
        total_distance = 0

        while unvisited_cities:
            next_city = max(unvisited_cities, key=lambda city: (pheromone_matrix[current_city, city] ** alpha) * (1 / distance_matrix[current_city, city]) ** beta)
            tour.append(next_city)
            unvisited_cities.remove(next_city)
            total_distance += distance_matrix[current_city, next_city]
            current_city = next_city
        
        
        # Add the distance from the last city to the starting city
        total_distance += distance_matrix[current_city, tour[0]]

        # Update the best tour if a shorter distance is found
        if total_distance < best_distance:
            best_tour = tour
            best_distance = total_distance

        ant_tours.append((tour, total_distance))

    # Update pheromone levels
    pheromone_matrix *= (1 - pheromone_decay)
    for tour, distance in ant_tours:
        for i in range(len(tour) - 1):
            pheromone_matrix[tour[i], tour[i + 1]] += pheromone_constant / distance

print("Best TSP Tour:", best_tour)
print("Total Distance:", best_distance)
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
