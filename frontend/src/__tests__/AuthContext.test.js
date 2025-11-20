import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { renderHook, act } from '@testing-library/react';
import { AuthContext, AuthProvider } from '../context/AuthContext';

// Mock axios before importing
jest.mock('axios', () => ({
  get: jest.fn(),
  post: jest.fn(),
  put: jest.fn(),
  delete: jest.fn(),
  defaults: {
    headers: {
      common: {}
    }
  }
}));

import axios from 'axios';

describe('AuthContext', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    localStorage.clear();
  });

  test('provides default auth state', () => {
    const { result } = renderHook(() => {
      const context = React.useContext(AuthContext);
      return context;
    }, {
      wrapper: ({ children }) => <AuthProvider>{children}</AuthProvider>
    });

    expect(result.current.user).toBeNull();
    expect(typeof result.current.login).toBe('function');
    expect(typeof result.current.register).toBe('function');
    expect(typeof result.current.logout).toBe('function');
  });

  test('login successfully', async () => {
    const mockResponse = {
      data: {
        access_token: 'mock-token',
        user: {
          id: 1,
          username: 'testuser',
          email: 'test@example.com'
        }
      }
    };

    axios.post.mockResolvedValue(mockResponse);

    const { result } = renderHook(() => {
      return React.useContext(AuthContext);
    }, {
      wrapper: ({ children }) => <AuthProvider>{children}</AuthProvider>
    });

    await act(async () => {
      const response = await result.current.login('testuser', 'password123');
      expect(response.success).toBe(true);
    });

    expect(result.current.user).toEqual(mockResponse.data.user);
    expect(localStorage.getItem).toHaveBeenCalled();
  });

  test('login with invalid credentials', async () => {
    axios.post.mockRejectedValue({
      response: {
        data: { error: 'Invalid credentials' }
      }
    });

    const { result } = renderHook(() => {
      return React.useContext(AuthContext);
    }, {
      wrapper: ({ children }) => <AuthProvider>{children}</AuthProvider>
    });

    await act(async () => {
      const response = await result.current.login('testuser', 'wrongpassword');
      expect(response.success).toBe(false);
    });

    expect(result.current.user).toBeNull();
  });

  test('register successfully', async () => {
    const mockResponse = {
      data: {
        access_token: 'mock-token',
        user: {
          id: 1,
          username: 'newuser',
          email: 'newuser@example.com'
        }
      }
    };

    axios.post.mockResolvedValue(mockResponse);

    const { result } = renderHook(() => {
      return React.useContext(AuthContext);
    }, {
      wrapper: ({ children }) => <AuthProvider>{children}</AuthProvider>
    });

    await act(async () => {
      const response = await result.current.register('newuser', 'newuser@example.com', 'password123');
      expect(response.success).toBe(true);
    });

    expect(result.current.user).toEqual(mockResponse.data.user);
  });

  test('logout clears user and token', () => {
    localStorage.setItem('token', 'mock-token');

    const { result } = renderHook(() => {
      return React.useContext(AuthContext);
    }, {
      wrapper: ({ children }) => <AuthProvider>{children}</AuthProvider>
    });

    act(() => {
      result.current.logout();
    });

    expect(result.current.user).toBeNull();
    expect(localStorage.removeItem).toHaveBeenCalledWith('token');
  });
});

