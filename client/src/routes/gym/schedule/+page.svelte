<script>
	import { onMount } from 'svelte';

	const baseURL = 'http://127.0.0.1:8000';
	const gymID = '1'; // TODO: Add to store

	const weekdays = [
		{ label: 'Monday', value: 'mon' },
		{ label: 'Tuesday', value: 'tue' },
		{ label: 'Wednesday', value: 'wed' },
		{ label: 'Thursday', value: 'thu' },
		{ label: 'Friday', value: 'fri' },
		{ label: 'Saturday', value: 'sat' },
		{ label: 'Sunday', value: 'sun' }
	];

	const weekdayAbbreviations = {
		mon: 'Monday',
		tue: 'Tuesday',
		wed: 'Wednesday',
		thu: 'Thursday',
		fri: 'Friday',
		sat: 'Saturday',
		sun: 'Sunday'
	};

	async function getSchedule() {
		try {
			const response = await fetch(`${baseURL}/app/schedule/`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ gym_id: gymID })
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

	let schedule = {
		mon: [],
		tue: [],
		wed: [],
		thu: [],
		fri: [],
		sat: [],
		sun: []
	};

	let isAdmin = true;
	let dayToday = 'mon';

	let addClassModal;
	let addClassErrorFlag = false;
	let addClassFormErrors = {};

	// form fields
	$: addClassDay = dayToday;
	let addClassTitle = null;
	let addClassDescription = null;
	let addClassStartHour = null;
	let addClassStartMinute = null;
	let addClassEndHour = null;
	let addClassEndMinute = null;
	let addClassCapacity = null;
	let addClassCoach = null;

	// const addClassFormSchema = z.object({
	// 	day: z.enum(['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'], { message: 'Day is required' }),
	// 	title: z
	// 		.string()
	// 		.min(1, { message: 'Title is required' })
	// 		.max(20, { message: 'Title must be less than 20 characters' })
	// 		.trim(),
	// 	description: z.string().max(200),
	// 	startHour: z.number(),
	// 	startMinute: z.number(),
	// 	endHour: z.number(),
	// 	endMinute: z.number(),
	// 	capacity: z.number(),
	// 	coach: z.string().max(20).trim()
	// });

	async function postAddClassData() {
		addClassFormErrors = {};
		addClassErrorFlag = false;

		const addClassData = {
			day: addClassDay,
			title: addClassTitle,
			description: addClassDescription,
			startHour: Number(addClassStartHour),
			startMinute: Number(addClassStartMinute),
			endHour: Number(addClassEndHour),
			endMinute: Number(addClassEndMinute),
			capacity: Number(addClassCapacity),
			coach: addClassCoach
		};

		const result = addClassFormSchema.safeParse(addClassData);
		if (!result.success) {
			addClassErrorFlag = true;
			addClassFormErrors = result.error.flatten().fieldErrors;
			return;
		}

		try {
			const response = await fetch(`${baseURL}/admin/class/create/`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(addClassData)
			});

			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}

			console.log('Class created:', await response.json());
		} catch (error) {
			console.error('Failed to create class:', error);
			addClassErrorFlag = true;
		}
	}

	function deleteClass() {
		console.log('Class Deleted');
	}

	function formatTime(time) {
		const [hours, minutes] = time.split(':');
		return `${parseInt(hours)}:${minutes}`;
	}

	function getDuration(start, end) {
		const [startHours, startMinutes] = start.split(':').map(Number);
		const [endHours, endMinutes] = end.split(':').map(Number);
		const durationMinutes = endHours * 60 + endMinutes - (startHours * 60 + startMinutes);
		return `${Math.floor(durationMinutes / 60)}h ${durationMinutes % 60}m`;
	}

	onMount(async () => {
		try {
			schedule = await getSchedule();
		} catch (error) {
			console.error('Failed to fetch schedule:', error);
		}
	});
</script>

