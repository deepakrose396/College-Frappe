<!-- src/components/GlobalLoader.vue -->
<template>
  <div v-if="loadingStore.isLoading" class="fixed inset-0 flex items-center justify-center bg-black/30 z-50">
    <div class="w-16 h-16 border-4 border-t-transparent border-white rounded-full animate-spin"></div>
  </div>
</template>

<script setup>
import { useLoadingStore } from "@/stores/loadingStore"
const loadingStore = useLoadingStore()
</script>
