<script lang="ts">
    import { onMount } from "svelte";
    import { api_url } from "../lib/store";  

    let flights

    onMount(() => {
        fetch($api_url + "/flights", {
            method: "GET",
            headers: { 
                "Content-Type": "application/json",
                "Authorization": "Bearer " + localStorage.getItem("access_token")
            },
        })
        .then((res: Response) => {
            if (res.status === 200) { 
                res.json().then((data: any) => {
                    flights = data
                });
                console.log(flights)
            } else if (res.status === 401){
                localStorage.setItem("access_token", "");
                window.location.href = "/login";
            } else {
                console.log("Error: " + res.status);
            }
        })
        .catch((err: Error) => {
            console.log(err);
        });
    })

</script>

<div id="home">
    {flights}
</div>

<style>
    #home {
        background-color: lightgoldenrodyellow;
        width: 100%;
        height: 100%;
    }
</style>