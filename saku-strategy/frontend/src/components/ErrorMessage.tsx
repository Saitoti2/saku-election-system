import React from 'react'
import { AlertTriangle, RefreshCw } from 'lucide-react'

interface ErrorMessageProps {
  error: Error
  onRetry?: () => void
}

export default function ErrorMessage({ error, onRetry }: ErrorMessageProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md w-full">
        <div className="flex items-center">
          <AlertTriangle className="w-8 h-8 text-red-600 flex-shrink-0" />
          <div className="ml-4">
            <h3 className="text-lg font-medium text-red-800">Error Loading Data</h3>
            <p className="mt-1 text-sm text-red-700">{error.message}</p>
            {onRetry && (
              <button
                onClick={onRetry}
                className="mt-3 inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-red-700 bg-red-100 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
              >
                <RefreshCw className="w-4 h-4 mr-2" />
                Try Again
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

