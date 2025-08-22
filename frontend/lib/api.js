import axios from 'axios'

// Create axios instance with default configuration
const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle errors
apiClient.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    if (error.response?.status === 401) {
      // Unauthorized - redirect to login
      localStorage.removeItem('authToken')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error.response?.data || error)
  }
)

// API methods
const api = {
  // Auth endpoints
  login: (credentials) => apiClient.post('/api/auth/login', credentials),
  register: (userData) => apiClient.post('/api/auth/register', userData),
  
  // Website endpoints
  getWebsites: () => apiClient.get('/api/websites'),
  createWebsite: (websiteData) => {
    // Validate required fields before sending
    if (!websiteData.url) {
      return Promise.reject(new Error('Website URL is required'))
    }
    return apiClient.post('/api/websites', websiteData)
  },
  updateWebsite: (id, websiteData) => apiClient.put(`/api/websites/${id}`, websiteData),
  deleteWebsite: (id) => apiClient.delete(`/api/websites/${id}`),
  scrapeWebsite: (id) => apiClient.post(`/api/websites/${id}/scrape`),
  startScraping: (id) => apiClient.post(`/api/websites/${id}/scrape`), // Alias for backward compatibility
  
  // Chat endpoints
  sendMessage: (websiteId, message) => apiClient.post('/api/chat/', { website_id: websiteId, message }),
  getConversations: (websiteId) => apiClient.get(`/api/chat/conversations/${websiteId}`),
  
  // Embeddings endpoints
  createEmbeddings: (websiteId) => apiClient.post(`/api/embeddings/${websiteId}/create`),
  searchEmbeddings: (websiteId, query) => apiClient.post(`/api/embeddings/${websiteId}/search`, { query }),
}

export default api 