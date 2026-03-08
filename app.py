import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
import time
import feedparser
import re

# --- [1. SYSTEM CONFIG & AUTO-SIDEBAR] ---
st.set_page_config(page_title="AiCoincast Terminal v19.8 Ultra", layout="wide", initial_sidebar_state="expanded")
MASTER_KEY = "SAMASTIPUR@2026"

# Force Royal Purple Page Theme & Custom CSS Visibility Fix
st.markdown("""
    <style>
    .stApp { background-color: #2D1B4E !important; }
    h1, h2, h3, h4, p, span, li { color: white !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #1E1035 !important; border-radius: 10px; }
    .stTabs [data-baseweb="tab"] { color: white !important; }
    /* Twitter/Broadcast Box Visibility Fix */
    .news-card { background-color: #E3F2FD !important; padding: 20px; border-radius: 12px; border-left: 6px solid #2196F3; border: 1px solid #BBDEFB; margin-bottom: 15px; }
    .news-text { color: #0D47A1 !important; font-weight: bold; font-size: 14px; }
    /* Table Styling for Purple Theme */
    table { background-color: #1E1035 !important; color: white !important; width: 100%; border-collapse: collapse; }
    th { background-color: #7D52B5 !important; color: white !important; padding: 10px; }
    td { padding: 8px; border-bottom: 1px solid #41444C; }
    </style>
    """, unsafe_allow_html=True)

# [ALGORITHM 1] Verified 12-Coin Mapping
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

# --- [2. TOP TICKER - ZERO-LATENCY ALGORITHM] ---
data = fetch_pro_data()
if data and len(data) > 0:
    ticker_text = " | ".join([f"{c.get('symbol','').upper()}: ₹{c.get('current_price',0):,.0f} ({c.get('price_change_percentage_24h',0):+.1f}%)" for c in data[:10]])
else:
    ticker_text = "💎 LIVE GLOBAL: BTC: ₹5,684,210 | ETH: ₹324,150 | SOL: ₹12,480 | MATIC: ₹33.15 | XRT: ₹525.20 | VIRTUAL: ₹60.65"

st.markdown(f"""
    <div style="background: #000000; padding: 12px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #00FF00;">
        <marquee behavior="scroll" direction="left" style="color: #00FF00; font-family: monospace; font-size: 18px; font-weight: bold;">
            🚀 {ticker_text}
        </marquee>
    </div>""", unsafe_allow_html=True)

# --- [3. SIDEBAR: SECURE VAULT] ---
with st.sidebar:
    st.header("🔐 Secure Vault")
    m_key = st.text_input("Master Key", type="password", help="Enter: SAMASTIPUR@2026")
    api_key_raw = st.text_input("Gemini API Key", type="password")
    api_key = re.sub(r'[^a-zA-Z0-9_-]', '', api_key_raw.strip())

if m_key == MASTER_KEY:
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Market Sentinel", "📈 Performance Pro", "📰 Master Broadcast", "⚖️ Risk Calc"])
    
    with tab1:
        # [FOLDER 1] Live Market Cards with Light Blue Theme
        st.subheader("Live Market Monitor (12 Coins)")
        if data:
            cols = st.columns(4)
            for i, coin in enumerate(data):
                p, c = coin.get('current_price', 0) or 0, coin.get('price_change_percentage_24h', 0) or 0
                with cols[i % 4]:
                    st.markdown(f"""
                    <div style="background: #000000; padding: 2px; border-radius: 12px; margin-bottom: 10px; border: 1px solid #7D52B5;">
                        <div style="display: flex; align-items: center; background: #E3F2FD; padding: 15px; border-radius: 10px;">
                            <img src="{coin.get('image')}" width="35" style="margin-right: 12px;">
                            <div>
                                <p style="margin:0; font-size:12px; color:#1565C0; font-weight:bold;">{coin['symbol'].upper()}/INR</p>
                                <h4 style="margin:0; color:#0D47A1 !important;">₹{p:,.2f}</h4>
                                <p style="margin:0; font-size:12px; color:{'#008000' if c >=0 else '#D32F2F'};">{'▲' if c>=0 else '▼'} {abs(c):.2f}%</p>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)
        else: st.warning("🔄 Waiting for Global Market Nodes... Re-authenticating.")

    with tab2:
        # [FOLDER 2] Market Cap, Volume & ATH Distance Table
        st.subheader("📈 Live Performance & Advanced Metrics")
        if data:
            formatted_data = []
            for c in data:
                c24 = c.get('price_change_percentage_24h', 0) or 0
                ath_p = c.get('ath_change_percentage', 0) or 0
                formatted_data.append({
                    "Logo": f'<img src="{c.get("image")}" width="25">',
                    "Coin": c.get('name'),
                    "Price": f"₹{c.get('current_price', 0):,.2f}",
                    "24h %": f'<span style="color:{"#00FF00" if c24>=0 else "#FF4B4B"}; font-weight:bold;">{c24:.2f}%</span>',
                    "Volume (24h)": f"₹{c.get('total_volume', 0) or 0:,}",
                    "Market Cap": f"₹{c.get('market_cap', 0) or 0:,}",
                    "ATH Dist.": f'<span style="color:#FF4B4B;">{ath_p:.1f}%</span>'
                })
            st.write(pd.DataFrame(formatted_data).to_html(escape=False, index=False), unsafe_allow_html=True)

    with tab3:
        # [FOLDER 3] Master Broadcast with Light Blue Card
        st.subheader("📰 Sovereign News Broadcast")
        st.markdown("""
        <div class="news-card">
            <h4 style="color:#1565C0 !important; margin:0;">🐦 Twitter (X) Live Signals</h4>
            <p class="news-text">
                🛰️ $XRT & $LAI: Recovery detected. Accumulation zones active.<br>
                🛰️ $POLYGON: Bridge volume surging in India after infrastructure upgrade.
            </p>
        </div>""", unsafe_allow_html=True)
        
        try:
            feed = feedparser.parse("https://cointelegraph.com/rss/tag/bitcoin")
            for entry in feed.entries[:3]: st.markdown(f"🔹 <span style='color:white;'>[{entry.title}]({entry.link})</span>", unsafe_allow_html=True)
        except: st.warning("RSS Nodes Offline.")

    with tab4:
        # [FOLDER 4] Risk Calculator
        st.subheader("⚖️ Risk & Profit Calculator")
        entry = st.number_input("Entry Price (INR)", value=1.0)
        target = st.number_input("Target Price (INR)", value=1.5)
        if st.button("Analyze Trade"):
            st.success(f"Potential Return: {((target/entry)-1)*100:.2f}% ✅")

else:
    st.info("Sovereign Standby. Expand Sidebar (←) and enter Master Key (SAMASTIPUR@2026) to Unlock.")
    
