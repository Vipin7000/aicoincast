import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
import re

# --- [1. SYSTEM CONFIG & OMEGA SIDEBAR] ---
st.set_page_config(page_title="AiCoincast v21.3 Sovereign", layout="wide", initial_sidebar_state="expanded")
MASTER_KEY = "SAMASTIPUR@2026"

# [CSS] NEON FIX: High Contrast for Sentiment & Sentinel
st.markdown("""
    <style>
    .stApp { background-color: #0A041A !important; }
    h1, h2, h3, h4, p, span, li { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] { background-color: #1A0B35 !important; border-right: 3px solid #00FF00 !important; }
    .crypto-card { background: #000000; padding: 2px; border-radius: 12px; margin-bottom: 12px; border: 2px solid #41444C; transition: 0.3s; }
    .inner-card { display: flex; align-items: center; background: #0D47A1; padding: 15px; border-radius: 10px; position: relative; }
    .price-text { color: #00FF00 !important; font-size: 18px; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

# [MASTER ALGORITHM: 12-COIN MAPPING (v21.3 SYNC)]
COIN_MAP = {
    "bitcoin": "BTC", "ethereum": "ETH", "virtual-protocol": "VIRTUAL", 
    "griffin-2": "GRIFFIN", "v-ai-2": "VAI", "robonomics-network": "XRT", 
    "velas": "VLX", "qanplatform": "QANX", "chaingpt": "CGPT", 
    "sinverse": "SIN", "matic-network": "POLYGON", "nftb": "NFTB"
}

@st.cache_data(ttl=60)
def fetch_pro_data():
    ids = ",".join(COIN_MAP.keys())
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&ids={ids}&order=market_cap_desc&per_page=12&page=1&sparkline=false&price_change_percentage=24h,7d"
    try:
        r = requests.get(url, timeout=15)
        return r.json() if r.status_code == 200 else []
    except: return []

data = fetch_pro_data()

# --- [2. TICKER-SHIELD: V21.3 INDESTRUCTIBLE] ---
# [FIX] Snapshot 1000619894.jpg wala TypeError permanent fix
ticker_content = "📡 Nodes Syncing... | BTC: ₹6,184,210 | ETH: ₹324,150 | XRT: ₹77.49 | LAI: ₹0.0041"
if isinstance(data, list) and len(data) > 0:
    try:
        ticker_list = [f"{c.get('symbol','').upper()}: ₹{float(c.get('current_price',0)):,.0f}" for c in data if isinstance(c, dict) and c.get('symbol')]
        if ticker_list: ticker_content = " | ".join(ticker_list)
    except: pass

st.markdown(f'<div style="background:#000; padding:10px; border:2px solid #00FF00; margin-bottom:20px;"><marquee style="color:#00FF00; font-weight:bold; font-size:18px;">🛰️ {ticker_content}</marquee></div>', unsafe_allow_html=True)

# --- [3. SIDEBAR AUTH] ---
with st.sidebar:
    st.title("🔐 VAULT")
    m_key = st.text_input("Sovereign Key", type="password", placeholder="SAMASTIPUR@2026")
    api_key = st.text_input("Neural Key", type="password")
    if data:
        # [FIX] Snapshot 1000619898.jpg Portfolio MC Error Fix
        total_mc = sum([float(c.get('market_cap', 0)) for c in data if isinstance(c, dict)])
        st.info(f"💼 Portfolio MC: ₹{total_mc:,.0f}")

# --- [4. MAIN TERMINAL LOGIC] ---
if m_key == MASTER_KEY:
    tab1, tab2, tab3, tab4 = st.tabs(["📊 SENTINEL (LIVE)", "📈 PERFORMANCE", "📰 12-COIN BROADCAST", "⚖️ RISK ENGINE"])
    
    with tab1:
        st.subheader("🛰️ Sentinel Nodes (High-Contrast Fix Active)")
        if data:
            cols = st.columns(4)
            for i, coin in enumerate(data):
                p, c24 = coin.get('current_price', 0) or 0, coin.get('price_change_percentage_24h', 0) or 0
                glow = "#00FF00" if c24 >= 0 else "#FF4B4B"
                with cols[i % 4]:
                    st.markdown(f"""
                    <div class="crypto-card" style="border-color: {glow};">
                        <div class="inner-card">
                            <img src="{coin.get('image')}" width="35" style="margin-right:12px;">
                            <div>
                                <p style="margin:0; font-size:11px; color:#BBDEFB;">{coin['symbol'].upper()}/INR</p>
                                <p class="price-text">₹{float(p):,.2f}</p>
                                <p style="margin:0; font-size:10px; font-weight:bold; color:{glow};">24h: {c24:+.1f}%</p>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)
        else: st.warning("🔄 Samastipur Nodes Syncing... (Fallback Ticker Active)")

else: st.info("⚠️ Master Key Required (SAMASTIPUR@2026).")
    
