import React, { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from 'react-query'
import { Plus, Search, Filter, Edit, Trash2, Eye, CheckCircle, XCircle } from 'lucide-react'
import { api } from '../services/api'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorMessage from '../components/ErrorMessage'

interface Delegate {
  id: number
  full_name: string
  gender: string
  department: { id: number; name: string }
  course: { id: number; name: string }
  year_of_study: number
  student_id: string
  contacts: Record<string, string>
  vetting_status: string
  is_qualified: boolean
  notes: string
  created_at: string
}

export default function Delegates() {
  const [searchTerm, setSearchTerm] = useState('')
  const [filterStatus, setFilterStatus] = useState('all')
  const [showAddModal, setShowAddModal] = useState(false)
  const queryClient = useQueryClient()

  const { data: delegates, isLoading, error, refetch } = useQuery<Delegate[]>(
    'delegates',
    () => api.getDelegates().then(res => res.data),
    {
      refetchInterval: 30000,
    }
  )

  const deleteMutation = useMutation(
    (id: number) => api.deleteDelegate(id),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('delegates')
      },
    }
  )

  if (isLoading) {
    return <LoadingSpinner />
  }

  if (error) {
    return <ErrorMessage error={error} onRetry={refetch} />
  }

  if (!delegates) {
    return <ErrorMessage error={new Error('No delegates data available')} onRetry={refetch} />
  }

  const filteredDelegates = delegates.filter(delegate => {
    const matchesSearch = delegate.full_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         delegate.student_id.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesStatus = filterStatus === 'all' || delegate.vetting_status === filterStatus
    return matchesSearch && matchesStatus
  })

  const getStatusBadge = (status: string) => {
    const statusConfig = {
      'NOT_STARTED': { class: 'badge badge-info', text: 'Not Started' },
      'IN_PROGRESS': { class: 'badge badge-warning', text: 'In Progress' },
      'PASSED': { class: 'badge badge-success', text: 'Passed' },
      'FAILED': { class: 'badge badge-danger', text: 'Failed' },
    }
    const config = statusConfig[status as keyof typeof statusConfig] || statusConfig['NOT_STARTED']
    return <span className={config.class}>{config.text}</span>
  }

  const getGenderIcon = (gender: string) => {
    return gender === 'Male' ? '👨' : gender === 'Female' ? '👩' : '👤'
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Delegates Management</h1>
          <p className="mt-2 text-gray-600">View, manage, and analyze all registered delegates</p>
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
            <Plus className="w-4 h-4 mr-2" />
            Register New Delegate
          </a>
        </div>
      </div>

      {/* Filters */}
      <div className="card">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <input
                type="text"
                placeholder="Search delegates..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="input pl-10"
              />
            </div>
          </div>
          <div className="sm:w-48">
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="select"
            >
              <option value="all">All Status</option>
              <option value="NOT_STARTED">Not Started</option>
              <option value="IN_PROGRESS">In Progress</option>
              <option value="PASSED">Passed</option>
              <option value="FAILED">Failed</option>
            </select>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="card">
          <div className="text-2xl font-bold text-gray-900">{delegates.length}</div>
          <div className="text-sm text-gray-600">Total Delegates</div>
        </div>
        <div className="card">
          <div className="text-2xl font-bold text-green-600">
            {delegates.filter(d => d.vetting_status === 'PASSED').length}
          </div>
          <div className="text-sm text-gray-600">Passed Vetting</div>
        </div>
        <div className="card">
          <div className="text-2xl font-bold text-yellow-600">
            {delegates.filter(d => d.vetting_status === 'IN_PROGRESS').length}
          </div>
          <div className="text-sm text-gray-600">In Progress</div>
        </div>
        <div className="card">
          <div className="text-2xl font-bold text-red-600">
            {delegates.filter(d => d.vetting_status === 'FAILED').length}
          </div>
          <div className="text-sm text-gray-600">Failed</div>
        </div>
      </div>

      {/* Delegates Table */}
      <div className="card">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Delegate
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Department
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Year
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Qualified
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredDelegates.map((delegate) => (
                <tr key={delegate.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 h-10 w-10">
                        <div className="h-10 w-10 rounded-full bg-gray-200 flex items-center justify-center">
                          <span className="text-lg">{getGenderIcon(delegate.gender)}</span>
                        </div>
                      </div>
                      <div className="ml-4">
                        <div className="text-sm font-medium text-gray-900">
                          {delegate.full_name}
                        </div>
                        <div className="text-sm text-gray-500">
                          {delegate.student_id}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">{delegate.department.name}</div>
                    <div className="text-sm text-gray-500">{delegate.course.name}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    Year {delegate.year_of_study}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {getStatusBadge(delegate.vetting_status)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {delegate.is_qualified ? (
                      <CheckCircle className="w-5 h-5 text-green-500" />
                    ) : (
                      <XCircle className="w-5 h-5 text-gray-400" />
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <div className="flex items-center justify-end space-x-2">
                      <button className="text-blue-600 hover:text-blue-900">
                        <Eye className="w-4 h-4" />
                      </button>
                      <button className="text-yellow-600 hover:text-yellow-900">
                        <Edit className="w-4 h-4" />
                      </button>
                      <button 
                        onClick={() => deleteMutation.mutate(delegate.id)}
                        className="text-red-600 hover:text-red-900"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {filteredDelegates.length === 0 && (
          <div className="text-center py-8">
            <p className="text-gray-500">No delegates found matching your criteria.</p>
          </div>
        )}
      </div>

      {/* Add Delegate Modal Placeholder */}
      {showAddModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Add New Delegate</h3>
              <p className="text-sm text-gray-500 mb-4">
                This feature will be implemented in the next iteration.
              </p>
              <button
                onClick={() => setShowAddModal(false)}
                className="btn btn-secondary w-full"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
