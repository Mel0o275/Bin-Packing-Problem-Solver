# number of items       
n_items = int(input("enter # of bins : "))
items = []
# list of items
for i in range(n_items):
    size = int(input(f"Item {i+1} size: "))
    items.append(size)
# bin capacity
bin_capacity = int(input("enter bin capacity : "))
# sort
items.sort(reverse=True)
# list of best solution bin
best_bins = 10**9
best_solution = []

# backtracking function
def backtracking(index, current_bins):
    global best_bins, best_solution
    if index == len(items):
        if len(current_bins) < best_bins:
            best_bins = len(current_bins)
            best_solution = [bin.copy() for bin in current_bins]
        return
    item = items[index]
    for i in current_bins:
        if sum(i) + item <= bin_capacity:
            i.append(item)
            backtracking(index + 1, current_bins)
            i.pop()
    if(len(current_bins) + 1 < best_bins):
        new_bin =[item]
        current_bins.append(new_bin)
        backtracking(index + 1, current_bins)
        current_bins.remove(new_bin)
backtracking(0, [])
print("\nBest number of bins:", best_bins)
print("Best Solution:", best_solution)