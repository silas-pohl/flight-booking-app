import { readable, Readable, writable, Writable } from 'svelte/store';

export const API_URL: Readable<string> = readable('http://localhost:80');

export const access_token: Writable<string> = writable('');
