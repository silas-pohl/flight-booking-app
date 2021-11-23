<script lang="ts">
    import { Form, TextInput, Button, InlineNotification } from "carbon-components-svelte";
    import ArrowRight32 from "carbon-icons-svelte/lib/ArrowRight32";

    import { createEventDispatcher } from 'svelte';
    const dispatch = createEventDispatcher();

    export let type: "login" | "register" = "login";
    export let error: AuthError = "";

    let firstName: string;
    let lastName: string;
    let email: string;
    let password: string;
    let confPassword: string;
    let emailInvalid: boolean = false;
    let passwordInvalid: boolean = false;
    let confPasswordInvalid: boolean = false;

    const checkEmail = (): void => {
        const regex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        email.match(regex) ? (emailInvalid = false) : (emailInvalid = true);
    }
    const checkPassword = (): void => {
        password.length < 12 ? (passwordInvalid = true) : (passwordInvalid = false);
    }
    const checkConfPassword = (): void => {
        confPassword !== password ? (confPasswordInvalid = true) : (confPasswordInvalid = false);
    }
    const submit = (): void => {
        if (type === "login") {
            dispatch('submit', { email, password });
        } else {
            if (emailInvalid || passwordInvalid || firstName === "" || lastName === "") return;
            dispatch('submit', { firstName, lastName, email, password });
        }
    }
</script>

<div id="card">
    <img src="images/logo.svg" alt="The Flight Booking Company" style="position: relative; left: 10%; width: 80%;"/>

    <Form on:submit={submit}>

        <!-- Registration: Input for First and Last Name -->
        {#if type === "register"}
        <TextInput
            bind:value={firstName}
            labelText="Enter First Name"
            required={true}
        />
        <div style="margin-bottom: calc(1rem + 20px);"/>
        <TextInput
            bind:value={lastName}
            labelText="Enter Last Name"
            required={true}
        />
        <div style="margin-bottom: calc(1rem + 20px);"/>
        {/if}

        <!-- Input for Email -->
        <TextInput
            bind:value={email}
            on:change={type === "register" ? checkEmail : null}
            labelText="Enter Email"
            invalid={emailInvalid}
            invalidText="Enter a valid email adress."
            required={true}
        />
        {#if emailInvalid}
            <div class="test" style="margin-bottom: 1rem;"/>
        {:else}
            <div style="margin-bottom: calc(1rem + 20px);"/>
        {/if}

        <!-- Input for password -->
        <TextInput
            bind:value={password}
            on:change={type === "register" ? checkPassword: null}
            labelText="Enter Password"
            type="password"
            invalid={passwordInvalid}
            invalidText="Password must contain at least 12 characters."
            required={true}
        />
        {#if passwordInvalid}
            <div style="margin-bottom: 1rem;"/>
        {:else}
            <div style="margin-bottom: calc(1rem + 20px);"/>
        {/if}

        <!-- Registration: Input to confirm password -->
        {#if type === "register"}
        <TextInput
            bind:value={confPassword}
            on:change={checkConfPassword}
            labelText="Confirm Password"
            type="password"
            invalid={confPasswordInvalid}
            invalidText="Passwords are not equal."
            required={true}
        />
        {#if confPasswordInvalid}
            <div style="margin-bottom: 1rem;"/>
        {:else}
            <div style="margin-bottom: calc(1rem + 20px);"/>
        {/if}
        {/if}

        {#if error === "incorrectCred"}
            <InlineNotification
                kind="error"
                title="Incorrect email or password."
                subtitle="Please try again."
                on:close={() => error = ""}
                lowContrast={true}
            />
        {:else if error === "emailTaken"}
            <InlineNotification
                kind="error"
                title="Email already registered."
                subtitle="Please try again."
                on:close={() => error = ""}
                lowContrast={true}
            />
        {/if}

        <!-- Button to submit form -->
        <Button style="width: 100%; max-width: 100%; margin-bottom: 1.5rem;"
            kind="primary"
            type="submit"
            icon={ArrowRight32}
        >
        {#if type === "login"}
            Login
        {:else}
            Register
        {/if}
        </Button>

        <!-- Link to toggle Login/Register -->
        {#if type === "login"}
            <div>Don't have an account? <a href="/register" tinro-ignore>Register</a></div>
        {:else}
            <div>Already have an account? <a href="/login" tinro-ignore>Log in</a></div>
        {/if}
    </Form>
</div>

<style>
    #card {
        width: 600px;
        padding: 20px;
        background-color: white;
    }
</style>