import React, { useState } from 'react'
import { Save, RefreshCw, AlertTriangle, CheckCircle } from 'lucide-react'

export default function Settings() {
  const [settings, setSettings] = useState({
    minDelegatesPerDept: 3,
    genderBalanceTarget: 0.33,
    genderBalanceTolerance: 0.05,
    autoRefreshInterval: 30,
    notifications: true,
    emailAlerts: false,
  })

  const [isSaving, setIsSaving] = useState(false)
  const [saveStatus, setSaveStatus] = useState<'idle' | 'success' | 'error'>('idle')

  const handleSave = async () => {
    setIsSaving(true)
    setSaveStatus('idle')
    
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      setSaveStatus('success')
    } catch (error) {
      setSaveStatus('error')
    } finally {
      setIsSaving(false)
    }
  }

  const handleReset = () => {
    setSettings({
      minDelegatesPerDept: 3,
      genderBalanceTarget: 0.33,
      genderBalanceTolerance: 0.05,
      autoRefreshInterval: 30,
      notifications: true,
      emailAlerts: false,
    })
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
          <p className="mt-2 text-gray-600">Configure system parameters and preferences</p>
        </div>
        <div className="flex space-x-3">
          <button
            onClick={handleReset}
            className="btn btn-secondary"
          >
            <RefreshCw className="w-4 h-4 mr-2" />
            Reset to Defaults
          </button>
          <button
            onClick={handleSave}
            disabled={isSaving}
            className="btn btn-primary"
          >
            <Save className="w-4 h-4 mr-2" />
            {isSaving ? 'Saving...' : 'Save Changes'}
          </button>
        </div>
      </div>

      {/* Save Status */}
      {saveStatus === 'success' && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <div className="flex items-center">
            <CheckCircle className="w-5 h-5 text-green-600" />
            <p className="ml-3 text-sm text-green-800">Settings saved successfully!</p>
          </div>
        </div>
      )}

      {saveStatus === 'error' && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-center">
            <AlertTriangle className="w-5 h-5 text-red-600" />
            <p className="ml-3 text-sm text-red-800">Failed to save settings. Please try again.</p>
          </div>
        </div>
      )}

      {/* Settings Sections */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Election Rules */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Election Rules</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Minimum Delegates per Department
              </label>
              <input
                type="number"
                min="1"
                max="10"
                value={settings.minDelegatesPerDept}
                onChange={(e) => setSettings(prev => ({
                  ...prev,
                  minDelegatesPerDept: parseInt(e.target.value) || 3
                }))}
                className="input"
              />
              <p className="text-xs text-gray-500 mt-1">
                Minimum number of qualified delegates required per department
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Gender Balance Target (Female %)
              </label>
              <input
                type="number"
                min="0"
                max="1"
                step="0.01"
                value={settings.genderBalanceTarget}
                onChange={(e) => setSettings(prev => ({
                  ...prev,
                  genderBalanceTarget: parseFloat(e.target.value) || 0.33
                }))}
                className="input"
              />
              <p className="text-xs text-gray-500 mt-1">
                Target percentage of female delegates (0.33 = 33%)
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Gender Balance Tolerance
              </label>
              <input
                type="number"
                min="0"
                max="0.5"
                step="0.01"
                value={settings.genderBalanceTolerance}
                onChange={(e) => setSettings(prev => ({
                  ...prev,
                  genderBalanceTolerance: parseFloat(e.target.value) || 0.05
                }))}
                className="input"
              />
              <p className="text-xs text-gray-500 mt-1">
                Acceptable deviation from gender balance target (0.05 = 5%)
              </p>
            </div>
          </div>
        </div>

        {/* System Preferences */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">System Preferences</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Auto Refresh Interval (seconds)
              </label>
              <select
                value={settings.autoRefreshInterval}
                onChange={(e) => setSettings(prev => ({
                  ...prev,
                  autoRefreshInterval: parseInt(e.target.value) || 30
                }))}
                className="select"
              >
                <option value={10}>10 seconds</option>
                <option value={30}>30 seconds</option>
                <option value={60}>1 minute</option>
                <option value={300}>5 minutes</option>
                <option value={0}>Disabled</option>
              </select>
              <p className="text-xs text-gray-500 mt-1">
                How often to automatically refresh data
              </p>
            </div>

            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div>
                  <label className="text-sm font-medium text-gray-700">
                    Enable Notifications
                  </label>
                  <p className="text-xs text-gray-500">
                    Show browser notifications for important updates
                  </p>
                </div>
                <input
                  type="checkbox"
                  checked={settings.notifications}
                  onChange={(e) => setSettings(prev => ({
                    ...prev,
                    notifications: e.target.checked
                  }))}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <label className="text-sm font-medium text-gray-700">
                    Email Alerts
                  </label>
                  <p className="text-xs text-gray-500">
                    Send email notifications for critical issues
                  </p>
                </div>
                <input
                  type="checkbox"
                  checked={settings.emailAlerts}
                  onChange={(e) => setSettings(prev => ({
                    ...prev,
                    emailAlerts: e.target.checked
                  }))}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Advanced Settings */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Advanced Settings</h3>
        <div className="space-y-4">
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <div className="flex">
              <AlertTriangle className="w-5 h-5 text-yellow-600 flex-shrink-0" />
              <div className="ml-3">
                <h4 className="text-sm font-medium text-yellow-800">Warning</h4>
                <p className="text-sm text-yellow-700 mt-1">
                  Advanced settings are not yet implemented. These features will be available in future updates.
                </p>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                API Endpoint
              </label>
              <input
                type="text"
                value="http://localhost:8000/api"
                disabled
                className="input bg-gray-100"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Database Status
              </label>
              <div className="flex items-center">
                <div className="h-2 w-2 bg-green-400 rounded-full mr-2"></div>
                <span className="text-sm text-gray-600">Connected</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

