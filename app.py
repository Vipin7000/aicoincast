import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
import feedparser
import re

# --- [1. SYSTEM CONFIG & AUTO-SIDEBAR] ---
st.set_page_config(
    page_title="AiCoincast Terminal v20.0 Ultra", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

MASTER_KEY = "SAMASTIPUR@2026"

# [FIX] Sidebar Background Color & Card Rendering Fix
st.markdown("""
    <style>
    .stApp { background-color: #2D1B4E !important; }
    h1, h2, h3, h4, p, span, li { color: white !important; }
    
    /* Sidebar: Deep Purple with Clear Borders */
    section[data-testid="stSidebar"] {
        background-color: #1E1035 !important;
        border-right: 2px solid #7D52B5 !important;
    }
    
    /* Folder 1: Sentinel Cards Visibility Fix */
    .crypto-card { background: #000000; padding: 2px; border-radius: 12px; margin-bottom: 12px; }
    .inner-card { display: flex; align-items: center; background: #E3F2FD; padding: 15px; border-radius: 10px; position: relative; }
    .hot-tag { position: absolute; top: 5px; right: 5px; background: #FF4B4B; color: white !important; font-size: 10px; padding: 2px 6px; border-radius: 4px; font-weight: bold; }
    
    /* Performance Table Styles */
    table { background-color: #1E1035 !important; color: white !important; width: 100%; border-radius: 10px; }
    th { background-color: #7D52B5 !important; color: white !important; padding: 12px; text-align: left; }
    td { padding: 10px; border-bottom: 1px solid #41444C; }
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

# --- [2. TOP TICKER - ZERO-ERROR ALGORITHM] ---
ticker_text = " | ".join([f"{c.get('symbol','').upper()}: ₹{c.get('current_price',0):,.0f}" for c in data if c.get('symbol')]) if data else "📡 Nodes Syncing..."
st.markdown(f'<div style="background:#000; padding:12px; border:1px solid #0f0; margin-bottom:20px;"><marquee style="color:#0f0; font-weight:bold; font-size:18px;">🚀 {ticker_text}</marquee></div>', unsafe_allow_html=True)

# --- [3. SIDEBAR: SECURE VAULT (COLOR FIXED)] ---
with st.sidebar:
    st.header("🔐 Secure Vault")
    st.markdown("---")
    m_key = st.text_input("Master Key", type="password", placeholder="SAMASTIPUR@2026")
    
    if data:
        avg = sum([c.get('price_change_percentage_24h', 0) or 0 for c in data]) / len(data)
        st.info(f"Market Sentiment: {'GREED 🚀' if avg > 0 else 'FEAR 📉'}")
        
    api_key_raw = st.text_input("Gemini API Key", type="password", placeholder="Enter AI Key")
    api_key = re.sub(r'[^a-zA-Z0-9_-]', '', api_key_raw.strip())

# --- [4. MAIN TERMINAL LOGIC] ---
if m_key == MASTER_KEY:
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Market Sentinel", "📈 Performance Pro", "📰 Master Broadcast", "⚖️ Risk Calc"])
    
    with tab1:
        st.subheader("🛰️ Market Sentinel (12 Coins Glow)")
        if data:
            max_vol = max(data, key=lambda x: x.get('total_volume', 0) or 0).get('id', '')
            cols = st.columns(4)
            for i, coin in enumerate(data):
                p, c24 = coin.get('current_price', 0) or 0, coin.get('price_change_percentage_24h', 0) or 0
                c7d = coin.get('price_change_percentage_7d_in_currency', 0) or 0
                glow = "#00FF00" if c24 >= 0 else "#FF4B4B"
                with cols[i % 4]:
                    st.markdown(f"""
                    <div class="crypto-card" style="border: 2px solid {glow};">
                        <div class="inner-card">
                            {"<div class='hot-tag'>🔥 HOT</div>" if coin.get('id') == max_vol else ""}
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
        else: st.warning("🔄 Re-syncing Global Market Nodes...")

    with tab2:
        # [NEW UPDATED FOLDER 2: WITH ATH PRICE COLUMN]
        st.subheader("📈 Institutional Performance (ATH Recovery Tracker)")
        if data:
            formatted_data = []
            for c in data:
                c24 = c.get('price_change_percentage_24h', 0) or 0
                ath_price = c.get('ath', 0) or 0
                ath_dist = c.get('ath_change_percentage', 0) or 0
                formatted_data.append({
                    "Logo": f'<img src="{c.get("image")}" width="25">',
                    "Coin": c.get('name'),
                    "Price": f"₹{c.get('current_price', 0):,.2f}",
                    "24h %": f'<span style="color:{"#00FF00" if c24>=0 else "#FF4B4B"}; font-weight:bold;">{c24:.2f}%</span>',
                    "ATH Price": f"₹{ath_price:,.2f}",
                    "ATH Dist.": f'<span style="color:#FF4B4B;">{ath_dist:.1f}%</span>',
                    "Volume": f"₹{c.get('total_volume', 0) or 0:,}"
                })
            st.write(pd.DataFrame(formatted_data).to_html(escape=False, index=False), unsafe_allow_html=True)

    with tab3:
        st.subheader("📰 Sovereign News Broadcast")
        st.markdown(f"""
        <div style="background: rgba(227, 242, 253, 0.95); padding: 20px; border-radius: 15px; border-left: 8px solid #2196F3; border: 1px solid #BBDEFB;">
            <p style="color:#1565C0 !important; font-weight:800; margin:0;">🐦 Twitter (X) Live Signals</p>
            <p style="color:#0D47A1 !important; font-size:14px; margin-top:10px; font-weight:600;">
                🛰️ $XRT & $LAI: Recovery phase detected. Samastipur AI nodes scaling.<br>
                🛰️ $POLYGON: Institutional bridge volume surging hitting targets.
            </p>
        </div>""", unsafe_allow_html=True)
else:
    st.info("⚠️ Master Key Required. Use the Sidebar on the left (←) to unlock (SAMASTIPUR@2026).")
    