<!-- Tabs -->
<!-- Schedule -->
<div class="tabs tabs-lift fixed top-0 grid w-full grid-cols-7">
	{#each Object.keys(schedule) as day}
		<input type="radio" name="days" class="tab" aria-label={day.slice(0, 3).toUpperCase()} />
		{#each schedule[day] as event}
			<!-- DaisyUI Card -->
			<div class="tab-content p-6">
				<div class="card card-border w-full">
					<div class="card-body">
						<h2 class="card-title">Card Title</h2>
						<p>
							A card component has a figure, a body part, and inside body there are title and
							actions parts
						</p>
						<div class="card-actions justify-end">
							<button class="btn btn-primary">Buy Now</button>
						</div>
					</div>
				</div>
				<div class="card my-2 bg-base-100 shadow-md">
					<div class="card-body p-4">
						<div class="flex flex-row items-center">
							<div class="rounded-lg p-2 font-bold text-black">
								<p>{formatTime(event.start)}</p>
								<p class="text-xs">
									{getDuration(formatTime(event.start), formatTime(event.end))}
								</p>
							</div>
							<div class="ml-4">
								<h1 class="text-lg font-semibold">{event.title}</h1>
								<p class="text-sm opacity-70">{event.coach}</p>
							</div>
						</div>

						{#if event.capacity}
							<progress
								class="progress progress-primary mt-2 w-full"
								value={event.bookings_count}
								max={event.capacity}
							></progress>
						{/if}
					</div>
				</div>
			</div>
		{/each}
	{/each}
</div>

<!-- Add Class Button -->
{#if isAdmin}
	<div class="fixed bottom-0 w-full">
		<button class="btn btn-secondary w-full rounded-none" onclick={() => addClassModal.showModal()}
			>Add Class</button
		>
	</div>

	<!-- Add Class Modal -->
	<dialog bind:this={addClassModal} class="modal">
		<div class="modal-box w-11/12 max-w-2xl">
			<h3 class="text-lg font-bold">Add Class</h3>
			<p class="py-2">Fill in class info here. Click save when you're done.</p>

			{#if addClassErrorFlag}
				<div class="alert alert-error my-2">
					<span>Please fill in the missing information</span>
				</div>
			{/if}

			<div class="grid gap-4 py-4">
				<!-- Day -->
				<div class="form-control">
					<label class="label" for="add-class-day">Day *</label>
					<select id="add-class-day" bind:value={addClassDay} class="select-bordered select w-full">
						{#each weekdays as day}
							<option value={day.value}>{day.label}</option>
						{/each}
					</select>
				</div>

				<!-- Title -->
				<div class="form-control">
					<label class="label" for="add-class-title">Title *</label>
					<input
						id="add-class-title"
						bind:value={addClassTitle}
						type="text"
						class="input-bordered input w-full"
					/>
					{#if addClassFormErrors.title}
						<p class="text-sm text-red-500">{addClassFormErrors.title[0]}</p>
					{/if}
				</div>

				<!-- Description -->
				<div class="form-control">
					<label class="label" for="add-class-description">Description</label>
					<textarea
						id="add-class-description"
						bind:value={addClassDescription}
						class="textarea-bordered textarea w-full"
					></textarea>
				</div>

				<!-- Start -->
				<div class="form-control">
					<label class="label" for="add-class-time-start">Start *</label>
					<div id="add-class-time-start" class="flex gap-2">
						<input
							bind:value={addClassStartHour}
							type="number"
							placeholder="00"
							class="input-bordered input w-16"
						/>
						<span>:</span>
						<input
							bind:value={addClassStartMinute}
							type="number"
							placeholder="00"
							class="input-bordered input w-16"
						/>
					</div>
				</div>

				<!-- End -->
				<div class="form-control">
					<label class="label" for="add-class-time-end">End *</label>
					<div id="add-class-time-end" class="flex gap-2">
						<input
							bind:value={addClassEndHour}
							type="number"
							placeholder="00"
							class="input-bordered input w-16"
						/>
						<span>:</span>
						<input
							bind:value={addClassEndMinute}
							type="number"
							placeholder="00"
							class="input-bordered input w-16"
						/>
					</div>
				</div>

				<!-- Capacity -->
				<div class="form-control">
					<label class="label" for="add-class-capacity">Capacity</label>
					<input
						id="add-class-capacity"
						bind:value={addClassCapacity}
						type="number"
						placeholder="Max students (optional)"
						class="input-bordered input w-full"
					/>
				</div>

				<!-- Coach -->
				<div class="form-control">
					<label class="label" for="add-class-coach">Coach</label>
					<input
						id="add-class-coach"
						bind:value={addClassCoach}
						type="text"
						class="input-bordered input w-full"
					/>
				</div>
			</div>

			<div class="modal-action">
				<button class="btn btn-primary" onclick={postAddClassData}>Save changes</button>
				<form method="dialog">
					<button class="btn">Cancel</button>
				</form>
			</div>
		</div>
	</dialog>
{/if}
