import streamlit as st
import yfinance as yf
import google.generativeai as genai
import requests
import time
from datetime import datetime
import pytz

# --- 1. ARCHITECTURE & PURPLE THEME ---
st.set_page_config(page_title="AiCoincast v18.3 Ultimate", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
MASTER_PASSWORD = "SAMASTIPUR@2026"

# CSS: UI Glitch Fixes & Styling
st.markdown("""
    <style>
    .main { background-color: #120024; color: #E0B0FF; }
    [data-testid="stSidebar"] { background-color: #080015 !important; border-right: 2px solid #BF40BF; }
    [data-testid="stMetricValue"] { color: #BF40BF !important; font-weight: bold !important; text-shadow: 0px 0px 10px #BF40BF; }
    .master-card { background: rgba(30, 0, 50, 0.9); border: 2px solid #BF40BF; padding: 20px; border-radius: 15px; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SECURITY ---
if "password_correct" not in st.session_state:
    st.markdown("<h2 style='text-align: center; color: #BF40BF;'>🛡️ Sovereign Final Vault</h2>", unsafe_allow_html=True)
    pwd = st.text_input("Master Key:", type="password")
    if st.button("Unlock Terminal"):
        if pwd == MASTER_PASSWORD:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("Invalid Key!")
    st.stop()

# --- 3. THE FIXED AI ENGINE (Enhanced for Reliability) ---
def final_ai_engine(query):
    try:
        if "GEMINI_API_KEY" not in st.secrets:
            return "Error: API Key missing in Secrets!", None
        
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        
        # Latest Stable Models
        model_names = ['gemini-1.5-flash', 'gemini-1.5-pro']
        ai_response = "AI Node is currently congested. Please try again in 10 seconds."
        
        for m_name in model_names:
            try:
                model = genai.GenerativeModel(m_name)
                # Generation with Safety Handling
                res = model.generate_content(f"Analyze this crypto/finance query in Hinglish: {query}", 
                                           generation_config={"temperature": 0.7})
                if res and res.text:
                    ai_report = res.text
                    break
            except Exception:
                continue
        else:
            ai_report = ai_response

        # Image Generation (Pollinations AI)
        img_url = f"https://pollinations.ai/p/{query.replace(' ','_')}_cyber_finance?seed={time.time()}&width=600&height=400"
        return ai_report, img_url

    except Exception as e:
        return f"System Sync Error: {str(e)}", None

# --- 4. DATA PULSE (Optimized) ---
@st.cache_data(ttl=60) # 1 minute cache to prevent API blocking
def get_safe_pulse():
    pulse_data = {"crypto": [], "nifty": "Offline"}
    try:
        # Nifty 50
        nifty_ticker = yf.Ticker("^NSEI")
        nifty_hist = nifty_ticker.history(period="1d")
        if not nifty_hist.empty:
            price = nifty_hist['Close'].iloc[-1]
            pulse_data["nifty"] = f"₹{price:,.2f}"
            
        # Crypto Pulse
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_desc&per_page=5"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            pulse_data["crypto"] = r.json()
    except:
        pass
    return pulse_data

# --- 5. UI DISPLAY ---
st.title("🤖 AiCoincast v18.3 Ultimate")
st.caption(f"Sovereign Node Active | {datetime.now(IST).strftime('%H:%M:%S IST')}")

st.markdown('<div style="background:#4B0082;color:white;padding:10px;text-align:center;font-weight:bold;border-radius:10px;">🚀 NIFTY 50 LIVE | AI COMMANDER ONLINE | PURPLE PROTOCOL</div>', unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.title("🛰️ Sentinel")
    pulse = get_safe_pulse()
    st.metric("NIFTY 50 INDEX", pulse["nifty"])
    st.divider()
    
    if pulse["crypto"]:
        for coin in pulse["crypto"]:
            st.metric(label=coin['name'], 
                      value=f"₹{coin['current_price']:,}", 
                      delta=f"{coin['price_change_percentage_24h']:.2f}%")
    else:
        st.warning("Crypto Pulse Delayed...")
    
    if st.button("🔒 Logout"):
        del st.session_state["password_correct"]
        st.rerun()

# MAIN SEARCH INTERFACE
query = st.text_input("🔍 Intelligence Search:", placeholder="e.g. XRT and LayerAI India News")

if query:
    with st.spinner("Connecting to Sovereign Node..."):
        report, visual = final_ai_engine(query)
        
        st.markdown("<div class='master-card'>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1.5])
        
        with col1:
            if visual:
                st.image(visual, use_container_width=True, caption="AI Visual Analysis")
        
        with col2:
            st.subheader(f"📝 Master Report: {query.upper()}")
            st.markdown(f"<div style='color:#E0B0FF; line-height:1.6;'>{report}</div>", unsafe_allow_html=True)
            
            # WhatsApp Share
            share_text = f"AiCoincast Report on {query}: {report[:200]}..."
            st.markdown(f'''
                <a href="https://wa.me/?text={share_text}" target="_blank" 
                style="background:#25D366;color:white;padding:12px;border-radius:10px;text-decoration:none;display:inline-block;width:100%;text-align:center;font-weight:bold;margin-top:20px;">
                📲 Share Analysis on WhatsApp
                </a>''', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
