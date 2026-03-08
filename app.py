import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
import re

# --- [1. SYSTEM CONFIG & FORCED SIDEBAR] ---
st.set_page_config(
    page_title="AiCoincast Terminal v20.3 Ultra", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

MASTER_KEY = "SAMASTIPUR@2026"

# [CSS] Royal Purple Theme + Glass-morphism Layout
st.markdown("""
    <style>
    .stApp { background-color: #2D1B4E !important; }
    h1, h2, h3, h4, p, span, li { color: white !important; }
    section[data-testid="stSidebar"] { background-color: #1E1035 !important; border-right: 2px solid #7D52B5 !important; }
    
    /* Folder 1: Sentinel Cards Upgrade */
    .crypto-card { background: #000000; padding: 2px; border-radius: 12px; margin-bottom: 12px; transition: 0.3s; }
    .crypto-card:hover { transform: translateY(-5px); border-color: #00FF00 !important; }
    .inner-card { display: flex; align-items: center; background: #E3F2FD; padding: 15px; border-radius: 10px; position: relative; }
    
    /* Global Table Styling */
    table { background-color: #1E1035 !important; color: white !important; width: 100%; border-radius: 10px; }
    th { background-color: #7D52B5 !important; color: white !important; padding: 12px; text-align: left; }
    td { padding: 10px; border-bottom: 1px solid #41444C; }
    </style>
    """, unsafe_allow_html=True)

# [ALGORITHM: VERIFIED 12-COIN MAPPING]
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

# --- [2. TICKER-SHIELD ALGORITHM] ---
ticker_content = "💎 LIVE GLOBAL: BTC: ₹8,421,500 | ETH: ₹342,100 | XRT: ₹525.20 | VIRTUAL: ₹60.65"
if isinstance(data, list) and len(data) > 0:
    try:
        ticker_list = [f"{c.get('symbol','').upper()}: ₹{c.get('current_price',0):,.0f} ({c.get('price_change_percentage_24h',0):+.1f}%)" for c in data if c.get('symbol')]
        ticker_content = " | ".join(ticker_list[:12])
    except: pass

st.markdown(f'<div style="background:#000; padding:12px; border:1px solid #00FF00; margin-bottom:20px;"><marquee style="color:#00FF00; font-weight:bold; font-size:18px;">🚀 {ticker_content}</marquee></div>', unsafe_allow_html=True)

# --- [3. SIDEBAR: SECURE VAULT] ---
with st.sidebar:
    st.header("🔐 Secure Vault")
    m_key = st.text_input("Master Key", type="password", placeholder="SAMASTIPUR@2026")
    api_key_raw = st.text_input("Gemini API Key", type="password")
    api_key = re.sub(r'[^a-zA-Z0-9_-]', '', api_key_raw.strip())
    
    if data:
        st.divider()
        st.write("📊 **Market Dominance**")
        total_mc = sum([c.get('market_cap', 0) for c in data])
        for c in data[:3]:
            dom = (c.get('market_cap', 0) / total_mc) * 100
            st.caption(f"{c['symbol'].upper()}: {dom:.1f}%")

# --- [4. MAIN UI LOGIC] ---
if m_key == MASTER_KEY:
    tab1, tab2, tab3, tab4 = st.tabs(["📊 SENTINEL (LIVE)", "📈 PRO METRICS", "📰 AI BROADCAST", "⚖️ POSITION ENGINE"])
    
    with tab1:
        # [FOLDER 1 UPGRADE: Glow Cards + Dominance Tags]
        st.subheader("🛰️ Sentinel Live Nodes (Glow Active)")
        if data:
            cols = st.columns(4)
            for i, coin in enumerate(data):
                p, c24 = coin.get('current_price', 0) or 0, coin.get('price_change_percentage_24h', 0) or 0
                glow = "#00FF00" if c24 >= 0 else "#FF4B4B"
                with cols[i % 4]:
                    st.markdown(f"""
                    <div class="crypto-card" style="border: 2px solid {glow};">
                        <div class="inner-card">
                            <img src="{coin.get('image')}" width="38" style="margin-right: 12px;">
                            <div>
                                <p style="margin:0; font-size:11px; color:#1565C0; font-weight:bold;">{coin.get('symbol','').upper()}/INR</p>
                                <h4 style="margin:0; color:#0D47A1 !important; font-size:17px;">₹{p:,.2f}</h4>
                                <p style="margin:0; font-size:10px; font-weight:bold; color:{glow};">24h: {c24:+.1f}%</p>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)
        else: st.warning("🔄 Waiting for Global Market Nodes...")

    with tab2:
        # [FOLDER 2 UPGRADE: Volume-Color Algorithm]
        st.subheader("📈 Institutional Heatmap (ATH Tracker)")
        if data:
            formatted = []
            for c in data:
                formatted.append({
                    "Logo": f'<img src="{c["image"]}" width="25">',
                    "Coin": c["name"],
                    "Price": f"₹{c['current_price']:,.2f}",
                    "ATH Price": f"₹{c.get('ath',0):,.2f}",
                    "Recovery": f"{c.get('ath_change_percentage',0):.1f}%",
                    "Volume (24h)": f"₹{c.get('total_volume',0):,.0f}"
                })
            st.write(pd.DataFrame(formatted).to_html(escape=False, index=False), unsafe_allow_html=True)

    with tab3:
        # [FOLDER 3 UPGRADE: AI Trade Signals]
        st.subheader("📰 AI Sovereign Broadcast")
        st.markdown("""<div style="background:rgba(227,242,253,0.95); padding:20px; border-radius:15px; border-left:8px solid #2196F3;">
            <p style="color:#1565C0 !important; font-weight:800; margin:0;">🐦 Twitter (X) Live Signals</p>
            <p style="color:#0D47A1 !important; font-size:14px; font-weight:bold;">🛰️ $XRT: Support found at ₹510. AI sectors showing 2026 strength.</p>
        </div>""", unsafe_allow_html=True)
        
        if st.button("🚀 Generate AI Trade Intelligence"):
            if api_key:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"Analyze these coins: {list(COIN_MAP.values())}. Provide Hinglish 'Buy/Hold/Sell' signals based on 2026 crypto market trends."
                st.success(model.generate_content(prompt).text)

    with tab4:
        # [FOLDER 4 UPGRADE: Position Sizing Algorithm]
        st.subheader("⚖️ Sovereign Position Sizing Engine")
        col1, col2 = st.columns(2)
        with col1:
            budget = st.number_input("Total Trading Budget (INR)", value=50000)
            risk_per_trade = st.slider("Risk Per Trade (%)", 1, 10, 2)
        with col2:
            entry_p = st.number_input("Coin Entry Price (INR)", value=100.0)
            sl_p = st.number_input("Stop Loss Price (INR)", value=95.0)
        
        if st.button("Calculate Sovereign Position"):
            risk_amt = budget * (risk_per_trade / 100)
            risk_per_coin = entry_p - sl_p
            if risk_per_coin > 0:
                quantity = risk_amt / risk_per_coin
                st.divider()
                st.header(f"🛒 Buy Quantity: {quantity:.2f} Coins")
                st.info(f"Total Investment: ₹{quantity * entry_p:,.2f} | Risking: ₹{risk_amt}")
            else: st.error("Stop Loss must be below Entry Price.")

else: st.info("⚠️ Master Key Required. Use the Sidebar on the left (←) to unlock (SAMASTIPUR@2026).")
            
