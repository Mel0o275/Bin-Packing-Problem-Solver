import tkinter as tk
from tkinter import ttk
import bin
# import BacktrackingMenna as bt
# print(bin.cultural_algorithm([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 10))
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import time

# ======================= Tkinter Setup ======================
root = tk.Tk()
root.title("Bin Packing")
root.geometry("500x550")
root.configure(bg="#f0f4f7")
root.resizable(False, False)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Make Window Centered
window_width = 500
window_height = 700
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

style = ttk.Style()
style.theme_use('default')
style.configure('TNotebook.Tab', font=('Helvetica', 10, 'bold'), padding=[10, 5])
style.configure('TNotebook', background='#f0f4f7', borderwidth=0)
style.map('TNotebook.Tab', background=[('selected', '#d1e7dd')])

# ======================= Title =============================
label = tk.Label(root, text="Welcome to the Bin Packing Application",
                    font=("Helvetica", 14, "bold"), bg="#f0f4f7", fg="#0d3b66")
label.pack(pady=20)

# ======================= Tabs ==============================
tab = ttk.Notebook(root)
tab.pack(expand=True, fill='both', padx=10, pady=5)

input_tab = ttk.Frame(tab)
run_tab = ttk.Frame(tab)
compare_tab = ttk.Frame(tab)
plot_tab = ttk.Frame(tab)

tab.add(input_tab, text='Inputs')
tab.add(run_tab, text='Run')
tab.add(compare_tab, text='Compare')
tab.add(plot_tab, text='Plot')
# ======================= Input Tab =========================
input_frame = tk.Frame(input_tab, bg="#f0f4f7", bd=1, relief="solid")
input_frame.pack(pady=10, padx=10, fill='x')

tk.Label(input_frame, text='Enter Bin Capacity:', font=("Arial", 10, "bold"),
            bg="#f0f4f7").grid(row=0, column=0, sticky='w', pady=5, padx=5)
tk.Label(input_frame, text='Enter Items (comma separated):', font=("Arial", 10, "bold"),
            bg="#f0f4f7").grid(row=1, column=0, sticky='w', pady=5, padx=5)
tk.Label(input_frame, text='Choose your Max Bins:', font=("Arial", 10, "bold"),
            bg="#f0f4f7").grid(row=2, column=0, sticky='w', pady=5, padx=5)
tk.Label(input_frame, text='Choose your Algorithm:', font=("Arial", 10, "bold"),
            bg="#f0f4f7").grid(row=3, column=0, sticky='w', pady=5, padx=5)

# =================== Culture Parameters ===================
culture_frame = tk.Frame(input_frame, bg="#f0f4f7")
culture_frame.grid(row=4, column=0, columnspan=2, sticky="w")
culture_frame.grid_remove()

tk.Label(culture_frame, text='Population Size:', font=("Arial", 10, "bold"),
         bg="#f0f4f7").grid(row=0, column=0, sticky='w', pady=5, padx=5)
pop_entry = tk.Entry(culture_frame, font=("Arial", 10), bd=2, relief="groove")
pop_entry.grid(row=0, column=1, pady=5, padx=5)
pop_entry.insert(0, "50")

tk.Label(culture_frame, text='Generations:', font=("Arial", 10, "bold"),
         bg="#f0f4f7").grid(row=1, column=0, sticky='w', pady=5, padx=5)
gen_entry = tk.Entry(culture_frame, font=("Arial", 10), bd=2, relief="groove")
gen_entry.grid(row=1, column=1, pady=5, padx=5)
gen_entry.insert(0, "200")

tk.Label(culture_frame, text='Mutation Type:', font=("Arial", 10, "bold"),
         bg="#f0f4f7").grid(row=2, column=0, sticky='w', pady=5, padx=5)
mutation_var = tk.StringVar(value="standard")
mutation_frame = tk.Frame(culture_frame, bg="#f0f4f7")
mutation_frame.grid(row=2, column=1, sticky='w')
tk.Radiobutton(mutation_frame, text="Standard",
               variable=mutation_var, value="standard",
               bg="#f0f4f7").pack(side="left")
tk.Radiobutton(mutation_frame, text="Inversion",
               variable=mutation_var, value="inversion",
               bg="#f0f4f7").pack(side="left", padx=10)

