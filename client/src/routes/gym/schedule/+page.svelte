<script>
	import * as Dialog from '$lib/components/ui/dialog';
	import * as Tabs from '$lib/components/ui/tabs/index.js';
	import { Button } from '$lib/components/ui/button/index.js';

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
				<button
					onclick={() => eventDialog(event.title, event.start, event.end, event.colour)}
					class="w-full bg-blue-200"
				>
					<div>{event.title}</div>
					<div>{formatTime(event.start)} - {formatTime(event.end)}</div>
				</button>
			{/each}
		</Tabs.Content>
	{/each}
</Tabs.Root>

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
