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
        right_frame = tk.Frame(self, width=300, height=350)
        right_frame.pack(side=tk.LEFT, padx=10, pady=10, anchor='n')
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
        if not hasattr(self, "selected_items_meta"):
            self.selected_items_meta = []

        def sync_listbox_with_meta():
            self.selected_listbox.delete(0, tk.END)
            for item in self.selected_items_meta:
                self.selected_listbox.insert(tk.END, f"{item['name']} [{item['group']}]")

        def get_visible_left_items():
            return [self.listbox.get(i) for i in range(self.listbox.size())]

        def get_selected_items(listbox):
            return [listbox.get(i) for i in listbox.curselection()]

        def get_selected_meta_indices():
            return list(self.selected_listbox.curselection())

        def get_next_group_number():
            if not self.selected_items_meta:
                return 1
            return max(item['group'] for item in self.selected_items_meta) + 1

        match index:
            case 0:  # ">>"
                visible = get_visible_left_items()
                if visible:
                    group_num = get_next_group_number()
                    for i, item in enumerate(visible):
                        self.selected_items_meta.append({'name': item, 'group': group_num + i})
                    sync_listbox_with_meta()

            case 1:  # "[>>]"
                visible = get_visible_left_items()
                if visible:
                    group_num = get_next_group_number()
                    for item in visible:
                        self.selected_items_meta.append({'name': item, 'group': group_num})
                    sync_listbox_with_meta()

            case 2:  # ">"
                selected = get_selected_items(self.listbox)
                if selected:
                    group_num = get_next_group_number()
                    for i, item in enumerate(selected):
                        self.selected_items_meta.append({'name': item, 'group': group_num + i})
                    sync_listbox_with_meta()

            case 3:  # "[>]"
                selected = get_selected_items(self.listbox)
                if selected:
                    group_num = get_next_group_number()
                    for item in selected:
                        self.selected_items_meta.append({'name': item, 'group': group_num})
                    sync_listbox_with_meta()

            case 4:  # "↑"
                sel = get_selected_meta_indices()
                if not sel:
                    return
                for i in sel:
                    if i == 0:
                        continue
                    self.selected_items_meta[i-1], self.selected_items_meta[i] = self.selected_items_meta[i], self.selected_items_meta[i-1]
                sync_listbox_with_meta()
                for i in [s-1 for s in sel if s > 0]:
                    self.selected_listbox.selection_set(i)

            case 5:  # "↓"
                sel = get_selected_meta_indices()
                if not sel:
                    return
                for i in reversed(sel):
                    if i == len(self.selected_items_meta) - 1:
                        continue
                    self.selected_items_meta[i], self.selected_items_meta[i+1] = self.selected_items_meta[i+1], self.selected_items_meta[i]
                sync_listbox_with_meta()
                for i in [s+1 for s in sel if s < len(self.selected_items_meta)-1]:
                    self.selected_listbox.selection_set(i)

            case 6:  # "<"
                sel = get_selected_meta_indices()
                if sel:
                    for i in reversed(sel):
                        del self.selected_items_meta[i]
                    sync_listbox_with_meta()

            case 7:  # "<<"
                self.selected_items_meta.clear()
                sync_listbox_with_meta()
            case _:
                print(f"Unknown button index: {index}")
def plot_assist(df):
    app = Plotter(df)
    app.mainloop()

plot_assist(df)