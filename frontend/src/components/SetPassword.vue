<template>
  <section class="reset-password">
    <div class="card">
      <h2>Reset Password</h2>

      <form @submit.prevent="handleSubmit">
        <!-- Old password (only if no key is present) -->
        <div v-if="!key">
          <input
            v-model="oldPassword"
            type="password"
            placeholder="Old Password"
            autocomplete="current-password"
          />
        </div>

        <!-- New password -->
        <div>
          <input
            v-model="newPassword"
            type="password"
            placeholder="New Password"
            autocomplete="new-password"
          />
        </div>

        <!-- Confirm password -->
        <div>
          <input
            v-model="confirmPassword"
            type="password"
            placeholder="Confirm Password"
            autocomplete="new-password"
          />
        </div>

        <!-- Messages -->
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
        <p v-if="successMessage" class="success">{{ successMessage }}</p>

        <button type="submit" :disabled="loading">
          {{ loading ? "Updating..." : "Confirm" }}
        </button>
      </form>
    </div>
  </section>
</template>

<script setup>
import { ref, watch } from "vue"
import { useRoute } from "vue-router"

// state
const route = useRoute()
const key = ref(route.query.key || "")
const user = ref(route.query.user || "")
const oldPassword = ref("")
const newPassword = ref("")
const confirmPassword = ref("")
const loading = ref(false)
const errorMessage = ref("")
const successMessage = ref("")

// Watch if URL query changes
watch(
  () => route.query,
  (q) => {
    key.value = q.key || ""
    user.value = q.user || ""
  },
  { immediate: true }
)

// Submit handler
const handleSubmit = async () => {
  errorMessage.value = ""
  successMessage.value = ""

  if (!newPassword.value) {
    errorMessage.value = "Please enter a new password."
    return
  }
  if (newPassword.value !== confirmPassword.value) {
    errorMessage.value = "Passwords do not match."
    return
  }

  loading.value = true
  try {
    const res = await fetch("/api/method/frappe.core.doctype.user.user.update_password", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        key: key.value || "",
        old_password: oldPassword.value,
        new_password: newPassword.value,
        confirm_password: confirmPassword.value,
        logout_all_sessions: 1,
      }),
    })

    if (res.status === 200) {
      const data = await res.json()
      successMessage.value = "Password updated successfully!"
      console.log("Response:", data)
      setTimeout(() => {
        router.push("/my-profile");
      }, 2000)
    } else {
      const err = await res.json()
      errorMessage.value = err.message || "Something went wrong."
    }
  } catch (err) {
    errorMessage.value = err.message || "Network error."
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.reset-password {
  display: flex;
  justify-content: center;
  margin-top: 5rem;
}
.card {
  width: 400px;
  padding: 2rem;
  border: 1px solid #ddd;
  border-radius: 10px;
}
input {
  width: 100%;
  padding: 0.5rem;
  margin-bottom: 1rem;
}
button {
  width: 100%;
  padding: 0.75rem;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 5px;
}
.error {
  color: red;
  font-size: 0.9rem;
}
.success {
  color: green;
  font-size: 0.9rem;
}
</style>
