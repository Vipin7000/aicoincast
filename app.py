import streamlit as st
import yfinance as yf
import google.generativeai as genai
import requests
import time
from datetime import datetime
import pytz
import streamlit.components.v1 as components

# --- 1. SYSTEM IDENTITY & VISIBILITY THEME ---
st.set_page_config(page_title="AiCoincast v17.7 Sovereign", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
MASTER_PASSWORD = "SAMASTIPUR@2026"

# FIX: CSS for Price Visibility (Dark Background par Neon Blue text)
st.markdown("""
    <style>
    .main { background-color: #030008; color: #FFFFFF; }
    /* Sidebar Metric Visibility Fix */
    [data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: #00F5FF !important;
        font-weight: bold !important;
        font-size: 1.5rem !important;
    }
    [data-testid="stSidebar"] [data-testid="stMetricLabel"] {
        color: #FFFFFF !important;
        opacity: 0.9;
    }
    .stMetric { background-color: #10002B; padding: 15px; border-radius: 12px; border: 1px solid #BC13FE; }
    .report-card { background: rgba(16,0,43,0.95); border: 2px solid #BC13FE; padding: 25px; border-radius: 20px; box-shadow: 0px 0px 15px #BC13FE; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. IRON VAULT GATEWAY ---
if "password_correct" not in st.session_state:
    st.markdown("<h2 style='text-align: center; color: #BC13FE;'>🛡️ Sovereign Iron Vault</h2>", unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        pwd = st.text_input("Enter Master Key:", type="password")
        if st.button("Unlock Terminal"):
            if pwd == MASTER_PASSWORD:
                st.session_state["password_correct"] = True
                st.rerun()
            else: st.error("🚫 Access Denied")
    st.stop()

# --- 3. THE OMNISCIENT AI ENGINE (Final 404 Fix) ---
def get_ai_report_v17_7(query):
    try:
        if "GEMINI_API_KEY" not in st.secrets: return "❌ Key Missing", None
        
        # Explicitly configure to bypass v1beta issue
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        
        # FIXED: Standardized model call to avoid 404
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Simple content generation with strict limits
        res = model.generate_content(f"3-line Hinglish crypto report on {query} for Indian market.")
        
        img = f"https://pollinations.ai/p/{query.replace(' ','_')}_digital_art?seed={time.time()}"
        return res.text, img
    except Exception as e:
        # User-friendly fallback if AI is still busy
        return f"⚠️ Node Recalibrating. Error: 404/Connection Issue. Please check API settings.", None

# --- 4. DATA PULSE ALGORITHM (CEX/DEX) ---
def fetch_pulse():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_desc&per_page=6&page=1"
        return requests.get(url, timeout=5).json()
    except: return []

# --- 5. MAIN INTERFACE ---
st.title("🤖 AiCoincast v17.7 Master Node")
st.caption(f"Status: Sovereign | Node: Reliance Digital | {datetime.now(IST).strftime('%H:%M:%S')}")

# Top Ticker (v12.0)
st.markdown(f'<div style="background:#BC13FE;color:white;padding:10px;"><marquee scrollamount="8">📈 NIFTY 50 LIVE | 🪙 BITCOIN PRICE: SYNCED | 🛰️ AI COMMANDER ONLINE</marquee></div>', unsafe_allow_html=True)

# SIDEBAR: Price Visibility Fix
with st.sidebar:
    st.title("🛰️ Sentinel")
    st.success("v17.7 Node Active")
    st.divider()
    pulse = fetch_pulse()
    if pulse:
        for c in pulse:
            # Color coding for 24h change
            delta_color = "normal" if c['price_change_percentage_24h'] > 0 else "inverse"
            st.metric(
                label=f"{c['name']} ({c['symbol'].upper()})", 
                value=f"₹{c['current_price']:,}", 
                delta=f"{c['price_change_percentage_24h']:.2f}%",
                delta_color=delta_color
            )
    else:
        st.warning("Market Syncing...")
    
    st.divider()
    if st.button("🔒 Secure Logout"):
        del st.session_state["password_correct"]
        st.rerun()

# Main Search
query = st.text_input("🔍 Search ANY Market Asset:", "XRT and LayerAI India News")
if query:
    with st.spinner("AI Bot Analyzing Global Data..."):
        report, visual = get_ai_report_v17_7(query)
        
        st.markdown("<div class='report-card'>", unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1.5])
        with c1:
            if visual: st.image(visual, caption="AI Contextual Visual")
        with c2:
            st.subheader(f"📝 Sovereign Report: {query.upper()}")
            st.info(report)
            wa_text = f"AiCoincast Master Update: {report[:250]}..."
            st.markdown(f'<a href="https://wa.me/?text={wa_text}" target="_blank" style="background:#25D366;color:white;padding:12px;border-radius:10px;text-decoration:none;display:inline-block;width:100%;text-align:center;font-weight:bold;">📲 Share on WhatsApp</a>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()
st.caption("© 2026 AiCoincast India | v17.7 Price Visibility & AI Fix | Samastipur Master Node")
    
