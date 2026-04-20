# Contributing to LLM Tutor

Thank you for your interest in contributing! This document provides guidelines for contributing to the LLM Tutor project.

## Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in all interactions.

## How Can I Contribute?

### 1. Reporting Bugs

If you find a bug, please submit an issue with:
- **Title**: Clear, concise description
- **Description**: What happened and what you expected
- **Steps to Reproduce**: Detailed steps to reproduce the issue
- **Environment**: Python version, OS, installed packages
- **Screenshots**: If applicable

### 2. Suggesting Enhancements

Have an idea for improvement? Open an issue with:
- **Title**: Clear feature description
- **Motivation**: Why this feature would be useful
- **Expected Behavior**: How it should work
- **Examples**: Use cases or mockups

### 3. Submitting Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/llm-tutor.git
   cd llm-tutor
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Make your changes**
   - Follow the code style (see below)
   - Add tests if applicable
   - Update documentation
   - Update CHANGELOG.md

4. **Install dev dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

5. **Run tests and linting**
   ```bash
   pytest
   flake8 .
   black .
   ```

6. **Commit with clear messages**
   ```bash
   git commit -m "feat: add new feature X"
   git commit -m "fix: resolve issue Y"
   git commit -m "docs: update README for Z"
   ```

7. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then open a Pull Request on GitHub

## Code Style

### Python

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use [Black](https://github.com/psf/black) for formatting
- Use [Flake8](https://flake8.pycqa.org/) for linting
- Type hints recommended for new code

```python
# Good
def process_query(query: str, context: str) -> str:
    """Process a query with given context.
    
    Args:
        query: User question
        context: Retrieved context
        
    Returns:
        Model response
    """
    result = llm.invoke(query + context)
    return result

# Avoid
def process_query(q, c):
    r = llm.invoke(q + c)
    return r
```

### Docstrings

Use Google-style docstrings:

```python
def add_documents(texts: List[str], ids: List[str]) -> None:
    """Add documents to the vector store.

    Args:
        texts: List of document texts
        ids: List of unique document IDs

    Raises:
        ValueError: If texts and ids have different lengths
        
    Example:
        >>> add_documents(["text1", "text2"], ["id1", "id2"])
    """
    pass
```

### Comments

```python
# Good: explains WHY
# Use lower temperature to reduce hallucinations
temperature = 0.1

# Avoid: explains WHAT (code already shows this)
# Set temperature to 0.1
temperature = 0.1
```

## Testing

### Write tests for:
- New functions
- Bug fixes
- Edge cases
- Error handling

### Test template

```python
# tests/test_agent.py
import pytest
from agent import create_agent

def test_router_classifies_retrieve_queries():
    """Test that router correctly identifies retrieval queries."""
    agent = create_agent(llm, embedder, collection)
    result = agent.invoke({"question": "What is RAG?"})
    assert result["route"] == "retrieve"

def test_faithfulness_score_above_threshold():
    """Test that good answers score high on faithfulness."""
    # Arrange
    question = "What is a transformer?"
    # Act
    result = agent.invoke({"question": question})
    # Assert
    assert result["faithfulness"] > 0.7
```

### Run tests

```bash
pytest                    # Run all tests
pytest -v               # Verbose output
pytest tests/test_agent.py  # Run specific test file
pytest -x               # Stop on first failure
```

## Documentation

### Update docs for:
- New features
- API changes
- Configuration options
- Known limitations

### Doc files to update:
- `README.md`: Quick start, overview
- `docs/ARCHITECTURE.md`: Technical details
- `docs/API.md`: Function/class reference
- Docstrings: In-code documentation

### Example doc format

```markdown
## Feature Name

**Description**: What it does

**Usage**:
```python
# Code example
```

**Parameters**:
- `param1` (type): Description

**Returns**: What it returns

**Example**:
```
Input: ...
Output: ...
```

**See also**: Related features
```

## Adding Knowledge Base Documents

To expand the knowledge base:

1. Edit `kb_data.py`
2. Add new document entry:

```python
{
    "id": "doc_016",
    "topic": "Your Topic",
    "text": (
        "Comprehensive, well-written content about the topic. "
        "Should be 200-500 words. "
        "Include examples, key concepts, and practical information. "
        "Write in clear, educational language."
    )
}
```

3. Test retrieval:
```python
from kb_data import documents
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer('all-MiniLM-L6-v2')
query = "your test query"
# Verify your new doc is retrieved
```

4. Submit PR with the new document

## Commit Message Format

Follow conventional commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (formatting)
- `refactor`: Code restructuring
- `test`: Adding/updating tests
- `chore`: Build, deps, tooling

### Examples:
```
feat(rag): add hybrid retrieval with BM25

fix(eval): handle null faithfulness scores

docs(readme): add installation instructions

test(agent): add router classification tests
```

## Development Workflow

### 1. Set up environment

```bash
git clone <your-fork>
cd llm-tutor
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 2. Make changes

```bash
git checkout -b feat/my-feature
# Edit files
```

### 3. Test locally

```bash
pytest
flake8 .
black . --check
streamlit run capstone_streamlit.py
```

### 4. Commit and push

```bash
git add .
git commit -m "feat(scope): description"
git push origin feat/my-feature
```

### 5. Open PR

- Link related issues: "Closes #123"
- Describe changes clearly
- Reference any breaking changes
- Request review from maintainers

## Review Process

### What reviewers look for:
- ✅ Code quality & style
- ✅ Tests & coverage
- ✅ Documentation
- ✅ Breaking changes
- ✅ Performance impact
- ✅ Security implications

### Timeline:
- Small PRs (< 100 lines): 1-2 days
- Medium PRs (100-500 lines): 2-5 days
- Large PRs (> 500 lines): 5-10 days

## Release Process

Maintainers handle releases. We follow [Semantic Versioning](https://semver.org/):

- `MAJOR.MINOR.PATCH`
- Example: `v1.2.3`

### Changelog Format

```markdown
## [1.2.3] - 2026-04-20

### Added
- New feature description

### Fixed
- Bug fix description

### Changed
- Breaking changes

### Deprecated
- Deprecated features

### Removed
- Removed features
```

## Questions?

- 📖 Check the [FAQ](docs/FAQ.md)
- 💬 Open a discussion on GitHub
- 📧 Email the maintainers
- 🐛 Search existing issues

---

Thank you for contributing to LLM Tutor! 🙏

**Happy coding!** 🚀
