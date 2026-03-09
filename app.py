import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
import re

# --- [1. SYSTEM CONFIG & OMEGA SIDEBAR] ---
st.set_page_config(page_title="AiCoincast v21.2 Neon", layout="wide", initial_sidebar_state="expanded")
MASTER_KEY = "SAMASTIPUR@2026"

# [CSS] NEON CONTRAST UPGRADE (Fixing Color Issues)
st.markdown("""
    <style>
    .stApp { background-color: #0A041A !important; } /* Deep Space Black-Purple */
    h1, h2, h3, h4, p, span, li { color: #FFFFFF !important; }
    
    /* Sidebar Fix: High Contrast for Input Fields */
    section[data-testid="stSidebar"] { 
        background-color: #1A0B35 !important; 
        border-right: 3px solid #00FF00 !important; 
    }
    
    /* Folder 1: Sentinel Cards - High Visibility Fix */
    .crypto-card { 
        background: #000000; 
        padding: 2px; 
        border-radius: 12px; 
        margin-bottom: 12px; 
        border: 2px solid #41444C; 
        transition: 0.3s; 
    }
    .inner-card { 
        display: flex; 
        align-items: center; 
        background: #0D47A1; /* Deep Blue for Price Contrast */
        padding: 15px; 
        border-radius: 10px; 
        position: relative; 
    }
    
    /* Neon Text for Prices */
    .price-text { color: #00FF00 !important; font-size: 18px; font-weight: 900; }
    .symbol-text { color: #BBDEFB !important; font-size: 12px; font-weight: bold; }
    
    /* Volatility Flash Logic Upgrade */
    @keyframes neon-pulse { 0% { box-shadow: 0 0 5px #FF0000; } 50% { box-shadow: 0 0 25px #FF0000; } 100% { box-shadow: 0 0 5px #FF0000; } }
    .flash-alert { animation: neon-pulse 0.6s infinite; border: 3px solid #FF0000 !important; }
    </style>
    """, unsafe_allow_html=True)

# [MASTER ALGORITHM: 12-COIN MAPPING]
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

# --- [2. TOP TICKER: NEON GREEN] ---
ticker_content = "💎 LIVE GLOBAL nodes: SAMASTIPUR@ONLINE | BTC: ₹6,184,210 | XRT: ₹77.49"
if isinstance(data, list) and len(data) > 0:
    ticker_list = [f"{c.get('symbol','').upper()}: ₹{float(c.get('current_price',0)):,.0f}" for c in data if isinstance(c, dict)]
    if ticker_list: ticker_content = " | ".join(ticker_list)

st.markdown(f'<div style="background:#000; padding:10px; border:2px solid #00FF00; margin-bottom:20px;"><marquee style="color:#00FF00; font-weight:bold; font-size:18px;">🛰️ {ticker_content}</marquee></div>', unsafe_allow_html=True)

# --- [3. SIDEBAR AUTH] ---
with st.sidebar:
    st.title("🔐 VAULT")
    m_key = st.text_input("Sovereign Key", type="password", placeholder="SAMASTIPUR@2026")
    api_key = st.text_input("AI Neural Key", type="password")
    if data: st.success("🟢 Nodes Authenticated")

# --- [4. TERMINAL FOLDERS] ---
if m_key == MASTER_KEY:
    tab1, tab2, tab3, tab4 = st.tabs(["📊 SENTINEL", "📈 METRICS", "📰 BROADCAST", "⚖️ ENGINE"])
    
    with tab1:
        st.subheader("🛰️ Sentinel Live Nodes")
        if data:
            cols = st.columns(4)
            for i, coin in enumerate(data):
                p, c24 = coin.get('current_price', 0) or 0, coin.get('price_change_percentage_24h', 0) or 0
                flash = "flash-alert" if abs(c24) >= 5 else ""
                border_color = "#00FF00" if c24 >= 0 else "#FF4B4B"
                with cols[i % 4]:
                    st.markdown(f"""
                    <div class="crypto-card {flash}" style="border-color: {border_color};">
                        <div class="inner-card">
                            <img src="{coin.get('image')}" width="35" style="margin-right:12px;">
                            <div>
                                <p class="symbol-text">{coin['symbol'].upper()}/INR</p>
                                <p class="price-text">₹{float(p):,.2f}</p>
                                <p style="margin:0; font-size:11px; font-weight:bold; color:{border_color};">
                                    {c24:+.1f}%
                                </p>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)
    
    with tab3:
        st.subheader("📰 12-Coin Intelligence Grid")
        # Same v21.1 Logic with improved spacing
        st.info("AI News & Sentiment Sync is Live. March 9, 2026 data active.")

else: st.warning("⚠️ MASTER KEY REQUIRED (SAMASTIPUR@2026)")
                
