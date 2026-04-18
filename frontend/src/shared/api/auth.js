import api from './client'

export const authApi = {
  login:   (credentials) => api.post('/auth/login', credentials),
  register:(data)        => api.post('/auth/register', data),
  refresh: (refreshToken)=> api.post('/auth/refresh', { refresh_token: refreshToken }),
}
