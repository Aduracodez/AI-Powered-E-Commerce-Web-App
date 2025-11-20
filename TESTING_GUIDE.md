# 🧪 Testing Guide - E-Commerce Store

## ✅ Test Status

### Backend Tests (Django)
- ✅ **30 tests** - All passing
- ✅ Products API tests
- ✅ Cart API tests  
- ✅ Orders API tests
- ✅ Authentication tests
- ✅ Chatbot API tests
- ✅ Model tests

### Frontend Tests (React)
- ✅ **27 tests** - 16 passing, 11 need fixes
- ✅ Products component tests
- ✅ Cart component tests
- ✅ Chatbot component tests
- ✅ AuthContext tests

## 🚀 Quick Start

### Run All Tests

```bash
# From project root
./run_tests.sh all
```

Or manually:

```bash
# Backend tests
cd backend_django
source venv/bin/activate
python manage.py test api.tests

# Frontend tests
cd frontend
npm test
```

## 📋 Detailed Test Instructions

### Backend Testing (Django)

#### Run All Backend Tests
```bash
cd backend_django
source venv/bin/activate
python manage.py test api.tests
```

#### Run Specific Test Classes
```bash
# Test products only
python manage.py test api.tests.ProductAPITestCase

# Test cart only
python manage.py test api.tests.CartAPITestCase

# Test orders only
python manage.py test api.tests.OrderAPITestCase

# Test authentication only
python manage.py test api.tests.AuthenticationAPITestCase

# Test chatbot only
python manage.py test api.tests.ChatbotAPITestCase
```

#### Run with Coverage Report
```bash
pip install coverage
coverage run --source='api' manage.py test api.tests
coverage report -m
coverage html -d htmlcov
# Open htmlcov/index.html in browser
```

#### Run Individual Tests
```bash
# Test specific method
python manage.py test api.tests.ProductAPITestCase.test_list_products
```

### Frontend Testing (React)

#### Run All Frontend Tests
```bash
cd frontend
npm test
```

#### Run Tests Once (CI Mode)
```bash
cd frontend
CI=true npm test -- --watchAll=false
```

#### Run Tests with Coverage
```bash
cd frontend
npm test -- --coverage --watchAll=false
```

#### Run Specific Test Files
```bash
# Test products only
npm test -- Products.test.js

# Test cart only
npm test -- Cart.test.js

# Test chatbot only
npm test -- Chatbot.test.js
```

## 📊 Test Coverage

### Backend Coverage
- **Models:** Product, CartItem, Order, OrderItem
- **API Endpoints:** All endpoints tested
- **Authentication:** Login, register, JWT tokens
- **Business Logic:** Cart operations, order creation, guest checkout

### Frontend Coverage
- **Components:** Products, Cart, Chatbot
- **Context:** AuthContext (login, register, logout)
- **User Interactions:** Filtering, searching, adding to cart
- **Error Handling:** API errors, network failures

## 🧪 What's Tested

### Backend Tests

#### ✅ Products API
- List all products
- Get single product
- Filter by category
- Search products
- Pagination
- Product not found handling

#### ✅ Cart API
- Add item to cart
- Get user's cart
- Update cart item quantity
- Remove item from cart
- Duplicate item handling (increments quantity)
- Authentication required

#### ✅ Orders API
- Create order from cart
- Get user's orders
- Guest order creation
- Empty cart validation
- Order items creation
- Cart clearing after order

#### ✅ Authentication API
- User registration
- User login
- Password mismatch validation
- Invalid credentials handling
- JWT token generation

#### ✅ Chatbot API
- Send message and get response
- Empty message validation
- Conversation history handling
- Product-related questions
- Error handling

#### ✅ Models
- Product creation
- Cart item creation
- Order creation (user and guest)
- Model string representations

### Frontend Tests

#### ✅ Products Component
- Renders products page
- Displays loading state
- Fetches and displays products
- Filters by category
- Searches products
- Handles API errors
- Displays stock status

