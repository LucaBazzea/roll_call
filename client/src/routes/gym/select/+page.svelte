<script>
	import { onMount } from 'svelte';

	const baseURL = 'http://127.0.0.1:8000';

	let gyms = null;

	async function getGyms() {
		try {
			const response = await fetch(`${baseURL}/app/user/gyms/`, {
				method: 'GET',
				headers: { 'Content-Type': 'application/json' }
			});

			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}

			return await response.json();
		} catch (error) {
			console.error('Failed to fetch schedule:', error);
			return null;
		}
	}

	onMount(async () => {
		try {
			gyms = await getGyms();
		} catch (error) {
			console.error('Failed to fetch gyms:', error);
		}

		csrftoken = document.cookie
			.split('; ')
			.find((row) => row.startsWith('csrftoken='))
			?.split('=')[1];
	});
</script>

<div>
	{#if gyms}
		{#each Object.keys(gyms) as gym}
			<div>{gym}</div>
		{/each}
	{:else}
		<p>No gyms :(</p>
	{/if}
</div>
