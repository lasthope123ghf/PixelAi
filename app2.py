# Import necessary libraries
import streamlit as st
import base64
from dotenv import load_dotenv
import os
import requests

# Import functions from other files
from gen_image import generate_image
from image_prompt import image_to_prompt
from remove_bg import remove_background

# Load environment variables
load_dotenv()
replicate_api_key = os.getenv("REPLICATE_API_KEY")
headers = {
    "Authorization": f"Bearer {replicate_api_key}",
    "Content-Type": "application/json"
}



# Add custom CSS to set the background





# Configure the page
st.set_page_config(
    page_title="PixelFlex AI - RAJ",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set the title of the page
st.title("Pixel :blue[Flex AI] -:red[Raj]")
# Replace the line with a valid function call or define the function get_img_as_base64
img = "YOUR_BASE64_ENCODED_IMAGE_HERE"

import streamlit as st
import base64

def get_img_as_base64(file_path):
    with open(file_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def set_background_with_css():
    # Encode your image
    encoded_img = get_img_as_base64("img.jpg")  # Make sure the path is correct
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
    background-image: url("data:image/jpeg;base64,{encoded_img}");
    background-size: cover;
    background-position: top left;
    background-repeat: no-repeat;
    background-attachment: local;
    }}

    [data-testid="stSidebar"] > div:first-child {{
    background-image: url("data:image/jpeg;base64,{encoded_img}");
    background-position: center; 
    background-repeat: no-repeat;
    background-attachment: fixed;
    }}

    [data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
    }}

    [data-testid="stToolbar"] {{
    right: 2rem;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Call the function to apply the custom CSS
set_background_with_css()

# Create two columns for inputs and image generation
col1, col2 = st.columns(2)

html_content = """
<div>
    <h2 class="fade-in-text">About This Project</h2>
    <p class="fade-in-text">PixelFlex AI is an advanced text-to-image generator web app designed for versatility and user-friendly experience. The app features a comprehensive tool menu with three main functionalities: "Prompt to Image," "Image to Prompt," and "Background Remover."
    In the "Prompt to Image" section, users can enter descriptive prompts to generate high-quality images. This section includes a submenu where users can specify the size of the output image, with predefined options for mobile, laptop, fullscreen, and web-based sizes, along with a custom size option. Users can also select the desired image quality, ranging from Default and Better to HD and Ultra HD. To prevent abuse, the number of output images is limited to two for HD and Ultra HD settings, while up to four images can be generated for other quality settings. Each generated image comes with an associated download button, making it easy for users to save their creations.
<br><br>The "Image to Prompt" feature allows users to upload an image and receive a descriptive prompt that best matches the image content. The "Background Remover" tool enables users to remove backgrounds from their images quickly and efficiently.
    PixelFlex AI combines robust functionality with a seamless user interface, ensuring a smooth and enjoyable experience for all users. Created by The Raj, this project aims to provide powerful and accessible tools for creative image generation and manipulation. It Was little Hard Project But Totally fun ,I Learn a lot.
    </p>
    <img src="https://user-images.githubusercontent.com/74038190/218265814-3084a4ba-809c-4135-afc0-8685d0f634b3.gif" class="fade-in-text" alt="Loading..." style="width:100%;max-width:300px;">
</div>
"""

html_content += """
<div style="margin-top: 20px;">
    <a href="https://www.linkedin.com/in/the-raj71" target="_blank" style="text-decoration: none;">
        <button style="margin-right: 10px; background-color: #0077B5; color: white; padding: 10px 20px; border: none; cursor: pointer;">Connect on LinkedIn</button>
    </a>
    <a href="https://instagram.com/theraj71" target="_blank" style="text-decoration: none;">
        <button style="background-color: #E4405F; color: white; padding: 10px 20px; border: none; cursor: pointer;">Follow on Instagram</button>
    </a>
</div>
"""

with col1:
    st.markdown(html_content, unsafe_allow_html=True)



# Use the 2nd column for inputs
with col2:
    # Dropdown for tools selection in the main page
    current_page = st.selectbox("Select a tool:",
                                ["Generate Image", "Image to Prompt", "Remove Background"],
                                key="page_selector")

# Use the second column for displaying the selected tool's functionality
with col2:
    # Generate Image
    if current_page == "Generate Image":
        generate_image()

    # Image to Prompt
    elif current_page == "Image to Prompt":
        image_to_prompt()

    # Remove Background
    elif current_page == "Remove Background":
        remove_background()

# Add a footer to the page
# hide_st_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             header {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_st_style, unsafe_allow_html=True)