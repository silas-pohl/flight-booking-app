<script lang="ts">
    import AuthForm from "../components/AuthForm.svelte";

    let error: AuthError = "";

    const login = (data: LoginData): void => {
        console.log(data)
        error = "incorrectCred"
    }
</script>

<AuthForm type="login" bind:error={error} on:submit={(event) => login(event.detail)}/>   