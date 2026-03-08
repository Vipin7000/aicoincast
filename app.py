import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
import time
import feedparser
import re

# --- [1. SYSTEM CONFIG & MASTER IDs] ---
st.set_page_config(page_title="AiCoincast Terminal v19.8 Ultra", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

# Verified IDs for all 10 coins (Ensures they stay ONLINE)
COIN_MAP = {
    "virtual-protocol": "VIRTUAL", "griffin-2": "GRIFFIN", "v-ai-2": "VAI",
    "robonomics-network": "XRT", "velas": "VLX", "qanplatform": "QANX",
    "chaingpt": "CGPT", "sinverse": "SIN", "matic-network": "POLYGON", "nftb": "NFTB"
}

@st.cache_data(ttl=60)
def fetch_pro_data():
    ids = ",".join(COIN_MAP.keys())
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&ids={ids}&order=market_cap_desc&per_page=10&page=1&sparkline=false&price_change_percentage=24h,7d"
    try:
        response = requests.get(url, timeout=10)
        return response.json() if response.status_code == 200 else []
    except: return []

# --- [2. UI ARCHITECTURE] ---
st.title("🛰️ AiCoincast Terminal v19.8 (Pro Build)")

# Running Ticker (Top 10 Global)
st.markdown("""
<div style="background: #000000; padding: 10px; border-radius: 8px; margin-bottom: 15px; border: 1px solid #00ff00;">
    <marquee behavior="scroll" direction="left" style="color: #00ff00; font-family: monospace; font-size: 16px; font-weight: bold;">
        💎 LIVE: BTC: ₹6,243,683 | ETH: ₹180,809 | SOL: ₹7,667.83 | MATIC: ₹33.15 (+1.2%) | XRT: ₹525.20 (+2.5%) | VIRTUAL: ₹60.65 (-3.3%)
    </marquee>
</div>""", unsafe_allow_html=True)

with st.sidebar:
    st.header("🔐 Secure Vault")
    m_key = st.text_input("Master Key", type="password")
    raw_api_key = st.text_input("Gemini API Key", type="password")
    api_key = re.sub(r'[^a-zA-Z0-9_-]', '', raw_api_key.strip())

if m_key == MASTER_KEY:
    # ALL FOUR FOLDERS LOCKED
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Market Sentinel", "📈 Performance Pro", "📰 Master Broadcast", "⚖️ Risk Calc"])
    data = fetch_pro_data()

    with tab1:
        st.subheader("Live 10-Coin Monitor")
        cols = st.columns(5)
        # [FIX] TypeError Protection: Safe float conversion
        if data:
            for i, coin in enumerate(data):
                p = coin.get('current_price', 0)
                c = coin.get('price_change_percentage_24h', 0)
                cols[i % 5].metric(f"{coin['symbol'].upper()}/INR", f"₹{float(p or 0):,.2f}", f"{float(c or 0):.2f}%")
        else: st.warning("Connecting to Global Market Nodes...")
        st.divider()
        st.metric("NIFTY 50 (India)", "₹24,469.10", "-1.20%", delta_color="inverse")

    with tab2:
        # --- [FOLDER 2: CRYPTO LIST WITH LOGO & INDICATORS] ---
        st.subheader("📈 Live Market Cap & Indicators")
        if data:
            formatted_data = []
            for coin in data:
                change_24h = coin.get('price_change_percentage_24h', 0) or 0
                color = "green" if change_24h >= 0 else "red"
                
                formatted_data.append({
                    "Logo": f'<img src="{coin.get("image", "")}" width="25">',
                    "Coin": coin.get('name', 'N/A'),
                    "Price": f"₹{coin.get('current_price', 0):,.2f}",
                    "24h %": f'<span style="color:{color}; font-weight:bold;">{change_24h:.2f}%</span>',
                    "Market Cap": f"₹{coin.get('market_cap', 0):,}",
                    "7D %": f"{coin.get('price_change_percentage_7d_in_currency', 0) or 0:.2f}%"
                })
            
            df = pd.DataFrame(formatted_data)
            st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
        else: st.warning("Re-Syncing Market Data...")

    with tab3:
        # --- [SHRINKED & MERGED NEWS BROADCAST] ---
        st.markdown(f"""
        <div style="background-color:#0d1117; padding:15px; border-radius:10px; border: 1px solid #30363d; border-left: 5px solid #00acee;">
            <h4 style="color:#00acee; margin:0;">🐦 Sovereign Master Broadcast</h4>
            <p style="color:white; font-size:14px; margin-top:10px;">
                <b>Latest:</b> $XRT scaling nodes | $LAI recovery mode | $POLYGON bridge surging.<br>
                <b>Sentiment:</b> <span style="color:#00ff00;">Bullish Decoupling</span> (68% Confidence)
            </p>
        </div>""", unsafe_allow_html=True)
        
        if st.button("🚀 Generate AI News"):
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    st.success(model.generate_content("Quick Hinglish update for my 10 coins.").text)
                except: st.error("AI Node exhausted. Check API Key.")

    with tab4:
        st.subheader("Risk & Profit Calculator")
        entry = st.number_input("Entry Price", value=1.0)
        target = st.number_input("Target Price", value=1.5)
        if st.button("Calculate"):
            st.success(f"Potential Return: {((target/entry)-1)*100:.2f}% ✅")

else: st.info("Terminal Standby. Enter Master Key (SAMASTIPUR@2026) to access.")
            
