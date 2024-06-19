import streamlit as st
import replicate
import time
import base64
from PIL import Image, ImageEnhance
import io
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dotenv import load_dotenv
import os
load_dotenv()
replicate_api_key = os.getenv("REPLICATE_API_KEY")

def display_images_in_grid(images, grid_size=(2, 2)):
    cols = st.columns(grid_size[1])
    for index, image in enumerate(images):
        with cols[index % grid_size[1]]:
            st.image(image, use_column_width=True)
            # Add download button for each image
            image_bytes = io.BytesIO()
            image.save(image_bytes, format='PNG')
            st.download_button(label="Download Image", data=image_bytes.getvalue(), file_name=f"image_{index}.png", mime="image/png")

def display_images_full_size(images):
    for index, image in enumerate(images):
        st.image(image, use_column_width=True)
        # Add download button for each image
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='PNG')
        st.download_button(label="Download Image", data=image_bytes.getvalue(), file_name=f"image_{index}.png", mime="image/png")

def adjust_dimension(dimension):
    return dimension + (8 - dimension % 8) if dimension % 8 != 0 else dimension

def fetch_and_convert_image(image_url, retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504), timeout=5):
    session = requests.Session()
    retries = Retry(total=retries, read=retries, connect=retries, backoff_factor=backoff_factor, status_forcelist=status_forcelist)
    session.mount('https://', HTTPAdapter(max_retries=retries))
    try:
        response = session.get(image_url, timeout=timeout)
        response.raise_for_status()  # Raises stored HTTPError, if one occurred.
        image = Image.open(io.BytesIO(response.content))
        return image
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)

def generate_image():
    start_time = time.time()  
    st.subheader("Generate Image")
    prompt = st.text_input(label="Enter a prompt for the image:", key="generate_image_prompt")
    size_option = st.selectbox("Choose the image size:", ["Default", "Mobile", "Laptop", "Web", "Fullscreen", "Custom"], index=0)
    if size_option == "Custom":
        width = st.number_input("Width:", min_value=1, value=1024)
        height = st.number_input("Height:", min_value=1, value=1024)
    elif size_option == "Default":
        width, height = 1024, 1024
    else:
        size_dict = {"Mobile": (480, 848), "Laptop": (1368, 768), "Web": (1920, 1080), "Fullscreen": (1024, 1024)}
        width, height = size_dict.get(size_option, (1024, 1024))
    width = adjust_dimension(width)
    height = adjust_dimension(height)
    quality_option = st.selectbox("Choose the quality of the image:", ["Default", "Better HD", "Ultra HD"], index=0)
    num_inference_steps = {"Default": 25, "Better HD": 50, "Ultra HD": 75}.get(quality_option, 25)
    # Adjust the maximum number of outputs based on quality option
    max_outputs = 1 if quality_option in ["Better HD", "Ultra HD"] else 4
    # Ensure min_value is less than max_value for the slider
    num_outputs = st.slider("Number of images to generate:", min_value=1, max_value=max(max_outputs, 2), value=1 if max_outputs == 1 else 4)
    output = None  # Define the output variable
    if st.button("Generate Image", key="generate_image_button"):
        with st.spinner("Raj is Generating image..."):
            try:
                output = replicate.run(
                    "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                    input={
                        "width": width,
                        "height": height,
                        "prompt": prompt,
                        "refine": "expert_ensemble_refiner",
                        "negative_prompt": "low quality, worst quality",
                        "num_inference_steps": num_inference_steps,
                        "num_outputs": 1 if quality_option in ["Better HD", "Ultra HD"] else num_outputs,
                    }
                )
                # Assuming the images list contains all the generated images
                image_urls = output  # Assuming output is a list of image URLs
                images = [fetch_and_convert_image(url) for url in image_urls]
                
                # Decide on layout based on image size
                if size_option in ["Mobile", "Default", "Custom"] and (width <= 1024 and height <= 1024):
                    # Use a 2x2 grid for smaller images
                    display_images_in_grid(images, grid_size=(2, 2))
                else:
                    # For larger images, display them using the full resources
                    display_images_full_size(images)
            except Exception as e:
                st.error(f"Due to Extreme Abuse of this free service 😁, Developer has set restrictions to manage the load or there maybe any error. Kindly contact the owner, Raj {e}")
            end_time = time.time()
            elapsed_time = end_time - start_time
            st.write(f"Image generated in {elapsed_time:.2f} seconds")