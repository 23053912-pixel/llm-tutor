import streamlit as st
import os
import uuid
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize session state for API key if not present
if 'groq_api_key' not in st.session_state:
    st.session_state.groq_api_key = os.environ.get('GROQ_API_KEY', '')

# Set the API key from session_state to environment
if st.session_state.groq_api_key:
    os.environ['GROQ_API_KEY'] = st.session_state.groq_api_key

from agent import create_agent
from kb_data import documents
import chromadb
from langchain_groq import ChatGroq
from sentence_transformers import SentenceTransformer

# ─── Page Config ───
st.set_page_config(
    page_title="LLM Tutor — Learn About Large Language Models",
    page_icon="🧠",
    layout="wide"
)

# ─── Custom CSS to match the dark premium UI ───
st.markdown("""
<style>
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Dark background */
    .stApp {
        background-color: #0f1117;
    }

    /* Hero gradient card */
    .hero-card {
        background: linear-gradient(135deg, #1a5c4c 0%, #2d8b74 30%, #c96b3c 70%, #d4845a 100%);
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 24px;
        color: white;
    }
    .hero-card h1 {
        font-size: 28px;
        font-weight: 700;
        margin: 0 0 8px 0;
        color: white;
    }
    .hero-card p {
        font-size: 14px;
        margin: 4px 0;
        color: rgba(255,255,255,0.9);
    }
    .hero-card .deadline {
        font-weight: 600;
        color: #ffe0c0;
    }

    /* Suggestion cards row */
    .suggestion-row {
        display: flex;
        gap: 12px;
        margin-bottom: 24px;
    }
    .suggestion-card {
        flex: 1;
        background: linear-gradient(135deg, #1a3a4a 0%, #1a4a3a 50%, #3a2a1a 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 16px;
        cursor: pointer;
        transition: transform 0.2s, border-color 0.2s;
    }
    .suggestion-card:hover {
        transform: translateY(-2px);
        border-color: rgba(255,255,255,0.2);
    }
    .suggestion-card h3 {
        font-size: 14px;
        font-weight: 600;
        color: #e0e0e0;
        margin: 0 0 6px 0;
    }
    .suggestion-card p {
        font-size: 12px;
        color: #888;
        margin: 0;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #21262d;
    }
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #e6edf3;
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li {
        color: #8b949e;
    }

    /* Trace expander styling */
    .streamlit-expanderHeader {
        font-size: 13px;
        color: #8b949e;
    }
</style>
""", unsafe_allow_html=True)

# ─── System Init (cached) ───
@st.cache_resource
def load_system(api_key=''):
    if not api_key:
        return None, len(documents)
    
    embedder = SentenceTransformer('all-MiniLM-L6-v2')

    chroma_client = chromadb.Client()
    try:
        chroma_client.delete_collection(name="course_kb")
    except Exception:
        pass
    collection = chroma_client.create_collection(name="course_kb")

    texts = [doc['text'] for doc in documents]
    ids = [doc['id'] for doc in documents]
    metadatas = [{'topic': doc['topic']} for doc in documents]
    embeddings = embedder.encode(texts).tolist()

    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

    try:
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, api_key=api_key)
    except Exception as e:
        st.error(f"Failed to initialize GROQ API: {str(e)}")
        return None, len(documents)

    app = create_agent(llm, embedder, collection)
    return app, len(documents)

app, kb_count = load_system(st.session_state.groq_api_key)

# ─── Session State ───
if 'thread_id' not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())[:8]
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_trace' not in st.session_state:
    st.session_state.current_trace = None

# ─── Deadline Countdown ───
def get_deadline_info():
    deadline = datetime(2026, 4, 21, 23, 59, 0, tzinfo=timezone(timedelta(hours=5, minutes=30)))
    now = datetime.now(tz=timezone(timedelta(hours=5, minutes=30)))
    diff = deadline - now
    if diff.total_seconds() <= 0:
        return "Deadline has passed!"
    days = diff.days
    hours = diff.seconds // 3600
    return f"{days} days and {hours} hours left until the capstone submission window closes on 21 Apr 2026, 11:59 PM IST."

