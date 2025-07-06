import time
import pandas as pd
import tkinter as tk
import tkinter.ttk as ttk
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

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
    def __init__(self, df: pd.DataFrame) -> None:
        # Data validation
        idx = df.index
        if not (isinstance(idx, pd.DatetimeIndex) or pd.api.types.is_integer_dtype(idx) or pd.api.types.is_float_dtype(idx)):
            raise ValueError("DataFrame index must be DatetimeIndex or numeric.")
        for col in df.columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                raise ValueError(f"Column '{col}' must be numeric for plotting/highlighting.")
        self.df = df
        self.available_channels = sorted(df.columns)
        self.selected_channels: list[dict[str, int]] = []
        self.current_group = 1
        self.index = df.index
    
    def get_index(self):
        return self.index

    def get_channel_data(self, channel: str):
        if channel in self.df.columns:
            return self.df[channel]

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
        if not isinstance(listbox, tk.Listbox):
            raise TypeError("Expected a tk.Listbox instance.")
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
        if not isinstance(listbox, tk.Listbox):
            raise TypeError("Expected a tk.Listbox instance.")
        visible_items = list(listbox.get(0, tk.END))
        channels_to_remove = []
        for item in visible_items:
            if ' [' in item:
                channel_name = item.split(' [')[0]
                channels_to_remove.append(channel_name)
            else:
                channels_to_remove.append(item)
        self.selected_channels = [
            channel_dict for channel_dict in self.selected_channels
            if list(channel_dict.keys())[0] not in channels_to_remove
        ]
        return self.reorder_groups()
    
    def move(self, channels: list[str], direction: str) -> list[dict[str, int]]:
        if direction not in ["up", "down"]:
            return self.selected_channels
        
        groups_to_move = set()
        for channel_dict in self.selected_channels:
            channel_name = list(channel_dict.keys())[0]
            if channel_name in channels:
                groups_to_move.add(channel_dict[channel_name])
        
        if not groups_to_move:
            return self.selected_channels
        
        all_groups = sorted(set(channel_dict[list(channel_dict.keys())[0]] for channel_dict in self.selected_channels))
        
        if direction == "up":
            min_group = min(groups_to_move)
            current_group_idx = all_groups.index(min_group)
            
            if current_group_idx == 0:
                new_group = max(all_groups) + 1
                for channel_dict in self.selected_channels:
                    channel_name = list(channel_dict.keys())[0]
                    if channel_dict[channel_name] in groups_to_move:
                        channel_dict[channel_name] = new_group
                
                for channel_dict in self.selected_channels:
                    channel_name = list(channel_dict.keys())[0]
                    if channel_dict[channel_name] not in groups_to_move:
                        channel_dict[channel_name] = max(1, channel_dict[channel_name] - 1)
            else:
                target_group = all_groups[current_group_idx - 1]
                
                channels_to_target = []
                channels_to_original = []
                
                for channel_dict in self.selected_channels:
                    channel_name = list(channel_dict.keys())[0]
                    if channel_dict[channel_name] in groups_to_move:
                        channels_to_target.append(channel_name)
                    elif channel_dict[channel_name] == target_group:
                        channels_to_original.append(channel_name)
                
                for channel_dict in self.selected_channels:
                    channel_name = list(channel_dict.keys())[0]
                    if channel_dict[channel_name] in groups_to_move:
                        channel_dict[channel_name] = target_group
                
                for channel_dict in self.selected_channels:
                    channel_name = list(channel_dict.keys())[0]
                    if channel_dict[channel_name] == target_group and channel_name not in channels_to_target:
                        channel_dict[channel_name] = min_group
        
        else:
            max_group = max(groups_to_move)
            current_group_idx = all_groups.index(max_group)
            
            if current_group_idx == len(all_groups) - 1:
                for channel_dict in self.selected_channels:
                    channel_name = list(channel_dict.keys())[0]
                    if channel_dict[channel_name] in groups_to_move:
                        channel_dict[channel_name] = 1
                
                for channel_dict in self.selected_channels:
                    channel_name = list(channel_dict.keys())[0]
                    if channel_dict[channel_name] not in groups_to_move:
                        channel_dict[channel_name] = channel_dict[channel_name] + 1
            else:
                target_group = all_groups[current_group_idx + 1]
                
                channels_to_target = []
                channels_to_original = []
                
                for channel_dict in self.selected_channels:
                    channel_name = list(channel_dict.keys())[0]
                    if channel_dict[channel_name] in groups_to_move:
                        channels_to_target.append(channel_name)
                    elif channel_dict[channel_name] == target_group:
                        channels_to_original.append(channel_name)
                
                for channel_dict in self.selected_channels:
                    channel_name = list(channel_dict.keys())[0]
                    if channel_dict[channel_name] in groups_to_move:
                        channel_dict[channel_name] = target_group

                for channel_dict in self.selected_channels:
                    channel_name = list(channel_dict.keys())[0]
                    if channel_dict[channel_name] == target_group and channel_name not in channels_to_target:
                        channel_dict[channel_name] = max_group

        self.selected_channels.sort(key=lambda x: list(x.values())[0])
        
        return self.reorder_groups()

