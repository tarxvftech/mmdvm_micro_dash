<script>
  import { onMount } from "svelte";

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

  const apiURL = "http://localhost:8000/";
  let files = {};
  let svcs = {};
  let currentfile = "";
  let lang = undefined;
  let filecontents = "File not loaded yet, this is example text. If you're seeing this there might be an error loading the file.";
  const svcapi = {
    base: apiURL,
    _get: async function (url){
      const r = await fetch(url);
      const c = await r.json();
      console.log(c);
      return c;
    },
    restart: async function (name){
      const r = await fetch( this.base + "services/" + name + "/restart", {
	method: "POST",
      });
      const c = await r.json();
      return c;
    },
    list: async function (){
      let svcs = await this._get( this.base + "services" );
      let statuses = await this._get( this.base + "services/all/status" );
      console.log("svcs,statuses",svcs,statuses);
      for( let s in statuses ){
	svcs[s].status = statuses[s].returncode;
      }
      return svcs;
    },
  };
  const fileapi = {
    base: apiURL,
    _get: async function (url){
      const r = await fetch(url);
      const c = await r.json();
      return c;
    },
    list: async function (){
      return await this._get( this.base + "files/" );
    },
    list_snapshots: async function (hash){
      return await this._get( this.base + "files/" + hash + "/backups" );
    },
    backup: async function (hash){
      const r = await fetch( this.base + "files/" + hash + "/backups", {
	method: "POST",
      });
      const c = await r.json();
      return c;
    },
    restore: async function (hash,bid){
      const r = await fetch( this.base + "files/" + hash + "/backups/" + bid + "/restore", {
	method: "POST",
      });
      const c = await r.json();
      return c;
    },
    read: async function (hash){
      return await this._get( this.base + "files/" + hash + "/read" );
    },
    write: async function (hash, contents){
      let fd = new FormData();
      fd.append("contents", contents);
      const r = await fetch( this.base + "files/" + hash + "/write", {
	method: "PUT",
	body: fd,
      });
      const c = await r.json();
      return c;
    },
  };
  onMount(async function() {
    files = await fileapi.list();
    svcs = await svcapi.list();
    console.log("Files:",files);
  });
  async function save(e){
    console.log("Save:",e);
    return await fileapi.write(currentfile, filecontents);
  }
  async function selected(e){
    console.log("Selected:",e);
    currentfile = e.target.value;
    if( currentfile == "nofile" ){
      currentfile = "";
      filecontents = "";
      return;
    }
    try {
      filecontents = await fileapi.read(currentfile);
      console.log("Contents:",filecontents);
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
.services {
  clear:both;
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
	  <td><button on:click="{svcapi.restart(svc.name)}">restart</button></td>
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
    <CodeMirror bind:value={filecontents} lang={lang} theme={oneDark} />
    <button on:click={save}>Save</button>
    <!-- With Thanks to https://github.com/touchifyapp/svelte-codemirror-editor and all the upstream projects for making this so easy! -->
    {/if}
  </div>
</div>
