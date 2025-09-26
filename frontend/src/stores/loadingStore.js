// src/stores/loadingStore.js
import { defineStore } from "pinia"
import { ref,computed } from "vue"

export const useLoadingStore = defineStore("loading", () => {
  const loadingCount = ref(0)

  const startLoading = () => loadingCount.value++
  const stopLoading = () => {
    if (loadingCount.value > 0) loadingCount.value--
  }

  const isLoading = computed(() => loadingCount.value > 0)

  return { startLoading, stopLoading, isLoading }
})
