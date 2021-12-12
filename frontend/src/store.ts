import { readable, Readable, writable, Writable } from 'svelte/store';

export const API_URL: Readable<string> = readable(process.env.API_URL || 'http://localhost:80');

export const access_token: Writable<string> = writable('');
