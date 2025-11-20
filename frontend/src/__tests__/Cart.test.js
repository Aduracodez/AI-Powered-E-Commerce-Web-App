import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Cart from '../pages/Cart';
import { AuthContext } from '../context/AuthContext';

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

const mockUser = {
  id: 1,
  username: 'testuser',
  email: 'test@example.com'
};

const AuthProvider = ({ children, user = null }) => (
  <AuthContext.Provider value={{ user, login: jest.fn(), register: jest.fn(), logout: jest.fn(), loading: false }}>
    {children}
  </AuthContext.Provider>
);

const Wrapper = ({ children, user = null }) => (
  <BrowserRouter>
    <AuthProvider user={user}>
      {children}
    </AuthProvider>
  </BrowserRouter>
);

describe('Cart Component', () => {
  const mockCartItems = [
    {
      id: 1,
      quantity: 2,
      product: {
        id: 1,
        name: 'Test Product 1',
        price: 99.99,
        stock: 10,
        image_url: 'https://example.com/image1.jpg'
      }
    },
    {
      id: 2,
      quantity: 1,
      product: {
        id: 2,
        name: 'Test Product 2',
        price: 49.99,
        stock: 5,
        image_url: 'https://example.com/image2.jpg'
      }
    }
  ];

  beforeEach(() => {
    // Reset all mocks
    jest.clearAllMocks();
    // Setup axios mocks
    axios.get.mockResolvedValue({ data: mockCartItems });
    axios.put.mockResolvedValue({ data: {} });
    axios.delete.mockResolvedValue({ data: {} });
    axios.post.mockResolvedValue({ data: {} });
    
    // Mock localStorage
    Storage.prototype.getItem = jest.fn(() => null);
    Storage.prototype.setItem = jest.fn();
    Storage.prototype.removeItem = jest.fn();
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  test('renders cart page for authenticated user', async () => {
    render(
      <Wrapper user={mockUser}>
        <Cart />
      </Wrapper>
    );

    await waitFor(() => {
      expect(screen.getByText('Shopping Cart')).toBeInTheDocument();
    });
  });

  test('displays cart items for authenticated user', async () => {
    render(
      <Wrapper user={mockUser}>
        <Cart />
      </Wrapper>
    );

    await waitFor(() => {
      expect(screen.getByText('Test Product 1')).toBeInTheDocument();
      expect(screen.getByText('Test Product 2')).toBeInTheDocument();
    });
  });

  test('displays empty cart message', async () => {
    axios.get.mockResolvedValue({ data: [] });

    render(
      <Wrapper user={mockUser}>
        <Cart />
      </Wrapper>
    );

    await waitFor(() => {
      expect(screen.getByText('Your cart is empty')).toBeInTheDocument();
    });
  });

  test('calculates total correctly', async () => {
    render(
      <Wrapper user={mockUser}>
        <Cart />
      </Wrapper>
    );

    await waitFor(() => {
      expect(screen.getByText('Test Product 1')).toBeInTheDocument();
    });

    // Total should be: (99.99 * 2) + (49.99 * 1) = 249.97
    await waitFor(() => {
      const totalElements = screen.getAllByText(/€249.97/);
      expect(totalElements.length).toBeGreaterThan(0);
    }, { timeout: 3000 });
  });

  test('updates item quantity', async () => {
    axios.put.mockResolvedValue({ data: { ...mockCartItems[0], quantity: 3 } });

    render(
      <Wrapper user={mockUser}>
        <Cart />
      </Wrapper>
    );

    await waitFor(() => {
      expect(screen.getByText('Test Product 1')).toBeInTheDocument();
    });

    const increaseButtons = screen.getAllByText('+');
    fireEvent.click(increaseButtons[0]);

    await waitFor(() => {
      expect(axios.put).toHaveBeenCalled();
    });
  });

  test('removes item from cart', async () => {
    axios.delete.mockResolvedValue({});
    axios.get.mockResolvedValueOnce({ data: mockCartItems })
           .mockResolvedValueOnce({ data: [] });

    render(
      <Wrapper user={mockUser}>
        <Cart />
      </Wrapper>
    );

    await waitFor(() => {
      expect(screen.getByText('Test Product 1')).toBeInTheDocument();
    });

    const removeButtons = screen.getAllByText('×');
    if (removeButtons.length > 0) {
      fireEvent.click(removeButtons[0]);

      await waitFor(() => {
        expect(axios.delete).toHaveBeenCalled();
      });
    }
  });

  test('handles guest cart', async () => {
    // Mock localStorage for guest cart
    const guestCart = [
      {
        product_id: 1,
        quantity: 2,
        product: {
          id: 1,
          name: 'Guest Product',
          price: 99.99,
          stock: 10,
          image_url: 'https://example.com/image.jpg'
        }
      }
    ];

    Storage.prototype.getItem = jest.fn(() => JSON.stringify(guestCart));

    render(
      <Wrapper user={null}>
        <Cart />
      </Wrapper>
    );

    await waitFor(() => {
      expect(screen.getByText('Guest Product')).toBeInTheDocument();
    });
  });
});

