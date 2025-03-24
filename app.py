import streamlit as st
from PIL import Image
import backend  # Importing the backend
from dermatology_bot import DermatologyExpert  # Import the chatbot
import json

def main():
    st.set_page_config(page_title="AI Dermatologist", layout="wide")
    
    # Initialize chatbot
    bot = DermatologyExpert()
    
    # Main app layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.title("📸 AI Dermatologist")
        st.write("Upload an image or take a photo to analyze your skin condition.")
        
        # Image input section
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
                
                # Show additional info from knowledge base
                condition_info = bot.get_condition_info(backend.disease_classes[predicted_class])
                if condition_info:
                    with st.expander("ℹ️ More about this condition"):
                        st.markdown(condition_info)
                
                if backend.disease_classes[predicted_class] == "Healthy Skin":
                    st.balloons()
                    st.success("Your skin appears to be healthy! Keep up with good skincare practices.")
                elif backend.disease_classes[predicted_class] in ["Cuts", "Burns"]:
                    st.warning("This condition may require first aid or medical attention. Please take necessary precautions.")
            else:
                st.error("An error occurred while processing the image.")
    
    with col2:
        st.title("💬 Dermatology Assistant")
        st.write("Ask any questions about skin conditions, treatments, or care routines.")
        
        # Chat interface
        user_input = st.text_input("Type your dermatology question here:")
        if user_input:
            if user_input.lower() in ['quit', 'exit']:
                st.info("Remember to check your skin regularly. Goodbye!")
            else:
                response = bot.respond(user_input)
                st.markdown(f"**AI Dermatologist:** {response}")
        
        # Quick question buttons
        st.subheader("Common Questions:")
        cols = st.columns(2)
        with cols[0]:
            if st.button("Acne treatment options"):
                st.markdown(f"**AI Dermatologist:** {bot.respond('acne treatments')}")
            if st.button("Eczema management"):
                st.markdown(f"**AI Dermatologist:** {bot.respond('how to manage eczema')}")
        with cols[1]:
            if st.button("Sun protection tips"):
                st.markdown(f"**AI Dermatologist:** {bot.respond('sun protection advice')}")
            if st.button("Mole evaluation"):
                st.markdown(f"**AI Dermatologist:** {bot.respond('ABCDE rule for moles')}")

if __name__ == "__main__":
    main()
