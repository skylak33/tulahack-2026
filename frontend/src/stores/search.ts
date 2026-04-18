import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from '@/shared/api/client'
import type { SearchRequest } from '@/shared/api/types'

export const useSearchStore = defineStore('search', () => {
  const history = ref<SearchRequest[]>([])
  const current = ref<SearchRequest | null>(null)
  const loading = ref(false)

  async function fetchHistory() {
    loading.value = true
    try {
      history.value = await api.get<SearchRequest[]>('/search')
    } finally {
      loading.value = false
    }
  }

  async function createSearch(queryText: string) {
    loading.value = true
    try {
      const result = await api.post<SearchRequest>('/search', { query_text: queryText })
      current.value = result
      history.value.unshift(result)
      return result
    } finally {
      loading.value = false
    }
  }

  async function fetchById(id: number) {
    loading.value = true
    try {
      current.value = await api.get<SearchRequest>(`/search/${id}`)
    } finally {
      loading.value = false
    }
  }

  return { history, current, loading, fetchHistory, createSearch, fetchById }
})
