import streamlit as st
import yfinance as yf
import google.generativeai as genai
import requests
import time
from datetime import datetime
import pytz

# --- 1. SYSTEM IDENTITY & THEME ---
st.set_page_config(page_title="AiCoincast v17.6 Sovereign", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
MASTER_PASSWORD = "SAMASTIPUR@2026"

# Cyber-Vault Styling
st.markdown("""
    <style>
    .main { background-color: #030008; color: #FFFFFF; }
    .stMetric { background-color: #10002B; padding: 15px; border-radius: 12px; border: 1px solid #BC13FE; }
    .report-card { background: rgba(16,0,43,0.95); border: 2px solid #BC13FE; padding: 25px; border-radius: 20px; box-shadow: 0px 0px 15px #BC13FE; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. IRON VAULT GATEWAY (v16.3 Security) ---
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

# --- 3. THE OMNISCIENT AI ENGINE (Fixes 404 & Version Errors) ---
def get_ai_report_v17_6(query):
    try:
        if "GEMINI_API_KEY" not in st.secrets: return "❌ Key Missing", None
        
        # Explicit Configuration
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        
        # Try-Catch for Model Versioning
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            res = model.generate_content(f"Market Report (Hinglish): {query}. 3 lines max.")
        except:
            model = genai.GenerativeModel('gemini-pro') # Fallback to older stable model
            res = model.generate_content(f"Analyze {query} in Hinglish briefly.")
            
        img = f"https://pollinations.ai/p/{query.replace(' ','_')}_high_tech?seed={time.time()}"
        return res.text, img
    except Exception as e:
        return f"⚠️ Sync Error: {str(e)}", None

# --- 4. DATA PULSE (CEX/DEX + Indices) ---
def fetch_pulse():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_desc&per_page=5&page=1"
        return requests.get(url, timeout=5).json()
    except: return []

# --- 5. MAIN INTERFACE ---
st.title("🤖 AiCoincast v17.6 Master Node")
st.caption(f"Node: Reliance Digital | Status: Sovereign | {datetime.now(IST).strftime('%H:%M:%S')}")

# Top Ticker (v12.0)
st.markdown(f'<div style="background:#BC13FE;color:white;padding:10px;"><marquee scrollamount="8">🌐 MARKET LIVE | 🛰️ OMNISCIENT AI ACTIVE | 🛡️ SECURED BY IRON VAULT</marquee></div>', unsafe_allow_html=True)

# Sidebar sentinel
with st.sidebar:
    st.title("🛰️ Sentinel")
    st.success("v17.6 Node Active")
    st.divider()
    pulse = fetch_pulse()
    for c in pulse:
        st.metric(c['name'], f"₹{c['current_price']:,}", f"{c['price_change_percentage_24h']:.2f}%")
    if st.button("🔒 Logout"):
        del st.session_state["password_correct"]
        st.rerun()

# Search & Report
query = st.text_input("🔍 Search ANY Market Asset:", "XRT and LayerAI India News")
if query:
    with st.spinner("AI Bot Analyzing Global Data..."):
        report, visual = get_ai_report_v17_6(query)
        
        st.markdown("<div class='report-card'>", unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1.5])
        with c1:
            if visual: st.image(visual) # Fixed Rendering
        with c2:
            st.subheader(f"📝 Sovereign Report: {query.upper()}")
            st.info(report)
            wa_text = f"AiCoincast Master Update: {report[:250]}..."
            st.markdown(f'<a href="https://wa.me/?text={wa_text}" target="_blank" style="background:#25D366;color:white;padding:12px;border-radius:10px;text-decoration:none;display:inline-block;width:100%;text-align:center;font-weight:bold;">📲 Share on WhatsApp</a>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()
st.caption("© 2026 AiCoincast India | v17.6 Final Resilience | Samastipur Master Node")
