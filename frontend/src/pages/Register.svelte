<script lang="ts">
  //-------------------------------------------------------------------------------------------------
  // Imports
  import { Form, TextInput, Button, InlineNotification, Modal } from 'carbon-components-svelte';
  import ArrowRight from 'carbon-icons-svelte/lib/ArrowRight32';

  //-------------------------------------------------------------------------------------------------
  // Variables and Constants
  const NAME_REGEX = /^([A-Z][a-zA-Z]*)$/;
  const EMAIL_REGEX = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  const PASSWORD_REGEX = /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{12,}$/;
  const VERIFICATION_CODE_REGEX = /^[1-9]\d{7,7}$/;
  let first_name: string, last_name: string, email: string, password: string, conf_password: string;
  let first_name_error: string, last_name_error: string, email_error: string, password_error: string, conf_password_error: string;
  let notification: AuthNotification = { kind: 'info', title: '', subtitle: '' };
  let showVerificationForm: boolean, verification_code: number, verification_code_error: string;

  //-------------------------------------------------------------------------------------------------
  // Register Form Validation
  const check_first_name = (): void => {
    switch (true) {
      case first_name.length === 0:
        first_name_error = 'First name is required.';
        break;
      case first_name.length < 2:
        first_name_error = 'First name must be at least 2 characters long.';
        break;
      case !first_name.match(NAME_REGEX):
        first_name_error = 'First name must start with a capital letter and contain only letters.';
        break;
      default:
        first_name_error = '';
    }
  };
  const check_last_name = (): void => {
    switch (true) {
      case last_name.length === 0:
        last_name_error = 'Last name is required.';
        break;
      case last_name.length < 2:
        last_name_error = 'Last name must be at least 2 characters long.';
        break;
      case !last_name.match(NAME_REGEX):
        last_name_error = 'Last name must start with a capital letter and contain only letters.';
        break;
      default:
        last_name_error = '';
    }
  };
  const check_email = (): void => {
    switch (true) {
      case email.length === 0:
        email_error = 'Email is required.';
        break;
      case !email.match(EMAIL_REGEX):
        email_error = 'Email adress is not valid.';
        break;
      default:
        email_error = '';
    }
  };
  const check_password = (): void => {
    switch (true) {
      case password.length === 0:
        password_error = 'Password is required.';
        break;
      case password.length < 12:
        password_error = 'Password must be at least 12 characters long.';
        break;
      case !password.match(PASSWORD_REGEX):
        password_error = 'Password must contain uppercase letter, lowercase letter, number and special character.';
        break;
      default:
        password_error = '';
    }
  };
  const check_conf_password = (): void => {
    switch (true) {
      case conf_password.length === 0:
        conf_password_error = 'Password confirmation is required.';
        break;
      case conf_password !== password:
        conf_password_error = 'Passwords are not equal.';
        break;
      default:
        conf_password_error = '';
    }
  };
  const check_form = (): void => {
    check_first_name();
    check_last_name();
    check_email();
    check_password();
    check_conf_password();
    if (!(first_name_error || last_name_error || email_error || password_error || conf_password_error)) {
      get_verification_code();
    }
  };

  //-------------------------------------------------------------------------------------------------
  // Verification Code Form Validation
  const check_verification_code = (): void => {
    switch (true) {
      case verification_code === null:
        verification_code_error = 'Verification code is required.';
        break;
      case !verification_code.toString().match(VERIFICATION_CODE_REGEX):
        verification_code_error = 'Verification code is not valid.';
        break;
      default:
        verification_code_error = '';
    }
  };
  const check_verification_code_form = (): void => {
    check_first_name();
    check_last_name();
    check_email();
    check_password();
    check_conf_password();
    check_verification_code();
    if (!(first_name_error || last_name_error || email_error || password_error || conf_password_error || verification_code_error)) {
      register();
    }
  };

  //-------------------------------------------------------------------------------------------------
  // Endpoint calls
  const get_verification_code = (): void => {
    fetch('http://localhost:80/verificationcode', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, action: 'register' }),
    })
      .then((res: Response) => {
        if (res.status === 200) {
          showVerificationForm = true;
          notification = { kind: 'info', title: '', subtitle: '' };
        } else if (res.status === 409) {
          notification = { kind: 'error', title: 'Email already in use.', subtitle: 'Please log in or use different email.' };
        } else {
          notification = { kind: 'error', title: 'Something went wrong.', subtitle: 'Please try again later or contact support.' };
        }
      })
      .catch(() => {
        notification = { kind: 'error', title: 'Something went wrong.', subtitle: 'Please try again later or contact support.' };
      });
  };
  const register = (): void => {
    fetch('http://localhost:80/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ first_name, last_name, email, password, verification_code }),
    })
      .then((res: Response) => {
        if (res.status === 200) {
          window.location.href = '/login';
        } else if (res.status === 403) {
          notification = { kind: 'error', title: 'Incorrect verification code.', subtitle: 'Please try again.' };
          verification_code = 0;
        } else {
          notification = { kind: 'error', title: 'Something went wrong.', subtitle: 'Please try again later or contact support.' };
          verification_code = 0;
        }
      })
      .catch(() => {
        notification = { kind: 'error', title: 'Something went wrong.', subtitle: 'Please try again later or contact support.' };
        verification_code = 0;
      });
  };
