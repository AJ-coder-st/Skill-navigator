import React, { useEffect, useRef } from 'react'
import { 
  Sparkles, CheckCircle, AlertTriangle, TrendingUp, 
  Target, Lightbulb, Copy, ChevronDown, ChevronUp
} from 'lucide-react'

function AIResponsePanel({ title, icon: Icon = Sparkles, children, type = 'default' }) {
  const panelRef = useRef(null)

  useEffect(() => {
    if (panelRef.current) {
      panelRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  }, [])

  const typeStyles = {
    default: 'border-blue-200 bg-gradient-to-br from-blue-50 to-indigo-50',
    success: 'border-green-200 bg-gradient-to-br from-green-50 to-emerald-50',
    warning: 'border-yellow-200 bg-gradient-to-br from-yellow-50 to-amber-50',
    error: 'border-red-200 bg-gradient-to-br from-red-50 to-rose-50',
    premium: 'border-purple-200 bg-gradient-to-br from-purple-50 via-indigo-50 to-blue-50 shadow-xl'
  }

  return (
    <div 
      ref={panelRef}
      className={`mt-6 rounded-xl border-2 ${typeStyles[type]} p-6 animate-fadeIn shadow-lg`}
    >
      <div className="flex items-center gap-3 mb-4">
        <div className="p-2 bg-white rounded-lg shadow-sm">
          <Icon className="h-6 w-6 text-blue-600" />
        </div>
        <h2 className="text-2xl font-bold text-gray-900">{title}</h2>
        <div className="ml-auto flex items-center gap-2">
          <span className="px-3 py-1 bg-white/80 rounded-full text-xs font-semibold text-blue-700 border border-blue-200">
            AI Analysis
          </span>
        </div>
      </div>
      <div className="mt-4">
        {children}
      </div>
    </div>
  )
}

export function SkillCard({ skill, level, category, importance, explanation }) {
  const levelColors = {
    strong: 'bg-green-100 text-green-800 border-green-300',
    partial: 'bg-yellow-100 text-yellow-800 border-yellow-300',
    missing: 'bg-red-100 text-red-800 border-red-300'
  }

  const levelIcons = {
    strong: CheckCircle,
    partial: AlertTriangle,
    missing: Target
  }

  const Icon = levelIcons[level] || Target

  return (
    <div className={`p-4 rounded-lg border-2 ${levelColors[level]} transition-all hover:shadow-md`}>
      <div className="flex items-start justify-between mb-2">
        <div className="flex items-center gap-2">
          <Icon className="h-5 w-5" />
          <h4 className="font-semibold text-lg">{skill}</h4>
        </div>
        {importance && (
          <span className="px-2 py-1 bg-white/60 rounded text-xs font-medium">
            {importance}
          </span>
        )}
      </div>
      {category && (
        <span className="inline-block px-2 py-1 bg-white/60 rounded text-xs mb-2">
          {category}
        </span>
      )}
      {explanation && (
        <p className="text-sm mt-2 opacity-90">{explanation}</p>
      )}
    </div>
  )
}

export function MatchScore({ score, label, size = 'lg' }) {
  const percentage = Math.round(score * 100)
  const colorClass = percentage >= 70 ? 'bg-green-500' : percentage >= 40 ? 'bg-yellow-500' : 'bg-red-500'
  
  const sizeClasses = {
    sm: 'h-2',
    md: 'h-3',
    lg: 'h-4'
  }

  return (
    <div className="bg-white rounded-lg p-4 border-2 border-gray-200 shadow-sm">
      <div className="flex items-center justify-between mb-2">
        <span className="font-medium text-gray-700">{label}</span>
        <span className="text-2xl font-bold text-gray-900">{percentage}%</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full overflow-hidden">
        <div 
          className={`${colorClass} ${sizeClasses[size]} rounded-full transition-all duration-500 ease-out`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  )
}

export function InsightCard({ icon: Icon, title, content, type = 'info' }) {
  const typeStyles = {
    info: 'bg-blue-50 border-blue-200 text-blue-900',
    success: 'bg-green-50 border-green-200 text-green-900',
    warning: 'bg-yellow-50 border-yellow-200 text-yellow-900',
    tip: 'bg-purple-50 border-purple-200 text-purple-900'
  }

  return (
    <div className={`p-4 rounded-lg border-2 ${typeStyles[type]} flex gap-3`}>
      <div className="flex-shrink-0">
        <Icon className="h-6 w-6" />
      </div>
      <div className="flex-1">
        <h4 className="font-semibold mb-1">{title}</h4>
        <p className="text-sm">{content}</p>
      </div>
    </div>
  )
}

export function AccordionSection({ title, children, defaultOpen = false }) {
  const [isOpen, setIsOpen] = React.useState(defaultOpen)

  return (
    <div className="border-2 border-gray-200 rounded-lg overflow-hidden bg-white">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full px-4 py-3 flex items-center justify-between bg-gray-50 hover:bg-gray-100 transition-colors"
      >
        <span className="font-semibold text-gray-900">{title}</span>
        {isOpen ? (
          <ChevronUp className="h-5 w-5 text-gray-600" />
        ) : (
          <ChevronDown className="h-5 w-5 text-gray-600" />
        )}
      </button>
      {isOpen && (
        <div className="p-4 border-t border-gray-200 animate-fadeIn">
          {children}
        </div>
      )}
    </div>
  )
}

export function LoadingSkeleton({ type = 'default' }) {
  if (type === 'analysis') {
    return (
      <div className="space-y-4 animate-pulse">
        <div className="h-8 bg-gray-200 rounded w-1/3"></div>
        <div className="h-4 bg-gray-200 rounded w-full"></div>
        <div className="h-4 bg-gray-200 rounded w-5/6"></div>
        <div className="grid grid-cols-3 gap-4 mt-6">
          {[1, 2, 3].map(i => (
            <div key={i} className="h-24 bg-gray-200 rounded"></div>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-3 animate-pulse">
      <div className="h-4 bg-gray-200 rounded w-3/4"></div>
      <div className="h-4 bg-gray-200 rounded w-full"></div>
      <div className="h-4 bg-gray-200 rounded w-5/6"></div>
    </div>
  )
}

export default AIResponsePanel
