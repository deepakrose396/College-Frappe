<template>
  <header class=" bg-green-900 p-2 shadow-md border-b border-gray-600">
    <nav class="max-w-7xl mx-auto  px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Left: Brand -->
        <div class="flex-shrink-0 text-2xl font-bold text-white">
          College Portal
        </div>

        <!-- Right: Conditional Nav -->
        <div>
          <!-- If user is logged in -->
          <div v-if="isLoggedIn" class="flex items-center space-x-4">
            <!-- <router-link to="/my-profile"
              class="px-4 py-2 rounded-lg bg-blue-600 text-white font-medium hover:bg-blue-700 transition">
              Track Application
            </router-link> -->
            <button @click="logout"
              class="px-4 py-2 rounded-lg bg-red-500 text-white font-medium hover:bg-red-600 transition">
              Logout
            </button>

          </div>

          <!-- If not logged in -->
          <div v-else class="space-x-4">
            <router-link to="/application"
              class="px-4 py-2 rounded-lg bg-green-500/50 text-white font-medium hover:bg-green-800 hover:border-dark-amber-50 solid hover:border transition">
              Application
            </router-link>
            <router-link to="/account/login"
              class="px-4 py-2 rounded-lg bg-green-500/50 text-white font-medium hover:bg-green-800 hover:border-dark-amber-50 solid hover:border transition">
              Login
            </router-link>
          </div>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { ref, watch } from "vue"
import { useRouter } from "vue-router"
import { session } from "../data/session"
const router = useRouter()

// Simulate user state (replace with actual auth state from Frappe session)
const isLoggedIn = ref(session.isLoggedIn)   // toggle true/false to test

function logout() {
  session.logout.submit()
}

watch(() => session.isLoggedIn, (newVal) => {
  isLoggedIn.value = newVal
})

</script>
