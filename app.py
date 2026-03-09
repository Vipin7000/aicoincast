import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
import re

# --- [1. SYSTEM CONFIG & NEON UI] ---
st.set_page_config(page_title="AiCoincast v22.0 Omega", layout="wide", initial_sidebar_state="expanded")
MASTER_KEY = "SAMASTIPUR@2026"

st.markdown("""
    <style>
    .stApp { background-color: #0A041A !important; }
    h1, h2, h3, h4, p, span, li { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] { background-color: #1A0B35 !important; border-right: 3px solid #00FF00 !important; }
    
    /* Sentinel Cards & Badges */
    .crypto-card { background: #000000; padding: 2px; border-radius: 12px; margin-bottom: 12px; border: 2px solid #41444C; }
    .inner-card { display: flex; align-items: center; background: #0D47A1; padding: 15px; border-radius: 10px; }
    .price-neon { color: #00FF00 !important; font-size: 20px; font-weight: 900; }
    
    /* Highlight Boxes for Performance Folder */
    .mover-box { background: rgba(0, 255, 0, 0.1); border: 1px solid #00FF00; padding: 10px; border-radius: 8px; margin-bottom: 15px; }
    .laggard-box { background: rgba(255, 0, 0, 0.1); border: 1px solid #FF4B4B; padding: 10px; border-radius: 8px; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# [MASTER ALGORITHM: 12 SOVEREIGN COINS]
SOVEREIGN_COINS = {
    "bitcoin": "BTC", "ethereum": "ETH", "virtual-protocol": "VIRTUAL", 
    "griffin-2": "GRIFFIN", "v-ai-2": "VAI", "robonomics-network": "XRT", 
    "velas": "VLX", "qanplatform": "QANX", "chaingpt": "CGPT", 
    "sinverse": "SIN", "matic-network": "POL", "nftb": "NFTB"
}

@st.cache_data(ttl=60)
def fetch_intelligence():
    ids = ",".join(SOVEREIGN_COINS.keys())
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&ids={ids}&order=market_cap_desc&sparkline=false&price_change_percentage=24h,7d"
    try:
        r = requests.get(url, timeout=15)
        return r.json() if r.status_code == 200 else []
    except: return []

data = fetch_intelligence()

# --- [2. OMNI-TICKER] ---
ticker_text = "📡 Syncing Samastipur Nodes... BTC: ₹6,256,000 | XRT: ₹124.91"
if data:
    ticker_text = " | ".join([f"{'🟢' if c.get('price_change_percentage_24h',0)>0 else '🔴'} {c['symbol'].upper()}: ₹{c['current_price']:,.0f}" for c in data])

st.markdown(f'<div style="background:#000; padding:12px; border:2px solid #00FF00; margin-bottom:20px;"><marquee style="color:#00FF00; font-weight:bold; font-size:18px;">🚀 {ticker_text}</marquee></div>', unsafe_allow_html=True)

# --- [3. SIDEBAR VAULT] ---
with st.sidebar:
    st.title("🔐 OMNI VAULT")
    m_key = st.text_input("Master Key", type="password", placeholder="SAMASTIPUR@2026")
    api_key = st.text_input("Neural Key", type="password")

# --- [4. MAIN TERMINAL LOGIC] ---
if m_key == MASTER_KEY:
    tab1, tab2, tab3, tab4 = st.tabs(["📊 SENTINEL (LIVE)", "📈 PERFORMANCE (ALPHA)", "📰 BROADCAST Feed", "⚖️ RISK ENGINE"])
    
    with tab1:
        st.subheader("🛰️ Sentinel Live Nodes")
        if data:
            cols = st.columns(4)
            for i, coin in enumerate(data):
                c24 = float(coin.get('price_change_percentage_24h', 0) or 0)
                color = "#00FF00" if c24 >= 0 else "#FF4B4B"
                with cols[i % 4]:
                    st.markdown(f"""
                    <div class="crypto-card" style="border-color: {color};">
                        <div class="inner-card">
                            <img src="{coin.get('image')}" width="35" style="margin-right:12px;">
                            <div>
                                <p style="margin:0; font-size:11px; color:#BBDEFB;">{coin['symbol'].upper()}/INR</p>
                                <p class="price-neon">₹{coin['current_price']:,.0f}</p>
                                <p style="margin:0; font-size:10px; font-weight:bold; color:{color};">{c24:+.1f}%</p>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)

    with tab2:
        # [NEW: INTEGRATED TOP MOVERS & LAGGARDS]
        st.subheader("📈 Institutional Heatmap & Movers")
        if data:
            # Algorithm: Sort for Gainers and Losers
            sorted_data = sorted(data, key=lambda x: x.get('price_change_percentage_24h', 0), reverse=True)
            
            col_gain, col_loss = st.columns(2)
            with col_gain:
                st.markdown('<div class="mover-box"><b>🔥 Top 3 Movers (24h)</b></div>', unsafe_allow_html=True)
                for c in sorted_data[:3]:
                    st.write(f"🟢 **{c['name']}**: {c['price_change_percentage_24h']:+.2f}%")
            
            with col_loss:
                st.markdown('<div class="laggard-box"><b>❄️ Top 3 Laggards (24h)</b></div>', unsafe_allow_html=True)
                for c in sorted_data[-3:]:
                    st.write(f"🔴 **{c['name']}**: {c['price_change_percentage_24h']:+.2f}%")
            
            st.divider()
            # Main Table with Logos
            perf_list = []
            for c in data:
                perf_list.append({
                    "Logo": f'<img src="{c["image"]}" width="20">',
                    "Coin": c['name'],
                    "Price": f"₹{c['current_price']:,.2f}",
                    "24h Change": f"{c['price_change_percentage_24h']:+.1f}%",
                    "7D Change": f"{c.get('price_change_percentage_7d_in_currency', 0):+.1f}%"
                })
            st.write(pd.DataFrame(perf_list).to_html(escape=False, index=False), unsafe_allow_html=True)

    with tab3:
        st.subheader("📰 Neural Broadcast (Social & RSS)")
        st.info("Twitter Alpha: $XRT & $VIRTUAL leading social volume in Bihar nodes. RSS: Institutional accumulation steady.")

else: st.info("⚠️ Master Key Required (SAMASTIPUR@2026).")
                    
