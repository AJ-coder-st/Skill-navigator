import React, { useState, useEffect } from 'react'
import { generatePractice } from '../services/api'
import { Loader2, Code, MessageSquare, Briefcase, BookOpen } from 'lucide-react'

function Practice() {
  const [roadmap, setRoadmap] = useState(null)
  const [role, setRole] = useState('')
  const [skillGaps, setSkillGaps] = useState(null)
  const [practice, setPractice] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    const savedRoadmap = localStorage.getItem('roadmap')
    const savedSkillGaps = localStorage.getItem('skillGaps')
    const savedRole = localStorage.getItem('role')
    
    if (savedRoadmap) {
      try {
        setRoadmap(JSON.parse(savedRoadmap))
      } catch (e) {
        console.error('Error loading roadmap:', e)
      }
    }
    
    if (savedSkillGaps) {
      try {
        setSkillGaps(JSON.parse(savedSkillGaps))
      } catch (e) {
        console.error('Error loading skill gaps:', e)
      }
    }
    
    if (savedRole) {
      setRole(savedRole)
    }
  }, [])

  const handleGeneratePractice = async () => {
    if (!roadmap || !skillGaps) {
      setError('Please complete the analysis and roadmap generation first')
      return
    }

    setLoading(true)
    setError(null)
    try {
      const result = await generatePractice(roadmap, role || 'Software Developer', skillGaps)
      setPractice(result.data)
      localStorage.setItem('practice', JSON.stringify(result.data))
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate practice materials')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="px-4 py-6 sm:px-0">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Practice Materials</h1>

      {error && (
        <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {(!roadmap || !skillGaps) && (
        <div className="mb-6 bg-yellow-50 border border-yellow-200 text-yellow-700 px-4 py-3 rounded">
          Please complete the analysis and roadmap generation first.
        </div>
      )}

      <div className="bg-white shadow rounded-lg p-6 mb-6">
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Target Role
          </label>
          <input
            type="text"
            value={role}
            onChange={(e) => setRole(e.target.value)}
            placeholder="e.g., Data Analyst, Full Stack Developer"
            className="w-full p-2 border border-gray-300 rounded-md"
          />
        </div>
        <button
          onClick={handleGeneratePractice}
          disabled={loading || !roadmap || !skillGaps}
          className="bg-purple-600 text-white px-6 py-2 rounded-md hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
        >
          {loading ? (
            <>
              <Loader2 className="animate-spin h-5 w-5 mr-2" />
              Generating...
            </>
          ) : (
            'Generate Practice Materials'
          )}
        </button>
      </div>

      {practice && (
        <div className="space-y-6">
          {/* Coding Challenges */}
          {practice.coding_challenges && practice.coding_challenges.length > 0 && (
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-xl font-semibold mb-4 flex items-center">
                <Code className="h-6 w-6 mr-2 text-blue-600" />
                Coding Challenges
              </h2>
              <div className="space-y-4">
                {practice.coding_challenges.map((challenge, idx) => (
                  <div key={idx} className="p-4 border border-gray-200 rounded-lg">
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="font-semibold text-gray-900">{challenge.title}</h3>
                      <span className={`px-2 py-1 text-xs rounded ${
                        challenge.difficulty === 'beginner' ? 'bg-green-100 text-green-800' :
                        challenge.difficulty === 'intermediate' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {challenge.difficulty}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 mb-2">{challenge.description}</p>
                    {challenge.skill_focus && (
                      <p className="text-xs text-gray-500 mb-2">
                        <strong>Focus:</strong> {challenge.skill_focus}
                      </p>
                    )}
                    {challenge.requirements && challenge.requirements.length > 0 && (
                      <div className="mb-2">
                        <p className="text-xs font-semibold text-gray-700 mb-1">Requirements:</p>
                        <ul className="list-disc list-inside text-xs text-gray-600">
                          {challenge.requirements.map((req, rIdx) => (
                            <li key={rIdx}>{req}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                    {challenge.hints && challenge.hints.length > 0 && (
                      <details className="mt-2">
                        <summary className="text-xs text-blue-600 cursor-pointer">Show hints</summary>
                        <ul className="list-disc list-inside text-xs text-gray-600 mt-1">
                          {challenge.hints.map((hint, hIdx) => (
                            <li key={hIdx}>{hint}</li>
                          ))}
                        </ul>
                      </details>
                    )}
                    {challenge.estimated_time && (
                      <p className="text-xs text-gray-500 mt-2">
                        Estimated time: {challenge.estimated_time}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Behavioral Questions */}
          {practice.behavioral_questions && practice.behavioral_questions.length > 0 && (
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-xl font-semibold mb-4 flex items-center">
                <MessageSquare className="h-6 w-6 mr-2 text-green-600" />
                Behavioral Interview Questions
              </h2>
              <div className="space-y-4">
                {practice.behavioral_questions.map((question, idx) => (
                  <div key={idx} className="p-4 border border-gray-200 rounded-lg">
                    <h3 className="font-semibold text-gray-900 mb-2">{question.question}</h3>
                    {question.skill_focus && (
                      <p className="text-xs text-gray-500 mb-2">
                        <strong>Focus:</strong> {question.skill_focus}
                      </p>
                    )}
                    {question.guidance && (
                      <div className="mb-2">
                        <p className="text-xs font-semibold text-gray-700 mb-1">What interviewers are looking for:</p>
                        <p className="text-sm text-gray-600">{question.guidance}</p>
                      </div>
                    )}
                    {question.sample_answer_structure && (
                      <details className="mt-2">
                        <summary className="text-xs text-blue-600 cursor-pointer">Answer structure</summary>
                        <p className="text-sm text-gray-600 mt-1">{question.sample_answer_structure}</p>
                      </details>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Mini Projects */}
          {practice.mini_projects && practice.mini_projects.length > 0 && (
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-xl font-semibold mb-4 flex items-center">
                <Briefcase className="h-6 w-6 mr-2 text-purple-600" />
                Mini Projects
              </h2>
              <div className="space-y-4">
                {practice.mini_projects.map((project, idx) => (
                  <div key={idx} className="p-4 border border-gray-200 rounded-lg">
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="font-semibold text-gray-900">{project.title}</h3>
                      <span className={`px-2 py-1 text-xs rounded ${
                        project.difficulty === 'beginner' ? 'bg-green-100 text-green-800' :
                        project.difficulty === 'intermediate' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {project.difficulty}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 mb-2">{project.description}</p>
                    {project.skills_demonstrated && (
                      <p className="text-xs text-gray-500 mb-2">
                        <strong>Skills:</strong> {project.skills_demonstrated.join(', ')}
                      </p>
                    )}
                    {project.scope && (
                      <div className="mb-2">
                        <p className="text-xs font-semibold text-gray-700 mb-1">Scope:</p>
                        <p className="text-sm text-gray-600">{project.scope}</p>
                      </div>
                    )}
                    {project.deliverables && project.deliverables.length > 0 && (
                      <div className="mb-2">
                        <p className="text-xs font-semibold text-gray-700 mb-1">Deliverables:</p>
                        <ul className="list-disc list-inside text-xs text-gray-600">
                          {project.deliverables.map((del, dIdx) => (
                            <li key={dIdx}>{del}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                    {project.estimated_time && (
                      <p className="text-xs text-gray-500 mt-2">
                        Estimated time: {project.estimated_time}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {practice.reasoning && (
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 mb-2">AI Reasoning</h3>
              <p className="text-sm text-gray-700">{practice.reasoning}</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default Practice
