/**
 * Authentication service for SAKU Election Platform
 * Handles JWT tokens, session management, and secure API calls
 */

const API_BASE_URL = 'http://127.0.0.1:8000/api';

interface AuthTokens {
    access: string;
    refresh: string;
}

interface UserProfile {
    id: number;
    username: string;
    email: string;
    full_name: string;
    student_id: string;
    user_type: 'ASPIRANT' | 'DELEGATE' | 'IECK';
    is_admin: boolean;
    [key: string]: any;
}

interface LoginResponse {
    access: string;
    refresh: string;
    profile: UserProfile;
    user_type: string;
    is_admin: boolean;
}

class AuthService {
    private accessToken: string | null = null;
    private refreshToken: string | null = null;
    private userProfile: UserProfile | null = null;
    private sessionTimeout: number | null = null;
    private readonly SESSION_DURATION = 5 * 60 * 1000; // 5 minutes in milliseconds

    constructor() {
        this.loadTokensFromStorage();
        this.setupSessionTimeout();
    }

    /**
     * Load tokens from localStorage
     */
    private loadTokensFromStorage(): void {
        try {
            const tokens = localStorage.getItem('saku_tokens');
            if (tokens) {
                const parsedTokens: AuthTokens = JSON.parse(tokens);
                this.accessToken = parsedTokens.access;
                this.refreshToken = parsedTokens.refresh;
                
                // Load user profile
                const profile = localStorage.getItem('saku_user_profile');
                if (profile) {
                    this.userProfile = JSON.parse(profile);
                }
            }
        } catch (error) {
            console.error('Error loading tokens from storage:', error);
            this.clearTokens();
        }
    }

    /**
     * Save tokens to localStorage
     */
    private saveTokensToStorage(tokens: AuthTokens): void {
        try {
            localStorage.setItem('saku_tokens', JSON.stringify(tokens));
            this.accessToken = tokens.access;
            this.refreshToken = tokens.refresh;
        } catch (error) {
            console.error('Error saving tokens to storage:', error);
        }
    }

    /**
     * Save user profile to localStorage
     */
    private saveUserProfileToStorage(profile: UserProfile): void {
        try {
            localStorage.setItem('saku_user_profile', JSON.stringify(profile));
            this.userProfile = profile;
        } catch (error) {
            console.error('Error saving user profile to storage:', error);
        }
    }

    /**
     * Clear all tokens and user data
     */
    private clearTokens(): void {
        localStorage.removeItem('saku_tokens');
        localStorage.removeItem('saku_user_profile');
        this.accessToken = null;
        this.refreshToken = null;
        this.userProfile = null;
        this.clearSessionTimeout();
    }

    /**
     * Setup session timeout
     */
    private setupSessionTimeout(): void {
        if (this.isAuthenticated()) {
            this.sessionTimeout = window.setTimeout(() => {
                this.logout();
                // Redirect to login page
                window.location.href = '/login.html';
            }, this.SESSION_DURATION);
        }
    }

    /**
     * Clear session timeout
     */
    private clearSessionTimeout(): void {
        if (this.sessionTimeout) {
            clearTimeout(this.sessionTimeout);
            this.sessionTimeout = null;
        }
    }

    /**
     * Reset session timeout (call on user activity)
     */
    public resetSessionTimeout(): void {
        this.clearSessionTimeout();
        this.setupSessionTimeout();
    }

    /**
     * Check if user is authenticated
     */
    public isAuthenticated(): boolean {
        return !!(this.accessToken && this.userProfile);
    }

    /**
     * Get current user profile
     */
    public getCurrentUser(): UserProfile | null {
        return this.userProfile;
    }

    /**
     * Get access token
     */
    public getAccessToken(): string | null {
        return this.accessToken;
    }

    /**
     * Login user
     */
    public async login(username: string, password: string): Promise<LoginResponse> {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Login failed');
            }

            const data: LoginResponse = await response.json();
            
