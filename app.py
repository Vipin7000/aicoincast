import streamlit as st
import yfinance as yf
import google.generativeai as genai
import requests
import time
from datetime import datetime
import pytz

# --- 1. SYSTEM IDENTITY & CLEAN UI THEME ---
st.set_page_config(page_title="AiCoincast v17.8 Sovereign", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
MASTER_PASSWORD = "SAMASTIPUR@2026"

# FIX: CSS for Price Visibility & Removing Black Bar Glitch
st.markdown("""
    <style>
    .main { background-color: #030008; color: #FFFFFF; }
    /* Sidebar Metric Visibility - Neon Blue */
    [data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: #00F5FF !important;
        font-weight: bold !important;
    }
    /* Removing the black horizontal glitch bar */
    .stProgress > div > div > div > div { background-color: transparent !important; }
    hr { border-top: 1px solid #BC13FE !important; margin: 10px 0 !important; }
    .report-card { background: rgba(16,0,43,0.95); border: 2px solid #BC13FE; padding: 25px; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. IRON VAULT GATEWAY ---
if "password_correct" not in st.session_state:
    st.markdown("<h3 style='text-align: center; color: #BC13FE;'>🛡️ Sovereign Iron Vault</h3>", unsafe_allow_html=True)
    pwd = st.text_input("Enter Master Key:", type="password")
    if st.button("Unlock Terminal"):
        if pwd == MASTER_PASSWORD:
            st.session_state["password_correct"] = True
            st.rerun()
    st.stop()

# --- 3. THE OMNISCIENT AI ENGINE (Stable Model Call) ---
def get_ai_report_v17_8(query):
    try:
        if "GEMINI_API_KEY" not in st.secrets: return "❌ Key Missing", None
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # Explicitly using flash for speed and to avoid 404
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(f"Crypto/Market report in 2 lines Hinglish: {query}")
        img = f"https://pollinations.ai/p/{query.replace(' ','_')}_futuristic?seed={time.time()}"
        return res.text, img
    except Exception as e:
        return f"Node Syncing... (Details: {str(e)})", None

# --- 4. DATA PULSE ALGORITHM (CEX/DEX) ---
def fetch_pulse():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_desc&per_page=6&page=1"
        return requests.get(url, timeout=5).json()
    except: return []

# --- 5. MAIN INTERFACE ---
st.title("🤖 AiCoincast v17.8 Master Node")
st.caption(f"Sovereign Node Active | Reliance Digital Hub | {datetime.now(IST).strftime('%H:%M:%S')}")

# Top Ticker (Clean Style)
st.info("🛰️ AI COMMANDER ONLINE | MARKET DATA SYNCED | RELIANCE DIGITAL SECURE")

# SIDEBAR: High-Contrast Prices
with st.sidebar:
    st.title("🛰️ Sentinel")
    st.success("v17.8 Node Active")
    st.divider()
    pulse = fetch_pulse()
    if pulse:
        for c in pulse:
            st.metric(label=c['name'], value=f"₹{c['current_price']:,}", delta=f"{c['price_change_percentage_24h']:.2f}%")
    else: st.warning("Pulse Offline")
    if st.button("🔒 Logout"):
        del st.session_state["password_correct"]
        st.rerun()

# Main Search Area
query = st.text_input("🔍 Search Any Market Asset:", "XRT and LayerAI India News")

if query:
    with st.spinner("AI Bot Analyzing..."):
        report, visual = get_ai_report_v17_8(query)
        st.markdown("<div class='report-card'>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1.5])
        with col1:
            if visual: st.image(visual)
        with col2:
            st.subheader(f"📝 Sovereign Report: {query.upper()}")
            st.write(report)
            wa_text = f"AiCoincast Update: {report[:250]}..."
            st.markdown(f'<a href="https://wa.me/?text={wa_text}" target="_blank" style="background:#25D366;color:white;padding:12px;border-radius:10px;text-decoration:none;display:inline-block;width:100%;text-align:center;font-weight:bold;">📲 Share on WhatsApp</a>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()
st.caption("© 2026 AiCoincast India | v17.8 Sovereign Master | Glitch Fixed")