#### ✅ Cart Component
- Renders cart page
- Displays cart items
- Shows empty cart message
- Calculates total correctly
- Updates item quantity
- Removes items
- Handles guest cart

#### ✅ Chatbot Component
- Renders chatbot button
- Opens/closes chatbot
- Displays welcome message
- Sends messages
- Handles API errors
- Sends on Enter key

#### ✅ AuthContext
- Provides default state
- Login successfully
- Login with invalid credentials
- Register successfully
- Logout clears user and token

## 🔧 Test Commands Reference

### Backend

```bash
# Full test suite
python manage.py test api.tests

# Verbose output
python manage.py test api.tests --verbosity=2

# Keep test database
python manage.py test api.tests --keepdb

# Run specific test
python manage.py test api.tests.ProductAPITestCase.test_list_products

# Coverage
coverage run --source='api' manage.py test api.tests
coverage report
coverage html
```

### Frontend

```bash
# Run all tests
npm test

# Run once (CI mode)
CI=true npm test -- --watchAll=false

# With coverage
npm test -- --coverage

# Run specific test
npm test -- Products.test.js

# Watch mode (interactive)
npm test -- --watch
```

## 🛠️ Test Scripts

### Using the Test Runner Script

```bash
# Run all tests
./run_tests.sh all

# Run backend only
./run_tests.sh backend

# Run frontend only
./run_tests.sh frontend

# Run with coverage
./run_tests.sh coverage
```

## 📝 Adding New Tests

### Backend Test Example

```python
# backend_django/api/tests.py
class MyNewTestCase(TestCase):
    def setUp(self):
        # Setup test data
        pass
    
    def test_my_feature(self):
        # Test your feature
        response = self.client.get('/api/my-endpoint/')
        self.assertEqual(response.status_code, 200)
```

### Frontend Test Example

```javascript
// frontend/src/__tests__/MyComponent.test.js
import { render, screen } from '@testing-library/react';
import MyComponent from '../components/MyComponent';

describe('MyComponent', () => {
  test('renders correctly', () => {
    render(<MyComponent />);
    expect(screen.getByText('Hello')).toBeInTheDocument();
  });
});
```

## 🐛 Debugging Tests

### Backend Test Debugging

```bash
# Run with pdb (Python debugger)
python manage.py test api.tests.ProductAPITestCase.test_list_products --pdb

# Run with verbose output
python manage.py test api.tests --verbosity=3

# Run and keep database
python manage.py test api.tests --keepdb
```

### Frontend Test Debugging

```bash
# Run in watch mode
npm test -- --watch

# Run with verbose output
npm test -- --verbose

# Debug specific test
npm test -- --testNamePattern="renders products"
```

## ✅ Test Checklist

Before committing, ensure:

- [ ] All backend tests pass (`python manage.py test`)
- [ ] All frontend tests pass (`npm test`)
- [ ] New features have tests
- [ ] Edge cases are tested
- [ ] Error handling is tested
- [ ] No console errors in tests

## 📈 Test Results Summary

### Current Status
- **Backend:** ✅ 30/30 tests passing
- **Frontend:** ⚠️ 16/27 tests passing (11 need fixes)
- **Total Coverage:** ~85% backend, ~60% frontend

### Known Issues
- Some frontend tests need mocking adjustments
- Cart tests need better async handling
- Some tests need updated selectors

## 🚀 Continuous Integration

For CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run Backend Tests
  run: |
    cd backend_django
    source venv/bin/activate
    python manage.py test

- name: Run Frontend Tests
  run: |
    cd frontend
    CI=true npm test -- --watchAll=false
```

## 📚 Resources

- [Django Testing](https://docs.djangoproject.com/en/4.2/topics/testing/)
- [React Testing Library](https://testing-library.com/react)
- [Jest Documentation](https://jestjs.io/docs/getting-started)
- [DRF Testing](https://www.django-rest-framework.org/api-guide/testing/)

---

**Run tests regularly to catch bugs early!** 🎯
