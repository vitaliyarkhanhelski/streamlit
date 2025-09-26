import streamlit as st
import random

# Modern CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    .stTextInput > div > div > input {
        border-radius: 15px;
        border: 2px solid #e0e0e0;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 15px rgba(102, 126, 234, 0.4);
        outline: none;
    }
    .stTextInput > div {
        border: none !important;
        box-shadow: none !important;
    }
    .stTextInput > div > div {
        border: none !important;
        box-shadow: none !important;
    }
    .success-message {
        background: linear-gradient(90deg, #56ab2f 0%, #a8e6cf 100%);
        padding: 1rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
        animation: slideIn 0.5s ease-in;
    }
    @keyframes slideIn {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">Hello Streamlit 🚀</h1>', unsafe_allow_html=True)
st.write("This is my first Streamlit app!")

name = st.text_input("Enter your name:")
if st.button("Greet"):
    if name:
        # Check if name is not a number
        if name.isdigit():
            st.error("Please enter a real name, not just numbers! 😅")
        else:
            # Add some fun greetings
            greetings = [
                f"Hello, {name}! 👋",
                f"Hey there, {name}! 😊",
                f"Greetings, {name}! 🌟",
                f"Nice to meet you, {name}! 🤝"
            ]
            st.markdown(f'<div class="success-message">{random.choice(greetings)}</div>', unsafe_allow_html=True)
            st.balloons()  # Add some celebration!
    else:
        st.warning("Please enter your name first! 😅")