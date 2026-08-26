import streamlit as st
from groq import Groq

# 1. Page Configuration
st.set_page_config(page_title="Ammars_GPT", page_icon="⚫", layout="centered")

# Custom CSS for an ultra-premium, forced dark theme and clean layout
st.markdown("""
    <style>
    /* Remove padding and hide default UI garbage */
    .block-container { padding-top: 1.5rem !important; max-width: 720px !important; }
    footer { visibility: hidden !important; }
    header { visibility: hidden !important; }
    #MainMenu { visibility: hidden !important; }
    
    /* Strict Dark Mode Overrides */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #0b0b0f !important;
        color: #e3e3e6 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Aesthetic Logo Styling */
    .logo-container {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 0.5rem;
    }
    .logo-text {
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        background: linear-gradient(135deg, #ffffff 30%, #a3a3a3 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .custom-caption {
        color: #8e8e93 !font-family: inherit;
        font-size: 0.95rem;
        margin-bottom: 2.5rem;
    }
    
    /* Clean ChatGPT style Chat Inputs */
    [data-testid="stChatInput"] {
        background-color: #16161a !important;
        border: 1px solid #232329 !important;
        border-radius: 14px !important;
    }
    [data-testid="stChatInput"] textarea {
        color: #e3e3e6 !important;
    }
    
    /* Strip away avatars, spacing, borders, and backgrounds from chat logs */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding-left: 0px !important;
        padding-right: 0px !important;
        margin-top: 1rem !important;
    }
    /* Hide the residual avatar container entirely to preserve strict alignment */
    [data-testid="stChatMessageAvatarContainer"] {
        display: none !important;
    }
    /* Smooth line spacing for readable paragraphs */
    [data-testid="stChatMessageContent"] {
        padding-top: 0px !important;
        font-size: 1.05rem !important;
        line-height: 1.65 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Aesthetic Custom SVG Logo Header System
st.markdown("""
    <div class="logo-container">
        <svg width="40" height="40" viewBox="0 0 100 100" fill="none" xmlns="http://w3.org">
            <defs>
                <linearGradient id="logo-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#ffffff"/>
                    <stop offset="100%" stop-color="#3a3a3c"/>
                </linearGradient>
            </defs>
            <circle cx="50" cy="50" r="44" stroke="url(#logo-grad)" stroke-width="8" fill="none"/>
            <circle cx="50" cy="50" r="20" fill="url(#logo-grad)"/>
        </svg>
        <span class="logo-text">Ammars_GPT</span>
    </div>
    <div class="custom-caption">A minimalist, custom AI companion built by Ammar.</div>
""", unsafe_allow_html=True)

# 3. Establish Secure Connection with Groq
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=groq_api_key)
except Exception:
    st.error("Setup Error: Missing Groq API Key! Please configure it in your Streamlit secrets management panel.")
    st.stop()

# 4. System Prompt
SYSTEM_PROMPT = {
    "role": "system",
    "content": "You are Ammars_GPT, a highly intelligent, precise, and friendly AI assistant created by Ammar. Always maintain this identity and mention your name when greeting users."
}

# 5. Initialize Active Conversation Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# 6. Display Previous Chat Stream (Avatar hidden globally via CSS)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. Monitor and Process User Input
if user_input := st.chat_input("Ask Ammars_GPT..."):
    # Append user message to display logs
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 8. Request Real-time Processing from Groq
    with st.chat_message("assistant"):
        # Combine System identity prompt with chronological chat context
        api_messages = [SYSTEM_PROMPT] + [
            {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
        ]
        
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=api_messages,
            stream=True
        )
        
        # High performance Stream parser
        def parse_stream():
            for chunk in completion:
                if chunk.choices and chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    
        response = st.write_stream(parse_stream())
      
    # Commit the AI's final answer to memory session
    st.session_state.messages.append({"role": "assistant", "content": response})

