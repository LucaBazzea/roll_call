<script>
	import * as Dialog from '$lib/components/ui/dialog';

	let schedule = {
		mon: [
			{ title: 'No-gi', start: '11:14', end: '12:30', colour: '#f456' },
			{ title: 'No-gi', start: '18:00', end: '19:30', colour: '#f456' }
		],
		tue: [],
		wed: [],
		thu: [
			{ title: 'No-gi', start: '16:00', end: '17:30', colour: '#98fb98' },
			{ title: 'No-gi', start: '18:00', end: '19:30', colour: '#f456' }
		],
		fri: [],
		sat: [],
		sun: []
	};

	let eventDialogOpen = $state(false);
	let eventTitle;
	let eventStart;
	let eventEnd;
	let eventColour;

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

	function eventDialog(title, start, end, colour) {
		eventTitle = title;
		eventStart = start;
		eventEnd = end;
		eventColour = colour;

		eventDialogOpen = true;
	}
</script>

<div class="grid grid-cols-8 p-4 text-sm">
	<div class="col-span-1 border-b-2 border-gray-300 font-bold">Time</div>
	<div class="border-b-1 col-span-1 border-gray-300 text-center font-bold">Monday</div>
	<div class="border-b-1 col-span-1 border-gray-300 text-center font-bold">Tuesday</div>
	<div class="border-b-1 col-span-1 border-gray-300 text-center font-bold">Wednesday</div>
	<div class="border-b-1 col-span-1 border-gray-300 text-center font-bold">Thursday</div>
	<div class="border-b-1 col-span-1 border-gray-300 text-center font-bold">Friday</div>
	<div class="border-b-1 col-span-1 border-gray-300 text-center font-bold">Saturday</div>
	<div class="border-b-1 col-span-1 border-gray-300 text-center font-bold">Sunday</div>

	{#each Array.from({ length: 24 }, (_, i) => i) as hour}
		<div class="col-span-1 font-bold">{formatTime(`${hour}:00`)}</div>
		{#each Object.keys(schedule) as day}
			{#if schedule[day].some((event) => event.start.startsWith(`${hour}:`) || event.end.startsWith(`${hour}:`))}
				<div class="border-1 col-span-1 border-blue-300">
					{#each schedule[day] as event}
						{#if event.start.split(':')[0] === `${hour}` || event.end.split(':')[0] === `${hour}`}
							{#if event.start.split(':')[0] === `${hour}`}
								<button
									onclick={() => eventDialog(event.title, event.start, event.end)}
									class="w-full bg-blue-200"
								>
									<div class="font-bold">{event.title}</div>
									<div class="font-bold">{formatTime(event.start)} - {formatTime(event.end)}</div>
								</button>
							{/if}
							{#if event.end.split(':')[0] === `${hour}`}
								<button
									onclick={() => eventDialog(event.title, event.start, event.end)}
									class="size-full min-h-8 bg-blue-200"
									aria-label="end-time-block"
								></button>
							{/if}
						{/if}
					{/each}
				</div>
			{:else}
				<div class="border-1 col-span-1 border-gray-300"></div>
			{/if}
		{/each}
	{/each}
</div>

<Dialog.Root bind:open={eventDialogOpen}>
	<Dialog.Content>
		<Dialog.Header>
			<Dialog.Title>{eventTitle}</Dialog.Title>
			<Dialog.Description>
				{eventStart} - {eventEnd}
			</Dialog.Description>
		</Dialog.Header>
	</Dialog.Content>
</Dialog.Root>
