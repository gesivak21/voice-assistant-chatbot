# === Import necessary libraries ===
import streamlit as st
from transcript import get_transcripts
from response import get_llm_response
from gtts import gTTS
from io import BytesIO
import base64
import tempfile
import os

if "api_key" not in st.session_state:
    st.switch_page("pages/0_api_key_config.py")

# =====================================================================================
# Add navigation buttons in sidebar
# =====================================================================================
st.sidebar.title("⚡ Quick Actions")

if st.sidebar.button("🗝️ Config"):
    st.switch_page("pages/0_api_key_config.py")

if st.sidebar.button("⚙️ Settings"):
    st.switch_page("pages/1_settings.py")  

st.sidebar.divider()

# === Streamlit UI ===
st.set_page_config(page_title="🎤 Voice Assistant Chatbot", page_icon="🗣️", layout="wide")

# Initialize session state
if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "tts_enabled" not in st.session_state:
    st.session_state.tts_enabled = True

if "stt_enabled" not in st.session_state:
    st.session_state.stt_enabled = True

if "audio_key" not in st.session_state:
    st.session_state.audio_key = 0

if "latest_audio_b64" not in st.session_state:
    st.session_state.latest_audio_b64 = None

# Language settings (defaults)
if "language" not in st.session_state:
    st.session_state.language = "en"

if "tts_voice" not in st.session_state:
    st.session_state.tts_voice = "com"

if "speech_rate" not in st.session_state:
    st.session_state.speech_rate = False

# Sidebar for settings and voice input
with st.sidebar:
    st.header("⚙️ Customization")
    
    # Toggle switches
    st.session_state.stt_enabled = st.toggle("🎤 Voice Input (STT)", value=st.session_state.stt_enabled)
    
    col1, col2 = st.columns([4, 1])
    with col1:
        st.session_state.tts_enabled = st.toggle("🔊 Voice Output (TTS)", value=st.session_state.tts_enabled)
    with col2:
        # Stop button only visible when TTS is playing
        if st.session_state.latest_audio_b64 and st.button("⏹️", help="Stop current audio", use_container_width=True):
            st.session_state.latest_audio_b64 = None
            st.rerun()
    
    st.divider()
    
    # Voice input in sidebar (if enabled)
    if st.session_state.stt_enabled:
        st.subheader("🎙️ Voice Input")
        audio = st.audio_input("Record", key=f"audio_{st.session_state.audio_key}")
        
        # Process audio only if it exists
        if audio:
            with st.spinner("Transcribing..."):
                # Use temp file for transcription (works on Render)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
                    tmp_audio.write(audio.getbuffer())
                    tmp_audio_path = tmp_audio.name
                
                # Speech to text
                user_input = get_transcripts(
                    output_file_path=tmp_audio_path,
                    language=st.session_state.language
                )
                
                # Clean up temp file
                os.unlink(tmp_audio_path)
            
            # Add user message to conversation
            st.session_state.conversation.append({"role": "user", "content": user_input})
            
            # Generate response
            with st.spinner("Thinking..."):
                bot_response = get_llm_response(transcript=user_input)
            
            # Add bot response to conversation
            st.session_state.conversation.append({"role": "assistant", "content": bot_response})
            
            # TTS if enabled - store in memory
            if st.session_state.tts_enabled:
                with st.spinner("Generating speech..."):
                    tts = gTTS(
                        text=bot_response, 
                        lang=st.session_state.language,
                        slow=st.session_state.speech_rate,
                        tld=st.session_state.tts_voice
                    )
                    mp3_fp = BytesIO()
                    tts.write_to_fp(mp3_fp)
                    mp3_fp.seek(0)
                    
                    # Store in session state (in-memory)
                    st.session_state.latest_audio_b64 = base64.b64encode(mp3_fp.read()).decode()
            
            # Change key to reset audio widget
            st.session_state.audio_key += 1
            st.rerun()
    
    st.divider()
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.conversation = []
        st.session_state.latest_audio_b64 = None
        st.session_state.audio_key += 1  # Reset audio widget
        st.rerun()

# Main chat area
st.title("🎤 Voice Assistant Chatbot")

# Display chat history
for message in st.session_state.conversation:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Auto-play TTS audio if it exists (for the latest response)
if st.session_state.tts_enabled and st.session_state.latest_audio_b64:
    if len(st.session_state.conversation) > 0 and st.session_state.conversation[-1]["role"] == "assistant":
        audio_html = f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{st.session_state.latest_audio_b64}" type="audio/mp3">
        </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)

# Text input (always available)
with st.spinner("Thinking..."):
    user_input = st.chat_input("Type your message here...")
    if user_input:
        # Add user message to conversation
        st.session_state.conversation.append({"role": "user", "content": user_input})
        
        # Generate response
        bot_response = get_llm_response(transcript=user_input)

        # Add bot response to conversation
        st.session_state.conversation.append({"role": "assistant", "content": bot_response})
        
        # TTS if enabled - store in memory
        if st.session_state.tts_enabled:
            tts = gTTS(
                text=bot_response, 
                lang=st.session_state.language,
                slow=st.session_state.speech_rate,
                tld=st.session_state.tts_voice
            )
            mp3_fp = BytesIO()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            
            # Store in session state (in-memory)
            st.session_state.latest_audio_b64 = base64.b64encode(mp3_fp.read()).decode()
        

        st.rerun()
