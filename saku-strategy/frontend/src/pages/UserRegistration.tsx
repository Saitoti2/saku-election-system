import React, { useState, useEffect } from 'react';
import { api } from '../services/api';

interface Faculty {
  id: number;
  code: string;
  name: string;
}

interface Department {
  id: number;
  code: string;
  name: string;
  faculty: Faculty;
}

interface Course {
  id: number;
  name: string;
  code?: string;
  department: Department;
  faculty: Faculty;
}

interface RegistrationData {
  username: string;
  email: string;
  password: string;
  user_type: 'ASPIRANT' | 'DELEGATE' | 'IECK';
  full_name: string;
  gender: 'Male' | 'Female' | 'Other';
  student_id: string;
  course_id: number;
  year_of_study: number;
  whatsapp_number: string;
  phone_number: string;
  council_position?: string;
  school_fees_screenshot: File | null;
  last_semester_results: File | null;
  second_last_semester_results: File | null;
  course_registration_screenshot: File | null;
  good_conduct_certificate: File | null;
  school_id_image: File | null;
  last_semester_transcript: File | null;
  second_last_semester_transcript: File | null;
}

const UserRegistration: React.FC = () => {
  const [courses, setCourses] = useState<Course[]>([]);
  const [filteredCourses, setFilteredCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [courseSearchTerm, setCourseSearchTerm] = useState('');
  const [showCourseDropdown, setShowCourseDropdown] = useState(false);

  const [formData, setFormData] = useState<RegistrationData>({
    username: '',
    email: '',
    password: '',
    user_type: 'ASPIRANT',
    full_name: '',
    gender: 'Male',
    student_id: '',
    course_id: 0,
    year_of_study: 1,
    whatsapp_number: '',
    phone_number: '',
    council_position: '',
    school_fees_screenshot: null,
    last_semester_results: null,
    second_last_semester_results: null,
    course_registration_screenshot: null,
    good_conduct_certificate: null,
    school_id_image: null,
    last_semester_transcript: null,
    second_last_semester_transcript: null,
  });

  const councilPositions = [
    { value: 'CHAIR', label: 'Chair (President)' },
    { value: 'VICE_CHAIR', label: 'Vice Chair' },
    { value: 'SECRETARY_GENERAL', label: 'Secretary General' },
    { value: 'FINANCE_SECRETARY', label: 'Finance Secretary' },
    { value: 'ACADEMIC_SECRETARY', label: 'Academic Secretary' },
    { value: 'SPORTS_SECRETARY', label: 'Sports Secretary' },
    { value: 'SPECIAL_INTERESTS_SECRETARY', label: 'Special Interests Secretary' },
  ];

  useEffect(() => {
    fetchAllCourses();
  }, []);

  useEffect(() => {
    if (courseSearchTerm.length >= 2) {
      searchCourses(courseSearchTerm);
    } else {
      setFilteredCourses([]);
      setShowCourseDropdown(false);
    }
  }, [courseSearchTerm]);

  const fetchAllCourses = async () => {
    try {
      const response = await api.get('/courses/');
      setCourses(response.data);
    } catch (error) {
      console.error('Error fetching courses:', error);
    }
  };

  const searchCourses = async (query: string) => {
    try {
      const response = await api.get(`/courses/search/?q=${encodeURIComponent(query)}`);
      setFilteredCourses(response.data);
      setShowCourseDropdown(true);
    } catch (error) {
      console.error('Error searching courses:', error);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleCourseSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setCourseSearchTerm(value);
    
    // If user clears the search, reset course selection
    if (!value) {
      setFormData(prev => ({ ...prev, course_id: 0 }));
    }
  };

  const handleCourseSelect = (course: Course) => {
    setFormData(prev => ({ ...prev, course_id: course.id }));
    setCourseSearchTerm(course.name);
    setShowCourseDropdown(false);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, files } = e.target;
    if (files && files[0]) {
      setFormData(prev => ({
        ...prev,
        [name]: files[0]
      }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const formDataToSend = new FormData();
      
      // Add all form fields
      Object.entries(formData).forEach(([key, value]) => {
        if (value !== null && value !== undefined && value !== '') {
          if (value instanceof File) {
            formDataToSend.append(key, value);
          } else {
            formDataToSend.append(key, value.toString());
          }
        }
      });

      await api.post('/profiles/', formDataToSend, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setSuccess(true);
    } catch (error: any) {
      setError(error.response?.data?.detail || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="max-w-md w-full bg-white rounded-lg shadow-md p-6 text-center">
          <div className="text-green-500 text-6xl mb-4">✓</div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Registration Successful!</h2>
          <p className="text-gray-600 mb-4">
            Your application has been submitted successfully. You will receive a WhatsApp notification once your application is reviewed.
          </p>
          <button
            onClick={() => window.location.reload()}
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
          >
            Register Another
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-6 text-center">
            SAKU Council Election Registration
          </h1>

          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* User Type Selection */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Registration Type *
                </label>
                <select
                  name="user_type"
                  value={formData.user_type}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                >
                  <option value="ASPIRANT">Council Aspirant</option>
                  <option value="DELEGATE">Delegate</option>
                  <option value="IECK">IECK Member</option>
                </select>
              </div>

              {formData.user_type === 'ASPIRANT' && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Council Position *
                  </label>
                  <select
                    name="council_position"
                    value={formData.council_position}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  >
                    <option value="">Select Position</option>
                    {councilPositions.map(pos => (
                      <option key={pos.value} value={pos.value}>
                        {pos.label}
                      </option>
                    ))}
                  </select>
                </div>
              )}
            </div>

            {/* Account Information */}
            <div className="border-t pt-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Account Information</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Username *
                  </label>
                  <input
                    type="text"
                    name="username"
                    value={formData.username}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Email *
                  </label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Password *
                  </label>
                  <input
                    type="password"
                    name="password"
                    value={formData.password}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                    minLength={8}
                  />
                </div>
              </div>
            </div>

            {/* Personal Information */}
            <div className="border-t pt-6">
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
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
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
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
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
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
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
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
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
            <div className="border-t pt-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Academic Information</h3>
              <div className="grid grid-cols-1 gap-4">
                <div className="relative">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Course *
                  </label>
                  <input
                    type="text"
                    value={courseSearchTerm}
                    onChange={handleCourseSearch}
                    placeholder="Type your course name to search..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                  
                  {/* Course Dropdown */}
                  {showCourseDropdown && filteredCourses.length > 0 && (
                    <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg max-h-60 overflow-y-auto">
                      {filteredCourses.map((course) => (
                        <div
                          key={course.id}
                          onClick={() => handleCourseSelect(course)}
                          className="px-3 py-2 hover:bg-gray-100 cursor-pointer border-b border-gray-100 last:border-b-0"
                        >
                          <div className="font-medium text-gray-900">{course.name}</div>
                          <div className="text-sm text-gray-500">
                            {course.department.name} • {course.faculty.name}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                  
                  {/* Selected Course Info */}
                  {formData.course_id > 0 && (
                    <div className="mt-2 p-3 bg-blue-50 border border-blue-200 rounded-md">
                      <div className="text-sm text-blue-800">
                        <strong>Selected Course:</strong> {courseSearchTerm}
                      </div>
                      {(() => {
                        const selectedCourse = courses.find(c => c.id === formData.course_id);
                        return selectedCourse ? (
                          <div className="text-xs text-blue-600 mt-1">
                            Department: {selectedCourse.department.name} • Faculty: {selectedCourse.faculty.name}
                          </div>
                        ) : null;
                      })()}
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Contact Information */}
            <div className="border-t pt-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Contact Information</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Phone Number *
                  </label>
                  <input
                    type="tel"
                    name="phone_number"
                    value={formData.phone_number}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    WhatsApp Number *
                  </label>
                  <input
                    type="tel"
                    name="whatsapp_number"
                    value={formData.whatsapp_number}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                    placeholder="+254700000000"
                  />
                </div>
              </div>
            </div>

            {/* Document Uploads */}
            <div className="border-t pt-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Required Documents</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    School Fees Screenshot (80%+ clearance) *
                  </label>
                  <input
                    type="file"
                    name="school_fees_screenshot"
                    onChange={handleFileChange}
                    accept="image/*"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Last Semester Results (PDF) *
                  </label>
                  <input
                    type="file"
                    name="last_semester_results"
                    onChange={handleFileChange}
                    accept=".pdf"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Second Last Semester Results (PDF) *
                  </label>
                  <input
                    type="file"
                    name="second_last_semester_results"
                    onChange={handleFileChange}
                    accept=".pdf"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Course Registration Screenshot *
                  </label>
                  <input
                    type="file"
                    name="course_registration_screenshot"
                    onChange={handleFileChange}
                    accept="image/*"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
                {formData.user_type === 'ASPIRANT' && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Certificate of Good Conduct (PDF) *
                    </label>
                    <input
                      type="file"
                      name="good_conduct_certificate"
                      onChange={handleFileChange}
                      accept=".pdf"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  </div>
                )}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    School ID Image *
                  </label>
                  <input
                    type="file"
                    name="school_id_image"
                    onChange={handleFileChange}
                    accept="image/*"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Last Semester Transcript (PDF) *
                  </label>
                  <input
                    type="file"
                    name="last_semester_transcript"
                    onChange={handleFileChange}
                    accept=".pdf"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Second Last Semester Transcript (PDF) *
                  </label>
                  <input
                    type="file"
                    name="second_last_semester_transcript"
                    onChange={handleFileChange}
                    accept=".pdf"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
              </div>
            </div>

            {/* Submit Button */}
            <div className="border-t pt-6">
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-blue-600 text-white py-3 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Submitting...' : 'Submit Registration'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default UserRegistration;
