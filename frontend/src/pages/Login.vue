<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-600 via-purple-600 to-pink-500 px-4">
    <div
      class="w-full max-w-lg bg-white/10 backdrop-blur-xl border border-white/20 rounded-2xl shadow-2xl p-8 space-y-6 animate-fadeIn relative z-10">

      <h2 class="text-2xl font-bold text-white text-center mb-6 tracking-wide animate-slideDown">
        Welcome Back
      </h2>
      <!-- <p class="text-sm text-gray-200 text-center mb-6 animate-fadeInDelay">
        Login to your <span class="font-semibold">FrappeUI App</span>
      </p> -->

      <form class="flex flex-col space-y-4" @submit.prevent="submit">
        <div class="animate-slideUp">
          <label for="email" class="block mb-1 text-gray-200 text-sm font-medium">User ID</label>
          <input v-model="email" required id="email" name="email" type="text" placeholder="johndoe@email.com"
            class="w-full px-4 py-3 rounded-xl bg-white/20 text-white placeholder-gray-300 focus:ring-2 focus:ring-pink-400 focus:outline-none transition-all" />
        </div>

        <div class="animate-slideUp delay-200">
          <label for="password" class="block mb-1 text-gray-200 text-sm font-medium">Password</label>
          <input v-model="password" required id="password" name="password" type="text" placeholder="••••••••"
            class="w-full px-4 py-3 rounded-xl bg-white/20 text-white placeholder-gray-300 focus:ring-2 focus:ring-pink-400 focus:outline-none transition-all" />
        </div>

        <button type="submit"
          class="mt-4 w-full py-3 rounded-xl bg-gradient-to-r from-blue-500 to-blue-500 text-white font-semibold hover:scale-105 transform transition-all duration-300 focus:ring-2 focus:ring-offset-2 focus:ring-pink-400 animate-bounceIn"
          :disabled="loading">
          <span v-if="!loading">Login</span>
          <span v-else class="animate-pulse">Loading...</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { session } from "../data/session"


const router = useRouter()
const email = ref("")
const password = ref("")
const loading = ref(false)

async function waitForSession(maxRetries = 5, delay = 100) {
  for (let i = 0; i < maxRetries; i++) {
    const res = await fetch("/api/method/frappe.auth.get_logged_user", { credentials: "include" })
    const data = await res.json()
    if (data.message && data.message !== "Guest") return data.message
    await new Promise(r => setTimeout(r, delay))
  }
  return null
}

async function submit() {
  if (!email.value || !password.value) {
    alert("Please enter email and password")
    return
  }

  loading.value = true

  try {
    const res = await fetch("/api/method/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ usr: email.value.trim(), pwd: password.value.trim() })
    })
    const data = await res.json()

    if (res.ok && !data.exc) {
      console.log("✅ Login success")

      const currentUserEmail = await waitForSession()
      if (!currentUserEmail) {
        alert("Session not ready. Please try again.")
        return
      }

      // ✅ Fetch user roles
      const userRes = await fetch("/api/method/collage.api.user.get_current_user", {
        credentials: "include"
      })
      const userData = await userRes.json()
      const roles = userData.message?.roles || []
      console.log("Roles:", roles)

      // ✅ Update session
      session.isLoggedIn = true
      session.user = currentUserEmail

      // ✅ Redirect based on role
      if (roles.includes("Applicant") || roles.includes("Student")) {
        await router.push({ name: "ApplicantProfile" })
      } else if (roles.includes("Administrator")) {
        await router.push({ name: "ApplicantList" })
      } else {
        await router.push({ name: "ApplicationForm" })
      }

      // ✅ Force re-render (this solves your issue)
      router.go(0)

    } else {
      alert("Login failed: " + (data.message || "Invalid credentials"))
    }
  } catch (err) {
    console.error(err)
    alert("Login error: " + err)
    console.log("login error",err);
    
  } finally {
    loading.value = false
  }
}
</script>


<style scoped>
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
@keyframes slideDown { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }
@keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
@keyframes bounceIn { 0% { transform: scale(0.9); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }

.animate-fadeIn { animation: fadeIn 0.6s ease forwards; }
.animate-slideDown { animation: slideDown 0.7s ease forwards; }
.animate-slideUp { animation: slideUp 0.7s ease forwards; }
.animate-slideUp.delay-200 { animation-delay: 0.2s; }
.animate-fadeInDelay { animation: fadeIn 1s ease forwards; animation-delay: 0.4s; }
.animate-bounceIn { animation: bounceIn 0.8s ease forwards; }
</style>
