import streamlit as st
import os
import sys
import uuid
from datetime import datetime, timezone, timedelta

# ─── Load API Key ───
# First try .env file in current directory
from dotenv import load_dotenv
load_dotenv(override=True)

api_key = os.environ.get('GROQ_API_KEY', '')

# Fallback to Streamlit secrets if running on cloud
if not api_key:
    try:
        api_key = st.secrets.get("GROQ_API_KEY", "")
    except:
        pass

# Ensure API key is available for all imports
if api_key:
    os.environ['GROQ_API_KEY'] = api_key

# Now import dependencies
from agent import create_agent
from kb_data import documents
import chromadb
from langchain_groq import ChatGroq
from sentence_transformers import SentenceTransformer
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage

# ─── Page Config ───
st.set_page_config(
    page_title="LLM Tutor — Learn About Large Language Models",
    page_icon="🧠",
    layout="wide"
)

# ─── Check for API Key ───
if not api_key:
    st.error("""
    ### ⚠️ API Key Not Configured
    
    The application requires a Groq API key to function.
    
    **For Streamlit Cloud:**
    1. Go to your deployment settings
    2. Click "Secrets" and add:
       ```
       GROQ_API_KEY = "your_api_key_here"
       ```
    3. Redeploy the app
    
    **For Local Use:**
    1. Create `.streamlit/secrets.toml` with your API key
    2. Or create `.env` file with `GROQ_API_KEY=your_api_key`
    
    Get a free API key: https://console.groq.com
    """)
    st.stop()

