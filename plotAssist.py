from copy import copy
import pandas as pd
import tkinter as tk
import tkinter.ttk as ttk
import matplotlib.pyplot as plt

COLORS = {
    "red": "#FF0000",
    "orange": "#FFA500",
    "green": "#00FF00",
    "blue": "#0000FF",
    "magenta": "#FF00FF",
    "cyan": "#00FFFF",
    "yellow": "#FFFF00",
}

class DataHandler():
    def __init__(self, available_channels: list[str]) -> None:
        self.available_channels = sorted(available_channels)
        self.selected_channels: list[dict[str, int]] = []
        self.current_group = 1
    
    def get_next_group(self):
        self.current_group += 1
        return self.current_group -1

    def select_channels(self, channels: list[str], keep_group = False) -> list[dict[str, int]]:
        new_channels: list[dict[str, int]] = []
        if not keep_group:
            for channel in channels:
                group = self.get_next_group()
                new_channels.append({channel: group})
        else:
            group = self.get_next_group()
            for channel in channels:
                new_channels.append({channel: group})    

        new_channels = sorted(new_channels, key=lambda x: list(x.keys())[0])
        self.selected_channels.extend(new_channels)
        return new_channels
    
    def select_all_channels(self, listbox: tk.Listbox, keep_group = False) -> list[dict[str, int]]:
        channels = list(listbox.get(0, tk.END))
        return self.select_channels(channels, keep_group)
    
    def reorder_groups(self) -> list[dict[str, int]]:
        unique_groups = sorted(set(channel_dict[list(channel_dict.keys())[0]] for channel_dict in self.selected_channels))
        group_mapping = {old_group: new_group for new_group, old_group in enumerate(unique_groups, 1)}
        
        for channel_dict in self.selected_channels:
            channel_name = list(channel_dict.keys())[0]
            channel_dict[channel_name] = group_mapping[channel_dict[channel_name]]
        
        return self.selected_channels
    
    def combine_channels(self, channels: list[str]) -> list[dict[str, int]]:
        base_group = None
        for channel_dict in self.selected_channels:
            channel_name = list(channel_dict.keys())[0]
            if channel_name in channels:
                base_group = channel_dict[channel_name]
                break
        
        if base_group is None:
            return self.selected_channels
        
        for channel_dict in self.selected_channels:
            channel_name = list(channel_dict.keys())[0]
            if channel_name in channels:
                channel_dict[channel_name] = base_group
        
        return self.reorder_groups()
    
    def split_channels(self, channels: list[str]) -> list[dict[str, int]]:
        for channel_dict in self.selected_channels:
            channel_name = list(channel_dict.keys())[0]
            if channel_name in channels:
                channel_dict[channel_name] = self.get_next_group()
        
        return self.reorder_groups()
    
    def remove_channels(self, channels: list[str]) -> list[dict[str, int]]:
        self.selected_channels = [
            channel_dict for channel_dict in self.selected_channels
            if list(channel_dict.keys())[0] not in channels
        ]
        
        return self.reorder_groups()
    
    def remove_all_channels(self, listbox) -> list[dict[str, int]]:
        visible_items = listbox.get(0, tk.END)
        
        self.selected_channels = [
            channel_dict for channel_dict in self.selected_channels
            if list(channel_dict.keys())[0] not in visible_items
        ]
        
        return self.reorder_groups()
    
    def move(self, channels: list[str], direction: str) -> list[dict[str, int]]:
        if direction not in ["up", "down"]:
            return self.selected_channels
        
        channels_to_move = []
        for channel_dict in self.selected_channels:
            channel_name = list(channel_dict.keys())[0]
            if channel_name in channels:
                channels_to_move.append((channel_name, channel_dict[channel_name]))
        
        if not channels_to_move:
            return self.selected_channels
        
        all_groups = sorted(set(channel_dict[list(channel_dict.keys())[0]] for channel_dict in self.selected_channels))
        
        if direction == "up":
            for channel_name, current_group in channels_to_move:
                current_group_idx = all_groups.index(current_group)
                
                if current_group_idx == 0:
                    new_group = max(all_groups) + 1
                    for channel_dict in self.selected_channels:
                        if list(channel_dict.keys())[0] == channel_name:
                            channel_dict[channel_name] = new_group
                    
                    for channel_dict in self.selected_channels:
                        ch_name = list(channel_dict.keys())[0]
                        if ch_name != channel_name:
                            channel_dict[ch_name] = max(1, channel_dict[ch_name] - 1)
                else:
                    target_group = all_groups[current_group_idx - 1]
                    new_group = target_group
                    
                    for channel_dict in self.selected_channels:
                        if list(channel_dict.keys())[0] == channel_name:
                            channel_dict[channel_name] = new_group
                    
                    for channel_dict in self.selected_channels:
                        ch_name = list(channel_dict.keys())[0]
                        if ch_name != channel_name:
                            current_ch_group = channel_dict[ch_name]
                            if current_ch_group == target_group:
                                channel_dict[ch_name] = current_ch_group + 1
        
        else:
            for channel_name, current_group in channels_to_move:
                current_group_idx = all_groups.index(current_group)
                
                if current_group_idx == len(all_groups) - 1:
                    new_group = 1
                    for channel_dict in self.selected_channels:
                        if list(channel_dict.keys())[0] == channel_name:
                            channel_dict[channel_name] = new_group
                    
                    for channel_dict in self.selected_channels:
                        ch_name = list(channel_dict.keys())[0]
                        if ch_name != channel_name:
                            channel_dict[ch_name] = channel_dict[ch_name] + 1
                else:
                    target_group = all_groups[current_group_idx + 1]
                    new_group = target_group
                    
                    for channel_dict in self.selected_channels:
                        if list(channel_dict.keys())[0] == channel_name:
                            channel_dict[channel_name] = new_group
                    
                    for channel_dict in self.selected_channels:
                        ch_name = list(channel_dict.keys())[0]
                        if ch_name != channel_name:
                            current_ch_group = channel_dict[ch_name]
                            if current_ch_group == target_group:
                                channel_dict[ch_name] = max(1, current_ch_group - 1)
        
        return self.reorder_groups()

