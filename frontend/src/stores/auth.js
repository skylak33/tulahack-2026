import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/shared/api/auth'
import { usersApi } from '@/shared/api/users'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const accessToken = ref(localStorage.getItem('access_token'))
  const refreshToken = ref(localStorage.getItem('refresh_token'))
  const loading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => !!accessToken.value && !!user.value)
  const isManager = computed(() => user.value?.role === 'manager')
  const isEmployee = computed(() => user.value?.role === 'employee')
  const isCandidate = computed(() => user.value?.role === 'candidate')

  function setTokens(access, refresh) {
    accessToken.value = access
    refreshToken.value = refresh
    localStorage.setItem('access_token', access)
    if (refresh) localStorage.setItem('refresh_token', refresh)
  }

  function clearTokens() {
    accessToken.value = null
    refreshToken.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  async function login(credentials) {
    loading.value = true
    error.value = null
    try {
      const { data } = await authApi.login(credentials)
      setTokens(data.access_token, data.refresh_token)
      await fetchMe()
      return true
    } catch (e) {
      error.value = e.response?.data?.detail || 'Ошибка авторизации'
      return false
    } finally {
      loading.value = false
    }
  }

  async function register(userData) {
    loading.value = true
    error.value = null
    try {
      // Backend returns UserFull on register (no tokens) — login separately
      await authApi.register(userData)
      const ok = await login({ email: userData.email, password: userData.password })
      return ok
    } catch (e) {
      error.value = e.response?.data?.detail || 'Ошибка регистрации'
      loading.value = false
      return false
    }
  }

  async function fetchMe() {
    try {
      const { data } = await usersApi.getMe()
      user.value = data
    } catch (e) {
      clearTokens()
      user.value = null
    }
  }

  function logout() {
    user.value = null
    clearTokens()
  }

  async function init() {
    if (accessToken.value && !user.value) {
      await fetchMe()
    }
  }

  return {
    user, accessToken, loading, error,
    isAuthenticated, isManager, isEmployee, isCandidate,
    login, register, logout, fetchMe, init,
  }
})
