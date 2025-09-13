import axios from 'axios'

const API_BASE_URL = 'http://127.0.0.1:8000/api'

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
})

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    console.error('API Request Error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`)
    return response
  },
  (error) => {
    console.error('API Response Error:', error)
    
    if (error.response) {
      // Server responded with error status
      const message = error.response.data?.message || error.response.data?.detail || 'Server error'
      throw new Error(`${error.response.status}: ${message}`)
    } else if (error.request) {
      // Request was made but no response received
      throw new Error('Network error: Unable to connect to server')
    } else {
      // Something else happened
      throw new Error(error.message || 'Unknown error occurred')
    }
  }
)

// API endpoints
export const api = {
  // Delegates
  getDelegates: (params?: any) => apiClient.get('/delegates/', { params }),
  getDelegate: (id: number) => apiClient.get(`/delegates/${id}/`),
  createDelegate: (data: any) => apiClient.post('/delegates/', data),
  updateDelegate: (id: number, data: any) => apiClient.patch(`/delegates/${id}/`, data),
  deleteDelegate: (id: number) => apiClient.delete(`/delegates/${id}/`),
  
  // Departments
  getDepartments: () => apiClient.get('/departments/'),
  getDepartment: (id: number) => apiClient.get(`/departments/${id}/`),
  
  // Courses
  getCourses: (departmentId?: number) => 
    apiClient.get('/courses/', { params: departmentId ? { department: departmentId } : {} }),
  
  // Metrics
  getMetrics: () => apiClient.get('/delegates/metrics/'),
}

export default apiClient

