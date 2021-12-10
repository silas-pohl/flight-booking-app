import { readable, Readable } from 'svelte/store';

export const API_URL: Readable<string> = readable('http://localhost:80');
