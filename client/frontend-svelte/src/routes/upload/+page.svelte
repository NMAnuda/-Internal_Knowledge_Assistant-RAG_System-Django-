<script lang="ts">
  import { auth } from '$lib/auth';
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  
  let file: File | null = null;
  let docName = '';
  let department = 'HR';
  let loading = false;
  let error = '';
  let user: any = null;

  // Subscribe to store for reactive user
  onMount(() => {
    return auth.subscribe((state) => {
      user = state.user;
    });
  });

  // Role gate: Redirect if not authorized
  $: if (user && (user.role !== 'admin' && user.role !== 'hr')) {
    error = `Upload not available for ${user.role} role. Redirecting...`;
    setTimeout(() => goto('/chat'), 2000);
  }

  // Role-based dept options (matches backend structure)
  $: allowedDepts = user?.role === 'admin' ? ['HR', 'FINANCE', 'IT', 'GENERAL'] : 
                    user?.role === 'hr' ? ['HR', 'GENERAL'] : ['GENERAL'];

  const handleUpload = async () => {
    if (!file) {
      error = 'Please select a file';
      return;
    }
    if (!docName) {
      error = 'Please enter document name';
      return;
    }
    if (!allowedDepts.includes(department)) {
      error = 'Invalid department for your role';
      return;
    }
    loading = true;
    error = '';

    const formData = new FormData();
    formData.append('file', file);
    formData.append('doc_name', docName);
    formData.append('department', department);

    try {
      const token = localStorage.getItem('token');
      const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/documents/upload/`, {
        method: 'POST',
        body: formData,
        headers: { Authorization: `Bearer ${token}` }
      });
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.error || 'Upload failed');
      }
      alert('Upload successful!');
      goto('/chat');
    } catch {
      error = 'Failed upload file';
    }
    loading = false;
  };

  const onFileChange = (e: Event) => {
    const target = e.target as HTMLInputElement;
    file = target.files?.[0] || null;
  };
</script>

<div class="flex min-h-screen items-center justify-center bg-gray-100">
  <form on:submit|preventDefault={handleUpload} class="w-full max-w-md space-y-4 p-6 bg-white rounded shadow">
    <h1 class="text-2xl font-bold text-center">Upload Document ({user?.role || 'Loading...'} role)</h1>
    {#if error}
      <p class="text-red-500 text-center">{error}</p>
    {/if}
    <input type="file" on:change={onFileChange} class="w-full p-2 border rounded" accept=".pdf,.docx" required />
    <input type="text" bind:value={docName} placeholder="Document Name" class="w-full p-2 border rounded" required />
    <select bind:value={department} class="w-full p-2 border rounded">
      {#each allowedDepts as dept}
        <option value={dept}>{dept}</option>
      {/each}
    </select>
    <button type="submit" disabled={loading || !file || !docName} class="w-full p-2 bg-green-500 text-white rounded">
      {loading ? 'Uploading...' : 'Upload'}
    </button>
  </form>
</div>