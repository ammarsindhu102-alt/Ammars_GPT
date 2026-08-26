import streamlit as st
from groq import Groq

# 1. Page Configuration (Strictly Ammars_GPT Branding)
st.set_page_config(page_title="Ammars_GPT", page_icon="🤖", layout="centered")

# Visual tweaks to remove Streamlit's default header padding
st.markdown("""
    <style>
    .block-container {padding-top: 2rem;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Ammars_GPT")
st.caption("Welcome! I am Ammars_GPT, a custom AI assistant built by Ammar.")

# 2. Establish Secure Connection with Groq
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=groq_api_key)
except Exception:
    st.error("Setup Error: Missing Groq API Key! Please configure it in your Streamlit secrets management panel.")
    st.stop()

# 3. System Prompt (Hardcodes the AI's identity so it never breaks character)
SYSTEM_PROMPT = {
    "role": "system",
    "content": "You are Ammars_GPT, a highly intelligent, precise, and friendly AI assistant created by Ammar. Always maintain this identity and mention your name when greeting users."
}

# 4. Initialize Active Conversation Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Display Previous Chat Stream
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Monitor and Process User Input
if user_input := st.chat_input("Ask Ammars_GPT anything..."):
    # Append user message to display logs
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 7. Request Real-time Processing from Groq
    with st.chat_message("assistant"):
        # Combine System identity prompt with chronological chat context
        api_messages = [SYSTEM_PROMPT] + [
            {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
        ]
        
        # Pull response using Llama-3.3-70b (Fastest open-source model available)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=api_messages,
            stream=True
        )
        
        # Generator function for a dynamic visual typing effect
        def parse_stream():
            for chunk in completion:
                if chunk.choices.delta.content:
                    yield chunk.choices.delta.content
                    
        response = st.write_stream(parse_stream())
        
    # Commit the AI's final answer to memory session
    st.session_state.messages.append({"role": "assistant", "content": response})
