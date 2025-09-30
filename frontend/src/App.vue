<template>
  <div class="h-screen flex flex-col">
    <!-- Top Navbar -->
      <Navbar />
    <!-- Main layout -->
    <div class="flex flex-1 overflow-hidden">
      <!-- Sidebar -->
        <Sidebar />

      <!-- Content -->
      <main class="flex-1  overflow-y-auto">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import Navbar from './pages/Navbar.vue'
import Sidebar from './pages/Sidebar.vue';
</script>