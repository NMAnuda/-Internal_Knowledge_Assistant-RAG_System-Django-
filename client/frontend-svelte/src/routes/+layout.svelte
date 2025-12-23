<script lang="ts">
	import favicon from '$lib/assets/favicon.svg';
	import "$lib/app.css"; // correct if app.css is in src/routes/
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<slot /> <!-- This renders the child pages -->
