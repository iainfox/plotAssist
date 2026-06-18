import {available_channels_list} from './core/dom'
import './style.css'
import type {AppData} from './types'

window.addEventListener('pywebviewready', async () => {
	const data = await window.pywebview.api.get_data()
	const channels = new channelHandler(data)
})
