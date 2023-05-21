<script>
    import CodeMirror from "svelte-codemirror-editor";

    let value = "File not loaded yet, this is example text";
</script>
<style>
  .editor {
  width:100%;
  }
</style>
<div class="editor">
<h2>Filename.txt</h2>
<CodeMirror bind:value />
</div>

