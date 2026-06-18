function requiredElement<T extends HTMLElement>(id: string): T {
	const element = document.getElementById(id);

	if (!element) {
		throw new Error(`Couldn't find element: #${id}`);
	}

	return element as T;
}

export const dom = {
	get app() {
		return requiredElement<HTMLDivElement>("app");
	},

	get appTemplate() {
		return requiredElement<HTMLTemplateElement>("app-template");
	},

	get availableChannelsList() {
		return requiredElement<HTMLUListElement>("available-channels-list");
	},

	get addAllButton() {
		return requiredElement<HTMLButtonElement>("add-all");
	},

	get addAllGroupedButton() {
		return requiredElement<HTMLButtonElement>("add-all-grouped");
	},

	get addSelectedButton() {
		return requiredElement<HTMLButtonElement>("add-selected");
	},

	get addSelectedGroupedButton() {
		return requiredElement<HTMLButtonElement>("add-selected-grouped");
	},

	get splitGroupButton() {
		return requiredElement<HTMLButtonElement>("split-group");
	},

	get joinGroupButton() {
		return requiredElement<HTMLButtonElement>("join-group");
	},

	get moveGroupUpButton() {
		return requiredElement<HTMLButtonElement>("move-group-up");
	},

	get moveGroupDownButton() {
		return requiredElement<HTMLButtonElement>("move-group-down");
	},

	get removeSelectedButton() {
		return requiredElement<HTMLButtonElement>("remove-selected");
	},

	get removeAllButton() {
		return requiredElement<HTMLButtonElement>("remove-all");
	},

	get selectedChannelsList() {
		return requiredElement<HTMLUListElement>("selected-channels-list");
	},
};