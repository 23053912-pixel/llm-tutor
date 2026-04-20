# Security Policy

## Reporting Security Vulnerabilities

### Do Not Publicly Disclose Security Issues

If you discover a security vulnerability in LLM Tutor, please **DO NOT** open a public GitHub issue. Instead, follow responsible disclosure practices:

1. **Email**: Send details to `security@llm-tutor.dev` (or maintainers' email)
2. **Include**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact (low/medium/high/critical)
   - Suggested fix (if any)
3. **Wait**: Allow 72 hours for acknowledgment, 30 days for patch before disclosure
4. **Credit**: Will be acknowledged in CHANGELOG and security advisory

### Expected Response Timeline
- **Initial response**: Within 24-48 hours
- **Assessment**: Within 1 week
- **Patch release**: Within 2-4 weeks (depending on severity)
- **Public disclosure**: Coordinated with security team

---

## Security Best Practices

### API Key Management

**DO**:
✅ Store `GROQ_API_KEY` in `.env` file  
✅ Add `.env` to `.gitignore` (already included)  
✅ Use environment variables in production  
✅ Rotate keys periodically  
✅ Use Groq's key management dashboard to revoke old keys  
✅ Enable rate limiting in Groq console  

**DON'T**:
❌ Commit API keys to Git  
❌ Hardcode keys in source code  
❌ Share keys in emails, chat, or public forums  
❌ Use same key across multiple deployments  
❌ Store keys in comments or documentation  

### Example Secure Setup
```bash
# Load from environment
export GROQ_API_KEY=gsk_your_key_here

# Or use .env file (git-ignored)
cat > .env << EOF
GROQ_API_KEY=gsk_your_key_here
EOF

# Verify .gitignore includes .env
grep "^\.env$" .gitignore  # Should return .env

# Never commit!
git status | grep .env  # Should show as ignored
```

---

## Dependency Security

### Vulnerability Scanning

**Manual checking**:
```bash
# Check for known vulnerabilities in dependencies
pip install safety
safety check

# Or check specific package
pip-audit
```

**Automated (CI/CD)**:
```yaml
# GitHub Actions example (add to .github/workflows/security.yml)
name: Security Scan
on: [push, pull_request]
jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install safety
      - run: safety check
```

### Keeping Dependencies Updated
```bash
# Check outdated
pip list --outdated

# Security patches only
pip install --upgrade safety
pip install --upgrade -r requirements.txt

# Note breaking changes
pip install --upgrade --dry-run -r requirements.txt
```

### Critical Dependencies Security
| Package | Known Issues | Mitigation |
|---------|------------|-----------|
| langchain | Supply chain risks (rapidly evolving) | Pin versions, review changes |
| chromadb | In-memory storage (no encryption) | Only local dev data |
| groq | External API dependency | Rate limiting, key rotation |
| streamlit | XSS in older versions | Keep updated |

---

## Input Validation & Sanitization

### Query Input

**Current behavior**:
- Queries passed to LLM via prompt injection protection
- Groq API handles intent parsing
- ChromaDB handles text queries safely

**Future hardening**:
```python
# Example sanitization (could add to agent.py)
def sanitize_query(query: str) -> str:
    """Remove potentially harmful patterns."""
    # Remove SQL injection attempts
    query = re.sub(r'(;--|\/\*|DROP|DELETE|INSERT)', '', query)
    
    # Remove prompt injection attempts
    query = re.sub(r'(System:|System prompt:|Ignore instructions)', '', query)
    
    # Limit length
    if len(query) > 2000:
        query = query[:2000]
    
    return query.strip()
```

### File Upload Security (Future Feature)
When implementing file upload for custom KB:
```python
# Validate file type
ALLOWED_EXTENSIONS = {'.pdf', '.txt', '.docx', '.md'}
UPLOAD_FOLDER = './uploads'
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

def validate_upload(file):
    _, ext = os.path.splitext(file.filename)
    if ext.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Invalid file type: {ext}")
    if len(file) > MAX_FILE_SIZE:
        raise ValueError("File too large")
    return True
```

---

## Environment & Infrastructure Security

### Secrets Management

**Local Development**:
```bash
# .env should be git-ignored (check .gitignore)
echo "*.env" >> .gitignore
echo ".env.local" >> .gitignore

# Never commit these files
git status --short | grep .env  # Should be empty
```

**GitHub Secrets** (for CI/CD):
```bash
# Settings → Secrets and variables → Actions
gh secret set GROQ_API_KEY -b "gsk_your_key"
gh secret set OPENAI_API_KEY -b "sk_..."
```

**Deployment** (Streamlit Cloud, AWS, etc.):
```bash
# Use platform's secret management
# NOT environment files in Git
# NOT environment files in containers without secrets
```

### Code Security

**Use linters + type checking**:
```bash
# Installation
pip install -r requirements-dev.txt

# Run checks
black capstone_streamlit.py  # Formatting
flake8 capstone_streamlit.py  # Linting
mypy capstone_streamlit.py    # Type checking
pylint capstone_streamlit.py  # Code analysis
```

**Example pre-commit hook** (auto-run before commit):
```bash
# Install
pip install pre-commit
pre-commit install

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/psf/black
    rev: 23.0.0
    hooks:
      - id: black
  - repo: https://github.com/PyCQA/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.1.0
    hooks:
      - id: check-merge-conflict
      - id: end-of-file-fixer
      - id: trailing-whitespace
EOF
```

---

## Data Security & Privacy

### Current Data Handling

**Knowledge Base**:
- ✅ All documents public/educational
- ✅ No PII (Personally Identifiable Information)
- ✅ No credentials stored
- ✅ No user tracking

**Conversations**:
- ⚠️ Currently in-memory only
- ⚠️ Lost on app restart
- ⚠️ Not encrypted
- ✅ No database persistence

### Future Privacy Considerations
```python
# When implementing persistence (future)

# 1. Encrypt at rest
from cryptography.fernet import Fernet
cipher = Fernet(encryption_key)
encrypted_conversation = cipher.encrypt(conversation.encode())

# 2. Anonymize where possible
# Remove user identifiable info before storing
def anonymize_query(query: str) -> str:
    # Remove emails
    query = re.sub(r'[\w\.-]+@[\w\.-]+', '[EMAIL]', query)
    # Remove phone numbers
    query = re.sub(r'\d{3}-\d{3}-\d{4}', '[PHONE]', query)
    return query

# 3. Implement data retention policy
# Delete conversations after 90 days
DELETE_AFTER_DAYS = 90

# 4. GDPR compliance (if EU users)
# - Right to be forgotten
# - Data export
# - Consent tracking
```

### User Data Policy (When Applicable)
```markdown
## Data We Collect
- Chat queries (for improving model)
- Conversation feedback (optional)
- Usage statistics (aggregated, anonymous)

## Data We DON'T Collect
- Personal information
- Credentials (except API keys in .env, local only)
- Browsing history
- IP addresses (unless logging needed)

## Data Retention
- Conversations: Session only (currently)
- Logs: 7 days max
- Feedback: 1 year

## Your Rights
- Access: Request your data
- Delete: Right to be forgotten
- Export: Export conversations in JSON
```

---

## Supply Chain Security

### Dependency Trust
```bash
# Verify package sources
pip index versions langgraph

# Check package maintainers
pip show langgraph | grep Author

# Use hash verification
pip install --require-hashes -r requirements.txt
```

### Git Security
```bash
# Sign commits with GPG (recommended)
git config --global user.signingkey YOUR_GPG_KEY
git commit -S -m "Secure commit"

# Or use SSH keys for GitHub
ssh-keygen -t ed25519 -C "your@email.com"
```

---

## Performance & DoS Protection

### Rate Limiting (Future Implementation)

**For API endpoints** (when REST API added):
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()

@app.post("/chat")
@limiter.limit("10/minute")
async def chat(request: ChatRequest):
    # Limited to 10 requests per minute per IP
    pass
```

**For Groq API**:
```bash
# In Groq console, set rate limits:
# - 10,000 tokens per minute
# - 100 requests per minute
```

### Resource Limits (Streamlit)

Already enforced in `agent.py`:
- ✅ Max context messages: 6
- ✅ Token limit: 4096 (Llama 3.3)
- ✅ Timeout: 30 seconds (implicit)
- ✅ Retry limit: 2 attempts

**Could add**:
- Request queue length
- Memory ceiling (detect OOM early)
- Concurrent session limits

---

## Monitoring & Logging

### Security Logging

```python
# Log security events (add to agent.py)
import logging

security_logger = logging.getLogger('security')
security_logger.setLevel(logging.WARNING)

# Handler
handler = logging.FileHandler('security.log')
security_logger.addHandler(handler)

# Usage
security_logger.warning(f"Invalid API key format: {api_key[:10]}...")
security_logger.warning(f"Suspicious query pattern detected: {query[:50]}...")
security_logger.error(f"Authentication failed: {ip_address}")
```

### Audit Trail (Future)

```python
# Track all API calls and major actions
audit_log = [
    {
        "timestamp": "2026-04-20T10:30:00Z",
        "user_id": "anonymous",
        "action": "query_submitted",
        "query_length": 150,
        "status": "success",
        "model": "llama-3.3-70b",
        "response_time_ms": 2450
    }
]
```

---

## Incident Response Plan

### If Breach Occurs

1. **Immediate** (0-1 hour):
   - [ ] Notify security team
   - [ ] Revoke compromised API keys
   - [ ] Check logs for suspicious activity
   - [ ] Lock down sensitive data

2. **Short-term** (1-24 hours):
   - [ ] Assess scope of breach
   - [ ] Issue security advisory
   - [ ] Patch vulnerability
   - [ ] Review access logs

3. **Long-term** (1-7 days):
   - [ ] Implement additional safeguards
   - [ ] Root cause analysis
   - [ ] Update documentation
   - [ ] Communication with stakeholders

### Template Security Advisory
```markdown
# Security Advisory [YEAR]-[NUMBER]

## Title
[Issue title]

## Severity
[CRITICAL | HIGH | MEDIUM | LOW]

## Affected Versions
- LLM Tutor < 1.0.1

## Description
[Technical description]

## Workaround
[Temporary fix]

## Patch
Available in 1.0.1+

## Timeline
- Reported: [Date]
- Confirmed: [Date]
- Patched: [Date]

## Credits
[Finder name] for responsible disclosure
```

---

## Security Checklist

- [ ] API keys stored in `.env`, not in code
- [ ] `.env` is in `.gitignore` and never committed
- [ ] All dependencies pinned to specific versions
- [ ] No debug mode in production
- [ ] HTTPS enabled (if deployed to web)
- [ ] Input validation on user queries
- [ ] Error messages don't expose internals
- [ ] Logging enabled for audit trail
- [ ] Security tests in CI/CD pipeline
- [ ] Dependencies regularly updated
- [ ] No credentials in logs
- [ ] Rate limiting implemented
- [ ] CORS properly configured (if API)
- [ ] Security.md in repository
- [ ] Regular security reviews scheduled

---

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [PEP 8 Security](https://pep8.org/)
- [Python Security](https://python.readthedocs.io/en/latest/library/security_warnings.html)
- [LangChain Security](https://docs.langchain.com/docs/ecosystem/integrations/groq)
- [Streamlit Security](https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker)

---

## Contact

- 🔒 **Security Issues**: security@llm-tutor.dev
- 📧 **Maintainers**: maintainers@llm-tutor.dev
- 🐛 **Bug Bounty**: [Future program details]

---

**Last Updated**: 2026-04-20
**Version**: 1.0.0
**Next Review**: 2026-07-20 (quarterly)
