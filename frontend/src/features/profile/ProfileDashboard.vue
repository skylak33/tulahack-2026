<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Мой профиль</h1>
      <p class="page-subtitle">Ваши данные, DISC и мотивационный профиль</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Profile summary -->
      <div class="lg:col-span-1">
        <div class="card text-center">
          <div class="w-20 h-20 rounded-2xl bg-gradient-to-br from-accent-400 to-accent-600 flex items-center justify-center text-white font-display text-2xl font-bold mx-auto mb-4">
            {{ initials }}
          </div>
          <h2 class="font-display font-semibold text-ink text-lg">{{ authStore.user?.full_name }}</h2>
          <p class="text-ink-400 text-sm mt-0.5">{{ authStore.user?.email }}</p>
          <div class="flex justify-center flex-wrap gap-2 mt-3">
            <span class="badge-accent">{{ roleLabel }}</span>
            <span v-if="authStore.user?.team_role" class="badge-ink">{{ authStore.user.team_role }}</span>
          </div>
          <RouterLink to="/profile" class="btn-secondary btn-sm mt-4 w-full">
            <Pencil class="w-3.5 h-3.5" />
            Редактировать
          </RouterLink>
        </div>
      </div>

      <!-- DISC + motivation -->
      <div class="lg:col-span-2 space-y-5">
        <div class="card">
          <div class="flex items-center gap-2 mb-5">
            <BarChart2 class="w-4 h-4 text-accent" />
            <h2 class="font-semibold text-ink">DISC профиль</h2>
          </div>
          <DiscChart v-if="authStore.user?.disc_profile" :disc="authStore.user.disc_profile" />
          <EmptyState v-else icon="BarChart2" title="Профиль DISC не заполнен" />
        </div>

        <div class="card">
          <div class="flex items-center gap-2 mb-5">
            <Zap class="w-4 h-4 text-accent" />
            <h2 class="font-semibold text-ink">Мотивация</h2>
          </div>
          <div v-if="authStore.user?.motivation_profile && Object.keys(authStore.user.motivation_profile).length" class="flex flex-wrap gap-2">
            <div
              v-for="(value, key) in authStore.user.motivation_profile"
              :key="key"
              class="px-3 py-2 rounded-xl bg-surface-100 border border-ink-100 text-sm"
            >
              <span class="font-medium text-ink">{{ key }}</span>
              <span class="text-ink-400 ml-2">{{ value }}</span>
            </div>
          </div>
          <EmptyState v-else icon="Zap" title="Мотивационный профиль не заполнен" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { Pencil, BarChart2, Zap } from 'lucide-vue-next'
import { useAuthStore } from '@/stores/auth'
import DiscChart from '@/shared/components/DiscChart.vue'
import EmptyState from '@/shared/components/EmptyState.vue'

const authStore = useAuthStore()

const initials = computed(() => {
  const name = authStore.user?.full_name || ''
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2) || 'U'
})

const roleLabel = computed(() => ({
  manager: 'Руководитель',
  employee: 'Сотрудник',
  candidate: 'Кандидат',
}[authStore.user?.role] || authStore.user?.role))
</script>
