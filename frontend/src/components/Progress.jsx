import React, { useState, useEffect } from 'react'
import { updateProgress } from '../services/api'
import { Loader2, TrendingUp, CheckCircle, AlertCircle } from 'lucide-react'

function Progress() {
  const [originalRoadmap, setOriginalRoadmap] = useState(null)
  const [progress, setProgress] = useState({
    completed_milestones: [],
    current_week: 1,
    skill_confidence: {},
    completed_practices: [],
    challenges_faced: []
  })
  const [reflection, setReflection] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    const savedRoadmap = localStorage.getItem('roadmap')
    if (savedRoadmap) {
      try {
        setOriginalRoadmap(JSON.parse(savedRoadmap))
      } catch (e) {
        console.error('Error loading roadmap:', e)
      }
    }
  }, [])

  const handleUpdateProgress = async () => {
    if (!originalRoadmap) {
      setError('Please generate a roadmap first')
      return
    }

    setLoading(true)
    setError(null)
    try {
      const result = await updateProgress(originalRoadmap, progress)
      setReflection(result.data)
      localStorage.setItem('reflection', JSON.stringify(result.data))
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update progress')
    } finally {
      setLoading(false)
    }
  }

  const addMilestone = () => {
    const milestone = prompt('Enter completed milestone:')
    if (milestone) {
      setProgress({
        ...progress,
        completed_milestones: [...progress.completed_milestones, milestone]
      })
    }
  }

  const addPractice = () => {
    const practice = prompt('Enter completed practice task:')
    if (practice) {
      setProgress({
        ...progress,
        completed_practices: [...progress.completed_practices, practice]
      })
    }
  }

  const addChallenge = () => {
    const challenge = prompt('Enter challenge faced:')
    if (challenge) {
      setProgress({
        ...progress,
        challenges_faced: [...progress.challenges_faced, challenge]
      })
    }
  }

  return (
    <div className="px-4 py-6 sm:px-0">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Progress Tracking</h1>

      {error && (
        <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {!originalRoadmap && (
        <div className="mb-6 bg-yellow-50 border border-yellow-200 text-yellow-700 px-4 py-3 rounded">
          Please generate a roadmap first on the Roadmap page.
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Progress Input */}
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Update Your Progress</h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Current Week
              </label>
              <input
                type="number"
                min="1"
                value={progress.current_week}
                onChange={(e) => setProgress({ ...progress, current_week: parseInt(e.target.value) })}
                className="w-full p-2 border border-gray-300 rounded-md"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Completed Milestones
              </label>
              <div className="flex items-center space-x-2 mb-2">
                <button
                  onClick={addMilestone}
                  className="text-sm bg-blue-100 text-blue-700 px-3 py-1 rounded hover:bg-blue-200"
                >
                  + Add Milestone
                </button>
              </div>
              <ul className="list-disc list-inside text-sm text-gray-700">
                {progress.completed_milestones.map((m, idx) => (
                  <li key={idx}>{m}</li>
                ))}
                {progress.completed_milestones.length === 0 && (
                  <li className="text-gray-400">No milestones completed yet</li>
                )}
              </ul>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Completed Practices
              </label>
              <div className="flex items-center space-x-2 mb-2">
                <button
                  onClick={addPractice}
                  className="text-sm bg-green-100 text-green-700 px-3 py-1 rounded hover:bg-green-200"
                >
                  + Add Practice
                </button>
              </div>
              <ul className="list-disc list-inside text-sm text-gray-700">
                {progress.completed_practices.map((p, idx) => (
                  <li key={idx}>{p}</li>
                ))}
                {progress.completed_practices.length === 0 && (
                  <li className="text-gray-400">No practices completed yet</li>
                )}
              </ul>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Challenges Faced
              </label>
              <div className="flex items-center space-x-2 mb-2">
                <button
                  onClick={addChallenge}
                  className="text-sm bg-yellow-100 text-yellow-700 px-3 py-1 rounded hover:bg-yellow-200"
                >
                  + Add Challenge
                </button>
              </div>
              <ul className="list-disc list-inside text-sm text-gray-700">
                {progress.challenges_faced.map((c, idx) => (
                  <li key={idx}>{c}</li>
                ))}
                {progress.challenges_faced.length === 0 && (
                  <li className="text-gray-400">No challenges recorded</li>
                )}
              </ul>
            </div>

            <button
              onClick={handleUpdateProgress}
              disabled={loading || !originalRoadmap}
              className="w-full bg-purple-600 text-white px-4 py-2 rounded-md hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
            >
              {loading ? (
                <>
                  <Loader2 className="animate-spin h-5 w-5 mr-2" />
                  Analyzing...
                </>
              ) : (
                <>
                  <TrendingUp className="h-5 w-5 mr-2" />
                  Get Progress Reflection
                </>
              )}
            </button>
          </div>
        </div>

        {/* Reflection Results */}
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4 flex items-center">
            <TrendingUp className="h-6 w-6 mr-2 text-purple-600" />
            AI Reflection
          </h2>

          {reflection ? (
            <div className="space-y-4">
              <div className="p-4 bg-blue-50 border border-blue-200 rounded">
                <h3 className="font-semibold text-blue-900 mb-2">Progress Summary</h3>
                <p className="text-sm text-blue-800">{reflection.progress_summary}</p>
              </div>

              {reflection.strengths_identified && reflection.strengths_identified.length > 0 && (
                <div className="p-4 bg-green-50 border border-green-200 rounded">
                  <h3 className="font-semibold text-green-900 mb-2 flex items-center">
                    <CheckCircle className="h-4 w-4 mr-2" />
                    Strengths Identified
                  </h3>
                  <ul className="list-disc list-inside text-sm text-green-800">
                    {reflection.strengths_identified.map((strength, idx) => (
                      <li key={idx}>{strength}</li>
                    ))}
                  </ul>
                </div>
              )}

              {reflection.areas_needing_attention && reflection.areas_needing_attention.length > 0 && (
                <div className="p-4 bg-yellow-50 border border-yellow-200 rounded">
                  <h3 className="font-semibold text-yellow-900 mb-2 flex items-center">
                    <AlertCircle className="h-4 w-4 mr-2" />
                    Areas Needing Attention
                  </h3>
                  <div className="space-y-2">
                    {reflection.areas_needing_attention.map((area, idx) => (
                      <div key={idx} className="text-sm text-yellow-800">
                        <p className="font-medium">{area.area}</p>
                        <p className="text-xs mt-1">{area.reason}</p>
                        <p className="text-xs mt-1 italic">{area.recommendation}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {reflection.updated_roadmap && (
                <div className="p-4 bg-gray-50 border border-gray-200 rounded">
                  <h3 className="font-semibold text-gray-900 mb-2">Updated Recommendations</h3>
                  {reflection.updated_roadmap.adjustments && (
                    <div className="mb-2">
                      <p className="text-xs font-semibold text-gray-700 mb-1">Adjustments:</p>
                      <ul className="list-disc list-inside text-sm text-gray-700">
                        {reflection.updated_roadmap.adjustments.map((adj, idx) => (
                          <li key={idx}>{adj}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  {reflection.updated_roadmap.next_priorities && (
                    <div className="mb-2">
                      <p className="text-xs font-semibold text-gray-700 mb-1">Next Priorities:</p>
                      <ul className="list-disc list-inside text-sm text-gray-700">
                        {reflection.updated_roadmap.next_priorities.map((pri, idx) => (
                          <li key={idx}>{pri}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}

              {reflection.encouragement && (
                <div className="p-4 bg-purple-50 border border-purple-200 rounded">
                  <h3 className="font-semibold text-purple-900 mb-2">Encouragement</h3>
                  <p className="text-sm text-purple-800">{reflection.encouragement}</p>
                </div>
              )}

              {reflection.reasoning && (
                <div className="p-4 bg-gray-50 border border-gray-200 rounded">
                  <h3 className="font-semibold text-gray-900 mb-2">AI Reasoning</h3>
                  <p className="text-sm text-gray-700">{reflection.reasoning}</p>
                </div>
              )}
            </div>
          ) : (
            <div className="text-center text-gray-500 py-8">
              Complete your progress and click "Get Progress Reflection" to see AI insights
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Progress
