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

        ## Channel Selection Box and Label
        left_frame = tk.Frame(self, width=300)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        left_frame.pack_propagate(False)
        
        list_label = tk.Label(left_frame, text="Available Chanels")
        list_label.pack(anchor='w')

        self.listbox = tk.Listbox(left_frame, selectmode=tk.MULTIPLE, activestyle='none')
        self.listbox.pack(fill=tk.BOTH, expand=True)
        ## ↓ adds data ↓
        for col in self.df.columns:
            self.listbox.insert(tk.END, col)

        ## Middle Column with Buttons
        middle_frame = tk.Frame(self)
        middle_frame.pack(side=tk.LEFT, fill=tk.Y, pady=10)
        
        top_frame = tk.Frame(middle_frame)
        top_frame.pack(fill=tk.X, pady=20)
        
        bottom_frame = tk.Frame(middle_frame)
        bottom_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        right_buttons = [">>", "[>>]", ">", "[>]"]
        self.right_buttons = []
        for i, label in enumerate(right_buttons):
            button = tk.Button(top_frame, text=label, width=4, height=2)
            button.pack(pady=1)
            button.config(command=lambda btn=button, idx=i: self.buttonClick(btn, idx))
            self.right_buttons.append(button)
        
        left_buttons = ["<", "<<"]
        self.left_buttons = []
        for i, label in enumerate(left_buttons):
            button = tk.Button(bottom_frame, text=label, width=4, height=2)
            button.pack(pady=1)
            button.config(command=lambda btn=button, idx=i+len(right_buttons): self.buttonClick(btn, idx))
            self.left_buttons.append(button)

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