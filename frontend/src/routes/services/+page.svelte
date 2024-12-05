<script>
  import { onMount } from "svelte";
  import { svcapi} from "$lib/microdash";

  let svcs = {};
  const apiURL = "http://localhost:8000/";
  let apis = {"svcapi":new svcapi(apiURL)};
  onMount(async function() {
    svcs = await apis.svcapi.list();
  });
</script>
<style>
.services {
  clear:both;
}

</style>
<div>
  <div class="services">
    {#if svcs }
    <table>
      <tr>
	<th>name</th>
	<th>status</th>
	<th>do</th>
      </tr>
      {#each Object.values(svcs) as svc }
      <tr>
	<th>{svc.name}</th>
	<td>{svc.status}</td>
	<td><button on:click="{apis.svcapi.status(svc.name)}">status</button></td>
	<td><button on:click="{apis.svcapi.start(svc.name)}">start/enable</button></td>
	<td><button on:click="{apis.svcapi.restart(svc.name)}">restart</button></td>
	<td><button on:click="{apis.svcapi.stop(svc.name)}">stop/disable</button></td>
      </tr>
      {/each}
    </table>
    {/if}
  </div>
</div>
