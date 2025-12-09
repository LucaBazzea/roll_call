<script>
	const baseURL = 'http://127.0.0.1:8000';

	let otpSent = true;

	let warningEmail = null;
	let errorEmail = null;

	let formEmail = 'email@example.com';

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
	<div class="my-2"></div>
	<div class="mx-auto">
		<h1 class="font-bold text-xl text-center">RollCall</h1>
	</div>

	{#if otpSent === true}
		<div class="my-12"></div>
		<h2 class="font-bold text-2xl my-2 text-center">We emailed you an OTP</h2>
		<div class="px-6 text-center">
			<p>
				We’ve sent an email to <strong>{formEmail}</strong>, enter the OTP here.
			</p>
		</div>

		<div class="flex flex-col my-6 px-6">
			<input
				type="text"
				inputmode="numeric"
				class="input validator text-center text-xl py-6"
				required
				placeholder="OTP"
				maxlength="6"
				title="OTP is 6 digits long and comprised of numbers"
			/>
			<p class="validator-hint">6 digit OTP</p>
			<button class="btn btn-primary w-full">Submit</button>
		</div>

		<p class="text-sm mx-8">If you can’t see the email, check your spam or junk folder.</p>
		<p>
			Can't find your code? <button class="btn-link" onclick={submitEmail(formEmail)}
				>Request a new OTP</button
			>
		</p>
	{:else}
		{#if errorEmail === null && warningEmail === null}
			<div class="my-12"></div>
		{:else}
			<div class="my-5"></div>
		{/if}

		{#if warningEmail}
			<div role="alert" class="alert alert-warning alert-outline mb-2">
				<span>{warningEmail}</span>
			</div>
		{/if}
		{#if errorEmail}
			<div role="alert" class="alert alert-error alert-outline mb-2">
				<span>{errorEmail}</span>
			</div>
		{/if}

		<fieldset class="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4">
			<input type="email" bind:value={formEmail} class="input" placeholder="Email" />

			<button class="btn btn-primary mt-4" onclick={submitEmail(formEmail)}>Login</button>
		</fieldset>
	{/if}
</div>
