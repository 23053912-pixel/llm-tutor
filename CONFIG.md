# Configuration Guide for LLM Tutor

This file documents all configuration options, environment variables, and setup instructions for the LLM Tutor project.

## Environment Setup

### Quick Setup
```bash
# 1. Create virtual environment
python -m venv .venv

# 2. Activate it
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment variables
cp .env.example .env
# Edit .env with your own values
```

### Required Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Groq API Configuration (REQUIRED)
GROQ_API_KEY=gsk_your_api_key_here

# Optional: Streamlit Configuration
STREAMLIT_CONFIG_THEME_PRIMARYCOLOR=#FF6B35
STREAMLIT_CONFIG_THEME_TEXTCOLOR=#000000
STREAMLIT_CONFIG_THEME_FONT=sans serif

# Optional: ChromaDB Configuration
CHROMADB_COLLECTION_NAME=llm_tutor_docs
CHROMADB_DISTANCE_METRIC=cosine

# Optional: Agent Configuration
MEMORY_SAVE_DIR=./memory_state
MAX_CONTEXT_MESSAGES=6
MIN_FAITHFULNESS_SCORE=0.8
EVALUATION_RETRIES=2
```

### Environment Variable Details

#### GROQ_API_KEY
- **Type**: String
- **Required**: Yes
- **Description**: API key for Groq inference service
- **Format**: Must start with `gsk_`
- **How to get**:
  1. Sign up at https://console.groq.com
  2. Navigate to API Keys section
  3. Create new key
  4. Copy and paste into .env

#### STREAMLIT_CONFIG_THEME_PRIMARYCOLOR
- **Type**: Hex color code
- **Required**: No
- **Default**: Theme color (currently #FF6B35 - orange)
- **Description**: Primary UI color for Streamlit theme

#### CHROMADB_COLLECTION_NAME
- **Type**: String
- **Required**: No
- **Default**: `llm_tutor_docs`
- **Description**: Name of ChromaDB collection storing embeddings

#### CHROMADB_DISTANCE_METRIC
- **Type**: String (cosine | l2 | ip)
- **Required**: No
- **Default**: `cosine`
- **Description**: Distance metric for vector similarity search

#### MEMORY_SAVE_DIR
- **Type**: Path string
- **Required**: No
- **Default**: `./memory_state`
- **Description**: Directory for persisting conversation memory

#### MAX_CONTEXT_MESSAGES
- **Type**: Integer (positive)
- **Required**: No
- **Default**: 6
- **Description**: Number of previous messages to keep in context window

#### MIN_FAITHFULNESS_SCORE
- **Type**: Float (0.0 - 1.0)
- **Required**: No
- **Default**: 0.8
- **Description**: Minimum acceptable faithfulness score; triggers retry if below

#### EVALUATION_RETRIES
- **Type**: Integer (positive)
- **Required**: No
- **Default**: 2
- **Description**: Maximum number of retries if faithfulness score is low

---

## Running the Application

### Development Mode
```bash
# Ensure virtual environment is activated
.venv\Scripts\activate

# Run Streamlit app
streamlit run capstone_streamlit.py
```

**Output**:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.x:8501
```

### Production Mode (with Gunicorn)
```bash
# Install production dependencies (optional)
pip install gunicorn

# Run with gunicorn
gunicorn --workers 4 --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 capstone_streamlit:app
```

### Docker Mode (Future)
```bash
# Build image
docker build -t llm-tutor:1.0.0 .

# Run container
docker run -p 8501:8501 \
  -e GROQ_API_KEY=$GROQ_API_KEY \
  llm-tutor:1.0.0
```

---

## Configuration Files

### Project Structure
```
llm-tutor/
├── .env                          # Environment variables (git ignored)
├── .streamlit/
│   └── config.toml              # Streamlit configuration
├── .gitignore                   # Git ignore patterns
├── requirements.txt             # Production dependencies
├── requirements-dev.txt         # Development dependencies
├── capstone_streamlit.py        # Main Streamlit app
├── agent.py                     # LangGraph agent workflow
├── kb_data.py                   # Knowledge base (15 documents)
└── memory_state/                # Conversation memory (auto-created)
```

### .streamlit/config.toml
Customize Streamlit behavior:

```toml
[theme]
primaryColor = "#FF6B35"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#000000"
font = "sans serif"

[client]
showErrorDetails = true
toolbarMode = "developer"

[logger]
level = "info"

[server]
port = 8501
headless = true
runOnSave = true
```

---

## Dependencies Configuration

### Production Dependencies (requirements.txt)
See [requirements.txt](requirements.txt) for:
- Core: langgraph, langchain, langchain-groq
- Vector: chromadb, sentence-transformers
- Web: streamlit
- Inference: groq
- Utilities: python-dotenv, jupyter

### Development Dependencies (requirements-dev.txt)
See [requirements-dev.txt](requirements-dev.txt) for:
- Testing: pytest, pytest-cov
- Quality: black, flake8, pylint, mypy
- Documentation: sphinx, sphinx-rtd-theme
- Debugging: ipdb, memory-profiler

### Installing Dependencies

**Production only**:
```bash
pip install -r requirements.txt
```

