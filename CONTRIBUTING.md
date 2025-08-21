# Contributing to AI Chatbot Builder

Thank you for your interest in contributing to the AI Chatbot Builder project! This document provides guidelines for contributing while maintaining security best practices.

## 🔒 Security First

Before contributing, please ensure you understand our security practices:

1. **Never commit secrets** - All .env files are in .gitignore
2. **Use environment examples** - Copy from `env.example` files
3. **Validate inputs** - Always validate and sanitize user inputs
4. **Follow OWASP guidelines** - Review [OWASP Top 10](https://owasp.org/www-project-top-ten/)

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- Git
- Basic understanding of security best practices

### Setup Development Environment

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/chatbotgen.git
   cd chatbotgen
   ```

2. **Run the setup script**
   ```bash
   # On Unix-like systems
   ./setup.sh
   
   # On Windows
   setup.bat
   ```

3. **Configure environment variables**
   - Copy `backend/env.example` to `backend/.env`
   - Copy `frontend/env.example` to `frontend/.env.local`
   - Copy `widget/env.example` to `widget/.env`
   - Add your actual API keys and configuration

## 📝 Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Follow the existing code style
- Add tests for new functionality
- Update documentation as needed
- Ensure security best practices are followed

### 3. Test Your Changes

```bash
# Backend tests
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python -m pytest

# Frontend tests
cd frontend
npm test

# Widget tests
cd widget
npm test
```

### 4. Security Checklist

Before submitting your changes, ensure:

- [ ] No hardcoded secrets or API keys
- [ ] Input validation is implemented
- [ ] Error messages don't expose sensitive information
- [ ] CORS is properly configured
- [ ] Authentication is required where needed
- [ ] SQL injection is prevented
- [ ] XSS protection is in place

### 5. Commit Your Changes

```bash
git add .
git commit -m "feat: add your feature description"
```

Use conventional commit messages:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `style:` for formatting changes
- `refactor:` for code refactoring
- `test:` for adding tests
- `chore:` for maintenance tasks

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

## 🛡️ Security Guidelines for Contributors

### Code Security

1. **Input Validation**
   ```python
   # ✅ Good: Use Pydantic models
   from pydantic import BaseModel, validator
   
   class UserInput(BaseModel):
       email: str
       
       @validator('email')
       def validate_email(cls, v):
           if '@' not in v:
               raise ValueError('Invalid email format')
           return v
   ```

2. **SQL Injection Prevention**
   ```python
   # ✅ Good: Use parameterized queries
   result = supabase.table("users").select("*").eq("email", email).execute()
   
   # ❌ Bad: String concatenation
   query = f"SELECT * FROM users WHERE email = '{email}'"
   ```

3. **Error Handling**
   ```python
   # ✅ Good: Generic error messages
   try:
       # Your code
   except Exception as e:
       logger.error(f"Internal error: {e}")
       raise HTTPException(status_code=500, detail="Internal server error")
   ```

### Environment Security

1. **Never commit .env files**
   ```bash
   # ✅ Good: Use .env.example
   cp env.example .env
   
   # ❌ Bad: Don't commit actual .env files
   git add .env  # This should fail due to .gitignore
   ```

2. **Use strong secret keys**
   ```python
   # ✅ Good: Generate secure keys
   import secrets
   secret_key = secrets.token_urlsafe(32)
   ```

### API Security

1. **Authentication**
   ```python
   # ✅ Good: Require authentication
   @router.get("/protected")
   async def protected_route(current_user: User = Depends(get_current_user)):
       return {"message": "Protected data"}
   ```

2. **Rate Limiting**
   ```python
   # ✅ Good: Implement rate limiting
   from slowapi import Limiter, _rate_limit_exceeded_handler
   from slowapi.util import get_remote_address
   
   limiter = Limiter(key_func=get_remote_address)
   ```

## 🧪 Testing Guidelines

### Backend Testing

```python
# Example test with security focus
def test_user_registration_validation():
    """Test that user registration validates input properly"""
    with pytest.raises(ValueError, match="Invalid email"):
        UserCreate(
            email="invalid-email",
            password="password123",
            full_name="Test User"
        )
```

### Frontend Testing

```javascript
// Example test for input validation
test('should validate email format', () => {
  const { getByLabelText, getByText } = render(<RegistrationForm />);
  
  fireEvent.change(getByLabelText(/email/i), {
    target: { value: 'invalid-email' }
  });
  
  fireEvent.click(getByText(/register/i));
  
  expect(getByText(/invalid email format/i)).toBeInTheDocument();
});
```

## 📚 Documentation

When adding new features:

1. **Update README.md** if needed
2. **Add API documentation** for new endpoints
3. **Update security guidelines** if new security considerations arise
4. **Add inline comments** for complex security logic

## 🔍 Code Review Process

All contributions go through a security-focused review:

1. **Automated checks** - CI/CD pipeline runs security scans
2. **Manual review** - Maintainers review for security issues
3. **Testing** - Ensure tests pass and cover security scenarios
4. **Documentation** - Verify documentation is updated

## 🚨 Reporting Security Issues

If you discover a security vulnerability:

1. **DO NOT** create a public issue
2. **Email** the maintainers directly
3. **Include** detailed information about the vulnerability
4. **Wait** for acknowledgment before disclosing publicly

## 📋 Pull Request Template

When creating a pull request, use this template:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Security Checklist
- [ ] No hardcoded secrets
- [ ] Input validation implemented
- [ ] Error messages are generic
- [ ] Authentication required where needed
- [ ] Tests added for security scenarios

## Testing
- [ ] Backend tests pass
- [ ] Frontend tests pass
- [ ] Manual testing completed
- [ ] Security testing completed

## Documentation
- [ ] README updated if needed
- [ ] API docs updated if needed
- [ ] Security guidelines updated if needed
```

## 🎯 Areas for Contribution

We welcome contributions in these areas:

- **Security improvements** - Vulnerability fixes, security enhancements
- **Feature development** - New chatbot capabilities
- **Performance optimization** - Faster response times, better resource usage
- **Documentation** - Better guides, examples, tutorials
- **Testing** - More comprehensive test coverage
- **UI/UX improvements** - Better user experience

## 📞 Getting Help

If you need help:

1. Check the documentation
2. Search existing issues
3. Create a new issue with detailed information
4. Join our community discussions

Thank you for contributing to making AI Chatbot Builder more secure and better! 🚀 