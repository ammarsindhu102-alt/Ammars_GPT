import streamlit as st
from groq import Groq

# 1. Page Configuration (Initializes the app window metrics)
st.set_page_config(
    page_title="Ammars_GPT", 
    page_icon="✨", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Complete Visual Theme Overhaul (Injects clean CSS stylings)
st.html("""
    <style>
    /* Completely mask default Streamlit structural frames and footers */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stAppDeployButton {display: none !important;}
    
    /* Global Background and Canvas Settings */
    .stApp {
        background-color: #1e1e1e !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
    }
    
    /* Central Column Framework Padding */
    .block-container {
        max-width: 720px !important;
        padding-top: 5rem !important; 
        padding-bottom: 7rem !important;
    }
    
    /* Fixed Upper Branding Header Container */
    .top-brand-banner {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background-color: rgba(30, 30, 30, 0.95);
        backdrop-filter: blur(8px);
        padding: 0.75rem 1.5rem;
        border-bottom: 1px solid #2d2d2d;
        z-index: 999999;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    /* Custom Inline SVG Minimal Graphic */
    .aesthetic-logo {
        width: 22px;
        height: 22px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .top-brand-text {
        color: #ffffff !important;
        font-size: 1.05rem !important;
        font-weight: 500 !important;
        letter-spacing: -0.2px;
    }
    .top-brand-badge {
        color: #9b9b9b !important;
        font-size: 0.75rem !important;
        background-color: #2d2d2d;
        padding: 2px 8px;
        border-radius: 12px;
        font-weight: 400;
    }
    
    /* Conversational Layout Configurations */
    div[data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding: 1.25rem 0.5rem !important;
        color: #e3e3e3 !important;
    }
    
    /* Distinct User Profile Message Shading */
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatar"] img[alt="user"]) {
        background-color: #2d2d2d !important;
        border-radius: 20px !important;
        padding-left: 1.25rem !important;
        padding-right: 1.25rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Input Form Elements Alignment */
    div[data-testid="stChatInput"] {
        background-color: #2d2d2d !important;
        border: 1px solid #3c3c3c !important;
        border-radius: 26px !important;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.15) !important;
    }
    div[data-testid="stChatInput"] textarea {
        color: #e3e3e3 !important;
    }
    
    /* Collapsible Side Panel Overrides */
    [data-testid="stSidebar"] {
        background-color: #141414 !important;
        border-right: 1px solid #2d2d2d !important;
    }
    
    /* Empty State Splash Banner */
    .welcome-container {
        text-align: center;
        margin-top: 20vh !important;
        margin-bottom: 3rem !important;
    }
    .welcome-title {
        color: #ffffff !important;
        font-size: 2.1rem !important;
        font-weight: 500 !important;
        letter-spacing: -0.5px;
    }
    .welcome-subtitle {
        color: #9b9b9b !important;
        font-size: 0.95rem !important;
        margin-top: 0.5rem;
    }
    </style>
""")

# 3. Mount Permanent Branding Navigation Bar
st.markdown("""
    <div class="top-brand-banner">
        <div class="aesthetic-logo">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://w3.org" style="width: 100%; height: 100%;">
                <circle cx="12" cy="12" r="9" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round" stroke-dasharray="4 2"/>
                <polygon points="12,7 16,15 8,15" fill="none" stroke="#ffffff" stroke-width="1.5" stroke-linejoin="round"/>
            </svg>
        </div>
        <div class="top-brand-text">Ammars_GPT</div>
        <div class="top-brand-badge">Official</div>
    </div>
""", unsafe_allow_html=True)

# 4. Check for Security Access Parameters
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=groq_api_key)
except Exception:
    st.error("Missing Security Credentials. Please configure your Groq API Key.")
    st.stop()

# 5. Continuous Session Cache Initializer
if "messages" not in st.session_state:
    st.session_state.messages = []

# 6. Display Splash Prompt (Only visible if the workspace log is blank)
if len(st.session_state.messages) == 0:
    st.markdown("""
        <div class="welcome-container">
            <div class="welcome-title">How can I help you today?</div>
            <div class="welcome-subtitle">Your personal secure AI companion</div>
        </div>
    """, unsafe_allow_html=True)

# 7. Render Cached Dialogue Context
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 8. Monitor User Actions & Execute Inference Sequences
if user_input := st.chat_input("Message Ammars_GPT..."):
    # Clear splash layout on initial message payload engagement
    if len(st.session_state.messages) == 0:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.rerun()
        
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        # System instructions enforcing the core bot profile parameters
        SYSTEM_PROMPT = {
            "role": "system",
            "content": "You are Ammars_GPT, an intelligent, helpful, and highly sophisticated personal AI assistant engineered by Ammar. Keep your responses crisp, conversational, and direct. Do not say your name or repeat your setup details in every single sentence."
        }
        
        # Build request parameters array
        api_messages = [SYSTEM_PROMPT] + [
            {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
        ]
        
        # Launch token generation process block
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=api_messages,
            stream=True
        )
        
        # Safe stream extraction callback loop
        def parse_stream():
            for chunk in completion:
                if chunk.choices and chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    
        response = st.write_stream(parse_stream())
        
    st.session_state.messages.append({"role": "assistant", "content": response})
    import streamlit as st
