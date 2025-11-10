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

	$: schedule = {
		mon: { date: null, classes: null },
		tue: { date: null, classes: null },
		wed: { date: null, classes: null },
		thu: { date: null, classes: null },
		fri: { date: null, classes: null },
		sat: { date: null, classes: null },
		sun: { date: null, classes: null }
	};

	let isAdmin = true;
	let dayToday = 'mon';
	$: selectedDay = dayToday;

	let messageToast = null;

	let selectedClass = null;
	let showClassModal = false;
	let classModalWarning = null;
	let classModalError = null;

	function showMessageToast(message) {
		messageToast = message;
		setTimeout(() => {
			messageToast = null;
		}, 5000);
	}

	function openClassModal(event) {
		selectedClass = event;
		showClassModal = true;
	}

	function closeClassModal() {
		selectedClass = null;
		showClassModal = false;

		classModalWarning = null;
		classModalError = null;
	}

	function showClassModalAlert(type, message) {
		if (type === 'warning') {
			classModalWarning = message;
		} else if (type === 'error') {
			classModalError = message;
		}
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
			if (response.status === 200) {
				closeClassModal();
				schedule = await getSchedule();
				showMessageToast('Class booked, train hard!');
			}

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
			schedule = await getSchedule();
		} catch (error) {
			console.error('Failed to create class');
			addClassErrorFlag = true;
		}
	}

	// Delete Class //
	$: deleteClassModal = false;

	function showDeleteClassModal() {
		showClassModal = false;
		deleteClassModal = true;
	}

	function closeDeleteClassModal() {
		deleteClassModal = false;
	}

	function cancelDeleteClassModal() {
		deleteClassModal = false;
		openClassModal(selectedClass);
	}

	async function deleteClass(class_id) {
		try {
			const response = await fetch(`${baseURL}/app/admin/class/delete/`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
				body: JSON.stringify({ gym_id: gymID, class_id: class_id }),
				credentials: 'include'
			});

			closeDeleteClassModal();

			if (response.status === 200) {
				closeClassModal();
				schedule = await getSchedule();
				showMessageToast('Class deleted');
			}

			if (!response.ok) {
				showClassModalAlert('warning', 'Failed to delete class');
			}
		} catch (error) {
			showClassModalAlert('warning', 'Failed to delete class');
		}
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

		// The day today will be the first day in the schedule dict
		dayToday = Object.keys(schedule)[0];

		csrftoken = document.cookie
			.split('; ')
			.find((row) => row.startsWith('csrftoken='))
			?.split('=')[1];
	});
</script>

<div class="toast toast-center w-full mb-8">
	{#if messageToast}
		<div class="alert alert-success">
			<span>{messageToast}</span>
		</div>
	{/if}
</div>

{#if deleteClassModal === true}
	<div class="modal modal-open">
		<div class="modal-box">
			<h3 class="text-lg font-bold">Delete class "{selectedClass.title}"?</h3>
			<p class="py-4">This action is irreversible</p>
			<div class="flex flex-row space-x-2">
				<div class="modal-action w-full">
					<button class="btn btn-md w-full" onclick={cancelDeleteClassModal}>Cancel</button>
				</div>
				<div class="modal-action w-full">
					<button class="btn btn-secondary btn-md w-full" onclick={deleteClass(selectedClass.id)}
						>Delete</button
					>
				</div>
			</div>
		</div>
	</div>
{/if}

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
{#if schedule[selectedDay]?.classes && schedule[selectedDay].classes.length > 0}
	{#each schedule[selectedDay]?.classes as event}
		<div class="mx-2">
			<div class="card card-border my-2 bg-base-100 shadow-md">
				<button class="cursor-pointer" onclick={() => openClassModal(event)}>
					<div class="card-body p-4">
						<div class="flex flex-row items-center">
							<div class="rounded-lg p-2 font-bold text-black bg-primary">
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
								class="progress mt-2 w-full"
								value={event.bookings_count}
								max={event.capacity}
							></progress>
						{/if}
					</div>
				</button>
			</div>
		</div>
	{/each}
{:else}
	<div class="mx-2 my-4 text-center text-gray-500">No classes scheduled</div>
{/if}

<!-- Class Information Modal -->
{#if showClassModal && selectedClass}
	<div class="modal modal-open">
		<div class="modal-box">
			{#if classModalWarning}
				<div role="alert" class="alert alert-warning alert-soft">
					<span>{classModalWarning}</span>
				</div>
			{/if}
			{#if classModalError}
				<div role="alert" class="alert alert-error alert-soft">
					<span>{classModalError}</span>
				</div>
			{/if}
			<div class="flex flex-row justify-between">
				<h2 class="font-bold text-xl">{selectedClass.title}</h2>

				<details class="dropdown dropdown-bottom dropdown-end">
					<summary class="btn btn-xs">Options</summary>
					<ul class="menu dropdown-content bg-base-100 rounded-box z-1 w-52 p-2 shadow-sm">
						{#if isAdmin === true}
							<li>
								<button onclick={showDeleteClassModal}> Delete </button>
							</li>
							<li>
								<button> Edit </button>
							</li>
						{/if}
					</ul>
				</details>
			</div>

			<div class="divider my-0"></div>

			<div class="space-y-2">
				<div class="flex flex-row space-x-4">
					<div class="flex flex-col">
						<h4 class="font-bold text-md">Start</h4>
						<p class="text-xl/6">
							{formatTime(selectedClass.start)}
						</p>
					</div>
					<div class="flex flex-col">
						<h4 class="font-bold text-md">End</h4>
						<p class="text-xl/6">
							{formatTime(selectedClass.end)}
						</p>
					</div>
				</div>

				{#if selectedClass.description}
					<div class="flex flex-col">
						<h4 class="font-bold text-md mb-1">Description</h4>
						<div class="card bg-neutral text-neutral-content rounded-field p-2 w-full">
							<p class="text-sm">{selectedClass.description}</p>
						</div>
					</div>
				{/if}

				{#if selectedClass.coach}
					<div class="flex flex-col">
						<h4 class="font-bold text-md">Coach</h4>
						<p class="text-xl/6">{selectedClass.coach}</p>
					</div>
				{/if}
			</div>

			<div class="flex flex-row items-center space-x-2">
				<div class="modal-action w-full">
					<button class="btn btn-md btn-neutral w-full" onclick={closeClassModal}> Close </button>
				</div>

				<div class="modal-action w-full">
					{#if selectedClass.capacity}
						{#if selectedClass.bookings_count === selectedClass.capacity}
							<button class="btn btn-md btn-secondary w-full" onclick={bookClass}
								>Book {selectedClass.bookings_count}/{selectedClass.capacity}</button
							>
						{:else}
							<button class="btn btn-md btn-primary w-full" onclick={bookClass}
								>Book {selectedClass.bookings_count}/{selectedClass.capacity}</button
							>
						{/if}
					{:else}
						<button class="btn btn-md btn-primary w-full" onclick={bookClass}>Book</button>
					{/if}
				</div>
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
