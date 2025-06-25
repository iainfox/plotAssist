import pandas as pd
import numpy as np
import tkinter as tk

df = pd.read_csv('example_dataframe.csv')

class Plotter(tk.Tk):
    def __init__(self, df: pd.DataFrame):
        super().__init__()
        self.df = df

        self.title("Plot Assist")
        self.geometry("700x400")

        ## Channel Selection Box, Filter Entry, and Label
        left_frame = tk.Frame(self, width=300)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        left_frame.pack_propagate(False)

        filter_label_frame = tk.Frame(left_frame)
        filter_label_frame.pack(fill=tk.X, pady=(0, 2))

        self.filter_entry = tk.Entry(filter_label_frame)
        self.filter_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        self._last_filter_text = ""
        def on_filter_entry_change(event):
            new_text = self.filter_entry.get()

            if new_text != self._last_filter_text:
                self.listbox.delete(0, tk.END)
                print("Entry changed:", new_text)

                for col in self.df.columns:
                    if new_text.lower() in col.lower():
                        self.listbox.insert(tk.END, col)
                self._last_filter_text = new_text
            else:
                pass

        self.filter_entry.bind("<KeyRelease>", on_filter_entry_change)

        list_label = tk.Label(filter_label_frame, text="Available Chanels")
        list_label.pack(side=tk.RIGHT, anchor='e')

        self.listbox = tk.Listbox(left_frame, selectmode=tk.MULTIPLE, activestyle='none')
        self.listbox.pack(fill=tk.BOTH, expand=True)
        ## ↓ adds data ↓
        for col in self.df.columns:
            self.listbox.insert(tk.END, col)

        # Create a second (right) listbox, initially empty
        right_frame = tk.Frame(self, width=300)
        right_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        right_frame.pack_propagate(False)

        selected_label = tk.Label(right_frame, text="Selected Channels")
        selected_label.pack(anchor='w')

        self.selected_listbox = tk.Listbox(right_frame, selectmode=tk.MULTIPLE, activestyle='none')
        self.selected_listbox.pack(fill=tk.BOTH, expand=True)
        # self.selected_listbox.insert(tk.END, "column_name")
            
        ## Middle Column with Buttons
        middle_frame = tk.Frame(self)
        middle_frame.pack(side=tk.LEFT, fill=tk.Y, pady=10, before=right_frame)
        
        top_frame = tk.Frame(middle_frame)
        top_frame.pack(fill=tk.X, pady=20)
        
        bottom_frame = tk.Frame(middle_frame)
        bottom_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        right_buttons = [">>", "[>>]", ">", "[>]"]
        for i, label in enumerate(right_buttons):
            button = tk.Button(top_frame, text=label, width=3)
            button.pack(pady=1)
            button.config(command=lambda btn=button, idx=i: self.buttonClick(btn, idx))
        
        left_buttons = ["↑", "↓", "<", "<<"]
        for i, label in enumerate(left_buttons):
            button = tk.Button(bottom_frame, text=label, width=3)
            button.pack(pady=1)
            button.config(command=lambda btn=button, idx=i+len(right_buttons): self.buttonClick(btn, idx))

    def buttonClick(self, button, index):
        def get_visible_left_items():
            return [self.listbox.get(i) for i in range(self.listbox.size())]

        def get_selected_items(listbox):
            return [listbox.get(i) for i in listbox.curselection()]

        def remove_items_from_listbox(listbox, items):
            indices = []
            for i in range(listbox.size()):
                if listbox.get(i) in items:
                    indices.append(i)
            for i in reversed(indices):
                listbox.delete(i)

        def add_items_to_listbox(listbox, items):
                for item in items:
                    listbox.insert(tk.END, item)

        def get_previous_group():
            max_group = 0
            for i in range(self.selected_listbox.size()):
                item = self.selected_listbox.get(i)
                left = item.rfind('[')
                right = item.rfind(']')
                if left != -1 and right != -1 and right > left + 1:
                    num_str = item[left+1:right]
                    if num_str.isdigit():
                        group_num = int(num_str)
                        if group_num > max_group:
                            max_group = group_num
            return max_group
        match index:
            case 0:  # ">>"
                visible = get_visible_left_items()
                if visible:
                    group_num = get_previous_group() + 1
                    items_with_group = [f"{item} [{group_num+i}]" for item in visible]
                    add_items_to_listbox(self.selected_listbox, items_with_group)
            case 1:  # "[>>]"
                visible = get_visible_left_items()
                if visible:
                    group_num = get_previous_group() + 1
                    items_with_group = [f"{item} [{group_num}]" for item in visible]
                    add_items_to_listbox(self.selected_listbox, items_with_group)
            case 2:  # ">"
                selected = get_selected_items(self.listbox)
                if selected:
                    group_num = get_previous_group() + 1
                    items_with_group = [f"{item} [{group_num+i}]" for i, item in enumerate(selected)]
                    add_items_to_listbox(self.selected_listbox, items_with_group)
            case 3:  # "[>]"
                selected = get_selected_items(self.listbox)
                if selected:
                    group_num = get_previous_group() + 1
                    items_with_group = [f"{item} [{group_num}]" for item in selected]
                    add_items_to_listbox(self.selected_listbox, items_with_group)
            case 4:  # "↑"
                lb = self.selected_listbox
                sel = lb.curselection()
                if not sel:
                    return
                for i in sel:
                    if i == 0:
                        continue
                    item = lb.get(i)
                    lb.delete(i)
                    lb.insert(i-1, item)
                    lb.selection_set(i-1)
                    lb.selection_clear(i)
            case 5:  # "↓"
                lb = self.selected_listbox
                sel = list(lb.curselection())
                if not sel:
                    return
                for i in reversed(sel):
                    if i == lb.size() - 1:
                        continue
                    item = lb.get(i)
                    lb.delete(i)
                    lb.insert(i+1, item)
                    lb.selection_set(i+1)
                    lb.selection_clear(i)
            case 6:  # "<"
                selected = get_selected_items(self.selected_listbox)
                if selected:
                    items_to_move = []
                    for item in selected:
                        if item.startswith("[") and item.endswith("]"):
                            items = [x.strip() for x in item[1:-1].split(",")]
                            items_to_move.extend(items)
                        else:
                            items_to_move.append(item)
                    remove_items_from_listbox(self.selected_listbox, selected)
            case 7:  # "<<"
                all_items = [self.selected_listbox.get(i) for i in range(self.selected_listbox.size())]
                if all_items:
                    items_to_move = []
                    for item in all_items:
                        if item.startswith("[") and item.endswith("]"):
                            items = [x.strip() for x in item[1:-1].split(",")]
                            items_to_move.extend(items)
                        else:
                            items_to_move.append(item)
                    self.selected_listbox.delete(0, tk.END)
            case _:
                print(f"Unknown button index: {index}")
def plot_assist(df):
    app = Plotter(df)
    app.mainloop()

plot_assist(df)