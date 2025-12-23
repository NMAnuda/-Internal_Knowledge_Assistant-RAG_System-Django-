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
      console.log('🔄 Loading history...');  //  DEBUG
      const token = localStorage.getItem('token');
      const res = await fetch(
        `${import.meta.env.VITE_BACKEND_URL}/api/chat/history/?limit=20&page=1`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      console.log('📥 History response status:', res.status);  //  DEBUG
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      console.log('📦 History data:', data.history?.length || 0);  //  DEBUG
      messages = data.history || [];
      console.log("message",messages)
      error = '';  // Clear error
    } catch (err) {
      console.error('❌ History load error:', err);  //  DEBUG
      error = 'Failed to load chat history. Try asking a question.';
      messages = [];  // Ensure empty
    }
  }

  async function askQuestion() {
    if (!question.trim()) return;

    loading = true;
    error = '';
    const q = question;
    question = '';

    try {
      console.log('🚀 Asking:', q);  // 🔥 DEBUG
      const token = localStorage.getItem('token');
      const res = await fetch(
        `${import.meta.env.VITE_BACKEND_URL}/api/chat/ask/`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`
          },
          body: JSON.stringify({ question: q, department })
        }
      );
      console.log('📥 Ask response status:', res.status);  // 🔥 DEBUG
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      console.log('📦 Ask data:', data);  // 🔥 DEBUG
      messages = [data, ...messages];  // Append to top
      loadHistory();  // Re-load full history (ensures sync)
    } catch (err) {
      console.error('❌ Ask error:', err);  // 🔥 DEBUG
      error = 'Failed to get answer. Check connection.';
      question = q;  // Restore input
    } finally {
      loading = false;
    }
  }

  function handleLogout() {
    auth.logout();
  }
</script>

<svelte:head>
  <title>Knowledge Bot | Chat</title>
</svelte:head>

<div class="flex h-screen bg-gray-100">

  <!-- SIDEBAR -->
  <aside class="w-80 bg-white border-r flex flex-col">
    <div class="p-5 border-b">
      <h2 class="text-xl font-bold text-gray-800">Knowledge Bot</h2>
      {#if user}
        <p class="text-sm text-gray-600 mt-2">
          {user.username}
          <span class="ml-2 text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
            {user.role}
          </span>
        </p>
      {/if}
    </div>

    <div class="flex-1 overflow-y-auto p-4">
      <p class="text-xs text-gray-500 mb-3">Recent Questions</p>

      {#if messages.length === 0}
        <p class="text-sm text-gray-400 text-center mt-10">
          No history yet. Ask a question to start!
        </p>
      {:else}
        <ul class="space-y-2">
          {#each messages as msg}
            <li class="p-3 rounded-lg bg-gray-50 hover:bg-gray-100 cursor-pointer">
              <p class="text-sm font-medium text-gray-800 line-clamp-2">
                {msg.question}
              </p>
              <p class="text-xs text-gray-500 mt-1">
                {new Date(msg.timestamp).toLocaleString()}
              </p>
            </li>
          {/each}
        </ul>
      {/if}
    </div>

    <div class="p-4 border-t">
      <button
        on:click={handleLogout}
        class="w-full bg-red-500 hover:bg-red-600 text-white py-2 rounded-lg font-semibold"
      >
        Logout
      </button>
    </div>
  </aside>

  <!-- MAIN CHAT -->
  <main class="flex-1 flex flex-col">

    <!-- HEADER -->
    <header class="bg-blue-600 text-white px-6 py-4 flex justify-between items-center">
      <h1 class="text-xl font-semibold">Internal Knowledge Assistant</h1>

      <div class="flex items-center gap-4">
        <select
          bind:value={department}
          class="bg-white text-gray-800 px-3 py-1.5 rounded-lg text-sm focus:ring-2 focus:ring-blue-300"
        >
          <option value="HR">HR</option>
          <option value="FINANCE">Finance</option>
          <option value="IT">IT</option>
          <option value="GENERAL">General</option>
        </select>
        {#if user?.role === 'admin' || user?.role === 'hr'}
          <button 
            on:click={() => goto('/upload')} 
            class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
          >
            📁 Upload Document
          </button>
        {/if}
      </div>
    </header>

    <!-- CHAT AREA -->
    <section class="flex-1 overflow-y-auto p-6 space-y-5">
      {#if error}
        <div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      {/if}

      {#if messages.length === 0 && !loading}
        <div class="text-center text-gray-400 mt-20">
          Ask a question to get started
        </div>
      {/if}

      {#each messages as msg}
  <div class="bg-white rounded-xl shadow p-5">
    <div class="mb-3">
      <p class="text-xs text-gray-500">Question</p>
      <p class="font-semibold text-gray-800">{msg.question}</p>
    </div>

    <div class="mb-3">
      <p class="text-xs text-gray-500">Answer</p>
      <p class="text-gray-700 leading-relaxed">{msg.answer}</p>
    </div>

    <div class="flex items-center gap-4 text-xs text-gray-500">
      <span class="text-blue-600 font-medium">
        Confidence: {msg.confidence || 'medium'} 
      </span>
      <span>
        {new Date(msg.timestamp).toLocaleString()}  
      </span>
    </div>

    {#if msg.sources?.length}
      <div class="mt-4 pt-3 border-t">
        <p class="text-xs text-gray-500 mb-2">Sources</p>
        <ul class="space-y-1">
          {#each msg.sources as src, i}
            <li class="text-xs text-gray-600">
              {i + 1}. {src.doc_name} ({src.score.toFixed(2)})
            </li>
          {/each}
        </ul>
      </div>
    {/if}
  </div>
{/each}
    </section>

    <!-- INPUT -->
    <footer class="bg-white border-t p-4">
      <form on:submit|preventDefault={askQuestion} class="flex gap-3">
        <input
          type="text"
          bind:value={question}
          placeholder="Ask about company policies, procedures, benefits..."
          disabled={loading}
          class="flex-1 px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          disabled={loading || !question.trim()}
          class="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400
                 text-white px-6 py-3 rounded-lg font-semibold"
        >
          {loading ? 'Thinking...' : 'Send'}
        </button>
      </form>
    </footer>

  </main>
</div>

<style>
  .line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
</style>