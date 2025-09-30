<template>
  <!-- ✅ Success Dialog -->
  <Dialog class="fixed inset-0 z-60" :options="{
    title: '🎉 Application Submitted',
    message: 'Your application has been successfully submitted!',
    actions: [{ label: 'Close', variant: 'solid' }],
  }" :disable-outside-click-to-close="true" v-model="dialog5" />

  <div class="min-h-screen items-center justify-center p-8">
    <!-- 🔄 Loading Overlay -->
    <div v-if="loadingStore.isLoading"
      class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50">
      <div class="flex flex-col items-center">
        <svg class="animate-spin h-10 w-10 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"
          viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
        </svg>
        <p class="text-white mt-3 text-sm font-semibold animate-pulse">
          Loading...
        </p>
      </div>
    </div>

    <div>
      <h2 class="text-3xl font-bold text-green-800 text-center mb-2">
        Online Admission Application 2025-2026
      </h2>


    </div>
    <!-- 💎 Glass Card Form -->
    <form @submit.prevent="submitForm" novalidate
      class="relative w-full max-w-8xl bg-white/60 backdrop-blur-xl p-10 space-y-10 animate-fadeIn z-10">
      <!-- 🧍 Personal Details -->
      <section class="bg-gray-100 p-6 rounded-xl shadow-sm">
        <h3 class=" text-xl font-semibold text-gray-100 w-fit p-2 rounded-br-xl bg-green-800 border-b pb-2 mb-5">
          Personal Details
        </h3>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-gray-700 font-medium mb-1">
              First Name <span class="text-red-500">*</span>
            </label>
            <input type="text" v-model="form.first_name" placeholder="Enter first name"
              class="w-full p-3 rounded-lg bg-white text-gray-800 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400"
              @blur="validateField('first_name')" />
            <transition enter-active-class="transition ease-out duration-700" enter-from-class="opacity-0 translate-y-1"
              enter-to-class="opacity-100 translate-y-0" leave-active-class="transition ease-in duration-200"
              leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-1">
              <p v-if="errors.first_name" class="text-red-500 text-sm mt-1">
                {{ errors.first_name }}
              </p>
            </transition>
          </div>


          <div>
            <label class="block text-gray-700 font-medium mb-1">Last Name</label>
            <input type="text" v-model="form.last_name" placeholder="Enter last name"
              class="w-full p-3 rounded-lg bg-white text-gray-800 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400" />
          </div>

          <div>
            <label class="block text-gray-700 font-medium mb-1">Email <span class="text-red-500">*</span></label>
            <input type="email" v-model="form.email" placeholder="example@email.com" @blur="validateField('email')"
              class="w-full p-3 rounded-lg bg-white text-gray-800 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400" />
            <transition enter-active-class="transition ease-out duration-700" enter-from-class="opacity-0 translate-y-1"
              enter-to-class="opacity-100 translate-y-0" leave-active-class="transition ease-in duration-200"
              leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-1">
              <p v-if="errors.email" class="text-red-500 text-sm mt-1">
                {{ errors.email }}
              </p>
            </transition>

          </div>

          <div>
            <label class="block text-gray-700 font-medium mb-1">Phone</label>
            <input type="text" v-model="form.phone" placeholder="+91 98765 43210" pattern="[0-9]{10}"
              title="Enter valid 10-digit phone number"
              class="w-full p-3 rounded-lg bg-white text-gray-800 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400" />
          </div>

          <div>
            <label class="block text-gray-700 font-medium mb-1">Gender</label>
            <select v-model="form.gender"
              class="w-full p-3 rounded-lg bg-white text-gray-800 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400">
              <option disabled value="">Select Gender</option>
              <option>Male</option>
              <option>Female</option>
              <option>Other</option>
            </select>
          </div>

          <div>
            <label class="block text-gray-700 font-medium mb-1">Date of Birth <span
                class="text-red-500">*</span></label>
            <input type="date" v-model="form.date_of_birth" @blur="validateField('date_of_birth')"
              class="w-full p-3 rounded-lg bg-white text-gray-800 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400" />

            <transition enter-active-class="transition ease-out duration-700" enter-from-class="opacity-0 translate-y-1"
              enter-to-class="opacity-100 translate-y-0" leave-active-class="transition ease-in duration-200"
              leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-1">
              <p v-if="errors.date_of_birth" class="text-red-500 text-sm mt-1">
                {{ errors.date_of_birth }}
              </p>
            </transition>
          </div>



        </div>
      </section>

      <!-- 🏠 Address Details -->
      <section class="bg-gray-100 p-6 rounded-xl shadow-sm">
        <h3 class="text-xl font-semibold text-gray-100 w-fit p-2 rounded-br-xl bg-green-800 border-b pb-2 mb-5">
          Address Details
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="md:col-span-2">
            <label class="block text-gray-700 font-medium mb-1">Address</label>
            <textarea v-model="form.address" rows="2" placeholder="Full address"
              class="w-full p-3 rounded-lg bg-white text-gray-800 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400"></textarea>
          </div>
          <div>
            <label class="block text-gray-700 font-medium mb-1">City</label>
            <input type="text" v-model="form.city" placeholder="City"
              class="w-full p-3 rounded-lg bg-white text-gray-800 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400" />
          </div>
          <div>
            <label class="block text-gray-700 font-medium mb-1">State</label>
            <input type="text" v-model="form.state" placeholder="State"
              class="w-full p-3 rounded-lg bg-white text-gray-800 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400" />
          </div>
          <div>
            <label class="block text-gray-700 font-medium mb-1">Postal Code</label>
            <input type="text" v-model="form.postal_code" placeholder="Postal Code" pattern="[0-9]{6}"
              class="w-full p-3 rounded-lg bg-white text-gray-800 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400" />
          </div>
          <div>
            <label class="block text-gray-700 font-medium mb-1">Nationality</label>
            <input type="text" v-model="form.nationality" placeholder="Indian"
              class="w-full p-3 rounded-lg bg-white text-gray-800 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400" />
          </div>
        </div>
      </section>

      <!-- 👨‍👩 Guardian Details -->
      <section class="bg-gray-100 p-6 rounded-xl shadow-sm">
        <h3 class="text-xl font-semibold text-gray-100 w-fit p-2 rounded-br-xl bg-green-800 border-b pb-2 mb-5">
          Guardian Details
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-gray-700 font-medium mb-1">Guardian Name</label>
            <input type="text" v-model="form.guardian_name" placeholder="Guardian full name"
              class="w-full p-3 rounded-lg bg-white text-gray-800 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400" />
          </div>
          <div>
            <label class="block text-gray-700 font-medium mb-1">Guardian Phone</label>
            <input type="text" v-model="form.guardian_phone" placeholder="+91 98765 43210" pattern="[0-9]{10}"
              class="w-full p-3 rounded-lg bg-white text-gray-800 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400" />
          </div>
        </div>
      </section>

      <!-- 🎓 Academic Details -->
      <section class="bg-gray-100 p-6 rounded-xl shadow-sm">
        <h3 class="text-xl font-semibold text-gray-100 w-fit p-2 rounded-br-xl bg-green-800 border-b pb-2 mb-5">
          Academic Details
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-gray-700 font-medium mb-1">Department <span class="text-red-500">*</span></label>
            <select v-model="form.department" @blur="validateField('department')"
              class="w-full p-3 rounded-lg bg-white text-gray-800 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400">
              <option disabled value="">Select Department</option>
              <option v-for="d in departments" :key="d.value" :value="d.value">
                {{ d.label }}
              </option>
            </select>

            <transition enter-active-class="transition ease-out duration-700" enter-from-class="opacity-0 translate-y-1"
              enter-to-class="opacity-100 translate-y-0" leave-active-class="transition ease-in duration-200"
              leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-1">
              <p v-if="errors.department" class="text-red-500 text-sm mt-1">
                {{ errors.department }}
              </p>
            </transition>
          </div>

          <div>
            <label class="block text-gray-700 font-medium mb-1">Program <span class="text-red-500">*</span></label>
            <input type="text" v-model="form.program" readonly placeholder="Auto-filled"
              @blur="validateField('program')"
              class="w-full p-3 rounded-lg bg-gray-100 text-gray-600 border border-gray-300" />

            <transition enter-active-class="transition ease-out duration-700" enter-from-class="opacity-0 translate-y-1"
              enter-to-class="opacity-100 translate-y-0" leave-active-class="transition ease-in duration-200"
              leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-1">
              <p v-if="errors.program" class="text-red-500 text-sm mt-1">
                {{ errors.program }}
              </p>
            </transition>
          </div>

          <div>
            <label class="block text-gray-700 font-medium mb-1">Previous School</label>
            <input type="text" v-model="form.previous_school" placeholder="School Name"
              class="w-full p-3 rounded-lg bg-white text-gray-800 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400" />
          </div>

          <div>
            <label class="block text-gray-700 font-medium mb-1">Marks Obtained (%) <span
                class="text-red-500">*</span></label>
            <input type="number" v-model="form.marks_obtained" min="0" max="100" placeholder="Ex: 85"
              @blur="validateField('marks_obtained')"
              class="w-full p-3 rounded-lg bg-white text-gray-800 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400" />

            <transition enter-active-class="transition ease-out duration-700" enter-from-class="opacity-0 translate-y-1"
              enter-to-class="opacity-100 translate-y-0" leave-active-class="transition ease-in duration-200"
              leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-1">
              <p v-if="errors.marks_obtained" class="text-red-500 text-sm mt-1">
                {{ errors.marks_obtained }}
              </p>
            </transition>
          </div>

          <div>
            <label class="block text-gray-700 font-medium mb-1">12th Certificate <span
                class="text-red-500">*</span></label>
            <input type="file" @change="handleFileUpload($event, '_12th_certificate')" accept=".pdf,.jpg,.png"
              @blur="validateField('_12th_certificate')"
              class="block w-fit text-gray-700 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100" />

            <transition enter-active-class="transition ease-out duration-700" enter-from-class="opacity-0 translate-y-1"
              enter-to-class="opacity-100 translate-y-0" leave-active-class="transition ease-in duration-200"
              leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-1">
              <p v-if="errors._12th_certificate" class="text-red-500 text-sm mt-1">
                {{ errors._12th_certificate }}
              </p>
            </transition>
          </div>

          <div v-if="form.program === 'PG'">
            <label class="block text-gray-700 font-medium mb-1">UG Certificate</label>
            <input type="file" @change="handleFileUpload($event, 'ug_certificate')" accept=".pdf,.jpg,.png"
              class="block w-fit text-gray-700 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100" />
          </div>

          <div class="flex items-center gap-2 mt-2 md:col-span-2">
            <input type="checkbox" id="paid" v-model="form.paid"
              class="h-4 w-4 text-blue-500 rounded-2xl p-2 border-gray-300 focus:ring-blue-400" />
            <label for="paid" class="text-gray-700">Paid</label>
          </div>
        </div>
      </section>

      <!-- Submit -->
      <div class="flex justify-center pt-6">
        <button type="reset"
          class="bg-red-800 w-40 py-3 text-white font-semibold rounded-lg shadow-lg transition delay-150 duration-300 ease-in-out hover:-translate-y-1 hover:scale-110 hover:bg-indigo-500 ">
          Reset
        </button>
        <button
          class="bg-green-800 w-40 py-3 ml-8 text-white font-semibold rounded-lg shadow-lg transition delay-150 duration-300 ease-in-out hover:-translate-y-1 hover:scale-110 hover:bg-indigo-500 ">
          Submit
        </button>
      </div>
    </form>
  </div>
