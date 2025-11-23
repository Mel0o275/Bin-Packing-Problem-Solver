def bin_packing_backtrack_2d(items, bins, bin_capacity, index, best_solution):
    if index == len(items):

        if best_solution[0] == -1 or len(bins) < best_solution[0]:
            best_solution[0] = len(bins)
            best_solution[1] = [bin[:] for bin in bins]  
            # print(best_solution , "MAlak")
            # print(bins , "Moka")
        return
    
    if best_solution[0] != -1 and len(bins) >= best_solution[0]:
        return

    item = items[index]

    for i in range(len(bins)):
        if sum(bins[i]) + item <= bin_capacity:
            bins[i].append(item)
            bin_packing_backtrack_2d(items, bins, bin_capacity, index+1, best_solution)
            print(bins[i], "=" * 60)
            bins[i].pop()  

  
    bins.append([item])
    # print(bins, "+" * 60)
    bin_packing_backtrack_2d(items, bins, bin_capacity, index+1, best_solution)
    bins.pop()  
    # print(bins,"after pop", "+" * 60)


items_input = input("Enter items separated by space: ")
items = list(map(int, items_input.split()))

bin_capacity = int(input("Enter bin capacity: "))

items.sort(reverse=True)

best_solution = [-1, []]

bin_packing_backtrack_2d(items, [], [], bin_capacity, 0, best_solution)

print("\nSorted items (descending):", items)
print("Minimum number of bins:", best_solution[0])
print("Bins content:")

for i, b in enumerate(best_solution[1], 1):
    print(f"Bin {i}: {b}")