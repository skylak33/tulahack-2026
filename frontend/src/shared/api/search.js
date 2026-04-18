import api from './client'

export const searchApi = {
  createSearch:     (data) => api.post('/search/', data),
  getSearchHistory: ()     => api.get('/search/'),
  getSearch:        (id)   => api.get(`/search/${id}`),
}
