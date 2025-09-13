import React from 'react'
import { useQuery } from 'react-query'
import { 
  TrendingUp, 
  Users, 
  Target, 
  AlertTriangle, 
  CheckCircle, 
  XCircle,
  BarChart3,
  PieChart
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

const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6']

export default function Dashboard() {
  const { data, isLoading, error, refetch } = useQuery<MetricsData>(
    'dashboard-metrics',
    () => apiClient.get('/delegates/metrics/').then(res => res.data),
    {
      refetchInterval: 30000, // Refetch every 30 seconds
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

  // Prepare chart data
  const departmentChartData = departments.map(dept => ({
    name: dept.department,
    qualified: dept.qualified,
    target: dept.target_min,
    gap: dept.gap_to_min
  }))

  const genderChartData = departments.map(dept => ({
    name: dept.department,
    male: dept.male,
    female: dept.female
  }))

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getScoreStatus = (score: number) => {
    if (score >= 80) return 'Excellent'
    if (score >= 60) return 'Good'
    return 'Needs Improvement'
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">SAKU Delegate Management Dashboard</h1>
          <p className="mt-2 text-gray-600">Track delegate registrations, analyze performance, and monitor election readiness</p>
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
            Register New Delegate
          </a>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                <TrendingUp className="w-5 h-5 text-blue-600" />
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Win Score</p>
              <p className={`text-2xl font-bold ${getScoreColor(score.score)}`}>
                {score.score.toFixed(1)}/100
              </p>
              <p className="text-sm text-gray-600">{getScoreStatus(score.score)}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                <Users className="w-5 h-5 text-green-600" />
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Total Qualified</p>
              <p className="text-2xl font-bold text-gray-900">{totalQualified}</p>
              <p className="text-sm text-gray-600">of {totalTarget} target</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-yellow-100 rounded-lg flex items-center justify-center">
                <Target className="w-5 h-5 text-yellow-600" />
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Departments Under Min</p>
              <p className="text-2xl font-bold text-gray-900">{departmentsUnderMin}</p>
              <p className="text-sm text-gray-600">of {departments.length} total</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                <AlertTriangle className="w-5 h-5 text-purple-600" />
              </div>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Gender Gap Issues</p>
              <p className="text-2xl font-bold text-gray-900">{departmentsWithGenderGap}</p>
              <p className="text-sm text-gray-600">departments affected</p>
            </div>
          </div>
        </div>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Department Progress Chart */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Department Progress</h3>
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

        {/* Gender Distribution Chart */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Gender Distribution</h3>
            <PieChart className="w-5 h-5 text-gray-400" />
          </div>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={genderChartData}
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  dataKey="male"
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

      {/* Department Status Table */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Department Status</h3>
          <div className="flex space-x-2">
            <span className="badge badge-success">✅ Good</span>
            <span className="badge badge-warning">⚠️ Gender Gap</span>
            <span className="badge badge-danger">❌ Under Min</span>
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
                  Total
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
                const isUnderMin = dept.gap_to_min > 0
                const hasGenderGap = dept.gender_gap > 0.05
                const statusClass = isUnderMin ? 'bg-red-50' : hasGenderGap ? 'bg-yellow-50' : 'bg-green-50'
                
                return (
                  <tr key={dept.code} className={statusClass}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="font-medium text-gray-900">{dept.department}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center">
                      <div className="text-sm text-gray-900">
                        {dept.qualified} / {dept.target_min}
                        {isUnderMin && (
                          <span className="text-red-600 font-medium"> (-{dept.gap_to_min})</span>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-gray-900">
                      {dept.total_candidates}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-gray-900">
                      {dept.male}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-gray-900">
                      {dept.female}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-gray-900">
                      {dept.gender_gap.toFixed(2)}
                      {hasGenderGap && <span className="text-yellow-600 ml-1">⚠️</span>}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center">
                      {isUnderMin ? (
                        <span className="badge badge-danger">❌ Under Min</span>
                      ) : hasGenderGap ? (
                        <span className="badge badge-warning">⚠️ Gender Gap</span>
                      ) : (
                        <span className="badge badge-success">✅ Good</span>
                      )}
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
