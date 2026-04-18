import { defineStore } from 'pinia'
import { ref } from 'vue'
import { searchApi } from '@/shared/api/search'

export const useSearchStore = defineStore('search', () => {
  const history = ref([])
  const currentSearch = ref(null)
  const loading = ref(false)
  const error = ref(null)

  async function fetchHistory() {
    loading.value = true
    try {
      const { data } = await searchApi.getSearchHistory()
      history.value = data
    } catch (e) {
      error.value = e.response?.data?.detail || 'Ошибка загрузки истории'
    } finally {
      loading.value = false
    }
  }

  // async function createSearch(queryText) {
  //   loading.value = true
  //   error.value = null
  //   try {
  //     const { data } = await searchApi.createSearch({ query_text: queryText })
  //     currentSearch.value = data
  //     history.value.unshift(data)
  //     return data
  //   } catch (e) {
  //     error.value = e.response?.data?.detail || 'Ошибка поиска'
  //     return null
  //   } finally {
  //     loading.value = false
  //   }
  // }
  async function createSearch(queryText) {
  loading.value = true
  await new Promise(r => setTimeout(r, 1500)) // тоже мок
  const mockResult = {
    id: Date.now(),
    query_text: queryText,
    created_at: new Date().toISOString(),
    verdict: [
      { user_id: 10, full_name: 'Козлов Дмитрий', team_role: 'senior', age: 31,
        disc_type: 'D', compatibility_score: 87,
        motivation_profile: { Карьера: 'высокая' },
        description: 'Сильный технический лидер с опытом в agile-командах.' },
      { user_id: 11, full_name: 'Новикова Елена', team_role: 'middle', age: 27,
        disc_type: 'I', compatibility_score: 74,
        motivation_profile: { Команда: 'высокая' },
        description: 'Хорошо работает в команде, высокий EQ.' },
      { user_id: 12, full_name: 'Морозов Павел', team_role: 'lead', age: 38,
        disc_type: 'C', compatibility_score: 61,
        motivation_profile: { Качество: 'высокая' },
        description: 'Методичный, ориентирован на качество кода.' },
    ]
  }
  currentSearch.value = mockResult
  history.value.unshift(mockResult)
  loading.value = false
  return mockResult
}

  async function getSearch(id) {
    loading.value = true
    try {
      const { data } = await searchApi.getSearch(id)
      currentSearch.value = data
      return data
    } catch (e) {
      error.value = e.response?.data?.detail || 'Ошибка загрузки'
      return null
    } finally {
      loading.value = false
    }
  }

  return { history, currentSearch, loading, error, fetchHistory, createSearch, getSearch }
})
