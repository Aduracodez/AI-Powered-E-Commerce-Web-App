#!/bin/bash
# Comprehensive Test Runner for E-Commerce Store

echo "🧪 Running All Tests for E-Commerce Store"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test results
BACKEND_TESTS_PASSED=0
FRONTEND_TESTS_PASSED=0
TOTAL_TESTS=0

# Function to run backend tests
run_backend_tests() {
    echo -e "${YELLOW}📦 Running Backend Tests (Django)...${NC}"
    echo "-----------------------------------"
    
    cd backend_django || exit 1
    
    if [ ! -d "venv" ]; then
        echo "❌ Virtual environment not found. Creating..."
        python3 -m venv venv
    fi
    
    source venv/bin/activate
    
    echo "📥 Installing dependencies..."
    pip install -q -r requirements.txt
    
    echo "🧪 Running Django tests..."
    python manage.py test api.tests --verbosity=1
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Backend tests passed!${NC}"
        BACKEND_TESTS_PASSED=1
    else
        echo -e "${RED}❌ Backend tests failed!${NC}"
    fi
    
    cd ..
    echo ""
}

# Function to run backend tests with coverage
run_backend_tests_coverage() {
    echo -e "${YELLOW}📦 Running Backend Tests with Coverage...${NC}"
    echo "-----------------------------------"
    
    cd backend_django || exit 1
    
    if [ ! -d "venv" ]; then
        echo "❌ Virtual environment not found. Creating..."
        python3 -m venv venv
    fi
    
    source venv/bin/activate
    
    echo "📥 Installing dependencies..."
    pip install -q -r requirements.txt
    
    echo "🧪 Running Django tests with coverage..."
    coverage run --source='api' manage.py test api.tests
    coverage report -m
    coverage html -d htmlcov
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Backend coverage report generated in htmlcov/${NC}"
    else
        echo -e "${RED}❌ Coverage generation failed!${NC}"
    fi
    
    cd ..
    echo ""
}

# Function to run frontend tests
run_frontend_tests() {
    echo -e "${YELLOW}⚛️  Running Frontend Tests (React)...${NC}"
    echo "-----------------------------------"
    
    cd frontend || exit 1
    
    if [ ! -d "node_modules" ]; then
        echo "📥 Installing dependencies..."
        npm install --silent
    fi
    
    echo "🧪 Running React tests..."
    CI=true npm test -- --watchAll=false --passWithNoTests --no-coverage
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Frontend tests passed!${NC}"
        FRONTEND_TESTS_PASSED=1
    else
        echo -e "${RED}❌ Frontend tests failed!${NC}"
    fi
    
    cd ..
    echo ""
}

# Function to run frontend tests with coverage
run_frontend_tests_coverage() {
    echo -e "${YELLOW}⚛️  Running Frontend Tests with Coverage...${NC}"
    echo "-----------------------------------"
    
    cd frontend || exit 1
    
    if [ ! -d "node_modules" ]; then
        echo "📥 Installing dependencies..."
        npm install --silent
    fi
    
    echo "🧪 Running React tests with coverage..."
    CI=true npm test -- --watchAll=false --passWithNoTests --coverage
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Frontend coverage report generated in coverage/${NC}"
    else
        echo -e "${RED}❌ Coverage generation failed!${NC}"
    fi
    
    cd ..
    echo ""
}

# Main menu
case "$1" in
    backend)
        run_backend_tests
        ;;
    frontend)
        run_frontend_tests
        ;;
    coverage)
        run_backend_tests_coverage
        run_frontend_tests_coverage
        ;;
    all)
        run_backend_tests
        run_frontend_tests
        
        echo "=========================================="
        if [ $BACKEND_TESTS_PASSED -eq 1 ] && [ $FRONTEND_TESTS_PASSED -eq 1 ]; then
            echo -e "${GREEN}✅ All tests passed!${NC}"
            exit 0
        else
            echo -e "${RED}❌ Some tests failed!${NC}"
            exit 1
        fi
        ;;
    *)
        echo "Usage: ./run_tests.sh [backend|frontend|coverage|all]"
        echo ""
        echo "Options:"
        echo "  backend   - Run only backend tests"
        echo "  frontend  - Run only frontend tests"
        echo "  coverage  - Run all tests with coverage reports"
        echo "  all       - Run all tests (default)"
        echo ""
        echo "Running all tests..."
        run_backend_tests
        run_frontend_tests
        ;;
esac