class HighlightCreator:
    def __init__(self, df: pd.DataFrame, parent_frame):
        self.df = df
        self.parent_frame = parent_frame
        self.highlight_configs = []
    
    def create_highlight_section(self):
        highlight_frame = tk.Frame(self.parent_frame, bd=1, relief="flat", highlightbackground="black", highlightcolor="black", highlightthickness=1)
        highlight_frame.pack(fill=tk.BOTH, expand=True)

        top_row = tk.Frame(highlight_frame)
        top_row.pack(anchor='nw', pady=(8, 4), padx=8, fill=tk.X)

        highlight_label = tk.Label(top_row, text="Highlight", font=("Arial", 10, "bold"))
        highlight_label.pack(side=tk.LEFT)

        highlight_channel_var = tk.StringVar(value="None")
        highlight_channel_dropdown = ttk.Combobox(
            top_row, textvariable=highlight_channel_var, state="readonly", width=25, values=["None"] + sorted(self.df.columns)
        )
        highlight_channel_dropdown.pack(side=tk.LEFT, padx=(8, 0))

        highlight_filter_entry = tk.Entry(top_row)
        highlight_filter_entry.insert(0, "Search channels...")
        highlight_filter_entry.pack(side=tk.LEFT, padx=(8, 0), fill=tk.X, expand=True)

        _last_highlight_filter_text = ""
        def on_highlight_filter_entry_change(event):
            nonlocal _last_highlight_filter_text
            new_text = highlight_filter_entry.get().strip()

            if new_text != _last_highlight_filter_text:
                current_values = ["None"]
                
                if new_text == "":
                    current_values.extend(sorted(self.df.columns))
                else:
                    for col in self.df.columns:
                        if new_text.lower() in col.lower():
                            current_values.append(col)
                
                highlight_channel_dropdown['values'] = current_values
                _last_highlight_filter_text = new_text

        highlight_filter_entry.bind("<KeyRelease>", on_highlight_filter_entry_change)

        filter_row = tk.Frame(highlight_frame)
        filter_row.pack(anchor='nw', pady=(8, 4), padx=8, fill=tk.X)

        filter_modes = ["==", ">=", "<=", ">", "<", "isin"]
        filter_mode_var = tk.StringVar(value="==")
        filter_mode_dropdown = ttk.Combobox(filter_row, textvariable=filter_mode_var, values=filter_modes, state="readonly", width=4)
        filter_mode_dropdown.pack(side=tk.LEFT)

        value_var = tk.StringVar(value="1")
        value_entry = tk.Entry(filter_row, textvariable=value_var, width=10)
        value_entry.pack(side=tk.LEFT, padx=(6, 0))

        color_var = tk.StringVar(value="red")
        color_dropdown = ttk.Combobox(filter_row, textvariable=color_var, values=list(COLORS.keys()), state="readonly", width=8)
        color_dropdown.pack(side=tk.LEFT, padx=(6, 0))
        
        # Store the configuration for this highlight section
        highlight_config = {
            'highlight_channel_var': highlight_channel_var,
            'filter_mode_var': filter_mode_var,
            'value_var': value_var,
            'color_var': color_var,
            'highlight_frame': highlight_frame
        }
        
        self.highlight_configs.append(highlight_config)
        return highlight_frame
        
    def get_highlight_configs(self):
        return self.highlight_configs

