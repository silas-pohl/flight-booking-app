/// <reference types="svelte" />

declare interface LoginData {
    email: string,
    password: string
}

declare interface RegisterData {
    firstName: string,
    lastName: string,
    email: string,
    password: string
}

declare type AuthError = "" | "incorrectCred" | "emailTaken" 