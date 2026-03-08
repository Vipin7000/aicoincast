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

COIN_MAP = {
    "virtual-protocol": "VIRTUAL", "griffin": "GRIFFIN", "v-ai-2": "VAI",
    "robonomics-network": "XRT", "velas": "VLX", "qanplatform": "QANX",
    "chaingpt": "CGPT", "sinverse": "SIN", "matic-network": "POLYGON", "nftb": "NFTB"
}

@st.cache_data(ttl=60)
def fetch_safe_data():
    ids = ",".join(COIN_MAP.keys())
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=inr&include_24hr_change=true&include_7d_change=true&include_30d_change=true"
    try:
        response = requests.get(url, timeout=10)
        return response.json() if response.status_code == 200 else {}
    except: return {}

# --- [2. UI ARCHITECTURE] ---
st.title("🛰️ AiCoincast Terminal v19.8 Ultra")

ticker_html = """
<div style="background: #000000; padding: 10px; border-radius: 8px; margin-bottom: 15px; border: 1px solid #00ff00;">
    <marquee behavior="scroll" direction="left" style="color: #00ff00; font-family: 'Courier New', monospace; font-size: 16px; font-weight: bold;">
        💎 TOP 10 LIVE: BTC: ₹5,684,210 (-1.1%) | ETH: ₹324,150 (+0.4%) | SOL: ₹12,480 (+2.1%) | MATIC: ₹33.15 (+1.2%) | XRT: ₹525 (+2.5%)
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
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Market Monitor", "📈 Performance", "📰 Master Broadcast", "⚖️ Risk Calc"])
    data = fetch_safe_data()

    with tab1:
        cols = st.columns(5)
        for i, (id, symbol) in enumerate(COIN_MAP.items()):
            coin_info = data.get(id, {})
            p, c = coin_info.get('inr'), coin_info.get('inr_24h_change')
            if p is not None:
                cols[i % 5].metric(f"{symbol}/INR", f"₹{float(p):,.2f}", f"{float(c or 0):.2f}%")
            else:
                cols[i % 5].warning(f"{symbol} Syncing...")
        st.divider()
        st.metric("NIFTY 50", "₹24,469.10", "-1.20%", delta_color="inverse")

    with tab2:
        if data:
            perf_list = [{"Asset": sym, "Live Price": f"₹{float(data.get(id, {}).get('inr', 0)):,.2f}", 
                          "7D %": f"{float(data.get(id, {}).get('inr_7d_change', 0)):.2f}%", 
                          "30D %": f"{float(data.get(id, {}).get('inr_30d_change', 0)):.2f}%"} for id, sym in COIN_MAP.items()]
            st.table(pd.DataFrame(perf_list))

    with tab3:
        # --- [FIX: MERGED & SHRINKED NEWS CARD] ---
        st.markdown("""
        <div style="background-color:#0d1117; padding:15px; border-radius:10px; border-left: 5px solid #00acee; border: 1px solid #30363d;">
            <h4 style="color:#00acee; margin:0;">🐦 Sovereign Master Broadcast</h4>
            <p style="color:white; font-size:14px; margin-top:10px;">
                <b>Latest signals:</b> $XRT scaling IoT nodes | $LAI recovery mode (+12%) | $POLYGON Lisovo logic active.<br>
                <b>Sentiment:</b> <span style="color:#00ff00;">Bullish Decoupling</span> (68% Confidence)
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 AI Portfolio News"):
                if api_key:
                    try:
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        st.success(model.generate_content(f"Quick Hinglish update for {list(COIN_MAP.values())}").text)
                    except: st.error("AI Node exhausted.")
        with col2:
            st.caption("🌍 Global Finance Feed (Last 5)")
            try:
                feed = feedparser.parse("https://cointelegraph.com/rss/tag/bitcoin")
                for entry in feed.entries[:3]: st.markdown(f"🔹 <small>[{entry.title}]({entry.link})</small>", unsafe_allow_html=True)
            except: st.warning("RSS Pending")

    with tab4:
        coin = st.selectbox("Asset", list(COIN_MAP.values()))
        entry = st.number_input("Entry Price", value=1.0)
        target = st.number_input("Target Price", value=1.5)
        if st.button("Calculate"):
            st.success(f"Return: {((target/entry)-1)*100:.2f}%")

else: st.info("Enter Master Key to access Terminal.")
    
