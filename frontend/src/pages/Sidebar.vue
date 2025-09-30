<template>
    <div class="sm:w-20 lg:w-64 bg-green-900 text-white">
        <h2 class="text-2xl font-semibold text-center mt-8">College Portal</h2>
        <nav class=" pr-2 mt-12 space-y-4">
            <div class="bg-green-700 p-2 rounded">
                <router-link>
                    list 1
                </router-link>
            </div>
            <div>
                list 2
            </div>
            <div>
                list 3
            </div>
        </nav>
    </div>
</template>
<script setup>
import { useRouter } from "vue-router"

</script>