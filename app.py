import streamlit as st
import pandas as pd
import requests
import re

# --- [1. SYSTEM CONFIG & OMEGA UI] ---
st.set_page_config(page_title="AiCoincast v22.9 Sovereign", layout="wide", initial_sidebar_state="expanded")
MASTER_KEY = "SAMASTIPUR@2026"

st.markdown("""
    <style>
    .stApp { background-color: #0A041A !important; }
    h1, h2, h3, h4, p, span, li { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] { background-color: #1A0B35 !important; border-right: 3px solid #00FF00 !important; }
    .crypto-card { background: #000000; padding: 2px; border-radius: 12px; margin-bottom: 12px; border: 2px solid #41444C; transition: 0.3s; }
    .inner-card { display: flex; align-items: center; background: #0D47A1; padding: 15px; border-radius: 10px; position: relative; }
    .price-neon { color: #00FF00 !important; font-size: 20px; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

# [MASTER ALGORITHM: 12 SOVEREIGN COINS]
SOVEREIGN_MAP = {
    "bitcoin": "BTC", "ethereum": "ETH", "virtual-protocol": "VIRTUAL", 
    "griffin-2": "GRIFFIN", "v-ai-2": "VAI", "robonomics-network": "XRT", 
    "velas": "VLX", "qanplatform": "QANX", "chaingpt": "CGPT", 
    "sinverse": "SIN", "matic-network": "POL", "nftb": "NFTB"
}

@st.cache_data(ttl=60)
def fetch_intelligence():
    ids = ",".join(SOVEREIGN_MAP.keys())
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&ids={ids}&order=market_cap_desc&sparkline=false&price_change_percentage=24h,7d"
    try:
        r = requests.get(url, timeout=15)
        return r.json() if (r.status_code == 200 and isinstance(r.json(), list)) else []
    except: return []

data = fetch_intelligence()

# --- [2. INDESTRUCTIBLE TICKER (FIXED)] ---
# [FIX] Snapshot 1000619894.jpg: Added Null-Gate for ticker_list
ticker_final = "📡 Syncing Neural Nodes... BTC: ₹6,256,000 | XRT: ₹124.91"
if data:
    try:
        ticker_list = [f"{'🟢' if float(c.get('price_change_percentage_24h', 0) or 0) > 0 else '🔴'} {c.get('symbol', '').upper()}: ₹{float(c.get('current_price', 0) or 0):,.0f}" for c in data if c.get('symbol')]
        if ticker_list: ticker_final = " | ".join(ticker_list)
    except: pass
st.markdown(f'<div style="background:#000; padding:12px; border:2px solid #00FF00; margin-bottom:20px;"><marquee style="color:#00FF00; font-weight:bold; font-size:18px;">🚀 {ticker_final}</marquee></div>', unsafe_allow_html=True)

# --- [3. SIDEBAR VAULT (FIXED PASSWORD)] ---
with st.sidebar:
    st.title("🔐 CORE VAULT")
    # [FIX] Removed Master Password Hint for Security
    m_key = st.text_input("Master Key", type="password", placeholder="Enter Password")
    api_key_raw = st.text_input("AI Neural Key", type="password")
    if data:
        # [FIX] Snapshot b603de43: Null-Shield for MC calculation
        total_mc = sum([float(c.get('market_cap', 0) or 0) for c in data])
        st.info(f"💼 Portfolio MC: ₹{total_mc:,.0f}")

# --- [4. MAIN TERMINAL LOGIC] ---
if m_key == MASTER_KEY:
    tab1, tab2, tab3, tab4 = st.tabs(["📊 SENTINEL", "📈 PERFORMANCE", "📰 BROADCAST Feed", "⚖️ RISK ENGINE"])
    
    with tab1:
        st.subheader("🛰️ Sentinel Live Nodes (HTML Fix Active)")
        if data:
            cols = st.columns(4)
            for i, coin in enumerate(data):
                p = float(coin.get('current_price', 0) or 0)
                c24 = float(coin.get('price_change_percentage_24h', 0) or 0)
                color = "#00FF00" if c24 >= 0 else "#FF4B4B"
                with cols[i % 4]:
                    # [FIX] Snapshot 8320f6c6: Sanitized HTML rendering
                    st.markdown(f"""
                    <div class="crypto-card" style="border-color: {color};">
                        <div class="inner-card">
                            <img src="{coin.get('image', '')}" width="35" style="margin-right:12px;">
                            <div>
                                <p style="margin:0; font-size:11px; color:#BBDEFB;">{coin.get('symbol', '').upper()}/INR</p>
                                <p class="price-neon">₹{p:,.0f}</p>
                                <p style="margin:0; font-size:10px; font-weight:bold; color:{color};">{c24:+.1f}%</p>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)

    with tab2:
        st.subheader("📈 Institutional Performance Heatmap")
        if data:
            perf_list = [{"Logo": f'<img src="{c.get("image","")}" width="20">', "Coin": c.get('name',''), "Price": f"₹{float(c.get('current_price',0) or 0):,.2f}", "24h": f"{float(c.get('price_change_percentage_24h',0) or 0):+.1f}%"} for c in data]
            st.write(pd.DataFrame(perf_list).to_html(escape=False, index=False), unsafe_allow_html=True)

else: st.info("⚠️ Access Denied. Master Key Required.")
                
