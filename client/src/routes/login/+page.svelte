<script>
	const baseURL = 'http://127.0.0.1:8000';

	let warningEmail = null;
	let errorEmail = null;

	let formEmail = null;

	async function submitEmail(email) {
		if (email === null || email === '' || !email) {
			warningEmail = 'Email address invalid';
		} else {
			try {
				const response = await fetch(`${baseURL}/app/login/otp/send/`, {
					method: 'POST',
					headers: { 'Content-Type': 'application/json' },
					body: JSON.stringify({ email: email })
				});

				if (!response.ok) {
					errorEmail = 'Error sending OTP';
				}

				if (response.ok) {
					warningEmail = null;
					errorEmail = null;
				}
			} catch (error) {
				errorEmail = 'Error sending OTP';
				return null;
			}
		}
	}
</script>

<div class="flex flex-col h-screen items-center">
	<div class="my-12"></div>
	<div class="mx-auto">
		<h1 class="font-bold text-6xl text-center">RollCall</h1>
	</div>

	{#if errorEmail === null && warningEmail === null}
		<div class="my-12"></div>
	{:else}
		<div class="my-5"></div>
	{/if}

	{#if warningEmail}
		<div role="alert" class="alert alert-warning alert-soft mb-2">
			<span>{warningEmail}</span>
		</div>
	{/if}
	{#if errorEmail}
		<div role="alert" class="alert alert-error alert-soft mb-2">
			<span>{errorEmail}</span>
		</div>
	{/if}

	<fieldset class="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4">
		<input type="email" bind:value={formEmail} class="input" placeholder="Email" />

		<button class="btn btn-primary mt-4" onclick={submitEmail(formEmail)}>Login</button>
	</fieldset>
</div>
