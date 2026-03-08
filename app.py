import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
import time
import re

# --- [1. SYSTEM CONFIG & VERIFIED MASTER IDs] ---
st.set_page_config(page_title="AiCoincast Terminal v19.8 Pro", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

# [FIX] BTC aur ETH ko top priority par add kiya gaya hai
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
st.title("🛰️ AiCoincast Terminal v19.8 (Pro Build)")

with st.sidebar:
    st.header("🔐 Secure Vault")
    m_key = st.text_input("Master Key", type="password")
    raw_api_key = st.text_input("Gemini API Key", type="password")
    api_key = re.sub(r'[^a-zA-Z0-9_-]', '', raw_api_key.strip())

if m_key == MASTER_KEY:
    # Charo folders locked aur visible
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Market Sentinel", "📈 Performance Pro", "📰 Master Broadcast", "⚖️ Risk Calc"])
    data = fetch_pro_data()

    with tab1:
        # --- [FOLDER 1: LOGOS ADDED TO ALL COINS] ---
        st.subheader("Live Market Monitor (With Logos)")
        if data:
            cols = st.columns(4)
            for i, coin in enumerate(data):
                p = coin.get('current_price', 0) or 0
                c = coin.get('price_change_percentage_24h', 0) or 0
                # [FIX] Logo integration in Folder 1
                with cols[i % 4]:
                    st.markdown(f"""
                    <div style="display: flex; align-items: center; background: #1e1e1e; padding: 10px; border-radius: 10px; border: 1px solid #333;">
                        <img src="{coin.get('image')}" width="30" style="margin-right: 10px;">
                        <div>
                            <p style="margin:0; font-size:12px; color:#888;">{coin['symbol'].upper()}/INR</p>
                            <h4 style="margin:0; color:white;">₹{p:,.2f}</h4>
                            <p style="margin:0; font-size:12px; color:{'#00ff00' if c >=0 else '#ff4b4b'};">{c:.2f}%</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else: st.warning("Connecting to Global Nodes...")
        st.divider()
        st.metric("NIFTY 50 (India)", "₹24,469.10", "-1.20%", delta_color="inverse")

    with tab2:
        # --- [FOLDER 2: BTC/ETH ADDED WITH PRO INDICATORS] ---
        st.subheader("📈 Live Market Cap & Volume Indicators")
        if data:
            formatted_data = []
            for coin in data:
                c24 = coin.get('price_change_percentage_24h', 0) or 0
                formatted_data.append({
                    "Logo": f'<img src="{coin.get("image")}" width="25">',
                    "Coin": coin.get('name'),
                    "Price": f"₹{coin.get('current_price', 0):,.2f}",
                    "24h %": f'<span style="color:{"green" if c24>=0 else "red"}; font-weight:bold;">{c24:.2f}%</span>',
                    "Volume (24h)": f"₹{coin.get('total_volume', 0):,}",
                    "Market Cap": f"₹{coin.get('market_cap', 0):,}",
                    "7D %": f"{coin.get('price_change_percentage_7d_in_currency', 0) or 0:.2f}%"
                })
            st.write(pd.DataFrame(formatted_data).to_html(escape=False, index=False), unsafe_allow_html=True)

    with tab3:
        # Shrinked Master News Section
        st.markdown("""<div style='background:#0d1117; padding:15px; border-radius:10px; border-left:5px solid #00acee;'>
        <p style='color:white; margin:0;'><b>Sovereign Broadcast:</b> BTC aur ETH stable hain. XRT aur LAI mein growth signals active hain.</p>
        </div>""", unsafe_allow_html=True)
        if st.button("🚀 Generate AI Update"):
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    st.success(model.generate_content("Hinglish update for BTC, ETH and AI coins.").text)
                except: st.error("AI Node exhausted.")

    with tab4:
        st.subheader("Risk & Profit Calculator")
        entry = st.number_input("Entry Price", value=1.0)
        target = st.number_input("Target Price", value=1.5)
        if st.button("Calculate"):
            st.success(f"Return: {((target/entry)-1)*100:.2f}%")

else: st.info("Terminal Standby. Enter Master Key (SAMASTIPUR@2026) to unlock.")
