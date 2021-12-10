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
