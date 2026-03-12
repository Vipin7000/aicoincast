import streamlit as st
import pandas as pd
import requests
from streamlit_autorefresh import st_autorefresh

# --- [1. MASTER CONFIG & CRYSTAL DESIGN] ---
st.set_page_config(page_title="AiCoincast v4.3 Crystal", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

# Refresh every 60s to prevent API Bans (Crashes)
st_autorefresh(interval=60000, key="crystal_sync")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@400;700&display=swap');
    
    /* BACKGROUND & TEXT VISIBILITY */
    .stApp { background: #050505 !important; color: #FFFFFF !important; }
    h1, h2, h3, b, p, span, div { font-family: 'Inter', sans-serif; color: #FFFFFF !important; }
    .neon-label { color: #00FF00 !important; font-family: 'Orbitron', sans-serif; font-weight: bold; text-shadow: 0 0 5px #00FF00; }

    /* TOP 20 TICKER */
    .ticker-wrap { width: 100%; overflow: hidden; background: #111; border-bottom: 2px solid #00FF00; padding: 12px 0; }
    .ticker { display: flex; white-space: nowrap; animation: ticker 30s linear infinite; }
    .t-card { flex-shrink: 0; padding: 0 30px; border-right: 1px solid #333; font-weight: bold; font-size: 1rem; }
    @keyframes ticker { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }

    /* RADAR GRID - BIGGER FONTS */
    .radar-grid { 
        display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); 
        gap: 15px; padding: 20px; border: 2px solid #00FF00; 
        background: rgba(0,255,0,0.05); margin: 20px 0; border-radius: 12px; 
    }
    .radar-box { text-align: center; font-size: 1.1rem; font-weight: bold; border-right: 1px solid #444; }
    .radar-box:last-child { border-right: none; }

    /* SENTINEL CRYSTAL CARDS */
    .node-card { 
        background: rgba(255, 255, 255, 0.05); border-radius: 15px; padding: 20px; 
        border: 1px solid #333; border-left: 5px solid #00FF00; margin-bottom: 15px;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.5);
    }
    
    .up { color: #00FF00 !important; font-weight: bold; }
    .down { color: #FF4B4B !important; font-weight: bold; }
    .gray { color: #AAAAAA !important; font-size: 0.8rem; }
    </style>
    """, unsafe_allow_html=True)

# --- [CORE ENGINE WITH ANTI-CRASH CACHE] ---
@st.cache_data(ttl=60)
def fetch_master_data(ids=None):
    # Fetching 200d for long term indicator
    base = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&price_change_percentage=24h,7d,30d,200d"
    url = f"{base}&ids={','.join(ids)}" if ids else f"{base}&order=market_cap_desc&per_page=100"
    try:
        r = requests.get(url, timeout=15)
        return r.json() if r.status_code == 200 else []
    except: return []

def safe_fmt(val, prefix=""):
    try:
        v = float(val) if val is not None else 0.0
        arr, cls = ("▲", "up") if v > 0 else (("▼", "down") if v < 0 else ("▬", "gray"))
        return f'<span class="{cls}">{prefix}{arr} {abs(v):.1f}%</span>'
    except: return "▬"

CORE_IDS = ["bitcoin", "ethereum", "polygon-ecosystem-token", "virtual-protocol", "qanplatform", "chaingpt", "velas", "griffain", "vaiot", "everdome", "bloktopia", "sin-city", "robonomics-network", "unmarshal", "layerai", "nftb"]

# --- [DEPLOYMENT] ---
with st.sidebar:
    st.markdown("<h2 class='neon-label'>🛡️ CRYSTAL VAULT</h2>", unsafe_allow_html=True)
    key = st.text_input("Sovereign Key", type="password")
    h_qty = st.number_input("Holdings (XRT)", 369)
    h_buy = st.number_input("Buy Price (₹)", 480)

if key == MASTER_KEY:
    full_data = fetch_master_data() # Top 100
    sentinel = fetch_master_data(ids=CORE_IDS) # Specific Nodes

    # 1. TOP 20 TICKER
    if full_data:
        t_html = "".join([f'<div class="t-card"><span class="neon-label">{c["symbol"].upper()}</span> ₹{c["current_price"]:,.0f} {safe_fmt(c.get("price_change_percentage_24h_in_currency"))}</div>' for c in (full_data[:20]*2)])
        st.markdown(f'<div class="ticker-wrap"><div class="ticker">{t_html}</div></div>', unsafe_allow_html=True)

    # 2. WORLD RADAR (BIGGER & CLEARER)
    st.markdown(f"""<div class="radar-grid">
        <div class="radar-box">🇮🇳 NIFTY<br>{safe_fmt(0.8)}</div><div class="radar-box">🇺🇸 S&P 500<br>{safe_fmt(1.2)}</div>
        <div class="radar-box">🇯🇵 NIKKEI<br>{safe_fmt(-0.3)}</div><div class="radar-box">🇩🇪 DAX 40<br>{safe_fmt(0.9)}</div>
        <div class="radar-box">🇨🇳 SHANGHAI<br>{safe_fmt(0.1)}</div>
    </div>""", unsafe_allow_html=True)

    # 3. MASTER VAULT
    x_coin = next((i for i in sentinel if i["id"] == "robonomics-network"), None)
    if x_coin:
        val = x_coin['current_price'] * h_qty
        st.markdown(f"""<div style="background:rgba(0,255,0,0.08); border:2px solid #00FF00; border-radius:20px; padding:30px; text-align:center; margin-bottom:25px;">
            <div style="font-size:3.5rem; color:#00FF00; font-weight:800; text-shadow: 0 0 15px #00FF00;">₹{val:,.2f}</div>
            <div class="neon-label" style="letter-spacing:5px;">STRATEGIC ASSET COMMAND (XRT)</div></div>""", unsafe_allow_html=True)

    # 4. SENTINEL ALPHA (ALL INDICATORS ADDED)
    st.markdown("<h2 class='neon-label'>🛰️ Sentinel Alpha Command</h2>", unsafe_allow_html=True)
    cols = st.columns(3)
    for idx, c in enumerate(sentinel):
        with cols[idx % 3]:
            st.markdown(f"""<div class="node-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <b style="font-size:1.3rem;">{c.get('name','').upper()}</b>
                    <img src="{c.get('image','')}" width="30">
                </div>
                <h2 style="margin:10px 0; color:#FFFFFF;">₹{c.get('current_price',0):,.2f}</h2>
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
                    <div class="gray">24H: {safe_fmt(c.get('price_change_percentage_24h_in_currency'))}</div>
                    <div class="gray">7D: {safe_fmt(c.get('price_change_percentage_7d_in_currency'))}</div>
                    <div class="gray">30D: {safe_fmt(c.get('price_change_percentage_30d_in_currency'))}</div>
                    <div class="gray">200D: {safe_fmt(c.get('price_change_percentage_200d_in_currency'))}</div>
                </div>
            </div>""", unsafe_allow_html=True)

    # 5. GLOBAL MEGA NODE (PREMIUM TABLE)
    st.markdown("<br><h2 class='neon-label'>🌍 Global Mega Node</h2>", unsafe_allow_html=True)
    if full_data:
        df = pd.DataFrame([{
            "Rank": i["market_cap_rank"], "Logo": i["image"], "Asset": i["name"], 
            "Price": f"₹{i['current_price']:,.2f}", 
            "24H": i.get("price_change_percentage_24h_in_currency"),
            "7D": i.get("price_change_percentage_7d_in_currency"),
            "30D": i.get("price_change_percentage_30d_in_currency"),
            "200D": i.get("price_change_percentage_200d_in_currency")
        } for i in full_data])
        
        # Rendering table with white text and clear indicators
        st.write(df.to_html(escape=False, formatters={
            "Logo": lambda x: f'<img src="{x}" width="25">',
            "24H": safe_fmt, "7D": safe_fmt, "30D": safe_fmt, "200D": safe_fmt
        }, index=False), unsafe_allow_html=True)

else:
    st.info("🔒 Sovereign Master, authentication required to reveal the Crystal Blueprint.")
    
