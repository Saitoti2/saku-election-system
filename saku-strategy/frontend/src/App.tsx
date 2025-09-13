import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from 'react-query'
import { ReactQueryDevtools } from 'react-query/devtools'
import Layout from './components/Layout'
import StrategicDashboard from './pages/StrategicDashboard'
import DelegateRegistration from './pages/DelegateRegistration'
import Delegates from './pages/Delegates'
import UserRegistration from './pages/UserRegistration'
import AdminDashboard from './pages/AdminDashboard'
import './index.css'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Layout>
            <Routes>
              <Route path="/" element={<Navigate to="/strategy" replace />} />
              <Route path="/strategy" element={<StrategicDashboard />} />
              <Route path="/register" element={<DelegateRegistration />} />
              <Route path="/delegates" element={<Delegates />} />
              <Route path="/user-registration" element={<UserRegistration />} />
              <Route path="/admin" element={<AdminDashboard />} />
            </Routes>
          </Layout>
        </div>
      </Router>
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  )
}

export default App
