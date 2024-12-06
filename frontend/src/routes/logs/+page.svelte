<script>
  import { onDestroy } from 'svelte';
  import { onMount } from "svelte";
  import { logapi} from "$lib/microdash";
  import { apiURL, wsURL } from '$lib/config';

  let ws;
  let logs = {};
  let apis = {"logapi":new logapi(apiURL)};
  let pageerror = "Loading...";

  let currentfile = "";

  function wsconnect() {
    ws = new WebSocket(wsURL);

    ws.onopen = () => {
      console.log('WebSocket connected');
    };

    ws.onmessage = (event) => {
      console.log(event);
      const data = JSON.parse(event.data);
      console.log(data);
      for( let key in data ){
        if( key in logs ){
          logs[key] = data[key];
        }
      }
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
      //setTimeout(wsconnect, 1000);
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      //setTimeout(wsconnect, 5000);
    };
  }

  onMount(async function() {
    try {
      logs = await apis.logapi.list();
      console.log(logs);
      pageerror = "";
      wsconnect();
    }catch(e){
      console.log(e);
    }
  });
  onDestroy(() => {
    if (ws) {
      ws.close();
    }
  });
  async function selected(e){
    console.log("Selected:",e);
    currentfile = e.target.value;
  }
</script>
<style>
  .logs {
    clear: both;
  }
</style>
<div>
  <div class="logs">
    <div class="error">{pageerror}</div>
    <select on:change={selected}>
      <option value="">Select log to view</option>
      {#each Object.keys(logs) as file }
      <option value={file}>{file}</option>
      {/each}
    </select>
    <div>
    {#if currentfile }
      <h2>{currentfile}</h2>
      <pre>{#each logs[currentfile] as line }{line + "\n"}{/each}</pre> 
    {/if}
    </div>
  </div>
</div>
