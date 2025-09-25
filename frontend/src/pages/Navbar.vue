<template>
  <header class="bg-white shadow">
    <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Left: Brand -->
        <div class="flex-shrink-0 text-xl font-bold text-blue-600">
          College Portal
        </div>

        <!-- Right: Conditional Nav -->
        <div>
          <!-- If user is logged in -->
          <div v-if="isLoggedIn" class="flex items-center space-x-4">
            <span class="text-gray-700">Welcome, <b>{{ user.name }}</b></span>
            <button
              @click="logout"
              class="px-4 py-2 rounded-lg bg-red-500 text-white font-medium hover:bg-red-600 transition"
            >
              Logout
            </button>
          </div>

          <!-- If not logged in -->
          <div v-else>
            <router-link
              to="/account/login"
              class="px-4 py-2 rounded-lg bg-blue-600 text-white font-medium hover:bg-blue-700 transition"
            >
              Login
            </router-link>
          </div>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { ref,onMounted } from "vue"
import { useRouter } from "vue-router"
import { session } from "../data/session"
const router = useRouter()

// Simulate user state (replace with actual auth state from Frappe session)
const isLoggedIn = ref(session.isLoggedIn)   // toggle true/false to test
const user = ref({ name: session.user })

function logout() {
  session.logout.submit()
}

</script>
