import api from './client'

export const teamsApi = {
  getTeams: () => api.get('/teams'),
  createTeam: (data) => api.post('/teams', data),
  addMember: (teamId, data) => api.post(`/teams/${teamId}/members`, data),
  removeMember: (teamId, userId) => api.delete(`/teams/${teamId}/members/${userId}`),
}
