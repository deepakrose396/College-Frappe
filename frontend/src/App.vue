<template>
  <div class="h-screen flex flex-col">
    <!-- Top Navbar -->
    <header class="h-14 bg-blue-600 text-white flex items-center px-4 shadow-md">
      <Navbar />
    </header>

    <!-- Main layout -->
    <div class="flex flex-1 overflow-hidden">
      <!-- Sidebar -->
      <aside class="w-64 bg-gray-800 text-white h-full p-4 overflow-y-auto">
        <Sidebar />
      </aside>

      <!-- Content -->
      <main class="flex-1 bg-gray-100 p-6 overflow-y-auto">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import Navbar from './pages/Navbar.vue'
import Sidebar from './pages/Sidebar.vue';
</script>