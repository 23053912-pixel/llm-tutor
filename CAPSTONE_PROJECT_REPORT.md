# CAPSTONE PROJECT REPORT
## LLM Tutor: Agentic AI Educational Assistant

**Course:** Agentic AI Hands-On Course  
**Project Domain:** Large Language Model Education  
**Prepared For:** Capstone submission  
**Prepared From Repository State:** April 21, 2026  
**Primary Files Reviewed:** [agent.py](agent.py), [capstone_streamlit.py](capstone_streamlit.py), [kb_data.py](kb_data.py), [day13_capstone.ipynb](day13_capstone.ipynb)

## Executive Summary

This project implements **LLM Tutor**, an educational assistant that answers questions about large language models using a LangGraph-based workflow, a ChromaDB knowledge base, session memory, a datetime tool, and a Streamlit interface. The report is organized to follow the structure taught in the **Agentic AI Project Guidance** document and the submission-oriented expectations referenced by the capstone guidelines.

The implementation is grounded in the repository's actual code rather than template text. For this report, the project was verified in two ways:

- static review of the codebase and notebook
- live Groq-backed checks run on April 21, 2026 for retrieval, tool use, memory, and red-team behavior

## 1. Session Guidance Alignment

### 1.1 Framing and Expectations

The course guidance emphasized that the notebook is the working space and the `.py` files are the product. This repository follows that pattern:

- [day13_capstone.ipynb](day13_capstone.ipynb) contains the guided capstone flow
- [agent.py](agent.py) contains the deployable LangGraph agent
- [capstone_streamlit.py](capstone_streamlit.py) contains the user-facing application
- [kb_data.py](kb_data.py) contains the domain knowledge base

The selected domain is **LLM education**, with the goal of providing grounded, multi-turn answers to learners who need a single place to study architecture, training, evaluation, safety, and applications of LLM systems.

### 1.2 Six Mandatory Capabilities

| Capability | Current Implementation | Evidence |
|---|---|---|
| LangGraph StateGraph | 8-node workflow: `memory`, `router`, `retrieve`, `skip`, `tool`, `answer`, `eval`, `save` | [agent.py](agent.py) |
| ChromaDB RAG (10+ docs) | 15 domain documents embedded with `all-MiniLM-L6-v2` and queried with top-3 retrieval | [kb_data.py](kb_data.py), [capstone_streamlit.py](capstone_streamlit.py) |
| MemorySaver + `thread_id` | `MemorySaver` is used in graph compilation and `st.session_state.thread_id` is passed into `app.invoke()` | [agent.py](agent.py), [capstone_streamlit.py](capstone_streamlit.py) |
| Self-reflection eval node | `eval_node` scores faithfulness from `0.0` to `1.0` and can send low-scoring answers back through `answer_node` | [agent.py](agent.py) |
| Tool use beyond retrieval | `tool_node` returns current date and time for time-aware questions | [agent.py](agent.py) |
| Streamlit deployment | Cached system initialization, session state, chat UI, sidebar, and new conversation reset | [capstone_streamlit.py](capstone_streamlit.py) |

### 1.3 Architecture Demonstrated

```text
User question
  -> memory_node
  -> router_node
  -> retrieve_node | skip_retrieval_node | tool_node
  -> answer_node
  -> eval_node
  -> save_node
  -> END
```

Key design choices:

- `memory_node` keeps a sliding window of the last 6 messages and extracts a user name when provided
- `router_node` selects among `retrieve`, `tool`, or `skip`
- `retrieval_node` queries the vector store and formats context with topic labels
- `answer_node` combines knowledge base context, tool result, and chat history
- `eval_node` checks grounding and supports a retry loop for low-faithfulness answers

### 1.4 Red-Teaming Alignment

The course guidance required testing out-of-scope, false-premise, hallucination bait, and prompt-injection scenarios. During live verification for this report:

- prompt injection request: the assistant refused to reveal the system prompt
- harmful request: the assistant refused help with illegal activity and redirected back to the project scope
- memory test: the assistant correctly recalled a user name from earlier in the session

## 2. Problem Statement

### Domain

Large Language Model education and guided self-study.

### Target Users

- students learning core LLM concepts
- developers who need a compact conceptual reference
- beginners exploring agentic AI workflows

