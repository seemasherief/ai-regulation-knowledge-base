import streamlit as st
import os
from documents import load_all_documents
from rag import build_knowledge_base, ask_question

st.set_page_config(
    page_title="AI Regulation Knowledge Base",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ AI Regulation Knowledge Base")
st.markdown("### Powered by Claude (Anthropic)")
st.markdown("Ask any question about global AI regulations — EU AI Act, GDPR, CCPA, UK AI Framework, UNESCO AI Ethics, and the US Executive Order on AI.")

# Load documents once
@st.cache_resource
def initialize():
    with st.spinner("Loading official regulatory documents..."):
        documents = load_all_documents()
        collection, all_chunks, all_metadata = build_knowledge_base(documents)
        return collection, all_chunks, all_metadata

collection, all_chunks, all_metadata = initialize()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Example questions
st.markdown("#### Try these questions:")
col1, col2 = st.columns(2)

with col1:
    if st.button("What AI systems are prohibited under the EU AI Act?"):
        st.session_state.pending_question = "What AI systems are prohibited under the EU AI Act?"
    if st.button("What rights do individuals have under GDPR?"):
        st.session_state.pending_question = "What rights do individuals have under GDPR?"
    if st.button("What does the US Executive Order say about AI safety?"):
        st.session_state.pending_question = "What does the US Executive Order say about AI safety?"

with col2:
    if st.button("How does CCPA protect California residents?"):
        st.session_state.pending_question = "How does CCPA protect California residents?"
    if st.button("What are the key principles of the UK AI Framework?"):
        st.session_state.pending_question = "What are the key principles of the UK AI Framework?"
    if st.button("What are UNESCO's core AI ethics principles?"):
        st.session_state.pending_question = "What are UNESCO's core AI ethics principles?"

# Display chat history
st.markdown("---")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle pending question from buttons
if "pending_question" in st.session_state and st.session_state.pending_question:
    question = st.session_state.pending_question
    st.session_state.pending_question = None

    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching regulations..."):
            answer, sources = ask_question(question, collection, all_chunks, all_metadata)
        st.markdown(answer)
        st.markdown(f"**Sources:** {', '.join(set(sources))}")
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"{answer}\n\n**Sources:** {', '.join(set(sources))}"
        })

# Chat input
if question := st.chat_input("Ask any question about AI regulations..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching regulations..."):
            answer, sources = ask_question(question, collection, all_chunks, all_metadata)
        st.markdown(answer)
        st.markdown(f"**Sources:** {', '.join(set(sources))}")
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"{answer}\n\n**Sources:** {', '.join(set(sources))}"
        })

# Clear chat button
if st.session_state.messages:
    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()