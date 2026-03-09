import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
import re

# --- [1. SYSTEM CONFIG & OMEGA UI] ---
st.set_page_config(page_title="AiCoincast v22.8 Absolute", layout="wide", initial_sidebar_state="expanded")
MASTER_KEY = "SAMASTIPUR@2026"

st.markdown("""
    <style>
    .stApp { background-color: #0A041A !important; }
    h1, h2, h3, h4, p, span, li { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] { background-color: #1A0B35 !important; border-right: 3px solid #00FF00 !important; }
    .crypto-card { background: #000000; padding: 2px; border-radius: 12px; margin-bottom: 12px; border: 2px solid #41444C; transition: 0.3s; }
    .inner-card { display: flex; align-items: center; background: #0D47A1; padding: 15px; border-radius: 10px; position: relative; }
    .price-neon { color: #00FF00 !important; font-size: 20px; font-weight: 900; text-shadow: 0 0 5px #00FF00; }
    .alpha-badge { background: #FFD700; color: #000 !important; font-size: 10px; padding: 2px 6px; border-radius: 4px; font-weight: bold; position: absolute; top: 5px; right: 5px; }
    </style>
    """, unsafe_allow_html=True)

# [MASTER ALGORITHM: 12 SOVEREIGN ASSETS]
SOVEREIGN_MAP = {
    "bitcoin": "BTC", "ethereum": "ETH", "virtual-protocol": "VIRTUAL", 
    "griffin-2": "GRIFFIN", "v-ai-2": "VAI", "robonomics-network": "XRT", 
    "velas": "VLX", "qanplatform": "QANX", "chaingpt": "CGPT", 
    "sinverse": "SIN", "matic-network": "POL", "nftb": "NFTB"
}

@st.cache_data(ttl=60)
def fetch_intelligence():
    ids = ",".join(SOVEREIGN_MAP.keys())
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&ids={ids}&order=market_cap_desc&sparkline=false&price_change_percentage=24h,7d"
    try:
        r = requests.get(url, timeout=15)
        # [FIX] Ensures data is always a list to avoid TypeError
        return r.json() if (r.status_code == 200 and isinstance(r.json(), list)) else []
    except: return []

data = fetch_intelligence()

# --- [2. INDESTRUCTIBLE TICKER] ---
ticker_fallback = "📡 Nodes Syncing... BTC: ₹6,256,000 | XRT: ₹124.91 | LAI: ₹0.28"
if data:
    try:
        ticker_list = [f"{'🟢▲' if float(c.get('price_change_percentage_24h',0) or 0)>0 else '🔴▼'} {c.get('symbol','').upper()}: ₹{float(c.get('current_price',0) or 0):,.0f}" for c in data if c.get('symbol')]
        ticker_fallback = " | ".join(ticker_list)
    except: pass
st.markdown(f'<div style="background:#000; padding:12px; border:2px solid #00FF00; margin-bottom:20px;"><marquee style="color:#00FF00; font-weight:bold; font-size:18px;">🚀 {ticker_fallback}</marquee></div>', unsafe_allow_html=True)

# --- [3. SIDEBAR VAULT] ---
with st.sidebar:
    st.title("🔐 CORE VAULT")
    m_key = st.text_input("Master Key", type="password", placeholder="SAMASTIPUR@2026")
    api_key = st.text_input("AI Neural Key", type="password")
    if data:
        # [ALGORITHM: Precise Portfolio MC]
        total_mc = sum([float(c.get('market_cap', 0) or 0) for c in data])
        st.info(f"💼 Portfolio MC: ₹{total_mc:,.0f}")

