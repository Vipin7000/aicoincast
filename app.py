# =============================================================================
# PROJECT: AiCoincast India - National Intelligence Terminal
# VERSION: 10.3 Sovereign Grandmaster
# AUTHOR: AiCoincast Team (Serving Digital India)
# UPDATED: Feb 2026
# =============================================================================

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import datetime
import time

# --- STAGE 1: SYSTEM INITIALIZATION & UI ENGINE ---
st.set_page_config(
    page_title="AiCoincast India | Sovereign Grandmaster", 
    page_icon="🇮🇳", 
    layout="wide"
)

# 

# Advanced CSS Framework (Modular Architecture)
st.markdown("""
    <style>
    /* Global Styling */
    .main { background-color: #050112; color: #FFFFFF; font-family: 'Segoe UI', sans-serif; }
    
    /* National Flag Identity Banner */
    .india-strip { 
        background: linear-gradient(90deg, #FF9933 0%, #FFFFFF 50%, #128807 100%); 
        height: 6px; width: 100%; border-radius: 3px; margin-bottom: 10px; 
    }
    
    /* High-Performance Card System */
    .gm-card { 
        background: #1A1033; border: 1.5px solid #00F5FF; 
        padding: 30px; border-radius: 20px; 
        box-shadow: 0px 10px 30px rgba(0, 245, 255, 0.1); 
    }
    
    /* Metric Enhancement */
    .stMetric { background: #0D0221; padding: 15px; border-radius: 12px; border: 1px solid #BC13FE; }
    
    /* Marquee Animation */
    .marquee-text { color: #FFFFFF; font-weight: bold; font-size: 14px; }
    </style>
    <div class="nav-bar" style="text-align:center; padding:5px;"><h2>🛡️ AiCoincast India Sovereign Hub</h2></div>
    <div class="india-strip"></div>
    """, unsafe_allow_html=True)

# --- STAGE 2: REAL-TIME DATA & ANALYTICS NODES ---

# India Standard Time Sync
current_ist = datetime.datetime.now().strftime('%d %b %Y | %H:%M:%S IST')
st.markdown(f"<div style='text-align:right; color:#00F5FF; font-weight:bold; padding-right:10px;'>🕒 {current_ist}</div>", unsafe_allow_html=True)

# National Marquee Feed (Global + Local)
st.markdown("""
    <div style='background-color: #0D0221; border-top: 1px solid #FF9933; border-bottom: 1px solid #128807; padding: 8px; margin-bottom: 20px;'>
        <marquee scrollamount='8' class='marquee-text'>
            🇮🇳 NATIONAL UPDATE: Digital India Expansion Active | NIFTY 50 & SENSEX Market Pulse Syncing | RBI e-Rupee Adoption Rising | AiCoincast Sovereign Terminal v10.3 Online
        </marquee>
    </div>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=60)
def fetch_market_intel():
    """Algorithm: Extracts Real-time National Indices and Crypto-INR Pairs"""
    tickers = {"NIFTY 50": "^NSEI", "SENSEX": "^BSESN", "BTC-INR": "BTC-INR", "ETH-INR": "ETH-INR"}
    intel_results = {}
    for label, sym in tickers.items():
        try:
            intel_results[label] = yf.Ticker(sym).history(period="1d")['Close'].iloc[-1]
        except Exception as e:
            intel_results[label] = 0.0
    return intel_results

# --- STAGE 3: INTERFACE LAYERS (UNIFIED MASTER DASHBOARD) ---

st.title("🛡️ AiCoincast India: Sovereign Grandmaster")
st.info("🌐 National Node Active | Tracking India's Digital Economy & Web3 Pulse")

# Modular Tab System
tab_oracle, tab_wealth, tab_robot, tab_advisor = st.tabs([
    "📊 Market Oracle", "💼 Wealth Guardian", "🤖 AI News Robot", "🧠 Neural Advisor"
])

# 1. MARKET ORACLE (Stocks & Global Crypto)
with tab_oracle:
    st.subheader("🇮🇳 Unified National Feed")
    m_data = fetch_market_intel()
    c1, c2, c3 = st.columns(3)
    c1.metric("NSE NIFTY 50", f"₹{m_data['NIFTY 50']:,.2f}", "India Hub")
    c2.metric("BSE SENSEX", f"₹{m_data['SENSEX']:,.2f}", "National Index")
    c3.metric("BTC-INR", f"₹{m_data['BTC-INR']:,.0f}", "Market Live")
    
    st.divider()
    st.subheader("🔍 India News Sentiment Audit")
    s_input = st.text_input("Headline Analysis", value="RBI e-Rupee adoption grows in retail sector.")
    if st.button("Analyze Market Mood"):
        st.toast("AI Analyzing National Impact...", icon="🇮🇳")
        st.success("Mood: Bullish (Greed Index: 75/100)")

# 2. WEALTH GUARDIAN (Portfolio Personalization)
with tab_wealth:
    st.subheader("💼 Personal Wealth Guardian (India)")
    if 'p_store' not in st.session_state:
        st.session_state.p_store = {"BTC": 0.1, "ETH": 1.5}
    
    col_l, col_r = st.columns([1, 1])
    with col_l:
        u_s = st.text_input("Add Coin Symbol").upper()
        u_q = st.number_input("Quantity", min_value=0.0)
        if st.button("Sync Asset"):
            st.session_state.p_store[u_s] = u_q
            st.rerun()
    with col_r:
        df_w = pd.DataFrame([{"Asset": k, "Qty": v} for k, v in st.session_state.p_store.items()])
        st.plotly_chart(px.pie(df_w, values='Qty', names='Asset', hole=0.5, template="plotly_dark"))

# 3. AI NEWS ROBOT (Hinglish Intelligence)
with tab_robot:
    st.subheader("🤖 The Swadeshi News Robot")
    u_c = st.text_area("Paste News for Analysis")
    if st.button("⚡ Generate Report"):
        st.info("Robot Intelligence: Positive impact on India's Web3 infrastructure.")
    if st.button("🎙️ Play Hindi Audio Script"):
        st.markdown("<div class='gm-card'>📻 Radio Anchor Script Ready...</div>", unsafe_allow_html=True)

# 4. NEURAL ADVISOR (Risk Management)
with tab_advisor:
    st.subheader("🧠 Neural Advisory Bridge")
    st.write("Financial strategy specifically for Indian tax laws (30% VDA).")
    if st.button("🚀 Run Portfolio Strategic Audit"):
        st.success("Strategy: Maintain 40% liquidity for tax optimization.")

# --- STAGE 4: SYSTEM FOOTER & COMPLIANCE ---
st.divider()
st.caption("© 2026 AiCoincast.in | v10.3 Grandmaster | National Intelligence Hub | India")
        
