import os
from PIL import Image
from phi.agent import Agent
from phi.model.google import Gemini
from dotenv import load_dotenv
import streamlit as st
from phi.tools.duckduckgo import DuckDuckGo

load_dotenv()
GOOGLE_API_KEY = os.getenv("AIzaSyBy791VYFuQjFIkCTV_ELBkGKIsv17wH_M")

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
- Language or symbols (text, street signs, billboards, any names mentioned in the picture as clues)
- People’s clothing or cultural aspects
- Environmental clues like weather, time of day

Return in this format:
Location Name, City, Country and Reasoning
Structure the response in markdown.

Instructions:
1. Examine the image thoroughly.
2. Provide a reasoned guess for the street name, city, state, and country.
3. Explain your reasoning in detail by pointing out the visual clues that led to your conclusion.
4. If uncertain, offer possible guesses with reasoning.
"""

# Streamlit UI
st.title("🌍 Geography Buddy")
st.write("Upload an image, and I’ll try to guess the location based on visible clues!")

# Layout with columns: Left for Image, Right for Response
col1, col2 = st.columns([1, 2])

# File uploader
uploaded_file = st.file_uploader("Upload an Image 🖼️", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open and resize the image using Pillow
    image = Image.open(uploaded_file)
    resized_image = image.resize((500, 500))  # Set width and height

    image_path = "temp_image.png"
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Display the resized image
    col1.image(resized_image, caption="Uploaded Image", use_container_width=True)

    # Submit button
    if col2.button("🚀 Submit"):
        col2.info("Analyzing the image... please wait.")

        # Send image and query to Gemini
        try:
            response = geo_agent.run(query, images=[image_path])
            col2.success("Here's my guess:")
            col2.markdown(response.content)
        except Exception as e:
            col2.error(f"An error occurred: {e}")

        # Cleanup
        os.remove(image_path)
