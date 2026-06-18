export const available_channels_list = document.getElementById("available-channels-list") as HTMLUListElement

export const add_all_button = document.getElementById("add-all") as HTMLButtonElement
export const add_all_grouped = document.getElementById("add-all-grouped") as HTMLButtonElement
export const add_selected_button = document.getElementById("add-selected") as HTMLButtonElement
export const add_selected_grouped_button = document.getElementById("add-selected-grouped") as HTMLButtonElement
export const split_group_button = document.getElementById("split-group") as HTMLButtonElement
export const join_group_button = document.getElementById("join-group") as HTMLButtonElement
export const move_group_up_button = document.getElementById("move-group-up") as HTMLButtonElement
export const move_group_down_button = document.getElementById("move-group-down") as HTMLButtonElement
export const remove_selected_button = document.getElementById("remove-selected") as HTMLButtonElement
export const remove_all_button = document.getElementById("remove-all") as HTMLButtonElement

export const selected_channels_list = document.getElementById("selected-channels-list") as HTMLUListElement

if (!available_channels_list) {
	throw new Error("Couldn't find element of id: #available-channels-list")
}

if (!add_all_button) {
	throw new Error("Couldn't find element of idL #add-all")
}

if (!add_all_grouped) {
	throw new Error("Couldn't find element of id: #add-all-grouped")
}

if (!add_selected_button) {
	throw new Error("Couldn't find element of idL #add-selected")
}

if (!add_selected_grouped_button) {
	throw new Error("Couldn't find element of id: #add-selected-grouped")
}

if (!split_group_button) {
	throw new Error("Couldn't find element of id: #split-group")
}

if (!join_group_button) {
	throw new Error("Couldn't find element of id: #join-group")
}

if (!move_group_up_button) {
	throw new Error("Couldn't find element of id: #move-group-up")
}

if (!move_group_down_button) {
	throw new Error("Couldn't find element of id: #move-group-down")
}

if (!remove_selected_button) {
	throw new Error("Couldn't find element of id: #remove-selected")
}

if (!remove_all_button) {
	throw new Error("Couldn't find element of id: #remove-all")
}

if (!selected_channels_list) {
	throw new Error("Couldn't find element of id: #selected-channels-list")
}
