import streamlit as st
import random

# Modern CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0rem;
        margin-top: 0rem;
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
        transform: translateY(-2px) scale(1.1);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    .stButton {
        display: flex !important;
        justify-content: center !important;
        margin: 1rem auto !important;
        position: relative;
        width: fit-content !important;
    }
    .stButton::after {
        content: "👆";
        position: absolute;
        left: 50%;
        top: 100%;
        transform: translateX(-50%);
        font-size: 2.5rem;
        animation: pointDown 2s ease-in-out infinite;
        z-index: 10;
        margin-top: 10px;
    }
    @keyframes pointDown {
        0%, 100% { 
            transform: translateX(-50%) translateY(-20px);
            opacity: 0.7;
        }
        50% { 
            transform: translateX(-50%) translateY(5px);
            opacity: 1;
        }
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
    .main .block-container {
        padding-top: 0rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }
    .ceremonial-welcome {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.3rem;
        font-weight: 600;
        color: white;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
        margin: 1rem 0;
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    .image-container {
        margin: 0.4rem auto;
        max-width: 600px;
        text-align: center;
    }
    .image-container img {
        display: block;
        margin: 0 auto;
        max-width: 100%;
        height: auto;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">Big Important Meeting! 🚀</h1>', unsafe_allow_html=True)

# Add the Temple Bar image
st.markdown('<div class="image-container">', unsafe_allow_html=True)
st.image("https://templebarbcn.com/wp-content/uploads/2022/08/20-TempleMyBar_by_WitekPhotography_RECORTADA-1024x576.jpg", 
         caption="Temple Bar Barcelona - A beautiful bar experience")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="ceremonial-welcome">Glad to see you all here!</div>', unsafe_allow_html=True)

name = "FRIENDS"
st.markdown('<div style="display: flex; justify-content: center; width: 100%;">', unsafe_allow_html=True)
if st.button("Greet"):
    # Add some fun greetings
    greetings = [
        f"Hello, {name}! 👋",
        f"Hey there, {name}! 😊",
        f"Greetings, {name}! 🌟",
        f"Nice to meet you, {name}! 🤝"
    ]
    st.markdown(f'<div class="success-message">{random.choice(greetings)}</div>', unsafe_allow_html=True)
    st.balloons()  # Add some celebration!
st.markdown('</div>', unsafe_allow_html=True)