class HighlightCreator:
    def __init__(self, data_handler: DataHandler, parent_frame):
        self.data_handler = data_handler
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
            top_row, textvariable=highlight_channel_var, state="readonly", width=25, values=["None"] + sorted(self.data_handler.available_channels)
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
                    current_values.extend(sorted(self.data_handler.available_channels))
                else:
                    for col in self.data_handler.available_channels:
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

        def remove_highlight():
            highlight_frame.destroy()
            self.highlight_configs[:] = [cfg for cfg in self.highlight_configs if cfg['highlight_frame'] != highlight_frame]
        remove_btn = tk.Button(filter_row, text="Remove", command=remove_highlight, width=7)
        remove_btn.pack(side=tk.LEFT, padx=(8, 0))
        
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
        #self.df = df
        self.data_handler = DataHandler(df)
        self.titleText = title
        self._axes = []
        self._fig = None

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

                for col in self.data_handler.available_channels:
                    if new_text.lower() in col.lower():
                        self.listbox.insert(tk.END, col)
                self._last_filter_text = new_text
            else:
                pass

        self.filter_entry.bind("<KeyRelease>", on_filter_entry_change)

        list_label = tk.Label(filter_label_frame, text="Available Channels")
        list_label.pack(side=tk.RIGHT, anchor='e')

        self.listbox = tk.Listbox(left_frame, selectmode=tk.EXTENDED, activestyle='none')
        self.listbox.pack(fill=tk.BOTH, expand=True)
        
        self.listbox.insert(tk.END, *sorted(self.data_handler.available_channels))

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
        self.hc = HighlightCreator(self.data_handler, settings_frame)
        self.hc.create_highlight_section()

        add_highlight_button = tk.Button(settings_frame, text="+", width=2, height=1, 
                                       command=lambda: self.hc.create_highlight_section())
        add_highlight_button.pack(side=tk.BOTTOM, anchor='sw', padx=5, pady=5)

        plot_btn_frame = tk.Frame(right_frame)
        plot_btn_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(3, 1))

        plot_btn = tk.Button(plot_btn_frame, text="Plot", command=self.plot)
        plot_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def plot(self):
        if not self.data_handler.selected_channels:
            return

        groups = {}
        for channel_dict in self.data_handler.selected_channels:
            channel_name = list(channel_dict.keys())[0]
            group_num = channel_dict[channel_name]
            if group_num not in groups:
                groups[group_num] = []
            groups[group_num].append(channel_name)

        sorted_groups = sorted(groups.items(), key=lambda x: x[0])

        n_groups = len(sorted_groups)
        fig, axes = plt.subplots(n_groups, 1, sharex=True, sharey=False, figsize=(8, 2.5 * n_groups))
        if n_groups == 1:
            axes = [axes]
        else:
            axes = list(axes)
        self._axes = axes
        self._fig = fig

        for ax_idx, (group_num, channel_names) in enumerate(sorted_groups):
            ax = axes[ax_idx]
            for channel in channel_names:
                if channel not in self.data_handler.available_channels:
                    continue
                ax.plot(self.data_handler.get_index(), self.data_handler.get_channel_data(channel), label=channel, linewidth=2)

            ax.grid(True, which='both', linestyle='--', alpha=0.6)
            ax.set_ylabel(f"Group {group_num}")
            ax.legend(loc='upper right', fontsize=8)
            if ax_idx != 0:
                ax.spines['top'].set_visible(False)

            self.highlight(ax)

        axes[-1].set_xlabel("Index")
        fig.suptitle(self.titleText)
        fig.canvas.mpl_connect('button_press_event', self._on_click)
        plt.tight_layout()
        if self._fig is not None:
            self._fig.canvas.draw_idle()
        plt.show()

    def highlight(self, ax):
        highlight_configs = self.hc.get_highlight_configs()
        
        for config in highlight_configs:
            highlight_channel_var = config['highlight_channel_var']
            filter_mode_var = config['filter_mode_var']
            value_var = config['value_var']
            color_var = config['color_var']
            
            if highlight_channel_var.get() in (None, "", "None"):
                continue
                
            channel_name = highlight_channel_var.get()
            if channel_name not in self.data_handler.available_channels:
                continue
                
            channel_data = self.data_handler.get_channel_data(channel_name)

            if channel_data is None:
                continue
            
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
                            start = self.data_handler.index[i]
                        elif v != val and highlighting:
                            highlighting = False
                            ax.axvspan(start, self.data_handler.index[i-1], color=color, alpha=0.5)
                    if highlighting and start is not None:
                        ax.axvspan(start, self.data_handler.index[-1], color=color, alpha=0.5)
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
                            start = self.data_handler.index[i]
                        elif v < val and highlighting:
                            highlighting = False
                            ax.axvspan(start, self.data_handler.index[i-1], color=color, alpha=0.5)
                    if highlighting and start is not None:
                        ax.axvspan(start, self.data_handler.index[-1], color=color, alpha=0.5)
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
                            start = self.data_handler.index[i]
                        elif v > val and highlighting:
                            highlighting = False
                            ax.axvspan(start, self.data_handler.index[i-1], color=color, alpha=0.5)
                    if highlighting and start is not None:
                        ax.axvspan(start, self.data_handler.index[-1], color=color, alpha=0.5)
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
                            start = self.data_handler.index[i]
                        elif v <= val and highlighting:
                            highlighting = False
                            ax.axvspan(start, self.data_handler.index[i-1], color=color, alpha=0.5)
                    if highlighting and start is not None:
                        ax.axvspan(start, self.data_handler.index[-1], color=color, alpha=0.5)
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
                            start = self.data_handler.index[i]
                        elif v >= val and highlighting:
                            highlighting = False
                            ax.axvspan(start, self.data_handler.index[i-1], color=color, alpha=0.5)
                    if highlighting and start is not None:
                        ax.axvspan(start, self.data_handler.index[-1], color=color, alpha=0.5)
                case "isin":
                    val_str = value_var.get()
                    vals = [s.strip() for s in val_str.split(",")]
                    highlighting = False
                    start = None
                    for i, v in enumerate(channel_data):
                        if str(v) in vals and not highlighting:
                            highlighting = True
                            start = self.data_handler.index[i]
                        elif str(v) not in vals and highlighting:
                            highlighting = False
                            ax.axvspan(start, self.data_handler.index[i-1], color=color, alpha=0.5)
                    if highlighting and start is not None:
                        ax.axvspan(start, self.data_handler.index[-1], color=color, alpha=0.5)

    def _on_click(self, event):
        start = int(time.time() * 1000)
        if getattr(getattr(event.canvas, "toolbar", None), "mode", None):
            return
        if not getattr(self, '_axes', None):
            return

        clicked_ax = next((ax for ax in self._axes if event.inaxes == ax), None)
        if event.xdata is None or event.ydata is None or clicked_ax is None:
            return

        df = self.data_handler.df
        idx = self.data_handler.index
        x_click, y_click = event.x, event.y

        if event.button == 1:
            min_dist = float('inf')
            closest_info = None
            for line in clicked_ax.get_lines():
                label = line.get_label()
                if label not in df.columns:
                    continue
                ydata = df[label].values
                xdata = mdates.date2num(idx) if isinstance(idx, pd.DatetimeIndex) else np.asarray(idx)
                for i in range(len(xdata)):
                    x_val, y_val = xdata[i], ydata[i]
                    x_disp, y_disp = clicked_ax.transData.transform((x_val, y_val))
                    dist = np.hypot(x_disp - x_click, y_disp - y_click)
                    if dist < min_dist:
                        min_dist = dist
                        closest_info = (line, x_val, y_val, idx[i], label)
            if closest_info:
                end = int(time.time() * 1000)
                line, x_val, y_val, idx_val, col_name = closest_info
                print(f"\n({end-start}) Left click closest point: {idx_val}\nData: {col_name}: {y_val}")
                old_xlim, old_ylim = clicked_ax.get_xlim(), clicked_ax.get_ylim()
                clicked_ax.plot(x_val, y_val, marker='o', markersize=4,
                                markerfacecolor=line.get_color(), markeredgecolor='black',
                                markeredgewidth=1, linestyle='None', zorder=5, label='_nolegend_')
                clicked_ax.annotate(
                    f"{col_name}: {y_val:.2f}",
                    xy=(x_val, y_val),
                    xytext=(0, 10),
                    textcoords='offset points',
                    ha='center',
                    va='bottom',
                    color='black',
                    fontsize=8
                )
                clicked_ax.set_xlim(old_xlim)
                clicked_ax.set_ylim(old_ylim)

        elif event.button == 3 and clicked_ax is not None:
            if isinstance(idx, pd.DatetimeIndex):
                xdata = mdates.date2num(idx)
            else:
                xdata = np.asarray(idx)
            y_center = 0.5 * (clicked_ax.get_ylim()[0] + clicked_ax.get_ylim()[1])
            x_disp_all = []
            for xv in xdata:
                x_disp, _ = clicked_ax.transData.transform((xv, y_center))
                x_disp_all.append(x_disp)
            x_disp_all = np.array(x_disp_all)
            x_click = event.x
            closest_idx = np.argmin(np.abs(x_disp_all - x_click))
            closest_time = idx[closest_idx]
            data_at_time = df.loc[closest_time]
            print()
            print(f"Right click at time: {closest_time}")
            print("Data at this time (shown):")
            for ax in self._axes:
                for line in ax.get_lines():
                    if line.get_label() in df.columns:
                        column = line.get_label()
                        value = data_at_time[column]
                        print(f"{column}: {value}")
                        if isinstance(idx, pd.DatetimeIndex):
                            x_plot = float(mdates.date2num(closest_time))
                        else:
                            x_plot = float(np.asarray(closest_time))
                        old_xlim = ax.get_xlim()
                        old_ylim = ax.get_ylim()
                        ax.plot(x_plot, value, marker='o', markersize=4,
                                markerfacecolor=line.get_color(), markeredgecolor='black', markeredgewidth=1,
                                linestyle='None', zorder=5, label='_nolegend_')
                        ax.annotate(
                            f"{column}: {value:.2f}",
                            xy=(x_plot, value),
                            xytext=(0, 10),
                            textcoords='offset points',
                            ha='center',
                            va='bottom',
                            color='black',
                            fontsize=8
                        )
                        ax.set_xlim(old_xlim)
                        ax.set_ylim(old_ylim)
            print(f"({int(time.time() * 1000)-start})")
        if self._fig is not None:
            self._fig.canvas.draw_idle()

    def buttonClick(self, index):
        match index:
            case 0:  # ">>"
                channels = [self.listbox.get(i) for i in range(self.listbox.size())]
                if channels:
                    self.data_handler.select_channels(channels, keep_group=False)
                    self.update_selected_listbox()

            case 1:  # "[>>]"
                channels = [self.listbox.get(i) for i in range(self.listbox.size())]
                if channels:
                    self.data_handler.select_channels(channels, keep_group=True)
                    self.update_selected_listbox()

            case 2:  # ">"
                selected_indices = [i for i in self.listbox.curselection()]
                if selected_indices:
                    channels = [self.listbox.get(i) for i in selected_indices]
                    self.data_handler.select_channels(channels, keep_group=False)
                    self.update_selected_listbox()

            case 3:  # "[>]"
                selected_indices = [i for i in self.listbox.curselection()]
                if selected_indices:
                    channels = [self.listbox.get(i) for i in selected_indices]
                    self.data_handler.select_channels(channels, keep_group=True)
                    self.update_selected_listbox()

            case 4: # "[<>]"
                selected_indices = [i for i in self.selected_listbox.curselection()]
                if not selected_indices:
                    return
                
                channels = []
                for i in selected_indices:
                    channel_name = list(self.data_handler.selected_channels[i].keys())[0]
                    channels.append(channel_name)
                
                self.data_handler.split_channels(channels)
                self.update_selected_listbox()

            case 5: # "[><]"
                selected_indices = [i for i in self.selected_listbox.curselection()]
                if not selected_indices:
                    return
                
                channels = []
                for i in selected_indices:
                    channel_name = list(self.data_handler.selected_channels[i].keys())[0]
                    channels.append(channel_name)
                
                self.data_handler.combine_channels(channels)
                self.update_selected_listbox()
            
            case 6:  # "↑"
                selected_indices = [i for i in self.selected_listbox.curselection()]
                if not selected_indices:
                    return
                
                channels = []
                for i in selected_indices:
                    channel_name = list(self.data_handler.selected_channels[i].keys())[0]
                    channels.append(channel_name)
                
                self.data_handler.move(channels, "up")
                self.update_selected_listbox()

            case 7:  # "↓"
                selected_indices = [i for i in self.selected_listbox.curselection()]
                if not selected_indices:
                    return
                
                channels = []
                for i in selected_indices:
                    channel_name = list(self.data_handler.selected_channels[i].keys())[0]
                    channels.append(channel_name)
                
                self.data_handler.move(channels, "down")
                self.update_selected_listbox()

            case 8:  # "<"
                selected_indices = [i for i in self.selected_listbox.curselection()]
                if selected_indices:
                    channels = []
                    for i in selected_indices:
                        channel_name = list(self.data_handler.selected_channels[i].keys())[0]
                        channels.append(channel_name)
                    
                    self.data_handler.remove_channels(channels)
                    self.update_selected_listbox()

            case 9:  # "<<"
                self.data_handler.remove_all_channels(self.selected_listbox)
                self.update_selected_listbox()
                
            case _:
                print(f"Unknown button index: {index}")

    def update_selected_listbox(self):
        self.selected_listbox.delete(0, tk.END)
        for channel_dict in self.data_handler.selected_channels:
            channel_name = list(channel_dict.keys())[0]
            group = channel_dict[channel_name]
            self.selected_listbox.insert(tk.END, f"{channel_name} [{group}]")

def plot_assist_df(df, title):
    app = Plotter(df, title)
    app.mainloop()

if __name__ == "__main__":
    df = pd.read_csv('example_dataframe_time.csv', index_col=0)
    df.index = pd.to_datetime(df.index)
    plot_assist_df(df, "Plot Assist")