class Plotter(tk.Tk):
    def __init__(self, df: pd.DataFrame, title: str):
        super().__init__()
        self.df = df
        self.titleText = title

        self.title(title)
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
        
        left_buttons = ["[<>]", "[><]", "↑", "↓", "<", "<<"]
        for i, label in enumerate(left_buttons):
            button = tk.Button(bottom_frame, text=label, width=3)
            button.pack(pady=1)
            button.config(command=lambda btn=button, idx=i+len(right_buttons): self.buttonClick(idx))

        settings_frame = tk.Frame(self, width=350)
        settings_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10, anchor='n')
        settings_frame.pack_propagate(False)
        # Create initial highlight area
        self.hc = HighlightCreator(df, settings_frame)
        self.hc.create_highlight_section()

        add_highlight_button = tk.Button(settings_frame, text="+", width=2, height=1, 
                                       command=lambda: self.hc.create_highlight_section())
        add_highlight_button.pack(side=tk.BOTTOM, anchor='sw', padx=5, pady=5)

        plot_btn_frame = tk.Frame(right_frame)
        plot_btn_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(3, 1))

        plot_btn = tk.Button(plot_btn_frame, text="Plot", command=self.plot)
        plot_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def plot(self):
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

            self.highlight(ax, self.df[channel])

        axes[-1].set_xlabel("Index")
        fig.suptitle(self.titleText)
        plt.show()

    def highlight(self, ax, data):
        highlight_configs = self.hc.get_highlight_configs()
        
        for config in highlight_configs:
            highlight_channel_var = config['highlight_channel_var']
            filter_mode_var = config['filter_mode_var']
            value_var = config['value_var']
            color_var = config['color_var']
            
            if highlight_channel_var.get() in (None, "", "None"):
                continue
                
            channel_name = highlight_channel_var.get()
            if channel_name not in self.df.columns:
                continue
                
            channel_data = self.df[channel_name]
            
            filter_modes = ["==", ">=", "<=", ">", "<", "isin"]
            if filter_mode_var.get() not in filter_modes:
                continue
                
            if value_var.get() in (None, ""):
                continue

            fm = filter_mode_var.get()
            color = COLORS[color_var.get()]

            match fm:
                case "==":
                    try:
                        val = float(value_var.get())
                    except ValueError:
                        continue
                    highlighting = False
                    start = None
                    for i, v in enumerate(channel_data):
                        if v == val and not highlighting:
                            highlighting = True
                            start = self.df.index[i]
                        elif v != val and highlighting:
                            highlighting = False
                            ax.axvspan(start, self.df.index[i], color=color, alpha=0.5)
                    if highlighting and start is not None:
                        ax.axvspan(start, self.df.index[-1], color=color, alpha=0.5)
                case ">=": 
                    try:
                        val = float(value_var.get())
                    except ValueError:
                        continue
                    highlighting = False
                    start = None
                    for i, v in enumerate(channel_data):
                        if v >= val and not highlighting:
                            highlighting = True
                            start = self.df.index[i]
                        elif v < val and highlighting:
                            highlighting = False
                            ax.axvspan(start, self.df.index[i], color=color, alpha=0.5)
                    if highlighting and start is not None:
                        ax.axvspan(start, self.df.index[-1], color=color, alpha=0.5)
                case "<=":
                    try:
                        val = float(value_var.get())
                    except ValueError:
                        continue
                    highlighting = False
                    start = None
                    for i, v in enumerate(channel_data):
                        if v <= val and not highlighting:
                            highlighting = True
                            start = self.df.index[i]
                        elif v > val and highlighting:
                            highlighting = False
                            ax.axvspan(start, self.df.index[i], color=color, alpha=0.5)
                    if highlighting and start is not None:
                        ax.axvspan(start, self.df.index[-1], color=color, alpha=0.5)
                case ">":
                    try:
                        val = float(value_var.get())
                    except ValueError:
                        continue
                    highlighting = False
                    start = None
                    for i, v in enumerate(channel_data):
                        if v > val and not highlighting:
                            highlighting = True
                            start = self.df.index[i]
                        elif v <= val and highlighting:
                            highlighting = False
                            ax.axvspan(start, self.df.index[i], color=color, alpha=0.5)
                    if highlighting and start is not None:
                        ax.axvspan(start, self.df.index[-1], color=color, alpha=0.5)
                case "<":
                    try:
                        val = float(value_var.get())
                    except ValueError:
                        continue
                    highlighting = False
                    start = None
                    for i, v in enumerate(channel_data):
                        if v < val and not highlighting:
                            highlighting = True
                            start = self.df.index[i]
                        elif v >= val and highlighting:
                            highlighting = False
                            ax.axvspan(start, self.df.index[i], color=color, alpha=0.5)
                    if highlighting and start is not None:
                        ax.axvspan(start, self.df.index[-1], color=color, alpha=0.5)
                case "isin":
                    val_str = value_var.get()
                    vals = val_str.split(",")
                    highlighting = False
                    start = None
                    for i, v in enumerate(channel_data):
                        if str(v) in vals and not highlighting:
                            highlighting = True
                            start = self.df.index[i]
                        elif str(v) not in vals and highlighting:
                            highlighting = False
                            ax.axvspan(start, self.df.index[i], color=color, alpha=0.5)
                    if highlighting and start is not None:
                        ax.axvspan(start, self.df.index[-1], color=color, alpha=0.5)

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

        def get_next_group_number():
            if not self.selected_items_meta:
                return 1
            return max(item['group'] for item in self.selected_items_meta) + 1

        def normalize_groups():
            if not self.selected_items_meta:
                return

            unique_groups = sorted(set(item['group'] for item in self.selected_items_meta))
            group_mapping = {old_group: new_group for new_group, old_group in enumerate(unique_groups, 1)}

            for item in self.selected_items_meta:
                item['group'] = group_mapping[item['group']]

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

            case 4: # "[<>]"
                sel = get_selected_items(self.selected_listbox)
                if not sel:
                    return
                    
                group_num = get_next_group_number()
                for i in reversed(sel):
                    item = self.selected_items_meta[i]
                    del self.selected_items_meta[i]
                    self.selected_items_meta.append({'name': item['name'], 'group': group_num})
                    group_num += 1
                normalize_groups()
                sync_listbox_with_meta()

            case 5: # "[><]"
                sel = get_selected_items(self.selected_listbox)
                if not sel:
                    return
                    
                group_num = get_next_group_number()
                for i in sel:
                    self.selected_items_meta[i]['group'] = group_num
                normalize_groups()
                sync_listbox_with_meta()
            
            case 6:  # "↑"
                sel = get_selected_items(self.selected_listbox)
                if not sel:
                    return
                for i in sel:
                    if i == 0:
                        continue
                    self.selected_items_meta[i-1], self.selected_items_meta[i] = self.selected_items_meta[i], self.selected_items_meta[i-1]
                sync_listbox_with_meta()
                for i in [s-1 for s in sel if s > 0]:
                    self.selected_listbox.selection_set(i)

            case 7:  # "↓"
                sel = get_selected_items(self.selected_listbox)
                if not sel:
                    return
                for i in reversed(sel):
                    if i == len(self.selected_items_meta) - 1:
                        continue
                    self.selected_items_meta[i], self.selected_items_meta[i+1] = self.selected_items_meta[i+1], self.selected_items_meta[i]
                sync_listbox_with_meta()
                for i in [s+1 for s in sel if s < len(self.selected_items_meta)-1]:
                    self.selected_listbox.selection_set(i)

            case 8:  # "<"
                sel = get_selected_items(self.selected_listbox)
                if sel:
                    for i in reversed(sel):
                        del self.selected_items_meta[i]
                    normalize_groups()
                    sync_listbox_with_meta()

            case 9:  # "<<"
                self.selected_items_meta.clear()
                sync_listbox_with_meta()
            case _:
                print(f"Unknown button index: {index}")

def plot_assist_df(df, title):
    app = Plotter(df, title)
    app.mainloop()

if __name__ == "__main__":
    df = pd.read_csv('example_dataframe_time.csv', index_col=0)
    df.index = pd.to_datetime(df.index)
    plot_assist_df(df, "Plot Assist")