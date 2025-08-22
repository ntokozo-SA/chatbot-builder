# GitHub Setup Guide

This guide will help you set up the AI Chatbot Builder project for development and contribution.

## 🚀 Quick Setup for Contributors

### 1. Fork and Clone

```bash
# Fork the repository on GitHub first, then:
git clone https://github.com/YOUR_USERNAME/chatbotgen.git
cd chatbotgen
```

### 2. Environment Setup

#### Backend Environment
```bash
cd backend
cp env.example .env
```

**Important**: Edit `.env` with your actual API keys:
- Get Supabase keys from [Supabase Dashboard](https://app.supabase.com)
- Get HuggingFace API key from [HuggingFace Settings](https://huggingface.co/settings/tokens)
- Get Qdrant keys from [Qdrant Cloud](https://cloud.qdrant.io)
- Generate a secret key: `python -c "import secrets; print(secrets.token_urlsafe(32))"`

#### Frontend Environment
```bash
cd frontend
cp env.example .env.local
```

Edit `.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### Widget Environment
```bash
cd widget
cp env.example .env
```

Edit `.env`:
```bash
VITE_BACKEND_URL=http://localhost:8000
```

### 3. Install Dependencies

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install

# Widget
cd widget
npm install
```

### 4. Database Setup

1. Create a Supabase project at [supabase.com](https://supabase.com)
2. Go to SQL Editor in your Supabase dashboard
3. Run the migration files in order:
   ```sql
   -- Run these in your Supabase SQL Editor:
   -- 1. backend/migrations/001_create_users_table.sql
   -- 2. backend/migrations/002_create_websites_table.sql
   -- 3. backend/migrations/003_create_conversations_table.sql
   ```

### 5. Start Development Servers

```bash
# Terminal 1: Backend
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Widget (optional)
cd widget
npm run dev
```

## 🔐 Security Checklist

Before pushing to GitHub, ensure:

- [ ] `.env` files are in `.gitignore` (already configured)
- [ ] No hardcoded API keys in source code
- [ ] All sensitive data uses environment variables
- [ ] Database migrations don't contain sensitive data
- [ ] Test files don't contain real credentials

## 🧪 Testing Your Setup

### Backend Tests
```bash
cd backend
python test_supabase_connection.py
python test_registration.py
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📝 Making Changes

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes

3. Test your changes:
   ```bash
   # Backend
   cd backend
   python -m pytest
   
   # Frontend
   cd frontend
   npm test
   ```

4. Commit with descriptive messages:
   ```bash
   git add .
   git commit -m "feat: add new chatbot feature"
   ```

5. Push and create a Pull Request:
   ```bash
   git push origin feature/your-feature-name
   ```

## 🐛 Troubleshooting

### Common Issues

1. **Module not found errors**: Ensure you're in the correct directory and dependencies are installed
2. **Environment variable errors**: Check that `.env` files exist and contain valid values
3. **Database connection errors**: Verify Supabase credentials and database setup
4. **CORS errors**: Check `ALLOWED_ORIGINS` in backend `.env`

### Getting Help

1. Check existing issues on GitHub
2. Create a new issue with:
   - Your operating system
   - Python/Node.js versions
   - Error messages
   - Steps to reproduce

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Supabase Documentation](https://supabase.com/docs)
- [HuggingFace Documentation](https://huggingface.co/docs)

## 🤝 Contributing Guidelines

1. **Code Style**: Follow existing patterns in the codebase
2. **Documentation**: Update README.md if adding new features
3. **Testing**: Add tests for new functionality
4. **Security**: Never commit sensitive information
5. **Commits**: Use conventional commit messages

## 🔄 Keeping Updated

```bash
# Update your fork
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

---

**Remember**: Never commit your `.env` files or any files containing real API keys! 