tk.Label(culture_frame, text='Selection Type:', font=("Arial", 10, "bold"),
         bg="#f0f4f7").grid(row=3, column=0, sticky='w', pady=5, padx=5)
selection_var = tk.StringVar(value="top50")
selection_frame = tk.Frame(culture_frame, bg="#f0f4f7")
selection_frame.grid(row=3, column=1, sticky='w')
tk.Radiobutton(selection_frame, text="Top 50%",
               variable=selection_var, value="top50",
               bg="#f0f4f7").pack(side="left")
tk.Radiobutton(selection_frame, text="Tournament",
               variable=selection_var, value="tournament",
               bg="#f0f4f7").pack(side="left", padx=10)

# =================== Input Entries ========================
input_tab_entry = tk.Entry(input_frame, font=("Arial", 10), bd=2, relief="groove")
input_tab_entry.grid(row=0, column=1, sticky='ew', pady=5, padx=5)
input_tab_entry.insert(0, "10")

input_tab_entry2 = tk.Entry(input_frame, font=("Arial", 10), bd=2, relief="groove")
input_tab_entry2.grid(row=1, column=1, sticky='ew', pady=5, padx=5)
input_tab_entry2.insert(0, "2,5,4,7,1,3,8")

input_tab_entry3 = tk.Entry(input_frame, font=("Arial", 10), bd=2, relief="groove")
input_tab_entry3.grid(row=2, column=1, sticky='ew', pady=5, padx=5)
input_tab_entry3.insert(0, "5")

input_frame.columnconfigure(1, weight=1)

# =================== Algorithm Selection ==================
algorithm_var = tk.StringVar(value="Backtracking")
radio_frame = tk.Frame(input_frame, bg="#f0f4f7")
radio_frame.grid(row=3, column=1, sticky='w', pady=5, padx=5)

# =================== Plot ==================
plot_frame_tab = tk.Frame(plot_tab, bg="#f0f4f7", bd=2, relief="solid")
plot_frame_tab.pack(fill="both", expand=True, padx=10, pady=10)

plot_button_compare = tk.Button(compare_tab, text="Show Plot", font=("Arial", 10, "bold"),
                                bg="#00a6fb", fg="white", bd=0, padx=10, pady=5)
plot_button_compare.pack(pady=10)
plot_button_compare.bind("<Enter>", lambda e: on_enter(e, plot_button_compare))
plot_button_compare.bind("<Leave>", lambda e: on_leave(e, plot_button_compare))

