<template>
  <div class="mt-12 flex justify-center">
    <h1 class="text-gray-700">Welcome, <b>{{ user.name }}</b></h1>
  </div>
  <div class="max-w-3xl mx-auto mt-10 p-8 bg-white shadow-lg rounded-xl space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <h2 class="text-2xl font-bold">My Application</h2>
    </div>

    <!-- Status Card -->
    <div class="p-4 rounded-lg flex items-center gap-3" :class="statusCardClass">
      <span class="font-semibold">{{ applicant.status }}</span>
      <span class="text-sm opacity-80">
        {{
          statusDescription[applicant.status] ||
          "Track your application progress"
        }}
      </span>
    </div>

    <!-- Profile Form -->
    <form @submit.prevent="updateProfile" class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div>
        <label class="block font-medium mb-1">First Name</label>
        <input v-model="applicant.first_name" type="text"
          class="w-full border p-2 rounded focus:ring-2 focus:ring-blue-400" />
      </div>

      <div>
        <label class="block font-medium mb-1">Last Name</label>
        <input v-model="applicant.last_name" type="text"
          class="w-full border p-2 rounded focus:ring-2 focus:ring-blue-400" />
      </div>

      <div>
        <label class="block font-medium mb-1">Email</label>
        <input v-model="applicant.email" type="email" disabled class="w-full border p-2 rounded bg-gray-100" readonly/>
      </div>

      <div>
        <label class="block font-medium mb-1">Phone</label>
        <input v-model="applicant.phone" type="text"
          class="w-full border p-2 rounded focus:ring-2 focus:ring-blue-400" />
      </div>

      <div>
        <label class="block font-medium mb-1">Department</label>
        <input v-model="applicant.department" type="text"
          class="w-full border p-2 rounded focus:ring-2 focus:ring-blue-400" readonly/>
      </div>

      <div>
        <label class="block font-medium mb-1">Program</label>
        <input v-model="applicant.program" type="text"
          class="w-full border p-2 rounded focus:ring-2 focus:ring-blue-400" readonly/>
      </div>

      <div>
        <label class="block font-medium mb-1">Academic Year</label>
        <input v-model="applicant.academic_year" type="text"
          class="w-full border p-2 rounded focus:ring-2 focus:ring-blue-400" readonly/>
      </div>

      <div class="flex items-center gap-2">
        <input type="checkbox" v-model="applicant.paid" true-value="1" false-value="0" class="w-5 h-5 rounded-full" />
        <label class="font-medium">Payment Status</label>
        <span class="ml-2 text-sm px-2 py-1 rounded-full"
          :class="applicant.paid == 1 ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'">
          {{ applicant.paid == 1 ? "Paid" : "Unpaid" }}
        </span>
      </div>
    </form>

    <!-- Action Buttons -->
    <div class="flex justify-end">
      <button type="button" @click="updateProfile"
        class="px-6 py-2 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 disabled:opacity-50"
        :disabled="loading">
        {{ loading ? "Updating..." : "Update Profile" }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue"
import { session } from "../data/session"
import { useLoadingStore } from "@/stores/loadingStore"


const loadingStore = useLoadingStore()
const applicant = ref({})
const loading = ref(false)
const user = ref({ name: session.user })

async function fetchProfile() {
  loadingStore.startLoading()
  const res = await fetch("/api/method/collage.api.applicant.get_my_applicant")
  const data = await res.json()
  if (!data.exc) {
    applicant.value = data.message
  }
  loadingStore.stopLoading()
}

async function updateProfile() {
  loading.value = true
  loadingStore.startLoading()
  if (applicant.value.paid == 1) {
    applicant.value.status = "Applied"
  } else if (applicant.value.paid == 0) {
    applicant.value.status = "Payment Pending"
  }

  const res = await fetch("/api/method/collage.api.applicant.update_my_applicant", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ data: applicant.value }),
  })

  const data = await res.json()
  loading.value = false

  if (!data.exc) {
    loadingStore.stopLoading()
    alert("✅ Profile updated successfully")
  } else {
    loadingStore.stopLoading()
    alert("❌ Update failed")
  }
}

const statusThemeMap = {
  Applied: "blue",
  "Payment Pending": "yellow",
  Shortlisted: "cyan",
  Selected: "green",
  "Wait Listed": "gray",
  Rejected: "red",
}

const statusDescription = {
  Applied: "Your application has been submitted.",
  "Payment Pending": "Please complete the payment to proceed.",
  Shortlisted: "You’ve been shortlisted! Await further instructions.",
  Selected: "🎉 Congratulations! You are selected.",
  "Wait Listed": "You’re on the waitlist, stay tuned.",
  Rejected: "Unfortunately, your application was not successful.",
}

const statusTheme = computed(() => statusThemeMap[applicant.value.status] || "gray")

const statusCardClass = computed(() => {
  return {
    "bg-blue-100 text-blue-800": applicant.value.status === "Applied",
    "bg-yellow-100 text-yellow-800": applicant.value.status === "Payment Pending",
    "bg-cyan-100 text-cyan-800": applicant.value.status === "Shortlisted",
    "bg-green-100 text-green-800": applicant.value.status === "Selected",
    "bg-gray-100 text-gray-800": applicant.value.status === "Wait Listed",
    "bg-red-100 text-red-800": applicant.value.status === "Rejected",
  }
})

onMounted(fetchProfile)
</script>
