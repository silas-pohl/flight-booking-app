<style>
  #login {
    width: 600px;
    padding: 20px;
    background-color: white;
  }
</style>

<script lang="ts">
  //-------------------------------------------------------------------------------------------------
  // Imports
  import { Button, Form, InlineNotification, TextInput } from 'carbon-components-svelte';
  import ArrowRight32 from 'carbon-icons-svelte/lib/ArrowRight32';
  import { API_URL } from '../store';

  //-------------------------------------------------------------------------------------------------
  // Variables and Constants
  let email: string, password: string;
  let email_error: string, password_error: string;
  let notification: AuthNotification = { kind: 'info', title: '', subtitle: '' };

  //-------------------------------------------------------------------------------------------------
  // Login Form Validation
  const check_email = (): void => {
    email_error = email.length > 0 ? '' : 'Email is required.';
  };
  const check_password = (): void => {
    password_error = password.length > 0 ? '' : 'Password is required.';
  };
  const check_form = (): void => {
    check_email();
    check_password();
    if (!(email_error || password_error)) {
      login();
    }
  };

  //-------------------------------------------------------------------------------------------------
  // Endpoint calls
  const login = (): void => {
    fetch(($API_URL as string) + '/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ email, password }),
    })
      .then((res: Response) => {
        if (res.status === 200) {
          res
            .json()
            .then(() => {
              window.location.href = '/';
            })
            .catch((err: Error) => {
              console.error(err);
            });
        } else if (res.status === 401) {
          notification = { kind: 'error', title: 'Incorrect email or password.', subtitle: 'Please try again.' };
        } else {
          notification = { kind: 'error', title: 'Something went wrong.', subtitle: 'Please try again later or contact support.' };
        }
      })
      .catch(() => {
        notification = { kind: 'error', title: 'Something went wrong.', subtitle: 'Please try again later or contact support.' };
      });
  };
</script>

<div id="login">
  <img src="images/logo.svg" alt="The Flight Booking Company" style="position: relative; left: 10%; width: 80%;" />
  <Form on:submit={check_form}>
    <TextInput bind:value={email} on:change={check_email} labelText="Enter Email" invalid={Boolean(email_error)} invalidText={email_error} />
    {#if Boolean(email_error)} <div style="margin-bottom: 1rem;" /> {:else} <div style="margin-bottom: calc(1rem + 20px);" /> {/if}
    <TextInput bind:value={password} on:change={check_password} labelText="Enter Password" type="password" invalid={Boolean(password_error)} invalidText={password_error} />
    {#if Boolean(password_error)} <div style="margin-bottom: 1rem;" /> {:else} <div style="margin-bottom: calc(1rem + 20px);" /> {/if}
    {#if notification.title !== ''}
      <InlineNotification
        kind={notification.kind}
        title={notification.title}
        subtitle={notification.subtitle}
        on:close={() => (notification = { kind: 'info', title: '', subtitle: '' })}
        lowContrast={true}
      />
    {/if}
    <Button style="width: 100%; max-width: 100%;" kind="primary" type="submit" icon={ArrowRight32}>Login</Button>
    <div style="margin-bottom: 1rem;" />
    <div>Don't have an account? <a href="/register" tinro-ignore>Register</a></div>
  </Form>
</div>
