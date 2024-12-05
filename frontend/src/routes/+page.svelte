<script>
	import Time from "svelte-time";
	const columns = ["Type","Mode","Time","Length","From","To","BER"];
	//const columns = ["Type","From","To","BER"];
	let timeouts = [];
	if( timeouts.length ){
		for( let t of timeouts ){
			console.log(t);
		}
	}
	let lastheard = [
	];
	lastheard.maxq = 15;
	lastheard.forceUpdate = function(){
		lastheard = lastheard; //reactivity force for svelte
		if( lastheard.length > lastheard.maxq ){
			lastheard.pop();
		}
	}

	function demo(){
		const talktime = 20;
		const waittime = 5;
		const talkers = ["KC1AWV","W2FBI","SP5WWP","G4KLX","VK3JED","N2XDD","N7TAE","WX9O"]; //etc
		const idx = Math.floor(Math.random() * talkers.length)
		const tx = talkers[idx];
		const ber = Math.random().toFixed(2);
		const txtype = tx == "W2FBI"? "RF" : "Net";
		const len = Math.random() * talktime * 1000; //60
		const lens = (len/1000).toFixed(1) + " s";

		const pushme = {Type:txtype, Mode:"M17", Time:new Date(), Length:lens, From: tx, To: "M17-M17 C", BER:ber};
		console.log("New!", pushme, lastheard.length);
		lastheard.splice(0,0, pushme );
		//TODO: live updates and counting length up as a call is happening and then close it off once it's done
		timeouts.push(setTimeout(demo, len + Math.random()*waittime*1000)); //10
		lastheard.forceUpdate();
	}
	demo();
</script>
<style>
</style>

<table>
	<tr>
		{#each columns as col}
			<th>{col}</th>
		{/each}
	</tr>

	{#each lastheard as e}
		<tr>
			{#each columns as col}
				{#if col == "Time" }
					<td><Time timestamp="{e[col]}" live="10" relative /></td>
				{:else}
					<td>{ e[col] }</td>
				{/if}
			{/each}
		</tr>
	{/each}
</table>
