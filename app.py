import streamlit as st
from PIL import Image
import backend
from dermatology_bot import DermatologyExpert
import time
from streamlit_chat import message

# Initialize session state
def init_session():
    if 'bot' not in st.session_state:
        st.session_state.bot = DermatologyExpert()
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'diagnosis' not in st.session_state:
        st.session_state.diagnosis = None

# Load custom CSS
def load_css():
    st.markdown("""
    <style>
        .stApp {
            background-color: #f8f9fa;
        }
        .diagnosis-card {
            border-left: 4px solid #4e73df;
            border-radius: 0.35rem;
            padding: 1rem;
            margin: 1rem 0;
            background: white;
            box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15);
        }
        .chat-container {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.1);
        }
        .status-badge {
            display: inline-block;
            padding: 0.35em 0.65em;
            font-size: 0.75em;
            font-weight: 700;
            line-height: 1;
            text-align: center;
            white-space: nowrap;
            vertical-align: baseline;
            border-radius: 0.25rem;
            background-color: #1cc88a;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

# Initialize app
init_session()
load_css()

# Sidebar - Branding
with st.sidebar:
    st.image("assets/hospital-icon.png", width=80)
    st.title("DermAI Clinic")
    st.markdown("<span class='status-badge'>ONLINE</span>", unsafe_allow_html=True)
    st.markdown("---")
    st.caption("24/7 Dermatology Assistance")
    if st.session_state.diagnosis:
        with st.expander("Current Diagnosis"):
            st.write(f"**Condition:** {st.session_state.diagnosis}")

# Main App Layout
col1, col2 = st.columns([1, 1])

# Image Analysis Column
with col1:
    st.subheader("📷 Skin Analysis")
    tab1, tab2 = st.tabs(["Upload Image", "Take Photo"])
    
    with tab1:
        uploaded_file = st.file_uploader("Choose skin image", 
                                       type=["jpg", "jpeg", "png"],
                                       label_visibility="collapsed")
        if uploaded_file:
            image = Image.open(uploaded_file).convert("RGB")
            st.image(image, use_column_width=True)
    
    with tab2:
        camera_img = st.camera_input("Take photo of skin condition",
                                   label_visibility="collapsed")
        if camera_img:
            image = Image.open(camera_img).convert("RGB")
    
    if 'image' in locals():
        with st.spinner("🔍 Analyzing skin..."):
            time.sleep(1.5)  # Simulate processing
            predicted_class, confidence = backend.predict_skin_disease(image)
            st.session_state.diagnosis = backend.disease_classes[predicted_class]
            
            st.success("Analysis Complete!")
            with st.expander("View Diagnosis Report", expanded=True):
                st.markdown(f"""
                <div class="diagnosis-card">
                    <h4>{st.session_state.diagnosis}</h4>
                    <p>Confidence: <strong>{confidence:.1f}%</strong></p>
                </div>
                """, unsafe_allow_html=True)
                
                condition_info = st.session_state.bot.get_condition_info(st.session_state.diagnosis)
                if condition_info:
                    st.markdown(condition_info)

# Chat Interface Column
with col2:
    st.subheader("💬 Chat with DermAI")
    
    # Quick action buttons
    cols = st.columns(3)
    with cols[0]:
        if st.button("Acne Help", help="Get acne treatment advice"):
            st.session_state.chat_history.append({"sender": "user", "message": "Acne treatment options"})
    with cols[1]:
        if st.button("Rash Help", help="Get rash guidance"):
            st.session_state.chat_history.append({"sender": "user", "message": "How to treat a rash?"})
    with cols[2]:
        if st.button("Sun Care", help="Sun protection tips"):
            st.session_state.chat_history.append({"sender": "user", "message": "Sun protection advice"})
    
    # Chat input
    user_input = st.text_input("Type your skin concern...", 
                             key="input",
                             label_visibility="collapsed",
                             placeholder="Describe your skin concern...")
    
    if user_input:
        st.session_state.chat_history.append({"sender": "user", "message": user_input})
        
        # Get bot response
        bot_response = st.session_state.bot.respond(user_input)
        st.session_state.chat_history.append({"sender": "bot", "message": bot_response})
        st.experimental_rerun()
    
    # Display chat messages
    for i, chat in enumerate(st.session_state.chat_history[-6:]):  # Show last 6 messages
        if chat['sender'] == 'user':
            message(chat['message'], is_user=True, key=f"user_{i}")
        else:
            message(chat['message'], key=f"bot_{i}")

    # Diagnosis context in chat
    if st.session_state.diagnosis:
        st.caption(f"ℹ️ Current diagnosis context: {st.session_state.diagnosis}")
