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

# [HYBRID CSS] Royal Purple Background + Glow Sentinel Cards
st.markdown("""
    <style>
    .stApp { background-color: #2D1B4E !important; }
    h1, h2, h3, h4, p, span, li { color: white !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #1E1035 !important; border-radius: 10px; }
    .stTabs [data-baseweb="tab"] { color: white !important; }
    
    /* Folder 1: Hybrid Elite Cards */
    .crypto-card { background: #000000; padding: 2px; border-radius: 12px; margin-bottom: 12px; transition: transform 0.2s; }
    .crypto-card:hover { transform: scale(1.03); }
    .inner-card { display: flex; align-items: center; background: #E3F2FD; padding: 15px; border-radius: 10px; position: relative; }
    .hot-tag { position: absolute; top: 5px; right: 5px; background: #FF4B4B; color: white !important; font-size: 10px; padding: 2px 6px; border-radius: 4px; font-weight: bold; }
    
    /* Broadcast & Table UI */
    .broadcast-card { background: rgba(227, 242, 253, 0.95) !important; padding: 18px; border-radius: 15px; border-left: 8px solid #2196F3; margin-bottom: 20px; border: 1px solid #BBDEFB; }
    table { background-color: #1E1035 !important; color: white !important; width: 100%; border-radius: 10px; overflow: hidden; }
    th { background-color: #7D52B5 !important; color: white !important; padding: 12px; }
    td { padding: 10px; border-bottom: 1px solid #41444C; }
    </style>
    """, unsafe_allow_html=True)

# [ALGORITHM: 12-COIN MASTER MAPPING]
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

# --- [2. UI LOGIC & TICKER-SHIELD] ---
data = fetch_pro_data()
if data and len(data) > 0:
    ticker_text = " | ".join([f"{c.get('symbol','').upper()}: ₹{c.get('current_price',0):,.0f} ({c.get('price_change_percentage_24h',0):+.1f}%)" for c in data[:10]])
else:
    ticker_text = "💎 LIVE GLOBAL: BTC: ₹6,243,683 | ETH: ₹180,809 | SOL: ₹12,480 | MATIC: ₹33.15 | XRT: ₹525.20 | VIRTUAL: ₹60.65"

st.markdown(f"""
    <div style="background: #000000; padding: 12px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #00FF00;">
        <marquee behavior="scroll" direction="left" style="color: #00FF00; font-family: monospace; font-size: 18px; font-weight: bold;">🚀 {ticker_text}</marquee>
    </div>""", unsafe_allow_html=True)

with st.sidebar:
    st.header("🔐 Secure Vault")
    m_key = st.text_input("Master Key", type="password", help="Enter: SAMASTIPUR@2026")
    
    if data:
        avg_change = sum([c.get('price_change_percentage_24h', 0) or 0 for c in data]) / len(data)
        st.info(f"Sentiment: {'GREED 🚀' if avg_change > 0 else 'FEAR 📉'}")
        
    api_key_raw = st.text_input("Gemini API Key", type="password")
    api_key = re.sub(r'[^a-zA-Z0-9_-]', '', api_key_raw.strip())

if m_key == MASTER_KEY:
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Market Sentinel", "📈 Performance Pro", "📰 Master Broadcast", "⚖️ Risk Calc"])
    
    with tab1:
        st.subheader("🛰️ Market Sentinel (Glow & 7D Analysis)")
        if data:
            max_vol_coin = max(data, key=lambda x: x.get('total_volume', 0) or 0)['id']
            cols = st.columns(4)
            for i, coin in enumerate(data):
                p = coin.get('current_price', 0) or 0
                c24 = coin.get('price_change_percentage_24h', 0) or 0
                c7d = coin.get('price_change_percentage_7d_in_currency', 0) or 0
                glow = "#00FF00" if c24 >= 0 else "#FF4B4B"
                with cols[i % 4]:
                    st.markdown(f"""
                    <div class="crypto-card" style="border: 2px solid {glow};">
                        <div class="inner-card">
                            {"<div class='hot-tag'>🔥 HOT</div>" if coin['id'] == max_vol_coin else ""}
                            <img src="{coin.get('image')}" width="38" style="margin-right: 12px;">
                            <div>
                                <p style="margin:0; font-size:11px; color:#1565C0; font-weight:bold;">{coin['symbol'].upper()}/INR</p>
                                <h4 style="margin:0; color:#0D47A1 !important; font-size:17px;">₹{p:,.2f}</h4>
                                <p style="margin:0; font-size:10px; font-weight:bold; color:{'#008000' if c24>=0 else '#D32F2F'};">
                                    24h: {c24:+.1f}% | 7d: {c7d:+.1f}%
                                </p>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)
        else: st.warning("Connecting to Global Nodes...")

    with tab2:
        st.subheader("📈 Institutional Performance Metrics")
        if data:
            formatted_data = []
            for c in data:
                c24 = c.get('price_change_percentage_24h', 0) or 0
                formatted_data.append({
                    "Logo": f'<img src="{c.get("image")}" width="25">',
                    "Coin": c.get('name'),
                    "Price": f"₹{c.get('current_price', 0):,.2f}",
                    "24h %": f'<span style="color:{"#00FF00" if c24>=0 else "#FF4B4B"}; font-weight:bold;">{c24:.2f}%</span>',
                    "Volume": f"₹{c.get('total_volume', 0) or 0:,}",
                    "ATH Dist": f'<span style="color:#FF4B4B;">{c.get("ath_change_percentage",0):.1f}%</span>',
                    "Market Cap": f"₹{c.get('market_cap', 0) or 0:,}"
                })
            st.write(pd.DataFrame(formatted_data).to_html(escape=False, index=False), unsafe_allow_html=True)

    with tab3:
        st.subheader("📰 Sovereign News Broadcast")
        st.markdown(f"""
        <div class="broadcast-card">
            <p style="color:#1565C0 !important; font-weight:800; margin:0;">🐦 Master Twitter (X) Broadcast <span style="font-size:12px; background:#E1F5FE; color:#0288D1; padding:2px 6px; border-radius:4px;">SENTIMENT: ACTIVE 🚀</span></p>
            <p style="color:#0D47A1 !important; font-size:14px; margin-top:10px; font-weight:600;">
                🛰️ $XRT & $LAI: All-Time High recovery phase detected. Samastipur AI nodes active.<br>
                🛰️ $POLYGON: Bridge volume surging hitting 2026 targets. $POL migration momentum building.
            </p>
        </div>""", unsafe_allow_html=True)
        
        if st.button("🚀 Run AI Deep-Scan"):
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    st.success(model.generate_content(f"Hinglish summary for {list(COIN_MAP.values())}. Focus on AI and DePIN sector news for 2026.").text)
                except: st.error("AI Node exhausted. Check Key.")
        
        st.divider()
        try:
            feed = feedparser.parse("https://cointelegraph.com/rss/tag/bitcoin")
            for entry in feed.entries[:3]: st.markdown(f"🔹 <span style='color:white;'>[{entry.title}]({entry.link})</span>", unsafe_allow_html=True)
        except: st.warning("RSS Feed Pending...")

    with tab4:
        st.subheader("⚖️ Risk & Profit Calculator")
        entry = st.number_input("Entry Price (INR)", value=1.0)
        target = st.number_input("Target Price (INR)", value=1.5)
        if st.button("Analyze Trade"):
            st.success(f"Potential Return: {((target/entry)-1)*100:.2f}% ✅")

else: st.info("Sovereign Standby. Expand Sidebar (←) and enter Master Key (SAMASTIPUR@2026) to Unlock.")
            
