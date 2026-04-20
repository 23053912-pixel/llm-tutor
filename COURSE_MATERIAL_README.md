# 📚 Agentic AI Course Material

## Overview

This directory contains a comprehensive 13-day Agentic AI course curriculum plus a capstone project. The course covers everything from fundamental LLM APIs to advanced multi-agent systems, RAG pipelines, and production deployment.

## 📖 Course Curriculum

### Foundation (Days 1-3)
- **Day 01**: LLM APIs and First Agent
  - Getting started with LLM APIs
  - Building your first AI agent
  - Basic agent patterns and workflows

- **Day 02**: Tool Calling and Function Agents
  - Understanding tool calling mechanisms
  - Building function-based agents
  - Integrating external tools and APIs

- **Day 03**: Agent Memory Systems
  - Implementing memory in agents
  - Memory types and management
  - Context windows and state handling

### RAG & Retrieval (Day 4)
- **Day 04**: Embeddings and RAG (Multiple Versions)
  - Embedding generation and management
  - Retrieval-Augmented Generation (RAG) fundamentals
  - LangChain framework deep dive
  - Vector similarity search and indexing

### Multi-Agent & Advanced (Days 5-8)
- **Day 05**: LangChain Agents and Tools
  - Advanced LangChain patterns
  - Agent chains and hierarchies
  - Tool orchestration

- **Day 06**: Multi-Agent with CrewAI
  - Introduction to CrewAI framework
  - Building multi-agent systems
  - Agent role definition and task assignment

- **Day 07**: Advanced Multi-Agent Architectures
  - Complex multi-agent patterns
  - Agent communication and coordination
  - Hierarchical and flat agent structures

- **Day 08**: LangGraph v1
  - LangGraph framework introduction
  - State machine design patterns
  - Graph-based agent workflows

### Autonomous & Complex (Days 9-11)
- **Day 09**: Autonomous Agents
  - Building agents that run autonomously
  - Planning and execution loops
  - Decision-making frameworks

- **Day 10**: RAG with Memory
  - Combining RAG with memory systems
  - Long-term and short-term memory
  - Context management in RAG

- **Day 11**: Evaluation
  - Evaluating agent performance
  - Metrics and benchmarks
  - Faithfulness scoring and answer quality

### Production Ready (Days 12-13)
- **Day 12**: Deployment v6
  - Deployment strategies and patterns
  - Containerization and scaling
  - Production considerations

- **Day 13**: Capstone Project
  - Full end-to-end application
  - Integrating all learned concepts
  - Real-world project implementation

## 🚀 How to Use This Material

### Prerequisites
- Python 3.10+
- Jupyter/JupyterLab
- Dependencies specified in main project's `requirements.txt`

### Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/23053912-pixel/llm-tutor.git
   cd llm-tutor
   ```

2. **Set up environment**
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
   pip install jupyter jupyterlab
   ```

4. **Start Jupyter**
   ```bash
   jupyter lab
   ```

5. **Navigate to course material**
   - Open `Agentic AI Course Material/Agentic AI Course Material/`
   - Start with `day01_*.ipynb`

### Learning Path

**Beginner**: Days 1-3 + Day 4
- Build foundational knowledge
- Understand agent basics
- Learn RAG fundamentals

**Intermediate**: Days 5-8
- Advanced agent patterns
- Multi-agent systems
- LangGraph workflows

**Advanced**: Days 9-11
- Autonomous systems
- Complex architectures
- Evaluation frameworks

**Project-Based**: Day 12-13
- Real-world deployment
- Capstone implementation

## 📊 Topics Covered

### Core Concepts
- ✅ LLM APIs and integrations
- ✅ Agent design patterns
- ✅ Tool calling and function execution
- ✅ Memory systems and state management
- ✅ Retrieval-Augmented Generation (RAG)

### Advanced Topics
- ✅ Multi-agent architectures
- ✅ CrewAI framework
- ✅ LangGraph state machines
- ✅ Autonomous agent loops
- ✅ Hierarchical agent systems

### Production Topics
- ✅ Evaluation and metrics
- ✅ Deployment strategies
- ✅ Scaling considerations
- ✅ Vector databases
- ✅ Caching and optimization

## 🔧 Technologies & Frameworks

| Framework | Topics |
|-----------|--------|
| **LangChain** | Agent building, chains, tools |
| **LangGraph** | State machines, graph workflows |
| **CrewAI** | Multi-agent orchestration |
| **Streamlit** | UI/Frontend (capstone) |
| **Groq** | Fast LLM inference |
| **ChromaDB** | Vector database for RAG |
| **Sentence Transformers** | Embeddings generation |

## 💡 Key Takeaways

After completing this course, you will understand:

1. **Agent Architecture**: How to design and build AI agents
2. **Multi-Agent Systems**: Creating systems with multiple specialized agents
3. **RAG Pipelines**: Implementing retrieval-augmented generation
4. **State Management**: Handling agent memory and context
5. **Production Deployment**: Taking systems from development to production
6. **Evaluation**: Assessing agent performance and reliability

## 📝 Notes

- Each notebook contains executable code and explanations
- Run notebooks in order for best understanding
- Notebooks include exercises for hands-on learning
- Day 13 (Capstone) integrates all previous concepts
- See main `README.md` for project setup and API keys

## 🎯 Common Projects to Build

After this course, consider building:
- Research Assistant  (Days 1-4)
- Multi-Document QA    (Days 4-7)
- Code Review Agent    (Days 3, 5-6)
- Data Analysis Pipeline (Days 2, 8+)
- Autonomous Workflow System (Days 9-12)
- Production RAG App    (Days 4, 10-12)

## 🤝 Contributing

Found improvements? Submit issues or PRs to the main repository.

## 📞 Support

For questions about the course material:
- Check notebook markdown cells for explanations
- Refer to main `README.md` for setup issues
- Open GitHub issues for bugs or clarifications

---

**Creator**: Prashant Bhandari  
**Repository**: [llm-tutor on GitHub](https://github.com/23053912-pixel/llm-tutor)  
**Last Updated**: April 2026
