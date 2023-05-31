<script>
  import { onMount } from "svelte";
  import { svcapi, fileapi } from "$lib/fileapi";

  import CodeMirror from "svelte-codemirror-editor";

  //langs
  import { javascript } from "@codemirror/lang-javascript";
  import { css } from "@codemirror/lang-css";
  import { python } from "@codemirror/lang-python";
  import { html } from "@codemirror/lang-html";
  import { json } from "@codemirror/lang-json";
  import { markdown } from "@codemirror/lang-markdown";

  //theme
  import { oneDark } from "@codemirror/theme-one-dark";

  let files = {};
  let snapshots = {};
  let svcs = {};
  let currentfile = "";
  let lang = undefined;
  let filecontents = "File not loaded yet, this is example text. If you're seeing this there might be an error loading the file.";
  const apiURL = "http://localhost:8000/";
  let apis = {"fileapi":new fileapi(apiURL), "svcapi":new svcapi(apiURL)};
  onMount(async function() {
    files = await apis.fileapi.list();
    svcs = await apis.svcapi.list();
    console.log("Files:",files);
  });
  async function save(e){
    console.log("Save:",e);
    return await apis.fileapi.write(currentfile, filecontents);
  }
  async function selected(e){
    console.log("Selected:",e);
    currentfile = e.target.value;
    if( currentfile == "nofile" ){
      currentfile = "";
      filecontents = "";
      snapshots = {};
      return;
    }
    try {
      filecontents = await apis.fileapi.read(currentfile);
      console.log("Contents:",filecontents);
      snapshots = await apis.fileapi.list_snapshots(currentfile);
    } catch(error){
      //currentfile = "";
      filecontents = "Error: Could not load file.\n";
      filecontents += error;
      filecontents += "\nSee console for details";
      set_lang("");
      return;
    }
    let parts = files[currentfile].path.split("/");
    let basename = parts[ parts.length-1];
    let nameparts = basename.split('.');
    let ext = nameparts[ nameparts.length - 1 ];
    set_lang(ext);
  }
  function set_lang(name){
    console.log(`set_lang(name='${name}')`);
    let langs  = {
      "css":css,
      "html":html,
      "json":json,
      "python":python,
      "javascript":javascript,
      "markdown":markdown,

      "conf":python, //not because it's right, but because it'll at least handle comments well
    };
    if( name in langs ){
      lang = langs[name]();
    } else {
      lang = undefined;
    }
    console.log("lang=",lang);
  }
  //TODO: show errors on errors
  //write files on change
  //UI around backups
  //UI for read-only examples
</script>
<style>
.editor {
  width:100%;
  clear:both;
}
.services, .filehistory {
  clear:both;
}
.filehistory button {
}

</style>
<div>
  <div class="services">
    {#if 0 && svcs }
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
	  <td><button on:click="{apis.svcapi.restart(svc.name)}">restart</button></td>
	</tr>
	{/each}
    </table>
    {/if}
  </div>
  <div class="editor">
    <select on:change={selected}>
      <option value="nofile">Select file to edit here</option>
      {#each Object.values(files) as file }
      <option value={file.pathhash}>{file.path}</option>
      {/each}
    </select>
    {#if currentfile }
    <h2>{files[currentfile].path}</h2>
  <div class="filehistory">
    <div class="diff">
    </div>
    <div class="timeline">
      <ul>
      {#each Object.values(snapshots) as snapshot}
	<li>{snapshot}</li>
      {/each}
      </ul>
    </div>
    <button>Older</button>
    <button>Restore</button>
    <button>Newer</button>
  </div>
    <CodeMirror bind:value={filecontents} lang={lang} theme={oneDark} />
    <button on:click={save}>Save</button>
    <!-- With Thanks to https://github.com/touchifyapp/svelte-codemirror-editor and all the upstream projects for making this so easy! -->
    {/if}
  </div>
</div>
