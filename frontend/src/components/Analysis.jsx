import React, { useState, useEffect } from 'react'
import { analyzeJD, analyzeProfile, analyzeSkillGap } from '../services/api'
import SkillGapChart from './SkillGapChart'
import AIResponsePanel, { 
  SkillCard, MatchScore, InsightCard, AccordionSection, LoadingSkeleton 
} from './AIResponsePanel'
import { 
  Loader2, CheckCircle, XCircle, AlertCircle, Sparkles, 
  Target, TrendingUp, Lightbulb, Copy, RefreshCw, FileText,
  Award, AlertTriangle, BookOpen, Code, Database, Wrench
} from 'lucide-react'

function Analysis() {
  const [jobDescription, setJobDescription] = useState('')
  const [profile, setProfile] = useState({
    degree: '',
    skills: '',
    experience_level: 'beginner',
    projects: '',
    certifications: '',
  })
  
  const [jdResult, setJdResult] = useState(null)
  const [profileResult, setProfileResult] = useState(null)
  const [skillGapResult, setSkillGapResult] = useState(null)
  const [loading, setLoading] = useState({ jd: false, profile: false, gap: false })
  const [error, setError] = useState(null)

  // Load from localStorage on mount
  useEffect(() => {
    const savedJd = localStorage.getItem('jdResult')
    const savedProfile = localStorage.getItem('profileResult')
    const savedGaps = localStorage.getItem('skillGaps')
    
    if (savedJd) setJdResult(JSON.parse(savedJd))
    if (savedProfile) setProfileResult(JSON.parse(savedProfile))
    if (savedGaps) setSkillGapResult(JSON.parse(savedGaps))
  }, [])

  const handleAnalyzeJD = async () => {
    if (!jobDescription.trim()) {
      setError('Please enter a job description')
      return
    }
    
    setLoading(prev => ({ ...prev, jd: true }))
    setError(null)
    try {
      const result = await analyzeJD(jobDescription)
      const data = result.data || result
      setJdResult(data)
      localStorage.setItem('jdResult', JSON.stringify(data))
      localStorage.setItem('role', data.role || '')
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to analyze job description')
    } finally {
      setLoading(prev => ({ ...prev, jd: false }))
    }
  }

  const handleAnalyzeProfile = async () => {
    const profileData = {
      degree: profile.degree,
      skills: profile.skills.split(',').map(s => s.trim()).filter(s => s),
      experience_level: profile.experience_level,
      projects: profile.projects.split(',').map(s => s.trim()).filter(s => s),
      certifications: profile.certifications.split(',').map(s => s.trim()).filter(s => s),
    }
    
    setLoading(prev => ({ ...prev, profile: true }))
    setError(null)
    try {
      const result = await analyzeProfile(profileData)
      const data = result.data || result
      setProfileResult(data)
      localStorage.setItem('profileResult', JSON.stringify(data))
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to analyze profile')
    } finally {
      setLoading(prev => ({ ...prev, profile: false }))
    }
  }

  const handleAnalyzeSkillGap = async () => {
    if (!jdResult || !profileResult) {
      setError('Please analyze both job description and profile first')
      return
    }
    
    setLoading(prev => ({ ...prev, gap: true }))
    setError(null)
    try {
      const result = await analyzeSkillGap(jdResult, profileResult)
      const data = result.data || result
      setSkillGapResult(data)
      localStorage.setItem('skillGaps', JSON.stringify(data))
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to analyze skill gaps')
    } finally {
      setLoading(prev => ({ ...prev, gap: false }))
    }
  }

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
    // Could add toast notification here
  }

  const getSkillIcon = (skill) => {
    const skillLower = skill.toLowerCase()
    if (skillLower.includes('python') || skillLower.includes('java') || skillLower.includes('javascript')) return Code
    if (skillLower.includes('sql') || skillLower.includes('database') || skillLower.includes('mongodb')) return Database
    if (skillLower.includes('react') || skillLower.includes('node') || skillLower.includes('framework')) return Code
    if (skillLower.includes('aws') || skillLower.includes('docker') || skillLower.includes('git')) return Wrench
    return BookOpen
  }

  const calculateMatchScore = () => {
    if (!skillGapResult) return 0
    const total = (skillGapResult.strong_skills?.length || 0) + 
                  (skillGapResult.partial_skills?.length || 0) + 
                  (skillGapResult.missing_skills?.length || 0)
    if (total === 0) return 0
    const strong = skillGapResult.strong_skills?.length || 0
    const partial = (skillGapResult.partial_skills?.length || 0) * 0.5
    return (strong + partial) / total
  }

  return (
    <div className="px-4 py-6 sm:px-0 max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">Skill Gap Analysis</h1>
        <p className="text-gray-600">Get AI-powered insights into your career readiness</p>
      </div>

      {error && (
        <div className="mb-6 bg-red-50 border-2 border-red-200 text-red-700 px-6 py-4 rounded-lg flex items-center gap-3 animate-fadeIn">
          <AlertCircle className="h-5 w-5 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Job Description Section */}
        <div className="bg-white shadow-lg rounded-xl p-6 border-2 border-gray-100">
          <div className="flex items-center gap-2 mb-4">
            <FileText className="h-6 w-6 text-blue-600" />
            <h2 className="text-xl font-bold text-gray-900">Job Description</h2>
          </div>
          <textarea
            className="w-full h-48 p-4 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all resize-none"
            placeholder="Paste the job description here..."
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
          />
          <button
            onClick={handleAnalyzeJD}
            disabled={loading.jd}
            className="mt-4 w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-6 py-3 rounded-lg hover:from-blue-700 hover:to-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 font-semibold shadow-md transition-all transform hover:scale-[1.02] active:scale-[0.98]"
          >
            {loading.jd ? (
              <>
                <Loader2 className="animate-spin h-5 w-5" />
                <span>Analyzing...</span>
              </>
            ) : (
              <>
                <Sparkles className="h-5 w-5" />
                <span>Analyze Job Description</span>
              </>
            )}
          </button>
          
          {loading.jd && (
            <div className="mt-4">
              <LoadingSkeleton type="analysis" />
            </div>
          )}

          {jdResult && !loading.jd && (
            <div className="mt-4 p-4 bg-green-50 border-2 border-green-200 rounded-lg animate-fadeIn">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <CheckCircle className="h-5 w-5 text-green-600" />
                  <h3 className="font-bold text-green-900">Analysis Complete</h3>
                </div>
                <button
                  onClick={() => copyToClipboard(JSON.stringify(jdResult, null, 2))}
                  className="p-1 hover:bg-green-100 rounded transition-colors"
                  title="Copy results"
                >
                  <Copy className="h-4 w-4 text-green-700" />
                </button>
              </div>
              <p className="text-sm text-green-800">
                <strong>Role:</strong> {jdResult.role || 'Not specified'}
              </p>
            </div>
          )}
        </div>

        {/* Student Profile Section */}
        <div className="bg-white shadow-lg rounded-xl p-6 border-2 border-gray-100">
          <div className="flex items-center gap-2 mb-4">
            <Target className="h-6 w-6 text-green-600" />
            <h2 className="text-xl font-bold text-gray-900">Your Profile</h2>
          </div>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Degree
              </label>
              <input
                type="text"
                className="w-full p-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                placeholder="e.g., B.Tech Computer Science"
                value={profile.degree}
                onChange={(e) => setProfile({ ...profile, degree: e.target.value })}
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Skills (comma-separated)
              </label>
              <input
                type="text"
                className="w-full p-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                placeholder="e.g., Python, JavaScript, React"
                value={profile.skills}
                onChange={(e) => setProfile({ ...profile, skills: e.target.value })}
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Experience Level
              </label>
              <select
                className="w-full p-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                value={profile.experience_level}
                onChange={(e) => setProfile({ ...profile, experience_level: e.target.value })}
              >
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Projects (comma-separated)
              </label>
              <input
                type="text"
                className="w-full p-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                placeholder="e.g., Todo App, E-commerce Site"
                value={profile.projects}
                onChange={(e) => setProfile({ ...profile, projects: e.target.value })}
              />
            </div>
          </div>
          <button
            onClick={handleAnalyzeProfile}
            disabled={loading.profile}
            className="mt-4 w-full bg-gradient-to-r from-green-600 to-emerald-600 text-white px-6 py-3 rounded-lg hover:from-green-700 hover:to-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 font-semibold shadow-md transition-all transform hover:scale-[1.02] active:scale-[0.98]"
          >
            {loading.profile ? (
              <>
                <Loader2 className="animate-spin h-5 w-5" />
                <span>Analyzing...</span>
              </>
            ) : (
              <>
                <Target className="h-5 w-5" />
                <span>Analyze Profile</span>
              </>
            )}
          </button>

          {loading.profile && (
            <div className="mt-4">
              <LoadingSkeleton type="analysis" />
            </div>
          )}

          {profileResult && !loading.profile && (
            <div className="mt-4 p-4 bg-blue-50 border-2 border-blue-200 rounded-lg animate-fadeIn">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <CheckCircle className="h-5 w-5 text-blue-600" />
                  <h3 className="font-bold text-blue-900">Profile Analyzed</h3>
                </div>
                <button
                  onClick={() => copyToClipboard(JSON.stringify(profileResult, null, 2))}
                  className="p-1 hover:bg-blue-100 rounded transition-colors"
                  title="Copy results"
                >
                  <Copy className="h-4 w-4 text-blue-700" />
                </button>
              </div>
              <p className="text-sm text-blue-800">
                <strong>Level:</strong> {profileResult.experience_level || 'Not specified'}
              </p>
            </div>
          )}
        </div>
      </div>

      {/* AI Analysis Results */}
      {jdResult && (
        <AIResponsePanel 
          title="Job Requirements Analysis" 
          icon={FileText}
          type="premium"
        >
          <div className="space-y-4">
            <div className="bg-white rounded-lg p-4 border-2 border-blue-200">
              <h3 className="text-lg font-bold text-gray-900 mb-3 flex items-center gap-2">
                <Award className="h-5 w-5 text-blue-600" />
                Role: {jdResult.role || 'Not specified'}
              </h3>
              <div className="flex items-center gap-2 mb-3">
                <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                  {jdResult.experience_level || 'Not specified'} Level
                </span>
                {jdResult.required_skills && (
                  <span className="px-3 py-1 bg-gray-100 text-gray-800 rounded-full text-sm font-medium">
                    {jdResult.required_skills.length} Required Skills
                  </span>
                )}
              </div>
            </div>

            {jdResult.required_skills && jdResult.required_skills.length > 0 && (
              <div>
                <h4 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                  <Target className="h-5 w-5 text-red-600" />
                  Required Skills
                </h4>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                  {jdResult.required_skills.map((skill, idx) => {
                    const Icon = getSkillIcon(skill)
                    return (
                      <div key={idx} className="flex items-center gap-2 p-3 bg-white rounded-lg border-2 border-gray-200">
                        <Icon className="h-4 w-4 text-gray-600 flex-shrink-0" />
                        <span className="text-sm font-medium text-gray-900">{skill}</span>
                      </div>
                    )
                  })}
                </div>
              </div>
            )}

            {jdResult.preferred_skills && jdResult.preferred_skills.length > 0 && (
              <AccordionSection title="Preferred Skills (Optional)">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                  {jdResult.preferred_skills.map((skill, idx) => {
                    const Icon = getSkillIcon(skill)
                    return (
                      <div key={idx} className="flex items-center gap-2 p-3 bg-gray-50 rounded-lg border border-gray-200">
                        <Icon className="h-4 w-4 text-gray-500 flex-shrink-0" />
                        <span className="text-sm text-gray-700">{skill}</span>
                      </div>
                    )
                  })}
                </div>
              </AccordionSection>
            )}

            {jdResult.reasoning && (
              <AccordionSection title="AI Reasoning">
                <p className="text-sm text-gray-700 leading-relaxed">{jdResult.reasoning}</p>
              </AccordionSection>
            )}
          </div>
        </AIResponsePanel>
      )}

      {profileResult && (
        <AIResponsePanel 
          title="Your Profile Analysis" 
          icon={Target}
          type="success"
        >
          <div className="space-y-4">
            {profileResult.normalized_skills && (
              <div className="space-y-4">
                {Object.entries(profileResult.normalized_skills).map(([category, skills]) => {
                  if (!skills || skills.length === 0) return null
                  const categoryIcons = {
                    programming_languages: Code,
                    frameworks: Code,
                    tools: Wrench,
                    databases: Database,
                    soft_skills: Lightbulb,
                    domain_knowledge: BookOpen
                  }
                  const Icon = categoryIcons[category] || BookOpen
                  
                  return (
                    <div key={category} className="bg-white rounded-lg p-4 border-2 border-gray-200">
                      <h4 className="font-semibold text-gray-900 mb-3 flex items-center gap-2 capitalize">
                        <Icon className="h-5 w-5 text-green-600" />
                        {category.replace(/_/g, ' ')}
                      </h4>
                      <div className="flex flex-wrap gap-2">
                        {skills.map((skill, idx) => (
                          <span 
                            key={idx}
                            className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium border border-green-300"
                          >
                            {skill}
                          </span>
                        ))}
                      </div>
                    </div>
                  )
                })}
              </div>
            )}

            {profileResult.strengths && profileResult.strengths.length > 0 && (
              <div>
                <h4 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                  <Award className="h-5 w-5 text-yellow-600" />
                  Your Strengths
                </h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {profileResult.strengths.map((strength, idx) => (
                    <InsightCard
                      key={idx}
                      icon={CheckCircle}
                      title={strength}
                      type="success"
                    />
                  ))}
                </div>
              </div>
            )}

            {profileResult.skill_summary && (
              <InsightCard
                icon={Lightbulb}
                title="Skill Summary"
                content={profileResult.skill_summary}
                type="info"
              />
            )}

            {profileResult.reasoning && (
              <AccordionSection title="AI Analysis Explanation">
                <p className="text-sm text-gray-700 leading-relaxed">{profileResult.reasoning}</p>
              </AccordionSection>
            )}
          </div>
        </AIResponsePanel>
      )}

      {/* Skill Gap Analysis */}
      {jdResult && profileResult && (
        <div className="mt-6 bg-white shadow-lg rounded-xl p-6 border-2 border-gray-100">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
                <TrendingUp className="h-7 w-7 text-purple-600" />
                Skill Gap Analysis
              </h2>
              <p className="text-gray-600 mt-1">See how your skills match the job requirements</p>
            </div>
            <button
              onClick={handleAnalyzeSkillGap}
              disabled={loading.gap}
              className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-6 py-3 rounded-lg hover:from-purple-700 hover:to-pink-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 font-semibold shadow-md transition-all transform hover:scale-[1.02] active:scale-[0.98]"
            >
              {loading.gap ? (
                <>
                  <Loader2 className="animate-spin h-5 w-5" />
                  <span>Analyzing...</span>
                </>
              ) : (
                <>
                  <RefreshCw className="h-5 w-5" />
                  <span>Analyze Skill Gaps</span>
                </>
              )}
            </button>
          </div>

          {loading.gap && (
            <div className="mb-6">
              <LoadingSkeleton type="analysis" />
            </div>
          )}

          {skillGapResult && !loading.gap && (
            <div className="space-y-6 animate-fadeIn">
              {/* Match Score */}
              <MatchScore 
                score={calculateMatchScore()} 
                label="Overall Skill Match"
                size="lg"
              />

              {/* Chart */}
              {skillGapResult && (
                <div className="bg-gray-50 rounded-lg p-4 border-2 border-gray-200">
                  <SkillGapChart data={skillGapResult} />
                </div>
              )}

              {/* Skills Breakdown */}
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
                {/* Missing Skills */}
                <div className="space-y-3">
                  <div className="flex items-center gap-2 mb-3">
                    <AlertTriangle className="h-6 w-6 text-red-600" />
                    <h3 className="text-lg font-bold text-gray-900">
                      Missing Skills
                    </h3>
                    <span className="px-2 py-1 bg-red-100 text-red-800 rounded-full text-xs font-bold">
                      {skillGapResult.missing_skills?.length || 0}
                    </span>
                  </div>
                  <div className="space-y-2">
                    {skillGapResult.missing_skills?.slice(0, 8).map((item, idx) => (
                      <SkillCard
                        key={idx}
                        skill={item.skill || item}
                        level="missing"
                        importance={item.importance}
                        explanation={item.explanation}
                      />
                    ))}
                  </div>
                </div>

                {/* Partial Skills */}
                <div className="space-y-3">
                  <div className="flex items-center gap-2 mb-3">
                    <AlertCircle className="h-6 w-6 text-yellow-600" />
                    <h3 className="text-lg font-bold text-gray-900">
                      Needs Improvement
                    </h3>
                    <span className="px-2 py-1 bg-yellow-100 text-yellow-800 rounded-full text-xs font-bold">
                      {skillGapResult.partial_skills?.length || 0}
                    </span>
                  </div>
                  <div className="space-y-2">
                    {skillGapResult.partial_skills?.slice(0, 8).map((item, idx) => (
                      <SkillCard
                        key={idx}
                        skill={item.skill || item}
                        level="partial"
                        importance={item.importance}
                        explanation={item.explanation}
                      />
                    ))}
                  </div>
                </div>

                {/* Strong Skills */}
                <div className="space-y-3">
                  <div className="flex items-center gap-2 mb-3">
                    <CheckCircle className="h-6 w-6 text-green-600" />
                    <h3 className="text-lg font-bold text-gray-900">
                      Strong Skills
                    </h3>
                    <span className="px-2 py-1 bg-green-100 text-green-800 rounded-full text-xs font-bold">
                      {skillGapResult.strong_skills?.length || 0}
                    </span>
                  </div>
                  <div className="space-y-2">
                    {skillGapResult.strong_skills?.slice(0, 8).map((item, idx) => (
                      <SkillCard
                        key={idx}
                        skill={item.skill || item}
                        level="strong"
                        importance={item.importance}
                        explanation={item.explanation}
                      />
                    ))}
                  </div>
                </div>
              </div>

              {/* AI Recommendations */}
              {skillGapResult.recommendations && skillGapResult.recommendations.length > 0 && (
                <div>
                  <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
                    <Lightbulb className="h-6 w-6 text-purple-600" />
                    AI Recommendations
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {skillGapResult.recommendations.map((rec, idx) => (
                      <InsightCard
                        key={idx}
                        icon={Lightbulb}
                        title={rec.title || `Recommendation ${idx + 1}`}
                        content={rec.description || rec}
                        type="tip"
                      />
                    ))}
                  </div>
                </div>
              )}

              {/* AI Reasoning */}
              {skillGapResult.reasoning && (
                <AccordionSection title="🧠 AI Analysis Explanation" defaultOpen={false}>
                  <div className="prose prose-sm max-w-none">
                    <p className="text-gray-700 leading-relaxed whitespace-pre-line">
                      {skillGapResult.reasoning}
                    </p>
                  </div>
                </AccordionSection>
              )}

              {/* Next Steps */}
              <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg p-6 border-2 border-purple-200">
                <h3 className="text-lg font-bold text-gray-900 mb-3 flex items-center gap-2">
                  <Target className="h-6 w-6 text-purple-600" />
                  Next Steps
                </h3>
                <ul className="space-y-2 text-gray-700">
                  <li className="flex items-start gap-2">
                    <CheckCircle className="h-5 w-5 text-green-600 flex-shrink-0 mt-0.5" />
                    <span>Focus on learning the missing skills identified above</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="h-5 w-5 text-green-600 flex-shrink-0 mt-0.5" />
                    <span>Improve your partial skills through practice and projects</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="h-5 w-5 text-green-600 flex-shrink-0 mt-0.5" />
                    <span>Check the Roadmap page for a personalized learning plan</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="h-5 w-5 text-green-600 flex-shrink-0 mt-0.5" />
                    <span>Use the Practice page for hands-on exercises</span>
                  </li>
                </ul>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default Analysis
