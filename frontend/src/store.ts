import { readable, Readable, writable, Writable } from 'svelte/store';

export const API_URL: Readable<string> = readable('https://backend-flight-booking-app.herokuapp.com/');

export const access_token: Writable<string> = writable('');
