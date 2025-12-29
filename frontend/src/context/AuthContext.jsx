import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from '../services/api';

const AuthContext = createContext(null);

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

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem('token');
    const userId = localStorage.getItem('userId');
    if (token && userId) {
      setUser({ userId, token });
    }
    setLoading(false);
  }, []);

  const login = async (username, password) => {
    try {
      // Development mode: Allow bypassing auth if backend is not available
      const DEV_MODE = import.meta.env.VITE_DEV_MODE === 'true';
      
      if (DEV_MODE) {
        // Mock authentication for development
        const mockToken = 'dev-token-' + Date.now();
        const mockUserId = 'dev-user-' + username;
        localStorage.setItem('token', mockToken);
        localStorage.setItem('userId', mockUserId);
        setUser({ userId: mockUserId, token: mockToken });
        return { success: true };
      }
      
      const data = await authAPI.login(username, password);
      const userId = data.userId || data.user_id || localStorage.getItem('userId');
      setUser({ userId, token: data.token });
      return { success: true };
    } catch (error) {
      // In development, if backend is down, allow mock login
      const DEV_MODE = import.meta.env.VITE_DEV_MODE === 'true';
      if (DEV_MODE && (!error.response || error.code === 'ERR_NETWORK')) {
        const mockToken = 'dev-token-' + Date.now();
        const mockUserId = 'dev-user-' + username;
        localStorage.setItem('token', mockToken);
        localStorage.setItem('userId', mockUserId);
        setUser({ userId: mockUserId, token: mockToken });
        return { success: true };
      }
      
      return {
        success: false,
        error: error.response?.data?.message || 'Login failed. Please try again.',
      };
    }
  };

  const signup = async (username, password) => {
    try {
      // Development mode: Allow bypassing auth if backend is not available
      const DEV_MODE = import.meta.env.VITE_DEV_MODE === 'true';
      
      if (DEV_MODE) {
        // Mock authentication for development
        const mockToken = 'dev-token-' + Date.now();
        const mockUserId = 'dev-user-' + username;
        localStorage.setItem('token', mockToken);
        localStorage.setItem('userId', mockUserId);
        setUser({ userId: mockUserId, token: mockToken });
        return { success: true };
      }
      
      const data = await authAPI.signup(username, password);
      const userId = data.userId || data.user_id || localStorage.getItem('userId');
      setUser({ userId, token: data.token });
      return { success: true };
    } catch (error) {
      // In development, if backend is down, allow mock login
      const DEV_MODE = import.meta.env.VITE_DEV_MODE === 'true';
      if (DEV_MODE && (!error.response || error.code === 'ERR_NETWORK')) {
        const mockToken = 'dev-token-' + Date.now();
        const mockUserId = 'dev-user-' + username;
        localStorage.setItem('token', mockToken);
        localStorage.setItem('userId', mockUserId);
        setUser({ userId: mockUserId, token: mockToken });
        return { success: true };
      }
      
      return {
        success: false,
        error: error.response?.data?.message || 'Signup failed. Please try again.',
      };
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userId');
    setUser(null);
  };

  const value = {
    user,
    login,
    signup,
    logout,
    loading,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
