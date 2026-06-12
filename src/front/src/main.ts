import './style.css'

window.addEventListener('pywebviewready', async () => {
	const data = await window.pywebview.api.get_data()

	console.log(data)
})
