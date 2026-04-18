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

  // async function login(credentials) {
  //   loading.value = true
  //   error.value = null
  //   try {
  //     const { data } = await authApi.login(credentials)
  //     setTokens(data.access_token, data.refresh_token)
  //     await fetchMe()
  //     return true
  //   } catch (e) {
  //     error.value = e.response?.data?.detail || 'Ошибка авторизации'
  //     return false
  //   } finally {
  //     loading.value = false
  //   }
  // }
  async function login(credentials) {
  loading.value = true
  // мок
  await new Promise(r => setTimeout(r, 500))
  
  const mockUsers = {
    'manager@test.com': {
      id: 1, email: 'manager@test.com', role: 'manager',
      full_name: 'Иванов Иван', age: 35, team_role: 'lead',
      disc_profile: { D: 72, I: 45, S: 30, C: 60 },
      motivation_profile: { Карьера: 'высокая', Деньги: 'средняя', Признание: 'высокая' }
    },
    'employee@test.com': {
      id: 2, email: 'employee@test.com', role: 'employee',
      full_name: 'Петрова Мария', age: 28, team_role: 'middle',
      disc_profile: { D: 40, I: 80, S: 55, C: 35 },
      motivation_profile: { Команда: 'высокая', Обучение: 'высокая' }
    },
    'candidate@test.com': {
      id: 3, email: 'candidate@test.com', role: 'candidate',
      full_name: 'Сидоров Алексей', age: 24, team_role: 'junior',
      disc_profile: { D: 55, I: 60, S: 70, C: 80 },
      motivation_profile: { Стабильность: 'высокая', Рост: 'средняя' }
    },
  }

  const found = mockUsers[credentials.email]
  if (found && credentials.password === '12345678') {
    user.value = found
    accessToken.value = 'mock-token'
    localStorage.setItem('access_token', 'mock-token')
    loading.value = false
    return true
  }
  error.value = 'Неверный email или пароль'
  loading.value = false
  return false
}

  async function register(userData) {
    loading.value = true
    error.value = null
    try {
      const { data } = await authApi.register(userData)
      setTokens(data.access_token, data.refresh_token)
      await fetchMe()
      return true
    } catch (e) {
      error.value = e.response?.data?.detail || 'Ошибка регистрации'
      return false
    } finally {
      loading.value = false
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


  // async function init() {
  //   if (accessToken.value && !user.value) {
  //     await fetchMe()
  //   }
  // }
  async function init() {
    if (accessToken.value && !user.value) {
      // мок
      const saved = localStorage.getItem('mock_user')
      if (saved) user.value = JSON.parse(saved)
    }
  }  

  return {
    user, accessToken, loading, error,
    isAuthenticated, isManager, isEmployee, isCandidate,
    login, register, logout, fetchMe, init,
  }
})

