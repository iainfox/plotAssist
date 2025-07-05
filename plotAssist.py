import pandas as pd
import tkinter as tk
import tkinter.ttk as ttk
import matplotlib.pyplot as plt

df = pd.read_csv('example_dataframe.csv')

class Plotter(tk.Tk):
    def __init__(self, df: pd.DataFrame):
        super().__init__()
        self.df = df

        self.title("Plot Assist")
        self.geometry("1050x400")

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

        self.listbox = tk.Listbox(left_frame, selectmode=tk.EXTENDED, activestyle='none')
        self.listbox.pack(fill=tk.BOTH, expand=True)
        
        self.listbox.insert(tk.END, *sorted(self.df.columns))

        right_frame = tk.Frame(self, width=300)
        right_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10, anchor='n')
        right_frame.pack_propagate(False)

        selected_label = tk.Label(right_frame, text="Selected Channels")
        selected_label.pack(anchor='w')

        self.selected_listbox = tk.Listbox(right_frame, selectmode=tk.EXTENDED, activestyle='none')
        self.selected_listbox.pack(fill=tk.BOTH, expand=True)

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
            button.config(command=lambda btn=button, idx=i: self.buttonClick(idx))
        
        left_buttons = ["↑", "↓", "<", "<<"]
        for i, label in enumerate(left_buttons):
            button = tk.Button(bottom_frame, text=label, width=3)
            button.pack(pady=1)
            button.config(command=lambda btn=button, idx=i+len(right_buttons): self.buttonClick(idx))

        settings_frame = tk.Frame(self, width=350)
        settings_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10, anchor='n')
        settings_frame.pack_propagate(False)

        highlight_frame = tk.Frame(settings_frame, bd=1, relief="flat", highlightbackground="black", highlightcolor="black", highlightthickness=1)
        highlight_frame.pack(fill=tk.BOTH, expand=True)

        top_row = tk.Frame(highlight_frame)
        top_row.pack(anchor='nw', pady=(8, 4), padx=8, fill=tk.X)

        highlight_label = tk.Label(top_row, text="Highlight", font=("Arial", 10, "bold"))
        highlight_label.pack(side=tk.LEFT)
 
        self.highlight_channel_var = tk.StringVar(value="None")
        self.highlight_channel_dropdown = ttk.Combobox(
            top_row, textvariable=self.highlight_channel_var, state="readonly", width=25, values=["None"] + sorted(self.df.columns)
        )
        self.highlight_channel_dropdown.pack(side=tk.LEFT, padx=(8, 0))

        self.highlight_filter_entry = tk.Entry(top_row)
        self.highlight_filter_entry.insert(0, "Search channels...")
        self.highlight_filter_entry.pack(side=tk.LEFT, padx=(8, 0), fill=tk.X, expand=True)

        self._last_highlight_filter_text = ""
        def on_highlight_filter_entry_change(event):
            new_text = self.highlight_filter_entry.get().strip()

            if new_text != self._last_highlight_filter_text:
                current_values = ["None"]
                
                if new_text == "":
                    current_values.extend(sorted(self.df.columns))
                else:
                    for col in self.df.columns:
                        if new_text.lower() in col.lower():
                            current_values.append(col)
                
                self.highlight_channel_dropdown['values'] = current_values
                self._last_highlight_filter_text = new_text

        self.highlight_filter_entry.bind("<KeyRelease>", on_highlight_filter_entry_change)

        filter_row = tk.Frame(highlight_frame)
        filter_row.pack(anchor='nw', pady=(8, 4), padx=8, fill=tk.X)

        filter_modes = ["==", ">=", "<=", ">", "<"]
        filter_mode_var = tk.StringVar(value="==")
        filter_mode_dropdown = ttk.Combobox(filter_row, textvariable=filter_mode_var, values=filter_modes, state="readonly", width=4)
        filter_mode_dropdown.pack(side=tk.LEFT)

        value_var = tk.StringVar(value="1")
        value_entry = tk.Entry(filter_row, textvariable=value_var, width=10)
        value_entry.pack(side=tk.LEFT, padx=(6, 0))

        color_values = {
            "red": "#FF0000",
            "orange": "#FFA500",
            "green": "#00FF00",
            "blue": "#0000FF",
            "magenta": "#FF00FF",
            "cyan": "#00FFFF",
            "yellow": "#FFFF00",
        }

        color_var = tk.StringVar(value="red")
        color_dropdown = ttk.Combobox(filter_row, textvariable=color_var, values=list(color_values.keys()), state="readonly", width=8)
        color_dropdown.pack(side=tk.LEFT, padx=(6, 0))

        plot_btn_frame = tk.Frame(right_frame)
        plot_btn_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(3, 1))

        def highlight(ax, data):
            if self.highlight_channel_var.get() in (None, "", "None"):
                return
            if filter_mode_var.get() not in filter_modes:
                return
            if value_var.get() in (None, ""):
                return
            try:
                float(value_var.get())
            except ValueError:
                return

            fm = filter_mode_var.get()
            val = float(value_var.get())
            color = color_values[color_var.get()]

            match fm:
                case "==":
                    highlighting = False
                    start = None
                    for i, v in enumerate(data):
                        if v == val and not highlighting:
                            highlighting = True
                            start = i
                        elif v != val and highlighting:
                            highlighting = False
                            ax.axvspan(start, i, color=color, alpha=0.5)
                    if highlighting and start is not None:
                        ax.axvspan(start, len(data), color=color, alpha=0.5)
                case ">=": 
                    highlighting = False
                    start = None
                    for i, v in enumerate(data):
                        if v >= val and not highlighting:
                            highlighting = True
                            start = i
                        elif v < val and highlighting:
                            highlighting = False
                            ax.axvspan(start, i, color=color, alpha=0.5)
                    if highlighting and start is not None:
                        ax.axvspan(start, len(data), color=color, alpha=0.5)
                case "<=":
                    highlighting = False
                    start = None
                    for i, v in enumerate(data):
                        if v <= val and not highlighting:
                            highlighting = True
                            start = i
                        elif v > val and highlighting:
                            highlighting = False
                            ax.axvspan(start, i, color=color, alpha=0.5)
                    if highlighting and start is not None:
                        ax.axvspan(start, len(data), color=color, alpha=0.5)
                case ">":
                    highlighting = False
                    start = None
                    for i, v in enumerate(data):
                        if v > val and not highlighting:
                            highlighting = True
                            start = i
                        elif v <= val and highlighting:
                            highlighting = False
                            ax.axvspan(start, i, color=color, alpha=0.5)
                    if highlighting and start is not None:
                        ax.axvspan(start, len(data), color=color, alpha=0.5)
                case "<":
                    highlighting = False
                    start = None
                    for i, v in enumerate(data):
                        if v < val and not highlighting:
                            highlighting = True
                            start = i
                        elif v >= val and highlighting:
                            highlighting = False
                            ax.axvspan(start, i, color=color, alpha=0.5)
                    if highlighting and start is not None:
                        ax.axvspan(start, len(data), color=color, alpha=0.5)

        def plot():
            if not hasattr(self, "selected_items_meta") or not self.selected_items_meta:
                return

            from collections import defaultdict
            groups = defaultdict(list)
            for item in self.selected_items_meta:
                groups[item['group']].append(item['name'])

            sorted_groups = sorted(groups.items(), key=lambda x: x[0])

            n_groups = len(sorted_groups)
            fig, axes = plt.subplots(n_groups, 1, sharex=True, sharey=False, figsize=(8, 2.5 * n_groups), constrained_layout=True)
            if n_groups == 1:
                axes = [axes]

            for ax_idx, (group_num, channel_names) in enumerate(sorted_groups):
                ax = axes[ax_idx]
                for channel in channel_names:
                    if channel not in self.df.columns:
                        continue
                    ax.plot(self.df.index, self.df[channel], label=channel, linewidth=2)

                ax.grid(True, which='both', linestyle='--', alpha=0.6)
                ax.set_ylabel(f"Group {group_num}")
                ax.legend(loc='upper right', fontsize=8)
                if ax_idx != 0:
                    ax.spines['top'].set_visible(False)

                highlight(ax, self.df[channel])

            axes[-1].set_xlabel("Index")
            plt.show()

        plot_btn = tk.Button(plot_btn_frame, text="Plot", command=plot)
        plot_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def update_highlight_dropdown(self, event=None):
            items = [self.selected_listbox.get(i) for i in range(self.selected_listbox.size())]
            values = ["None"] + items
            current = self.highlight_channel_var.get()
            self.highlight_channel_dropdown['values'] = values
            if current not in values:
                self.highlight_channel_var.set("None")

    def buttonClick(self, index):
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
                    self.update_highlight_dropdown()

            case 1:  # "[>>]"
                visible = get_visible_left_items()
                if visible:
                    group_num = get_next_group_number()
                    for item in visible:
                        self.selected_items_meta.append({'name': item, 'group': group_num})
                    sync_listbox_with_meta()
                    self.update_highlight_dropdown()

            case 2:  # ">"
                selected = get_selected_items(self.listbox)
                if selected:
                    group_num = get_next_group_number()
                    for i, item in enumerate(selected):
                        self.selected_items_meta.append({'name': item, 'group': group_num + i})
                    sync_listbox_with_meta()
                    self.update_highlight_dropdown()

            case 3:  # "[>]"
                selected = get_selected_items(self.listbox)
                if selected:
                    group_num = get_next_group_number()
                    for item in selected:
                        self.selected_items_meta.append({'name': item, 'group': group_num})
                    sync_listbox_with_meta()
                    self.update_highlight_dropdown()

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
                    self.update_highlight_dropdown()

            case 7:  # "<<"
                self.selected_items_meta.clear()
                sync_listbox_with_meta()
                self.update_highlight_dropdown()
            case _:
                print(f"Unknown button index: {index}")

def plot_assist(df):
    app = Plotter(df)
    app.mainloop()

if __name__ == "__main__":
    plot_assist(df)