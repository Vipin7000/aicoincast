import streamlit as st
import yfinance as yf
import google.generativeai as genai
import requests
import time
from datetime import datetime
import pytz

# --- 1. ARCHITECTURE & PURPLE OMNI THEME ---
st.set_page_config(page_title="AiCoincast v18.2 Ultimate", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
MASTER_PASSWORD = "SAMASTIPUR@2026"

# FINAL CSS FIX: Removing Black Glitch Patti & Pricing Visibility
st.markdown("""
    <style>
    /* Full Theme Purple */
    .main { background-color: #120024; color: #E0B0FF; }
    [data-testid="stSidebar"] { background-color: #080015 !important; border-right: 1px solid #BF40BF; }
    
    /* REMOVING THE BLACK PATTI GLITCH (CRITICAL FIX) */
    div[data-testid="stVerticalBlock"] > div:empty { display: none !important; height: 0px !important; margin: 0px !important; padding: 0px !important; }
    hr { border-top: 1px solid #BF40BF !important; }
    .stSpinner > div { border-top-color: #BF40BF !important; }
    
    /* Sidebar Metrics Visibility - Neon Purple Glow */
    [data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: #BF40BF !important;
        font-weight: bold !important;
        text-shadow: 0px 0px 12px #BF40BF;
        font-size: 1.6rem !important;
    }
    [data-testid="stSidebar"] [data-testid="stMetricLabel"] { color: #E0B0FF !important; }
    
    /* Master Card Styling */
    .master-card { 
        background: rgba(30, 0, 50, 0.95); 
        border: 2px solid #BF40BF; 
        padding: 25px; 
        border-radius: 20px; 
        box-shadow: 0px 0px 25px #4B0082;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. IRON VAULT GATEWAY (v16.3 Security) ---
if "password_correct" not in st.session_state:
    st.markdown("<h2 style='text-align: center; color: #BF40BF;'>🛡️ Sovereign Ultimate Vault</h2>", unsafe_allow_html=True)
    pwd = st.text_input("Master Key:", type="password")
    if st.button("Unlock Terminal"):
        if pwd == MASTER_PASSWORD:
            st.session_state["password_correct"] = True
            st.rerun()
    st.stop()

# --- 3. OMNISCIENT AI ENGINE (Fixing 404 & Version Issues) ---
def master_ai_engine(query):
    try:
        if "GEMINI_API_KEY" not in st.secrets: return "Missing API Key", None
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        
        # Stability Logic: Verifying model existence
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            res = model.generate_content(f"Market Analysis (Hinglish): {query}. Focus on India impact.")
        except:
            # Fallback to Pro if Flash is 404 or Busy
            model = genai.GenerativeModel('gemini-pro')
            res = model.generate_content(f"Analyze {query} in Hinglish for Indian investors.")
            
        img = f"https://pollinations.ai/p/{query.replace(' ','_')}_purple_neon_cyberpunk?seed={time.time()}"
        return res.text, img
    except Exception as e:
        return f"Node Syncing... (System Notice: {str(e)})", None

# --- 4. DATA PULSE (Global Market + Crypto CEX/DEX) ---
def get_pulse_data():
    data = {"crypto": [], "nifty": "Live"}
    try:
        # Crypto Top 6 (CEX/DEX Pulse)
        c_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_desc&per_page=6&page=1"
        data["crypto"] = requests.get(c_url, timeout=5).json()
        
        # Nifty 50 Live (Global Share Index)
        nifty = yf.Ticker("^NSEI").history(period="1d")['Close'].iloc[-1]
        data["nifty"] = f"₹{nifty:,.2f}"
    except: pass
    return data

# --- 5. TERMINAL UI DISPLAY ---
st.title("🤖 AiCoincast v18.2 Ultimate Node")
st.caption(f"Sovereign Protocol Active | {datetime.now(IST).strftime('%H:%M:%S IST')}")

# Top Header Ticker (v12.0 Algorithm)
st.markdown('<div style="background:#4B0082;color:white;padding:12px;border-radius:10px;text-align:center;font-weight:bold;border:1px solid #BF40BF;">🛰️ AI COMMANDER ONLINE | NIFTY 50 LIVE | RELIANCE DIGITAL NODE ACTIVE</div>', unsafe_allow_html=True)

# SIDEBAR: The Sentinel (All Data Showing)
with st.sidebar:
    st.title("🛰️ Sentinel")
    st.success("v18.2 Online")
    st.divider()
    pulse = get_pulse_data()
    
    st.subheader("🇮🇳 Index Watch")
    st.metric("NIFTY 50", pulse["nifty"])
    
    st.divider()
    st.subheader("💰 Top Cryptos")
    if pulse["crypto"]:
        for c in pulse["crypto"]:
            st.metric(label=c['name'], value=f"₹{c['current_price']:,}", delta=f"{c['price_change_percentage_24h']:.2f}%")
    else: st.warning("Pulse Offline")
    
    if st.button("🔒 Secure Logout"):
        del st.session_state["password_correct"]
        st.rerun()

# MAIN SEARCH & AI WRITER
query = st.text_input("🔍 Intelligence Search (BTC, XRT, LAI, Nifty):", "Robonomics XRT Future India")

if query:
    with st.spinner("AI Decoding Purple Intelligence..."):
        report, visual = master_ai_engine(query)
        
        st.markdown("<div class='master-card'>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1.5])
        with col1:
            if visual: st.image(visual, caption=f"AI Visualization: {query}")
        with col2:
            st.subheader(f"📝 Sovereign Report: {query.upper()}")
            st.info(report)
            # WhatsApp Share (v15.0)
            wa_text = f"AiCoincast Master Update: {report[:250]}..."
            st.markdown(f'<a href="https://wa.me/?text={wa_text}" target="_blank" style="background:#25D366;color:white;padding:12px;border-radius:10px;text-decoration:none;display:inline-block;width:100%;text-align:center;font-weight:bold;">📲 Share on WhatsApp</a>', unsafe_allow_html=True)
            if st.button("🔄 Refresh Pulse"): st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()
st.caption("© 2026 AiCoincast India | v18.2 Sovereign Ultimate | All Issues Fixed")
