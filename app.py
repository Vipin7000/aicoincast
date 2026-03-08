import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
import time
import feedparser
import re

# --- [1. SYSTEM CONFIG & VERIFIED MASTER IDs] ---
st.set_page_config(page_title="AiCoincast Terminal v19.8 Ultra", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

# Custom CSS for Royal Purple & High Visibility
st.markdown("""
    <style>
    .stApp { background-color: #2D1B4E; }
    .stTabs [data-baseweb="tab-list"] { background-color: #1E1035; border-radius: 10px; }
    .stTabs [data-baseweb="tab"] { color: white; }
    h1, h2, h3, h4, p { color: white !important; }
    div[data-testid="stExpander"] { background-color: #1E1035; border: 1px solid #7D52B5; }
    </style>
    """, unsafe_allow_html=True)

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

# --- [2. DATA FETCH & UI] ---
data = fetch_pro_data()

# [SUDHAR 1: DYNAMIC TICKER]
if data:
    ticker_text = " | ".join([f"{c['symbol'].upper()}: ₹{c['current_price']:,.2f} ({c['price_change_percentage_24h']:.1f}%)" for c in data[:8]])
    ticker_html = f"""
    <div style="background: #1E1035; padding: 12px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #7D52B5;">
        <marquee behavior="scroll" direction="left" style="color: #00FF00; font-family: monospace; font-size: 18px; font-weight: bold;">
            🚀 {ticker_text}
        </marquee>
    </div>"""
    st.markdown(ticker_html, unsafe_allow_html=True)

st.title("🛰️ AiCoincast Terminal v19.8 (Sovereign Pro)")

with st.sidebar:
    st.header("🔐 Secure Vault")
    m_key = st.text_input("Master Key", type="password")
    api_key_raw = st.text_input("Gemini API Key", type="password")
    api_key = re.sub(r'[^a-zA-Z0-9_-]', '', api_key_raw.strip())

if m_key == MASTER_KEY:
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Market Sentinel", "📈 Performance Pro", "📰 Master Broadcast", "⚖️ Risk Calc"])

    with tab1:
        st.subheader("Live Market Monitor (Light Blue Theme)")
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
                                <h4 style="margin:0; color:#0D47A1;">₹{p:,.2f}</h4>
                                <p style="margin:0; font-size:12px; color:{'#008000' if c >=0 else '#D32F2F'};">{'▲' if c>=0 else '▼'} {abs(c):.2f}%</p>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)
        else: st.warning("Connecting to Global Market Nodes...")

    with tab2:
        # [SUDHAR 2: PRO TABLE WITH VOLUME & ATH DISTANCE]
        st.subheader("📈 Live Market Cap & Advanced Metrics")
        if data:
            formatted_data = []
            for c in data:
                c24 = c.get('price_change_percentage_24h', 0) or 0
                ath_dist = c.get('ath_change_percentage', 0) or 0
                color = "green" if c24 >= 0 else "red"
                
                formatted_data.append({
                    "Logo": f'<img src="{c.get("image")}" width="25">',
                    "Coin": c.get('name'),
                    "Price": f"₹{c.get('current_price', 0):,.2f}",
                    "24h %": f'<span style="color:{color}; font-weight:bold;">{c24:.2f}%</span>',
                    "Volume (24h)": f"₹{c.get('total_volume', 0):,}",
                    "ATH Dist.": f'<span style="color:red;">{ath_dist:.1f}%</span>'
                })
            df = pd.DataFrame(formatted_data)
            # Render HTML for Professional Look
            st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)

    with tab3:
        st.subheader("📰 Sovereign News Broadcast")
        # News UI
        st.markdown("""
        <div style="background-color:#E3F2FD; padding:20px; border-radius:12px; border-left: 6px solid #2196F3; border: 1px solid #BBDEFB;">
            <h4 style="color:#1565C0; margin:0;">🐦 Twitter (X) Live Signals</h4>
            <p style="color:#0D47A1; font-size:15px; margin-top:10px;">
                <b>$XRT & $LAI:</b> Recovery detected. Whales are accumulating.<br>
                <b>$POLYGON:</b> Bridge volume surging.
            </p>
        </div>""", unsafe_allow_html=True)
        st.divider()
        try:
            feed = feedparser.parse("https://cointelegraph.com/rss/tag/bitcoin")
            for entry in feed.entries[:3]: st.markdown(f"🔹 <span style='color:white;'>[{entry.title}]({entry.link})</span>", unsafe_allow_html=True)
        except: st.warning("RSS Feed Pending...")

    with tab4:
        st.subheader("Risk & Profit Calculator")
        entry = st.number_input("Entry Price", value=1.0)
        target = st.number_input("Target Price", value=1.5)
        if st.button("Calculate"):
            st.success(f"Potential Return: {((target/entry)-1)*100:.2f}% ✅")

else: st.info("Sovereign Standby. Enter Master Key (SAMASTIPUR@2026) to Unlock.")
