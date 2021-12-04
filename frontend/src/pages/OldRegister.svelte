<script lang="ts">
    import { Form, TextInput, Button, InlineNotification } from "carbon-components-svelte";
    import ArrowRight32 from "carbon-icons-svelte/lib/ArrowRight32";
    import { authNotification } from "../lib/store";

    let registerData: RegisterData = { firstName: "", lastName: "", email: "", password: "" };
    let confPassword: string = "";
    let firstNameError: string = "";
    let lastNameError: string = "";
    let emailError: string = "";
    let passwordError: string = "";
    let confPasswordError: string = "";
    let showVerificationForm: boolean = false;

    const checkFirstName = (): void => {
        switch (true) {
            case registerData.firstName.length === 0: firstNameError =  "First name is required."; break;
            case registerData.firstName.length < 2: firstNameError =  "First name must be at least 2 characters long."; break;
            default: firstNameError =  "";
        }
    };
    const checkLastName = (): void => {
        switch (true) {
            case registerData.lastName.length === 0: lastNameError =  "Last name is required."; break;
            case registerData.lastName.length < 2: lastNameError =  "Last name must be at least 2 characters long."; break;
            default: lastNameError = "";
        }
    };
    const checkEmail = (): void => {
        const regex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        switch (true) {
            case registerData.email.length === 0: emailError = "Email is required."; break;
            case !registerData.email.match(regex): emailError = "Enter a valid email adress."; break;
            default: emailError = "";
        }
};
    const checkPassword = (): void => {
        switch (true) {
            case registerData.password.length === 0: passwordError = "Password is required."; break;
            case registerData.password.length < 12: passwordError = "Password must be at least 12 characters long."; break;
            default: passwordError = "";
        }
    };
    const checkConfPassword = (): void => {
        switch (true) {
            case confPassword.length === 0: confPasswordError = "Password confirmation is required."; break;
            case confPassword !== registerData.password: confPasswordError = "Passwords are not equal."; break;
            default: confPasswordError = "";
        }
    };
    const checkForm = (): void => { 
        checkFirstName(); checkLastName(); checkEmail(); checkPassword(); checkConfPassword(); 
        if (!(firstNameError || lastNameError || emailError || passwordError || confPasswordError)) {
            get_verificationcode(registerData.email);
        }
    };

    function get_verificationcode(email: string) {
        fetch("http://localhost:80/verificationcode", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: email, action: "register" })
        })
        .then((res: Response) => {
            if (res.status === 200) { showVerificationForm = true; }
        })
        .catch((err: Error) => {
            console.log(err);
        });
    }

    function register(data: RegisterData): void {
        fetch("http://localhost:80/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                first_name: data.firstName,
                last_name: data.lastName,
                email: data.email,
                password: data.password,
            }),
        })
        .then((res: Response) => {
            if (res.status === 201) {
                window.location.href = "/login";
                authNotification.set({ kind: "success", title: "Account was created successfully.", subtitle: "Please try to login." });
            } else if (res.status === 403) {
                authNotification.set({ kind: "error", title: "Incorrect verification code.", subtitle: "Please log in or use different email." });
            } else if (res.status === 422) {
                authNotification.set({ kind: "error", title: "Invalid request data.", subtitle: "Please log in or use different email." });
            }
        })
        .catch((err: Error) => {
            authNotification.set({ kind: "error", title: err.message, subtitle: "" })
        });
    }
</script>

<div id="card">
    <img src="images/logo.svg" alt="The Flight Booking Company" style="position: relative; left: 10%; width: 80%;"/>

    {#if showVerificationForm === false}
    <Form on:submit={checkForm}>

        <TextInput
            bind:value={registerData.firstName}
            on:change={checkFirstName}
            labelText="Enter First Name"
            invalid={Boolean(firstNameError)}
            invalidText={firstNameError}
        />
        {#if Boolean(firstNameError)}
            <div style="margin-bottom: 1rem;"/>
        {:else}
            <div style="margin-bottom: calc(1rem + 20px);"/>
        {/if}

        <TextInput
            bind:value={registerData.lastName}
            on:change={checkLastName}
            labelText="Enter Last Name"
            invalid={Boolean(lastNameError)}
            invalidText={lastNameError}
        />
        {#if Boolean(lastNameError)}
            <div style="margin-bottom: 1rem;"/>
        {:else}
            <div style="margin-bottom: calc(1rem + 20px);"/>
        {/if}

        <TextInput
            bind:value={registerData.email}
            on:change={checkEmail}
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
            bind:value={registerData.password}
            on:change={checkPassword}
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

        <TextInput
            bind:value={confPassword}
            on:change={checkConfPassword}
            labelText="Confirm Password"
            type="password"
            invalid={Boolean(confPasswordError)}
            invalidText={confPasswordError}
        />
        {#if Boolean(confPasswordError)}
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
            Continue
        </Button>

        <div>Already have an account? <a on:click={() => $authNotification = {"kind": "info", "title": "", "subtitle": ""}} href="/login" tinro-ignore>Log in</a></div>

    </Form>
    {:else}
    <Form>
        Test
    </Form>
    {/if}

</div>

<style>
    #card {
        width: 600px;
        padding: 20px;
        background-color: white;
    }
</style>