# Security Guidelines

This document outlines security best practices for the AI Chatbot Builder project.

## 🔐 Environment Security

### ✅ Required Actions

- [ ] **Never commit .env files** - All .env files are in .gitignore
- [ ] **Use strong secret keys** - Generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- [ ] **Rotate API keys regularly** - Update keys every 90 days
- [ ] **Use different keys per environment** - Dev, staging, and production should have separate keys

### 🔑 API Key Management

#### Supabase Keys
- **SUPABASE_URL**: Your project URL (safe to share)
- **SUPABASE_ANON_KEY**: Public key (safe for frontend)
- **SUPABASE_SERVICE_ROLE_KEY**: Private key (backend only, never expose)

#### HuggingFace Keys
- **HUGGINGFACE_API_KEY**: Private key (backend only)
- Get from: https://huggingface.co/settings/tokens

#### Qdrant Keys
- **QDRANT_URL**: Your cluster URL
- **QDRANT_API_KEY**: Private key (backend only)

#### Application Keys
- **SECRET_KEY**: JWT signing key (backend only)
- **ALGORITHM**: Use HS256 (default)

## 🌐 Network Security

### CORS Configuration
```python
# Configure ALLOWED_ORIGINS for your domains
ALLOWED_ORIGINS=[
    "https://yourdomain.com",
    "https://www.yourdomain.com"
]
```

### HTTPS Requirements
- ✅ Always use HTTPS in production
- ✅ Redirect HTTP to HTTPS
- ✅ Use secure cookies
- ✅ Enable HSTS headers

## 🗄️ Database Security

### Supabase Security
- [ ] **Enable Row Level Security (RLS)** on all tables
- [ ] **Create proper RLS policies** for each table
- [ ] **Use service role key** only for admin operations
- [ ] **Use anon key** for public operations

### Example RLS Policy
```sql
-- Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Policy for users to see only their own data
CREATE POLICY "Users can view own data" ON users
    FOR SELECT USING (auth.uid() = id);
```

## 🔒 Authentication Security

### Password Requirements
- Minimum 6 characters
- Must contain letters and numbers
- Stored as bcrypt hash

### JWT Token Security
- Tokens expire after 30 minutes (configurable)
- Use strong SECRET_KEY
- Validate token on every request

### Session Management
- Clear tokens on logout
- Implement token refresh
- Monitor for suspicious activity

## 🛡️ API Security

### Rate Limiting
- Implement rate limiting on auth endpoints
- Monitor for brute force attempts
- Use exponential backoff

### Input Validation
- Validate all user inputs
- Sanitize HTML content
- Use Pydantic models for validation

### Error Handling
- Don't expose internal errors
- Log security events
- Use generic error messages

## 📊 Monitoring & Logging

### Security Events to Log
- Failed login attempts
- API key usage
- Database access patterns
- CORS violations

### Log Management
- Store logs securely
- Rotate log files
- Monitor for anomalies
- Set up alerts for suspicious activity

## 🚀 Production Deployment

### Environment Checklist
- [ ] All .env files are properly configured
- [ ] HTTPS is enabled
- [ ] CORS is properly configured
- [ ] Database RLS is enabled
- [ ] Rate limiting is implemented
- [ ] Monitoring is set up
- [ ] Backup strategy is in place

### Infrastructure Security
- [ ] Use secure hosting provider
- [ ] Enable firewall rules
- [ ] Regular security updates
- [ ] SSL/TLS certificates are valid
- [ ] Database is not publicly accessible

## 🔍 Security Testing

### Regular Checks
- [ ] Dependency vulnerability scans
- [ ] API endpoint testing
- [ ] Authentication flow testing
- [ ] Database access testing
- [ ] CORS configuration testing

### Tools
- `npm audit` for Node.js dependencies
- `safety check` for Python dependencies
- OWASP ZAP for web application testing
- Burp Suite for API testing

## 🚨 Incident Response

### If You Suspect a Breach
1. **Immediate Actions**
   - Rotate all API keys
   - Check access logs
   - Review recent changes
   - Notify stakeholders

2. **Investigation**
   - Identify affected systems
   - Determine attack vector
   - Assess data exposure
   - Document findings

3. **Recovery**
   - Patch vulnerabilities
   - Restore from backups if needed
   - Update security measures
   - Monitor for recurrence

## 📞 Security Contacts

For security issues:
- Create a private issue in the repository
- Email: [your-security-email]
- Include detailed information about the issue

## 📚 Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Supabase Security](https://supabase.com/docs/guides/security)
- [HuggingFace Security](https://huggingface.co/docs/hub/security) 