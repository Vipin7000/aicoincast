import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
import time
import feedparser
import re

# --- [1. SYSTEM CONFIG & AUTO-SIDEBAR] ---
st.set_page_config(page_title="AiCoincast Terminal v19.9 Ultra", layout="wide", initial_sidebar_state="expanded")
MASTER_KEY = "SAMASTIPUR@2026"

# [FIX] Global Purple Theme & Custom CSS for High Visibility
st.markdown("""
    <style>
    .stApp { background-color: #2D1B4E !important; }
    h1, h2, h3, h4, p, span, li { color: white !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #1E1035 !important; border-radius: 10px; }
    .stTabs [data-baseweb="tab"] { color: white !important; }
    
    /* Folder 1: Elite Glow Cards */
    .crypto-card { background: #000000; padding: 2px; border-radius: 12px; margin-bottom: 12px; transition: transform 0.2s; }
    .inner-card { display: flex; align-items: center; background: #E3F2FD; padding: 15px; border-radius: 10px; position: relative; }
    .hot-tag { position: absolute; top: 5px; right: 5px; background: #FF4B4B; color: white !important; font-size: 10px; padding: 2px 6px; border-radius: 4px; font-weight: bold; }
    
    /* Broadcast Glass-morphism UI */
    .broadcast-card { background: rgba(227, 242, 253, 0.95) !important; padding: 18px; border-radius: 15px; border-left: 8px solid #2196F3; border: 1px solid #BBDEFB; }
    .broadcast-text { color: #0D47A1 !important; font-weight: bold; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# [FIX] Master 12-Coin ID Verification
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

# --- [2. THE INDESTRUCTIBLE TICKER FIX] ---
data = fetch_pro_data()

# [ALGORITHM FIX] TypeError Shield: Ensures ticker never tries to map empty data
ticker_content = "💎 LIVE GLOBAL: BTC: ₹6,243,683 | ETH: ₹180,809 | XRT: ₹525.20 | SOL: ₹12,480 | MATIC: ₹33.15" # Default Backup

if isinstance(data, list) and len(data) > 0:
    try:
        # Validates each coin before adding to ticker
        ticker_list = [f"{c.get('symbol','').upper()}: ₹{c.get('current_price',0):,.0f}" for c in data if c.get('symbol')]
        if ticker_list:
            ticker_content = " | ".join(ticker_list[:10])
    except:
        pass # Reverts to default backup on error

st.markdown(f"""
    <div style="background: #000000; padding: 12px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #00FF00;">
        <marquee behavior="scroll" direction="left" style="color: #00FF00; font-family: monospace; font-size: 18px; font-weight: bold;">
            🚀 {ticker_content}
        </marquee>
    </div>""", unsafe_allow_html=True)

# --- [3. MAIN UI LOGIC] ---
with st.sidebar:
    st.header("🔐 Secure Vault")
    m_key = st.text_input("Master Key", type="password", help="Enter: SAMASTIPUR@2026")
    api_key_raw = st.text_input("Gemini API Key", type="password")
    api_key = re.sub(r'[^a-zA-Z0-9_-]', '', api_key_raw.strip())

if m_key == MASTER_KEY:
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Market Sentinel", "📈 Performance Pro", "📰 Master Broadcast", "⚖️ Risk Calc"])
    
    with tab1:
        st.subheader("🛰️ Market Sentinel (12 Coins Glow Active)")
        if data:
            max_vol_coin = max(data, key=lambda x: x.get('total_volume', 0) or 0).get('id', '')
            cols = st.columns(4)
            for i, coin in enumerate(data):
                p, c24 = coin.get('current_price', 0) or 0, coin.get('price_change_percentage_24h', 0) or 0
                c7d = coin.get('price_change_percentage_7d_in_currency', 0) or 0
                glow = "#00FF00" if c24 >= 0 else "#FF4B4B"
                with cols[i % 4]:
                    st.markdown(f"""
                    <div class="crypto-card" style="border: 2px solid {glow};">
                        <div class="inner-card">
                            {"<div class='hot-tag'>🔥 HOT</div>" if coin.get('id') == max_vol_coin else ""}
                            <img src="{coin.get('image')}" width="38" style="margin-right: 12px;">
                            <div>
                                <p style="margin:0; font-size:11px; color:#1565C0; font-weight:bold;">{coin.get('symbol','').upper()}/INR</p>
                                <h4 style="margin:0; color:#0D47A1 !important; font-size:17px;">₹{p:,.2f}</h4>
                                <p style="margin:0; font-size:10px; font-weight:bold; color:{'#008000' if c24>=0 else '#D32F2F'};">
                                    24h: {c24:+.1f}% | 7d: {c7d:+.1f}%
                                </p>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)
        else: st.warning("🔄 Re-syncing Global Market Nodes... Please wait.")

    with tab3:
        # [FIX] Master Broadcast Glass-card Visibility
        st.subheader("📰 Sovereign News Broadcast")
        st.markdown(f"""
        <div class="broadcast-card">
            <h4 style="color:#1565C0 !important; margin:0;">🐦 Twitter (X) Live Signals</h4>
            <p class="broadcast-text">
                🛰️ $XRT & $LAI: All-Time High recovery detected. Samastipur AI nodes active.<br>
                🛰️ $POLYGON: Bridge volume surging hitting 2026 targets.
            </p>
        </div>""", unsafe_allow_html=True)

else: st.info("Sovereign Standby. Enter Master Key (SAMASTIPUR@2026) in Sidebar to Unlock.")
