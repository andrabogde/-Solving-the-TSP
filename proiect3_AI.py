import random
import math
import matplotlib.pyplot as plt

# -----------------------------
# GENERARE DATE & UTILE
# -----------------------------
#Generează n orașe cu coordonate aleatorii în intervalele specificate.
def generate_cities(n, x_range=(0, 100), y_range=(0, 100)):
    return [(random.uniform(*x_range), random.uniform(*y_range)) for _ in range(n)]

#Calculează distanța totală a unui traseu.
def total_distance(route, cities):
    dist = 0
    for i in range(len(route)):
        x1, y1 = cities[route[i]]
        x2, y2 = cities[route[(i + 1) % len(route)]]
        dist += math.hypot(x2 - x1, y2 - y1)
    return dist

# Vizualizează traseul într-un grafic.
def plot_route(route, cities, title="Traseu optimizat"):
    x = [cities[i][0] for i in route] + [cities[route[0]][0]]
    y = [cities[i][1] for i in route] + [cities[route[0]][1]]
    plt.figure(figsize=(10, 8))
    plt.plot(x, y, 'o-', color='blue')
    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    
    # Adăugăm numerotarea cronologică (1, 2, 3, ...) în loc de indexul orașului
    for step, city_idx in enumerate(route):
        xi, yi = cities[city_idx]
        # Numerotarea pornește de la 1
        plt.text(xi + 1, yi + 1, f"{step + 1} ({city_idx})", fontsize=9)
    
    # Marcăm punctul de start/finish cu un cerc mai mare
    start_idx = route[0]
    plt.plot(cities[start_idx][0], cities[start_idx][1], 'o', color='green', markersize=10)
    plt.text(cities[start_idx][0] + 1, cities[start_idx][1] + 1, "START/FINISH", fontsize=10, weight='bold')
    
    # Adăugăm legendă
    plt.figtext(0.5, 0.01, "Format: Pas cronologic (Index original oraș)", ha="center", fontsize=10)
    
    plt.tight_layout()
    plt.show()


# -----------------------------
# 1. HILL CLIMBING
# -----------------------------
def hill_climbing(cities, max_iterations=1000):
    current_route = list(range(len(cities)))
    random.shuffle(current_route)
    current_cost = total_distance(current_route, cities)

    for _ in range(max_iterations):
        i, j = random.sample(range(len(cities)), 2)
        neighbor = current_route[:]
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        neighbor_cost = total_distance(neighbor, cities)
        if neighbor_cost < current_cost:
            current_route = neighbor
            current_cost = neighbor_cost

    return current_route, current_cost


# -----------------------------
# 2. SIMULATED ANNEALING
# -----------------------------
def simulated_annealing(cities, T=1000, T_min=1e-3, alpha=0.995):
    current_route = list(range(len(cities)))
    random.shuffle(current_route)
    current_cost = total_distance(current_route, cities)
    best_route = current_route[:]
    best_cost = current_cost

    while T > T_min:
        i, j = random.sample(range(len(cities)), 2)
        neighbor = current_route[:]
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        neighbor_cost = total_distance(neighbor, cities)

        delta = neighbor_cost - current_cost
        if delta < 0 or random.random() < math.exp(-delta / T):
            current_route = neighbor
            current_cost = neighbor_cost
            if current_cost < best_cost:
                best_route = current_route[:]
                best_cost = current_cost

        T *= alpha

    return best_route, best_cost


# -----------------------------
# 3. ALGORITM GENETIC
# -----------------------------
def crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [None] * size
    child[start:end] = parent1[start:end]

    fill = [item for item in parent2 if item not in child]
    idx = 0
    for i in range(size):
        if child[i] is None:
            child[i] = fill[idx]
            idx += 1
    return child

def mutate(route, mutation_rate=0.02):
    for i in range(len(route)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(route)-1)
            route[i], route[j] = route[j], route[i]

def genetic_algorithm(cities, population_size=100, generations=500):
    population = [random.sample(range(len(cities)), len(cities)) for _ in range(population_size)]

    for _ in range(generations):
        population.sort(key=lambda route: total_distance(route, cities))
        new_population = population[:10]  # elitism

        while len(new_population) < population_size:
            parent1, parent2 = random.choices(population[:50], k=2)
            child = crossover(parent1, parent2)
            mutate(child)
            new_population.append(child)

        population = new_population

    best_route = min(population, key=lambda route: total_distance(route, cities))
    return best_route, total_distance(best_route, cities)


# -----------------------------
# RULARE & COMPARAȚIE
# -----------------------------
if __name__ == "__main__":
    # Folosim seed pentru reproducibilitate
    random.seed(42)
    
    num_cities = 20
    cities = generate_cities(num_cities)

    # Hill Climbing
    hc_route, hc_cost = hill_climbing(cities)
    print(f"Hill Climbing: {hc_cost:.2f}")
    plot_route(hc_route, cities, "Hill Climbing - Traseu Optimizat")

    # Simulated Annealing
    sa_route, sa_cost = simulated_annealing(cities)
    print(f"Simulated Annealing: {sa_cost:.2f}")
    plot_route(sa_route, cities, "Simulated Annealing - Traseu Optimizat")

    # Algoritm Genetic
    ga_route, ga_cost = genetic_algorithm(cities)
    print(f"Algoritm Genetic: {ga_cost:.2f}")
    plot_route(ga_route, cities, "Algoritm Genetic - Traseu Optimizat")

    # Afișăm ordinea exactă a vizitării orașelor pentru cel mai bun algoritm
    best_cost = min(hc_cost, sa_cost, ga_cost)
    best_route = None
    best_name = ""
    
    if best_cost == hc_cost:
        best_route = hc_route
        best_name = "Hill Climbing"
    elif best_cost == sa_cost:
        best_route = sa_route
        best_name = "Simulated Annealing"
    else:
        best_route = ga_route
        best_name = "Algoritm Genetic"
    
    print(f"\nCel mai bun algoritm: {best_name} cu costul {best_cost:.2f}")
    print(f"Ordinea de vizitare a orașelor (indexuri originale): {best_route}")
    
    # Afișăm și traseul detaliat, folosind numerotarea cronologică
    print("\nTraseul detaliat:")
    print("Format: Pas cronologic: Oraș vizitat (poziția în traseu)")
    for i in range(len(best_route)):
        current = best_route[i]
        next_city = best_route[(i + 1) % len(best_route)]
        x1, y1 = cities[current]
        x2, y2 = cities[next_city]
        dist = math.hypot(x2 - x1, y2 - y1)
        print(f"Pas {i+1}: Oraș {i+1} (index original {current}) → Oraș {(i+2) if i<len(best_route)-1 else 1} (index original {next_city}), distanță: {dist:.2f}")