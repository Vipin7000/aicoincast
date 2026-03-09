import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
import re

# --- [1. SYSTEM CONFIG & NEON UI] ---
st.set_page_config(page_title="AiCoincast v21.8 Core", layout="wide", initial_sidebar_state="expanded")
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

# [MASTER ALGORITHM: TOP 20 FETCH WITH FALLBACK SHIELD]
@st.cache_data(ttl=60)
def fetch_omniscient_data():
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_desc&per_page=20&page=1&sparkline=false&price_change_percentage=24h,7d"
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            return r.json()
        return []
    except: return []

data_20 = fetch_omniscient_data()

# --- [2. OMNI-TICKER (v21.8)] ---
ticker_items = []
if data_20:
    for c in data_20:
        change = c.get('price_change_percentage_24h', 0) or 0
        indicator = "🟢▲" if change > 0 else "🔴▼"
        ticker_items.append(f"{indicator} {c.get('symbol','').upper()}: ₹{c.get('current_price',0):,.0f}")
    ticker_final = " | ".join(ticker_items)
else: ticker_final = "📡 Neural Nodes Syncing... BTC: ₹6,184,210 | XRT: ₹77.49 | POL: ₹38.20"

st.markdown(f'<div style="background:#000; padding:12px; border:2px solid #00FF00; margin-bottom:20px;"><marquee style="color:#00FF00; font-weight:bold; font-size:18px; font-family: monospace;">🚀 {ticker_final}</marquee></div>', unsafe_allow_html=True)

# --- [3. SIDEBAR VAULT] ---
with st.sidebar:
    st.title("🔐 OMNI VAULT")
    m_key = st.text_input("Master Key", type="password", placeholder="SAMASTIPUR@2026")
    api_key_raw = st.text_input("AI Neural Key", type="password")
    api_key = re.sub(r'[^a-zA-Z0-9_-]', '', api_key_raw.strip())
    if data_20:
        total_mc = sum([float(c.get('market_cap', 0) or 0) for c in data_20])
        st.info(f"💼 Portfolio MC: ₹{total_mc:,.0f}")

# --- [4. MAIN TERMINAL LOGIC] ---
if m_key == MASTER_KEY:
    tab1, tab2, tab3, tab4 = st.tabs(["📊 SENTINEL", "📈 PERFORMANCE", "📰 BROADCAST", "⚖️ RISK ENGINE"])
    
    with tab1:
        st.subheader("🛰️ Sentinel Live Nodes (Volume-Context Active)")
        if data_20:
            cols = st.columns(4)
            for i, coin in enumerate(data_20[:12]):
                c24 = float(coin.get('price_change_percentage_24h', 0) or 0)
                mc = float(coin.get('market_cap', 1))
                vol = float(coin.get('total_volume', 0))
                v_to_mc = (vol / mc) * 100
                color = "#00FF00" if c24 >= 0 else "#FF4B4B"
                with cols[i % 4]:
                    st.markdown(f"""
                    <div class="crypto-card" style="border-color: {color};">
                        <div class="inner-card">
                            {"<div class='alpha-badge'>🔥 VOL SPIKE</div>" if v_to_mc > 15 else ""}
                            <img src="{coin.get('image')}" width="35" style="margin-right:12px;">
                            <div>
                                <p style="margin:0; font-size:11px; color:#BBDEFB;">{coin.get('symbol','').upper()}/INR</p>
                                <p class="price-neon">₹{coin.get('current_price',0):,.0f}</p>
                                <p style="margin:0; font-size:10px; font-weight:bold; color:{color};">24h: {c24:+.1f}% | V/MC: {v_to_mc:.1f}%</p>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)

    with tab2:
        st.subheader("📈 Trend Strength Index (No-Null Shield)")
        if data_20:
            perf_list = []
            for c in data_20:
                c24 = float(c.get('price_change_percentage_24h', 0) or 0)
                c7d = float(c.get('price_change_percentage_7d_in_currency', 0) or 0)
                tsi = (c24 + c7d) / 2
                perf_list.append({
                    "Coin": c.get('name'),
                    "Price": f"₹{c.get('current_price',0):,.2f}",
                    "TSI Strength": f"{tsi:+.2f}",
                    "7D Change": f"{c7d:+.1f}%"
                })
            st.table(pd.DataFrame(perf_list))

    with tab3:
        st.subheader("📰 Alpha Broadcast: Gainers & Losers")
        if data_20:
            sorted_data = sorted(data_20, key=lambda x: float(x.get('price_change_percentage_24h', 0) or 0), reverse=True)
            cL, cR = st.columns(2)
            with cL:
                st.success("🔥 Top 3 Movers")
                for c in sorted_data[:3]: st.write(f"**{c['name']}**: {c['price_change_percentage_24h']:+.2f}%")
            with cR:
                st.error("❄️ Top 3 Laggards")
                for c in sorted_data[-3:]: st.write(f"**{c['name']}**: {c['price_change_percentage_24h']:+.2f}%")

else: st.info("⚠️ Master Key Required (SAMASTIPUR@2026).")
