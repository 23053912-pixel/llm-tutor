# Changelog

All notable changes to LLM Tutor will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-04-20

### Added
- Initial release of LLM Tutor
- 15 comprehensive knowledge base documents covering:
  - LLM fundamentals and architecture
  - Training methodologies (pretraining, fine-tuning)
  - Prompt engineering and in-context learning
  - Retrieval-Augmented Generation (RAG)
  - LLM evaluation metrics and benchmarks
  - Model comparison and cost analysis
  - Parameter-efficient fine-tuning (LoRA/QLoRA)
  - Safety, bias, and alignment considerations
  - Real-world applications
  - Scaling laws and performance
  - Common pitfalls and debugging strategies
  - Future trends and emerging technologies
  - Token economics
- Multi-turn conversation support with memory management
- Intelligent routing system (retrieve/tool/skip)
- Faithfulness evaluation with automatic retry logic
- RAG pipeline with ChromaDB and SentenceTransformer
- Streamlit web interface with professional UI
- Groq API integration for fast inference
- Conversation history with sliding window (6-message limit)
- Source attribution and evaluation score display
- Comprehensive documentation and examples

### Features
- **Interactive Learning**: Engage with an AI tutor in natural conversations
- **RAG-Enhanced**: Answers grounded in curated knowledge base
- **Quality Evaluation**: Automatic faithfulness scoring (target > 0.8)
- **Multi-Route Architecture**: Intelligent query routing
- **Memory System**: Context-aware conversations with history
- **Fast Inference**: ~2-5s response time via Groq
- **Educational Focus**: Detailed explanations with examples

### Technical Stack
- **Framework**: LangGraph for agentic workflows
- **LLM**: Groq API (Llama 3.3 70B)
- **Embeddings**: SentenceTransformer (all-MiniLM-L6-v2)
- **Vector DB**: ChromaDB for in-memory storage
- **Frontend**: Streamlit
- **Memory**: MemorySaver with thread_id persistence
- **Evaluation**: LLM-as-Judge for faithfulness

### Documentation
- Comprehensive README with quick start guide
- Contributing guidelines for developers
- Development requirements file
- MIT license
- .gitignore for clean repo

---

## Planned Features (Roadmap)

### Version 1.1.0
- [ ] Web search tool integration
- [ ] Advanced retrieval (BM25 + semantic hybrid search)
- [ ] Re-ranking of retrieval results
- [ ] Conversation export (PDF, JSON)

### Version 1.2.0
- [ ] Fine-tuning support with LoRA
- [ ] Custom knowledge base upload
- [ ] Multi-language support
- [ ] User feedback loop for model improvement

### Version 2.0.0
- [ ] REST API endpoints
- [ ] Database persistence (PostgreSQL + pgvector)
- [ ] Admin dashboard
- [ ] Analytics and metrics tracking
- [ ] Docker containerization
- [ ] Kubernetes deployment templates

### Future
- [ ] Web interface redesign
- [ ] Mobile app support
- [ ] Real-time streaming responses
- [ ] Multi-model support (GPT-4, Claude, etc.)
- [ ] Advanced guardrails and safety filters
- [ ] Cost analytics dashboard

---

## Version History

### [Unreleased]
- Improvements in progress

### [1.0.0] - 2026-04-20 (Initial Release)
- ✅ MVP ready for public release
- ✅ 15 knowledge base documents
- ✅ Full evaluation pipeline
- ✅ Comprehensive documentation

---

## Installation & Upgrade

### First Installation
```bash
git clone https://github.com/yourusername/llm-tutor.git
cd llm-tutor
pip install -r requirements.txt
```

### Upgrade from Previous Version
```bash
git pull origin main
pip install --upgrade -r requirements.txt
```

---

## Migration Guides

### From Version 0.x to 1.0.0
- Knowledge base schema unchanged (backward compatible)
- Agent state structure compatible
- No breaking changes to API

---

## Known Issues

### v1.0.0
- ChromaDB in-memory storage (no persistence across restarts)
  - _Workaround_: Save/load conversation via JSON export
- Context window limit at 4096 tokens for Llama 3.3
  - _Workaround_: Use sliding window (6-message limit)
- Some specialty topics may hallucinate without RAG
  - _Expected behavior_: Normal for out-of-domain queries

---

## Support & Bug Reports

- 🐛 **Found a bug?** Open an issue on GitHub
- 💡 **Feature request?** Discuss in GitHub Discussions
- 📧 **Security concern?** Email maintainers privately
- 📖 **Need help?** Check documentation and FAQ

---

## Contributors

Thanks to everyone who contributed! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

---

**Last Updated**: 2026-04-20
**Current Version**: 1.0.0
