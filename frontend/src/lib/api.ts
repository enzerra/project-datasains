import axios from 'axios'

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  timeout: 180_000,
})

api.interceptors.request.use((config) => {
  config.headers['X-Request-ID'] = crypto.randomUUID()
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const message = error.response?.data?.detail || 'Something went wrong'
    return Promise.reject(new Error(message))
  },
)

export default api
