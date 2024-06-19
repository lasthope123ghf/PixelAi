import streamlit as st
import replicate
import time
from io import BytesIO
import requests
import base64

def remove_background():
    st.subheader("Background Remover")
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"], key="remove_background")

    if uploaded_file is not None:
        st.image(uploaded_file)
        if st.button("Generate Image"):
            with st.spinner('Generating image...'):
                start_time = time.time()

                # Convert uploaded file to base64 string if required by the model
                # This step depends on the model's input requirements
                bytes_data = uploaded_file.getvalue()
                base64_str = base64.b64encode(bytes_data).decode("utf-8")
                input = {"image": base64_str}  # Adjust this line based on the model's expected input format

                try:
                    output = replicate.run(
                        "cjwbw/rembg:fb8af171cfa1616ddcf1242c093f9c46bcada5ad4cf6f2fbe8b81b330ec5c003",
                        input=input
                    )
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    st.write(f"Image generated in {elapsed_time:.2f} seconds")

                    if output:
                        # Assuming 'output' is a URL to the image
                        response = requests.get(output)
                        if response.status_code == 200:
                            image_bytes = response.content
                            st.image(image_bytes)

                            # Use Streamlit's download_button to offer the image for download
                            st.download_button(
                                label="Download Image",
                                data=image_bytes,
                                file_name="processed_image.png",
                                mime="image/png"
                            )
                except Exception as e:
                    st.error(f"Failed to generate image: {e}")