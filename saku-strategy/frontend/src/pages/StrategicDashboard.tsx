import React from 'react'
import { useQuery } from 'react-query'
import { 
  Target, 
  Users, 
  AlertTriangle, 
  CheckCircle, 
  TrendingUp,
  BarChart3,
  UserPlus,
  Shield,
  Award
} from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { apiClient } from '../services/api'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorMessage from '../components/ErrorMessage'

interface DepartmentData {
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

interface MetricsData {
  departments: DepartmentData[]
  score: {
    score: number
    components: {
      min_gap_sum: number
      gender_gap_sum: number
      buffer_sum: number
      weights: Record<string, number>
    }
  }
}

const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4', '#84CC16', '#F97316']

export default function StrategicDashboard() {
  const { data, isLoading, error, refetch } = useQuery<MetricsData>(
    'strategic-dashboard',
    () => apiClient.get('/delegates/metrics/').then(res => res.data),
    {
      refetchInterval: 30000,
    }
  )

  if (isLoading) {
    return <LoadingSpinner />
  }

  if (error) {
    return <ErrorMessage error={error} onRetry={refetch} />
  }

  if (!data) {
    return <ErrorMessage error={new Error('No data available')} onRetry={refetch} />
  }

  const { departments, score } = data
  const totalCandidates = departments.reduce((sum, dept) => sum + dept.total_candidates, 0)
  const totalQualified = departments.reduce((sum, dept) => sum + dept.qualified, 0)
  const totalTarget = departments.reduce((sum, dept) => sum + dept.target_min, 0)
  const departmentsUnderMin = departments.filter(dept => dept.gap_to_min > 0).length
  const departmentsWithGenderGap = departments.filter(dept => dept.gender_gap > 0.05).length
  const departmentsFullyCompliant = departments.filter(dept => dept.gap_to_min === 0 && dept.gender_gap <= 0.05).length

  // Strategic Analysis
  const criticalDepartments = departments.filter(dept => dept.gap_to_min >= 2)
  const atRiskDepartments = departments.filter(dept => dept.gap_to_min === 1)
  const strongDepartments = departments.filter(dept => dept.gap_to_min === 0 && dept.qualified >= dept.target_min)

  // Prepare chart data
  const departmentChartData = departments.map(dept => ({
    name: dept.department,
    qualified: dept.qualified,
    target: dept.target_min,
    gap: dept.gap_to_min,
    status: dept.gap_to_min === 0 ? 'Compliant' : dept.gap_to_min === 1 ? 'At Risk' : 'Critical'
  }))

  const genderChartData = departments.map(dept => ({
    name: dept.department,
    male: dept.male,
    female: dept.female,
    total: dept.male + dept.female
  }))

  const getVictoryStatus = (score: number) => {
    if (score >= 85) return { status: 'Excellent', color: 'text-green-600', bg: 'bg-green-50', border: 'border-green-200' }
    if (score >= 70) return { status: 'Good', color: 'text-yellow-600', bg: 'bg-yellow-50', border: 'border-yellow-200' }
    if (score >= 50) return { status: 'Fair', color: 'text-orange-600', bg: 'bg-orange-50', border: 'border-orange-200' }
    return { status: 'Critical', color: 'text-red-600', bg: 'bg-red-50', border: 'border-red-200' }
  }

  const victoryStatus = getVictoryStatus(score.score)

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">SAKU Election Strategy Dashboard</h1>
          <p className="mt-2 text-gray-600">Strategic analysis for guaranteed election victory</p>
        </div>
        <div className="flex space-x-3">
          <button
            onClick={() => refetch()}
            className="btn btn-secondary"
          >
            Refresh Data
          </button>
          <a
            href="/register"
            className="btn btn-primary"
          >
            <UserPlus className="w-4 h-4 mr-2" />
            Register Delegate
          </a>
        </div>
      </div>

      {/* Victory Status */}
      <div className={`${victoryStatus.bg} ${victoryStatus.border} border-2 rounded-lg p-6`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <Award className={`w-8 h-8 ${victoryStatus.color} mr-4`} />
            <div>
              <h2 className={`text-2xl font-bold ${victoryStatus.color}`}>
                Victory Score: {score.score.toFixed(1)}/100
              </h2>
              <p className={`text-lg ${victoryStatus.color}`}>
                Status: {victoryStatus.status}
              </p>
            </div>
          </div>
          <div className="text-right">
            <p className="text-sm text-gray-600">Election Readiness</p>
            <div className="w-32 bg-gray-200 rounded-full h-3 mt-2">
              <div 
                className={`h-3 rounded-full ${score.score >= 85 ? 'bg-green-500' : score.score >= 70 ? 'bg-yellow-500' : score.score >= 50 ? 'bg-orange-500' : 'bg-red-500'}`}
                style={{ width: `${score.score}%` }}
              ></div>
            </div>
          </div>
        </div>
      </div>

      {/* Strategic Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                <Target className="w-5 h-5 text-blue-600" />
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Total Delegates</p>
              <p className="text-2xl font-bold text-gray-900">{totalQualified}</p>
              <p className="text-sm text-gray-600">of {totalTarget} target</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                <CheckCircle className="w-5 h-5 text-green-600" />
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Compliant Departments</p>
              <p className="text-2xl font-bold text-gray-900">{departmentsFullyCompliant}</p>
              <p className="text-sm text-gray-600">of {departments.length} total</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-red-100 rounded-lg flex items-center justify-center">
                <AlertTriangle className="w-5 h-5 text-red-600" />
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Critical Departments</p>
              <p className="text-2xl font-bold text-gray-900">{criticalDepartments.length}</p>
              <p className="text-sm text-gray-600">Need immediate attention</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-yellow-100 rounded-lg flex items-center justify-center">
                <TrendingUp className="w-5 h-5 text-yellow-600" />
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">At Risk Departments</p>
              <p className="text-2xl font-bold text-gray-900">{atRiskDepartments.length}</p>
              <p className="text-sm text-gray-600">Need 1 more delegate</p>
            </div>
          </div>
        </div>
      </div>

      {/* Strategic Analysis */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Department Status Chart */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Department Compliance Status</h3>
            <BarChart3 className="w-5 h-5 text-gray-400" />
          </div>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={departmentChartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="name" 
                  angle={-45}
                  textAnchor="end"
                  height={100}
                  fontSize={12}
                />
                <YAxis />
                <Tooltip />
                <Bar dataKey="qualified" fill="#10B981" name="Qualified" />
                <Bar dataKey="target" fill="#3B82F6" name="Target" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Gender Distribution */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Gender Distribution</h3>
            <Users className="w-5 h-5 text-gray-400" />
          </div>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={genderChartData}
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  dataKey="total"
                  nameKey="name"
                >
                  {genderChartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Strategic Recommendations */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Strategic Recommendations</h3>
        
        {criticalDepartments.length > 0 && (
          <div className="mb-4">
            <h4 className="text-md font-medium text-red-800 mb-2">🚨 Critical Action Required</h4>
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-sm text-red-800 mb-2">
                These departments need immediate attention (2+ delegates short):
              </p>
              <ul className="list-disc list-inside text-sm text-red-700">
                {criticalDepartments.map(dept => (
                  <li key={dept.code}>
                    {dept.department}: Need {dept.gap_to_min} more delegates
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}

        {atRiskDepartments.length > 0 && (
          <div className="mb-4">
            <h4 className="text-md font-medium text-yellow-800 mb-2">⚠️ At Risk Departments</h4>
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <p className="text-sm text-yellow-800 mb-2">
                These departments need 1 more delegate to be compliant:
              </p>
              <ul className="list-disc list-inside text-sm text-yellow-700">
                {atRiskDepartments.map(dept => (
                  <li key={dept.code}>
                    {dept.department}: Need 1 more delegate
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}

        {departmentsWithGenderGap > 0 && (
          <div className="mb-4">
            <h4 className="text-md font-medium text-purple-800 mb-2">⚖️ Gender Balance Issues</h4>
            <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
              <p className="text-sm text-purple-800">
                {departmentsWithGenderGap} departments have gender balance issues. 
                Focus on recruiting more {departments.filter(dept => dept.gender_ratio_female < 0.33).length > 0 ? 'female' : 'male'} delegates.
              </p>
            </div>
          </div>
        )}

        {departmentsFullyCompliant === departments.length && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <div className="flex items-center">
              <CheckCircle className="w-5 h-5 text-green-600 mr-2" />
              <p className="text-sm text-green-800 font-medium">
                🎉 Excellent! All departments are compliant. You're on track for victory!
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Department Status Table */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Department Status Overview</h3>
          <div className="flex space-x-2">
            <span className="badge badge-success">✅ Compliant</span>
            <span className="badge badge-warning">⚠️ At Risk</span>
            <span className="badge badge-danger">🚨 Critical</span>
          </div>
        </div>
        
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Department
                </th>
                <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Qualified / Target
                </th>
                <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Gap
                </th>
                <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Male
                </th>
                <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Female
                </th>
                <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Gender Gap
                </th>
                <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {departments.map((dept) => {
                const isCritical = dept.gap_to_min >= 2
                const isAtRisk = dept.gap_to_min === 1
                const isCompliant = dept.gap_to_min === 0
                const hasGenderGap = dept.gender_gap > 0.05
                
                let statusClass = 'bg-green-50'
                let statusText = '✅ Compliant'
                let statusBadge = 'badge-success'
                
                if (isCritical) {
                  statusClass = 'bg-red-50'
                  statusText = '🚨 Critical'
                  statusBadge = 'badge-danger'
                } else if (isAtRisk) {
                  statusClass = 'bg-yellow-50'
                  statusText = '⚠️ At Risk'
                  statusBadge = 'badge-warning'
                }
                
                return (
                  <tr key={dept.code} className={statusClass}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="font-medium text-gray-900">{dept.department}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center">
                      <div className="text-sm text-gray-900">
                        {dept.qualified} / {dept.target_min}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center">
                      <div className="text-sm text-gray-900">
                        {dept.gap_to_min > 0 ? (
                          <span className="text-red-600 font-medium">-{dept.gap_to_min}</span>
                        ) : (
                          <span className="text-green-600">✓</span>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-gray-900">
                      {dept.male}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-gray-900">
                      {dept.female}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-gray-900">
                      {dept.gender_gap.toFixed(2)}
                      {hasGenderGap && <span className="text-orange-600 ml-1">⚠️</span>}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center">
                      <span className={statusBadge}>{statusText}</span>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

