import { defineStore } from 'pinia'
import { ref } from 'vue'
import { teamsApi } from '@/shared/api/teams'

export const useTeamsStore = defineStore('teams', () => {
  const teams = ref([])
  const loading = ref(false)
  const error = ref(null)

  async function fetchTeams() {
    loading.value = true
    try {
      const { data } = await teamsApi.getTeams()
      teams.value = data
    } catch (e) {
      error.value = e.response?.data?.detail || 'Ошибка загрузки команд'
    } finally {
      loading.value = false
    }
  }

  async function createTeam(name) {
    loading.value = true
    error.value = null
    try {
      const { data } = await teamsApi.createTeam({ name })
      teams.value.push(data)
      return data
    } catch (e) {
      error.value = e.response?.data?.detail || 'Ошибка создания команды'
      return null
    } finally {
      loading.value = false
    }
  }

  async function addMember(teamId, userId) {
    try {
      await teamsApi.addMember(teamId, { user_id: userId })
      await fetchTeams()
    } catch (e) {
      error.value = e.response?.data?.detail || 'Ошибка добавления участника'
    }
  }

  async function removeMember(teamId, userId) {
    try {
      await teamsApi.removeMember(teamId, userId)
      await fetchTeams()
    } catch (e) {
      error.value = e.response?.data?.detail || 'Ошибка удаления участника'
    }
  }

  return { teams, loading, error, fetchTeams, createTeam, addMember, removeMember }
})