</template>


<script setup>
import { ref, computed, watch } from "vue";
import { createResource, Dialog } from "frappe-ui";
import { useLoadingStore } from "@/stores/loadingStore";

const loadingStore = useLoadingStore();
const dialog5 = ref(false);


// Reactive form fields
const form = ref({
  first_name: "",
  last_name: "",
  email: "",
  phone: "",
  gender: "",
  academic_year: "",
  date_of_birth: "",
  nationality: "",
  address: "",
  city: "",
  state: "",
  postal_code: "",
  guardian_name: "",
  guardian_phone: "",
  department: "",
  program: "",
  previous_school: "",
  marks_obtained: "",
  _12th_certificate: null,
  ug_certificate: null,
  paid: false,
});

// Fetch academic year
const academic = createResource({
    url: 'collage.api.academic_year.get_academic',
    method: 'GET',
    auto: true
});

// Watch academic resource and update form
const academicData = computed(() => academic.data ? academic.data[0] : null);

watch(academicData, (newVal) => {
    if (newVal) {
        loadingStore.startLoading()
        form.value.academic_year = newVal.academic_year ;
        loadingStore.stopLoading()
    }
});

// Optional computed getter
const academic_year = computed(() => year.data.value);

const errors = ref({});

// 📎 Handle File Upload
const handleFileUpload = (e, field) => {
  form.value[field] = e.target.files[0];
  validateField(field);
};

