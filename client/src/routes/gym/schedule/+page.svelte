<script>
	import * as Tabs from '$lib/components/ui/tabs/index.js';
	import * as Drawer from '$lib/components/ui/drawer';

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
</script>

<Tabs.Root value="mon" class="w-full">
	<Tabs.List class="grid w-full grid-cols-7">
		<Tabs.Trigger value="mon">Mon</Tabs.Trigger>
		<Tabs.Trigger value="tue">Tue</Tabs.Trigger>
		<Tabs.Trigger value="wed">Wed</Tabs.Trigger>
		<Tabs.Trigger value="thu">Thu</Tabs.Trigger>
		<Tabs.Trigger value="fri">Fri</Tabs.Trigger>
		<Tabs.Trigger value="sat">Sat</Tabs.Trigger>
		<Tabs.Trigger value="sun">Sun</Tabs.Trigger>
	</Tabs.List>
	{#each Object.keys(schedule) as day}
		<Tabs.Content value={day}>
			{#each schedule[day] as event}
				<Drawer.Root>
					<Drawer.Trigger>
						<button class="w-full bg-blue-200">
							<div>{event.title}</div>
							<div>{formatTime(event.start)} - {formatTime(event.end)}</div>
						</button>
					</Drawer.Trigger>
					<Drawer.Content>
						<Drawer.Header>
							<Drawer.Title>
								{event.title}
							</Drawer.Title>
							<Drawer.Description>
								{formatTime(event.start)} - {formatTime(event.end)}
							</Drawer.Description>
						</Drawer.Header>
						<Drawer.Footer>
							<Drawer.Close>Close</Drawer.Close>
						</Drawer.Footer>
					</Drawer.Content>
				</Drawer.Root>
			{/each}
		</Tabs.Content>
	{/each}
</Tabs.Root>
