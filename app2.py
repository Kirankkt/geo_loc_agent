import streamlit as st
import google.generativeai as genai
from PIL import Image
import pytesseract
import io
import os

# Configure Google Gemini API Key
os.environ["GOOGLE_API_KEY"] = "AIzaSyBy791VYFuQjFIkCTV_ELBkGKIsv17wH_M"  # Replace with your key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to extract visible text using OCR
def extract_text(image_bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes))
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        return f"Error extracting text: {str(e)}"

# Function to analyze image with Gemini API
def analyze_image(image_bytes, extracted_text):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Convert image bytes to PIL Image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Enhanced prompt for better analysis
        prompt = f"""
        You are an expert geographer. Analyze the image carefully and provide the most specific location information possible:
        - Architectural style, buildings, and landmarks.
        - Vegetation, natural features (e.g., mountains, rivers, coastlines).
        - Traffic, road layout, and visible vehicles.
        - Any visible text, signage, or billboards. Extracted text: "{extracted_text}".
        - Cultural aspects like clothing styles, street markets, or festivals.
        
        Return your response in this format:
        - **Most Likely Location**: City, State, Country (or region if applicable)
        - **Reasoning**: Explain the clues that led you to this conclusion, including the architectural style, vegetation, visible text, or cultural details.
        """

        # Generate content with streaming
        response = model.generate_content([prompt, image], stream=True)
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

    # Extract visible text using OCR
    st.write("Extracting visible text... 📝")
    extracted_text = extract_text(image_bytes)
    if extracted_text:
        st.write("**Extracted Text:**", extracted_text)
    else:
        st.write("No text found in the image.")

    # Analyze image with Gemini API
    st.write("Analyzing image... ⏳")
    result = analyze_image(image_bytes, extracted_text)
    st.write("### Analysis Result 🧭")
    st.markdown(result)
