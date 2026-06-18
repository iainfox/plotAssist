import type { AppData } from "../types";

export class channelHandler {
	private list: HTMLUListElement;

	private selectedItems = new Set<HTMLLIElement>();
	private lastClickedIndex: number | null = null;

	private isDragging = false
	private dragStartX = 0
	private dragStartY = 0
	private dragStartScrollTop = 0
	private currentMouseX = 0;
	private currentMouseY = 0;

	private selectionBox: HTMLDivElement | null = null

	constructor(list: HTMLUListElement, data: AppData) {
		this.list = list

		const channel_names = data.channels.map((channel) => channel.name)

		channel_names.forEach((channel_name, index) => {
			const li = document.createElement("li")
			li.id = crypto.randomUUID()
			li.innerHTML = `<p>${channel_name}</p>`

			li.addEventListener("click", (event) => {
				this.handleClick(event, li, index)
			})

			this.list.appendChild(li)
		});

		document.addEventListener("keydown", (event) => {
			if (event.key === "Escape") {
				this.clearSelection()
			}
		});

		this.list.addEventListener("mousedown", this.onMouseDown);
		this.list.addEventListener("scroll", this.onScroll);
		document.addEventListener("mousemove", this.onMouseMove);
		document.addEventListener("mouseup", this.onMouseUp);
	}

	private handleClick(
		event: MouseEvent,
		li: HTMLLIElement,
		index: number
	) {
		if (this.isDragging) return;

		const items = Array.from(
			this.list.querySelectorAll("li")
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

	private onMouseDown = (e: MouseEvent) => {
		if (e.button !== 0) return;


		this.isDragging = true;
		this.dragStartX = e.clientX;
		this.dragStartY = e.clientY;
		this.dragStartScrollTop = this.list.scrollTop;

		this.selectionBox = document.createElement("div");
		this.selectionBox.style.position = "fixed";
		this.selectionBox.style.border = "1px dashed #4c9ffe";
		this.selectionBox.style.background = "rgba(76,159,254,0.15)";
		this.selectionBox.style.pointerEvents = "none";
		this.selectionBox.style.zIndex = "9999";

		document.body.appendChild(this.selectionBox);
	};

	private updateSelectionBox(clientX: number, clientY: number) {
		const scrollDelta =
			this.list.scrollTop - this.dragStartScrollTop;

		const adjustedStartY =
			this.dragStartY - scrollDelta;

		const x1 = Math.min(this.dragStartX, clientX);
		const y1 = Math.min(adjustedStartY, clientY);
		const x2 = Math.max(this.dragStartX, clientX);
		const y2 = Math.max(adjustedStartY, clientY);

		this.selectionBox!.style.left = `${x1}px`;
		this.selectionBox!.style.top = `${y1}px`;
		this.selectionBox!.style.width = `${x2 - x1}px`;
		this.selectionBox!.style.height = `${y2 - y1}px`;

		this.updateSelection(x1, y1, x2, y2);
	}

	private onScroll = () => {
		if (!this.isDragging || !this.selectionBox) return;

		this.updateSelectionBox(
			this.currentMouseX,
			this.currentMouseY
		);
	};

	private onMouseMove = (e: MouseEvent) => {
		this.currentMouseX = e.clientX;
		this.currentMouseY = e.clientY;

		if (!this.isDragging || !this.selectionBox) return;

		this.updateSelectionBox(
			e.clientX,
			e.clientY
		);
	};

	private onMouseUp = () => {
		this.isDragging = false;

		if (this.selectionBox) {
			this.selectionBox.remove();
			this.selectionBox = null;
		}
	};

	private updateSelection(
		x1: number,
		y1: number,
		x2: number,
		y2: number
	) {
		const items = Array.from(
			this.list.querySelectorAll("li")
		) as HTMLLIElement[];

		const next = new Set<HTMLLIElement>();

		for (const li of items) {
			if (li.style.display === "none") continue

			const rect = li.getBoundingClientRect();

			const intersects =
				rect.right >= x1 &&
				rect.left <= x2 &&
				rect.bottom >= y1 &&
				rect.top <= y2;

			if (intersects) {
				next.add(li);
			}
		}

		for (const li of items) {
			if (next.has(li)) {
				if (!this.selectedItems.has(li)) {
					this.selectItem(li);
				}
			} else {
				if (this.selectedItems.has(li)) {
					this.deselectItem(li);
				}
			}
		}
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

	public sort(key: string) {
		const items = Array.from(
			this.list.querySelectorAll("li")
		) as HTMLLIElement[];

		items.forEach((item) => {
			if (!item.textContent.includes(key)) {
				item.style.display = "none"
			} else {
				item.style.display = "block"
			}
		})
	}
}