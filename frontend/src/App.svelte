<style>
  main {
    width: 100%;
    max-width: 1600px;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .w-header {
    margin-top: 47px;
    height: calc(100% - 47px);
  }
  .wo-header {
    height: 100%;
  }
</style>

<script lang="ts">
  import { onMount } from 'svelte';
  import { Route } from 'tinro';
  import Header from './components/Header.svelte';
  import Home from './pages/Home.svelte';
  import Login from './pages/Login.svelte';
  import Register from './pages/Register.svelte';
  import Profile from './pages/Profile.svelte';
  import { API_URL, access_token } from './store';

  onMount(() => {
    refreshtoken();
  });

  const refreshtoken = (): void => {
    fetch(($API_URL as string) + '/refreshtoken', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
    })
      .then((res: Response) => {
        if (res.status === 200) {
          if (['/login', '/register'].includes(window.location.pathname)) {
            //Refresh token is valid und wir sind auf einer Auth Seite
            window.location.href = '/';
          } else {
            //Refresh token is valid und wir sind auf keiner Auth Seite
            res
              .json()
              .then((data: { access_token: string; bearer: string; expires_in: number }) => {
                access_token.set(data.access_token);
                setTimeout(() => {
                  refreshtoken();
                }, data.expires_in - 1000);
              })
              .catch((err: Error) => {
                console.error(err);
              });
          }
        } else {
          if (['/login', '/register'].includes(window.location.pathname)) {
            //Refresh token is invalid und wir sind auf einer Auth Seite
          } else {
            //Refresh token is invalid und wir sind auf keiner Auth Seite
            window.location.href = '/login';
          }
        }
      })
      .catch((err: Error) => {
        console.error(err);
      });
  };
</script>

{#if !['/login', '/register'].includes(window.location.pathname)}
  <Header />
{/if}
<!-- Main content with page routing -->
<main class={!['/login', '/register'].includes(window.location.pathname) ? 'w-header' : 'wo-header'}>
  <!-- Global header for every page except Login and Register -->
  <Route path="/"><Home /></Route>
  <Route path="/about"><h1>About</h1></Route>
  <Route path="/login"><Login /></Route>
  <Route path="/register"><Register /></Route>
  <Route path="/profile"><Profile /></Route>
</main>
