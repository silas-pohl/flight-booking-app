<script lang="ts">
    import { Button, Form, InlineNotification, TextInput } from "carbon-components-svelte";
    import ArrowRight32 from "carbon-icons-svelte/lib/ArrowRight32";
    import { authNotification } from "../lib/store";

    let loginData: LoginData = { email: "", password: "" };
    let emailError: string = "";
    let passwordError: string = "";

    const validateEmail = (): void => { emailError = loginData.email.length > 0 ? "" : "Email is required." };
    const validatePassword = (): void => { passwordError = loginData.password.length > 0 ? "" : "Password is required." };
    const validateForm = (): void => { validateEmail(); validatePassword(); if (!(emailError || passwordError)) login(loginData);};

    const login = (data: LoginData): void => {
        $authNotification = ({ "kind": "error", "title": "Login failed.", "subtitle": "Invalid email or password." });
    }
</script>

<div id="card">
    <img src="images/logo.svg" alt="The Flight Booking Company" style="position: relative; left: 10%; width: 80%;"/>

    <Form on:submit={validateForm}>

        <TextInput
            bind:value={loginData.email}
            on:change={validateEmail}
            labelText="Enter Email"
            invalid={Boolean(emailError)}
            invalidText={emailError}
        />
        {#if Boolean(emailError)}
            <div style="margin-bottom: 1rem;"/>
        {:else}
            <div style="margin-bottom: calc(1rem + 20px);"/>
        {/if}

        <TextInput
            bind:value={loginData.password}
            on:change={validatePassword}
            labelText="Enter Password"
            type="password"
            invalid={Boolean(passwordError)}
            invalidText={passwordError}
        />
        {#if Boolean(passwordError)}
            <div style="margin-bottom: 1rem;"/>
        {:else}
            <div style="margin-bottom: calc(1rem + 20px);"/>
        {/if}

        {#if $authNotification.title !== ""}
        <InlineNotification
            kind={$authNotification.kind}
            title={$authNotification.title}
            subtitle={$authNotification.subtitle}
            on:close={() => $authNotification = {"kind": "info", "title": "", "subtitle": ""}}
            lowContrast={true}
        />
        {/if}

        <Button style="width: 100%; max-width: 100%; margin-bottom: 1.5rem;"
            kind="primary"
            type="submit"
            icon={ArrowRight32}
        >
            Login
        </Button>

        <div>Don't have an account? <a on:click={() => $authNotification = {"kind": "info", "title": "", "subtitle": ""}} href="/register" tinro-ignore>Register</a></div>

    </Form>
</div>

<style>
    #card {
        width: 600px;
        padding: 20px;
        background-color: white;
    }
</style>