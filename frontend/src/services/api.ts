import axios from 'axios'

const API_URL = '/api/v1'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_URL}/auth/refresh`, {
            refresh_token: refreshToken,
          })
          
          const { access_token, refresh_token } = response.data
          localStorage.setItem('access_token', access_token)
          localStorage.setItem('refresh_token', refresh_token)
          
          originalRequest.headers.Authorization = `Bearer ${access_token}`
          return api(originalRequest)
        } catch (refreshError) {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          window.location.href = '/login'
        }
      }
    }
    
    return Promise.reject(error)
  }
)

export const authAPI = {
  register: (data: { email: string; username: string; password: string; full_name?: string }) =>
    api.post('/auth/register', data),
  
  login: (data: { email: string; password: string }) =>
    api.post('/auth/login', data),
  
  refresh: (refresh_token: string) =>
    api.post('/auth/refresh', { refresh_token }),
  
  me: () => api.get('/auth/me'),
}

export const documentsAPI = {
  upload: (formData: FormData) =>
    api.post('/documents/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  
  list: () => api.get('/documents'),
  
  get: (id: number) => api.get(`/documents/${id}`),
  
  delete: (id: number) => api.delete(`/documents/${id}`),
}

export const chatAPI = {
  query: (document_id: number, question: string) =>
    api.post('/chat/query', { document_id, question }),
  
  getConversations: () => api.get('/chat/conversations'),
  
  getMessages: (conversationId: number) =>
    api.get(`/chat/conversations/${conversationId}/messages`),
}

export default api
