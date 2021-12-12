/// <reference types="svelte" />

declare interface LoginData {
  email: string;
  password: string;
}

declare interface RegisterData {
  firstName: string;
  lastName: string;
  email: string;
  password: string;
}

declare interface AuthNotification {
  kind: 'error' | 'info' | 'info-square' | 'success' | 'warning' | 'warning-alt';
  title: string;
  subtitle: string;
}

declare interface User {
  first_name: string;
  last_name: string;
  email: string;
}

declare interface Ticket {
  id: string;
  owner_id: string;
  flight_id: string;
  created: string;
}

declare interface DisplayTicket {
  id: string;
  departure_airport: string;
  departure_time: string;
  destination_airport: string;
  arrival_time: string;
  created: string;
}

declare interface Flight {
  departure_airport_id: string;
  destination_airport_id: string;
  departure_time_utc: string;
  arrival_time_utc: string;
  ticket_price_dollars: number;
  seats: number;
  id: string;
}

declare interface DisplayFlight {
  id: string;
  departure_airport: string;
  departure_time: string;
  destination_airport: string;
  arrival_time: string;
  price: number;
  seats: number;
}

declare interface Airport {
  title: string;
  description: string;
  id: string;
}
