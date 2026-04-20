import os
import re
from typing import TypedDict, List, Dict, Any
from datetime import datetime
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage

# Define State
class CapstoneState(TypedDict):
    question: str
    messages: List[Any]
    route: str
    retrieved: str
    sources: List[str]
    tool_result: str
    answer: str
    faithfulness: float
    eval_retries: int
    user_name: str

def create_agent(llm, embedder, collection):

    # Node 1: memory_node
    def memory_node(state: CapstoneState):
        question = state.get('question', '')
        messages = state.get('messages', [])
        user_name = state.get('user_name', '')

        match = re.search(r'my name is\s+([A-Za-z]+)', question, re.IGNORECASE)
        if match:
            user_name = match.group(1).title()

        messages = messages + [HumanMessage(content=question)]
        messages = messages[-6:]  # sliding window

        return {
            'messages': messages,
            'user_name': user_name,
            'eval_retries': 0,
            'tool_result': '',
            'retrieved': '',
            'sources': [],
            'faithfulness': 0.0,
            'route': ''
        }

    # Node 2: router_node
    def router_node(state: CapstoneState):
        question = state['question']
        sys_prompt = """You are a routing agent for an LLM Tutorial Assistant.
Classify the user question into EXACTLY ONE of the three routes below. Reply with ONE WORD only.
- 'retrieve': The user is asking about LLM concepts (transformers, attention, training, fine-tuning, embeddings, RAG, safety, alignment, models, applications, or any technical topic related to large language models).
- 'tool': The user is asking for the current date, current time, or any question requiring live date/time computation.
- 'skip': The user is making casual conversation (e.g., hello, thanks, how are you), referencing previous messages, or asking something completely out of scope (e.g., sports, cooking recipes, medical advice).
Reply only with: retrieve, tool, or skip."""
        response = llm.invoke([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": question}
        ])
        route = response.content.strip().lower()
        if route not in ['retrieve', 'tool', 'skip']:
            route = 'retrieve'  # default
        return {'route': route}

    # Node 3: retrieval_node
    def retrieval_node(state: CapstoneState):
        question = state['question']
        q_emb = embedder.encode([question]).tolist()
        results = collection.query(query_embeddings=q_emb, n_results=3)

        context_str = ""
        sources = []
        if results['documents'] and len(results['documents']) > 0:
            doc_texts = results['documents'][0]
            doc_metas = results['metadatas'][0]
            for i, txt in enumerate(doc_texts):
                topic = doc_metas[i].get('topic', 'Unknown')
                context_str += f"[{topic}]\n{txt}\n\n"
                sources.append(topic)

        return {'retrieved': context_str, 'sources': sources}

    # Node 4: skip_retrieval_node
    def skip_retrieval_node(state: CapstoneState):
        return {'retrieved': '', 'sources': []}

    # Node 5: tool_node
    def tool_node(state: CapstoneState):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tool_res = f"The current date and time is {now}."
        return {'tool_result': tool_res}

    # Node 6: answer_node
    def answer_node(state: CapstoneState):
        question = state['question']
        retrieved = state.get('retrieved', '')
        tool_result = state.get('tool_result', '')
        user_name = state.get('user_name', '')
        history = "\n".join([m.content for m in state.get('messages', [])[:-1]])

        sys_prompt = "You are LLM Tutor — an expert educational assistant that teaches about Large Language Models, their architecture, training, applications, and future trends."
        if user_name:
            sys_prompt += f" Address the user as {user_name}."

        sys_prompt += (
            "\n\nIMPORTANT RULES:\n"
            "1. ONLY use information from the provided KNOWLEDGE BASE context below.\n"
            "2. If the context does not contain the answer, or the question is completely out of scope "
            "(like cooking recipes, sports scores), say clearly 'I do not have that information in my knowledge base. "
            "This might be outside my training scope about LLMs.' DO NOT hallucinate.\n"
            "3. Answer in a clear, educational, friendly tone. Use examples and bullet points to explain complex concepts.\n"
            "4. When citing sources, mention which topic document or section you drew from.\n"
            "5. For LLM-related questions, provide both theoretical understanding and practical context."
        )

        if state.get('eval_retries', 0) > 0:
            sys_prompt += "\n\nWARNING: Your previous answer was not well-grounded in the context. Try again and stick strictly to the provided context."

        sys_prompt += f"\n\nKNOWLEDGE BASE CONTEXT:\n{retrieved}"
        if tool_result:
            sys_prompt += f"\n\nTOOL RESULT:\n{tool_result}"
        if history:
            sys_prompt += f"\n\nCHAT HISTORY:\n{history}"

        response = llm.invoke([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": question}
        ])

        return {'answer': response.content}

    # Node 7: eval_node
    def eval_node(state: CapstoneState):
        if not state.get('retrieved', '').strip():
            # Skip check for memory-only / out-of-scope queries
            return {'faithfulness': 1.0, 'eval_retries': state.get('eval_retries', 0)}

        eval_prompt = f"""Evaluate the faithfulness of the following answer based strictly on the provided context.
Does the answer only contain information found in the context? Ignore greetings.
Give it a score between 0.0 and 1.0, where 1.0 is perfectly faithful and 0.0 is completely hallucinated.
Reply with ONLY the floating point number.

CONTEXT:
{state['retrieved']}

ANSWER:
{state['answer']}"""
        response = llm.invoke([{"role": "user", "content": eval_prompt}])
        try:
            score = float(response.content.strip())
        except ValueError:
            score = 0.5

        retries = state.get('eval_retries', 0) + 1
        return {'faithfulness': score, 'eval_retries': retries}

    # Node 8: save_node
    def save_node(state: CapstoneState):
        messages = state['messages']
        messages = messages + [AIMessage(content=state['answer'])]
        return {'messages': messages}

    # Routing edges
    def route_decision(state: CapstoneState):
        r = state['route']
        if r == 'tool': return 'tool'
        if r == 'skip': return 'skip'
        return 'retrieve'

    def eval_decision(state: CapstoneState):
        score = state.get('faithfulness', 0.0)
        retries = state.get('eval_retries', 0)
        if score < 0.7 and retries < 2:
            return 'answer'  # retry
        return 'save'

    # Build Graph
    graph = StateGraph(CapstoneState)
    graph.add_node('memory', memory_node)
    graph.add_node('router', router_node)
    graph.add_node('retrieve', retrieval_node)
    graph.add_node('skip', skip_retrieval_node)
    graph.add_node('tool', tool_node)
    graph.add_node('answer', answer_node)
    graph.add_node('eval', eval_node)
    graph.add_node('save', save_node)

    graph.set_entry_point('memory')

    graph.add_edge('memory', 'router')
    graph.add_conditional_edges('router', route_decision, {'retrieve': 'retrieve', 'skip': 'skip', 'tool': 'tool'})
    graph.add_edge('retrieve', 'answer')
    graph.add_edge('skip', 'answer')
    graph.add_edge('tool', 'answer')
    graph.add_edge('answer', 'eval')
    graph.add_conditional_edges('eval', eval_decision, {'answer': 'answer', 'save': 'save'})
    graph.add_edge('save', END)

    app = graph.compile(checkpointer=MemorySaver())
    return app
