import React, { useState, useEffect } from 'react'
import { generateRoadmap } from '../services/api'
import { Loader2, Calendar, BookOpen, Target, CheckCircle } from 'lucide-react'

function Roadmap() {
  const [skillGaps, setSkillGaps] = useState(null)
  const [timeWeeks, setTimeWeeks] = useState(8)
  const [roadmap, setRoadmap] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // Load skill gaps from localStorage if available
  useEffect(() => {
    const savedSkillGaps = localStorage.getItem('skillGaps')
    if (savedSkillGaps) {
      try {
        setSkillGaps(JSON.parse(savedSkillGaps))
      } catch (e) {
        console.error('Error loading skill gaps:', e)
      }
    }
  }, [])

  // Save skill gaps to localStorage when Analysis component updates it
  useEffect(() => {
    const handleStorageChange = () => {
      const savedSkillGaps = localStorage.getItem('skillGaps')
      if (savedSkillGaps) {
        try {
          setSkillGaps(JSON.parse(savedSkillGaps))
        } catch (e) {
          console.error('Error loading skill gaps:', e)
        }
      }
    }
    window.addEventListener('storage', handleStorageChange)
    return () => window.removeEventListener('storage', handleStorageChange)
  }, [])

  const handleGenerateRoadmap = async () => {
    if (!skillGaps) {
      setError('Please complete the skill gap analysis first on the Analysis page')
      return
    }

    setLoading(true)
    setError(null)
    try {
      const result = await generateRoadmap(skillGaps, timeWeeks)
      setRoadmap(result.data)
      localStorage.setItem('roadmap', JSON.stringify(result.data))
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate roadmap')
    } finally {
      setLoading(false)
    }
  }

  // Try to load roadmap from localStorage on mount
  useEffect(() => {
    const savedRoadmap = localStorage.getItem('roadmap')
    if (savedRoadmap) {
      try {
        setRoadmap(JSON.parse(savedRoadmap))
      } catch (e) {
        console.error('Error loading roadmap:', e)
      }
    }
  }, [])

  return (
    <div className="px-4 py-6 sm:px-0">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Learning Roadmap</h1>

      {error && (
        <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {!skillGaps && (
        <div className="mb-6 bg-yellow-50 border border-yellow-200 text-yellow-700 px-4 py-3 rounded">
          Please complete the skill gap analysis on the Analysis page first.
        </div>
      )}

      <div className="bg-white shadow rounded-lg p-6 mb-6">
        <div className="flex items-center justify-between">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Timeline (weeks)
            </label>
            <input
              type="number"
              min="4"
              max="12"
              value={timeWeeks}
              onChange={(e) => setTimeWeeks(parseInt(e.target.value))}
              className="w-32 p-2 border border-gray-300 rounded-md"
            />
          </div>
          <button
            onClick={handleGenerateRoadmap}
            disabled={loading || !skillGaps}
            className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
          >
            {loading ? (
              <>
                <Loader2 className="animate-spin h-5 w-5 mr-2" />
                Generating...
              </>
            ) : (
              'Generate Roadmap'
            )}
          </button>
        </div>
      </div>

      {roadmap && (
        <div className="space-y-6">
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <Calendar className="h-6 w-6 mr-2 text-blue-600" />
              {roadmap.total_weeks}-Week Learning Roadmap
            </h2>
            {roadmap.reasoning && (
              <div className="mb-4 p-4 bg-gray-50 border border-gray-200 rounded">
                <p className="text-sm text-gray-700">{roadmap.reasoning}</p>
              </div>
            )}
          </div>

          {roadmap.weeks?.map((week, idx) => (
            <div key={idx} className="bg-white shadow rounded-lg p-6">
              <div className="flex items-center mb-4">
                <div className="flex-shrink-0 w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                  <span className="text-blue-600 font-bold">{week.week_number}</span>
                </div>
                <div className="ml-4">
                  <h3 className="text-lg font-semibold text-gray-900">Week {week.week_number}</h3>
                  <p className="text-sm text-gray-600">
                    Focus: {week.focus_skills?.join(', ') || 'N/A'}
                  </p>
                </div>
              </div>

              <div className="mt-4 space-y-4">
                {week.learning_objectives && week.learning_objectives.length > 0 && (
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2 flex items-center">
                      <Target className="h-4 w-4 mr-2 text-green-600" />
                      Learning Objectives
                    </h4>
                    <ul className="list-disc list-inside text-sm text-gray-700 space-y-1">
                      {week.learning_objectives.map((obj, objIdx) => (
                        <li key={objIdx}>{obj}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {week.milestones && week.milestones.length > 0 && (
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2 flex items-center">
                      <CheckCircle className="h-4 w-4 mr-2 text-blue-600" />
                      Milestones
                    </h4>
                    <div className="space-y-3">
                      {week.milestones.map((milestone, mIdx) => (
                        <div key={mIdx} className="p-3 bg-gray-50 rounded border border-gray-200">
                          <div className="flex items-start justify-between">
                            <div className="flex-1">
                              <h5 className="font-medium text-gray-900">{milestone.title}</h5>
                              <p className="text-sm text-gray-600 mt-1">{milestone.description}</p>
                              {milestone.skills_covered && (
                                <p className="text-xs text-gray-500 mt-1">
                                  Skills: {milestone.skills_covered.join(', ')}
                                </p>
                              )}
                              {milestone.estimated_hours && (
                                <p className="text-xs text-gray-500 mt-1">
                                  Estimated: {milestone.estimated_hours} hours
                                </p>
                              )}
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {week.practice_tasks && week.practice_tasks.length > 0 && (
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2 flex items-center">
                      <BookOpen className="h-4 w-4 mr-2 text-purple-600" />
                      Practice Tasks
                    </h4>
                    <ul className="list-disc list-inside text-sm text-gray-700 space-y-1">
                      {week.practice_tasks.map((task, tIdx) => (
                        <li key={tIdx}>{task}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {week.checkpoint && (
                  <div className="p-3 bg-blue-50 border border-blue-200 rounded">
                    <h4 className="font-semibold text-blue-900 mb-1">Checkpoint</h4>
                    <p className="text-sm text-blue-800">{week.checkpoint}</p>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default Roadmap
