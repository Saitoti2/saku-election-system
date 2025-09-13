import React, { useState } from 'react'
import { useMutation, useQueryClient } from 'react-query'
import { Save, UserPlus, CheckCircle, AlertCircle } from 'lucide-react'
import { api } from '../services/api'
import LoadingSpinner from '../components/LoadingSpinner'

interface DelegateFormData {
  full_name: string
  gender: string
  department: number
  course: number
  year_of_study: number
  student_id: string
  phone: string
  email: string
  address: string
  academic_standing: string
  leadership_experience: string
  motivation: string
  previous_positions: string
  references: string
  notes: string
}

export default function DelegateRegistration() {
  const [formData, setFormData] = useState<DelegateFormData>({
    full_name: '',
    gender: 'Male',
    department: 0,
    course: 0,
    year_of_study: 2,
    student_id: '',
    phone: '',
    email: '',
    address: '',
    academic_standing: 'Good',
    leadership_experience: '',
    motivation: '',
    previous_positions: '',
    references: '',
    notes: ''
  })

  const [showSuccess, setShowSuccess] = useState(false)
  const queryClient = useQueryClient()

  const { data: departments } = useQuery('departments', () => 
    api.getDepartments().then(res => res.data)
  )

  const { data: courses } = useQuery(['courses', formData.department], () => 
    api.getCourses(formData.department).then(res => res.data),
    { enabled: !!formData.department }
  )

  const createMutation = useMutation(
    (data: DelegateFormData) => api.createDelegate({
      full_name: data.full_name,
      gender: data.gender,
      department: data.department,
      course: data.course,
      year_of_study: data.year_of_study,
      student_id: data.student_id,
      contacts: {
        phone: data.phone,
        email: data.email,
        address: data.address
      },
      eligibility: {
        academic_standing: data.academic_standing,
        leadership_experience: data.leadership_experience,
        previous_positions: data.previous_positions,
        references: data.references
      },
      notes: data.notes
    }),
    {
      onSuccess: () => {
        setShowSuccess(true)
        setFormData({
          full_name: '',
          gender: 'Male',
          department: 0,
          course: 0,
          year_of_study: 2,
          student_id: '',
          phone: '',
          email: '',
          address: '',
          academic_standing: 'Good',
          leadership_experience: '',
          motivation: '',
          previous_positions: '',
          references: '',
          notes: ''
        })
        queryClient.invalidateQueries('delegates')
        queryClient.invalidateQueries('dashboard-metrics')
        setTimeout(() => setShowSuccess(false), 3000)
      }
    }
  )

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    createMutation.mutate(formData)
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: name === 'department' || name === 'course' || name === 'year_of_study' ? parseInt(value) || 0 : value
    }))
  }

  if (createMutation.isLoading) {
    return <LoadingSpinner text="Registering delegate..." />
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Delegate Registration</h1>
          <p className="mt-2 text-gray-600">Register new delegates for SAKU elections</p>
        </div>
        <div className="flex items-center space-x-2">
          <UserPlus className="w-6 h-6 text-blue-600" />
          <span className="text-sm text-gray-600">New Registration</span>
        </div>
      </div>

      {/* Success Message */}
      {showSuccess && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <div className="flex items-center">
            <CheckCircle className="w-5 h-5 text-green-600" />
            <p className="ml-3 text-sm text-green-800">
              Delegate registered successfully! They have been added to the database.
            </p>
          </div>
        </div>
      )}

      {/* Error Message */}
      {createMutation.isError && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-center">
            <AlertCircle className="w-5 h-5 text-red-600" />
            <p className="ml-3 text-sm text-red-800">
              Error: {createMutation.error?.message || 'Failed to register delegate'}
            </p>
          </div>
        </div>
      )}

      {/* Registration Form */}
      <div className="card">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Personal Information */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Personal Information</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Full Name *
                </label>
                <input
                  type="text"
                  name="full_name"
                  value={formData.full_name}
                  onChange={handleInputChange}
                  required
                  className="input"
                  placeholder="Enter full name"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Gender *
                </label>
                <select
                  name="gender"
                  value={formData.gender}
                  onChange={handleInputChange}
                  required
                  className="select"
                >
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                  <option value="Other">Other</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Student ID *
                </label>
                <input
                  type="text"
                  name="student_id"
                  value={formData.student_id}
                  onChange={handleInputChange}
                  required
                  className="input"
                  placeholder="e.g., CS/2021/001"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Year of Study *
                </label>
                <select
                  name="year_of_study"
                  value={formData.year_of_study}
                  onChange={handleInputChange}
                  required
                  className="select"
                >
                  <option value={1}>Year 1</option>
                  <option value={2}>Year 2</option>
                  <option value={3}>Year 3</option>
                  <option value={4}>Year 4</option>
                  <option value={5}>Year 5</option>
                </select>
              </div>
            </div>
          </div>

          {/* Academic Information */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Academic Information</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Department *
                </label>
                <select
                  name="department"
                  value={formData.department}
                  onChange={handleInputChange}
                  required
                  className="select"
                >
                  <option value={0}>Select Department</option>
                  {departments?.map((dept: any) => (
                    <option key={dept.id} value={dept.id}>{dept.name}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Course *
                </label>
                <select
                  name="course"
                  value={formData.course}
                  onChange={handleInputChange}
                  required
                  className="select"
                  disabled={!formData.department}
                >
                  <option value={0}>Select Course</option>
                  {courses?.map((course: any) => (
                    <option key={course.id} value={course.id}>{course.name}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Academic Standing
                </label>
                <select
                  name="academic_standing"
                  value={formData.academic_standing}
                  onChange={handleInputChange}
                  className="select"
                >
                  <option value="Excellent">Excellent</option>
                  <option value="Good">Good</option>
                  <option value="Average">Average</option>
                  <option value="Below Average">Below Average</option>
                </select>
              </div>
            </div>
          </div>

          {/* Contact Information */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Contact Information</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Phone Number *
                </label>
                <input
                  type="tel"
                  name="phone"
                  value={formData.phone}
                  onChange={handleInputChange}
                  required
                  className="input"
                  placeholder="+254 700 000 000"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Email Address
                </label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  className="input"
                  placeholder="student@kca.ac.ke"
                />
              </div>
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Address
                </label>
                <input
                  type="text"
                  name="address"
                  value={formData.address}
                  onChange={handleInputChange}
                  className="input"
                  placeholder="Residential address"
                />
              </div>
            </div>
          </div>

          {/* Leadership & Experience */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Leadership & Experience</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Leadership Experience
                </label>
                <textarea
                  name="leadership_experience"
                  value={formData.leadership_experience}
                  onChange={handleInputChange}
                  rows={3}
                  className="input"
                  placeholder="Describe your leadership experience..."
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Previous Positions Held
                </label>
                <input
                  type="text"
                  name="previous_positions"
                  value={formData.previous_positions}
                  onChange={handleInputChange}
                  className="input"
                  placeholder="e.g., Class Representative, Club President"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Motivation for Running
                </label>
                <textarea
                  name="motivation"
                  value={formData.motivation}
                  onChange={handleInputChange}
                  rows={3}
                  className="input"
                  placeholder="Why do you want to be a delegate?"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  References
                </label>
                <textarea
                  name="references"
                  value={formData.references}
                  onChange={handleInputChange}
                  rows={2}
                  className="input"
                  placeholder="Names and contacts of references"
                />
              </div>
            </div>
          </div>

          {/* Additional Notes */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Additional Notes
            </label>
            <textarea
              name="notes"
              value={formData.notes}
              onChange={handleInputChange}
              rows={3}
              className="input"
              placeholder="Any additional information..."
            />
          </div>

          {/* Submit Button */}
          <div className="flex justify-end space-x-4">
            <button
              type="button"
              onClick={() => setFormData({
                full_name: '',
                gender: 'Male',
                department: 0,
                course: 0,
                year_of_study: 2,
                student_id: '',
                phone: '',
                email: '',
                address: '',
                academic_standing: 'Good',
                leadership_experience: '',
                motivation: '',
                previous_positions: '',
                references: '',
                notes: ''
              })}
              className="btn btn-secondary"
            >
              Clear Form
            </button>
            <button
              type="submit"
              disabled={createMutation.isLoading}
              className="btn btn-primary"
            >
              <Save className="w-4 h-4 mr-2" />
              Register Delegate
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

