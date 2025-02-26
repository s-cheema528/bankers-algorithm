import tkinter as tk
from tkinter import ttk, messagebox


class BankersApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Banker's Algorithm")
        self.create_input_widgets()

    def create_input_widgets(self):
        # Main input frame
        self.input_frame = ttk.Frame(self.root, padding=10)
        self.input_frame.pack(fill='both', expand=True)

        ttk.Label(self.input_frame, text="Available Resources (R1 R2 R3):").grid(row=0, column=0, sticky='w', pady=5)
        self.avail_entries = []
        for i in range(3):
            entry = ttk.Entry(self.input_frame, width=5)
            entry.grid(row=0, column=i + 1, padx=2)
            self.avail_entries.append(entry)

        ttk.Label(self.input_frame, text="Processes | (Allocation Resources)   |   (Max Resources) (R1,R2,R3):").grid(row=1, column=0, columnspan=9, sticky='w', pady=5)
        self.process_container = ttk.Frame(self.input_frame)
        self.process_container.grid(row=2, column=0, columnspan=9, sticky='w')

        self.process_entries = []
        self.add_process_row()
        btn_frame = ttk.Frame(self.input_frame)
        btn_frame.grid(row=3, column=0, columnspan=9, pady=10)

        add_btn = ttk.Button(btn_frame, text="Add Process", command=self.add_process_row)
        add_btn.pack(side=tk.LEFT, padx=5)

        run_btn = ttk.Button(btn_frame, text="Run Algorithm", command=self.run_algorithm)
        run_btn.pack(side=tk.LEFT, padx=5)

        # Status label
        self.status_label = ttk.Label(self.input_frame, text="", foreground="red")
        self.status_label.grid(row=4, column=0, columnspan=9)

    def add_process_row(self):
        row = len(self.process_entries)
        entries = {}

        # Process name
        name_entry = ttk.Entry(self.process_container, width=8)
        name_entry.grid(row=row, column=0, padx=2)
        entries['name'] = name_entry

        # Allocation entries
        alloc_entries = []
        for i in range(3):
            entry = ttk.Entry(self.process_container, width=5)
            entry.grid(row=row, column=i + 1, padx=2)
            alloc_entries.append(entry)
        entries['alloc'] = alloc_entries

        # Add a spacer between Allocation and Max
        spacer = ttk.Label(self.process_container, text="   ")  # Add space here
        spacer.grid(row=row, column=4)

        # Max entries
        max_entries = []
        for i in range(3):
            entry = ttk.Entry(self.process_container, width=5)
            entry.grid(row=row, column=i + 5, padx=2)
            max_entries.append(entry)
        entries['max'] = max_entries

        self.process_entries.append(entries)

    def run_algorithm(self):
        try:
            available = [int(e.get()) for e in self.avail_entries]
            processes = []
            for entry in self.process_entries:
                name = entry['name'].get()
                alloc = [int(e.get()) for e in entry['alloc']]
                max_res = [int(e.get()) for e in entry['max']]

                if len(name) == 0:
                    raise ValueError("Process name cannot be empty")
                if any(a < 0 for a in alloc):
                    raise ValueError("Allocation values must be non-negative")
                if any(m < 0 for m in max_res):
                    raise ValueError("Max values must be non-negative")
                if any(a > m for a, m in zip(alloc, max_res)):
                    raise ValueError("Allocation cannot exceed Max")

                processes.append({
                    'name': name,
                    'allocation': alloc,
                    'max': max_res,
                    'need': [m - a for m, a in zip(max_res, alloc)]
                })

        except ValueError as e:
            self.status_label.config(text=f"Error: {str(e)}")
            return
        self.work = available.copy()
        self.finished = [False] * len(processes)
        self.safe_sequence = []

        # Create results window
        self.show_results_window(processes)

    def show_results_window(self, processes):
        # Create a new window for results
        results_window = tk.Toplevel(self.root)
        results_window.title("Banker's Algorithm Results")

        # Available resources display
        ttk.Label(results_window, text="Available Resources:", font=('Arial', 10, 'bold')).grid(row=0, column=0,
                                                                                                sticky='w')
        self.available_label = ttk.Label(results_window, text=str(self.work), font=('Arial', 10))
        self.available_label.grid(row=0, column=1, sticky='w', padx=5)

        # Process table
        columns = ('Process', 'Allocation', 'Max', 'Need')
        self.tree = ttk.Treeview(results_window, columns=columns, show='headings', height=8)
        for col in columns:
            self.tree.heading(col, text=col, anchor='w')
        self.tree.grid(row=1, column=0, columnspan=2, pady=10)

        for p in processes:
            self.tree.insert('', 'end', values=(
                p['name'],
                str(p['allocation']),
                str(p['max']),
                str(p['need'])
            ))

        # Safe sequence
        ttk.Label(results_window, text="Safe Sequence:", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky='w',
                                                                                          pady=5)
        self.sequence_label = ttk.Label(results_window, text="[]", font=('Arial', 10))
        self.sequence_label.grid(row=2, column=1, sticky='w', padx=5)

        # Control buttons
        btn_frame = ttk.Frame(results_window)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        self.next_btn = ttk.Button(btn_frame, text="Next Step", command=lambda: self.next_step(processes))
        self.next_btn.pack(side=tk.LEFT, padx=5)

        # Status bar
        self.status_bar = ttk.Label(results_window, text="Ready", foreground="blue")
        self.status_bar.grid(row=4, column=0, columnspan=2, sticky='ew')

    def next_step(self, processes):
        if len(self.safe_sequence) == len(processes):
            self.status_bar.config(text="All processes completed safely!", foreground="green")
            return

        for i, p in enumerate(processes):
            if not self.finished[i] and all(n <= w for n, w in zip(p['need'], self.work)):
                self.finished[i] = True
                self.safe_sequence.append(p['name'])
                self.work = [w + a for w, a in zip(self.work, p['allocation'])]
                self.status_bar.config(text=f"Process {p['name']} executed. New available: {self.work}",
                                       foreground="darkgreen")
                self.available_label.config(text=str(self.work))
                self.sequence_label.config(text=str(self.safe_sequence))
                return

        self.status_bar.config(text="Unsafe state detected! No safe sequence exists.", foreground="red")
        self.next_btn.config(state='disabled')


if __name__ == "__main__":
    root = tk.Tk()
    app = BankersApp(root)
    root.mainloop()
