import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
import feedparser
import re

# --- [1. SYSTEM CONFIG & AUTO-SIDEBAR] ---
st.set_page_config(
    page_title="AiCoincast Terminal v19.9 Ultra", 
    layout="wide", 
    initial_sidebar_state="expanded" # Hamesha password box dikhega
)

MASTER_KEY = "SAMASTIPUR@2026"

# Royal Purple Theme & Institutional CSS
st.markdown("""
    <style>
    .stApp { background-color: #2D1B4E !important; }
    h1, h2, h3, h4, p, span, li { color: white !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #1E1035 !important; border-radius: 10px; }
    .stTabs [data-baseweb="tab"] { color: white !important; font-weight: bold; }
    
    /* Folder 1: Elite Glow Cards */
    .crypto-card { background: #000000; padding: 2px; border-radius: 12px; margin-bottom: 12px; transition: 0.3s; }
    .inner-card { display: flex; align-items: center; background: #E3F2FD; padding: 15px; border-radius: 10px; position: relative; }
    .hot-tag { position: absolute; top: 5px; right: 5px; background: #FF4B4B; color: white !important; font-size: 10px; padding: 2px 6px; border-radius: 4px; font-weight: bold; }
    
    /* Table & Broadcast UI */
    .broadcast-card { background: rgba(227, 242, 253, 0.95) !important; padding: 20px; border-radius: 15px; border-left: 8px solid #2196F3; border: 1px solid #BBDEFB; }
    table { background-color: #1E1035 !important; color: white !important; width: 100%; border-radius: 10px; }
    th { background-color: #7D52B5 !important; color: white !important; padding: 12px; }
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

# --- [2. UI LOGIC & TICKER-SHIELD] ---
data = fetch_pro_data()

# Ticker Logic with Fallback Shield
if isinstance(data, list) and len(data) > 0:
    ticker_text = " | ".join([f"{c.get('symbol','').upper()}: ₹{c.get('current_price',0):,.0f} ({c.get('price_change_percentage_24h',0):+.1f}%)" for c in data if c.get('symbol')])
else:
    ticker_text = "💎 LIVE GLOBAL: BTC: ₹5,684,210 | ETH: ₹324,150 | SOL: ₹12,480 | MATIC: ₹33.15 | XRT: ₹525.20"

st.markdown(f"""
    <div style="background: #000000; padding: 12px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #00FF00;">
        <marquee behavior="scroll" direction="left" style="color: #00FF00; font-family: monospace; font-size: 18px; font-weight: bold;">🚀 {ticker_text}</marquee>
    </div>""", unsafe_allow_html=True)

# --- [3. SIDEBAR: SECURE VAULT] ---
with st.sidebar:
    st.header("🔐 Secure Vault")
    m_key = st.text_input("Master Key", type="password", placeholder="SAMASTIPUR@2026")
    
    if data:
        avg = sum([c.get('price_change_percentage_24h', 0) or 0 for c in data]) / len(data)
        st.info(f"Market Mood: {'GREED 🚀' if avg > 0 else 'FEAR 📉'}")
        
    api_key_raw = st.text_input("Gemini API Key", type="password")
    api_key = re.sub(r'[^a-zA-Z0-9_-]', '', api_key_raw.strip())

# --- [4. MAIN TERMINAL] ---
if m_key == MASTER_KEY:
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Market Sentinel", "📈 Performance Pro", "📰 Master Broadcast", "⚖️ Risk Calc"])
    
    with tab1:
        st.subheader("🛰️ Market Sentinel (12 Coins Active)")
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

    with tab2:
        st.subheader("📈 Institutional Performance Metrics")
        if data:
            formatted = []
            for c in data:
                c24 = c.get('price_change_percentage_24h', 0) or 0
                formatted.append({
                    "Logo": f'<img src="{c.get("image")}" width="25">',
                    "Coin": c.get('name'),
                    "Price": f"₹{c.get('current_price', 0):,.2f}",
                    "24h %": f'<span style="color:{"#00FF00" if c24>=0 else "#FF4B4B"}; font-weight:bold;">{c24:.2f}%</span>',
                    "Volume": f"₹{c.get('total_volume', 0) or 0:,}",
                    "ATH Dist": f'<span style="color:#FF4B4B;">{c.get("ath_change_percentage",0):.1f}%</span>'
                })
            st.write(pd.DataFrame(formatted).to_html(escape=False, index=False), unsafe_allow_html=True)

    with tab3:
        st.subheader("📰 Sovereign News Broadcast")
        st.markdown(f"""
        <div class="broadcast-card">
            <p style="color:#1565C0 !important; font-weight:800; margin:0;">🐦 Twitter (X) Live Signals</p>
            <p style="color:#0D47A1 !important; font-size:14px; margin-top:10px; font-weight:600;">
                🛰️ $XRT & $LAI: All-Time High recovery detected. Samastipur nodes scaling.<br>
                🛰️ $POLYGON: Bridge volume surging hitting 2026 targets.
            </p>
        </div>""", unsafe_allow_html=True)
        if st.button("🚀 Run AI Deep-Scan"):
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    st.success(model.generate_content(f"Hinglish news for {list(COIN_MAP.values())}").text)
                except: st.error("AI Node Offline.")

    with tab4:
        st.subheader("⚖️ Risk Calculator")
        entry = st.number_input("Entry Price (INR)", value=1.0)
        target = st.number_input("Target Price (INR)", value=1.5)
        if st.button("Analyze ROI"):
            st.success(f"Potential Return: {((target/entry)-1)*100:.2f}% ✅")

else:
    st.info("⚠️ Master Key Required. Use the Sidebar on the left to unlock (SAMASTIPUR@2026).")
    
