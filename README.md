# 🧠 LLM Tutor - Interactive Large Language Model Learning Platform

An AI-powered educational chatbot built with **LangGraph**, **Retrieval-Augmented Generation (RAG)**, and **Groq API** that teaches comprehensive knowledge about Large Language Models.

## ✨ Features

- **Interactive Learning**: Multi-turn conversations with an intelligent LLM tutor
- **RAG-Enhanced**: Retrieval-Augmented Generation grounded in a curated knowledge base
- **Evaluation Pipeline**: Automatic faithfulness scoring and answer quality evaluation
- **15+ Topics**: Comprehensive coverage of LLM concepts, training, evaluation, and applications
- **Memory System**: Conversation history with sliding window to manage context efficiently
- **Multi-Route Architecture**: Intelligent routing between retrieval, tool, and conversation modes
- **Real-time API**: Powered by Groq's ultra-fast Llama 3.3 70B model

## 📚 Knowledge Base Covers

1. What are Large Language Models (LLMs)
2. Transformer Architecture & Attention Mechanisms
3. Training: Pretraining & Fine-tuning
4. Prompt Engineering & In-Context Learning
5. Retrieval Augmented Generation (RAG)
6. LLM Evaluation & Metrics
7. Comparing Open-Source vs Proprietary Models
8. Safety, Bias & Alignment
9. Real-World Applications
10. Future Trends & Emerging Technologies
11. Token Economics & Cost Analysis
12. Parameter-Efficient Fine-Tuning (LoRA/QLoRA)
13. Benchmarks, Leaderboards & Evaluation
14. Common Pitfalls & Debugging
15. Scaling Laws & Model Performance

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- GROQ API key (free at [https://console.groq.com](https://console.groq.com))
- 2GB disk space for embeddings

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/llm-tutor.git
   cd llm-tutor
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/macOS
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure GROQ API key** (Choose one method)

   **Method 1: Streamlit Secrets (Recommended)**
   ```bash
   # Create secrets.toml from template
   cp .streamlit\secrets.toml.example .streamlit\secrets.toml
   
   # Edit the file and add your Groq API key
   notepad .streamlit\secrets.toml
   ```
   
   Then add your key:
   ```toml
   GROQ_API_KEY = "gsk_xxxxxxxxxxxxxxxxxxxxx"
   ```
   
   **Method 2: Environment File (.env)**
   ```bash
   cp .env.example .env
   notepad .env
   ```
   
   Then add your key:
   ```
   GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxx
   ```

   Get your free API key from: https://console.groq.com

5. **Run the application**
   ```bash
   streamlit run capstone_streamlit.py
   ```

6. **Open in browser**
   Navigate to `http://localhost:8502`
   
   The API key will be automatically loaded from your `.env` file.

## 🏗️ Architecture

### Component Overview

```
User Query
    ↓
[Streamlit UI] ← Session State Management
    ↓
[LangGraph Agent]
    ├─ memory_node: Process & store conversation history
    ├─ router_node: Classify query intent (retrieve/tool/skip)
    ├─ retrieval_node: Query RAG knowledge base
    ├─ answer_node: Generate grounded responses
    ├─ eval_node: Score faithfulness (0-1)
    └─ save_node: Persist conversation
    ↓
[ChromaDB Vector Store] with SentenceTransformer embeddings
    ↓
[Groq API] - Llama 3.3 70B Model
    ↓
Response with Sources & Evaluation Score
```

### Key Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | Streamlit | Web UI, chat interface |
| **Agent Framework** | LangGraph | Stateful multi-node agentic graph |
| **Retrieval** | ChromaDB + SentenceTransformer | Vector similarity search |
| **LLM** | Groq (Llama 3.3 70B) | Fast inference, conversational AI |
| **Evaluation** | LLM-as-Judge | Faithfulness scoring |
| **Memory** | MemorySaver | Persistent conversation state |

## 📁 Project Structure

```
llm-tutor/
├── capstone_streamlit.py      # Main Streamlit application
├── agent.py                   # LangGraph agent definition
├── kb_data.py                 # Knowledge base documents (15 topics)
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── .gitignore                 # Git ignore rules
├── LICENSE                    # MIT License
└── docs/
    ├── ARCHITECTURE.md        # Technical architecture details
    ├── API.md                 # API documentation
    └── DEVELOPMENT.md         # Development guide
```

## 🎯 How It Works

### Conversation Flow

1. **User Input**: Question in Streamlit chat
2. **Memory Node**: Append to conversation history (last 6 messages)
3. **Router Node**: Classify intent into 3 routes:
   - `retrieve`: Knowledge base questions
   - `tool`: Date/time questions
   - `skip`: Casual conversation
4. **Retrieval Node**: Embed query, find top-3 similar documents
5. **Answer Node**: Generate response using LLM + context
6. **Eval Node**: Score faithfulness (0-1 scale)
   - Score < 0.7: Retry up to 2x
   - Score ≥ 0.7: Return answer
7. **Save Node**: Persist to conversation history
8. **Display**: Show answer + sources + score

### RAG Pipeline

```
Question → Embed (all-MiniLM-L6-v2)
         → Search ChromaDB (cosine similarity)
         → Retrieve top-3 chunks
         → Insert into system prompt
         → Generate grounded answer
         → Score faithfulness
```

## 💡 Usage Examples

### Ask about concepts
```
User: "Explain how transformer architecture works"
→ Retrieves from doc_002
→ Returns detailed explanation with sources
```

### Ask about applications
```
User: "What are real-world applications of LLMs?"
→ Retrieves from doc_009
→ Lists industry use cases with examples
```

### Cost analysis
```
User: "How much does it cost to use different LLM APIs?"
→ Retrieves from doc_011 (Token Economics)
→ Provides pricing comparison and optimization tips
```

   
   The API key will be automatically loaded from your `secrets.toml` or `.env` file.

## ⚙️ Configuration

### API Key Setup

**Streamlit Secrets (Recommended for deployment)**
- Create `.streamlit/secrets.toml` from `secrets.toml.example`
- Add your Groq API key
- Never commit `secrets.toml` to Git (managed by `.gitignore`)
- Works with Streamlit Cloud deployments

**.env File (For local development)**
- Create `.env` from `.env.example`  
- Add your Groq API key
- Never commit `.env` to Git (managed by `.gitignore`)
- Fallback if Streamlit Secrets not configured

### Model Parameters
Edit `agent.py` to customize:
```python
llm = ChatGroq(
    model="llama-3.3-70b-versatile",  # Model selection
    temperature=0,                     # Deterministic responses
    api_key=api_key
)

# Retrieval settings
n_results=3                            # Top-3 documents
embedder = SentenceTransformer('all-MiniLM-L6-v2')  # Embedding model

# Evaluation settings
EVAL_THRESHOLD = 0.7                  # Faithfulness threshold
MAX_EVAL_RETRIES = 2                  # Max retry attempts
```

## 📊 Evaluation Metrics

Each response includes:

- **Faithfulness Score (0-1)**: How much is grounded in retrieved context
- **Sources**: Which knowledge base documents were used
- **Eval Retries**: Number of times answer was refined
- **Route**: Which path was taken (retrieve/tool/skip)

Target metrics:
- Faithfulness > 0.8
- Context precision > 0.7
- Answer relevancy > 0.75

## 🔧 Development

### Running Tests
```bash
# Test retrieval quality
python -c "from kb_data import documents; from sentence_transformers import SentenceTransformer; e = SentenceTransformer('all-MiniLM-L6-v2'); print(f'Loaded {len(documents)} documents')"

# Test agent
python -c "from agent import create_agent; print('Agent module loads successfully')"
```

### Adding More Documents

Edit `kb_data.py`:
```python
{
    "id": "doc_016",
    "topic": "Your Topic",
    "text": "Comprehensive text about the topic..."
}
```

### Debugging

Enable logs in Streamlit:
```bash
streamlit run capstone_streamlit.py --logger.level=debug
```

## 📈 Performance

- **Inference Speed**: ~2-5 seconds (Groq API)
- **Embedding Speed**: <1 second (SentenceTransformer)
- **Memory Usage**: ~2GB RAM (after first run)
- **Token Cost**: ~$0.0001 per query (Groq free tier)

## 🛡️ Safety & Limitations

### Strengths
- RAG grounding reduces hallucinations
- Faithfulness evaluation catches unreliable answers
- System prompt enforces source attribution

### Limitations
- Knowledge cutoff at training time (knowledge base dependent)
- Context window limit (4096 tokens for Llama 3.3)
- Mathematical reasoning requires output validation
- Code generation requires human review

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 📞 Support & Contact

- **Issues**: Open a GitHub issue for bugs
- **Discussions**: Use GitHub Discussions for questions
- **Email**: your-email@example.com

## 🙏 Acknowledgments

- Built with [LangGraph](https://python.langchain.com/docs/langgraph/) for agentic workflows
- Powered by [Groq](https://groq.com) for fast LLM inference
- Knowledge base concepts from [Agentic AI Course](https://example.com)
- Embeddings via [Sentence Transformers](https://www.sbert.net/)

## 🚀 Roadmap

- [x] Basic RAG pipeline
- [x] Faithfulness evaluation
- [x] Multi-turn conversations
- [ ] Fine-tuning support (LoRA)
- [ ] Advanced retrieval (hybrid search + re-ranking)
- [ ] Web search tool integration
- [ ] Database persistence (PostgreSQL + PGVector)
- [ ] REST API endpoints
- [ ] Docker containerization
- [ ] Deployment guides (AWS, GCP, Vercel)

## 📊 Metrics & Analytics

Track your usage:
```bash
# View conversation history
# Logs stored in .streamlit/logs/

# Monitor API costs
# Check Groq account: https://console.groq.com
```

---

**Made with ❤️ for LLM enthusiasts and educators**

Last updated: April 2026
