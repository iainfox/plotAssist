import type { AppData } from "../types";
import { dom } from "./dom";

export class channelHandler {
	constructor(data: AppData) {
		const channel_names = data.channels.map((channel) => channel.name)

		channel_names.forEach((channel_name) => {
			const li = document.createElement("li")
			li.innerHTML = `<p>${channel_name}</p>`

			dom.availableChannelsList.appendChild(li)
		})
	}
}

