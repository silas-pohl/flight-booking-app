<script>
  import { Route } from 'tinro'; 
  import Login from "./pages/Login.svelte";
  import Register from "./pages/Register.svelte";
</script>

<main>
  <Route path="/"><h1>Main</h1></Route>
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