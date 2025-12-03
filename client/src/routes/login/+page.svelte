<script>
	const baseURL = 'http://127.0.0.1:8000';

	let formEmail = null;

	async function submitEmail(email) {
		try {
			const response = await fetch(`${baseURL}/app/login/otp/send/`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ email: email })
			});

			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}

			return await response.json();
		} catch (error) {
			console.error('Failed', error);
			return null;
		}
	}
</script>

<div class="flex flex-col h-screen items-center">
	<div class="my-12"></div>
	<div class="mx-auto">
		<h1 class="font-bold text-6xl text-center">RollCall</h1>
	</div>

	<div class="my-12"></div>

	<fieldset class="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4">
		<input type="email" bind:value={formEmail} class="input" placeholder="Email" />

		<button class="btn btn-primary mt-4" onclick={submitEmail(formEmail)}>Login</button>
	</fieldset>
</div>
