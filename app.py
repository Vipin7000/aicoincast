import streamlit as st
import yfinance as yf
import google.generativeai as genai
import requests
import time
from datetime import datetime
import pytz

# --- 1. SYSTEM SETTINGS & FULL PURPLE THEME ---
st.set_page_config(page_title="AiCoincast v18.0 Purple", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
MASTER_PASSWORD = "SAMASTIPUR@2026"

# FIX: CSS for Deep Purple Theme & Black Bar Removal
st.markdown("""
    <style>
    .main { background-color: #1A0033; color: #E0B0FF; }
    [data-testid="stSidebar"] { background-color: #0D001A !important; }
    
    /* Sidebar Price Glow - Bright Purple/Cyan */
    [data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: #BF40BF !important;
        font-weight: bold !important;
        text-shadow: 0px 0px 8px #BF40BF;
    }
    
    /* CRITICAL FIX: Block the Black Glitch Bar */
    div[data-testid="stVerticalBlock"] > div:empty { display: none !important; }
    .stSpinner > div { border-top-color: #BF40BF !important; }
    
    /* News Card Styling */
    .purple-card { 
        background: rgba(48, 0, 77, 0.9); 
        border: 2px solid #BF40BF; 
        padding: 25px; 
        border-radius: 20px; 
        box-shadow: 0px 0px 20px #660099;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. IRON VAULT ---
if "password_correct" not in st.session_state:
    st.markdown("<h2 style='text-align: center; color: #BF40BF;'>🛡️ Purple Sovereign Vault</h2>", unsafe_allow_html=True)
    pwd = st.text_input("Master Key:", type="password")
    if st.button("Unlock"):
        if pwd == MASTER_PASSWORD:
            st.session_state["password_correct"] = True
            st.rerun()
    st.stop()

# --- 3. THE FIXED AI ENGINE (Explicit v1 Call) ---
def ai_commander_v18(query):
    try:
        if "GEMINI_API_KEY" not in st.secrets: return "Missing Key", None
        
        # Explicitly configure stable API
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        
        # Using a more robust model identification logic
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(f"Financial report on {query} in 2 lines Hinglish.")
        
        img = f"https://pollinations.ai/p/{query.replace(' ','_')}_purple_neon_art?seed={time.time()}"
        return res.text, img
    except Exception as e:
        # Fallback to older stable model if flash still 404s
        try:
            model = genai.GenerativeModel('gemini-pro')
            res = model.generate_content(f"Analyze {query} briefly in Hinglish.")
            return res.text, None
        except:
            return f"Node recalibrating. Check API settings. ({str(e)})", None

# --- 4. LIVE MARKET PULSE ---
def fetch_pulse():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_desc&per_page=6&page=1"
        return requests.get(url, timeout=5).json()
    except: return []

# --- 5. MAIN DASHBOARD ---
st.title("🤖 AiCoincast v18.0 Cyber-Purple")
st.caption(f"Sovereign Node Active | {datetime.now(IST).strftime('%H:%M:%S IST')}")

# Top Header (Purple Glow)
st.markdown('<div style="background:#4B0082;color:white;padding:10px;border-radius:10px;text-align:center;font-weight:bold;">🚀 AI COMMANDER ONLINE | MARKET DATA SYNCED | PURPLE PROTOCOL ACTIVE</div>', unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.title("🛰️ Sentinel")
    st.markdown("---")
    pulse = fetch_pulse()
    if pulse:
        for c in pulse:
            st.metric(label=c['name'], value=f"₹{c['current_price']:,}", delta=f"{c['price_change_percentage_24h']:.2f}%")
    else: st.warning("Connecting...")
    if st.button("🔒 Logout"):
        del st.session_state["password_correct"]
        st.rerun()

# SEARCH & REPORT
query = st.text_input("🔍 Search Asset:", "XRT and LayerAI India News")

if query:
    with st.spinner("Processing in Purple Mode..."):
        report, visual = ai_commander_v18(query)
        
        st.markdown("<div class='purple-card'>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1.5])
        with col1:
            if visual: st.image(visual)
        with col2:
            st.subheader(f"📝 Master Report: {query.upper()}")
            st.write(report)
            st.markdown(f'<a href="https://wa.me/?text={report[:250]}" target="_blank" style="background:#25D366;color:white;padding:12px;border-radius:10px;text-decoration:none;display:inline-block;width:100%;text-align:center;font-weight:bold;">📲 Share on WhatsApp</a>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