### Problem

Learners often study LLMs through fragmented sources: research papers, blog posts, scattered tutorials, and product marketing. That creates three recurring problems:

1. important concepts are spread across multiple places
2. generic chatbots can answer confidently without grounding
3. follow-up questions lose context if the system does not preserve session memory

### Success Criteria

- answer LLM-domain questions using a curated knowledge base
- support multi-turn learning through persisted session memory
- route time/date questions to a tool instead of hallucinating
- refuse out-of-scope or unsafe requests clearly
- provide a usable web interface for interactive study

### Tool Choice and Justification

The chosen tool is a **datetime tool**. This meets the capstone requirement for tool use beyond retrieval and handles questions such as the current date and time without depending on the knowledge base.

## 3. Project Process - 8 Parts

### Part 1: Domain Setup and Knowledge Base

The project uses 15 documents stored in [kb_data.py](kb_data.py). The topics include:

- LLM fundamentals
- transformer architecture and attention
- pretraining and fine-tuning
- prompt engineering
- RAG
- evaluation and RAGAS-related concepts
- safety and alignment
- applications, future trends, cost, LoRA, benchmarks, pitfalls, and scaling laws

The app initializes a `SentenceTransformer('all-MiniLM-L6-v2')`, creates an in-memory ChromaDB collection, encodes all documents, and adds them with topic metadata. Retrieval uses top-3 semantic search.

Representative live retrieval check from this report session:

| Question | Observed Route | Faithfulness | Retrieved Topics |
|---|---|---:|---|
| "Explain retrieval augmented generation in simple terms." | `retrieve` | 0.80 | Retrieval Augmented Generation (RAG), What are Large Language Models (LLMs), Transformer Architecture and Attention Mechanism |

### Part 2: State Design

The project defines a `CapstoneState` `TypedDict` before graph construction, matching the course guidance. The current fields are:

- `question`
- `messages`
- `route`
- `retrieved`
- `sources`
- `tool_result`
- `answer`
- `faithfulness`
- `eval_retries`
- `user_name`

This state is sufficient for routing, retrieval, memory, evaluation, and personalized follow-up handling.

### Part 3: Node Functions

The graph is implemented as eight explicit nodes:

| Node | Purpose |
|---|---|
| `memory_node` | Appends the latest question, trims history to the last 6 messages, and extracts a user name when present |
| `router_node` | Uses the LLM to choose `retrieve`, `tool`, or `skip` |
| `retrieval_node` | Embeds the query, retrieves top-3 chunks from ChromaDB, and formats topic-tagged context |
| `skip_retrieval_node` | Returns empty retrieval context for casual or out-of-scope turns |
| `tool_node` | Returns the current date and time |
| `answer_node` | Generates the final response using context, tool output, and prior chat history |
| `eval_node` | Scores answer faithfulness and increments retry count |
| `save_node` | Appends the assistant response back into message history |

### Part 4: Graph Assembly

The graph is assembled with conditional routing after both `router_node` and `eval_node`:

- `route_decision()` maps the route to `retrieve`, `skip`, or `tool`
- `eval_decision()` either retries through `answer` or sends the response to `save`
- the graph is compiled with `MemorySaver()`

One implementation detail worth noting for accuracy: the current code retries once after a low faithfulness score because `eval_retries` is incremented inside `eval_node` and the loop continues only while `eval_retries < 2`. This still provides a self-reflection loop, but it is slightly stricter than the notebook wording that mentions two retries.

### Part 5: Testing and Verification

The capstone guidance asks for domain tests, red-team tests, and memory checks. For this report, the following live checks were executed against the working agent:

| Scenario | Expected Behavior | Observed Result |
|---|---|---|
| RAG explanation | Retrieve KB context and answer from sources | `route=retrieve`, faithfulness `0.80`, relevant topics retrieved |
| Current date/time | Use tool path | `route=tool`, faithfulness `1.00`, correct tool-driven answer |
| Casual greeting | Skip retrieval | `route=skip`, faithfulness `1.00`, friendly domain-scoped greeting |
| Memory recall | Remember earlier name in same `thread_id` | Correctly answered "Your name is Prashant." |
| Prompt injection | Refuse to reveal system prompt | Refused and explained prompt-injection defense |
| Harmful request | Refuse unsafe or illegal guidance | Refused assistance and stated the request was outside project scope |

