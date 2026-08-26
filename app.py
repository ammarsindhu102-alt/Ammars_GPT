import streamlit as st
from groq import Groq

# 1. Page Configuration
st.set_page_config(page_title="Ammars_GPT", page_icon="⚪", layout="centered")

# Visual tweaks to remove Streamlit's default header padding and permanently KILL icons/gaps
st.markdown("""
    <style>
    /* Remove default layout spacing */
    .block-container { padding-top: 1.5rem !important; max-width: 720px !important; }
    footer { visibility: hidden !important; }
    header { visibility: hidden !important; }
    #MainMenu { visibility: hidden !important; }
    
    /* Forced Deep Dark Mode Background */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #08080c !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Ultra-Aesthetic Header Branding Layout */
    .logo-container {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 0.4rem;
    }
    .logo-text {
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.8px;
        color: #ffffff !important;
    }
    .custom-caption {
        color: #82828c !important;
        font-size: 0.95rem;
        margin-bottom: 2.5rem;
    }
    
    /* Clean Minimalist Chat Input Box */
    [data-testid="stChatInput"] {
        background-color: #121216 !important;
        border: 1px solid #22222a !important;
        border-radius: 14px !important;
    }
    [data-testid="stChatInput"] textarea {
        color: #ffffff !important;
    }
    
    /* Strip away background shading, borders, and margins from chat blocks */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding: 0px !important;
        margin: 0px !important;
        margin-top: 1.2rem !important;
    }
    
    /* ABSOLUTE ICON KILL SWITCH: Nuke every variation of Streamlit's avatar containers */
    [data-testid="stChatMessageAvatarContainer"],
    [data-testid="chatAvatarContainer"],
    .stChatMessage div[style*="width:"],
    div[class*="ChatMessageAvatarContainer"],
    div[class*="chatAvatarContainer"] {
        display: none !important;
        width: 0px !important;
        height: 0px !important;
        max-width: 0px !important;
        min-width: 0px !important;
        margin: 0px !important;
        padding: 0px !important;
        visibility: hidden !important;
    }
    
    /* COMPACT FLUSH LAYOUT: Ensure the remaining text sits perfectly left-aligned without gaps */
    [data-testid="stChatMessageContent"],
    div[class*="ChatMessageContent"] {
        margin-left: 0px !important;
        padding-left: 0px !important;
        padding-top: 0px !important;
        width: 100% !important;
    }
    
    /* Force BOTH User and Assistant message text to be BRIGHT WHITE */
    [data-testid="stChatMessageContent"], 
    [data-testid="stChatMessageContent"] p, 
    [data-testid="stChatMessageContent"] span {
        color: #ffffff !important;
        font-size: 1.05rem !important;
        line-height: 1.7 !important;
        font-weight: 400 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Modern Geometric Abstract Logo
st.markdown("""
    <div class="logo-container">
        <svg width="42" height="42" viewBox="0 0 100 100" fill="none" xmlns="http://w3.org">
            <defs>
                <linearGradient id="glow-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#ffffff" stop-opacity="1"/>
                    <stop offset="50%" stop-color="#888888" stop-opacity="0.8"/>
                    <stop offset="100%" stop-color="#111111" stop-opacity="0.3"/>
                </linearGradient>
            </defs>
            <polygon points="50,5 93,30 93,80 50,95 7,80 7,30" stroke="url(#glow-grad)" stroke-width="2" stroke-linejoin="round" fill="none" opacity="0.3"/>
            <polygon points="50,15 80,35 80,70 50,85 20,70 20,35" stroke="url(#glow-grad)" stroke-width="4" stroke-linejoin="round" fill="none"/>
            <line x1="50" y1="15" x2="50" y2="85" stroke="#ffffff" stroke-width="1.5" opacity="0.5"/>
            <line x1="20" y1="35" x2="80" y2="70" stroke="#ffffff" stroke-width="1.5" opacity="0.5"/>
            <line x1="20" y1="70" x2="80" y2="35" stroke="#ffffff" stroke-width="1.5" opacity="0.5"/>
            <circle cx="50" cy="50" r="7" fill="#ffffff"/>
        </svg>
        <span class="logo-text">Ammars_GPT</span>
    </div>
    <div class="custom-caption">A clean, high-performance intelligence gateway built by Ammar.</div>
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

# 6. Display Previous Chat Stream
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. Monitor and Process User Input
if user_input := st.chat_input("Ask Ammars_GPT..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 8. Request Real-time Processing from Groq (Using gpt-oss model)
    with st.chat_message("assistant"):
        api_messages = [SYSTEM_PROMPT] + [
            {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
        ]
        
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=api_messages,
            stream=True
        )
        
        # FIXED: Stream parser explicitly indexing choices[0]
        def parse_stream():
            for chunk in completion:
                if chunk.choices and chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    
        response = st.write_stream(parse_stream())
      
    st.session_state.messages.append({"role": "assistant", "content": response})
