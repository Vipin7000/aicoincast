import streamlit as st
import google.generativeai as genai
import requests
import time
from datetime import datetime
import pytz

# --- 1. CONFIG & ERROR TRACKING ---
st.set_page_config(page_title="AiCoincast | Resilient v16.4", layout="wide")
IST = pytz.timezone('Asia/Kolkata')

# Master Key (Wahi purana password)
MASTER_PASSWORD = "SAMASTIPUR@2026"

# --- 2. DEBUGGER ALGORITHM (Issues door karne ke liye) ---
def check_api_health():
    health = {"Gemini": False, "CryptoData": False}
    # Check Gemini
    if "GEMINI_API_KEY" in st.secrets:
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel('gemini-1.5-flash')
            model.generate_content("ping")
            health["Gemini"] = True
        except: pass
    # Check Crypto API
    try:
        res = requests.get("https://api.coingecko.com/api/v3/ping", timeout=3)
        if res.status_code == 200: health["CryptoData"] = True
    except: pass
    return health

# --- 3. LOGIN & SESSION GUARD ---
if "password_correct" not in st.session_state:
    st.title("🛡️ Iron Vault Login")
    pwd = st.text_input("Enter Master Key:", type="password")
    if st.button("Unlock"):
        if pwd == MASTER_PASSWORD:
            st.session_state["password_correct"] = True
            st.rerun()
        else: st.error("Invalid Key")
    st.stop()

# --- 4. MAIN TERMINAL UI ---
st.markdown("""<style>.main { background-color: #030008; color: #FFFFFF; } .news-container { border: 2px solid #BC13FE; padding: 20px; border-radius: 15px; background: rgba(16,0,43,0.9); }</style>""", unsafe_allow_html=True)

# Sidebar with Debugger Info
with st.sidebar:
    st.title("🛰️ System Health")
    status = check_api_health()
    st.write(f"Gemini AI: {'✅ Online' if status['Gemini'] else '❌ Key Error'}")
    st.write(f"Market Data: {'✅ Online' if status['CryptoData'] else '❌ API Limit'}")
    if st.button("🔄 Clear System Cache"):
        st.cache_data.clear()
        st.rerun()

# --- 5. NEWS GENERATION ALGORITHM (With Fallback Fix) ---
def fetch_resilient_news(topic):
    """Algorithm: Try Gemini first, then use local backup if it fails"""
    try:
        # Step 1: Try AI Generation
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(f"Top 3 India AI & Crypto news about {topic} in 2 lines Hinglish.")
        return response.text, f"https://pollinations.ai/p/{topic.replace(' ','_')}_cyberpunk?seed={time.time()}"
    except Exception as e:
        # Step 2: Fallback (Agar API fail ho jaye toh ye dikhega)
        return "⚠️ AI Link Temporary Down. Market is volatile today. Focus on XRT support levels and LAI growth. (Backup News Mode)", "https://via.placeholder.com/400x200?text=Market+Sentinel+Active"

st.title("🤖 AiCoincast: Resilient News Hub")
target = st.text_input("📡 News Target:", "India AI & Crypto")

# Executing News Display
news_text, img_url = fetch_resilient_news(target)

st.markdown("<div class='news-container'>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 1.5])
with col1:
    st.image(img_url, use_container_width=True)
with col2:
    st.subheader(f"📢 Latest Flash: {target}")
    st.info(news_text)
    st.caption(f"Last Sync: {datetime.now(IST).strftime('%H:%M:%S')} IST")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("© 2026 AiCoincast | v16.4 Resilient Guardian | Issues Resolved")