            // Save tokens and profile
            this.saveTokensToStorage({
                access: data.access,
                refresh: data.refresh
            });
            this.saveUserProfileToStorage(data.profile);
            
            // Setup session timeout
            this.setupSessionTimeout();
            
            return data;
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        }
    }

    /**
     * Register new user
     */
    public async register(userData: FormData): Promise<LoginResponse> {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/register/`, {
                method: 'POST',
                body: userData, // FormData for file uploads
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Registration failed');
            }

            const data: LoginResponse = await response.json();
            
            // Save tokens and profile
            this.saveTokensToStorage({
                access: data.access,
                refresh: data.refresh
            });
            this.saveUserProfileToStorage(data.profile);
            
            // Setup session timeout
            this.setupSessionTimeout();
            
            return data;
        } catch (error) {
            console.error('Registration error:', error);
            throw error;
        }
    }

    /**
     * Refresh access token
     */
    public async refreshAccessToken(): Promise<boolean> {
        if (!this.refreshToken) {
            return false;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/auth/refresh/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ refresh: this.refreshToken }),
            });

            if (!response.ok) {
                return false;
            }

            const data = await response.json();
            this.accessToken = data.access;
            
            // Update stored tokens
            const tokens = localStorage.getItem('saku_tokens');
            if (tokens) {
                const parsedTokens: AuthTokens = JSON.parse(tokens);
                parsedTokens.access = data.access;
                localStorage.setItem('saku_tokens', JSON.stringify(parsedTokens));
            }
            
            return true;
        } catch (error) {
            console.error('Token refresh error:', error);
            return false;
        }
    }

    /**
     * Logout user
     */
    public async logout(): Promise<void> {
        try {
            if (this.refreshToken) {
                await fetch(`${API_BASE_URL}/auth/logout/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${this.accessToken}`,
                    },
                    body: JSON.stringify({ refresh: this.refreshToken }),
                });
            }
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            this.clearTokens();
        }
    }

    /**
     * Make authenticated API request
     */
    public async authenticatedRequest(url: string, options: RequestInit = {}): Promise<Response> {
        if (!this.isAuthenticated()) {
            throw new Error('User not authenticated');
        }

        // Add authorization header
        const headers = {
            ...options.headers,
            'Authorization': `Bearer ${this.accessToken}`,
        };

        let response = await fetch(url, {
            ...options,
            headers,
        });

        // If token expired, try to refresh
        if (response.status === 401) {
            const refreshed = await this.refreshAccessToken();
            if (refreshed) {
                // Retry request with new token
                headers['Authorization'] = `Bearer ${this.accessToken}`;
                response = await fetch(url, {
                    ...options,
                    headers,
                });
            } else {
                // Refresh failed, logout user
                this.logout();
                throw new Error('Session expired. Please login again.');
            }
        }

        return response;
    }

    /**
     * Get user profile from API
     */
    public async getUserProfile(): Promise<UserProfile> {
        const response = await this.authenticatedRequest(`${API_BASE_URL}/auth/profile/`);
        
        if (!response.ok) {
            throw new Error('Failed to get user profile');
        }

        const data = await response.json();
        this.saveUserProfileToStorage(data.profile);
        return data.profile;
    }

    /**
     * Update user profile
     */
    public async updateUserProfile(profileData: any): Promise<UserProfile> {
        const response = await this.authenticatedRequest(`${API_BASE_URL}/auth/profile/update/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(profileData),
        });

        if (!response.ok) {
            throw new Error('Failed to update user profile');
        }

        const data = await response.json();
        this.saveUserProfileToStorage(data.profile);
        return data.profile;
    }
}

// Create singleton instance
export const authService = new AuthService();

// Setup activity listeners to reset session timeout
document.addEventListener('click', () => authService.resetSessionTimeout());
document.addEventListener('keypress', () => authService.resetSessionTimeout());
document.addEventListener('scroll', () => authService.resetSessionTimeout());

export default authService;
