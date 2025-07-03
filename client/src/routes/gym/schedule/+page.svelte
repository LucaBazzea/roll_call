<script>
	import { onMount } from 'svelte';
	import { Badge } from '$lib/components/ui/badge/index.js';
	import * as Tabs from '$lib/components/ui/tabs/index.js';
	import * as Drawer from '$lib/components/ui/drawer';
	import * as Avatar from '$lib/components/ui/avatar';
	import * as Card from '$lib/components/ui/card/index.js';
	import { Button, buttonVariants } from '$lib/components/ui/button/index.js';
	import * as Dialog from '$lib/components/ui/dialog/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Label } from '$lib/components/ui/label/index.js';
	import * as Select from '$lib/components/ui/select';
	import { Textarea } from '$lib/components/ui/textarea/index.js';
	import CircleAlert from 'lucide-svelte/icons/circle-alert';
	import * as Alert from '$lib/components/ui/alert/index.js';
	import DialogFooter from '$lib/components/ui/dialog/dialog-footer.svelte';
	import { Progress } from '$lib/components/ui/progress/index.js';

	const baseURL = 'http://127.0.0.1:8000';

	// TODO: Add to store
	const gymID = '1';

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
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ gym_id: gymID })
			});

			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}

			const jsonData = await response.json();
			return jsonData;
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

	// TODO: Put this in store
	let isAdmin = true;

	// TODO: Get the day today
	let dayToday = 'mon';

	let addClassErrorFlag = false;

	$: addClassDay = dayToday;
	let addClassTitle = null;
	let addClassDescription = null;
	let addClassStartHour = null;
	let addClassStartMinute = null;
	let addClassEndHour = null;
	let addClassEndMinute = null;
	let addClassCapacity = null;
	let addClassCoach = null;

	async function postAddClassData() {
		if (!addClassDay || !addClassTitle || !addClassStartHour || !addClassEndHour) {
			console.error('Null form value');
			addClassErrorFlag = true;
			return;
		}

		let addClassData = {
			day: addClassDay,
			title: addClassTitle,
			description: addClassDescription,
			start_hour: addClassStartHour,
			start_minute: addClassStartMinute,
			end_hour: addClassEndHour,
			end_minute: addClassEndMinute,
			addClassCapacity: addClassCapacity,
			coach: addClassCoach
		};
		console.log(addClassData);

		try {
			const response = await fetch(`${baseURL}/admin/class/create/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(addClassData)
			});

			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}

			const data = await response.json();
			console.log(data);
		} catch (error) {
			addClassErrorFlag = false;
		}

		addClassErrorFlag = false;
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
			schedule = await getSchedule(1); // Replace 1 with the actual gymID value
			console.log('Schedule:', schedule);
		} catch (error) {
			console.error('Failed to fetch schedule:', error);
		}
	});
</script>

<Tabs.Root value={dayToday} class="relative w-full pb-12 pt-10">
	<Tabs.List class="fixed top-0 grid w-full grid-cols-7 rounded-none">
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
					<Drawer.Trigger class="w-full p-2">
						<div class="flex flex-col rounded-md border px-4 py-3">
							<div class="flex flex-row">
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
							{#if event.capacity}
								<div class="mt-4">
									<Progress value={event.bookings_count} max={event.capacity} class="h-1" />
								</div>
							{/if}
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
							{#if isAdmin === true}
								<Dialog.Root>
									<Dialog.Trigger>
										<Button variant="secondary" class="mt-6 w-full">Delete Class</Button>
									</Dialog.Trigger>
									<Dialog.Content>
										<Dialog.Header>
											<Dialog.Title>Delete Class</Dialog.Title>
											<Dialog.Description>Are you sure?</Dialog.Description>
										</Dialog.Header>
										<DialogFooter>
											<Button variant="destructive" on:click={deleteClass}>Delete</Button>
										</DialogFooter>
									</Dialog.Content>
								</Dialog.Root>
							{/if}
						</Drawer.Footer>
					</Drawer.Content>
				</Drawer.Root>
			{/each}
		</Tabs.Content>
	{/each}

	{#if isAdmin}
		<div class="fixed bottom-0 w-full">
			<Dialog.Root>
				<Dialog.Trigger class="w-full">
					<Button variant="secondary" class="w-full rounded-none text-center">Add Class</Button>
				</Dialog.Trigger>
				<Dialog.Content class="sm:max-w-[425px]">
					<Dialog.Header>
						<Dialog.Title>Add Class</Dialog.Title>
						<Dialog.Description>
							Fill in class info here. Click save when you're done.
						</Dialog.Description>
					</Dialog.Header>
					{#if addClassErrorFlag}
						<Alert.Root class="text-left">
							<CircleAlert class="h-4 w-4" />
							<Alert.Title>Alert</Alert.Title>
							<Alert.Description>Please fill in the missing information</Alert.Description>
						</Alert.Root>
					{/if}
					<div class="grid gap-4 py-4">
						<div class="grid grid-cols-4 items-center gap-4">
							<Label for="addClassDay" class="text-right">Day *</Label>
							<Select.Root bind:value={addClassDay}>
								<Select.Trigger class="w-[180px]">
									<Select.Value placeholder={weekdayAbbreviations[addClassDay]} />
								</Select.Trigger>
								<Select.Content>
									<Select.Group>
										<Select.Item value="mon" label="Monday" />
										<Select.Item value="tue" label="Tuesday" />
										<Select.Item value="wed" label="Wednesday" />
										<Select.Item value="thu" label="Thursday" />
										<Select.Item value="fri" label="Friday" />
										<Select.Item value="sat" label="Saturday" />
										<Select.Item value="sun" label="Sunday" />
									</Select.Group>
								</Select.Content>
							</Select.Root>
						</div>
						<div class="grid grid-cols-4 items-center gap-4">
							<Label for="addClassTitle" class="text-right">Title *</Label>
							<Input id="addClassTitle" bind:value={addClassTitle} class="col-span-3" />
						</div>
						<div class="grid grid-cols-4 items-center gap-4">
							<Label for="addClassDescription" class="text-right">Description</Label>
							<Textarea
								id="addClassDescription"
								bind:value={addClassDescription}
								class="col-span-3"
								placeholder="Description (optional)"
							/>
						</div>
						<div class="grid grid-cols-4 items-center gap-4">
							<Label for="addClass" class="text-right">Start *</Label>
							<div class="col-span-3 flex flex-row space-x-1">
								<Input
									id="addClassStartHour"
									bind:value={addClassStartHour}
									placeholder="00"
									type="number"
									class=""
								/>
								<p>:</p>
								<Input
									id="addClassStartMinute"
									bind:value={addClassStartMinute}
									placeholder="00"
									type="number"
									class=""
								/>
							</div>
						</div>
						<div class="grid grid-cols-4 items-center gap-4">
							<Label for="username" class="text-right">End *</Label>
							<div class="col-span-3 flex flex-row space-x-1">
								<Input
									id="addClassEndHour"
									bind:value={addClassEndHour}
									placeholder="00"
									type="number"
									class=""
								/>
								<p>:</p>
								<Input
									id="addClassEndMinute"
									bind:value={addClassEndMinute}
									placeholder="00"
									type="number"
									class=""
								/>
							</div>
						</div>
						<div class="grid grid-cols-4 items-center gap-4">
							<Label for="addClassCapacity" class="text-right">Capacity</Label>
							<Input
								id="addClassCapacity"
								bind:value={addClassCapacity}
								placeholder="What is the max no. of students? (optional)"
								type="number"
								class="col-span-3"
							/>
						</div>
						<div class="grid grid-cols-4 items-center gap-4">
							<Label for="addClassCoach" class="text-right">Coach</Label>
							<Input id="addClassCoach" bind:value={addClassCoach} class="col-span-3" />
						</div>
					</div>
					<Dialog.Footer>
						<Button type="submit" on:click={postAddClassData}>Save changes</Button>
					</Dialog.Footer>
				</Dialog.Content>
			</Dialog.Root>
		</div>
	{/if}
</Tabs.Root>
