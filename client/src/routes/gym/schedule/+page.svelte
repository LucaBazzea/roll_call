<script>
	let schedule = {
		mon: [
			{ start: '11:00', end: '12:30' },
			{ start: '18:00', end: '19:30' }
		],
		tue: [],
		wed: [],
		thu: [
			{ start: '16:00', end: '17:30' },
			{ start: '18:00', end: '19:30' }
		],
		fri: [],
		sat: [],
		sun: []
	};

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
</script>

<div class="grid grid-cols-8 gap-4 text-sm">
	<div class="col-span-1 font-bold">Time</div>
	<div class="col-span-1 font-bold">Monday</div>
	<div class="col-span-1 font-bold">Tuesday</div>
	<div class="col-span-1 font-bold">Wednesday</div>
	<div class="col-span-1 font-bold">Thursday</div>
	<div class="col-span-1 font-bold">Friday</div>
	<div class="col-span-1 font-bold">Saturday</div>
	<div class="col-span-1 font-bold">Sunday</div>

	{#each Array.from({ length: 24 }, (_, i) => i) as hour}
		<div class="col-span-1 font-bold">{formatTime(`${hour}:00`)}</div>
		{#each Object.keys(schedule) as day}
			<div class="col-span-1">
				{#each schedule[day] as event}
					{#if event.start.split(':')[0] === `${hour}`}
						<div class="mb-2 rounded-md bg-blue-200 p-2">
							<div class="font-bold">{formatTime(event.start)} - {formatTime(event.end)}</div>
							<div>{getDuration(event.start, event.end)}</div>
						</div>
					{/if}
				{/each}
			</div>
		{/each}
	{/each}
</div>
