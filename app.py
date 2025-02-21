import streamlit as st
from PIL import Image
import backend  # Importing the backend

def main():
    st.set_page_config(page_title="AI Dermatologist", layout="wide")
    st.title("📸 AI Dermatologist: Skin Disease Scanner")
    st.write("Upload an image or take a photo to analyze your skin condition.")

    option = st.radio("Choose Image Input Method:", ("Upload from Device", "Use Camera"))
    image = None

    if option == "Upload from Device":
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            image = Image.open(uploaded_file).convert("RGB")
    elif option == "Use Camera":
        captured_image = st.camera_input("Take a photo")
        if captured_image:
            image = Image.open(captured_image).convert("RGB")

    if image:
        st.image(image, caption="Selected Image", use_column_width=True)
        st.write("🔍 Analyzing image...")
        predicted_class, confidence = backend.predict_skin_disease(image)
        
        if predicted_class is not None:
            st.subheader("🩺 Diagnosis:")
            st.success(f"Predicted Skin Condition: {backend.disease_classes[predicted_class]}")
            st.progress(confidence / 100)
            st.write(f"Confidence Level: {confidence:.2f}%")
            
            if backend.disease_classes[predicted_class] == "Healthy Skin":
                st.balloons()
                st.success("Your skin appears to be healthy! Keep up with good skincare practices.")
            elif backend.disease_classes[predicted_class] in ["Cuts", "Burns"]:
                st.warning("This condition may require first aid or medical attention. Please take necessary precautions.")
        else:
            st.error("An error occurred while processing the image.")

if __name__ == "__main__":
    main()