# --- [4. MAIN TERMINAL LOGIC] ---
if m_key == MASTER_KEY:
    tab1, tab2, tab3, tab4 = st.tabs(["📊 SENTINEL", "📈 PERFORMANCE", "📰 BROADCAST", "⚖️ RISK ENGINE"])
    
    with tab1:
        st.subheader("🛰️ Sentinel Live Nodes (Folder 1)")
        if data:
            cols = st.columns(4)
            for i, coin in enumerate(data):
                p = float(coin.get('current_price', 0) or 0)
                c24 = float(coin.get('price_change_percentage_24h', 0) or 0)
                mc = float(coin.get('market_cap', 1))
                vol = float(coin.get('total_volume', 0))
                v_to_mc = (vol / mc) * 100 # [ALGORITHM: Vol/MC Ratio]
                color = "#00FF00" if c24 >= 0 else "#FF4B4B"
                with cols[i % 4]:
                    st.markdown(f"""
                    <div class="crypto-card" style="border-color: {color};">
                        <div class="inner-card">
                            {"<div class='alpha-badge'>🔥 VOL SPIKE</div>" if v_to_mc > 15 else ""}
                            <img src="{coin.get('image','')}" width="35" style="margin-right:12px;">
                            <div>
                                <p style="margin:0; font-size:11px; color:#BBDEFB;">{coin.get('symbol','').upper()}/INR</p>
                                <p class="price-neon">₹{p:,.0f}</p>
                                <p style="margin:0; font-size:10px; font-weight:bold; color:{color};">{c24:+.1f}% | V/MC: {v_to_mc:.1f}%</p>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)

    with tab2:
        st.subheader("📈 Trend Strength & Movers Grid (Folder 2)")
        if data:
            # [ALGORITHM: Sorting for Top Movers]
            sorted_data = sorted(data, key=lambda x: float(x.get('price_change_percentage_24h', 0) or 0), reverse=True)
            cg, cl = st.columns(2)
            with cg:
                st.success("🔥 Top 3 Movers")
                for c in sorted_data[:3]: st.write(f"**{c['name']}**: {float(c.get('price_change_percentage_24h',0)):+.2f}%")
            with cl:
                st.error("❄️ Top 3 Laggards")
                for c in sorted_data[-3:]: st.write(f"**{c['name']}**: {float(c.get('price_change_percentage_24h',0)):+.2f}%")
            
            st.divider()
            # [ALGORITHM: 7D Heatmap Restoration]
            perf_list = [{"Logo": f'<img src="{c.get("image","")}" width="20">', "Coin": c['name'], "Price": f"₹{float(c['current_price']):,.2f}", "24h": f"{float(c.get('price_change_percentage_24h',0)):+.1f}%", "7D": f"{float(c.get('price_change_percentage_7d_in_currency', 0) or 0):+.1f}%"} for c in data]
            st.write(pd.DataFrame(perf_list).to_html(escape=False, index=False), unsafe_allow_html=True)

    with tab3:
        st.subheader("📰 Broadcast Alpha Sentiment (Folder 3)")
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; border-left: 5px solid #00FF00;">
            <p style="font-weight:bold; margin:0; color:#00FF00;">🐦 Twitter Neural Feed</p>
            <p style="font-size:12px;">Bullish accumulation detected for $XRT in Samastipur node. Social volume up 14%.</p>
        </div>
        """, unsafe_allow_html=True)

    with tab4:
        st.subheader("⚖️ Sovereign Risk Engine (Folder 4)")
        col1, col2 = st.columns(2)
        with col1:
            budget = st.number_input("Budget (INR)", value=50000)
            risk = st.slider("Risk (%)", 1, 10, 2)
        with col2:
            entry = st.number_input("Entry Price", value=100.0)
            sl = st.number_input("Stop Loss", value=95.0)
        
        if st.button("Calculate Optimal Size"):
            risk_amt = budget * (risk/100)
            diff = entry - sl
            if diff > 0:
                qty = risk_amt / diff
                st.success(f"🛒 Target Quantity: {qty:.2f} Coins | Total Risk: ₹{risk_amt}")
            else: st.error("Stop Loss must be below Entry.")

else: st.info("⚠️ Master Key Required (SAMASTIPUR@2026).")
