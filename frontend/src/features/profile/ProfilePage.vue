<template>
  <div class="p-8 max-w-4xl mx-auto">
    <button v-if="isViewingOther" class="btn-ghost btn-sm mb-6" @click="router.back()">
      <ArrowLeft class="w-4 h-4" />
      Назад
    </button>

    <Spinner v-if="loading" full-page />

    <div v-else-if="profileUser" class="space-y-6 animate-stagger">
      <!-- Header card -->
      <div class="card">
        <div class="flex items-start justify-between gap-4">
          <div class="flex items-start gap-5">
            <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-accent-400 to-accent-600 flex items-center justify-center text-white font-display text-xl font-bold shrink-0">
              {{ initials }}
            </div>
            <div>
              <h1 class="font-display text-2xl font-semibold text-ink">{{ profileUser.full_name }}</h1>
              <p class="text-ink-400 mt-0.5">{{ profileUser.email }}</p>
              <div class="flex flex-wrap gap-2 mt-3">
                <span class="badge-accent">{{ roleLabel }}</span>
                <span v-if="profileUser.team_role" class="badge-ink">{{ profileUser.team_role }}</span>
                <span v-if="profileUser.age" class="badge-ink">{{ profileUser.age }} лет</span>
              </div>
            </div>
          </div>

          <!-- Edit button (own profile only) -->
          <button
            v-if="!isViewingOther"
            class="btn-secondary btn-md shrink-0"
            @click="editMode = !editMode"
          >
            <Pencil class="w-4 h-4" />
            {{ editMode ? 'Отмена' : 'Редактировать' }}
          </button>
        </div>
      </div>

      <!-- Edit form -->
      <div v-if="editMode" class="card animate-scale-in">
        <h2 class="font-semibold text-ink mb-5 flex items-center gap-2">
          <Pencil class="w-4 h-4 text-accent" />
          Редактирование профиля
        </h2>
        <ProfileEditForm :user="profileUser" @saved="handleSaved" @cancel="editMode = false" />
      </div>

      <!-- DISC profile -->
      <div class="card">
        <div class="flex items-center gap-2 mb-5">
          <BarChart2 class="w-4 h-4 text-accent" />
          <h2 class="font-semibold text-ink">DISC профиль</h2>
          <span v-if="discDominant" class="badge-accent ml-auto">Доминанта: {{ discDominant }}</span>
        </div>

        <div v-if="profileUser.disc_profile">
          <DiscChart :disc="profileUser.disc_profile" />
        </div>
        <EmptyState
          v-else
          icon="BarChart2"
          title="DISC профиль не заполнен"
          :description="!isViewingOther ? 'Отредактируйте профиль, чтобы добавить DISC-данные' : ''"
        />
      </div>

      <!-- Motivation profile -->
      <div class="card">
        <div class="flex items-center gap-2 mb-5">
          <Zap class="w-4 h-4 text-accent" />
          <h2 class="font-semibold text-ink">Мотивационный профиль</h2>
        </div>

        <div v-if="profileUser.motivation_profile && Object.keys(profileUser.motivation_profile).length">
          <div class="flex flex-wrap gap-2">
            <div
              v-for="(value, key) in profileUser.motivation_profile"
              :key="key"
              class="flex items-center gap-2 px-3 py-2 rounded-xl bg-surface-100 border border-ink-100"
            >
              <span class="text-sm font-medium text-ink">{{ key }}</span>
              <span v-if="typeof value === 'number'" class="text-sm text-ink-400 font-mono">{{ value }}</span>
              <span v-else class="text-sm text-ink-400">{{ value }}</span>
            </div>
          </div>
        </div>
        <EmptyState
          v-else
          icon="Zap"
          title="Мотивационный профиль не заполнен"
          :description="!isViewingOther ? 'Добавьте данные через редактирование профиля' : ''"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, Pencil, BarChart2, Zap } from 'lucide-vue-next'
import { useAuthStore } from '@/stores/auth'
import { usersApi } from '@/shared/api/users'
import Spinner from '@/shared/components/Spinner.vue'
import EmptyState from '@/shared/components/EmptyState.vue'
import DiscChart from '@/shared/components/DiscChart.vue'
import ProfileEditForm from './ProfileEditForm.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const profileUser = ref(null)
const loading = ref(false)
const editMode = ref(false)

const isViewingOther = computed(() => !!route.params.id && route.params.id !== authStore.user?.id?.toString())

const initials = computed(() => {
  const name = profileUser.value?.full_name || ''
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2) || 'U'
})

const roleLabel = computed(() => ({
  manager: 'Руководитель',
  employee: 'Сотрудник',
  candidate: 'Кандидат',
}[profileUser.value?.role] || profileUser.value?.role))

const discDominant = computed(() => {
  const disc = profileUser.value?.disc_profile
  if (!disc) return null
  const sorted = Object.entries(disc).sort(([, a], [, b]) => b - a)
  return sorted[0]?.[0]
})

async function loadProfile() {
  loading.value = true
  try {
    if (isViewingOther.value) {
      const { data } = await usersApi.getUser(route.params.id)
      profileUser.value = data
    } else {
      profileUser.value = authStore.user
    }
  } finally {
    loading.value = false
  }
}

function handleSaved(updated) {
  profileUser.value = updated
  authStore.user = updated
  editMode.value = false
}

onMounted(loadProfile)
</script>