# ─── Sidebar ───
with st.sidebar:
    st.markdown("### Session")
    st.markdown(f"**Thread ID:** `{st.session_state.thread_id}`")
    st.markdown(f"**Knowledge base documents:** {kb_count}")
    st.markdown("**Model provider:** groq")
    st.markdown("**Model:** llama-3.3-70b-versatile")
    st.markdown("**Embedder:** all-MiniLM-L6-v2")

    st.markdown("---")
    st.markdown("### 📚 Topics Covered")
    st.markdown("Comprehensive guide to understanding and working with Large Language Models:")
    topics = [doc['topic'] for doc in documents]
    for t in topics:
        st.markdown(f"- {t}")

    st.markdown("---")
    if st.button("New conversation", use_container_width=True):
        st.session_state.thread_id = str(uuid.uuid4())[:8]
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("### 🔐 API Configuration")
    
    if not st.session_state.groq_api_key:
        st.warning("⚠️ GROQ API Key not configured")
        api_key_input = st.text_input("Enter your Groq API Key:", type="password", key="api_key_input")
        if api_key_input:
            if api_key_input.startswith('gsk_'):
                st.session_state.groq_api_key = api_key_input
                os.environ['GROQ_API_KEY'] = api_key_input
                st.success("✅ API Key set successfully!")
                st.rerun()
            else:
                st.error("❌ Invalid API key format. Groq keys start with 'gsk_'")
    else:
        st.success("✅ API Key configured")
        if st.button("Change API Key", use_container_width=True):
            st.session_state.groq_api_key = ''
            os.environ['GROQ_API_KEY'] = ''
            st.cache_resource.clear()
            st.rerun()

# ─── Hero Card ───
deadline_text = get_deadline_info()
st.markdown(f"""
<div class="hero-card">
    <h1>🧠 LLM Tutor</h1>
    <p>Your interactive guide to understanding Large Language Models, from architecture to real-world applications.</p>
    <p class="deadline">Powered by Llama 3.3 70B • Retrieval-Augmented • RAG-Enhanced Responses</p>
</div>
""", unsafe_allow_html=True)

# ─── Suggestion Cards ───
st.markdown("""
<div class="suggestion-row">
    <div class="suggestion-card">
        <h3>🏗️ Architecture & Theory</h3>
        <p>Try: Explain how transformer architecture and attention mechanisms work in LLMs.</p>
    </div>
    <div class="suggestion-card">
        <h3>🎯 Practical Applications</h3>
        <p>Try: What are the real-world applications of large language models?</p>
    </div>
    <div class="suggestion-card">
        <h3>🚀 LLM Trends & Future</h3>
        <p>Try: What are the emerging trends and future direction of LLMs?</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Two Column Layout: Chat + Processing ───
col_chat, col_process = st.columns([1.2, 1], gap="large")

with col_chat:
    st.markdown("### 💬 Conversation")
    
    # Chat History
    chat_container = st.container(height=400)
    with chat_container:
        for msg in st.session_state.messages:
            avatar = "🤖" if msg['role'] == "assistant" else "👤"
            with st.chat_message(msg['role'], avatar=avatar):
                st.markdown(msg['content'])
    
    # Chat Input
    st.markdown("---")
    if prompt := st.chat_input("Ask me about LLMs, training, evaluation, applications, or future trends..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user", avatar="👤"):
                st.markdown(prompt)

        with chat_container:
            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner("Processing..."):
                    if not st.session_state.groq_api_key:
                        st.error("❌ Please configure your GROQ API Key in settings.")
                    elif not app:
                        st.error("❌ Failed to initialize the AI system.")
                    else:
                        try:
                            result = app.invoke(
                                {"question": prompt},
                                config={"configurable": {"thread_id": st.session_state.thread_id}}
                            )
                            answer = result.get('answer', "I couldn't generate an answer.")
                            sources = result.get('sources', [])

                            # Display answer without sources in chat
                            st.markdown(answer)

                            trace_data = {
                                'route': result.get('route'),
                                'faithfulness': result.get('faithfulness'),
                                'sources': sources,
                                'eval_retries': result.get('eval_retries', 0)
                            }

                            # Store trace for right panel
                            st.session_state.current_trace = trace_data

                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": answer,
                                "trace": trace_data
                            })
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")

with col_process:
    st.markdown("### 🔍 Processing Details")
    
    if st.session_state.current_trace or (st.session_state.messages and st.session_state.messages[-1]['role'] == 'assistant'):
        # Get the latest trace
        trace = st.session_state.current_trace
        if not trace and st.session_state.messages:
            trace = st.session_state.messages[-1].get('trace', {})
        
        if trace:
            st.markdown("#### Information Retrieved")
            st.info(trace.get('route', 'Processing...'))
            
            st.markdown("#### Confidence Score")
            faithfulness = trace.get('faithfulness', 'N/A')
            if isinstance(faithfulness, (int, float)):
                score = min(100, int(faithfulness * 100)) if faithfulness <= 1 else int(faithfulness)
                st.metric("Faithfulness", f"{score}%")
            else:
                st.metric("Faithfulness", str(faithfulness))
            
            st.markdown("#### Sources Used")
            sources = trace.get('sources', [])
            if sources:
                for i, source in enumerate(sources, 1):
                    st.write(f"**{i}. {source}**")
            else:
                st.write("No specific sources referenced")
            
            st.markdown("#### Processing Info")
            st.write(f"**Retries:** {trace.get('eval_retries', 0)}")
        else:
            st.info("Processing details will appear here")
    else:
        st.info("💡 Start a conversation to see processing details")
