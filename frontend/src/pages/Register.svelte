<script lang="ts">
    import AuthForm from "../components/AuthForm.svelte";

    let error: AuthError = "";

    const register = (data: RegisterData): void => {
        console.log(data)
        error = "emailTaken"
    }
</script>

<AuthForm type="register" bind:error={error} on:submit={(event) => register(event.detail)} />