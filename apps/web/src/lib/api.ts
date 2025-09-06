import axios from 'axios'

export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'
export const api = axios.create({ baseURL: API_URL })

export function setToken(token?: string){
  if(token) api.defaults.headers.common['Authorization'] = `Bearer ${token}`
  else delete api.defaults.headers.common['Authorization']
}
