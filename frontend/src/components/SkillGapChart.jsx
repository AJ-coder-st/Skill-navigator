import React from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

function SkillGapChart({ data }) {
  const chartData = [
    {
      category: 'Missing',
      count: data.missing_skills?.length || 0,
      fill: '#ef4444'
    },
    {
      category: 'Partial',
      count: data.partial_skills?.length || 0,
      fill: '#eab308'
    },
    {
      category: 'Strong',
      count: data.strong_skills?.length || 0,
      fill: '#22c55e'
    }
  ]

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
