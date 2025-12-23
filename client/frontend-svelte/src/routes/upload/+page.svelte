<script>
  import { auth } from '$lib/stores/auth.js';
  import { goto } from '$app/navigation';
  let file;
  let docName = '';
  let department = 'HR';
  let loading = false;
  let error = '';

  $: user = auth.user;
  $: if (user && (user.role !== 'admin' && user.role !== 'hr')) goto('/chat');  // Role gate

  const handleUpload = async () => {
    if (!file) return;
    loading = true;
    error = '';

    const formData = new FormData();
    formData.append('file', file);
    formData.append('doc_name', docName);
    formData.append('department', department);

    try {
      await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/documents/upload/`, {
        method: 'POST',
        body: formData,
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      goto('/chat');
    } catch (err) {
      error = 'Upload failed';
    }
    loading = false;
  };

  const onFileChange = (e) => {
    file = e.target.files[0];
  };
</script>

<div class="flex min-h-screen items-center justify-center bg-gray-100">
  <form on:submit|preventDefault={handleUpload} class="w-full max-w-md space-y-4 p-6 bg-white rounded shadow">
    <h1 class="text-2xl font-bold text-center">Upload Document</h1>
    {#if error}
      <p class="text-red-500 text-center">{error}</p>
    {/if}
    <input type="file" on:change={onFileChange} class="w-full p-2 border rounded" accept=".pdf" required />
    <input type="text" bind:value={docName} placeholder="Document Name" class="w-full p-2 border rounded" required />
    <select bind:value={department} class="w-full p-2 border rounded">
      <option value="HR">HR</option>
      <option value="FINANCE">Finance</option>
      <option value="IT">IT</option>
      <option value="GENERAL">General</option>
    </select>
    <button type="submit" disabled={loading} class="w-full p-2 bg-green-500 text-white rounded">
      {loading ? 'Uploading...' : 'Upload'}
    </button>
  </form>
</div>