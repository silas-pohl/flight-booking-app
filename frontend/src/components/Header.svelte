<script lang="ts">
  import { Header, HeaderUtilities, HeaderActionLink, Button } from 'carbon-components-svelte';
  import Information from 'carbon-icons-svelte/lib/Information24';
  import UserAvatar from 'carbon-icons-svelte/lib/UserAvatar24';
  import Logout from 'carbon-icons-svelte/lib/Logout24';
  import { API_URL, access_token } from '../store';
  import { onMount } from 'svelte';

  let admin = false;

  onMount(() => {
    setTimeout(() => {
      let decoded: { admin: boolean } = JSON.parse(window.atob(String($access_token).split('.')[1])) as { admin: boolean };
      admin = decoded.admin;
    }, 300);
  });

  const logout = (e: Event): void => {
    e.preventDefault();
    console.log('logout');
    fetch(($API_URL as string) + '/logout', {
      method: 'DELETE',
      credentials: 'include',
    })
      .then(() => {
        access_token.set('');
        window.location.href = '/login';
      })
      .catch((err: Error) => {
        console.error(err);
      });
  };
</script>

<Header platformName="The Flight Booking Company" href="/">
  <HeaderUtilities>
    {#if admin}
      <span style="color: white; display: flex; align-items: center; margin-right: 12px;"><h5>Logged in as administrator</h5></span>
    {/if}
    <HeaderActionLink icon={Information} href="/about" />
    <HeaderActionLink icon={UserAvatar} href="/profile" />
    <Button on:click={logout} icon={Logout}>Logout</Button>
  </HeaderUtilities>
</Header>
