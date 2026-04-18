<template>
  <div class="min-h-screen flex bg-surface-100">
    <!-- Left panel -->
    <div class="hidden lg:flex flex-col justify-between w-96 bg-ink p-10 shrink-0">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-xl bg-accent flex items-center justify-center">
          <span class="text-white font-display text-base font-bold">TB</span>
        </div>
        <span class="font-display text-white font-semibold tracking-wide">Team Builder</span>
      </div>

      <div class="space-y-6">
        <h1 class="font-display text-3xl text-white font-semibold leading-tight">
          Найдите<br/>идеального<br/>кандидата
        </h1>
        <p class="text-ink-300 text-sm leading-relaxed">
          Интеллектуальная платформа подбора сотрудников с учётом DISC-профиля,
          мотивации и совместимости с командой.
        </p>
        <div class="space-y-3">
          <div v-for="feature in features" :key="feature" class="flex items-center gap-3">
            <div class="w-1.5 h-1.5 rounded-full bg-accent-400 shrink-0" />
            <span class="text-sm text-ink-300">{{ feature }}</span>
          </div>
        </div>
      </div>

      <p class="text-xs text-ink-500">TulaHack 2026 · Задача 4</p>
    </div>

    <!-- Right panel -->
    <div class="flex-1 flex items-center justify-center p-8">
      <div class="w-full max-w-sm animate-slide-up">
        <div class="lg:hidden flex items-center gap-3 mb-8">
          <div class="w-8 h-8 rounded-lg bg-accent flex items-center justify-center">
            <span class="text-white font-display text-sm font-bold">TB</span>
          </div>
          <span class="font-display text-ink font-semibold">Team Builder</span>
        </div>

        <h2 class="font-display text-2xl font-semibold text-ink mb-1">Войти в аккаунт</h2>
        <p class="text-sm text-ink-400 mb-8">Введите ваши данные для входа</p>

        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label class="label">Email</label>
            <input
              v-model="form.email"
              type="email"
              required
              class="input-base"
              placeholder="you@company.com"
              autocomplete="email"
            />
          </div>
          <div>
            <label class="label">Пароль</label>
            <div class="relative">
              <input
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                required
                class="input-base pr-10"
                placeholder="••••••••"
                autocomplete="current-password"
              />
              <button
                type="button"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-ink-300 hover:text-ink-500 transition-colors"
                @click="showPassword = !showPassword"
              >
                <Eye v-if="!showPassword" class="w-4 h-4" />
                <EyeOff v-else class="w-4 h-4" />
              </button>
            </div>
          </div>

          <div v-if="authStore.error" class="p-3 rounded-xl bg-rose-50 border border-rose-100 flex items-center gap-2">
            <AlertCircle class="w-4 h-4 text-rose-500 shrink-0" />
            <p class="text-sm text-rose-600">{{ authStore.error }}</p>
          </div>

          <button
            type="submit"
            class="btn-primary btn-lg w-full"
            :disabled="authStore.loading"
          >
            <Spinner v-if="authStore.loading" size="sm" />
            <span>{{ authStore.loading ? 'Входим...' : 'Войти' }}</span>
          </button>
        </form>

        <p class="mt-6 text-center text-sm text-ink-400">
          Нет аккаунта?
          <RouterLink to="/register" class="text-accent font-medium hover:text-accent-500 transition-colors">
            Зарегистрироваться
          </RouterLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { Eye, EyeOff, AlertCircle } from 'lucide-vue-next'
import { useAuthStore } from '@/stores/auth'
import Spinner from '@/shared/components/Spinner.vue'

const authStore = useAuthStore()
const router = useRouter()

const form = ref({ email: '', password: '' })
const showPassword = ref(false)

const features = [
  'Анализ DISC-профиля и совместимости',
  'Поиск кандидатов через Gemini AI',
  'Мотивационное профилирование',
  'Командная аналитика',
]

async function handleLogin() {
  const ok = await authStore.login(form.value)
  if (ok) router.push('/')
}
</script>
