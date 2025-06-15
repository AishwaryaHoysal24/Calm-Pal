import streamlit as st
import google.generativeai as genai
import os
import base64
from dotenv import load_dotenv
import time
import html

# Load environment variable
load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# ============ Background Setup ============

def set_background(image_file):
    with open(image_file, "rb") as f:
        base64_img = base64.b64encode(f.read()).decode()
    css_code = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{base64_img}");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        font-family: 'Segoe UI', sans-serif;
    }}

    .title-text {{
        color: #333;
        font-size: 40px;
        font-weight: 700;
        text-align: center;
        margin-top: 1rem;
    }}

    .subtitle-text {{
        color: #555;
        font-size: 18px;
        font-style: italic;
        text-align: center;
        margin-bottom: 2rem;
    }}

    .chat-container {{
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 20px;
        margin: 20px auto;
        max-height: 450px;
        overflow-y: auto;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        width: 85%;
    }}

    .stChatMessage {{
        background-color: transparent !important;
    }}

    .stChatMessage[data-testid="user-message"] {{
        background: linear-gradient(135deg, #6dd5fa, #2980b9) !important;
        color: white !important;
        border-radius: 18px 18px 0px 18px !important;
        margin: 10px 0 !important;
        padding: 12px 20px !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
    }}

    .stChatMessage[data-testid="assistant-message"] {{
        background: #f1f1f1 !important;
        color: #333 !important;
        border-radius: 18px 18px 18px 0px !important;
        margin: 10px 0 !important;
        padding: 12px 20px !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05) !important;
        border-left: 5px solid #81b29a !important;
    }}

    .stButton > button {{
        border-radius: 25px;
        background: #81b29a;
        color: white;
        padding: 10px 20px;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
    }}

    .stButton > button:hover {{
        background: #6b9080;
        transform: translateY(-1px);
    }}

    .clear-button {{
        background-color: #e07a5f !important;
    }}

    .clear-button:hover {{
        background-color: #d65a31 !important;
    }}

    .empty-chat {{
        text-align: center;
        color: #555;
        font-style: italic;
        padding: 40px 20px;
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        margin: 20px auto;
        width: 85%;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    }}

    /* Frosted translucent input bar */
    .stChatInput {{
        background-color: rgba(255, 255, 255, 0.3) !important;
        border-radius: 25px !important;
        backdrop-filter: blur(10px) !important;
        border: 1.5px solid #81b29a !important;
        padding: 10px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }}

    .stChatInput input, .stChatInput textarea {{
        background-color: transparent !important;
        color: #333 !important;
        font-size: 16px !important;
        border-radius: 25px !important;
        padding: 10px 18px !important;
    }}

    .stChatInput input::placeholder,
    .stChatInput textarea::placeholder {{
        color: #666 !important;
        opacity: 0.8;
    }}

    .stChatInput input:focus {{
        border-color: #6b9080 !important;
        box-shadow: 0 0 0 2px rgba(107,144,128,0.25) !important;
        background-color: rgba(255, 255, 255, 0.4) !important;
    }}

    hr {{
        display: none !important;
    }}

    .stMarkdown hr {{
        display: none !important;
    }}
    </style>
    """
    st.markdown(css_code, unsafe_allow_html=True)

# ✅ Background setup
set_background("Background1.jpeg")

# ============ Header =============
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("Logo.jpg", width=90)

st.markdown('<div class="title-text">CalmPal</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">Because your mental health matters 💜</div>', unsafe_allow_html=True)

# ============ Gemini Response Logic ============

def generate_response(user_msg):
    try:
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")
        system_prompt = """You are CalmPal, a supportive and empathetic mental health chatbot.
        Your role is to provide comfort, encouragement, and helpful suggestions for mental wellness.
        Always be kind, understanding, and non-judgmental. If someone seems to be in crisis,
        gently suggest they reach out to a mental health professional or crisis helpline.
        Keep responses warm, supportive, and conversational."""
        prompt = f"{system_prompt}\n\nUser: {user_msg}\n\nCalmPal:"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Sorry, I'm having trouble responding right now. (Error: {str(e)})"

# ============ Timestamp ============

def get_timestamp():
    return time.strftime("%H:%M")

# ============ Clear Button ============
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("Clear Chat", key="clear_chat"):
        st.session_state.messages = []
        st.rerun()

# ============ Chat Display ============
if not st.session_state.messages:
    st.markdown("""
    <div class="empty-chat">
        👋 Hey there! I'm <b>CalmPal</b>, your mental health companion.<br>
        How are you feeling today? I'm here to listen.💬
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "assistant"
        with st.chat_message(role):
            if msg["role"] == "assistant":
                st.write(f"**CalmPal:** {msg['content']}")
            else:
                st.write(msg['content'])
            st.caption(f"⏰ {msg['time']}")

# ============ Chat Input & Disclaimer ============
if prompt := st.chat_input("Message CalmPal..."):
    current_time = get_timestamp()
    st.session_state.messages.append({"role": "user", "content": prompt, "time": current_time})

    with st.spinner("CalmPal is thinking..."):
        bot_reply = generate_response(prompt)

    st.session_state.messages.append({"role": "assistant", "content": bot_reply, "time": get_timestamp()})
    st.rerun()

# 💬 Disclaimer just below the input
st.markdown("""
<div style="text-align: center; color: #555; font-size: 12px; opacity: 0.8; margin-top: 12px;">
    💙 Remember: You're not alone. If you're in crisis, reach out to a mental health professional or helpline.
</div>
""", unsafe_allow_html=True)
