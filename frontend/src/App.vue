<template>
  <div>
    <Navbar />
    <div class="flex-1">
      <router-view />
    </div>
  </div>
</template>
<script setup>
import Navbar from './pages/Navbar.vue'
</script>