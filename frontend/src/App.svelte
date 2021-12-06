<script lang="ts">
    import { onMount } from 'svelte';
    import { Route } from 'tinro'; 
    import Header from './lib/Header.svelte';
    import Home from "./pages/Home.svelte";
    import Login from "./pages/Login.svelte";
    import Register from "./pages/Register.svelte";

    onMount(() => {
        if (!localStorage.getItem('access_token') && !["/login", "/register", "/about"].includes(window.location.pathname)) {
           window.location.href = '/login';
        }
        else if (localStorage.getItem('access_token') && ["/login", "/register"].includes(window.location.pathname)) {
            window.location.href = '/';
        }
    })
</script>

<!-- Global header for every page except Login and Register -->
{#if !["/login", "/register"].includes(window.location.pathname)}
    <Header/>
{/if}

<!-- Main content with page routing -->
<main>
    <Route path="/"><Home/></Route>
    <Route path="/about"><h1>About</h1></Route>
    <Route path="/login"><Login/></Route>
    <Route path="/register"><Register/></Route>
</main>

<style>
    main {
        width: 100vw;
        height: 100vh;
        max-width: 1300px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
</style>