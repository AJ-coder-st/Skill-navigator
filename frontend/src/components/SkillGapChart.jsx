import React from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

function SkillGapChart({ data }) {
  if (!data) {
    return (
      <div className="w-full h-64 flex items-center justify-center text-gray-500">
        No data available
      </div>
    )
  }

  const missingCount = Array.isArray(data.missing_skills) ? data.missing_skills.length : 0
  const partialCount = Array.isArray(data.partial_skills) ? data.partial_skills.length : 0
  const strongCount = Array.isArray(data.strong_skills) ? data.strong_skills.length : 0

  const chartData = [
    {
      category: 'Missing',
      count: missingCount,
      fill: '#ef4444'
    },
    {
      category: 'Partial',
      count: partialCount,
      fill: '#eab308'
    },
    {
      category: 'Strong',
      count: strongCount,
      fill: '#22c55e'
    }
  ]

  // Don't render if all counts are zero
  if (missingCount === 0 && partialCount === 0 && strongCount === 0) {
    return (
      <div className="w-full h-64 flex items-center justify-center text-gray-500">
        No skill data to display
      </div>
    )
  }

  return (
    <div className="w-full h-64">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="category" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="count" fill="#8884d8" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

export default SkillGapChart
