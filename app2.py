import os
import inspect  # To patch getargspec
from PIL import Image
from phi.agent import Agent
from phi.model.google import Gemini
from dotenv import load_dotenv
import streamlit as st
from phi.tools.duckduckgo import DuckDuckGo

# Monkey patch: Fix inspect.getargspec for compatibility with Python 3.12+
if not hasattr(inspect, 'getargspec'):
    inspect.getargspec = inspect.getfullargspec

# Load API Key from .env
load_dotenv()
GOOGLE_API_KEY = os.getenv("AIzaSyBy791VYFuQjFIkCTV_ELBkGKIsv17wH_M")

# Initialize Gemini agent
geo_agent = Agent(
    model=Gemini(id="gemini-1.5-flash"),
    tools=[DuckDuckGo()],
    markdown=True
)

# Geography Identification Query
query = """
You are a geography expert. Your task is to analyze the given image and provide a reasoned guess of the location based on visible clues such as:
- Landmarks
- Architecture
- Natural features (mountains, rivers, coastlines)
- Language or symbols (street signs, billboards, text in the picture)
- Clothing or cultural symbols
- Environmental clues like weather, time of day

Format response in:
**Location Name, City, Country** with detailed reasoning.
"""

# Streamlit UI
st.title("🌍 Geography Buddy")
st.write("Upload an image, and I'll guess the location based on visible clues!")

# Layout with two columns
col1, col2 = st.columns([1, 2])

# File uploader
uploaded_file = st.file_uploader("Upload an Image 🖼️", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open and resize the image
    image = Image.open(uploaded_file)
    resized_image = image.resize((500, 500))

    image_path = "temp_image.png"
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Display uploaded image
    col1.image(resized_image, caption="Uploaded Image", use_column_width=True)

    # Submit button
    if col2.button("🚀 Submit"):
        col2.info("Analyzing the image... please wait!")
        try:
            response = geo_agent.run(query, images=[image_path])
            col2.success("Here's my guess:")
            col2.markdown(response.content)
        except Exception as e:
            col2.error(f"An error occurred: {e}")
        finally:
            # Clean up temp file
            os.remove(image_path)
