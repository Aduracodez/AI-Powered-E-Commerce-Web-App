// API Configuration
// This file centralizes API URL configuration for easy deployment

export const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// For debugging in development
if (process.env.NODE_ENV === 'development') {
  console.log('API URL:', API_URL);
}

