import React, { useState } from 'react'
import { useQuery } from 'react-query'
import { Download, FileText, BarChart3, Users, Calendar } from 'lucide-react'
import { api } from '../services/api'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorMessage from '../components/ErrorMessage'

export default function Reports() {
  const [selectedReport, setSelectedReport] = useState('overview')

  const { data: metrics, isLoading, error, refetch } = useQuery(
    'reports-metrics',
    () => api.getMetrics().then(res => res.data)
  )

  if (isLoading) {
    return <LoadingSpinner />
  }

  if (error) {
    return <ErrorMessage error={error} onRetry={refetch} />
  }

  if (!metrics) {
    return <ErrorMessage error={new Error('No metrics data available')} onRetry={refetch} />
  }

  const reportTypes = [
    {
      id: 'overview',
      name: 'Overview Report',
      description: 'High-level summary of election readiness',
      icon: BarChart3,
    },
    {
      id: 'delegates',
      name: 'Delegates Report',
      description: 'Detailed delegate information and status',
      icon: Users,
    },
    {
      id: 'departments',
      name: 'Department Analysis',
      description: 'Department-wise performance metrics',
      icon: FileText,
    },
    {
      id: 'gender',
      name: 'Gender Balance Report',
      description: 'Gender distribution and balance analysis',
      icon: Users,
    },
  ]

  const generateReport = (reportType: string) => {
    // This would generate and download the actual report
    console.log(`Generating ${reportType} report...`)
    // In a real implementation, this would call the backend to generate a PDF/CSV
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Reports & Analytics</h1>
          <p className="mt-2 text-gray-600">Generate detailed reports and export data</p>
        </div>
        <div className="flex items-center space-x-2 text-sm text-gray-500">
          <Calendar className="w-4 h-4" />
          <span>Last updated: {new Date().toLocaleDateString()}</span>
        </div>
      </div>

      {/* Report Types */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {reportTypes.map((report) => (
          <div
            key={report.id}
            className={`card cursor-pointer transition-all duration-200 ${
              selectedReport === report.id
                ? 'ring-2 ring-blue-500 bg-blue-50'
                : 'hover:shadow-md'
            }`}
            onClick={() => setSelectedReport(report.id)}
          >
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                  <report.icon className="w-5 h-5 text-blue-600" />
                </div>
              </div>
              <div className="ml-4">
                <h3 className="text-sm font-medium text-gray-900">{report.name}</h3>
                <p className="text-xs text-gray-500 mt-1">{report.description}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Report Preview */}
      <div className="card">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-gray-900">
            {reportTypes.find(r => r.id === selectedReport)?.name} Preview
          </h3>
          <button
            onClick={() => generateReport(selectedReport)}
            className="btn btn-primary"
          >
            <Download className="w-4 h-4 mr-2" />
            Generate Report
          </button>
        </div>

        <div className="space-y-6">
          {selectedReport === 'overview' && (
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <h4 className="text-sm font-medium text-blue-800">Win Score</h4>
                  <p className="text-2xl font-bold text-blue-900">
                    {metrics.score?.score?.toFixed(1) || 0}/100
                  </p>
                </div>
                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <h4 className="text-sm font-medium text-green-800">Total Qualified</h4>
                  <p className="text-2xl font-bold text-green-900">
                    {metrics.departments?.reduce((sum, dept) => sum + dept.qualified, 0) || 0}
                  </p>
                </div>
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                  <h4 className="text-sm font-medium text-yellow-800">Departments Under Min</h4>
                  <p className="text-2xl font-bold text-yellow-900">
                    {metrics.departments?.filter(dept => dept.gap_to_min > 0).length || 0}
                  </p>
                </div>
              </div>
            </div>
          )}

          {selectedReport === 'delegates' && (
            <div className="space-y-4">
              <h4 className="text-sm font-medium text-gray-700">Delegate Summary</h4>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Department
                      </th>
                      <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Total
                      </th>
                      <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Qualified
                      </th>
                      <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Male
                      </th>
                      <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Female
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {metrics.departments?.map((dept) => (
                      <tr key={dept.code}>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                          {dept.department}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-gray-900">
                          {dept.total_candidates}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-gray-900">
                          {dept.qualified}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-gray-900">
                          {dept.male}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-gray-900">
                          {dept.female}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {selectedReport === 'departments' && (
            <div className="space-y-4">
              <h4 className="text-sm font-medium text-gray-700">Department Analysis</h4>
              <div className="space-y-3">
                {metrics.departments?.map((dept) => (
                  <div key={dept.code} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between">
                      <h5 className="font-medium text-gray-900">{dept.department}</h5>
                      <div className="flex space-x-4 text-sm text-gray-600">
                        <span>Target: {dept.target_min}</span>
                        <span>Qualified: {dept.qualified}</span>
                        <span>Gap: {dept.gap_to_min}</span>
                      </div>
                    </div>
                    <div className="mt-2">
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-blue-600 h-2 rounded-full"
                          style={{ width: `${Math.min(100, (dept.qualified / dept.target_min) * 100)}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {selectedReport === 'gender' && (
            <div className="space-y-4">
              <h4 className="text-sm font-medium text-gray-700">Gender Balance Analysis</h4>
              <div className="space-y-3">
                {metrics.departments?.map((dept) => (
                  <div key={dept.code} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <h5 className="font-medium text-gray-900">{dept.department}</h5>
                      <span className="text-sm text-gray-600">
                        Gap: {dept.gender_gap.toFixed(2)}
                      </span>
                    </div>
                    <div className="flex space-x-2">
                      <div className="flex-1 bg-blue-100 rounded-lg p-2 text-center">
                        <div className="text-sm font-medium text-blue-800">Male</div>
                        <div className="text-lg font-bold text-blue-900">{dept.male}</div>
                      </div>
                      <div className="flex-1 bg-pink-100 rounded-lg p-2 text-center">
                        <div className="text-sm font-medium text-pink-800">Female</div>
                        <div className="text-lg font-bold text-pink-900">{dept.female}</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

