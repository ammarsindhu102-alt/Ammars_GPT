import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(
    page_title="⚡ Groq AI Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Hide Streamlit Footer, Header, and Menu
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
# App Header
st.title("⚡ Ultra-Fast AI Assistant")
st.markdown("created by Ammar")

# Sidebar for API Key & Settings
with st.sidebar:
    st.header("Configuration")
    
    # Secure API key input (checks Streamlit secrets first, falls back to manual input)
    api_key = st.secrets.get("GROQ_API_KEY")
    if not api_key:
        api_key = st.text_input("Enter Groq API Key", type="password")
        st.markdown("[Get a free Groq API key here](https://console.groq.com)")
    
    # Model Selection
    model_choice = st.selectbox(
        "Select Model",
        [
            "openai/gpt-oss-120b",
            "openai/gpt-oss-20b",
            "qwen/qwen3.8-27b"
        ],
        index=0
    )
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Validat
if not api_key:
    st.warning("⚠️ Please provide your Groq API Key in the sidebar or via Streamlit secrets to start chatting.")
    st.stop()

# Initialize Groq Client
client = Groq(api_key=api_key)

# Initialize Chat History in Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Prior Chat Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Chat Input
if prompt := st.chat_input("What would you like to know?"):
    # Append user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display assistant response with streaming
    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model=model_choice,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            
            # Stream the response chunks in real-time
            response = st.write_stream(
                chunk.choices[0].delta.content or "" 
                for chunk in stream
            )
            
            # Save assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
