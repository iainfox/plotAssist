import { channelHandler } from './core/channel_handler';
import { dom } from './core/dom';
import './style.css'

window.addEventListener('pywebviewready', async () => {
	const app = dom.app;
	const template = dom.appTemplate

	console.log("")
	const clone = template.content.cloneNode(true);
	app.appendChild(clone);

	const data = await window.pywebview.api.get_data()
	const channels = new channelHandler(dom.availableChannelsList, data)
})
