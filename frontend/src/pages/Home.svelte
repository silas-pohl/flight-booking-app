<style>
  #home {
    width: 100%;
    height: 100%;
  }
</style>

<script lang="ts">
  import { onMount } from 'svelte';
  import { API_URL, access_token } from '../store';
  import { DatePicker, NumberInput, Modal, ToastNotification, Loading, Button, Table, TableHead, TableBody, TableRow, TableCell, Select, SelectItem } from 'carbon-components-svelte';
  import ShoppingCart from 'carbon-icons-svelte/lib/ShoppingCart32';
  import Erase from 'carbon-icons-svelte/lib/Erase32';
  import AddAlt from 'carbon-icons-svelte/lib/AddAlt32';

  let flights: Promise<DisplayFlight[]> = new Promise(() => {});
  let show_booking_modal: {[key: string]: boolean} = {};
  let booking_fail = false;
  let booking_success = false;
  let admin = false;
  let new_flight: {[key: string]: string|number} = {
    'departure_airport': 'JFK - New York Airport', 
    'departure_time': '',
    'destination_airport': 'MUC - Munich Airport',
    'arrival_time': '',
    'price': 0,
    'seats': 0
  }

  onMount(() => {
    setTimeout(async () => {
      admin = JSON.parse(window.atob($access_token.split('.')[1])).admin;
      flights = get_flights();
      let res_flights = await flights;
      if (!admin) {
        res_flights.forEach(flight => { show_booking_modal[flight.id] = false })
      }
    }, 300);
  });

  const get_flights = async (): Promise<DisplayFlight[]> => {
    let res = await fetch(($API_URL as string) + '/flights', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${$access_token as string}`,
      },
    });
    let data: Flight[] = await res.json() as Flight[];
    let display_flights: DisplayFlight[] = [];
    for (const [i, flight] of data.entries()) {
      display_flights[i] = {
        id: flight.id,
        departure_airport: await get_airport(flight.departure_airport_id),
        departure_time: flight.departure_time_utc,
        destination_airport: await get_airport(flight.destination_airport_id),
        arrival_time: flight.arrival_time_utc,
        price: flight.ticket_price_dollars,
        seats: flight.seats,
      }
    }
    return display_flights;
  }

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

  const book_flight = async (flight_id: string): Promise<void> => {
    let res = await fetch(($API_URL as string) + '/me/booking', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${$access_token as string}`,
      },
      body: JSON.stringify({flight_id}),
    });
    if (res.ok) {
      booking_success = true;
      setTimeout(() => booking_success = false, 3000);
    } else {
      booking_fail = true;
      setTimeout(() => booking_fail = false, 3000);
    }
  };

  const delete_flight = async (flight_id: string): Promise<void> => {
    let res = await fetch(($API_URL as string) + '/flights/' + flight_id, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${$access_token as string}`,
      }
    });
    if (res.ok) {
      window.location.reload();
    }
  }

  const create_flight = async () => {}

</script>

<div id="home">
  {#await flights}
    <Loading />
  {:then res_flights} 
    <h1 style="text-align: center; margin-top: 1rem; margin-bottom: 1rem">All available flights</h1>
    <Table>
      <TableHead>
        <TableRow>
          <TableCell>Departure Airport</TableCell>
          <TableCell>Departure Time</TableCell>
          <TableCell>Destination Airport</TableCell>
          <TableCell>Arrival Time</TableCell>
          <TableCell>Price (USD)</TableCell>
          <TableCell>Seats</TableCell>
          <TableCell />
        </TableRow>
      </TableHead>
      <TableBody>
        {#each res_flights as flight}
          <TableRow>
            <TableCell>{flight.departure_airport}</TableCell>
            <TableCell>{new Date(flight.departure_time).toUTCString()}</TableCell>
            <TableCell>{flight.destination_airport}</TableCell>
            <TableCell>{new Date(flight.arrival_time).toUTCString()}</TableCell>
            <TableCell>{flight.price}</TableCell>
            <TableCell>{flight.seats}</TableCell>
            <TableCell style="padding: 0 !important;">
              {#if admin}
                <Button on:click={() => delete_flight(flight.id)} style="width: 100%;" kind="danger" icon={Erase}>Delete Flight</Button>
              {:else}
                <Button on:click={() => show_booking_modal[flight.id] = true} style="width: 100%;" kind="primary" icon={ShoppingCart}>Book Flight</Button>
              {/if}
            </TableCell>
          </TableRow>
          <Modal
            on:close={() => (show_booking_modal[flight.id] = false)}
            on:submit={() => (book_flight(String(flight.id)))}
            open={show_booking_modal[flight.id]}
            modalHeading="FLIGHT BOOKING"
            primaryButtonText="Book Flight"
            >
            This is the booking screen. 
            In a real application, there would be a link to our payment service provider, where the user enters his payment information.
            Only after successful payment processing, the ticket would be saved as purchased.<br><br>
            <h5>{flight.departure_airport} → {flight.destination_airport}</h5> on {new Date(flight.departure_time).toDateString()}
          </Modal>
        {/each}
        {#if admin}
          <TableRow>
            <TableCell>
              <Select bind:selected={new_flight.departure_airport} hideLabel>
                <SelectItem text="JFK - New York Airport" value="JFK - New York Airport"/>
                <SelectItem text="MUC - Munich Airport" value="MUC - Munich Airport"/>
                <SelectItem text="FRA - Frankfurt Airport" value="FRA - Frankfurt Airport"/>
                <SelectItem text="LHR - Heathrow Airport" value="LHR - Heathrow Airport"/>
                <SelectItem text="LCY - London City Airport" value="LCY - London City Airport"/>
                <SelectItem text="BRU - Brussels Airport" value="BRU - Brussels Airport"/>
              </Select>
            </TableCell>
            <TableCell>
              <DatePicker bind:selected={new_flight.departure_time} />
            </TableCell>
            <TableCell>
              <Select bind:selected={new_flight.destination_airport} hideLabel>
                <SelectItem text="JFK - New York Airport" value="JFK - New York Airport"/>
                <SelectItem text="MUC - Munich Airport" value="MUC - Munich Airport"/>
                <SelectItem text="FRA - Frankfurt Airport" value="FRA - Frankfurt Airport"/>
                <SelectItem text="LHR - Heathrow Airport" value="LHR - Heathrow Airport"/>
                <SelectItem text="LCY - London City Airport" value="LCY - London City Airport"/>
                <SelectItem text="BRU - Brussels Airport" value="BRU - Brussels Airport"/>
              </Select>
            </TableCell>
            <TableCell>
              <Select>
                <SelectItem text="Test"/>
              </Select>
            </TableCell>
            <TableCell>
              <NumberInput bind:value={new_flight.price} min={0} hideSteppers/>
            </TableCell>
            <TableCell>
              <NumberInput bind:value={new_flight.seats} min={0} hideSteppers/>
            </TableCell>
            <TableCell style="padding: 0 !important;">
              <Button on:click={() => create_flight()} style="width: 100%;" kind="primary" icon={AddAlt}>Create Flight</Button>
            </TableCell>
          </TableRow>
        {/if}
      </TableBody>
    </Table>
    {JSON.stringify(new_flight)}
    {#if booking_fail}
      <ToastNotification
        style="position: absolute; bottom: 0; right: 0; z-index: 9001;"
        kind="error"
        title="Flight booking failed!"
        subtitle="There are no more seats available."
        lowContrast
      />
    {:else if booking_success}
      <ToastNotification
        style="position: absolute; bottom: 0; right: 0; z-index: 9001;"
        kind="success"
        title="Flight booking was successful!"
        subtitle="Check your profile to see your tickets."
        lowContrast
      />
    {/if}
  {/await}
</div>
