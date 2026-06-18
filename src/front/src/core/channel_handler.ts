import type { AppData } from "../types";
import { dom } from "./dom";

export class channelHandler {
	private available_channels_list = dom.availableChannelsList;

	private selectedItems = new Set<HTMLLIElement>();
	private lastClickedIndex: number | null = null;

	constructor(data: AppData) {
		const channel_names = data.channels.map((channel) => channel.name)

		channel_names.forEach((channel_name, index) => {
			const li = document.createElement("li")
			li.id = crypto.randomUUID()
			li.innerHTML = `<p>${channel_name}</p>`

			li.addEventListener("click", (event) => {
				this.handleClick(event, li, index)
			})

			this.available_channels_list.appendChild(li)
		});

		document.addEventListener("keydown", (event) => {
			if (event.key === "Escape") {
				this.clearSelection();
			}
		});
	}

	private handleClick(
		event: MouseEvent,
		li: HTMLLIElement,
		index: number
	) {
		const items = Array.from(
			this.available_channels_list.querySelectorAll("li")
		) as HTMLLIElement[];

		if (event.shiftKey && this.lastClickedIndex !== null) {
			const start = Math.min(this.lastClickedIndex, index);
			const end = Math.max(this.lastClickedIndex, index);

			for (let i = start; i <= end; i++) {
				this.selectItem(items[i]);
			}

			return;
		}

		if (event.ctrlKey || event.metaKey) {
			if (this.selectedItems.has(li)) {
				this.deselectItem(li);
			} else {
				this.selectItem(li);
			}

			this.lastClickedIndex = index;
			return;
		}

		this.clearSelection();
		this.selectItem(li);
		this.lastClickedIndex = index;
	}

	private selectItem(li: HTMLLIElement) {
		this.selectedItems.add(li);
		li.classList.add("selected");
	}

	private deselectItem(li: HTMLLIElement) {
		this.selectedItems.delete(li);
		li.classList.remove("selected");
	}

	private clearSelection() {
		for (const item of this.selectedItems) {
			item.classList.remove("selected");
		}

		this.selectedItems.clear();
	}
}