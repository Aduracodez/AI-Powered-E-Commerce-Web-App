import React from 'react';
import { render, screen, waitFor, fireEvent, act } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Products from '../pages/Products';

// Mock axios before importing
jest.mock('axios', () => ({
  get: jest.fn(() => Promise.resolve({ data: { count: 0, results: [] } })),
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

// Wrapper component for router
const Wrapper = ({ children }) => <BrowserRouter>{children}</BrowserRouter>;

describe('Products Component', () => {
  const mockProducts = {
    data: {
      count: 2,
      results: [
        {
          id: 1,
          name: 'Test Product 1',
          description: 'Test description 1',
          price: 99.99,
          stock: 10,
          category: 'Electronics',
          image_url: 'https://example.com/image1.jpg'
        },
        {
          id: 2,
          name: 'Test Product 2',
          description: 'Test description 2',
          price: 49.99,
          stock: 5,
          category: 'Fashion',
          image_url: 'https://example.com/image2.jpg'
        }
      ]
    }
  };

  beforeEach(() => {
    jest.clearAllMocks();
    axios.get.mockResolvedValue(mockProducts);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  test('renders products page', async () => {
    render(
      <Wrapper>
        <Products />
      </Wrapper>
    );

    expect(screen.getByText('Our Products')).toBeInTheDocument();
    
    // Wait for products to load
    await waitFor(() => {
      expect(screen.queryByText('Loading products...')).not.toBeInTheDocument();
    }, { timeout: 3000 });
    
    await waitFor(() => {
      expect(screen.getByText('Test Product 1')).toBeInTheDocument();
    }, { timeout: 3000 });
  });

  test('displays loading state', () => {
    axios.get.mockImplementation(() => new Promise(() => {})); // Never resolves
    
    render(
      <Wrapper>
        <Products />
      </Wrapper>
    );

    expect(screen.getByText('Loading products...')).toBeInTheDocument();
  });

  test('fetches and displays products', async () => {
    axios.get.mockResolvedValue(mockProducts);
    
    render(
      <Wrapper>
        <Products />
      </Wrapper>
    );

    await waitFor(() => {
      expect(axios.get).toHaveBeenCalledWith(
        'http://localhost:8000/api/products/',
        expect.any(Object)
      );
    });

    await waitFor(() => {
      expect(screen.getByText('Test Product 1')).toBeInTheDocument();
    }, { timeout: 3000 });

    expect(screen.getByText('Test Product 2')).toBeInTheDocument();
    expect(screen.getByText('€99.99')).toBeInTheDocument();
    expect(screen.getByText('€49.99')).toBeInTheDocument();
  });

  test('displays no products message when empty', async () => {
    axios.get.mockResolvedValue({
      data: {
        count: 0,
        results: []
      }
    });

    render(
      <Wrapper>
        <Products />
      </Wrapper>
    );

    await waitFor(() => {
      expect(screen.getByText('No products found')).toBeInTheDocument();
    });
  });

  test('filters products by category', async () => {
    const filteredProducts = {
      data: {
        count: 1,
        results: [mockProducts.data.results[0]]
      }
    };

    axios.get.mockResolvedValueOnce(mockProducts);
    
    render(
      <Wrapper>
        <Products />
      </Wrapper>
    );

    // Wait for initial products to load
    await waitFor(() => {
      expect(screen.queryByText('Loading products...')).not.toBeInTheDocument();
    }, { timeout: 3000 });
    
    await waitFor(() => {
      expect(screen.getByText('Test Product 1')).toBeInTheDocument();
    }, { timeout: 3000 });

    // Mock filtered response
    axios.get.mockResolvedValueOnce(filteredProducts);

    const electronicsButton = screen.getByText('Electronics');
    fireEvent.click(electronicsButton);

    await waitFor(() => {
      expect(axios.get).toHaveBeenLastCalledWith(
        'http://localhost:8000/api/products/',
        { params: { category: 'Electronics' } }
      );
    }, { timeout: 3000 });
  });

  test('searches products', async () => {
    render(
      <Wrapper>
        <Products />
      </Wrapper>
    );

    // Wait for initial products to load
    await waitFor(() => {
      expect(screen.queryByText('Loading products...')).not.toBeInTheDocument();
    }, { timeout: 3000 });
    
    await waitFor(() => {
      expect(screen.getByText('Test Product 1')).toBeInTheDocument();
    }, { timeout: 3000 });

    const searchInput = screen.getByPlaceholderText('Search products...');
    fireEvent.change(searchInput, { target: { value: 'Test Product 1' } });

    // Wait for debounced search to trigger
    await waitFor(() => {
      expect(axios.get).toHaveBeenLastCalledWith(
        'http://localhost:8000/api/products/',
        { params: { search: 'Test Product 1' } }
      );
    }, { timeout: 3000 });
  });

  test('handles API error', async () => {
    const consoleError = jest.spyOn(console, 'error').mockImplementation(() => {});
    
    axios.get.mockRejectedValue({
      code: 'ECONNREFUSED',
      message: 'Connection refused'
    });

    render(
      <Wrapper>
        <Products />
      </Wrapper>
    );

    await waitFor(() => {
      expect(screen.getByText('No products found')).toBeInTheDocument();
    });

    consoleError.mockRestore();
  });

  test('displays product stock status', async () => {
    render(
      <Wrapper>
        <Products />
      </Wrapper>
    );

    // Wait for products to load
    await waitFor(() => {
      expect(screen.queryByText('Loading products...')).not.toBeInTheDocument();
    }, { timeout: 3000 });

    await waitFor(() => {
      const inStockElements = screen.getAllByText('In Stock');
      expect(inStockElements.length).toBeGreaterThan(0);
    }, { timeout: 3000 });
  });
});