</script>

<div id="register" style={'width: 600px; padding: 20px; background-color: white;'}>
  <img src="images/logo.svg" alt="The Flight Booking Company" style="position: relative; left: 10%; width: 80%;" />
  <Form on:submit={check_form}>
    <TextInput bind:value={first_name} on:change={check_first_name} invalid={!!first_name_error} invalidText={first_name_error} labelText="Enter First Name" />
    {#if !!first_name_error} <div style="margin-bottom: 0.7rem;" /> {:else} <div style="margin-bottom: calc(0.7rem + 20px);" /> {/if}
    <TextInput bind:value={last_name} on:change={check_last_name} invalid={!!last_name_error} invalidText={last_name_error} labelText="Enter Last Name" />
    {#if !!last_name_error} <div style="margin-bottom: 0.7rem;" /> {:else} <div style="margin-bottom: calc(0.7rem + 20px);" /> {/if}
    <TextInput bind:value={email} on:change={check_email} invalid={!!email_error} invalidText={email_error} labelText="Enter Email" />
    {#if !!email_error} <div style="margin-bottom: 0.7rem;" /> {:else} <div style="margin-bottom: calc(0.7rem + 20px);" /> {/if}
    <TextInput bind:value={password} on:change={check_password} invalid={!!password_error} invalidText={password_error} labelText="Enter Password" type="password" />
    {#if !!password_error} <div style="margin-bottom: 0.7rem;" /> {:else} <div style="margin-bottom: calc(0.7rem + 20px);" /> {/if}
    <TextInput bind:value={conf_password} on:change={check_conf_password} invalid={!!conf_password_error} invalidText={conf_password_error} labelText="Confirm Password" type="password" />
    {#if !!conf_password_error} <div style="margin-bottom: 0.7rem;" /> {:else} <div style="margin-bottom: calc(0.7rem + 20px);" /> {/if}
    {#if notification.title !== ''}
      <InlineNotification
        kind={notification.kind}
        title={notification.title}
        subtitle={notification.subtitle}
        on:close={() => (notification = { kind: 'info', title: '', subtitle: '' })}
        lowContrast={true}
      />
    {/if}
    <Button style={'width: 100%; max-width: 100%;'} icon={ArrowRight} kind="primary" type="submit">Continue</Button>
    <div style="margin-bottom: 1rem;" />
    <div>Already have an account? <a href="/login" tinro-ignore>Log in</a></div>
  </Form>
  <Modal
    on:close={() => (showVerificationForm = false)}
    on:submit={check_verification_code_form}
    open={showVerificationForm}
    size="sm"
    preventCloseOnClickOutside={true}
    primaryButtonText="Register"
    modalHeading="EMAIL VERIFICATION"
    style="margin-bottom: 0.7rem;"
    id="verification-code-modal"
  >
    For your security, we want to make sure it’s really you. We sent a text message with a 8-digit verification code to your email. Please enter the code below to verify your email.
    <div style="margin-bottom: 1rem;" />
    <TextInput
      bind:value={verification_code}
      on:change={check_verification_code}
      invalid={!!verification_code_error}
      invalidText={verification_code_error}
      labelText="Enter Verification Code"
      placeholder="e.g. 12345678"
    />
    {#if !!verification_code_error} <div style="margin-bottom: 1rem;" /> {:else} <div style="margin-bottom: calc(1rem + 20px);" /> {/if}
  </Modal>
</div>
