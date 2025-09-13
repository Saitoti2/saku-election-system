import React, { useState, useEffect } from 'react';
import { api } from '../services/api';

interface UserProfile {
  id: number;
  full_name: string;
  student_id: string;
  user_type: string;
  user_type_display: string;
  council_position_display?: string;
  faculty_name?: string;
  department_name?: string;
  course_name: string;
  vetting_status: string;
  vetting_status_display: string;
  is_qualified: boolean;
  verification_notes?: string;
  verified_by_name?: string;
  verified_at?: string;
  whatsapp_notification_sent: boolean;
  created_at: string;
}

interface Statistics {
  total_profiles: number;
  qualified_profiles: number;
  pending_profiles: number;
  by_user_type: {
    aspirants: number;
    delegates: number;
    ieck_members: number;
  };
  by_position: Record<string, number>;
}

const AdminDashboard: React.FC = () => {
  const [profiles, setProfiles] = useState<UserProfile[]>([]);
  const [statistics, setStatistics] = useState<Statistics | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedProfile, setSelectedProfile] = useState<UserProfile | null>(null);
  const [verificationNotes, setVerificationNotes] = useState('');
  const [isQualified, setIsQualified] = useState(false);
  const [verifying, setVerifying] = useState(false);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [profilesResponse, statsResponse] = await Promise.all([
        api.get('/profiles/'),
        api.get('/profiles/statistics/')
      ]);
      setProfiles(profilesResponse.data);
      setStatistics(statsResponse.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleVerify = async () => {
    if (!selectedProfile) return;

    setVerifying(true);
    try {
      await api.post(`/profiles/${selectedProfile.id}/verify/`, {
        is_qualified: isQualified,
        verification_notes: verificationNotes
      });
      
      // Refresh data
      await fetchData();
      setSelectedProfile(null);
      setVerificationNotes('');
      setIsQualified(false);
    } catch (error) {
      console.error('Error verifying profile:', error);
    } finally {
      setVerifying(false);
    }
  };

  const filteredProfiles = profiles.filter(profile => {
    if (filter === 'all') return true;
    if (filter === 'pending') return profile.vetting_status === 'NOT_STARTED';
    if (filter === 'qualified') return profile.is_qualified;
    if (filter === 'rejected') return profile.vetting_status === 'FAILED';
    return true;
  });

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">SAKU Election Admin Dashboard</h1>

        {/* Statistics Cards */}
        {statistics && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-gray-900">Total Applications</h3>
              <p className="text-3xl font-bold text-blue-600">{statistics.total_profiles}</p>
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-gray-900">Qualified</h3>
              <p className="text-3xl font-bold text-green-600">{statistics.qualified_profiles}</p>
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-gray-900">Pending Review</h3>
              <p className="text-3xl font-bold text-yellow-600">{statistics.pending_profiles}</p>
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-gray-900">Success Rate</h3>
              <p className="text-3xl font-bold text-purple-600">
                {statistics.total_profiles > 0 
                  ? Math.round((statistics.qualified_profiles / statistics.total_profiles) * 100)
                  : 0}%
              </p>
            </div>
          </div>
        )}

        {/* User Type Breakdown */}
        {statistics && (
          <div className="bg-white rounded-lg shadow p-6 mb-8">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Applications by Type</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="text-center">
                <p className="text-2xl font-bold text-blue-600">{statistics.by_user_type.aspirants}</p>
                <p className="text-gray-600">Council Aspirants</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-green-600">{statistics.by_user_type.delegates}</p>
                <p className="text-gray-600">Delegates</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-purple-600">{statistics.by_user_type.ieck_members}</p>
                <p className="text-gray-600">IECK Members</p>
              </div>
            </div>
          </div>
        )}

        {/* Position Breakdown for Aspirants */}
        {statistics && Object.keys(statistics.by_position).length > 0 && (
          <div className="bg-white rounded-lg shadow p-6 mb-8">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Council Positions</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {Object.entries(statistics.by_position).map(([position, count]) => (
                <div key={position} className="text-center">
                  <p className="text-xl font-bold text-indigo-600">{count}</p>
                  <p className="text-sm text-gray-600">{position}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Filter and Profiles Table */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b">
            <div className="flex justify-between items-center">
              <h3 className="text-lg font-semibold text-gray-900">Applications</h3>
              <select
                value={filter}
                onChange={(e) => setFilter(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">All Applications</option>
                <option value="pending">Pending Review</option>
                <option value="qualified">Qualified</option>
                <option value="rejected">Rejected</option>
              </select>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Type
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Position
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Faculty
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Department
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredProfiles.map((profile) => (
                  <tr key={profile.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm font-medium text-gray-900">{profile.full_name}</div>
                        <div className="text-sm text-gray-500">{profile.student_id}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800">
                        {profile.user_type_display}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {profile.council_position_display || '-'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {profile.faculty_name || '-'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {profile.department_name || '-'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                        profile.is_qualified 
                          ? 'bg-green-100 text-green-800'
                          : profile.vetting_status === 'FAILED'
                          ? 'bg-red-100 text-red-800'
                          : 'bg-yellow-100 text-yellow-800'
                      }`}>
                        {profile.vetting_status_display}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <button
                        onClick={() => setSelectedProfile(profile)}
                        className="text-blue-600 hover:text-blue-900"
                      >
                        Review
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Verification Modal */}
        {selectedProfile && (
          <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
              <div className="mt-3">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                  Review Application: {selectedProfile.full_name}
                </h3>
                
                <div className="mb-4">
                  <p><strong>Student ID:</strong> {selectedProfile.student_id}</p>
                  <p><strong>Type:</strong> {selectedProfile.user_type_display}</p>
                  {selectedProfile.council_position_display && (
                    <p><strong>Position:</strong> {selectedProfile.council_position_display}</p>
                  )}
                  <p><strong>Department:</strong> {selectedProfile.department_name}</p>
                </div>

                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Verification Notes
                  </label>
                  <textarea
                    value={verificationNotes}
                    onChange={(e) => setVerificationNotes(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    rows={3}
                    placeholder="Add verification notes..."
                  />
                </div>

                <div className="mb-4">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={isQualified}
                      onChange={(e) => setIsQualified(e.target.checked)}
                      className="mr-2"
                    />
                    <span className="text-sm text-gray-700">Qualified for election</span>
                  </label>
                </div>

                <div className="flex justify-end space-x-3">
                  <button
                    onClick={() => {
                      setSelectedProfile(null);
                      setVerificationNotes('');
                      setIsQualified(false);
                    }}
                    className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleVerify}
                    disabled={verifying}
                    className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:opacity-50"
                  >
                    {verifying ? 'Verifying...' : 'Submit Review'}
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;
