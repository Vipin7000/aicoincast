import streamlit as st
import google.generativeai as genai
import requests
import time
from datetime import datetime
import pytz

# --- 1. CONFIG & SYSTEM SETTINGS ---
st.set_page_config(page_title="AiCoincast Master", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
MASTER_PASSWORD = "SAMASTIPUR@2026"

# --- 2. LOGIN GUARD (Fixed Spelling Errors) ---
if "password_correct" not in st.session_state:
    st.markdown("<h2 style='text-align: center; color: #BC13FE;'>🛡️ Iron Vault Login</h2>", unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        pwd = st.text_input("Enter Master Key:", type="password")
        if st.button("Unlock Terminal"):
            if pwd == MASTER_PASSWORD:
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("🚫 Access Denied: Invalid Key")
    st.stop() # Fixed from st.step()

# --- 3. SIDEBAR: SYSTEM HEALTH ---
with st.sidebar:
    st.title("🛰️ System Sentinel")
    if "GEMINI_API_KEY" in st.secrets:
        st.success("Gemini AI: ✅ Online")
    else:
        st.error("Gemini AI: ❌ Key Missing")
    
    st.divider()
    if st.button("🔒 Secure Logout"):
        del st.session_state["password_correct"]
        st.rerun()

# --- 4. NEWS ENGINE (Fixed Attribute Error) ---
def get_master_news(topic):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(f"Top 3 India AI & Crypto news about {topic} in 2-line Hinglish.")
        # Visual Image URL
        img_url = f"https://pollinations.ai/p/{topic.replace(' ','_')}_futuristic?seed={time.time()}"
        return res.text, img_url
    except Exception as e:
        return f"⚠️ AI Node busy. Error: {str(e)}", None

# --- 5. MAIN DASHBOARD ---
st.title("🤖 AiCoincast v16.7")
target = st.text_input("📡 Enter Market Target:", "XRT and LayerAI India News")

if target:
    with st.spinner("Executing Algorithms..."):
        news_text, visual_url = get_master_news(target)
        
        # UI Container
        st.markdown("<div style='border:2px solid #BC13FE; padding:20px; border-radius:15px; background:rgba(16,0,43,0.9);'>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1.5])
        
        with col1:
            if visual_url:
                # Fixed: Use width instead of use_container_width if error persists
                st.image(visual_url, caption="AI Visual Context")
        
        with col2:
            st.subheader(f"📢 FLASH: {target.upper()}")
            st.info(news_text)
            
            # WhatsApp Share
            wa_url = f"https://wa.me/?text=AiCoincast%20Update%3A%0A{news_text[:500]}"
            st.markdown(f'<a href="{wa_url}" target="_blank" style="background:#25D366; color:white; padding:10px; border-radius:10px; text-decoration:none; display:inline-block; width:100%; text-align:center; font-weight:bold;">📲 Share on WhatsApp</a>', unsafe_allow_html=True)
            
            if st.button("🔄 Refresh Pulse"):
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()
st.caption("© 2026 AiCoincast India | v16.7 Final Fix | Mass Comm Excellence")
