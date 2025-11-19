import streamlit as st
import requests
import json
from datetime import datetime

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Chatbot with Multi-Agent & RAG")

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "use_rag" not in st.session_state:
    st.session_state.use_rag = False
if "use_multi_agent" not in st.session_state:
    st.session_state.use_multi_agent = False

with st.sidebar:
    st.header("⚙️ Settings")
    
    st.session_state.use_rag = st.toggle("📚 Use RAG (Documents)", value=st.session_state.use_rag)
    st.session_state.use_multi_agent = st.toggle("🤝 Use Multi-Agent", value=st.session_state.use_multi_agent)
    
    st.divider()
    
    st.subheader("📤 Upload Document")
    uploaded_file = st.file_uploader("Choose file", type=['txt', 'pdf', 'docx'])
    
    if uploaded_file and st.button("Upload"):
        files = {"file": uploaded_file}
        try:
            response = requests.post(f"{API_URL}/files/upload", files=files)
            if response.status_code == 200:
                st.success(f"✅ Uploaded: {uploaded_file.name}")
            else:
                st.error(f"❌ Upload failed: {response.text}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    st.divider()
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.conversation_id = None
        st.rerun()
    
    st.divider()
    
    st.caption("💡 Tips:")
    st.caption("• Toggle RAG to use uploaded documents")
    st.caption("• Multi-Agent routes to specialists")
    st.caption("• Code requests → Code Agent")
    st.caption("• Questions → Research Agent")
    st.caption("• Summaries → Summary Agent")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            st.caption(f"📚 Sources: {', '.join(message['sources'])}")
        if "agents" in message and message["agents"]:
            st.caption(f"🤖 Agents: {', '.join(message['agents'])}")

if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                payload = {
                    "message": prompt,
                    "conversation_id": st.session_state.conversation_id,
                    "use_rag": st.session_state.use_rag,
                    "use_multi_agent": st.session_state.use_multi_agent
                }
                
                response = requests.post(
                    f"{API_URL}/chat/send",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    st.markdown(data["response"])
                    
                    if data.get("sources"):
                        st.caption(f"📚 Sources: {', '.join(data['sources'])}")
                    
                    if data.get("agents_used"):
                        st.caption(f"🤖 Agents: {', '.join(data['agents_used'])}")
                    
                    st.session_state.conversation_id = data["conversation_id"]
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": data["response"],
                        "sources": data.get("sources"),
                        "agents": data.get("agents_used")
                    })
                else:
                    st.error(f"❌ Error: {response.text}")
            
            except Exception as e:
                st.error(f"❌ Connection error: {str(e)}")
                st.info("💡 Make sure backend is running on port 8000")