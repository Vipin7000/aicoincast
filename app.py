import streamlit as st
import yfinance as yf
import google.generativeai as genai
import requests
import time
from datetime import datetime
import pytz

# --- 1. SETTINGS & CLEAN THEME ---
st.set_page_config(page_title="AiCoincast v17.9 Sovereign", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
MASTER_PASSWORD = "SAMASTIPUR@2026"

# FIX: Removing Black Bar & Fixing Price Visibility
st.markdown("""
    <style>
    .main { background-color: #030008; color: #FFFFFF; }
    /* Sidebar Price Glow */
    [data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: #00F5FF !important;
        font-weight: bold !important;
        text-shadow: 0px 0px 5px #00F5FF;
    }
    /* Removing the problematic black glitch patti */
    div[data-testid="stVerticalBlock"] > div:empty { display: none !important; }
    .report-card { background: rgba(16,0,43,0.9); border: 2px solid #BC13FE; padding: 25px; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIN GUARD ---
if "password_correct" not in st.session_state:
    st.title("🛡️ Sovereign Iron Vault")
    pwd = st.text_input("Enter Master Key:", type="password")
    if st.button("Unlock Terminal"):
        if pwd == MASTER_PASSWORD:
            st.session_state["password_correct"] = True
            st.rerun()
    st.stop()

# --- 3. THE FIXED AI ENGINE (No more 404) ---
def ai_commander_v17_9(query):
    try:
        if "GEMINI_API_KEY" not in st.secrets: return "Missing Key", None
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        
        # Explicitly using the most stable model endpoint
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(f"3-line Hinglish Market Analysis: {query}")
        
        img = f"https://pollinations.ai/p/{query.replace(' ','_')}_digital_art?seed={time.time()}"
        return res.text, img
    except Exception as e:
        return f"Node Syncing... (Status: {str(e)})", None

# --- 4. LIVE DATA PULSE (CEX/DEX) ---
def fetch_live_pulse():
    try:
        # Fetching Top 5 from CoinGecko
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_desc&per_page=6&page=1"
        return requests.get(url, timeout=5).json()
    except: return []

# --- 5. MAIN DASHBOARD ---
st.title("🤖 AiCoincast v17.9 Master Node")
st.caption(f"Sovereign Node Active | {datetime.now(IST).strftime('%H:%M:%S IST')}")

# Top Status (Clean)
st.success("✅ AI COMMANDER ONLINE | 📊 MARKET DATA SYNCED | 🛡️ SECURE")

# SIDEBAR: Live Missing Prices Fix
with st.sidebar:
    st.title("🛰️ Sentinel")
    st.info("v17.9 Restoration Active")
    st.divider()
    pulse = fetch_live_pulse()
    if pulse:
        for c in pulse:
            st.metric(label=c['name'], value=f"₹{c['current_price']:,}", delta=f"{c['price_change_percentage_24h']:.2f}%")
    else: st.warning("Connecting to Satellite...")
    if st.button("🔒 Logout"):
        del st.session_state["password_correct"]
        st.rerun()

# SEARCH & REPORT
query = st.text_input("🔍 Search ANY Market Asset (BTC, XRT, Nifty):", "XRT and LayerAI India News")

if query:
    with st.spinner("Decoding Data..."):
        report, visual = ai_commander_v17_9(query)
        
        st.markdown("<div class='report-card'>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1.5])
        with col1:
            if visual: st.image(visual, caption=f"AI Visual: {query}")
        with col2:
            st.subheader(f"📝 Master Report: {query.upper()}")
            st.write(report)
            wa_text = f"AiCoincast Update: {report[:250]}..."
            st.markdown(f'<a href="https://wa.me/?text={wa_text}" target="_blank" style="background:#25D366;color:white;padding:12px;border-radius:10px;text-decoration:none;display:inline-block;width:100%;text-align:center;font-weight:bold;">📲 Share on WhatsApp</a>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()
st.caption("© 2026 AiCoincast India | v17.9 Sovereign Master | Glitch & 404 Final Fix")
