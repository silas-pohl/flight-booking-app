<style>
  #home {
    background-color: lightgoldenrodyellow;
    width: 100%;
    height: 100%;
  }
</style>

<script lang="ts">
  import { onMount } from 'svelte';
  import { API_URL } from '../store';

  let flights: any;

  onMount(() => {
    fetch($API_URL + '/flights', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + '',
      },
    })
      .then((res: Response) => {
        if (res.status === 200) {
          res.json().then((data: any) => {
            flights = data;
          });
          console.log(flights);
        } else if (res.status === 401) {
          window.location.href = '/login';
        } else {
          console.log('Error: ' + res.status);
        }
      })
      .catch((err: Error) => {
        console.log(err);
      });
  });
</script>

<div id="home">
  {flights}
</div>
