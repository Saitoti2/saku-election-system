// API Configuration
// This file manages the API base URL for the frontend
// In production, Vercel will inject the NEXT_PUBLIC_API_URL environment variable

const getApiUrl = () => {
  // Check if we're in a browser environment
  if (typeof window !== 'undefined') {
    // Check for environment variable (set by Vercel)
    const envApiUrl = window.API_URL || process?.env?.NEXT_PUBLIC_API_URL;
    if (envApiUrl) {
      return envApiUrl.replace(/\/$/, ''); // Remove trailing slash
    }
    
    // Check for data attribute on html tag (can be set in HTML)
    const htmlApiUrl = document.documentElement.getAttribute('data-api-url');
    if (htmlApiUrl) {
      return htmlApiUrl.replace(/\/$/, '');
    }
  }
  
  // Default to localhost for development
  return 'http://127.0.0.1:8000';
};

// Export API base URL
const API_BASE_URL = getApiUrl();

// Helper function to build API URLs
function apiUrl(endpoint) {
  // Remove leading slash if present to avoid double slashes
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint.slice(1) : endpoint;
  // The endpoint already includes 'api/', so just append to base URL
  return `${API_BASE_URL}/${cleanEndpoint}`;
}

// Make it available globally
if (typeof window !== 'undefined') {
  window.API_BASE_URL = API_BASE_URL;
  window.apiUrl = apiUrl;
}

