<script>
	import { onMount } from 'svelte';

	const baseURL = 'http://127.0.0.1:8000';
	const gymID = 1; // TODO: Add to store

	let csrftoken = null;

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
	let selectedDay = dayToday;

	let selectedClass = null;
	let showClassModal = false;

	function openClassModal(event) {
		selectedClass = event;
		showClassModal = true;
	}

	function closeClassModal() {
		selectedClass = null;
		showClassModal = false;
	}

	let addClassModal;
	let addClassErrorFlag = false;
	let addClassFormErrors = {};

	// form fields
	$: addClassDay = dayToday;
	let addClassTitle = null;
	let addClassDescription = null;
	let addClassStartTime = null;
	let addClassEndTime = null;
	let addClassCapacity = null;
	let addClassCoach = null;

	function updateSelectedDay(day) {
		selectedDay = day;
	}

	async function bookClass() {
		try {
			const response = await fetch(`${baseURL}/app/class/book/`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
				body: JSON.stringify({ gym_id: gymID, class_id: selectedClass['id'] }),
				credentials: 'include'
			});

			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}

			return await response.json();
		} catch (error) {
			console.error('Failed to book class:', error);
			return null;
		}
	}

	async function postAddClass() {
		addClassFormErrors = {};
		addClassErrorFlag = false;

		const addClassData = {
			gym_id: gymID,
			day: addClassDay,
			title: addClassTitle,
			description: addClassDescription,
			time_start: addClassStartTime,
			time_end: addClassEndTime,
			capacity: addClassCapacity ? Number(addClassCapacity) : null,
			coach: addClassCoach
		};

		try {
			const response = await fetch(`${baseURL}/app/admin/class/create/`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
				body: JSON.stringify(addClassData),
				credentials: 'include'
			});

			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}

			console.log('Class created');
			addClassModal.close();
		} catch (error) {
			console.error('Failed to create class');
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

		csrftoken = document.cookie
			.split('; ')
			.find((row) => row.startsWith('csrftoken='))
			?.split('=')[1];
	});
</script>

<!-- Days of the week tabs -->
<div class="tabs tabs-box w-full tabs-sm">
	{#each Object.keys(schedule) as day}
		{#if day === selectedDay}
			<input
				type="radio"
				name="days"
				class="tab flex-1"
				aria-label={day.slice(0, 3).toUpperCase()}
				checked="checked"
			/>
		{:else}
			<input
				type="radio"
				name="days"
				class="tab flex-1"
				aria-label={day.slice(0, 3).toUpperCase()}
				onclick={() => updateSelectedDay(day)}
			/>
		{/if}
	{/each}
</div>

<!-- Classes -->
{#each schedule[selectedDay] as event}
	<div class="mx-2">
		<div class="card card-border my-2 bg-base-100 shadow-md">
			<button class="cursor-pointer" onclick={() => openClassModal(event)}>
				<div class="card-body p-4">
					<div class="flex flex-row items-center">
						<div class="rounded-lg p-2 font-bold text-black bg-blue-400">
							<p>{formatTime(event.start)}</p>
							<p class="text-xs">
								{getDuration(formatTime(event.start), formatTime(event.end))}
							</p>
						</div>
						<div class="text-left ml-4">
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
			</button>
		</div>
	</div>
{/each}

<!-- Class Information Modal -->
{#if showClassModal && selectedClass}
	<div class="modal modal-open">
		<div class="modal-box">
			<div class="mb-2">
				<h2 class="font-bold text-xl">{selectedClass.title}</h2>
				<p>
					{formatTime(selectedClass.start)} - {formatTime(selectedClass.end)}
				</p>
			</div>

			{#if selectedClass.description}
				<div class="flex flex-col">
					<strong>Description:</strong>
					<p>{selectedClass.description}</p>
				</div>
			{/if}

			{#if selectedClass.capacity}
				<div class="flex flex-col">
					<strong>Bookings:</strong>
					<p>
						{selectedClass.bookings_count}/{selectedClass.capacity}
					</p>
				</div>
			{/if}

			{#if selectedClass.coach}
				<div class="flex flex-col">
					<strong>Coach:</strong>
					<p>{selectedClass.coach}</p>
				</div>
			{/if}

			<div class="modal-action">
				<button class="btn btn-primary" onclick={bookClass}>Book</button>
			</div>

			<div class="modal-action">
				<button class="btn" onclick={closeClassModal}>Close</button>
			</div>
		</div>
	</div>
{/if}

<!-- Add Class Button -->
{#if isAdmin}
	<div class="fixed bottom-0 w-full">
		<button class="btn btn-neutral w-full rounded-none" onclick={() => addClassModal.showModal()}>
			Add Class
		</button>
	</div>

	<!-- Add Class Modal -->
	<dialog bind:this={addClassModal} class="modal">
		<div class="modal-box max-w-md">
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
				<div class="form-control flex flex-col">
					<label class="label" for="add-class-time-start">Start *</label>
					<input
						id="add-class-time-start"
						bind:value={addClassStartTime}
						type="time"
						class="input input-bordered w-40"
					/>
				</div>

				<!-- End -->
				<div class="form-control flex flex-col">
					<label class="label" for="add-class-time-end">End *</label>
					<input
						id="add-class-time-end"
						bind:value={addClassEndTime}
						type="time"
						class="input input-bordered w-40"
					/>
				</div>

				<!-- Capacity -->
				<div class="form-control">
					<label class="label" for="add-class-capacity">Maximum Capacity</label>
					<input
						id="add-class-capacity"
						bind:value={addClassCapacity}
						type="number"
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
				<button class="btn btn-primary" onclick={postAddClass}>Save</button>
				<form method="dialog">
					<button class="btn">Cancel</button>
				</form>
			</div>
		</div>
	</dialog>
{/if}
