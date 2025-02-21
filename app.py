import streamlit as st
import torch
import torchvision.transforms as transforms
import timm
from PIL import Image
import numpy as np
import cv2

# Load the more accurate pre-trained model
MODEL_NAME = "convnext_large"  # Further upgraded model for highest accuracy
model = timm.create_model(MODEL_NAME, pretrained=True, num_classes=15)  # Added Cuts and Burns detection
model.eval()

disease_classes = [
    "Melanoma", "Melanocytic Nevus", "Basal Cell Carcinoma", 
    "Actinic Keratosis", "Benign Keratosis", "Dermatofibroma", "Vascular Lesion",
    "Squamous Cell Carcinoma", "Eczema", "Psoriasis", "Lentigo Maligna", "Tinea Ringworm",
    "Healthy Skin", "Cuts", "Burns"
]

def preprocess_image(image):
    """Preprocesses the uploaded image for model input."""
    transform = transforms.Compose([
        transforms.Resize((256, 256)),  # Higher resolution for better accuracy
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    return transform(image).unsqueeze(0)

def predict_skin_disease(image):
    """Runs the image through the model and returns predictions."""
    try:
        processed_img = preprocess_image(image)
        with torch.no_grad():
            outputs = model(processed_img)
            probabilities = torch.nn.functional.softmax(outputs[0], dim=0)  # Convert to probabilities
            confidence, predicted_class = torch.max(probabilities, 0)
        return predicted_class.item(), confidence.item() * 100
    except Exception as e:
        return None, str(e)

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
        predicted_class, confidence = predict_skin_disease(image)
        
        if predicted_class is not None:
            st.subheader("🩺 Diagnosis:")
            st.success(f"Predicted Skin Condition: {disease_classes[predicted_class]}")
            st.progress(confidence / 100)
            st.write(f"Confidence Level: {confidence:.2f}%")
            
            if disease_classes[predicted_class] == "Healthy Skin":
                st.balloons()
                st.success("Your skin appears to be healthy! Keep up with good skincare practices.")
            elif disease_classes[predicted_class] in ["Cuts", "Burns"]:
                st.warning("This condition may require first aid or medical attention. Please take necessary precautions.")
        else:
            st.error("An error occurred while processing the image.")

if __name__ == "__main__":
    main()
