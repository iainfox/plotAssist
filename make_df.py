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
        match index:
            case 0:  # ">>"
                pass
            case 1:  # "[>>]"
                pass
            case 2:  # ">"
                pass
            case 3:  # "[>]"
                pass
            case 4:  # "<"
                pass
            case 5:  # "<<"
                pass
            case _:
                print(f"Unknown button index: {index}")

def plot_assist(df):
    app = Plotter(df)
    app.mainloop()

plot_assist(df)