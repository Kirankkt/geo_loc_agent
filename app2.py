import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# Configure Google Gemini API Key
os.environ["GOOGLE_API_KEY"] = "AIzaSyBy791VYFuQjFIkCTV_ELBkGKIsv17wH_M"  # Replace with your key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

from PIL import Image
import io

def analyze_image(image_bytes):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Generate content with streaming
        response = model.generate_content(
            [
                "You are a geography expert. Analyze the image to guess the location and provide reasoning.",
                image
            ],
            stream=True
        )
        
        # Resolve the response to accumulate text
        response.resolve()
        
        # Return the final text output
        return response.text
    
    except Exception as e:
        return f"Error: {str(e)}"



# Streamlit UI
st.title("Geography Identification AI 🌍")
st.write("Upload a location image, and I'll analyze it to guess the location!")

# File upload
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)


    # Convert image to bytes
    image_bytes = uploaded_file.getvalue()

    # Analyze image
    st.write("Analyzing image... ⏳")
    result = analyze_image(image_bytes)
    st.write("### Analysis Result 🧭")
    st.markdown(result)
