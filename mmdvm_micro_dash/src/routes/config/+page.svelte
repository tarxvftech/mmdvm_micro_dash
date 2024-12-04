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

  async function hashString(message) {
    const encoder = new TextEncoder();
    const data = encoder.encode(message);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray.map(byte => byte.toString(16).padStart(2, '0')).join('');
    return hashHex;
  }

  let files = {};
  let snapshots = {};
  let svcs = {};
  let currentfile = "";
  let lang = undefined;
  let filecontents = "";
  let loadedfilecontenthash = "";
  let filecontenthashnew = "";
  let editorerrors = "File not loaded yet, this is example text. If you're seeing this there might be an error loading the file.";
  const apiURL = "http://localhost:8000/";
  let apis = {"fileapi":new fileapi(apiURL), "svcapi":new svcapi(apiURL)};
  onMount(async function() {
    files = await apis.fileapi.list();
    svcs = await apis.svcapi.list();
    console.log("Files:",files);
  });
  let contentschanged = false;
  let loadedrestore = false;
  async function save(e){
    editorerrors = "Saving...";
    console.log("Save:",e);
    try {
      let x = await apis.fileapi.write(currentfile, filecontents);
      editorerrors = "";
      loadedfilecontenthash = await hashString(filecontents);
      contentschanged = false;
      loadedrestore = false;
    } catch(e){
      editorerrors = "Error during save:";
      editorerrors += e;
      loadedfilecontenthash = "";
    }
    try {
      snapshots = await apis.fileapi.list_snapshots(currentfile);
    } catch(e){
      editorerrors = "Error during snapshot load:";
      editorerrors += e;
    }

  }
  async function restore(e){
    console.log("restore:",e);
    //return await apis.fileapi.write(currentfile, filecontents);
    loadedrestore = true;
    contentschanged = false;
    loadedfilecontenthash = await hashString(filecontents);
  }
  async function selected(e){
    console.log("Selected:",e);
    currentfile = e.target.value;
    if( currentfile == "nofile" ){
      currentfile = "";
      filecontents = "";
      editorerrors = "";
      loadedfilecontenthash = "";
      filecontenthashnew = "";
      contentschanged = false;
      loadedrestore = false;
      snapshots = {};
      return;
    }
    try {
      editorerrors = "Loading";
      filecontents = await apis.fileapi.read(currentfile);
      loadedfilecontenthash = await hashString(filecontents);
      filecontenthashnew = "";
      editorerrors = "File Loaded, loading snapshots";
      console.log("Contents:",filecontents,loadedfilecontenthash);
      snapshots = await apis.fileapi.list_snapshots(currentfile);
      if( Object.values(snapshots).length == 0 ){
	//backup();
	let backup = await apis.fileapi.backup(currentfile);
      }
      editorerrors = "";
    } catch(error){
      //currentfile = "";
      editorerrors = "Error: Could not load file.\n";
      editorerrors += error;
      set_lang("");
      filecontents = "";
      loadedfilecontenthash = "";
      snapshots = {};
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
  async function codechange(evt){
    console.log(evt);
    filecontenthashnew = await hashString(filecontents);
    if( loadedfilecontenthash == filecontenthashnew ){
      contentschanged = false;
    }
    else if( loadedfilecontenthash != filecontenthashnew ){
      contentschanged = true;
    }
  }
  //TODO
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
	  <li>
	    <!--<button>Load</button>-->
	    <!--<button>Restore</button>-->
	    <!--<button>Rename</button>-->
	    <!--<button on:click={apis.fileapi.delete(currentfile)}}>Delete</button>-->
	    {snapshot}
	  </li>
	  {/each}
	</ul>
      </div>
      {#if Object.values(snapshots).length }
      <button>Older</button>
      <button>Newer</button>
      {/if}
    </div>
    <div id="editorerrors" >
      {editorerrors}
    </div>
      <CodeMirror bind:value={filecontents} lang={lang} theme={oneDark} on:change="{codechange}" lineWrapping=true />
    {#if contentschanged }
    <button on:click={save}>Save*</button>
    {:else if !contentschanged && loadedrestore }
    <button on:click={restore}>Restore</button>
    {:else}
    <button disabled>(Current file)</button>
    {/if}
    <!-- With Thanks to https://github.com/touchifyapp/svelte-codemirror-editor and all the upstream projects for making this so easy! -->
    {/if}
  </div>
</div>
