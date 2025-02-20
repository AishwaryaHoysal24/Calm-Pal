import streamlit as st
import google.generativeai as genai
import os
import base64

# Set up Google Gemini API Key
os.environ["GOOGLE_API_KEY"] = "AIzaSyCvcZYhTr4w3PKhP4Tym8yLx-PAR5hGZ9g"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Function to set background image to cover the full screen
def set_background(image_file):
    with open(image_file, "rb") as f:
        base64_str = base64.b64encode(f.read()).decode()
    
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{base64_str}");
        background-size: cover;  /* Makes sure the image covers the whole screen */
        background-repeat: no-repeat;
        background-position: center center;  /* Centers the image */
        background-attachment: fixed;  /* Keeps the background fixed while scrolling */
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Apply background image (Replace 'background.jpg' with your image file)

set_background("background_3.jpg")

# Function to get response from Gemini API
def generate_response(user_message):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(user_message)
    return response.text  # Extract the text response

# Streamlit App UI
st.image("Logo.jpg", width=100)  # Adjust width as needed
st.title("CalmPal - Mental Health Chatbot")
st.write("**Because your mental health matters 🧠**")

user_input = st.text_input("You: ", "")

if st.button("Send"):
    if user_input:
        response = generate_response(user_input)
        st.text_area("CalmPal:", response, height=200)
    else:
        st.warning("Please enter a message.")