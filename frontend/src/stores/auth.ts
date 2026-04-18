import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '@/shared/api/client'
import type { User, AuthResponse } from '@/shared/api/types'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const loading = ref(false)

  const isAuthenticated = computed(() => !!user.value)
  const role = computed(() => user.value?.role ?? null)

  async function login(email: string, password: string) {
    const data = await api.post<AuthResponse>('/auth/login', { email, password })
    localStorage.setItem('access_token', data.access_token)
    localStorage.setItem('refresh_token', data.refresh_token)
    await fetchMe()
  }

  async function register(email: string, password: string, full_name: string, role: string) {
    await api.post('/auth/register', { email, password, full_name, role })
    await login(email, password)
  }

  async function fetchMe() {
    loading.value = true
    try {
      user.value = await api.get<User>('/users/me')
    } finally {
      loading.value = false
    }
  }

  function logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    user.value = null
  }

  return { user, loading, isAuthenticated, role, login, register, fetchMe, logout }
})
