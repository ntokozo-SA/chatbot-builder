#!/bin/bash

# AI Chatbot Builder Setup Script
# This script helps set up the project with proper security practices

set -e  # Exit on any error

echo "🚀 AI Chatbot Builder Setup"
echo "=========================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on Windows
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    print_warning "This script is designed for Unix-like systems. Please use the Windows setup instructions in the README."
    exit 1
fi

# Check prerequisites
print_status "Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8+ and try again."
    exit 1
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 16+ and try again."
    exit 1
fi

# Check npm
if ! command -v npm &> /dev/null; then
    print_error "npm is not installed. Please install npm and try again."
    exit 1
fi

print_success "Prerequisites check passed!"

# Generate secure secret key
print_status "Generating secure secret key..."
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")

# Backend setup
print_status "Setting up backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    print_status "Creating .env file from template..."
    cp env.example .env
    
    # Replace placeholder secret key
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/your-secret-key-here/$SECRET_KEY/g" .env
    else
        # Linux
        sed -i "s/your-secret-key-here/$SECRET_KEY/g" .env
    fi
    
    print_warning "Please edit backend/.env with your actual API keys and configuration."
else
    print_warning "backend/.env already exists. Please ensure it contains your actual API keys."
fi

deactivate
cd ..

# Frontend setup
print_status "Setting up frontend..."
cd frontend

# Install dependencies
print_status "Installing Node.js dependencies..."
npm install

# Create .env.local file if it doesn't exist
if [ ! -f ".env.local" ]; then
    print_status "Creating .env.local file from template..."
    cp env.example .env.local
    print_warning "Please edit frontend/.env.local with your backend URL."
else
    print_warning "frontend/.env.local already exists. Please ensure it contains your backend URL."
fi

cd ..

# Widget setup
print_status "Setting up widget..."
cd widget

# Install dependencies
print_status "Installing widget dependencies..."
npm install

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    print_status "Creating widget .env file from template..."
    cp env.example .env
    print_warning "Please edit widget/.env with your backend URL."
else
    print_warning "widget/.env already exists. Please ensure it contains your backend URL."
fi

cd ..

print_success "Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Edit the environment files with your actual API keys:"
echo "   - backend/.env"
echo "   - frontend/.env.local"
echo "   - widget/.env"
echo ""
echo "2. Set up your database:"
echo "   - Go to your Supabase dashboard"
echo "   - Run the migration files in backend/migrations/"
echo ""
echo "3. Start the application:"
echo "   - Backend: cd backend && source venv/bin/activate && python -m uvicorn app.main:app --reload"
echo "   - Frontend: cd frontend && npm run dev"
echo "   - Widget: cd widget && npm run dev"
echo ""
echo "🔒 Security reminder:"
echo "- Never commit .env files (they're already in .gitignore)"
echo "- Rotate your API keys regularly"
echo "- Use HTTPS in production"
echo "- Enable Row Level Security in Supabase"
echo ""
echo "📚 For more information, see:"
echo "- README.md for detailed setup instructions"
echo "- SECURITY.md for security best practices" 