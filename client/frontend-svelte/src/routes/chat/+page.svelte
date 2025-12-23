<!-- src/routes/chat/+page.svelte -->
<script lang="ts">
  import { auth } from '$lib/auth';
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  interface Message {
    id: number;
    question: string;
    answer: string;
    confidence: string;
    timestamp: string;
    sources?: Array<{ doc_name: string; score: number }>;
  }

  let messages: Message[] = [];
  let question = '';
  let department = 'HR';
  let loading = false;
  let error = '';
  let user: any = null;

  // Subscribe to auth store
  auth.subscribe(state => {
    user = state.user;
    if (!user && typeof window !== 'undefined') {
      goto('/login');
    }
  });

  onMount(() => {
    if (!localStorage.getItem('token')) {
      goto('/login');
      return;
    }
    loadHistory();
  });

  async function loadHistory() {
    try {
      const token = localStorage.getItem('token');
      const res = await fetch(
        `${import.meta.env.VITE_BACKEND_URL}/api/chat/history/?limit=20&page=1`,
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );
      
      if (!res.ok) throw new Error('Failed to load history');
      
      const data = await res.json();
      messages = data.history || [];
    } catch (err) {
      console.error('History error:', err);
      error = 'Failed to load chat history';
    }
  }

  async function askQuestion() {
    if (!question.trim()) return;
    
    loading = true;
    error = '';
    const userQuestion = question;
    question = '';

    try {
      const token = localStorage.getItem('token');
      const res = await fetch(
        `${import.meta.env.VITE_BACKEND_URL}/api/chat/ask/`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`
          },
          body: JSON.stringify({ question: userQuestion, department })
        }
      );

      if (!res.ok) throw new Error('Failed to get answer');

      const data = await res.json();
      messages = [data, ...messages];
    } catch (err) {
      console.error('Ask error:', err);
      error = 'Failed to get answer. Please try again.';
      question = userQuestion; // Restore question on error
    } finally {
      loading = false;
    }
  }

  function handleLogout() {
    auth.logout();
  }
</script>

<svelte:head>
  <title>Chat - Knowledge Bot</title>
</svelte:head>

<div class="flex h-screen bg-gray-100">
  <!-- Sidebar -->
  <div class="w-80 bg-white border-r border-gray-200 flex flex-col">
    <div class="p-4 border-b border-gray-200">
      <h2 class="text-xl font-bold text-gray-800">Chat History</h2>
      {#if user}
        <p class="text-sm text-gray-600 mt-1">
          Logged in as <span class="font-semibold">{user.username}</span>
          <span class="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded ml-2">
            {user.role}
          </span>
        </p>
      {/if}
    </div>

    <div class="flex-1 overflow-y-auto p-4">
      {#if messages.length === 0}
        <p class="text-gray-500 text-sm text-center mt-8">No chat history yet</p>
      {:else}
        <ul class="space-y-2">
          {#each messages as msg}
            <li class="p-3 bg-gray-50 hover:bg-gray-100 rounded-lg transition">
              <p class="font-semibold text-sm text-gray-800 line-clamp-2">
                {msg.question}
              </p>
              <p class="text-xs text-gray-500 mt-1">
                {new Date(msg.timestamp).toLocaleString()}
              </p>
              <p class="text-xs text-blue-600 mt-1">
                Confidence: {msg.confidence}
              </p>
            </li>
          {/each}
        </ul>
      {/if}
    </div>

    <div class="p-4 border-t border-gray-200">
      <button
        on:click={handleLogout}
        class="w-full bg-red-500 hover:bg-red-600 text-white font-semibold py-2 px-4 rounded-lg transition"
      >
        Logout
      </button>
    </div>
  </div>

  <!-- Main Chat Area -->
  <div class="flex-1 flex flex-col">
    <!-- Header -->
    <div class="bg-blue-600 text-white p-4 flex items-center justify-between">
      <h1 class="text-2xl font-bold">Knowledge Chatbot</h1>
      <div class="flex items-center gap-3">
        <label for="department" class="text-sm font-medium">Department:</label>
        <select
          id="department"
          bind:value={department}
          class="px-3 py-1 rounded bg-white text-gray-800 border-none focus:ring-2 focus:ring-blue-300"
        >
          <option value="HR">HR</option>
          <option value="FINANCE">Finance</option>
          <option value="IT">IT</option>
        </select>
      </div>
    </div>

    <!-- Messages -->
    <div class="flex-1 overflow-y-auto p-6 space-y-4">
      {#if messages.length === 0}
        <div class="text-center text-gray-500 mt-20">
          <p class="text-lg">Ask a question to get started!</p>
        </div>
      {/if}

      {#each messages as msg}
        <div class="bg-white rounded-lg shadow p-4">
          <div class="mb-3">
            <p class="text-sm text-gray-500 mb-1">Question:</p>
            <p class="font-semibold text-gray-800">{msg.question}</p>
          </div>
          
          <div class="mb-3">
            <p class="text-sm text-gray-500 mb-1">Answer:</p>
            <p class="text-gray-700">{msg.answer}</p>
          </div>

          <div class="flex items-center gap-4 text-sm">
            <span class="text-blue-600 font-medium">
              Confidence: {msg.confidence}
            </span>
            <span class="text-gray-400">
              {new Date(msg.timestamp).toLocaleString()}
            </span>
          </div>

          {#if msg.sources && msg.sources.length > 0}
            <div class="mt-3 pt-3 border-t border-gray-200">
              <p class="text-xs text-gray-500 mb-2">Sources:</p>
              <ul class="space-y-1">
                {#each msg.sources as src, i}
                  <li class="text-xs text-gray-600">
                    {i + 1}. {src.doc_name} (Score: {src.score.toFixed(2)})
                  </li>
                {/each}
              </ul>
            </div>
          {/if}
        </div>
      {/each}
    </div>

    <!-- Input Area -->
    <div class="bg-white border-t border-gray-200 p-4">
      {#if error}
        <div class="mb-3 bg-red-50 border border-red-200 text-red-700 px-4 py-2 rounded">
          {error}
        </div>
      {/if}

      <form on:submit|preventDefault={askQuestion} class="flex gap-2">
        <input
          type="text"
          bind:value={question}
          placeholder="Ask about company policy, procedures, benefits..."
          class="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          disabled={loading}
        />
        <button
          type="submit"
          disabled={loading || !question.trim()}
          class="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-semibold px-6 py-3 rounded-lg transition"
        >
          {loading ? 'Thinking...' : 'Send'}
        </button>
      </form>
    </div>
  </div>
</div>

<style>
  .line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
</style>