<template>
  <div class="p-8 max-w-6xl mx-auto">
    <!-- Manager dashboard -->
    <ManagerDashboard v-if="authStore.isManager" />

    <!-- Employee / Candidate dashboard -->
    <ProfileDashboard v-else />
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import ManagerDashboard from './ManagerDashboard.vue'
import ProfileDashboard from '@/features/profile/ProfileDashboard.vue'

const authStore = useAuthStore()
</script>
