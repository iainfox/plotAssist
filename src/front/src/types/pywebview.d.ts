declare global {
	interface Window {
		pywebview: {
			api: {
				get_data(): Promise<AppData>
			}
		}
	}
}

export {}
