import React, { useEffect, useState } from 'react'

// Simple fetch function instead of axios to avoid dependency issues
const apiCall = async (url: string) => {
  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    return await response.json()
  } catch (error) {
    console.error('API call failed:', error)
    throw error
  }
}

interface Dept {
  department: string
  code: string
  total_candidates: number
  qualified: number
  target_min: number
  gap_to_min: number
  male: number
  female: number
  gender_ratio_female: number
  gender_target_female: number
  gender_gap: number
}

interface ScoreData {
  score: number
  components: {
    min_gap_sum: number
    gender_gap_sum: number
    buffer_sum: number
    weights: Record<string, number>
  }
}

export default function App() {
  const [data, setData] = useState<Dept[]>([])
  const [score, setScore] = useState<number>(0)
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string>('')

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        setError('')
        const response = await apiCall('/api/delegates/metrics/')
        setData(response.departments || [])
        setScore(response.score?.score || 0)
      } catch (err) {
        console.error('Error fetching data:', err)
        setError('Failed to load data. Make sure the backend is running on http://localhost:8000')
        setData([])
        setScore(0)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  if (loading) {
    return (
      <div style={{ padding: 20, textAlign: 'center' }}>
        <h1>SAKU Strategy Dashboard</h1>
        <p>Loading...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div style={{ padding: 20, textAlign: 'center' }}>
        <h1>SAKU Strategy Dashboard</h1>
        <div style={{ color: 'red', margin: '20px 0' }}>
          <p>{error}</p>
          <p>Please ensure the backend server is running on http://localhost:8000</p>
        </div>
      </div>
    )
  }

  return (
    <div style={{ padding: 20, fontFamily: 'system-ui, sans-serif' }}>
      <h1>SAKU Strategy Dashboard</h1>
      <div style={{ 
        background: score >= 80 ? '#d4edda' : score >= 60 ? '#fff3cd' : '#f8d7da',
        padding: '10px',
        borderRadius: '5px',
        marginBottom: '20px',
        border: `1px solid ${score >= 80 ? '#c3e6cb' : score >= 60 ? '#ffeaa7' : '#f5c6cb'}`
      }}>
        <strong>Win Score: {score.toFixed(1)}/100</strong>
        {score >= 80 && <span style={{ color: 'green' }}> ✅ Excellent</span>}
        {score >= 60 && score < 80 && <span style={{ color: 'orange' }}> ⚠️ Good</span>}
        {score < 60 && <span style={{ color: 'red' }}> ❌ Needs Improvement</span>}
      </div>
      
      {data.length === 0 ? (
        <p>No department data available. Add some delegates to see metrics.</p>
      ) : (
        <div style={{ overflowX: 'auto' }}>
          <table style={{ 
            borderCollapse: 'collapse', 
            width: '100%',
            border: '1px solid #ddd'
          }}>
            <thead>
              <tr style={{ background: '#f8f9fa' }}>
                <th style={{ padding: '12px', border: '1px solid #ddd', textAlign: 'left' }}>Department</th>
                <th style={{ padding: '12px', border: '1px solid #ddd', textAlign: 'center' }}>Qualified / Target</th>
                <th style={{ padding: '12px', border: '1px solid #ddd', textAlign: 'center' }}>Total</th>
                <th style={{ padding: '12px', border: '1px solid #ddd', textAlign: 'center' }}>Male</th>
                <th style={{ padding: '12px', border: '1px solid #ddd', textAlign: 'center' }}>Female</th>
                <th style={{ padding: '12px', border: '1px solid #ddd', textAlign: 'center' }}>Gender Gap</th>
                <th style={{ padding: '12px', border: '1px solid #ddd', textAlign: 'center' }}>Status</th>
              </tr>
            </thead>
            <tbody>
              {data.map(d => {
                const isUnderMin = d.gap_to_min > 0
                const hasGenderGap = d.gender_gap > 0.05
                const status = isUnderMin ? '❌ Under Min' : hasGenderGap ? '⚠️ Gender Gap' : '✅ Good'
                
                return (
                  <tr key={d.code} style={{ background: isUnderMin ? '#f8d7da' : hasGenderGap ? '#fff3cd' : '#d4edda' }}>
                    <td style={{ padding: '12px', border: '1px solid #ddd', fontWeight: 'bold' }}>{d.department}</td>
                    <td style={{ padding: '12px', border: '1px solid #ddd', textAlign: 'center' }}>
                      {d.qualified} / {d.target_min} 
                      {isUnderMin && <span style={{ color: 'red' }}> (-{d.gap_to_min})</span>}
                    </td>
                    <td style={{ padding: '12px', border: '1px solid #ddd', textAlign: 'center' }}>{d.total_candidates}</td>
                    <td style={{ padding: '12px', border: '1px solid #ddd', textAlign: 'center' }}>{d.male}</td>
                    <td style={{ padding: '12px', border: '1px solid #ddd', textAlign: 'center' }}>{d.female}</td>
                    <td style={{ padding: '12px', border: '1px solid #ddd', textAlign: 'center' }}>
                      {d.gender_gap.toFixed(2)}
                      {hasGenderGap && <span style={{ color: 'orange' }}> ⚠️</span>}
                    </td>
                    <td style={{ padding: '12px', border: '1px solid #ddd', textAlign: 'center' }}>{status}</td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      )}
      
      <div style={{ marginTop: '20px', fontSize: '14px', color: '#666' }}>
        <p><strong>Legend:</strong></p>
        <p>✅ Good: Meets minimum requirements and gender balance</p>
        <p>⚠️ Gender Gap: Meets minimum but has gender imbalance</p>
        <p>❌ Under Min: Below minimum delegate requirements</p>
      </div>
    </div>
  )
}


