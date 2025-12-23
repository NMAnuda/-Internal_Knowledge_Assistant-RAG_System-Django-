<!-- 
  FILE: src/routes/login/+page.svelte
  
  Instructions:
  1. Create folder: frontend-svelte/src/routes/login/
  2. Create file: +page.svelte (inside login folder)
  3. Copy-paste this entire code
-->

<script lang="ts">
  import { auth } from '$lib/auth';
  import { onMount } from 'svelte';
  
  let username = '';
  let password = '';
  let error = '';
  let loading = false;

  onMount(() => {
    // Check if already logged in
    const token = localStorage.getItem('token');
    if (token) {
      window.location.href = '/chat';
    }
  });

  async function handleSubmit() {
    if (!username || !password) {
      error = 'Please fill in all fields';
      return;
    }
    
    loading = true;
    error = '';
    
    const result = await auth.login(username, password);
    
    if (!result.success) {
      error = result.error || 'Login failed. Please check your credentials.';
    }
    
    loading = false;
  }
</script>

<svelte:head>
  <title>Login - Knowledge Bot</title>
</svelte:head>

<div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
  <div class="w-full max-w-md">
    <form 
      on:submit|preventDefault={handleSubmit} 
      class="bg-white shadow-xl rounded-lg p-8 space-y-6"
    >
      <div class="text-center">
        <h1 class="text-3xl font-bold text-gray-800">Knowledge Bot</h1>
        <p class="text-gray-600 mt-2">Sign in to your account</p>
      </div>

      {#if error}
        <div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      {/if}

      <div>
        <label for="username" class="block text-sm font-medium text-gray-700 mb-2">
          Username
        </label>
        <input
          id="username"
          type="text"
          bind:value={username}
          placeholder="Enter your username"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          required
          disabled={loading}
        />
      </div>

      <div>
        <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
          Password
        </label>
        <input
          id="password"
          type="password"
          bind:value={password}
          placeholder="Enter your password"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          required
          disabled={loading}
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        class="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-semibold py-3 px-4 rounded-lg transition duration-200"
      >
        {loading ? 'Signing in...' : 'Sign In'}
      </button>
    </form>

    <p class="text-center text-gray-600 text-sm mt-4">
      Test credentials: test_hr / pass123
    </p>
  </div>
</div>

<style>
  :global(body) {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  }
</style>