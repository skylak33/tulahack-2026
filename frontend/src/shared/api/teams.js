import api from './client'

export const teamsApi = {
  getTeams:     ()             => api.get('/teams/'),
  createTeam:   (data)         => api.post('/teams/', data),
  getTeam:      (id)           => api.get(`/teams/${id}`),
  deleteTeam:   (id)           => api.delete(`/teams/${id}`),
  addMember:    (teamId, data) => api.post(`/teams/${teamId}/members`, data),
  removeMember: (teamId, userId) => api.delete(`/teams/${teamId}/members/${userId}`),
}
