import os
import json
import requests
import base64
import io
import streamlit as st
from PIL import Image
from gtts import gTTS
from google.cloud import firestore

# ---------------------------
# 0. Page Config
# ---------------------------
st.set_page_config(page_title="Wednesday Voice", page_icon="🎙️", layout="wide")

# ---------------------------
# 1. Setup
# ---------------------------
API_KEY = os.environ.get("GOOGLE_API_KEY")
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")

if not API_KEY:
    st.error("⚠️ GOOGLE_API_KEY is missing!")
    st.stop()

# ---------------------------
# 2. Direct API Logic (With History & Persona)
# ---------------------------
def call_gemini_api(current_text, current_image_bytes=None, history=[]):
    """
    Calls Gemini 2.5 Flash directly via HTTP with robust response parsing.
    """
    # URL for Gemini 2.5 Flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}

    # 1. System Instruction (The Persona) - Sent every time
    system_instruction = {
        "parts": [{
            "text": """You are Wednesday, a specialized Evidence Analyzer Agent. Your personality is cynical, precise, and dry.If an image is provided, analyze every detail in it like a detective. You do NOT suffer fools gladly. Never break character. Use Google Search to verify facts.
            """
        }]
    }

    # Build Payload
    contents = []
    
    # History
    for msg in history:
        role = "model" if msg["role"] == "assistant" else "user"
        parts = []
        if msg.get("image_data_b64"):
            parts.append({"inline_data": {"mime_type": "image/png", "data": msg["image_data_b64"]}})
        if msg.get("content"):
            parts.append({"text": msg["content"]})
        contents.append({"role": role, "parts": parts})

    # Current Message
    current_parts = []
    if current_image_bytes:
        b64_data = base64.b64encode(current_image_bytes).decode('utf-8')
        current_parts.append({"inline_data": {"mime_type": "image/png", "data": b64_data}})
    if current_text:
        current_parts.append({"text": current_text})
    contents.append({"role": "user", "parts": current_parts})

    payload = {
        "contents": contents,
        "system_instruction": system_instruction,
        "tools": [{"google_search": {}}] 
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code != 200:
            return f"[Error {response.status_code}]: {response.text}"
            
        result = response.json()
        
        # --- SEARCH FIX: Loop through parts ---
        try:
            if 'candidates' in result and result['candidates']:
                candidate = result['candidates'][0]
                full_text = ""
                
                # Check content/parts exists
                if 'content' in candidate and 'parts' in candidate['content']:
                    for part in candidate['content']['parts']:
                        if 'text' in part:
                            full_text += part['text']
                
                if full_text:
                    return full_text
                else:
                    # Debugging fallback if API returns weird structure
                    return f"Analysis complete. Raw Data: {json.dumps(candidate.get('content', {}).get('parts', []))}"
            else:
                return "Error: No response from Gemini."
                
        except Exception as e:
            return f"Parsing Error: {e}"
            
    except Exception as e:
        return f"Connection Error: {e}"

# ---------------------------
# 3. Database
# ---------------------------
db = None
if PROJECT_ID:
    try:
        db = firestore.Client(project=PROJECT_ID)
    except Exception:
        db = None

# ---------------------------
# 4. Helpers
# ---------------------------
def pil_to_bytes(img: Image.Image, fmt: str = "PNG") -> bytes:
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return buf.getvalue()

def safe_tts(text: str):
    try:
        tts = gTTS(text=text, lang="en", slow=False)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        return buf.getvalue()
    except Exception as e:
        st.error(f"Audio Error: {e}")
        return None

# ---------------------------
# 5. Session & UI
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Wednesday: Voice & Vision")
# --- CAPTION UPDATED HERE ---
st.caption("Powered by Gemini 2.5 Flash | Vision • Voice • Search")

with st.sidebar:
    st.header("🕵️‍♀️ Evidence Locker")

    # --- DEBUG STATUS ---
    if db:
        st.success(f"✅ Database Online")
    else:
        st.error("❌ Database Offline")
        if not PROJECT_ID:
            st.warning("⚠️ Reason: PROJECT_ID env var is missing.")
    # --------------------

    agent_id = st.text_input("Agent Name / ID", value="Guest_Detective")
    st.divider()
    
    uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
    
    # --- DOWNLOAD FIX IS HERE ---
    # We generate the text content using the current session state messages.
    if st.session_state.messages:
        # Generate the full conversation string from memory
        chat_text = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages])
        
        st.download_button(
            label="📂 Download Case",
            data=chat_text, 
            file_name=f"{agent_id}_Case_File.txt"
        )
    # --- END FIX ---
    if st.button("🧹 Clear History"):
        st.session_state.messages = []
        if "last_processed_file" in st.session_state:
            del st.session_state.last_processed_file
        st.rerun()

# ---------------------------
# 6. Logic
# ---------------------------
st.write("🎙️ **Voice Command:**")
try:
    from streamlit_mic_recorder import speech_to_text
    voice_text = speech_to_text(language="en", start_prompt="Speak", stop_prompt="Stop", just_once=True, key='STT')
except:
    voice_text = None

chat_input = st.chat_input("Type inquiry...")
user_text = voice_text if voice_text else chat_input

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("image_data_b64"):
            try:
                img_bytes = base64.b64decode(msg["image_data_b64"])
                st.image(img_bytes, width=200)
            except:
                pass
        st.markdown(msg["content"])
        if msg.get("audio"): st.audio(msg["audio"], format="audio/mp3")

should_process = False
if user_text:
    should_process = True
elif uploaded_file:
    file_id = f"{uploaded_file.name}_{uploaded_file.size}"
    if st.session_state.get("last_processed_file") != file_id:
        should_process = True

if should_process:
    current_image_bytes = None
    b64_str = None
    
    if uploaded_file:
        file_id = f"{uploaded_file.name}_{uploaded_file.size}"
        if st.session_state.get("last_processed_file") != file_id:
            img = Image.open(uploaded_file)
            current_image_bytes = pil_to_bytes(img)
            b64_str = base64.b64encode(current_image_bytes).decode('utf-8')
            if not user_text: user_text = "Analyze this evidence."
            st.session_state.last_processed_file = file_id
    
    st.session_state.messages.append({
        "role": "user", 
        "content": user_text, 
        "image_data_b64": b64_str
    })
    
    with st.chat_message("user"):
        if current_image_bytes: st.image(current_image_bytes, width=250)
        st.markdown(user_text)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        history_payload = st.session_state.messages[:-1]
        
        text = call_gemini_api(user_text, current_image_bytes, history_payload)
        
        placeholder.markdown(text)
        
        audio = safe_tts(text)
        if audio: st.audio(audio, format="audio/mp3", autoplay=True)

        st.session_state.messages.append({"role": "assistant", "content": text, "audio": audio})
        
        if db:
            db.collection("wednesday_cases").document().set({
                "agent_id": agent_id,
                "query": user_text, "response": text, "timestamp": firestore.SERVER_TIMESTAMP
            })