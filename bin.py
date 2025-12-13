import random
import time
import matplotlib.pyplot as plt
from collections import Counter

# --- 1. Evaluation Function ---
def evaluate(solution, capacity):
    """
    Standard First Fit heuristic.
    Returns: (number of bins used, list of bins)
    """
    bins = []
    for obj in solution:
        placed = False
        for b in bins:
            if sum(b) + obj <= capacity:
                b.append(obj)
                placed = True
                break
        if not placed:
            bins.append([obj])
    return len(bins), bins


def random_solution(objects):
    """Generates a random permutation of objects."""
    sol = objects[:]
    random.shuffle(sol)
    return sol


# --- 2. Mutation Strategies ---
def mutation_standard(solution):
    """Strategy A: Standard Random Swap or Insert."""
    new = solution[:]
    if random.random() < 0.5:
        # Swap two items
        i, j = random.sample(range(len(new)), 2)
        new[i], new[j] = new[j], new[i]
    else:
        # Move an item
        idx = random.randint(0, len(new) - 1)
        item = new.pop(idx)
        insert_pos = random.randint(0, len(new))
        new.insert(insert_pos, item)
    return new


def mutation_inversion(solution):
    """Strategy B: Inversion Mutation (Reverse a segment)."""
    new = solution[:]
    i, j = sorted(random.sample(range(len(new)), 2))
    new[i:j+1] = new[i:j+1][::-1]
    return new


# --- 3. Crossover Operator ---
def crossover(parent1, parent2):
    """
    Order Crossover (OX1) using Counter.
    Ensures no duplicates are created.
    """
    size = len(parent1)
    idx1, idx2 = sorted(random.sample(range(size), 2))
    
    child = [None] * size
    child[idx1:idx2] = parent1[idx1:idx2]
    
    counts_in_child = Counter(child[idx1:idx2])
    
    needed_items = []
    for item in parent2:
        if counts_in_child[item] > 0:
            counts_in_child[item] -= 1
        else:
            needed_items.append(item)

    needed_index = 0
    for i in range(size):
        if child[i] is None:
            child[i] = needed_items[needed_index]
            needed_index += 1
            
    return child


