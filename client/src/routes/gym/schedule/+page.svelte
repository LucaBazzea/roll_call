<script>
	import { onMount } from 'svelte';
	import { z } from 'zod';

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

	const addClassFormSchema = z.object({
		day: z.enum(['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'], { message: 'Day is required' }),
		title: z
			.string()
			.min(1, { message: 'Title is required' })
			.max(20, { message: 'Title must be less than 20 characters' })
			.trim(),
		description: z.string().max(200),
		startHour: z.number(),
		startMinute: z.number(),
		endHour: z.number(),
		endMinute: z.number(),
		capacity: z.number(),
		coach: z.string().max(20).trim()
	});

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
<div class="tabs fixed top-0 grid w-full grid-cols-7">
	{#each Object.keys(schedule) as day}
		<button
			class="tab tab-bordered"
			class:tab-active={dayToday === day}
			onclick={() => (dayToday = day)}
		>
			{day.slice(0, 3).toUpperCase()}
		</button>
	{/each}
</div>

<!-- Schedule -->
{#each Object.keys(schedule) as day}
	{#if dayToday === day}
		{#each schedule[day] as event}
			<!-- DaisyUI Card -->
			<div class="card bg-base-100 my-2 shadow-md">
				<div class="card-body p-4">
					<div class="flex flex-row items-center">
						<div class="rounded-lg bg-blue-400 p-2 font-bold text-black">
							<p>{formatTime(event.start)}</p>
							<p class="text-xs">{getDuration(formatTime(event.start), formatTime(event.end))}</p>
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

					<div class="card-actions mt-4 justify-end">
						<button class="btn btn-primary">Book</button>
						<button class="btn" onclick={showDetailsModal}> Details </button>
					</div>
				</div>
			</div>

			<!-- Details Modal -->
			<dialog id="details_modal" class="modal">
				<div class="modal-box">
					<h3 class="text-lg font-bold">{event.title}</h3>
					<p class="py-2">{formatTime(event.start)} - {formatTime(event.end)}</p>
					<div class="mt-2 flex items-center gap-4">
						<div class="avatar">
							<div class="w-12 rounded-full">
								<img src="https://avatars.githubusercontent.com/u/33540116" alt="Coach" />
							</div>
						</div>
						<div>
							<h3 class="text-md font-medium">{event.coach}</h3>
						</div>
					</div>
					<div class="modal-action">
						<form method="dialog">
							<button class="btn">Close</button>
						</form>
						{#if isAdmin}
							<button class="btn btn-error" onclick={deleteClass}>Delete Class</button>
						{/if}
					</div>
				</div>
			</dialog>
		{/each}
	{/if}
{/each}

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
					<select id="add-class-day" bind:value={addClassDay} class="select select-bordered w-full">
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
						class="input input-bordered w-full"
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
						class="textarea textarea-bordered w-full"
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
							class="input input-bordered w-16"
						/>
						<span>:</span>
						<input
							bind:value={addClassStartMinute}
							type="number"
							placeholder="00"
							class="input input-bordered w-16"
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
							class="input input-bordered w-16"
						/>
						<span>:</span>
						<input
							bind:value={addClassEndMinute}
							type="number"
							placeholder="00"
							class="input input-bordered w-16"
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
						class="input input-bordered w-full"
					/>
				</div>

				<!-- Coach -->
				<div class="form-control">
					<label class="label" for="add-class-coach">Coach</label>
					<input
						id="add-class-coach"
						bind:value={addClassCoach}
						type="text"
						class="input input-bordered w-full"
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
