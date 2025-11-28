import random


def evaluate(solution, capacity):
    """Evaluate how many bins are needed for a given ordering of objects.
    Each object is placed in the first bin that has enough remaining space.
    Returns: (num of bins used, list of bins)"""
    
    bins = []

    for obj in solution:
        placed = False

        for b in bins:        # Try to place object in an existing bin

            if sum(b) + obj <= capacity:
                b.append(obj)
                placed = True
                break

    
        if not placed:  # If it cannot fit in any existing bin -> create a new bin
            bins.append([obj])

    return len(bins), bins



def random_solution(objects):
    """
    Creates a random ordering (permutation) of the objects.
    This represents one candidate solution.
    """
    sol = objects[:]
    random.shuffle(sol)
    return sol



def mutate(solution, capacity):
    """
    Performs mutation on a solution.
    Two types:
      1. Swap two objects.
      2. Remove an object and insert it somewhere else.
    """
    new = solution[:]

    if random.random() < 0.5:# Swap mutation
        i, j = random.sample(range(len(new)), 2)
        new[i], new[j] = new[j], new[i]
    else:# Move mutation: remove then reinsert in random position
        idx = random.randint(0, len(new) - 1)
        item = new.pop(idx)
        insert_pos = random.randint(0, len(new))
        new.insert(insert_pos, item)
    return new



def cultural_algorithm(objects, capacity, population_size=40, generations=200):
    """
    Cultural Algorithm has:
        - Population Space: 
           normal evolutionary solutions.
        - Belief Space:
           Situational knowledge: best solution found.
           Normative knowledge: allowed range of bin usage.

    Algorithm steps:
        1- Initialize population.
        2- Evaluate.
        3- Update belief space.
        4- Create new population influenced by the belief space.
        5- Repeat.
    """
    population = [random_solution(objects) for _ in range(population_size)]    # 1. Create the initial population

    # Belief Space
    situational_best_solution = None         # Best found ordering
    situational_best_bins = float("inf")     # Best found number of bins

    normative_min_bin = float("inf")         # Lower limit of accepted results
    normative_max_bin = float("-inf")        # Upper limit

    # Main Evolution Loop
    for gen in range(generations):

        # Evaluate each solution in the population
        evaluated = []
        for sol in population:
            bins_used, bins = evaluate(sol, capacity)
            evaluated.append((sol, bins_used, bins))

        evaluated.sort(key=lambda x: x[1])        # Sort population by best (least bins)

        best_sol, best_bin_count, best_bins = evaluated[0]        # Get best solution in this generation

        # Update Situational Knowledge Keep the *best* solution found so far
        if best_bin_count < situational_best_bins:
            situational_best_solution = best_sol[:]
            situational_best_bins = best_bin_count

        # Update Normative Knowledge Update acceptable min/max bin usage
        normative_min_bin = min(normative_min_bin, best_bin_count)
        normative_max_bin = max(normative_max_bin, best_bin_count)

        # Create new population influenced by the belief space
        new_population = []
        for _ in range(population_size):

            if random.random() < 0.5:
                # Exploitation: mutate the best solution
                child = mutate(situational_best_solution, capacity)
            else:
                # Exploration: random fresh solution
                child = random_solution(objects)

            # Cultural influence:
            # Accept child only if it falls within the normative range
            child_bins, _ = evaluate(child, capacity)
            if normative_min_bin <= child_bins <= normative_max_bin:
                new_population.append(child)
            else:
                # Outside cultural norms → mutate again
                new_population.append(mutate(child, capacity))

        population = new_population 
    return situational_best_solution, situational_best_bins    # Return best solution found after all generations





def main():
    capacity = int(input("Enter max bin capacity: "))
    n = int(input("Enter number of objects: "))
    objects = []
    for i in range(n):
        size = int(input(f"Enter size of object {i+1}: "))

        # Ensure item is not larger than bin capacity
        while size > capacity:
            print("Size must be LESS than capacity. Try again.")
            size = int(input(f"Enter size of object {i+1}: "))
        objects.append(size)

    best_sol, bins_used = cultural_algorithm(objects, capacity)    # Run Cultural Algorithm

    _, bins = evaluate(best_sol, capacity)    # Build final bin packing for display


    print("RESULT\n")
    print(f"Best Sequence (order): {best_sol}")
    print(f"Bins Used: {bins_used}\n")
    for i, b in enumerate(bins):
        print(f"Bin {i+1}: {b}  (total = {sum(b)})")


# main()
