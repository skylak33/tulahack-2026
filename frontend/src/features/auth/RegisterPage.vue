<template>
  <div class="min-h-screen flex items-center justify-center bg-surface-100 p-8">
    <div class="w-full max-w-md animate-slide-up">
      <div class="flex items-center gap-3 mb-8">
        <div class="w-8 h-8 rounded-lg bg-accent flex items-center justify-center">
          <span class="text-white font-display text-sm font-bold">TB</span>
        </div>
        <span class="font-display text-ink font-semibold">Team Builder</span>
      </div>

      <div class="card">
        <h2 class="font-display text-xl font-semibold text-ink mb-1">Создать аккаунт</h2>
        <p class="text-sm text-ink-400 mb-6">Заполните данные для регистрации</p>

        <form @submit.prevent="handleRegister" class="space-y-4">
          <div>
            <label class="label">Полное имя</label>
            <input v-model="form.full_name" type="text" required class="input-base" placeholder="Иванов Иван Иванович" />
          </div>

          <div>
            <label class="label">Email</label>
            <input v-model="form.email" type="email" required class="input-base" placeholder="you@company.com" />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="label">Роль</label>
              <select v-model="form.role" class="input-base" required>
                <option value="manager">Руководитель</option>
                <option value="employee">Сотрудник</option>
                <option value="candidate">Кандидат</option>
              </select>
            </div>
            <div>
              <label class="label">Возраст</label>
              <input v-model.number="form.age" type="number" min="18" max="80" class="input-base" placeholder="30" />
            </div>
          </div>

          <div>
            <label class="label">Пароль</label>
            <input v-model="form.password" type="password" required class="input-base" placeholder="Минимум 8 символов" minlength="8" />
          </div>

          <div>
            <label class="label">Подтвердите пароль</label>
            <input v-model="form.confirmPassword" type="password" required class="input-base" placeholder="Повторите пароль" />
            <p v-if="passwordMismatch" class="text-xs text-rose-500 mt-1">Пароли не совпадают</p>
          </div>

          <div v-if="authStore.error" class="p-3 rounded-xl bg-rose-50 border border-rose-100">
            <p class="text-sm text-rose-600">{{ authStore.error }}</p>
          </div>

          <button type="submit" class="btn-primary btn-lg w-full" :disabled="authStore.loading || passwordMismatch">
            <Spinner v-if="authStore.loading" size="sm" />
            <span>{{ authStore.loading ? 'Регистрируем...' : 'Зарегистрироваться' }}</span>
          </button>
        </form>

        <p class="mt-5 text-center text-sm text-ink-400">
          Уже есть аккаунт?
          <RouterLink to="/login" class="text-accent font-medium hover:text-accent-500 transition-colors">
            Войти
          </RouterLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Spinner from '@/shared/components/Spinner.vue'

const authStore = useAuthStore()
const router = useRouter()

const form = ref({
  full_name: '',
  email: '',
  password: '',
  confirmPassword: '',
  role: 'manager',
  age: null,
})

const passwordMismatch = computed(() =>
  form.value.confirmPassword && form.value.password !== form.value.confirmPassword
)

async function handleRegister() {
  if (passwordMismatch.value) return
  const { confirmPassword, ...payload } = form.value
  const ok = await authStore.register(payload)
  if (ok) router.push('/')
}
</script>
