import streamlit as st
from backend import classify_skin_image
from PIL import Image
import io

# ✅ Set page config at the very top
st.set_page_config(page_title="AI Dermatologist", layout="centered")

def main():
    st.title("📸 AI Dermatologist: Skin Disease Scanner")
    st.write("Upload a skin image or take a picture to analyze and get a diagnosis.")

    # File Upload
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "bmp", "webp"])
    
    # Camera Input
    camera_file = st.camera_input("Take a picture")

    # Check if user uploaded or took a picture
    image_source = uploaded_file if uploaded_file else camera_file
    
    if image_source:
        # Display image
        image = Image.open(image_source)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Convert image to bytes for processing
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="PNG")

        # Process image
        st.write("🔍 Analyzing image...")
        result, confidence = classify_skin_image(image_bytes.getvalue())
        
        # Display result with confidence percentage
        st.subheader("🩺 Diagnosis:")
        st.success(f"**{result}** ({confidence:.2f}% confidence)")

if __name__ == "__main__":
    main()
