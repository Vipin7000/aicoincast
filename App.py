import streamlit as st
import pandas as pd
import requests
from streamlit_autorefresh import st_autorefresh

# --- [1. MASTER CONFIG & DESIGN] ---
st.set_page_config(page_title="AiCoincast v4.2 Absolute", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"
st_autorefresh(interval=30000, key="eternal_sync")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;600&display=swap');
    .stApp { background: #020105 !important; }
    
    /* TOP TICKER */
    .ticker-wrap { width: 100%; overflow: hidden; background: #000; border-bottom: 1px solid #00FF00; padding: 10px 0; }
    .ticker { display: flex; white-space: nowrap; animation: ticker 25s linear infinite; }
    .t-card { flex-shrink: 0; padding: 0 25px; border-right: 1px solid rgba(0,255,0,0.3); font-size: 0.85rem; font-weight: bold; color: white; }
    @keyframes ticker { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }

    /* RADAR GRID */
    .radar-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(110px, 1fr)); gap: 10px; padding: 12px; border: 1px solid #00FF00; background: rgba(0,255,0,0.02); margin: 15px 0; border-radius: 10px; }
    .radar-box { text-align: center; font-size: 0.7rem; border-right: 1px solid rgba(255,255,255,0.1); color: white; }

    /* SENTINEL CARDS */
    .node-card { background: rgba(255, 255, 255, 0.03); border-radius: 12px; padding: 15px; border-bottom: 3px solid #00FF00; margin-bottom: 10px; }
    .up { color: #00FF00 !important; font-weight: bold; }
    .down { color: #FF0000 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- [CORE ENGINE] ---
def fetch_data(ids=None):
    base = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&price_change_percentage=24h,7d,30d"
    url = f"{base}&ids={','.join(ids)}" if ids else f"{base}&order=market_cap_desc&per_page=100"
    try:
        r = requests.get(url, timeout=10)
        return r.json() if r.status_code == 200 else []
    except: return []

def safe_fmt(val):
    v = float(val) if val is not None else 0.0
    arr, cls = ("▲", "up") if v > 0 else (("▼", "down") if v < 0 else ("▬", ""))
    return f'<span class="{cls}">{arr} {abs(v):.1f}%</span>'

CORE_IDS = ["bitcoin", "ethereum", "polygon-ecosystem-token", "virtual-protocol", "qanplatform", "chaingpt", "velas", "griffain", "vaiot", "everdome", "bloktopia", "sin-city", "robonomics-network", "unmarshal", "layerai", "nftb"]

# --- [DEPLOYMENT] ---
with st.sidebar:
    st.title("🛡️ BLUEPRINT v4.2")
    key = st.text_input("Master Key", type="password")
    h_qty = st.number_input("Holdings (XRT)", 369)
    h_buy = st.number_input("Buy Price", 480)

if key == MASTER_KEY:
    top_list = fetch_data()
    sentinel = fetch_data(ids=CORE_IDS)

    # 1. TOP 20 SCROLLING TICKER
    if top_list:
        t_html = "".join([f'<div class="t-card">{c["symbol"].upper()} ₹{c["current_price"]:,.0f} {safe_fmt(c.get("price_change_percentage_24h"))}</div>' for c in (top_list[:20]*2)])
        st.markdown(f'<div class="ticker-wrap"><div class="ticker">{t_html}</div></div>', unsafe_allow_html=True)

    # 2. WORLD RADAR
    st.markdown(f"""<div class="radar-grid">
        <div class="radar-box">🇮🇳 NIFTY<br>{safe_fmt(0.7)}</div><div class="radar-box">🇺🇸 S&P 500<br>{safe_fmt(1.1)}</div>
        <div class="radar-box">🇯🇵 NIKKEI<br>{safe_fmt(-0.3)}</div><div class="radar-box">🇩🇪 DAX 40<br>{safe_fmt(0.8)}</div>
        <div class="radar-box">🇬🇧 FTSE 100<br>{safe_fmt(-0.1)}</div><div class="radar-box">🇫🇷 CAC 40<br>{safe_fmt(0.4)}</div>
        <div class="radar-box">🇨🇳 SHANGHAI<br>{safe_fmt(0.2)}</div><div class="radar-box">🇭🇰 HANG SENG<br>{safe_fmt(-0.9)}</div>
        <div class="radar-box">🇰🇷 KOSPI<br>{safe_fmt(0.5)}</div><div class="radar-box">🇦🇺 ASX 200<br>{safe_fmt(0.3)}</div>
    </div>""", unsafe_allow_html=True)

    # 3. VAULT
    x_coin = next((i for i in sentinel if i["id"] == "robonomics-network"), None)
    if x_coin:
        val = x_coin['current_price'] * h_qty
        st.markdown(f"""<div style="background:rgba(0,255,0,0.05); border:2px solid #00FF00; border-radius:15px; padding:20px; text-align:center; margin-bottom:20px;">
            <div style="font-size:3rem; color:#00FF00; font-weight:800; text-shadow:0 0 15px #00FF00;">₹{val:,.2f}</div>
            <div style="font-size:0.8rem; opacity:0.6; letter-spacing:3px;">XRT STRATEGIC RESERVE</div></div>""", unsafe_allow_html=True)

    # 4. SENTINEL ALPHA COMMAND
    st.subheader("🛰️ Sentinel Alpha Command")
    cols = st.columns(3)
    for idx, c in enumerate(sentinel):
        with cols[idx % 3]:
            p_24h = float(c.get('price_change_percentage_24h_in_currency') or 0.0)
            st.markdown(f"""<div class="node-card">
                <div style="display:flex; justify-content:space-between;"><b>{c.get('name','').upper()}</b><img src="{c.get('image','')}" width="20"></div>
                <h3 style="margin:5px 0;">₹{c.get('current_price',0):,.2f}</h3>
                <div style="font-size:0.75rem;">24H: {safe_fmt(p_24h)} | 🐋: {"Yes" if abs(p_24h)>4 else "No"}</div>
            </div>""", unsafe_allow_html=True)

    # 5. GLOBAL MEGA NODE (GLOBAL CRYPTO)
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🌍 Global Mega Node")
    if top_list:
        df = pd.DataFrame([{
            "Rank": i["market_cap_rank"], "Asset": i["name"], "Price": f"₹{i['current_price']:,.2f}",
            "24H": i.get("price_change_percentage_24h_in_currency"), "7D": i.get("price_change_percentage_7d_in_currency")
        } for i in top_list])
        st.write(df.to_html(escape=False, formatters={"24H": safe_fmt, "7D": safe_fmt}, index=False), unsafe_allow_html=True)

else:
    st.info("🔒 Sovereign Master, authentication required to reveal the Blueprint.")
    
