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
        
        self.listbox.bind('<<ListboxSelect>>', self.on_select)

        self.listbox.select_set(0)
        self.on_select(None)

    def on_select(self, event):
        # self.listbox.get(i)
        selection_indices = self.listbox.curselection()

def plot_assist(df):
    app = Plotter(df)
    app.mainloop()

plot_assist(df)