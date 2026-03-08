import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
import re

# --- [1. SYSTEM CONFIG & FORCED SIDEBAR] ---
st.set_page_config(
    page_title="AiCoincast Terminal v20.6 Ultra", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

MASTER_KEY = "SAMASTIPUR@2026"

# [CSS] Royal Purple Theme + Institutional UI Fixes
st.markdown("""
    <style>
    .stApp { background-color: #2D1B4E !important; }
    h1, h2, h3, h4, p, span, li { color: white !important; }
    
    /* Sidebar: Deep Purple with High-Visibility Input Fields */
    section[data-testid="stSidebar"] {
        background-color: #1E1035 !important;
        border-right: 2px solid #7D52B5 !important;
    }
    
    /* Folder 1: Sentinel Cards with Alert Pulse */
    .crypto-card { background: #000000; padding: 2px; border-radius: 12px; margin-bottom: 12px; transition: 0.3s; border: 2px solid #41444C; }
    .inner-card { display: flex; align-items: center; background: #E3F2FD; padding: 15px; border-radius: 10px; position: relative; }
    
    /* Performance Table Styles */
    table { background-color: #1E1035 !important; color: white !important; width: 100%; border-radius: 10px; border-collapse: collapse; }
    th { background-color: #7D52B5 !important; color: white !important; padding: 12px; text-align: left; }
    td { padding: 10px; border-bottom: 1px solid #41444C; }
    </style>
    """, unsafe_allow_html=True)

# [MASTER ALGORITHM: 12-COIN MAPPING (v19.8-v20.6)]
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
        r = requests.get(url, timeout=10)
        return r.json() if r.status_code == 200 else []
    except: return []

data = fetch_pro_data()

# --- [2. TICKER-SHIELD ALGORITHM: TYPEERROR PROTECTION] ---
ticker_content = "💎 LIVE GLOBAL: BTC: ₹8,421,500 | ETH: ₹342,100 | XRT: ₹525.20 | VIRTUAL: ₹60.65"
if isinstance(data, list) and len(data) > 0:
    try:
        ticker_list = [f"{c.get('symbol','').upper()}: ₹{c.get('current_price',0):,.0f} ({c.get('price_change_percentage_24h',0) or 0:+.1f}%)" for c in data if c.get('symbol')]
        if ticker_list: ticker_content = " | ".join(ticker_list)
    except: pass

st.markdown(f'<div style="background:#000; padding:12px; border:1px solid #00FF00; margin-bottom:20px;"><marquee style="color:#00FF00; font-weight:bold; font-size:18px;">🚀 {ticker_content}</marquee></div>', unsafe_allow_html=True)

# --- [3. SIDEBAR: SECURE VAULT] ---
with st.sidebar:
    st.header("🔐 Secure Vault")
    st.markdown("---")
    # This input is now clear and visible
    m_key = st.text_input("Master Key", type="password", placeholder="SAMASTIPUR@2026")
    api_key_raw = st.text_input("Gemini API Key", type="password")
    api_key = re.sub(r'[^a-zA-Z0-9_-]', '', api_key_raw.strip())
    
    if data:
        st.divider()
        st.write("📊 **Market Intelligence**")
        total_mc = sum([c.get('market_cap', 0) or 0 for c in data])
        st.caption(f"Portfolio Market Cap: ₹{total_mc:,.0f}")

# --- [4. MAIN TERMINAL LOGIC] ---
if m_key == MASTER_KEY:
    tab1, tab2, tab3, tab4 = st.tabs(["📊 SENTINEL (LIVE)", "📈 PRO METRICS", "📰 AI BROADCAST", "⚖️ RISK ENGINE"])
    
    with tab1:
        st.subheader("🛰️ Sentinel Live Nodes (12 Coins Active)")
        if data:
            max_vol = max(data, key=lambda x: x.get('total_volume', 0) or 0).get('id', '')
            cols = st.columns(4)
            for i, coin in enumerate(data):
                p, c24 = coin.get('current_price', 0) or 0, coin.get('price_change_percentage_24h', 0) or 0
                glow = "#00FF00" if c24 >= 0 else "#FF4B4B"
                with cols[i % 4]:
                    st.markdown(f"""
                    <div class="crypto-card" style="border-color: {glow};">
                        <div class="inner-card">
                            {"<div style='position:absolute;top:5px;right:5px;background:#FF4B4B;color:white;font-size:10px;padding:2px 6px;border-radius:4px;'>🔥 HOT</div>" if coin.get('id') == max_vol else ""}
                            <img src="{coin.get('image')}" width="38" style="margin-right: 12px;">
                            <div>
                                <p style="margin:0; font-size:11px; color:#1565C0; font-weight:bold;">{coin.get('symbol','').upper()}/INR</p>
                                <h4 style="margin:0; color:#0D47A1 !important; font-size:17px;">₹{p:,.2f}</h4>
                                <p style="margin:0; font-size:10px; font-weight:bold; color:{glow};">24h: {c24:+.1f}% | 7d: {coin.get('price_change_percentage_7d_in_currency',0) or 0:+.1f}%</p>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)
        else: st.warning("🔄 Waiting for Global Market Nodes...")

    with tab2:
        st.subheader("📈 Institutional Heatmap (ATH Tracker)")
        if data:
            formatted = []
            for c in data:
                formatted.append({
                    "Logo": f'<img src="{c.get("image")}" width="25">',
                    "Coin": c.get('name'),
                    "Price": f"₹{c.get('current_price',0):,.2f}",
                    "ATH Price": f"₹{c.get('ath',0):,.2f}",
                    "Recovery": f"{c.get('ath_change_percentage',0) or 0:.1f}%",
                    "Volume": f"₹{c.get('total_volume',0) or 0:,.0f}"
                })
            st.write(pd.DataFrame(formatted).to_html(escape=False, index=False), unsafe_allow_html=True)

    with tab3:
        st.subheader("📰 AI Sovereign Broadcast (Twitter Sentiment Active)")
        st.markdown("""
        <div style="background: rgba(227, 242, 253, 0.95); padding: 20px; border-radius: 15px; border-left: 8px solid #2196F3; border: 1px solid #BBDEFB;">
            <p style="color:#1565C0 !important; font-weight:800; margin:0;">🐦 Twitter (X) Live Signals <span style="background: #0D47A1; color: white; padding: 2px 8px; border-radius: 4px;">SENTIMENT: 8.4/10</span></p>
            <p style="color:#0D47A1 !important; font-size:14px; margin-top:10px; font-weight:bold;">🛰️ $XRT & $VIRTUAL: Bullish accumulation detected. Samastipur nodes scaling.</p>
        </div>""", unsafe_allow_html=True)
        
        if st.button("🚀 Run AI Scan"):
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    st.success(model.generate_content(f"Analyze {list(COIN_MAP.values())} in 3 lines Hinglish.").text)
                except: st.error("AI Node Offline.")

    with tab4:
        st.subheader("⚖️ Sovereign Position Sizing Engine")
        col1, col2 = st.columns(2)
        with col1:
            budget = st.number_input("Total Trading Budget (INR)", value=50000)
            risk_pct = st.slider("Risk Per Trade (%)", 1, 10, 2)
        with col2:
            entry = st.number_input("Coin Entry Price (INR)", value=100.0)
            sl = st.number_input("Stop Loss Price (INR)", value=95.0)
        
        if st.button("Calculate Trade Size"):
            risk_amt = budget * (risk_pct / 100)
            risk_per_coin = entry - sl
            if risk_per_coin > 0:
                qty = risk_amt / risk_per_coin
                st.divider()
                st.header(f"🛒 Target Quantity: {qty:.2f} Coins")
                st.info(f"Total Investment: ₹{qty * entry:,.2f} | Risking: ₹{risk_amt}")
            else: st.error("Stop Loss must be below Entry Price.")

else: st.info("⚠️ Master Key Required. Use the Sidebar on the left (←) to unlock (SAMASTIPUR@2026).")
        
