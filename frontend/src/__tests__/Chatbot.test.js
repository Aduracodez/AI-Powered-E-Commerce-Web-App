import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Chatbot from '../components/Chatbot';
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

const Wrapper = ({ children }) => <BrowserRouter>{children}</BrowserRouter>;

describe('Chatbot Component', () => {
  beforeEach(() => {
    axios.post.mockResolvedValue({
      data: {
        response: 'Hello! How can I help you?'
      }
    });
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  test('renders chatbot button', () => {
    render(
      <Wrapper>
        <Chatbot />
      </Wrapper>
    );

    const button = screen.getByLabelText('Toggle chatbot');
    expect(button).toBeInTheDocument();
  });

  test('opens chatbot on button click', () => {
    render(
      <Wrapper>
        <Chatbot />
      </Wrapper>
    );

    const button = screen.getByLabelText('Toggle chatbot');
    fireEvent.click(button);

    expect(screen.getByText('Shopping Assistant')).toBeInTheDocument();
    expect(screen.getByText("We're here to help!")).toBeInTheDocument();
  });

  test('displays welcome message', () => {
    render(
      <Wrapper>
        <Chatbot />
      </Wrapper>
    );

    const button = screen.getByLabelText('Toggle chatbot');
    fireEvent.click(button);

    expect(screen.getByText(/Hello! 👋 I'm your shopping assistant/)).toBeInTheDocument();
  });

  test('sends message and receives response', async () => {
    render(
      <Wrapper>
        <Chatbot />
      </Wrapper>
    );

    const button = screen.getByLabelText('Toggle chatbot');
    fireEvent.click(button);

    const input = screen.getByPlaceholderText('Type your message...');
    const sendButton = screen.getByRole('button', { name: /➤/ });

    fireEvent.change(input, { target: { value: 'Hello' } });
    fireEvent.click(sendButton);

    await waitFor(() => {
      expect(axios.post).toHaveBeenCalledWith(
        'http://localhost:8000/api/chatbot/',
        expect.objectContaining({
          message: 'Hello',
          history: expect.any(Array)
        })
      );
    });

    await waitFor(() => {
      expect(screen.getByText('Hello')).toBeInTheDocument(); // User message
    });
  });

  test('handles API error gracefully', async () => {
    axios.post.mockRejectedValue({
      message: 'Network error'
    });

    render(
      <Wrapper>
        <Chatbot />
      </Wrapper>
    );

    const button = screen.getByLabelText('Toggle chatbot');
    fireEvent.click(button);

    const input = screen.getByPlaceholderText('Type your message...');
    const sendButton = screen.getByRole('button', { name: /➤/ });

    fireEvent.change(input, { target: { value: 'Hello' } });
    fireEvent.click(sendButton);

    await waitFor(() => {
      expect(screen.getByText(/Sorry, I'm having trouble connecting/)).toBeInTheDocument();
    });
  });

  test('sends message on Enter key', async () => {
    render(
      <Wrapper>
        <Chatbot />
      </Wrapper>
    );

    const button = screen.getByLabelText('Toggle chatbot');
    fireEvent.click(button);

    const input = screen.getByPlaceholderText('Type your message...');

    fireEvent.change(input, { target: { value: 'Test message' } });
    fireEvent.keyPress(input, { key: 'Enter', code: 'Enter' });

    await waitFor(() => {
      expect(axios.post).toHaveBeenCalled();
    });
  });

  test('closes chatbot on close button click', () => {
    render(
      <Wrapper>
        <Chatbot />
      </Wrapper>
    );

    const toggleButton = screen.getByLabelText('Toggle chatbot');
    fireEvent.click(toggleButton);

    expect(screen.getByText('Shopping Assistant')).toBeInTheDocument();

    const closeButton = screen.getByLabelText('Close chatbot');
    fireEvent.click(closeButton);

    expect(screen.queryByText('Shopping Assistant')).not.toBeInTheDocument();
  });
});

