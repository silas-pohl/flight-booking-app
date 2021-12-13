<style>
  #profile {
    width: 100%;
    height: 100%;
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 50px 200px 2.2rem 1.7rem 50px 10fr;
    grid-template-areas: '1' 'avatar' 'name' 'email' '2' 'tickets';
    align-items: center;
    justify-content: center;
  }
  img {
    width: 200px;
    height: 200px;
    background-color: white;
    border-radius: 1000px;
  }
  #avatar {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    grid-area: avatar;
  }
  #name {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    grid-area: name;
    font-size: 2rem;
  }
  #email {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    grid-area: email;
    font-size: 1.5rem;
  }
  #tickets {
    width: 100%;
    height: 100%;
    grid-area: tickets;
  }
</style>

<script lang="ts">
  import { onMount } from 'svelte';
  import { API_URL, access_token } from '../store';
  import { ToastNotification, Modal, Loading, Table, TableBody, TableCell, TableHead, TableRow, Button } from 'carbon-components-svelte';
  import CloseOutline from 'carbon-icons-svelte/lib/CloseOutline32';

  let user: Promise<User> = new Promise(() => {}); //eslint-disable-line @typescript-eslint/no-empty-function
  let tickets: Promise<DisplayTicket[]> = new Promise(() => {}); //eslint-disable-line @typescript-eslint/no-empty-function
  let show_cancellation_modal: { [key: string]: boolean } = {};
  let cancellation_fail = false;
  let admin = false;

  onMount(() => {
    //eslint-disable-next-line @typescript-eslint/no-misused-promises
    setTimeout(async () => {
      let decoded: { admin: boolean } = JSON.parse(window.atob(String($access_token).split('.')[1])) as { admin: boolean };
      admin = decoded.admin;
      user = get_user_data();
      tickets = get_user_tickets();
      let res_tickets = await tickets;
      res_tickets.forEach(ticket => {
        show_cancellation_modal[ticket.id] = false;
      });
    }, 300);
  });

  const get_user_data = async (): Promise<User> => {
    let res = await fetch(($API_URL as string) + '/me', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${$access_token as string}`,
      },
    });
    let data: User = (await res.json()) as User;
    return data;
  };

  const get_user_tickets = async (): Promise<DisplayTicket[]> => {
    let res = await fetch(($API_URL as string) + '/me/tickets', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${$access_token as string}`,
      },
    });
    let data: Ticket[] = (await res.json()) as Ticket[];
    let display_tickets: DisplayTicket[] = [];
    for (const [i, ticket] of data.entries()) {
      let flight = await get_flight(ticket.flight_id);
      display_tickets[i] = {
        id: ticket.id,
        departure_airport: await get_airport(flight.departure_airport_id),
        departure_time: flight.departure_time_utc,
        destination_airport: await get_airport(flight.destination_airport_id),
        arrival_time: flight.arrival_time_utc,
        created: ticket.created,
      };
    }
    return display_tickets;
  };

  const get_flight = async (flight_id: string): Promise<Flight> => {
    let res: Response = await fetch(($API_URL as string) + '/flights/' + flight_id, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${$access_token as string}`,
      },
    });
    let data: Flight = (await res.json()) as Flight;
    return data;
  };
  const get_airport = async (airport_id: string): Promise<string> => {
    let res = await fetch(($API_URL as string) + '/airports/' + airport_id, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${$access_token as string}`,
      },
    });
    let data: Airport = (await res.json()) as Airport;
    return data.title;
  };
  const cancel_flight = async (ticket_id: string): Promise<void> => {
    let res = await fetch(($API_URL as string) + '/me/cancellation', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${$access_token as string}`,
      },
      body: JSON.stringify({ ticket_id }),
    });
    if (res.ok) {
      window.location.reload();
    } else {
      cancellation_fail = true;
      setTimeout(() => (cancellation_fail = false), 3000);
    }
  };
</script>

<div id="profile">
  {#await user}
    <Loading />
  {:then res_user}
    {#await tickets}
      <Loading />
    {:then res_tickets}
      <div id="avatar">
        <img alt="Avatar" src="https://avatars.dicebear.com/api/avataaars/{String(res_user.first_name)[0]}{String(res_user.last_name)[0]}{String(res_user.email)[0]}.svg" />
      </div>
      <div id="name">{res_user.first_name} {res_user.last_name} {admin ? '(Admin)' : ''}</div>
      <div id="email">{res_user.email}</div>
      {#if !admin}
        <div id="tickets">
          <h1 style="text-align: center; margin-bottom: 1rem">Your tickets</h1>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Departure Airport</TableCell>
                <TableCell>Departure Time</TableCell>
                <TableCell>Destination Airport</TableCell>
                <TableCell>Arrival Time</TableCell>
                <TableCell>Time of Purchase</TableCell>
                <TableCell />
              </TableRow>
            </TableHead>
            <TableBody>
              {#each res_tickets as ticket}
                <TableRow>
                  <TableCell>{ticket.departure_airport}</TableCell>
                  <TableCell>{new Date(String(ticket.departure_time)).toUTCString()}</TableCell>
                  <TableCell>{ticket.destination_airport}</TableCell>
                  <TableCell>{new Date(String(ticket.arrival_time)).toUTCString()}</TableCell>
                  <TableCell>{new Date(String(ticket.created)).toUTCString()}</TableCell>
                  <TableCell style="padding: 0 !important;"
                    ><Button on:click={() => (show_cancellation_modal[String(ticket.id)] = true)} style="width: 100%;" kind="danger" icon={CloseOutline}>Cancel</Button></TableCell
                  >
                </TableRow>
                <Modal
                  on:close={() => (show_cancellation_modal[String(ticket.id)] = false)}
                  on:submit={() => cancel_flight(String(ticket.id))}
                  open={show_cancellation_modal[String(ticket.id)]}
                  danger
                  modalHeading="FLIGHT CANCELLATION"
                  primaryButtonText="Cancel Flight"
                >
                  Flight cancellations are possible up to 48 hours before departure.<br />
                  Are you sure you want to cancel this flight? This action cannot be undone.<br />
                  The ticket price paid will be refunded as soon as possible.<br /><br />
                  <h5>{ticket.departure_airport} → {ticket.destination_airport}</h5>
                  on {new Date(String(ticket.departure_time)).toDateString()}
                </Modal>
              {/each}
            </TableBody>
          </Table>
          {#if cancellation_fail}
            <ToastNotification
              style="position: absolute; bottom: 0; right: 0; z-index: 9001;"
              kind="error"
              title="Flight cancellation failed!"
              subtitle="Flight cancellations are only possible up to 48 hours before departure."
              lowContrast
            />
          {/if}
        </div>
      {/if}
    {/await}
  {/await}
</div>
