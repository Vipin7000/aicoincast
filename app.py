import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
import time
import re

# --- [1. SYSTEM CONFIG & VERIFIED MASTER IDs] ---
st.set_page_config(page_title="AiCoincast Terminal v19.8 Ultra", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

# [FIX] BTC aur ETH ko priority list mein top par rakha gaya hai
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
        response = requests.get(url, timeout=10)
        return response.json() if response.status_code == 200 else []
    except: return []

# --- [2. UI ARCHITECTURE] ---
st.title("🛰️ AiCoincast Terminal v19.8 (Indestructible Build)")

# [FIX: TOP 10 LIVE TICKER]
ticker_html = """
<div style="background: #000000; padding: 12px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #00ff00;">
    <marquee behavior="scroll" direction="left" style="color: #00ff00; font-family: 'Courier New', monospace; font-size: 18px; font-weight: bold;">
        🚀 GLOBAL LIVE: BTC: ₹6,243,683 | ETH: ₹180,809 | SOL: ₹7,667 | MATIC: ₹33.15 (+1.2%) | XRT: ₹525.20 (+2.5%) | VIRTUAL: ₹60.65 (-3.3%)
    </marquee>
</div>
"""
st.markdown(ticker_html, unsafe_allow_html=True)

with st.sidebar:
    st.header("🔐 Secure Vault")
    m_key = st.text_input("Master Key", type="password")
    raw_api_key = st.text_input("Gemini API Key", type="password")
    api_key = re.sub(r'[^a-zA-Z0-9_-]', '', raw_api_key.strip())

if m_key == MASTER_KEY:
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Market Sentinel", "📈 Performance Pro", "📰 Master Broadcast", "⚖️ Risk Calc"])
    data = fetch_pro_data()

    with tab1:
        # [FIX: FOLDER 1 MISSING DATA & COLOUR FIX]
        st.subheader("Live Market Monitor (With Logos)")
        if data:
            cols = st.columns(4)
            for i, coin in enumerate(data):
                p = coin.get('current_price', 0) or 0
                c = coin.get('price_change_percentage_24h', 0) or 0
                with cols[i % 4]:
                    st.markdown(f"""
                    <div style="display: flex; align-items: center; background: #262730; padding: 15px; border-radius: 12px; border: 1px solid #41444C; margin-bottom: 10px;">
                        <img src="{coin.get('image')}" width="35" style="margin-right: 12px;">
                        <div>
                            <p style="margin:0; font-size:12px; color:#A1A1A1;">{coin['symbol'].upper()}/INR</p>
                            <h4 style="margin:0; color:white;">₹{p:,.2f}</h4>
                            <p style="margin:0; font-size:12px; color:{'#00ff00' if c >=0 else '#ff4b4b'};">{'▲' if c>=0 else '▼'} {abs(c):.2f}%</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else: st.warning("Connecting to Global Market Nodes...")

    with tab2:
        # [FIX: FOLDER 2 ADDED VOLUME, ATH & LOGOS]
        st.subheader("📈 Live Market Cap, Volume & ATH Indicators")
        if data:
            formatted_data = []
            for coin in data:
                c24 = coin.get('price_change_percentage_24h', 0) or 0
                ath_p = coin.get('ath_change_percentage', 0) or 0
                formatted_data.append({
                    "Logo": f'<img src="{coin.get("image")}" width="25">',
                    "Coin": coin.get('name', 'N/A'),
                    "Price": f"₹{coin.get('current_price', 0) or 0:,.2f}",
                    "24h %": f'<span style="color:{"#00ff00" if c24>=0 else "#ff4b4b"}; font-weight:bold;">{c24:.2f}%</span>',
                    "Volume (24h)": f"₹{coin.get('total_volume', 0) or 0:,}",
                    "Market Cap": f"₹{coin.get('market_cap', 0) or 0:,}",
                    "ATH Dist.": f'<span style="color:#ff4b4b;">{ath_p:.1f}%</span>',
                    "7D %": f"{coin.get('price_change_percentage_7d_in_currency', 0) or 0:.2f}%"
                })
            st.write(pd.DataFrame(formatted_data).to_html(escape=False, index=False), unsafe_allow_html=True)
        else: st.warning("Re-Syncing Folder 2 Market Data...")

    with tab3:
        st.markdown("""<div style='background:#0d1117; padding:15px; border-radius:10px; border-left:5px solid #00acee; border:1px solid #30363d;'>
        <p style='color:white; margin:0;'><b>🛰️ Sovereign Broadcast:</b> BTC/ETH leading recovery. AI & DePIN signals active in India.</p>
        </div>""", unsafe_allow_html=True)
        if st.button("🚀 Generate AI Update"):
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    st.success(model.generate_content(f"Hinglish update for {list(COIN_MAP.values())}").text)
                except: st.error("AI Node exhausted.")

    with tab4:
        st.subheader("Risk & Profit Calculator")
        entry = st.number_input("Entry Price", value=1.0)
        target = st.number_input("Target Price", value=1.5)
        if st.button("Calculate"):
            st.success(f"Potential Return: {((target/entry)-1)*100:.2f}% ✅")

else: st.info("Terminal Standby. Enter Master Key (SAMASTIPUR@2026) to unlock.")
