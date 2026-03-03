import streamlit as st
import yfinance as yf
import google.generativeai as genai
import requests
import time
from datetime import datetime
import pytz

# --- 1. ARCHITECTURE & PURPLE THEME ---
st.set_page_config(page_title="AiCoincast v18.3 Final", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
MASTER_PASSWORD = "SAMASTIPUR@2026"

# CSS: Removing Glitches & Fixing Visibility
st.markdown("""
    <style>
    .main { background-color: #120024; color: #E0B0FF; }
    [data-testid="stSidebar"] { background-color: #080015 !important; border-right: 2px solid #BF40BF; }
    /* REMOVING BLACK PATTI GLITCH */
    div[data-testid="stVerticalBlock"] > div:empty { display: none !important; }
    [data-testid="stSidebar"] [data-testid="stMetricValue"] { color: #BF40BF !important; font-weight: bold !important; text-shadow: 0px 0px 10px #BF40BF; }
    .master-card { background: rgba(30, 0, 50, 0.9); border: 2px solid #BF40BF; padding: 20px; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SECURITY (v16.3) ---
if "password_correct" not in st.session_state:
    st.markdown("<h2 style='text-align: center; color: #BF40BF;'>🛡️ Sovereign Final Vault</h2>", unsafe_allow_html=True)
    pwd = st.text_input("Master Key:", type="password")
    if st.button("Unlock Terminal"):
        if pwd == MASTER_PASSWORD:
            st.session_state["password_correct"] = True
            st.rerun()
    st.stop()

# --- 3. THE FIXED AI ENGINE (Anti-404 Logic) ---
def final_ai_engine(query):
    try:
        if "GEMINI_API_KEY" not in st.secrets: return "Missing Key", None
        # FORCE v1 API
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # Multi-Model Fallback
        model_names = ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-pro']
        res = None
        for m_name in model_names:
            try:
                model = genai.GenerativeModel(m_name)
                res = model.generate_content(f"Crypto analysis Hinglish: {query}")
                if res: break
            except: continue
        
        img = f"https://pollinations.ai/p/{query.replace(' ','_')}_purple_cyber?seed={time.time()}"
        return res.text if res else "AI Node Busy. Try later.", img
    except Exception as e:
        return f"Syncing Error: {str(e)}", None

# --- 4. DATA PULSE (Safe Handling - v18.3) ---
def get_safe_pulse():
    pulse_data = {"crypto": [], "nifty": "Live"}
    try:
        # Nifty (v8.0 Algorithm)
        nifty = yf.Ticker("^NSEI").history(period="1d")['Close'].iloc[-1]
        pulse_data["nifty"] = f"₹{nifty:,.2f}"
        # Crypto (CoinGecko)
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_desc&per_page=5&page=1"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            pulse_data["crypto"] = r.json()
    except: pass
    return pulse_data

# --- 5. UI DISPLAY ---
st.title("🤖 AiCoincast v18.3 Ultimate")
st.caption(f"Sovereign Node Active | {datetime.now(IST).strftime('%H:%M:%S IST')}")

# Top Header (v12.0)
st.markdown('<div style="background:#4B0082;color:white;padding:10px;text-align:center;font-weight:bold;border-radius:10px;">🚀 NIFTY 50 LIVE | AI COMMANDER ONLINE | PURPLE PROTOCOL</div>', unsafe_allow_html=True)

# SIDEBAR: SAFE RENDERING
with st.sidebar:
    st.title("🛰️ Sentinel")
    data = get_safe_pulse()
    st.metric("NIFTY 50", data["nifty"])
    st.divider()
    if data["crypto"]:
        for c in data["crypto"]:
            # SAFE ACCESS to avoid TypeError
            name = c.get('name', 'Unknown')
            price = c.get('current_price', 0)
            change = c.get('price_change_percentage_24h', 0)
            st.metric(label=name, value=f"₹{price:,}", delta=f"{change:.2f}%")
    else:
        st.warning("Data Pulse Syncing...")
    
    if st.button("🔒 Logout"):
        del st.session_state["password_correct"]
        st.rerun()

# MAIN SEARCH
query = st.text_input("🔍 Intelligence Search:", "XRT and LayerAI India News")
if query:
    with st.spinner("Analyzing..."):
        report, visual = final_ai_engine(query)
        st.markdown("<div class='master-card'>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1.5])
        with col1:
            if visual: st.image(visual)
        with col2:
            st.subheader(f"📝 Master Report: {query.upper()}")
            st.info(report)
            st.markdown(f'<a href="https://wa.me/?text={report[:250]}" target="_blank" style="background:#25D366;color:white;padding:10px;border-radius:10px;text-decoration:none;display:inline-block;width:100%;text-align:center;font-weight:bold;">📲 Share on WhatsApp</a>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