def plot_in_plot_tab(history_best, history_avg):
    for widget in plot_frame_tab.winfo_children():
        if isinstance(widget, FigureCanvasTkAgg):
            widget.get_tk_widget().destroy()

    fig = Figure(figsize=(5, 3), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(history_best, label='Best Bins', color='red', linewidth=2)
    ax.plot(history_avg, label='Avg Bins per Gen', color='black', linestyle='--', alpha=0.5)
    ax.set_ylabel('Bins Used')
    ax.set_xlabel('Generations')
    ax.set_title('Cultural Algorithm Convergence')
    ax.legend()
    ax.grid(True)

    canvas_plot = FigureCanvasTkAgg(fig, master=plot_frame_tab)
    canvas_plot.draw()
    canvas_plot.get_tk_widget().pack(fill='both', expand=True)


def show_plot_compare():
    if algorithm_var.get() != "Culture":
        compare_tab_label.config(text="Plot is available only for Culture algorithm")
        return

    items_list = [int(x.strip()) for x in input_tab_entry2.get().split(',') if x.strip()]
    bin_capacity = int(input_tab_entry.get())

    best_sol, bins_used, hist_best, hist_avg = bin.cultural_algorithm(
        items_list,
        bin_capacity,
        pop_size=int(pop_entry.get()),
        generations=int(gen_entry.get()),
        mutation_type=mutation_var.get(),
        selection_type=selection_var.get()
    )

    plot_in_plot_tab(hist_best, hist_avg)
    tab.select(plot_tab)


plot_button_compare.config(command=show_plot_compare)
def toggle_culture_inputs():
    if algorithm_var.get() == "Culture":
        culture_frame.grid()
    else:
        culture_frame.grid_remove()

tk.Radiobutton(radio_frame, text="Backtracking", variable=algorithm_var, value="Backtracking",
                bg="#f0f4f7", font=("Arial", 10), command=toggle_culture_inputs).pack(side='left', padx=(0, 10))
tk.Radiobutton(radio_frame, text="Culture", variable=algorithm_var, value="Culture",
                bg="#f0f4f7", font=("Arial", 10), command=toggle_culture_inputs).pack(side='left')

# =================== Buttons ===============================
buttons_frame = tk.Frame(input_frame, bg="#f0f4f7")
buttons_frame.grid(row=8, column=0, columnspan=2, pady=10)

def on_enter(e, button):
    button['bg'] = '#0d3b66'
    button['fg'] = 'white'

def on_leave(e, button):
    button['bg'] = '#00a6fb'
    button['fg'] = 'white'

compare_button = tk.Button(buttons_frame, text='Compare Algorithms', font=("Arial", 10, "bold"),
                            bg="#00a6fb", fg="white", bd=0, padx=10, pady=5)
compare_button.pack(side='left', padx=(0, 10))
compare_button.bind("<Enter>", lambda e: on_enter(e, compare_button))
compare_button.bind("<Leave>", lambda e: on_leave(e, compare_button))

start_button = tk.Button(buttons_frame, text="Start Packing", font=("Arial", 10, "bold"),
                            bg="#00a6fb", fg="white", bd=0, padx=10, pady=5)
start_button.pack(side='left')
start_button.bind("<Enter>", lambda e: on_enter(e, start_button))
start_button.bind("<Leave>", lambda e: on_leave(e, start_button))

# ======================= Run Tab ===========================
canvas_frame = tk.Frame(run_tab)
canvas_frame.pack(fill="both", expand=True, pady=10)

v_scroll = tk.Scrollbar(canvas_frame, orient="vertical")
v_scroll.pack(side="right", fill="y")

canvas = tk.Canvas(
    canvas_frame,
    width=450,
    height=370,
    bg="white",
    bd=2,
    relief="solid",
    yscrollcommand=v_scroll.set
)
canvas.pack(side="left", fill="both", expand=True)

v_scroll.config(command=canvas.yview)

run_tab_label = tk.Label(
    run_tab,
    text='Results will be provided here',
    justify='left',
    anchor='nw',
    font=("Arial", 10),
    bg="#f0f4f7",
    wraplength=450
)
run_tab_label.pack(pady=5, padx=10, fill='both', expand=True)


ITEM_COLORS = {
    1: "#FF6B6B", 2: "#4ECDC4", 3: "#45B7D1", 4: "#96CEB4",
    5: "#FFEAA7", 6: "#DDA0DD", 7: "#FFA07A", 8: "#98D8C8",
    9: "#F7DC6F", 10: "#BB8FCE"
}


def draw_items_sequential(x, y, width, height, items, capacity, bin_number, index=0, current_y=None):
    if index >= len(items):
        if not items:
            canvas.create_rectangle(x, y, x + width, y + height, outline="black", fill="#e0e0e0", width=2)
            canvas.create_text(x + width // 2, y + height // 2, text="Empty", font=("Arial", 8, "italic"))
            canvas.create_text(x + width // 2, y + height + 15, text=f"Bin {bin_number}", font=("Arial", 9, "bold"))
        return

    if current_y is None:
        current_y = y + height * 0.9

    item = items[-(index + 1)]  
    block_height = (height * 0.8) / capacity
    item_height = block_height * item
    color = ITEM_COLORS.get(item, "#CCCCCC")
    block_y = current_y - item_height

    if index == 0:
        neck_width = width // 2
        neck_x = x + (width - neck_width) // 2
        canvas.create_rectangle(neck_x, y - 20, neck_x + neck_width, y,
                                outline="black", fill="#f8f9fa", width=2)
        canvas.create_rectangle(x, y, x + width, y + height, outline="black", fill="#f8f9fa", width=2)
        canvas.create_text(x + width // 2, y + height + 15, text=f"Bin {bin_number}", font=("Arial", 9, "bold"))
        used = sum(items)
        canvas.create_text(x + width // 2, y + height + 30, text=f"{used}/{capacity}", font=("Arial", 8, "bold"))

    block = canvas.create_rectangle(x + 5, y - 50, x + width - 5, y - 50 + item_height, fill=color, outline="black")
    text = canvas.create_text(x + width // 2, y - 50 + item_height / 2, text=str(item), font=("Arial", 8, "bold"))

    def animate():
        pos = canvas.coords(block)
        if pos[1] < block_y:
            canvas.move(block, 0, 2)
            canvas.move(text, 0, 2)
            canvas.after(20, animate)
        else:
            draw_items_sequential(x, y, width, height, items, capacity, bin_number, index + 1, current_y=block_y)

    animate()

# ======================= Backtracking Algorithm ========================

def backtracking(index, current_bins):
    global best_bins, best_solution, backtracking_calls
    backtracking_calls += 1    
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


# ======================= Algorithms Data ========================
# global bins, bins_used
# print(bins_used)
#cultural
bins_used=2
bins=[[3]]

#backtracking
items = []
bin_capacity = 0
backtracking_calls = 0
# # sort
# items.sort(reverse=True)
# list of best solution bin
best_bins = 10**9
best_solution = []

STATIC_DATA = {
    "Backtracking": {
        "bins": best_solution,
        #     [
        #     {"items": [8, 2], "used": 10},
        #     {"items": [7, 3], "used": 10},
        #     {"items": [5, 4, 1], "used": 10}
        # ],
        "total_bins": best_bins,
        "calls": backtracking_calls
    },
    "Culture": {
        "bins": bins,
        #     [
        #     {"items": [2, 5, 3], "used": 10},
        #     {"items": [4, 1], "used": 5},
        #     {"items": [7], "used": 7},
        #     {"items": [8], "used": 8}
        # ],
        "total_bins": bins_used
    }
}

def backtracking_algorithm(itemsx, capacity):
    global best_bins, best_solution , items, bin_capacity, backtracking_calls
    best_bins = 10**9
    backtracking_calls = 0
    best_solution = []
    items = itemsx
    bin_capacity = capacity
    # sort
    items.sort(reverse=True)
    backtracking(0, [])
    STATIC_DATA["Backtracking"]["bins"] = best_solution
    STATIC_DATA["Backtracking"]["total_bins"] = best_bins
    STATIC_DATA["Backtracking"]["calls"] = backtracking_calls
    # print(best_bins)
    # print(best_solution)
    # print(items)
    return STATIC_DATA["Backtracking"]

def culture_algorithm(items, capacity, pop_size, generations, mutation_type, selection_type):
    global bins_used, bins

    best_sol, bins_used, hist_best, hist_avg = bin.cultural_algorithm(
        items,
        capacity,
        pop_size=pop_size,
        generations=generations,
        mutation_type=mutation_type,
        selection_type=selection_type
    )

    _, bins = bin.evaluate(best_sol, capacity)

    STATIC_DATA["Culture"]["bins"] = bins
    STATIC_DATA["Culture"]["total_bins"] = bins_used

    return STATIC_DATA["Culture"]

def culture_wrapper(items, capacity):
    return culture_algorithm(
        items,
        capacity,
        int(pop_entry.get()),
        int(gen_entry.get()),
        mutation_var.get(),
        selection_var.get()
    )


ALGORITHMS = {
    "Backtracking": backtracking_algorithm,
    "Culture": culture_wrapper
}



# ======================= Start Packing =====================
def start_packing():
    canvas.delete("all")

    bin_capacity = input_tab_entry.get()
    items = input_tab_entry2.get()
    algorithm_name = algorithm_var.get()
    max_bins = input_tab_entry3.get()

    # Validation
    # if bin_capacity < items:
    #     run_tab_label.config(text="Error: Bin capacity must be greater than item.")
    #     return
    if not bin_capacity.isdigit() or not max_bins.isdigit():
        run_tab_label.config(text="Error: Bin capacity and Max Bins must be numbers.")
        tab.select(run_tab)
        return
    try:
        items_list = [int(x.strip()) for x in items.split(',') if x.strip()]
        if not items_list:
            run_tab_label.config(text="Error: Please enter at least one item.")
            tab.select(run_tab)
            return
        for item in items_list:
            if item > int(bin_capacity):
                run_tab_label.config(text=f"Error: Item {item} exceeds bin capacity {bin_capacity}.")
                tab.select(run_tab)
                return
    except ValueError:
        run_tab_label.config(text="Error: Items must be numbers separated by commas.")
        tab.select(run_tab)
        return

    bin_capacity = int(bin_capacity)
    max_bins = int(max_bins)
    algorithm_data = ALGORITHMS[algorithm_name](items_list, bin_capacity)

    bins = algorithm_data["bins"]
    bins_needed = algorithm_data["total_bins"]

    if bins_needed < max_bins:
        bins += [[] for _ in range(max_bins - bins_needed)]
        bins_needed = max_bins

    start_x = 60
    start_y = 60
    gap_x = 100        
    gap_y = 180        
    bins_per_row = 4 

    for i, bin_data in enumerate(bins):
        row = i // bins_per_row     
        col = i % bins_per_row       

        x = start_x + col * gap_x
        y = start_y + row * gap_y

        draw_items_sequential(x, y, 50, 100, bin_data, bin_capacity, i + 1)
        canvas.update_idletasks()
        bbox = canvas.bbox("all")
        if bbox:
            canvas.config(scrollregion=(0, 0, bbox[2] + 50, bbox[3] + 50))
    result_text = (
        f"Bin Capacity: {bin_capacity}\n"
        f"Items: {items_list}\n"
        f"Algorithm Selected: {algorithm_name}\n"
        f"Bins Needed by Algorithm: {algorithm_data['total_bins']}\n"
        f"Displayed Bins: {len(bins)}\n"
    )

    if algorithm_name == "Culture":
        result_text += (
            f"\n--- Culture Algorithm Parameters ---"
            f"\nPopulation Size: {pop_entry.get()}"
            f"\nGenerations: {gen_entry.get()}"
            f"\nMutation: {mutation_var.get()}"
            f"\nSelection: {selection_var.get()}\n"
        )

    result_text += f"\nBin Contents:\n{bins}"

    run_tab_label.config(text=result_text)
    tab.select(run_tab)


start_button.config(command=start_packing)

# ======================= Compare Tab =======================
compare_tab_label = tk.Label(compare_tab, text='Compare results will be provided here',
                                justify='left', font=("Arial", 10), bg="#f0f4f7")
compare_tab_label.pack(pady=10, padx=10, fill='x')
def compare_algo():
    bin_capacity = input_tab_entry.get()
    items = input_tab_entry2.get()

    # Validation
    if not bin_capacity.isdigit():
        compare_tab_label.config(text="Error: Bin capacity must be a number.")
        tab.select(compare_tab)
        return
    try:
        items_list = [int(x.strip()) for x in items.split(',') if x.strip()]
        if not items_list:
            compare_tab_label.config(text="Error: Please enter at least one item.")
            tab.select(compare_tab)
            return
    except ValueError:
        compare_tab_label.config(text="Error: Items must be numbers separated by commas.")
        tab.select(compare_tab)
        return

    bin_capacity = int(bin_capacity)
    compare_text = ""
    # population_tree.delete(*population_tree.get_children())  # نظف الـ Treeview قبل الإضافة

    for algo_name, algo_func in ALGORITHMS.items():
        start_time = time.time()
        data = algo_func(items_list, bin_capacity)
        end_time = time.time()
        elapsed_time = end_time - start_time
        efficiency = (sum(sum(int(item) for item in bin) for bin in data['bins']) / (data['total_bins'] * bin_capacity)) * 100
        calls_info = f" (Backtracking calls: {data.get('calls', 0)})" if algo_name == "Backtracking" else ""
        compare_text += (
            f"{algo_name} Algorithm{calls_info}:\n"
            f"  - Bins Needed: {data['total_bins']}\n"
            f"  - Bin Contents: {[bin for bin in data['bins']]}\n"
            f"  - Efficiency: {efficiency:.1f}%\n"
            f"  - Execution Time: {elapsed_time:.4f} seconds\n\n"
        )
    compare_tab_label.config(text=compare_text.strip())
    tab.select(compare_tab)


compare_button.config(command=compare_algo)

# ======================= Run App ===========================
root.mainloop()
