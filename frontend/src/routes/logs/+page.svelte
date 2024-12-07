<script>
  import { onDestroy } from 'svelte';
  import { onMount } from "svelte";
  import { logapi} from "$lib/microdash";
  import { apiURL, wsURL } from '$lib/config';
  import mqtt from 'mqtt';

  let ws;
  let logs = {};
  let apis = {"logapi":new logapi(apiURL)};
  let pageerror = "Loading...";

  let currentfile = "";
  let mq;

  onMount(async function() {
    try {
      logs = await apis.logapi.list();
      console.log(logs);
      pageerror = "";
    }catch(e){
      console.log(e);
    }
    mq = mqtt.connect(wsURL);

    mq.on('connect', () => {
      mq.subscribe('logs/#');
      //mq.publish('svelte/topic', 'Hello from Svelte');
    });

    mq.on('message', (topic, message) => {
      let m = message.toString();
      console.log(topic,m);
      if( topic.startsWith("logs/") ){
        let filename = topic.slice(5);
        if( filename in logs ){
          logs[filename].push(m)
        } else {
          logs[filename] = [m];
        }
        logs[filename] = logs[filename];
      }
    });
  });
  onDestroy(() => {
    mq.end();
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
    <select on:change={selected}>
      <option value="">Select log to view</option>
      {#each Object.keys(logs) as file }
      <option value={file}>{file}</option>
      {/each}
    </select>
    <div class="error">{pageerror}</div>
    <div>
    {#if currentfile }
      <h2>{currentfile}</h2>
      <pre>{#each logs[currentfile] as line }{line + "\n"}{/each}</pre> 
    {/if}
    </div>
  </div>
</div>