from groq import Groq

# 1. Page Configuration (Initializes the app window metrics)
st.set_page_config(
    page_title="Ammars_GPT", 
    page_icon="✨", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Complete Visual Theme Overhaul (Injects clean CSS stylings)
st.html("""
    <style>
    /* Completely mask default Streamlit structural frames and footers */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stAppDeployButton {display: none !important;}
    
    /* Global Background and Canvas Settings */
    .stApp {
        background-color: #1e1e1e !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
    }
    
    /* Central Column Framework Padding */
    .block-container {
        max-width: 720px !important;
        padding-top: 5rem !important; 
        padding-bottom: 7rem !important;
    }
    
    /* Fixed Upper Branding Header Container */
    .top-brand-banner {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background-color: rgba(30, 30, 30, 0.95);
        backdrop-filter: blur(8px);
        padding: 0.75rem 1.5rem;
        border-bottom: 1px solid #2d2d2d;
        z-index: 999999;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    /* Custom Inline SVG Minimal Graphic */
    .aesthetic-logo {
        width: 22px;
        height: 22px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .top-brand-text {
        color: #ffffff !important;
        font-size: 1.05rem !important;
        font-weight: 500 !important;
        letter-spacing: -0.2px;
    }
    .top-brand-badge {
        color: #9b9b9b !important;
        font-size: 0.75rem !important;
        background-color: #2d2d2d;
        padding: 2px 8px;
        border-radius: 12px;
        font-weight: 400;
    }
    
    /* Conversational Layout Configurations */
    div[data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding: 1.25rem 0.5rem !important;
        color: #e3e3e3 !important;
    }
    
    /* Distinct User Profile Message Shading */
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatar"] img[alt="user"]) {
        background-color: #2d2d2d !important;
        border-radius: 20px !important;
        padding-left: 1.25rem !important;
        padding-right: 1.25rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Input Form Elements Alignment */
    div[data-testid="stChatInput"] {
        background-color: #2d2d2d !important;
        border: 1px solid #3c3c3c !important;
        border-radius: 26px !important;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.15) !important;
    }
    div[data-testid="stChatInput"] textarea {
        color: #e3e3e3 !important;
    }
    
    /* Collapsible Side Panel Overrides */
    [data-testid="stSidebar"] {
        background-color: #141414 !important;
        border-right: 1px solid #2d2d2d !important;
    }
    
    /* Empty State Splash Banner */
    .welcome-container {
        text-align: center;
        margin-top: 20vh !important;
        margin-bottom: 3rem !important;
    }
    .welcome-title {
        color: #ffffff !important;
        font-size: 2.1rem !important;
        font-weight: 500 !important;
        letter-spacing: -0.5px;
    }
    .welcome-subtitle {
        color: #9b9b9b !important;
        font-size: 0.95rem !important;
        margin-top: 0.5rem;
    }
    </style>
""")

# 3. Mount Permanent Branding Navigation Bar
st.markdown("""
    <div class="top-brand-banner">
        <div class="aesthetic-logo">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://w3.org" style="width: 100%; height: 100%;">
                <circle cx="12" cy="12" r="9" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round" stroke-dasharray="4 2"/>
                <polygon points="12,7 16,15 8,15" fill="none" stroke="#ffffff" stroke-width="1.5" stroke-linejoin="round"/>
            </svg>
        </div>
        <div class="top-brand-text">Ammars_GPT</div>
        <div class="top-brand-badge">Official</div>
    </div>
""", unsafe_allow_html=True)

# 4. Check for Security Access Parameters
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=groq_api_key)
except Exception:
    st.error("Missing Security Credentials. Please configure your Groq API Key.")
    st.stop()

# 5. Continuous Session Cache Initializer
if "messages" not in st.session_state:
    st.session_state.messages = []

# 6. Display Splash Prompt (Only visible if the workspace log is blank)
if len(st.session_state.messages) == 0:
    st.markdown("""
        <div class="welcome-container">
            <div class="welcome-title">How can I help you today?</div>
            <div class="welcome-subtitle">Your personal secure AI companion</div>
        </div>
    """, unsafe_allow_html=True)

# 7. Render Cached Dialogue Context
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 8. Monitor User Actions & Execute Inference Sequences
if user_input := st.chat_input("Message Ammars_GPT..."):
    # Clear splash layout on initial message payload engagement
    if len(st.session_state.messages) == 0:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.rerun()
        
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        # System instructions enforcing the core bot profile parameters
        SYSTEM_PROMPT = {
            "role": "system",
            "content": "You are Ammars_GPT, an intelligent, helpful, and highly sophisticated personal AI assistant engineered by Ammar. Keep your responses crisp, conversational, and direct. Do not say your name or repeat your setup details in every single sentence."
        }
        
        # Build request parameters array
        api_messages = [SYSTEM_PROMPT] + [
            {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
        ]
        
        # Launch token generation process block
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=api_messages,
            stream=True
        )
        
        # Safe stream extraction callback loop
        def parse_stream():
            for chunk in completion:
                if chunk.choices and chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    
        response = st.write_stream(parse_stream())
        
    st.session_state.messages.append({"role": "assistant", "content": response})
