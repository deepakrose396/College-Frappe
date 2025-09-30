<template>
    <div class="min-h-screen bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 py-10 px-6">
        <!-- Header -->
        <h1 class="text-center text-3xl font-bold text-gray-700 mb-10">
            Applicant List
        </h1>

        <!-- Table Container -->
        <div class="flex justify-center overflow-x-auto">
            <table class="bg-white shadow-md rounded-2xl overflow-hidden">
                <thead class="bg-gradient-to-r from-blue-500 to-purple-500">
                    <tr>
                        <th class="py-3 px-4 text-left font-semibold">S.No</th>
                        <th class="py-3 px-4 text-left font-semibold">First Name</th>
                        <th class="py-3 px-4 text-left font-semibold">Last Name</th>
                        <th class="py-3 px-4 text-left font-semibold">Email</th>
                        <th class="py-3 px-4 text-left font-semibold">Department</th>
                        <th class="py-3 px-4 text-left font-semibold">Status</th>
                        <th class="py-3 px-4 text-center font-semibold">Actions</th>
                    </tr>
                </thead>

                <tbody>
                    <tr v-for="(applicant, index) in applicants" :key="applicant.id"
                        class="border-b hover:bg-gray-100 transition duration-150">
                        <td class="py-3 px-4">{{ index + 1 }}</td>
                        <td class="py-3 px-4">{{ applicant.first_name }}</td>
                        <td class="py-3 px-4">{{ applicant.last_name }}</td>
                        <td class="py-3 px-4">{{ applicant.email }}</td>
                        <td class="py-3 px-4">{{ applicant.department }}</td>
                        <td class="py-3 px-4">
                            <span class="px-3 py-1 rounded-full text-sm font-medium" :class="{
                                'bg-green-100 text-blue-700': applicant.status === 'Applied',
                                'bg-yellow-100 text-yellow-700': applicant.status === 'Payment Pending',
                                'bg-cyan-100 text-cyan-700': applicant.status === 'Shortlisted',
                                'bg-green-100 text-green-700': applicant.status === 'Selected',
                                'bg-gray-100 text-gray-700': applicant.status === 'Wait Listed',
                                'bg-red-100 text-red-700': applicant.status === 'Rejected'
                            }">
                                {{ applicant.status }}
                            </span>
                        </td>

                        <td class="py-3 px-4 text-center">
                            <button
                                class="inline-flex items-center gap-1 px-4 py-2 bg-blue-500 text-white text-sm rounded-lg shadow hover:bg-blue-600 transition"
                                @click="editApplicant(applicant)">
                                <svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                    stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M11 4H6a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2v-5M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" />
                                </svg>
                                Edit
                            </button>
                        </td>
                    </tr>

                    <tr v-if="!applicants.length">
                        <td colspan="6" class="py-6 text-center text-gray-500">
                            No applicants found.
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <!-- Modal for Edit -->
    <div v-if="edit" class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
        <div class="bg-white rounded-2xl shadow-lg p-8 w-full max-w-md relative">
            <button class="absolute top-3 right-3 text-gray-500 hover:text-red-600" @click="edit = false">
                ✕
            </button>
            <h2 class="text-xl font-semibold mb-6 text-gray-700">
                Edit Applicant Status
            </h2>

            <p class="mb-4 text-gray-600">
                <strong>Email:</strong> {{ selectedApplicant.email }}
            </p>

            <label class="block mb-2 text-sm font-medium text-gray-700">Application Status</label>
            <select v-model="selectedApplicant.status"
                class="w-full border border-gray-300 rounded-lg p-2 mb-6 focus:outline-none focus:ring-2 focus:ring-indigo-400">
                <option disabled value="">Select Status</option>
                <option>Shortlisted</option>
                <option>Selected</option>
                <option>Wait Listed</option>
                <option>Rejected</option>
            </select>

            <div class="flex justify-end space-x-3">
                <button class="px-4 py-2 rounded-lg bg-gray-200 text-gray-700 hover:bg-gray-300" @click="edit = false">
                    Cancel
                </button>
                <button class="px-4 py-2 rounded-lg bg-green-500 text-white hover:bg-green-600" @click="saveStatus">
                    Save
                </button>
            </div>
        </div>
    </div>

    <Dialog :options="{
        title: 'Modal Dialog',
        message: dialogMessage,
        actions: [
            {
                label: 'Close',
                variant: 'solid',
            },
        ],
    }" :disable-outside-click-to-close="true" v-model="dialog5" />

</template>

<script setup>
import { ref, onMounted } from "vue"
import { useLoadingStore } from "@/stores/loadingStore"
import { Dialog } from "frappe-ui"

const loadingStore = useLoadingStore()
const applicants = ref([])
const edit = ref(false)
const selectedApplicant = ref({})
const dialog5 = ref(false);
const dialogMessage = ref('')


async function fetchApplicants() {
    loadingStore.startLoading()
    try {
        const res = await fetch("/api/method/collage.api.applicant.get_applicants", {
            credentials: "include"
        })
        const data = await res.json()
        applicants.value = data.message || []
        loadingStore.stopLoading()
    } catch (e) {
        loadingStore.stopLoading()
        console.error("Error loading applicants:", e)
    }
}

onMounted(() => {
    fetchApplicants()
})

function editApplicant(applicant) {
    selectedApplicant.value = { ...applicant }
    edit.value = true
}

async function saveStatus() {
    console.log("Saving:", selectedApplicant.value)


    const index = applicants.value.findIndex(a => a.email === selectedApplicant.value.email)
    if (index !== -1) applicants.value[index].status = selectedApplicant.value.status

    edit.value = false

    try {
        loadingStore.startLoading()

        const res = await fetch("/api/method/collage.api.applicant.update_applicant", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({
                email: selectedApplicant.value.email,
                status: selectedApplicant.value.status
            })
        })

        loadingStore.stopLoading()

        if (res.ok) {
            const data = await res.json()
            console.log("✅ API JSON Response:", data)

            // ✅ Extract message properly
            let messageText = "Unknown response"
            if (data?.message) {
                if (typeof data.message === "string") {
                    messageText = data.message
                } else if (data.message.message) {
                    messageText = data.message.message
                }
            }

            dialogMessage.value = messageText
            dialog5.value = true

            await fetchApplicants()
        } else {
            console.error(" Failed to update status")
            dialogMessage.value = "Failed to update applicant status"
            dialog5.value = true
        }
    } catch (err) {
        loadingStore.stopLoading()
        console.error(" Error in update status:", err)
        dialogMessage.value = err.message || "Something went wrong"
        dialog5.value = true
    }

}
</script>
