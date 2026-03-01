import streamlit as st
import google.generativeai as genai
import requests
import time
from datetime import datetime
import pytz

# --- 1. CONFIG ---
st.set_page_config(page_title="AiCoincast Master", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
MASTER_PASSWORD = "SAMASTIPUR@2026"

# --- 2. LOGIN GUARD ---
if "password_correct" not in st.session_state:
    st.title("🛡️ Iron Vault Login")
    pwd = st.text_input("Enter Master Key:", type="password")
    if st.button("Unlock Terminal"):
        if pwd == MASTER_PASSWORD:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("Invalid Key") # Fixed spelling
    st.stop() # Fixed spelling

# --- 3. SIDEBAR MONITOR ---
with st.sidebar:
    st.title("🛰️ Sentinel")
    if "GEMINI_API_KEY" in st.secrets:
        st.write("Gemini AI: ✅ Online")
    else:
        st.write("Gemini AI: ❌ Key Missing")
    if st.button("🔄 Clear Cache"):
        st.cache_data.clear()
        st.rerun()

# --- 4. NEWS ENGINE ---
def get_news(topic):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(f"Top 3 news about {topic} in 2 lines Hinglish.")
        img = f"https://pollinations.ai/p/{topic.replace(' ','_')}?seed={time.time()}"
        return res.text, img
    except Exception as e:
        return f"AI Node busy. Error: {str(e)}", None

# --- 5. UI ---
st.title("🤖 AiCoincast v16.6")
target = st.text_input("📡 News Target:", "XRT and LayerAI India News")
news, visual = get_news(target)

st.markdown("<div style='border:2px solid #BC13FE; padding:20px; border-radius:15px;'>", unsafe_allow_html=True)
c1, c2 = st.columns([1, 1.5])
with c1: st.image(visual, use_container_width=True)
with c2:
    st.subheader(f"📢 FLASH: {target}")
    st.info(news)
    wa_url = f"https://wa.me/?text={news[:500]}"
    st.markdown(f'<a href="{wa_url}" target="_blank" style="background:#25D366; color:white; padding:10px; border-radius:10px; text-decoration:none;">📲 Share on WhatsApp</a>', unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
