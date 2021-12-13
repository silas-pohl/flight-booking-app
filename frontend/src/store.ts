import { readable, Readable, writable, Writable } from 'svelte/store';

export const API_URL: Readable<string> = readable('http://www.silaspohl.de');

export const access_token: Writable<string> = writable('');
