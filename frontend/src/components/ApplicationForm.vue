<template>
    <div class="p-6 max-w-md mx-auto space-y-4">
        <h2 class="text-xl font-bold">Application Form</h2>

        <Input type="text" size="sm" label="First Name" variant="subtle" placeholder="First Name"
            v-model="form.first_name" required />
        <Input type="text" size="sm" label="Last Name" variant="subtle" placeholder="Last Name"
            v-model="form.last_name" />
        <Input type="email" size="sm" label="Email" variant="subtle" placeholder="Email" v-model="form.email" />
        <Input type="text" size="sm" label="Phone" variant="subtle" placeholder="Phone" v-model="form.phone" />

        <Input type="select" size="sm" label="Department" variant="subtle" v-model="form.department"
            :options="departments" />

        <Input type="text" size="sm" label="Program" variant="subtle" v-model="form.program" readonly />


        <Input type="checkbox" size="sm" label="Paid" variant="subtle" v-model="form.paid" />

        <Button variant="solid" theme="gray" size="sm" label="Submit" @click="submitForm">
            Submit
        </Button>
    </div>
    <Dialog :options="{
        title: 'Modal Dialog',
        message: 'Application submitted successfully!',
        actions: [
            {
                label: 'Close',
                variant: 'solid',
            },
        ],
    }" :disable-outside-click-to-close="true" v-model="dialog5" />
</template>

<script setup>
import { ref, computed, watch } from "vue";
import { Input, Button, createResource, Dialog } from "frappe-ui";
import { useLoadingStore } from "@/stores/loadingStore"


const loadingStore = useLoadingStore()
const dialog5 = ref(false);

const form = ref({
    first_name: "",
    last_name: "",
    email: "",
    phone: "",
    department: "",
    program: "",
    academic_year: null,   // default
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

const submitForm = async () => {
    console.log(form.value);
    loadingStore.startLoading()
    try {
        const response = await fetch("/api/method/collage.api.applicant.submit_student_applicant", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(form.value)
        });
        const data = await response.json();
        if (data.message) {
            dialog5.value = true;   // ✅ fix: must use .value
            console.log("Success:", data.message);

            form.value = {
                first_name: "",
                last_name: "",
                email: "",
                phone: "",
                department: "",
                program: "",
                academic_year: null,
                paid: false
            };
        }
        loadingStore.stopLoading()
    } catch (err) {
        alert("Error submitting form:", err);
        loadingStore.stopLoading()
    }
};

// Fetch departments
const userResource = createResource({
    url: 'collage.api.department.get_departments',
    method: 'GET',
    auto: true
});

const departments = computed(() => {
    if (!userResource.data) return [];
    return userResource.data.map(d => ({
        label: d.department,
        value: d.department,
        program: d.program
    }));
});

// Watch selected department and update program
watch(() => form.value.department, (selectedDept) => {
    loadingStore.startLoading()
    const dept = departments.value.find(d => d.value === selectedDept);
    form.value.program = dept ? dept.program : "";
    loadingStore.stopLoading()
});
</script>