// 🎓 Fetch Departments
const departmentRes = createResource({
  url: "collage.api.department.get_departments",
  method: "GET",
  auto: true,
});

const departments = computed(() =>
  departmentRes.data
    ? departmentRes.data.map((d) => ({
      label: d.department,
      value: d.department,
      program: d.program,
    }))
    : []
);


// Auto-fill program
watch(
  () => form.value.department,
  (dept) => {
    const selected = departments.value.find((d) => d.value === dept);
    form.value.program = selected ? selected.program : "";
  }
);

// ✅ Required fields list
const requiredFields = [
  "first_name",
  "email",
  "date_of_birth",
  "department",
  "program",
  "marks_obtained",
  "_12th_certificate",
];

// ✅ Validate fields dynamically
const validateField = (field) => {
  if (requiredFields.includes(field)) {
    if (!form.value[field]) {
      errors.value[field] = `${field.replace("_", " ")} is required.`;
    } else {
      errors.value[field] = "";
    }
  }
};

// ✅ Validate all fields before submit
const validateForm = () => {
  requiredFields.forEach((f) => validateField(f));
  return Object.values(errors.value).every((msg) => !msg);
};

// 📨 Submit Form with FormData
const submitForm = async () => {
  if (!validateForm()) return;

  const formData = new FormData();

  // Append all form fields
  Object.keys(form.value).forEach((key) => {
    formData.append(key, form.value[key]);
  });

  loadingStore.startLoading();

  try {
    const response = await fetch(
      "/api/method/collage.api.applicant.submit_student_applicant",
      {
        method: "POST",
        body: formData, // ✅ No need for headers, browser handles it
      }
    );

    const data = await response.json();
    if (data.message) {
      dialog5.value = true;
      // reset form
      Object.keys(form.value).forEach((key) => (form.value[key] = key.includes("certificate") ? null : ""));
    }
  } catch (err) {
    alert("Error submitting form");
  } finally {
    loadingStore.stopLoading();
  }
};
</script>


<style scoped>
.animate-fadeIn {
  animation: fadeIn 0.8s ease-out forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
