export interface AppData {
	channels: Channel[]
}

export interface Channel {
	name: string
	index: string[]
	datapoints: number[]
}
