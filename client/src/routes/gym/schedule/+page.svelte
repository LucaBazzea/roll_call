<script>
	import { Badge } from '$lib/components/ui/badge/index.js';
	import * as Tabs from '$lib/components/ui/tabs/index.js';
	import * as Drawer from '$lib/components/ui/drawer';
	import * as Avatar from '$lib/components/ui/avatar';
	import * as Card from '$lib/components/ui/card/index.js';
	import { Button, buttonVariants } from '$lib/components/ui/button/index.js';
	import * as Dialog from '$lib/components/ui/dialog/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Label } from '$lib/components/ui/label/index.js';
	import * as Select from "$lib/components/ui/select";
	import { Textarea } from "$lib/components/ui/textarea/index.js";

	const weekdays = [
		{ label: "Monday", value: "mon" },
		{ label: "Tuesday", value: "tue" },
		{ label: "Wednesday", value: "wed" },
		{ label: "Thursday", value: "thu" },
		{ label: "Friday", value: "fri" },
		{ label: "Saturday", value: "sat" },
		{ label: "Sunday", value: "sun" }
	];

	let schedule = {
		mon: [
			{ title: 'No-gi', start: '11:14', end: '12:30', colour: '#f456', coach: 'Andre Ben' },
			{
				title: 'No-gi Pressure Passing',
				start: '18:00',
				end: '19:30',
				colour: '#f456',
				coach: 'Milton Friedman'
			}
		],
		tue: [],
		wed: [],
		thu: [
			{ title: 'No-gi', start: '16:00', end: '17:30', colour: '#98fb98', coach: 'Epictetus' },
			{ title: 'No-gi', start: '18:00', end: '19:30', colour: '#f456', coach: 'Plato' }
		],
		fri: [],
		sat: [],
		sun: []
	};

	// TODO: Put this in store
	let isAdmin = true;

	let dayToday = 'mon';

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

<Tabs.Root value={dayToday} class="w-full">
	<Tabs.List class="grid w-full grid-cols-7">
		<Tabs.Trigger value="mon">Mon</Tabs.Trigger>
		<Tabs.Trigger value="tue">Tue</Tabs.Trigger>
		<Tabs.Trigger value="wed">Wed</Tabs.Trigger>
		<Tabs.Trigger value="thu">Thu</Tabs.Trigger>
		<Tabs.Trigger value="fri">Fri</Tabs.Trigger>
		<Tabs.Trigger value="sat">Sat</Tabs.Trigger>
		<Tabs.Trigger value="sun">Sun</Tabs.Trigger>
	</Tabs.List>

	{#if isAdmin}
		<nav class="flex flex-row justify-between border bg-yellow-400 p-2">
			<Badge>Admin</Badge>
			<Dialog.Root>
				<Dialog.Trigger>
					<Button>Add Class</Button>
				</Dialog.Trigger>
				<Dialog.Content class="sm:max-w-[425px] border-yellow-400 rouned-md">
					<Dialog.Header>
						<Dialog.Title>Add Class</Dialog.Title>
						<Dialog.Description>
							Fill in class info here. Click save when you're done.
						</Dialog.Description>
					</Dialog.Header>
					<div class="grid gap-4 py-4">
						<div class="grid grid-cols-4 items-center gap-4">
							<Label for="addClassDay" class="text-right">Day *</Label>
							<Select.Root portal={null}>
							  <Select.Trigger class="w-[180px]">
							    <Select.Value placeholder="Day" />
							  </Select.Trigger>
							  <Select.Content>
							    <Select.Group>
							      {#each weekdays as day}
								<Select.Item value={day.value} label={day.label}
								  >{day.label}</Select.Item
								>
							      {/each}
							    </Select.Group>
							  </Select.Content>
							  <Select.Input name="favoriteFruit" />
							</Select.Root>
						</div>
						<div class="grid grid-cols-4 items-center gap-4">
							<Label for="title" class="text-right">Title *</Label>
							<Input id="title" value="" class="col-span-3" />
						</div>
						<div class="grid grid-cols-4 items-center gap-4">
							<Label for="description" class="text-right">Description</Label>
							<Textarea id="description" value="" class="col-span-3" placeholder="Description (optional)" />
						</div>
						<div class="grid grid-cols-4 items-center gap-4">
							<Label for="username" class="text-right">Start *</Label>
							<div class="flex flex-row col-span-3">
								<Input id="username" value="00" class="col-span-3" />
								<p>:</p>
								<Input id="username" value="00" class="col-span-3" />
							</div>
						</div>
						<div class="grid grid-cols-4 items-center gap-4">
							<Label for="username" class="text-right">End *</Label>
							<div class="flex flex-row col-span-3">
								<Input id="username" value="00" class="col-span-3" />
								<p>:</p>
								<Input id="username" value="00" class="col-span-3" />
							</div>
						</div>
						<div class="grid grid-cols-4 items-center gap-4">
							<Label for="username" class="text-right">Coach</Label>
							<Input id="username" value="" class="col-span-3" />
						</div>
					</div>
					<Dialog.Footer>
						<Button type="submit">Save changes</Button>
					</Dialog.Footer>
				</Dialog.Content>
			</Dialog.Root>
		</nav>
	{/if}

	{#each Object.keys(schedule) as day}
		<Tabs.Content value={day}>
			{#each schedule[day] as event}
				<Drawer.Root>
					<Drawer.Trigger class="w-full p-2">
						<div class="flex flex-row rounded-md border px-4 py-3">
							<div class="my-auto rounded-lg bg-blue-400 p-2">
								<p class="text-md font-bold text-black">{formatTime(event.start)}</p>
								<p class="text-xs font-bold text-black">
									{getDuration(formatTime(event.start), formatTime(event.end))}
								</p>
							</div>
							<div class="mx-4 my-auto flex flex-col text-left">
								<h1 class="text-lg">{event.title}</h1>
								<Card.Description>
									{event.coach}
								</Card.Description>
							</div>
						</div>
					</Drawer.Trigger>
					<Drawer.Content>
						<Drawer.Header>
							<Drawer.Title>
								<h1 class="text-lg">
									{event.title}
								</h1>
							</Drawer.Title>
							<Drawer.Description>
								{formatTime(event.start)} - {formatTime(event.end)}
							</Drawer.Description>
							<div class="flex flex-row rounded-md border px-4 py-3">
								<Avatar.Root>
									<Avatar.Image
										src="https://avatars.githubusercontent.com/u/33540116"
										alt="Coach's Avatar"
									/>
									<Avatar.Fallback>Coach</Avatar.Fallback>
								</Avatar.Root>
								<div class="mx-4 my-auto flex flex-col">
									<h3 class="text-md">{event.coach}</h3>
								</div>
							</div>
						</Drawer.Header>
						<Drawer.Footer>
							<Button>Book</Button>
							<Drawer.Close>
								<Button class="w-full" variant="outline">Close</Button>
							</Drawer.Close>
						</Drawer.Footer>
					</Drawer.Content>
				</Drawer.Root>
			{/each}
		</Tabs.Content>
	{/each}
</Tabs.Root>
