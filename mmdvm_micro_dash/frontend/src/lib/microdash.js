
class svcapi {
  constructor(apiURL){
	console.log(apiURL);
	this.base = apiURL;
  }
  async _get(url){
    const r = await fetch(url);
    const c = await r.json();
    console.log(c);
    return c;
  }
  async exec(verb,name){
    const r = await fetch( this.base + "services/" + name + "/" + verb, {
      method: "POST",
    });
    const c = await r.json();
    console.log(verb,name,c);
    return c;
  }
  async status(name){
    const r = await fetch( this.base + "services/" + name + "/" + "status", {
      method: "GET",
    });
    const c = await r.json();
    console.log("status",name,c);
    return c;
  }
  async start(name){
    return await this.exec("start",name);
  }
  async restart(name){
    return await this.exec("restart",name);
  }
  async stop(name){
    return await this.exec("stop",name);
  }
  async enable(name){
    return await this.exec("enable",name);
  }
  async disable(name){
    return await this.exec("disable",name);
  }
  async list(){
    let svcs = await this._get( this.base + "services" );
    let statuses = await this._get( this.base + "services/all/status" );
    console.log("svcs,statuses",svcs,statuses);
    for( let s in statuses ){
      svcs[s].status = statuses[s].returncode;
    }
    return svcs;
  }
};
class fileapi {
  constructor(apiURL){
	console.log(apiURL);
	this.base = apiURL;
  }
  async _get(url){
    console.log(url);
    const r = await fetch(url);
    const c = await r.json();
    return c;
  }
  async list(){
    return await this._get( this.base + "files/" );
  }
  async list_snapshots(hash){
    return await this._get( this.base + "files/" + hash + "/backups" );
  }
  async backup(hash){
    const r = await fetch( this.base + "files/" + hash + "/backups", {
      method: "POST",
    });
    const c = await r.json();
    return c;
  }
  async restore(hash,bid){
    const r = await fetch( this.base + "files/" + hash + "/backups/" + bid + "/restore", {
      method: "POST",
    });
    const c = await r.json();
    return c;
  }
  async read(hash){
    return await this._get( this.base + "files/" + hash + "/read" );
  }
  async write(hash, contents){
    const r = await fetch( this.base + "files/" + hash + "/write", {
      method: "PUT",
      headers: {
	"Content-Type": "application/octet-stream" 
      },
      body: contents instanceof Uint8Array ? contents : new TextEncoder().encode(contents),
    });
    const c = await r.json();
    return c;
  }
};

export { fileapi, svcapi };
