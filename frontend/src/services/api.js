import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const analyzeJD = async (jobDescription) => {
  const response = await api.post('/analyze-jd', {
    job_description: jobDescription,
  })
  return response.data
}

export const analyzeProfile = async (profile) => {
  const response = await api.post('/analyze-profile', profile)
  return response.data
}

export const analyzeSkillGap = async (jobSkills, studentProfile) => {
  const response = await api.post('/skill-gap', {
    job_skills: jobSkills,
    student_profile: studentProfile,
  })
  return response.data
}

export const generateRoadmap = async (skillGaps, timeWeeks = 8) => {
  const response = await api.post('/generate-roadmap', {
    skill_gaps: skillGaps,
    time_weeks: timeWeeks,
  })
  return response.data
}

export const generatePractice = async (roadmap, role, skillGaps) => {
  const response = await api.post('/generate-practice', {
    roadmap,
    role,
    skill_gaps: skillGaps,
  })
  return response.data
}

export const updateProgress = async (originalRoadmap, progress) => {
  const response = await api.post('/update-progress', {
    original_roadmap: originalRoadmap,
    progress,
  })
  return response.data
}

export const getDashboardSummary = async () => {
  const response = await api.get('/dashboard-summary')
  return response.data
}
