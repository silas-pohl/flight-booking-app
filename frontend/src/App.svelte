<script lang="ts">
  import { Route } from 'tinro'; 
  import Login from "./pages/Login.svelte";
  import Register from "./pages/Register.svelte";
  import Home from "./pages/Home.svelte";
  import { Header, HeaderActionLink, HeaderActionSearch, HeaderGlobalAction, HeaderNav, HeaderNavItem, HeaderNavMenu, HeaderPanelDivider, HeaderPanelLink, HeaderUtilities, Icon } from "carbon-components-svelte";
  import UserAvatar from "carbon-icons-svelte/lib/UserAvatar24";
  import Information from "carbon-icons-svelte/lib/Information24";
</script>

<Header 
    platformName="FLIGHT BOOKING COMPANY"
    href="/"
    style="padding-right: 16px;"
  >
    <HeaderActionLink
      href="/account"
      icon={UserAvatar}
      label="Account"
      style="padding-top: 12px !important; position: absolute; right: 0px;"
    />
    <HeaderActionLink
      href="/about"
      icon={Information}
      label="About"
      style="padding-top: 12px !important; position: absolute; right: 48px;"
    />
  </Header>
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