**Production + Development** (for contributors):
```bash
pip install -r requirements.txt -r requirements-dev.txt
```

**Specific component** (if adding features):
```bash
pip install -e .  # If setuptools available
```

---

## Knowledge Base Configuration

### Adding New Documents

Edit `kb_data.py` and add to the `documents` list:

```python
{
    "doc_id": "doc_016",
    "title": "New Topic Title",
    "content": "Full document content here. Should be comprehensive and well-structured.",
    "category": "LLM Fundamentals",  # or Applications, Advanced, etc.
    "keywords": ["keyword1", "keyword2"]
}
```

### Knowledge Base Statistics
- **Current documents**: 15
- **Total tokens**: ~15,000 (average 1000 per doc)
- **Embedding model**: SentenceTransformer all-MiniLM-L6-v2 (384 dimensions)
- **Storage**: ChromaDB (in-memory, persists during session)

---

## Agent Configuration

### Router Configuration
Located in `agent.py`:

```python
router_system_prompt = """
Classify the query into three categories:
1. 'retrieve' - Query about LLMs or related topics
2. 'tool' - Query about current date/time
3. 'skip' - Casual conversation
"""
```

### Evaluation Configuration
```python
eval_system_prompt = """
Score faithfulness of the response (0-1):
- 1.0: Fully grounded in context
- 0.8: Mostly grounded
- <0.8: Requires retry or clarification
"""
```

### Memory Configuration
```python
memory = MemorySaver()
MAX_CONTEXT: int = 6  # Keep last 6 messages
```

---

## Performance Tuning

### Optimization Tips

1. **Faster Responses**:
   - ✅ Groq API provides ~350 tokens/sec (already fast)
   - ✅ ChromaDB in-memory reduces latency
   - 💡 Consider: Switch to BM25 + reranking for better relevance

2. **Better Quality**:
   - ✅ Current: Faithfulness scoring + retry logic
   - 💡 Consider: Hybrid search (semantic + BM25)
   - 💡 Consider: Context compression/summarization
   - 💡 Consider: Few-shot examples in prompts

3. **Resource Usage**:
   - 💡 Consider: Batch API calls for multiple queries
   - 💡 Consider: Cache embeddings in Redis
   - 💡 Consider: Use lighter embeddings (e.g., all-MiniLM-L6-v2 → bge-small-en)

### Memory Usage
- **Embeddings**: ~50 MB (15 docs × 384 dimensions)
- **ChromaDB**: ~20 MB (in-memory storage)
- **Agent state**: < 1 MB (conversation history)
- **Total**: < 100 MB typical usage

### CPU/GPU
- **CPU**: Sufficient (embeddings + routing)
- **GPU**: Not required (inference via Groq API)
- **Recommended**: 2+ GB RAM, 1+ core

---

## Debugging Configuration

### Error Handling

```python
# Set debug mode in .env
LOG_LEVEL=DEBUG

# Or in code (capstone_streamlit.py)
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| API key invalid | Wrong format or expired | Check `gsk_` prefix, regenerate at console.groq.com |
| Import errors | Missing dependencies | `pip install -r requirements.txt` |
| Embedding errors | ChromaDB issue | Clear `.streamlit/cache`, restart app |
| Low faithfulness | Hallucination | Improve prompt, expand KB, increase retries |
| Slow responses | Network latency | Check internet, retry, use Groq anyway |
| Memory issues | Large conversation | Reduce `MAX_CONTEXT_MESSAGES` |
| CORS errors | Cross-origin requests | Only relevant if deploying API (future) |

### Logging
```bash
# Check logs
tail -f .streamlit/*.log

# Increase verbosity
streamlit run capstone_streamlit.py --logger.level=debug
```

---

## Deployment Configuration

### Local Deployment
```bash
streamlit run capstone_streamlit.py --server.port 8501 --server.address localhost
```

### Docker Deployment (Template)
```dockerfile
FROM python:3.11

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "capstone_streamlit.py"]
```

### Cloud Deployment (Future)
- **Streamlit Cloud**: Free tier available
- **AWS/GCP/Azure**: Standard containerization
- **Render/Railway**: Simple deployment platforms

---

## Testing Configuration

### Running Tests
```bash
# All tests
pytest

# With coverage
pytest --cov=.

# Specific test
pytest tests/test_agent.py -v

# Watch mode (requires pytest-watch)
ptw
```

### Test Environment
```bash
# Create test database
pytest --fixtures

# Run with specific Python version
python3.11 -m pytest
```

---

## Version Management

### Current Versions
- **Project**: 1.0.0 (see CHANGELOG.md)
- **Python**: 3.8+
- **LangGraph**: 0.0.64+
- **Streamlit**: 1.28.0+

### Upgrading Dependencies
```bash
# Check for updates
pip list --outdated

# Upgrade specific package
pip install --upgrade langgraph

# Upgrade all
pip install --upgrade -r requirements.txt
```

---

## Support

- 📖 **Documentation**: See README.md and CONTRIBUTING.md
- 🐛 **Issues**: Open GitHub issue
- 💬 **Discussions**: GitHub Discussions section
- 📧 **Email**: maintainers@llm-tutor.dev

---

**Last Updated**: 2026-04-20
**Config Version**: 1.0.0
