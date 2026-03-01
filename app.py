import streamlit as st
import yfinance as yf
import google.generativeai as genai
import requests
import time
from datetime import datetime
import pytz
import streamlit.components.v1 as components

# --- 1. SETTINGS & SYSTEM IDENTITY ---
st.set_page_config(page_title="AiCoincast Omniscient v17.3", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
MASTER_PASSWORD = "SAMASTIPUR@2026"

# --- 2. GLOBAL MARKET ENGINE (CoinGecko Integration) ---
def get_live_market_data():
    try:
        # Fetching Top 5 Coins like CoinGecko Dashboard
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_desc&per_page=10&page=1"
        response = requests.get(url, timeout=10)
        return response.json()
    except Exception:
        return []

# --- 3. LOGIN GUARD (v16.3 Iron Vault) ---
if "password_correct" not in st.session_state:
    st.markdown("<h2 style='text-align: center; color: #BC13FE;'>🛡️ Sovereign Iron Vault</h2>", unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        pwd = st.text_input("Enter Master Key:", type="password")
        if st.button("Unlock Terminal"):
            if pwd == MASTER_PASSWORD:
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("🚫 Access Denied")
    st.stop()

# --- 4. THE AI COMMANDER (Fixed 404 & Model Naming) ---
def ai_node_commander(query):
    try:
        if "GEMINI_API_KEY" not in st.secrets:
            return "❌ API Key Missing!", None
        
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # Standardized Model Call (Fixed version mismatch)
        model = genai.GenerativeModel('gemini-1.5-flash') 
        
        prompt = f"Professional Report: Analyze {query} for Indian market. Use Hinglish. 2 lines max."
        res = model.generate_content(prompt)
        
        # Visual Link
        img = f"https://pollinations.ai/p/{query.replace(' ','_')}_crypto_tech?seed={time.time()}"
        return res.text, img
    except Exception as e:
        return f"Node Syncing... (Error: {str(e)})", None

# --- 5. UI: OMNISCIENT DASHBOARD ---

# Top Ticker (v12.0)
ticker_html = """<div style="background-color: #BC13FE; color: white; padding: 10px; font-weight: bold;"><marquee scrollamount="8">📈 NIFTY 50 LIVE | 🪙 CRYPTO GLOBAL CAP: LIVE | 🛰️ AI COMMANDER ONLINE</marquee></div>"""
components.html(ticker_html, height=50)

# Sidebar: Market Pulse (CoinGecko Style)
with st.sidebar:
    st.title("🛰️ System Sentinel")
    st.success("v17.3 Master Node Active")
    st.divider()
    
    st.subheader("🪙 Live Crypto Pulse (INR)")
    market_items = get_live_market_data()
    if market_items:
        for item in market_items[:5]:
            change = item['price_change_percentage_24h']
            color = "#00FF00" if change > 0 else "#FF0000"
            st.markdown(f"**{item['name']}**: ₹{item['current_price']:,} (<span style='color:{color}'>{change:.2f}%</span>)", unsafe_allow_html=True)
    else:
        st.warning("Market Data Syncing...")
    
    st.divider()
    if st.button("🔒 Secure Logout"):
        del st.session_state["password_correct"]
        st.rerun()

# Main Terminal
st.title("🤖 AiCoincast v17.3 Master")
target = st.text_input("🔍 Search Any Asset (XRT, LAI, Nifty):", "XRT and LayerAI India News")

if target:
    with st.spinner("AI Bot Analyzing..."):
        report, visual = ai_node_commander(target)
        
        st.markdown("<div style='border:2px solid #BC13FE; padding:20px; border-radius:15px; background:rgba(16,0,43,0.95);'>", unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1.3])
        with c1:
            if visual: 
                # Removed 'use_container_width' to fix AttributeError
                st.image(visual) 
        with c2:
            st.subheader(f"📝 Master Report: {target.upper()}")
            st.info(report)
            wa_text = f"AiCoincast Update: {report[:250]}..."
            st.markdown(f'<a href="https://wa.me/?text={wa_text}" target="_blank" style="background:#25D366; color:white; padding:12px; border-radius:10px; text-decoration:none; display:inline-block; width:100%; text-align:center; font-weight:bold;">📲 Share on WhatsApp</a>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()
st.caption("© 2026 AiCoincast India | v17.3 Sovereign Master Sync | Fixed all Node & Rendering Issues")