Additional representative domain checks:

| Question | Observed Route | Faithfulness |
|---|---|---:|
| "What is LoRA and why is it useful?" | `retrieve` | 0.98 |
| "How do transformers use attention?" | `retrieve` | 0.80 |

Automated testing note:

- the repository contains [tests/test_basic.py](tests/test_basic.py), but the active Python interpreter in this environment did not have `pytest` installed
- `unittest` discovery found no runnable cases because the file uses pytest-style functions
- as a result, the report relies on direct live verification and code inspection instead of a full local automated test run

### Part 6: Evaluation

The repository is set up for RAG evaluation:

- `ragas` is listed in [requirements.txt](requirements.txt)
- Part 6 of [day13_capstone.ipynb](day13_capstone.ipynb) includes a 5-question evaluation scaffold
- the notebook also includes a fallback manual faithfulness scoring path if `ragas` is unavailable

However, the exact baseline mean scores were **not stored in a verifiable output artifact** inside the repository, and the notebook's written summary still contains placeholders for final numbers. To keep this report accurate, no unverified RAGAS averages are claimed here.

What was verified live during report preparation:

- sample retrieval answers produced faithfulness scores of `0.80`, `0.98`, and `0.80` on representative domain questions
- tool and skip-path questions returned `1.00` because the evaluator skips retrieval-less turns

If the final submission requires a numeric RAGAS table, the recommended next step is to run Part 6 in [day13_capstone.ipynb](day13_capstone.ipynb) and paste the resulting means into the exported PDF.

### Part 7: Deployment

The project includes a complete Streamlit frontend in [capstone_streamlit.py](capstone_streamlit.py). The implementation follows the deployment advice from the guidance:

- expensive initialization lives inside `@st.cache_resource`
- the app loads the Groq API key from `.env` first, then from Streamlit secrets
- `st.session_state` stores `thread_id`, message history, and current trace data
- a "New conversation" button resets the session thread
- the UI shows a topic sidebar, chat interface, and suggestion cards

The app passes `thread_id` into `app.invoke()` so conversation memory persists inside a session.

### Part 8: Written Summary and Reflection

The project meets the written-summary intent of the capstone by documenting:

- the chosen domain and users
- the role of the knowledge base
- the architecture and routing logic
- the use of memory and tool integration
- evaluation strategy
- future improvement ideas

Two strong improvement directions, both already suggested by the repository materials, are:

1. hybrid retrieval combining semantic search with keyword or BM25 search
2. real PDF ingestion instead of only hand-curated text documents

The most important engineering lesson from the current implementation is that grounding instructions and retrieval quality directly affect faithfulness. The memory window also improves user experience without letting the prompt grow uncontrollably.

## 4. Submission Notes

### Deliverables Present in the Repository

- [day13_capstone.ipynb](day13_capstone.ipynb)
- [agent.py](agent.py)
- [capstone_streamlit.py](capstone_streamlit.py)
- [kb_data.py](kb_data.py)
- [README.md](README.md)
- [CAPSTONE_PROJECT_REPORT.pdf](CAPSTONE_PROJECT_REPORT.pdf)

### Final Checks Recommended Before Submission

1. Run the notebook from top to bottom and replace any remaining placeholder text in the written-summary cells.
2. Run Part 6 evaluation and record final RAGAS values if your instructor expects numeric baselines in the report PDF.
3. Re-export the final report to PDF if the submission portal requires a 4-5 page document.
4. Verify any external GitHub or deployment URLs immediately before submission.

## Conclusion

LLM Tutor is a solid capstone implementation of an agentic educational assistant. It demonstrates the required LangGraph workflow, vector retrieval, session memory, self-evaluation, tool use, and a deployable Streamlit UI. Just as importantly, the repository shows a clear transition from guided notebook work to application code, which matches the core teaching goal of the capstone.

The project is strongest when it stays grounded in the curated LLM knowledge base and handles follow-up questions within the same session. The main remaining submission task is not architecture work; it is evidence finalization: rerun the notebook evaluation cells, replace placeholders, and export the final PDF version of this report.
