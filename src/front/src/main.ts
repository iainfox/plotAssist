import {available_channels_list} from './core/dom'
import './style.css'
import type {AppData} from './types'

window.addEventListener('pywebviewready', async () => {
	const data = await window.pywebview.api.get_data()

	addChannels(data)
})

function addChannels(data: AppData) {
	const channel_names = data.channels.map((channel) => channel.name)

	channel_names.forEach((channel_name) => {
		const li = document.createElement("li")
		li.innerHTML = `<p>${channel_name}</p>`

		available_channels_list.appendChild(li)
	})
}
