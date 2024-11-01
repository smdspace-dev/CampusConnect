import React, { createContext, useState, useContext, useEffect } from 'react';
import jwtDecode from 'jwt-decode';
import apiClient from '../api/apiClient';
import { toast } from 'react-toastify';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Initialize auth state from localStorage
  useEffect(() => {
    const initializeAuth = () => {
      const token = localStorage.getItem('access_token');
      if (token) {
        try {
          const decodedToken = jwtDecode(token);
          const currentTime = Date.now() / 1000;
          
          if (decodedToken.exp > currentTime) {
            // Token is valid
            setUser({
              id: decodedToken.user_id,
              username: decodedToken.username || 'Unknown',
              email: decodedToken.email || '',
              role: decodedToken.role || 'student',
              first_name: decodedToken.first_name || '',
              last_name: decodedToken.last_name || ''
            });
            setIsAuthenticated(true);
            apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
          } else {
            // Token is expired
            logout();
          }
        } catch (error) {
          console.error('Invalid token:', error);
          logout();
        }
      }
      setLoading(false);
    };

    initializeAuth();
  }, []);

  const login = async (credentials) => {
    try {
      setLoading(true);
      const response = await apiClient.post('/auth/login/', credentials);
      const { access, refresh, user: userData } = response.data;

      // Store tokens
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);

      // Set auth headers
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${access}`;

      // Decode token to get user info
      const decodedToken = jwtDecode(access);
      const userInfo = {
        id: userData.id || decodedToken.user_id,
        username: userData.username || decodedToken.username,
        email: userData.email || decodedToken.email || '',
        role: userData.role || decodedToken.role || 'student',
        first_name: userData.first_name || decodedToken.first_name || '',
        last_name: userData.last_name || decodedToken.last_name || ''
      };

      setUser(userInfo);
      setIsAuthenticated(true);
      toast.success(`Welcome back, ${userInfo.first_name || userInfo.username}!`);
      
      return { success: true, user: userInfo };
    } catch (error) {
      console.error('Login error:', error);
      const message = error.response?.data?.detail || 
                     error.response?.data?.message || 
                     'Login failed. Please check your credentials.';
      toast.error(message);
      return { success: false, error: message };
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    delete apiClient.defaults.headers.common['Authorization'];
    setUser(null);
    setIsAuthenticated(false);
    toast.info('You have been logged out.');
  };

  const refreshToken = async () => {
    try {
      const refresh = localStorage.getItem('refresh_token');
      if (!refresh) {
        throw new Error('No refresh token available');
      }

      const response = await apiClient.post('/auth/token/refresh/', {
        refresh: refresh
      });

      const { access } = response.data;
      localStorage.setItem('access_token', access);
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${access}`;

      return access;
    } catch (error) {
      console.error('Token refresh failed:', error);
      logout();
      throw error;
    }
  };

  const hasRole = (allowedRoles) => {
    if (!user || !allowedRoles) return false;
    if (Array.isArray(allowedRoles)) {
      return allowedRoles.includes(user.role);
    }
    return user.role === allowedRoles;
  };

  const value = {
    user,
    loading,
    isAuthenticated,
    login,
    logout,
    refreshToken,
    hasRole
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
