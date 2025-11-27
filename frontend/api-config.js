// API Configuration
// This file manages the backend API URL based on environment

(function() {
    'use strict';
    
    // Get API URL from environment variable or use default
    const getApiBaseUrl = function() {
        // Check if we're in a browser environment
        if (typeof window !== 'undefined') {
            // Try to get from window object (set by Vercel or build process)
            if (window.API_BASE_URL) {
                return window.API_BASE_URL;
            }
            
            // Try to get from meta tag (can be set during build)
            const metaTag = document.querySelector('meta[name="api-base-url"]');
            if (metaTag && metaTag.content) {
                return metaTag.content;
            }
            
            // Check localStorage for override (useful for development)
            const localOverride = localStorage.getItem('API_BASE_URL');
            if (localOverride) {
                return localOverride;
            }
            
            // Default: use environment variable from Vercel or fallback
            // In production on Vercel, try to fetch from serverless function
            // Otherwise, use hostname-based detection
            const isLocal = window.location.hostname === 'localhost' || 
                           window.location.hostname === '127.0.0.1';
            
            if (isLocal) {
                return 'http://127.0.0.1:8001';
            } else {
                // Production: use Render backend URL
                // Update this with your actual Render backend URL after deployment
                return 'https://saku-backend.onrender.com';
            }
        }
        
        // Fallback for Node.js environments (shouldn't happen in browser)
        return process.env.API_BASE_URL || 'http://127.0.0.1:8001';
    };
    
    // Set the API base URL
    window.API_BASE_URL = getApiBaseUrl();
    
    // API configuration object
    window.API_CONFIG = {
        baseURL: window.API_BASE_URL,
        endpoints: {
            auth: {
                login: '/api/auth/login/',
                register: '/api/auth/register/',
                refresh: '/api/auth/refresh/',
                logout: '/api/auth/logout/',
                profile: '/api/auth/profile/',
                updateProfile: '/api/auth/profile/update/',
                tokenRefresh: '/api/auth/token/refresh/'
            },
            profiles: {
                get: (id) => `/api/profiles/${id}/`,
                verify: (id) => `/api/profiles/${id}/verify/`,
                update: (id) => `/api/profiles/${id}/`
            },
            courses: {
                list: '/api/courses/',
                search: '/api/courses/search/'
            },
            elections: {
                list: '/api/elections/',
                register: '/api/elections/register/',
                vote: '/api/elections/vote/'
            }
        },
        
        // Helper function to build full URL
        url: function(endpoint) {
            // If endpoint already includes http, return as-is
            if (endpoint.startsWith('http://') || endpoint.startsWith('https://')) {
                return endpoint;
            }
            // Remove leading slash if present to avoid double slashes
            const cleanEndpoint = endpoint.startsWith('/') ? endpoint.substring(1) : endpoint;
            return `${this.baseURL}/${cleanEndpoint}`;
        },
        
        // Helper function for API calls with authentication
        fetch: async function(endpoint, options = {}) {
            const url = this.url(endpoint);
            const defaultOptions = {
                headers: {
                    'Content-Type': 'application/json',
                }
            };
            
            // Add authentication token if available
            const tokens = this.getTokens();
            if (tokens && tokens.access) {
                defaultOptions.headers['Authorization'] = `Bearer ${tokens.access}`;
            }
            
            // Merge with provided options
            const finalOptions = {
                ...defaultOptions,
                ...options,
                headers: {
                    ...defaultOptions.headers,
                    ...(options.headers || {})
                }
            };
            
            return fetch(url, finalOptions);
        },
        
        // Get stored tokens
        getTokens: function() {
            try {
                const tokensStr = localStorage.getItem('saku_tokens');
                if (tokensStr) {
                    return JSON.parse(tokensStr);
                }
            } catch (e) {
                console.error('Error parsing tokens:', e);
            }
            return null;
        },
        
        // Set tokens
        setTokens: function(tokens) {
            localStorage.setItem('saku_tokens', JSON.stringify(tokens));
        },
        
        // Clear tokens
        clearTokens: function() {
            localStorage.removeItem('saku_tokens');
            localStorage.removeItem('saku_user_profile');
        }
    };
    
    // Log API configuration in development
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        console.log('API Configuration:', window.API_CONFIG);
    }
})();

