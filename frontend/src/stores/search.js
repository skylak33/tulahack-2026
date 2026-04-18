import { defineStore } from 'pinia'
import { ref } from 'vue'
import { searchApi } from '@/shared/api/search'

// Normalize backend CandidateResult → flat shape expected by CandidateCard
function normalizeCandidate(c) {
  const u = c.user || {}
  return {
    id: u.id,
    user_id: u.id,
    full_name: u.full_name,
    team_role: u.team_role,
    age: u.age,
    disc_profile: u.disc_profile,
    motivation_profile: u.motivation_profile,
    compatibility_score: c.compatibility_score,
    description: c.compatibility_summary,
    strengths: c.strengths || [],
    risks: c.risks || [],
  }
}

// Normalize full SearchRequest returned by backend
function normalizeSearch(raw) {
  if (!raw) return raw
  const candidates = raw.verdict?.candidates?.map(normalizeCandidate) ?? []
  return {
    ...raw,
    verdict: {
      candidates,
      summary: raw.verdict?.summary ?? '',
    },
  }
}

export const useSearchStore = defineStore('search', () => {
  const history = ref([])
  const currentSearch = ref(null)
  const loading = ref(false)
  const error = ref(null)

  async function fetchHistory() {
    loading.value = true
    try {
      const { data } = await searchApi.getSearchHistory()
      // Backend returns { total, items }
      history.value = (data.items ?? []).map(normalizeSearch)
    } catch (e) {
      error.value = e.response?.data?.detail || 'Ошибка загрузки истории'
    } finally {
      loading.value = false
    }
  }

  async function createSearch(queryText, teamId) {
    loading.value = true
    error.value = null
    try {
      const { data } = await searchApi.createSearch({ query_text: queryText, team_id: teamId })
      const normalized = normalizeSearch(data)
      currentSearch.value = normalized
      history.value.unshift(normalized)
      return normalized
    } catch (e) {
      error.value = e.response?.data?.detail || 'Ошибка поиска'
      return null
    } finally {
      loading.value = false
    }
  }

  async function getSearch(id) {
    loading.value = true
    try {
      const { data } = await searchApi.getSearch(id)
      const normalized = normalizeSearch(data)
      currentSearch.value = normalized
      return normalized
    } catch (e) {
      error.value = e.response?.data?.detail || 'Ошибка загрузки'
      return null
    } finally {
      loading.value = false
    }
  }

  return { history, currentSearch, loading, error, fetchHistory, createSearch, getSearch }
})