# --- 4. Cultural Algorithm Core ---
def cultural_algorithm(objects, capacity, pop_size=50, generations=200, 
            mutation_type="standard", selection_type="top50"):
    """
    Main Loop with configurable strategies.
    """
    population = [random_solution(objects) for _ in range(pop_size)]

    situational_best_solution = None
    situational_best_bins = float("inf")
    
    history_best = []
    history_avg = []

    print(f"Starting Evolution (Gen: {generations}, Pop: {pop_size})...")
    print(f"Strategy: Mutation='{mutation_type}', Selection='{selection_type}'")

    for gen in range(generations):
        # --- Evaluation ---
        evaluated = []
        gen_scores = []
        
        for sol in population:
            score, _ = evaluate(sol, capacity)
            evaluated.append((sol, score))
            gen_scores.append(score)
        
        evaluated.sort(key=lambda x: x[1])
        best_sol_gen, best_score_gen = evaluated[0]
        
        # --- Update Belief Space ---
        if best_score_gen < situational_best_bins:
            situational_best_bins = best_score_gen
            situational_best_solution = best_sol_gen[:]
            print(f"Gen {gen}: New Best Found -> {situational_best_bins} bins")
        
        # Record Data
        history_best.append(situational_best_bins)
        avg_score = sum(gen_scores) / len(gen_scores)
        history_avg.append(avg_score)

        # --- Reproduction ---
        # Normative Knowledge (Acceptance bound)
        top_half = gen_scores[:len(gen_scores)//2]
        norm_max = max(top_half)

        new_population = []
        new_population.append(situational_best_solution) # Elitism

        while len(new_population) < pop_size:
            
            # --- SELECTION ---
            if selection_type == "tournament":
                # Tournament: Pick 5, take best
                candidates_a = random.sample(evaluated, 5)
                parent_a = min(candidates_a, key=lambda x: x[1])[0]
                
                candidates_b = random.sample(evaluated, 5)
                parent_b = min(candidates_b, key=lambda x: x[1])[0]
            else:
                # Top 50% Random
                if random.random() < 0.6:
                    parent_a = situational_best_solution
                else:
                    parent_a = evaluated[random.randint(0, len(evaluated)//4)][0]
                
                parent_b = evaluated[random.randint(0, len(evaluated)//2)][0]

            # --- CROSSOVER ---
            child = crossover(parent_a, parent_b)
            
            # --- MUTATION ---
            if random.random() < 0.3: 
                if mutation_type == "inversion":
                    child = mutation_inversion(child)
                else:
                    child = mutation_standard(child)
            
            # --- ACCEPTANCE ---
            child_score, _ = evaluate(child, capacity)
            if child_score <= norm_max + 2: 
                new_population.append(child)
        
        population = new_population

    return situational_best_solution, situational_best_bins, history_best, history_avg


def plot_data(history_best, history_avg):
    plt.figure(figsize=(10, 6))
    plt.plot(history_best, label='Best Bins (Situational)', color='red', linewidth=2)
    plt.plot(history_avg, label='Avg Bins per Gen', color='black', linestyle='--', alpha=0.5)
    plt.ylabel('Bins Used')
    plt.xlabel('Generations')
    plt.title('Cultural Algorithm Convergence')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def main():
    try:
        # capacity = 50
        # n = 150                                       #If u want large random numbers
        # print(f"Generating {n} random objects...")
        # objects = [random.randint(10, 50) for _ in range(n)]
        capacity = int(input("Enter max bin capacity: "))
        while capacity < 2:
            print("capacity must be MORE than 1. Try again.")
            capacity = int(input(f"Enter max bin capacity: "))
        n = int(input("Enter number of objects: "))
        objects = []
        for i in range(n):
            size = int(input(f"Enter size of object {i+1}: "))
            while size > capacity:
                print("Size must be LESS than capacity. Try again.")
                size = int(input(f"Enter size of object {i+1}: "))
            objects.append(size)

        print("\n    Configuration Options")
        pop_in = input("Population Size (default 50): ").strip()
        gen_in = input("Generations (default 200): ").strip()
        
        print("\nSelect Mutation Strategy:")
        print("1. Standard (Swap/Insert) - Default")
        print("2. Inversion (Reverse Segment)")
        mut_in = input("Choice (1/2): ").strip()
        
        print("\nSelect Parent Selection Strategy:")
        print("1. Top 50% Random - Default")
        print("2. Tournament Selection")
        sel_in = input("Choice (1/2): ").strip()

        pop_size = int(pop_in) if pop_in else 50
        gens = int(gen_in) if gen_in else 200
        
        mut_type = "inversion" if mut_in == "2" else "standard"
        sel_type = "tournament" if sel_in == "2" else "top50"

        start_time = time.time()
        
        best_sol, bins_used, hist_best, hist_avg = cultural_algorithm(
            objects, capacity, 
            pop_size=pop_size, 
            generations=gens,
            mutation_type=mut_type,
            selection_type=sel_type
        )
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        _, bins = evaluate(best_sol, capacity)

        print(f"\nTime: {elapsed:.4f} sec")
        print("RESULT")
        print(f"Bins Used: {bins_used}\n")
        
        for i, b in enumerate(bins):
            total_load = sum(b)
            fullness = (total_load / capacity) * 100
            print(f"Bin {i+1}: {b} (Load: {total_load}/{capacity} -> {fullness:.1f}% Full)")

        print("\nDisplaying plot...")
        plot_data(hist_best, hist_avg)

    except ValueError:
        print("Invalid Input. Please enter numbers.")

if __name__ == "__main__":
    main()
