import streamlit as st
import pandas as pd
import requests
from streamlit_autorefresh import st_autorefresh # NEW: Auto-Refresh Component

# --- [1. MASTER CONFIG & ETERNAL DESIGN] ---
st.set_page_config(page_title="AiCoincast v4.0 Eternal", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

# SILENT REFRESH: Updates every 30 seconds
count = st_autorefresh(interval=30000, key="fizzbuzzcounter")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;600&display=swap');
    .stApp { background: radial-gradient(circle at center, #0d0221 0%, #020105 100%) !important; }
    
    /* TRIPLE LAYER HEADER */
    .ticker-wrap { width: 100%; overflow: hidden; background: #000; border-bottom: 1px solid #00FF00; padding: 10px 0; }
    .ticker { display: flex; white-space: nowrap; animation: ticker 25s linear infinite; }
    .t-card { flex-shrink: 0; padding: 0 25px; border-right: 1px solid rgba(0,255,0,0.3); font-size: 0.85rem; font-weight: bold; }
    @keyframes ticker { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }

    .news-nexus { background: rgba(0, 255, 0, 0.08); color: #00FF00; padding: 8px; font-size: 0.8rem; border-bottom: 2px solid #00FF00; overflow: hidden; white-space: nowrap; }
    .news-scroll { display: inline-block; animation: scroll-news 45s linear infinite; }
    @keyframes scroll-news { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

    /* ELITE CARDS */
    .node-card {
        background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.1); border-radius: 15px;
        padding: 20px; transition: 0.4s; height: 100%; border-bottom: 4px solid #00FF00;
    }
    .up { color: #00FF00 !important; font-weight: bold; }
    .down { color: #FF0000 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- [CORE ENGINE] ---
def fetch_elite_data(ids=None):
    base = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&price_change_percentage=24h,7d,30d,200d"
    url = f"{base}&ids={','.join(ids)}" if ids else f"{base}&order=market_cap_desc&per_page=100&page=1"
    try:
        r = requests.get(url, timeout=15)
        return r.json() if r.status_code == 200 else []
    except: return []

def fmt(val):
    v = float(val) if val else 0.0
    arr, cls = ("▲", "up") if v > 0 else (("▼", "down") if v < 0 else ("▬", ""))
    return f'<span class="{cls}">{arr} {abs(v):.1f}%</span>'

CORE_IDS = ["bitcoin", "ethereum", "polygon-ecosystem-token", "virtual-protocol", "qanplatform", "chaingpt", "velas", "griffain", "vaiot", "everdome", "bloktopia", "sin-city", "robonomics-network", "unmarshal", "layerai", "nftb"]

# --- [SIDEBAR] ---
with st.sidebar:
    st.title("🛰️ ETERNAL WATCHER")
    key = st.text_input("Master Key", type="password")
    st.markdown("---")
    h_qty = st.number_input("Holdings (XRT)", 206)
    h_buy = st.number_input("Buy Price (₹)", 480)

if key == MASTER_KEY:
    top_data = fetch_elite_data()
    sentinel_data = fetch_elite_data(ids=CORE_IDS)

    # 1. HEADER LAYERS
    if top_data:
        t_html = "".join([f'<div class="t-card"><b>{c["symbol"].upper()}</b> ₹{c["current_price"]:,.0f} {fmt(c.get("price_change_percentage_24h"))}</div>' for c in (top_data[:20]*2)])
        st.markdown(f'<div class="ticker-wrap"><div class="ticker">{t_html}</div></div>', unsafe_allow_html=True)
    
    st.markdown("""<div class="news-nexus"><div class="news-scroll">💎 GHOST SYNC ACTIVE: Real-time price pulse engaged | No-blink refresh every 30s | XRT Strategic Reserve Monitoring...</div></div>""", unsafe_allow_html=True)

    # 2. SENTIMENT & VAULT
    col_v1, col_v2 = st.columns([1, 2])
    with col_v1:
        st.markdown("""<div style="background:rgba(255,255,255,0.02); border:2px solid #00FF00; border-radius:15px; padding:15px; text-align:center;">
            <div style="font-size:0.7rem; color:#00FF00; letter-spacing:2px;">ORACLE SENTIMENT</div>
            <div style="font-size:1.6rem; font-weight:bold;">72 | GREED 📈</div>
        </div>""", unsafe_allow_html=True)
    with col_v2:
        x_coin = next((i for i in sentinel_data if i["id"] == "robonomics-network"), None)
        if x_coin:
            val = x_coin['current_price'] * h_qty
            st.markdown(f"""<div style="background:rgba(0,255,0,0.05); border:1px solid #00FF00; border-radius:15px; padding:15px; text-align:center;">
                <div style="font-size:2.2rem; color:#00FF00; font-weight:bold; text-shadow:0 0 15px #00FF00;">₹{val:,.2f}</div>
                <div style="font-size:0.7rem; opacity:0.6; letter-spacing:3px;">XRT STRATEGIC RESERVE</div>
            </div>""", unsafe_allow_html=True)

    # 3. SENTINEL ALPHA (GRID)
    st.header("🛰️ Sentinel Alpha Command")
    cols = st.columns(3)
    for idx, c in enumerate(sentinel_data):
        with cols[idx % 3]:
            p_24h = c.get('price_change_percentage_24h_in_currency', 0)
            whale = "🐋" if abs(p_24h) > 4 else ""
            st.markdown(f"""
            <div class="node-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <b style="color:#00FF00;">{c['name'].upper()}</b>
                    <img src="{c['image']}" width="28">
                </div>
                <h2 style="margin:10px 0;">₹{c['current_price']:,.2f}</h2>
                <div style="display:grid; grid-template-columns:1fr 1fr; font-size:0.8rem; gap:10px;">
                    <div>24H: {fmt(p_24h)}</div>
                    <div>7D: {fmt(c.get('price_change_percentage_7d_in_currency'))}</div>
                </div>
                <div style="margin-top:10px; text-align:right;">{whale}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

else:
    st.info("🔒 Sovereign Master, initialize the Eternal Watcher.")
    