# ─── Custom CSS for Study & Focus Friendly Theme ───
st.markdown("""
<style>
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Light background - study friendly */
    .stApp {
        background-color: #f8f9fa;
    }

    /* Main container */
    .main {
        background-color: #ffffff;
    }

    /* Hero card - soft and professional */
    .hero-card {
        background: linear-gradient(135deg, #4a6fa5 0%, #7ba3c0 100%);
        border-radius: 12px;
        padding: 24px 28px;
        margin-bottom: 24px;
        color: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
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
        color: rgba(255,255,255,0.95);
    }

    /* Suggestion cards - clean and minimal */
    .suggestion-row {
        display: flex;
        gap: 12px;
        margin-bottom: 24px;
    }
    .suggestion-card {
        flex: 1;
        background: linear-gradient(135deg, #e8f0f7 0%, #f0f5fa 100%);
        border: 2px solid #cbd5e0;
        border-radius: 10px;
        padding: 16px;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .suggestion-card:hover {
        transform: translateY(-2px);
        border-color: #4a6fa5;
        box-shadow: 0 4px 12px rgba(74, 111, 165, 0.15);
        background: linear-gradient(135deg, #dfe8f5 0%, #e8f0fa 100%);
    }
    .suggestion-card h3 {
        font-size: 14px;
        font-weight: 600;
        color: #2d3748;
        margin: 0 0 6px 0;
    }
    .suggestion-card p {
        font-size: 12px;
        color: #718096;
        margin: 0;
    }

    /* Sidebar styling - clean and readable */
    section[data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 1px solid #e2e8f0;
    }
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #2d3748;
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li {
        color: #4a5568;
    }

    /* Chat messages - readable and clean */
    .stChatMessage {
        background-color: #ffffff;
    }

    /* Text styling for better readability */
    body, p, li, div {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
        letter-spacing: 0.3px;
    }

    /* Links - soft blue */
    a {
        color: #4a6fa5 !important;
        text-decoration: none;
    }
    a:hover {
        color: #2d4058 !important;
        text-decoration: underline;
    }

    /* Code blocks - soft background */
    code {
        background-color: #f0f4f8 !important;
        color: #2d3748 !important;
        border-radius: 4px;
        padding: 2px 6px;
    }

    /* Buttons - soft and professional */
    .stButton > button {
        background-color: #4a6fa5;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #3a5a8f;
        box-shadow: 0 2px 8px rgba(74, 111, 165, 0.2);
    }

    /* Alert boxes - soft colors */
    .stAlert {
        border-radius: 8px;
    }

    /* Input fields - clean */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border: 1px solid #cbd5e0 !important;
        border-radius: 6px !important;
        background-color: #ffffff !important;
        color: #2d3748 !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #4a6fa5 !important;
    }

    /* Expanders - soft styling */
    .streamlit-expanderHeader {
        font-size: 14px;
        color: #2d3748;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# ─── System Init (cached) ───
@st.cache_resource
def load_system():
    """Load the AI system once and cache it"""
    try:
        api_key_check = os.environ.get('GROQ_API_KEY', '')
        if not api_key_check:
            st.error("⚠️ GROQ_API_KEY not configured")
            return None, len(documents), None, None
        
        # Load embedder
        embedder = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Create ChromaDB
        chroma_client = chromadb.Client()
        try:
            chroma_client.delete_collection(name="course_kb")
        except:
            pass
        collection = chroma_client.create_collection(name="course_kb")
        
        # Load documents
        texts = [doc['text'] for doc in documents]
        ids = [doc['id'] for doc in documents]
        metadatas = [{'topic': doc['topic']} for doc in documents]
        
        # Generate embeddings
        embeddings = embedder.encode(texts).tolist()
        
        # Add to ChromaDB
        collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        
        # Initialize LLM
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            api_key=api_key_check
        )
        
        # Create agent
        app = create_agent(llm, embedder, collection)
        
        return app, len(documents), embedder, collection
        
    except Exception as e:
        st.error(f"❌ System initialization error: {str(e)}")
        return None, len(documents), None, None


app, kb_count, embedder, collection = load_system()

# ─── Session State ───
if 'thread_id' not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())[:8]
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_trace' not in st.session_state:
    st.session_state.current_trace = None
if 'pending_query' not in st.session_state:
    st.session_state.pending_query = None

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
    st.markdown("### ✅ Status")
    
    if api_key:
        st.success("✅ API Key Configured\n\nReady to use!")
    else:
        st.error("❌ API Key Missing\n\nPlease set GROQ_API_KEY in .env file")

# ─── Hero Card ───
deadline_text = get_deadline_info()
st.markdown(f"""
<div class="hero-card">
    <h1>🧠 LLM Tutor</h1>
    <p>Your interactive guide to understanding Large Language Models, from architecture to real-world applications.</p>
    <p class="deadline">Powered by Llama 3.3 70B • Retrieval-Augmented • RAG-Enhanced Responses</p>
</div>
""", unsafe_allow_html=True)

# ─── Helper function to process queries ───
def process_query(prompt):
    """Process a query and add response to chat"""
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        if not api_key:
            st.error("❌ Please configure your GROQ API Key.")
        elif not app:
            st.error("❌ Failed to initialize AI system.")
        else:
            try:
                with st.spinner("Processing..."):
                    result = app.invoke(
                        {"question": prompt},
                        config={"configurable": {"thread_id": st.session_state.thread_id}}
                    )
                    answer = result.get('answer', "I couldn't generate an answer.")
                    sources = result.get('sources', [])

                    st.markdown(answer)

                    trace_data = {
                        'route': result.get('route'),
                        'faithfulness': result.get('faithfulness'),
                        'sources': sources,
                        'eval_retries': result.get('eval_retries', 0)
                    }

                    st.session_state.current_trace = trace_data

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "trace": trace_data
                    })
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ─── Suggestion Cards with Functionality ───
if not st.session_state.messages:  # Only show if no conversation started
    st.markdown("#### 🎯 Quick Start Examples:")
    
    suggestions = [
        {
            "title": "🏗️ Architecture & Theory",
            "query": "Explain how transformer architecture and attention mechanisms work in LLMs.",
            "key": "arch"
        },
        {
            "title": "🎯 Practical Applications", 
            "query": "What are the real-world applications of large language models?",
            "key": "app"
        },
        {
            "title": "🚀 LLM Trends & Future",
            "query": "What are the emerging trends and future direction of LLMs?",
            "key": "trends"
        }
    ]
    
    cols = st.columns(3, gap="small")
    for col, sugg in zip(cols, suggestions):
        with col:
            if st.button(f"{sugg['title']}\n\n💬 Try →", use_container_width=True, key=f"sugg_{sugg['key']}"):
                process_query(sugg['query'])
                st.rerun()

# ─── Chat Layout ───
st.markdown("### 💬 Chat")

# Chat History Display
for msg in st.session_state.messages:
    avatar = "🤖" if msg['role'] == "assistant" else "👤"
    with st.chat_message(msg['role'], avatar=avatar):
        st.markdown(msg['content'])

# Chat Input
st.markdown("---")

if prompt := st.chat_input("Ask me about LLMs..."):
    process_query(prompt)
