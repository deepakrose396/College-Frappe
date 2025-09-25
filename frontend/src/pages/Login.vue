<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-500 px-4">
    <!-- Animated card -->
    <div
      class="relative w-full max-w-md bg-pink-500 backdrop-blur-xl rounded-2xl shadow-2xl p-8 border border-white/20 animate-fadeIn">
      <!-- Floating glow background -->
      <div class="absolute -top-10 -left-10 w-40 h-40 bg-pink-500/30 rounded-full blur-3xl animate-pulse"></div>
      <div class="absolute -bottom-10 -right-10 w-40 h-40 bg-indigo-500/30 rounded-full blur-3xl animate-pulse"></div>

      <!-- Title -->
      <h2 class="text-2xl font-bold text-white text-center mb-6 tracking-wide animate-slideDown">
        Welcome Back 👋
      </h2>
      <p class="text-sm text-gray-200 text-center mb-6 animate-fadeInDelay">
        Login to your <span class="font-semibold">FrappeUI App</span>
      </p>

      <!-- Login Form -->
      <form class="flex flex-col space-y-4" @submit.prevent="submit">
        <!-- Email -->
        <div class="animate-slideUp">
          <label for="email" class="block mb-1 text-gray-200 text-sm font-medium">User ID</label>
          <input required id="email" name="email" type="text" placeholder="johndoe@email.com"
            class="w-full px-4 py-3 rounded-xl bg-white/20 text-white placeholder-gray-300 focus:ring-2 focus:ring-pink-400 focus:outline-none transition-all" />
        </div>

        <!-- Password -->
        <div class="animate-slideUp delay-200">
          <label for="password" class="block mb-1 text-gray-200 text-sm font-medium">Password</label>
          <input required id="password" name="password" type="text" placeholder="••••••••"
            class="w-full px-4 py-3 rounded-xl bg-white/20 text-white placeholder-gray-300 focus:ring-2 focus:ring-pink-400 focus:outline-none transition-all" />
        </div>

        <!-- Button -->
        <button type="submit"
          class="mt-4 w-full py-3 rounded-xl bg-gradient-to-r from-blue-500 to-blue -500 text-white font-semibold hover:scale-105 transform transition-all duration-300 focus:ring-2 focus:ring-offset-2 focus:ring-pink-400 animate-bounceIn"
          :disabled="session.login.loading">
          <span v-if="!session.login.loading">🚀 Login</span>
          <span v-else class="animate-pulse">Loading...</span>
        </button>
      </form>

      <!-- Footer -->
      <p class="text-sm text-gray-300 text-center mt-6 animate-fadeInDelay cursor-pointer hover:text-white transition">
        Don’t have an account?
        <span class="underline text-pink-300 hover:text-pink-400">Register</span>
      </p>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { session } from "../data/session"

function submit(e: Event) {
  const formData = new FormData(e.target as HTMLFormElement)
  session.login.submit({
    email: formData.get("email"),
    password: formData.get("password"),
  })
}
</script>

<style scoped>
/* Custom keyframes for subtle animations */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes bounceIn {
  0% {
    transform: scale(0.9);
    opacity: 0;
  }

  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.animate-fadeIn {
  animation: fadeIn 0.6s ease forwards;
}

.animate-slideDown {
  animation: slideDown 0.7s ease forwards;
}

.animate-slideUp {
  animation: slideUp 0.7s ease forwards;
}

.animate-slideUp.delay-200 {
  animation-delay: 0.2s;
}

.animate-fadeInDelay {
  animation: fadeIn 1s ease forwards;
  animation-delay: 0.4s;
}

.animate-bounceIn {
  animation: bounceIn 0.8s ease forwards;
}
</style>
