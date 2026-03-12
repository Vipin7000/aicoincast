import streamlit as st
import pandas as pd
import requests
from streamlit_autorefresh import st_autorefresh

# --- [1. MASTER CONFIG & DESIGN LOCK] ---
st.set_page_config(page_title="AiCoincast v5.5 Singularity", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"
st_autorefresh(interval=60000, key="singularity_sync")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@400;700&display=swap');
    
    /* ABSOLUTE PAGE SCROLL LOCK */
    html, body, [data-testid="stAppViewContainer"], .main { 
        background: #020105 !important; color: white !important; 
        overflow: hidden !important; height: 100vh !important;
    }

    /* TOP 20 TICKER - FIXED Z-INDEX */
    .ticker-wrap { 
        width: 100%; overflow: hidden; background: #000; border-bottom: 2px solid #00FF00; 
        padding: 10px 0; position: fixed; top: 0; left: 0; z-index: 99999;
    }
    .ticker { display: flex; white-space: nowrap; animation: ticker 25s linear infinite; }
    .t-card { flex-shrink: 0; padding: 0 30px; border-right: 1px solid #333; font-weight: bold; color: #00FF00; font-size: 1rem; }
    @keyframes ticker { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }

    /* HEADER NEON BOXES */
    .header-box { background: rgba(0, 255, 0, 0.05); border: 2px solid #00FF00; border-radius: 12px; padding: 12px; text-align: center; }
    .neon-glow { color: #00FF00; text-shadow: 0 0 12px #00FF00; font-family: 'Orbitron'; font-weight: bold; }

    /* RADAR GRID - 11 INDICES */
    .radar-grid { 
        display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); 
        gap: 10px; padding: 12px; border: 1px solid #00FF00; background: rgba(0,255,0,0.02); border-radius: 10px; margin-top: 60px;
    }
    .radar-box { text-align: center; font-size: 0.85rem; font-weight: bold; color: white; border-right: 1px solid #333; }

    /* CHAMBER LOCK (vh BASED SCROLL) */
    .chamber-lock { 
        height: 36vh !important; overflow-y: auto !important; overflow-x: hidden !important;
        border: 2px solid #333; padding: 15px; border-radius: 15px; 
        background: rgba(255,255,255,0.01); display: block; width: 100%; box-sizing: border-box;
    }
    .chamber-lock::-webkit-scrollbar { width: 5px; }
    .chamber-lock::-webkit-scrollbar-thumb { background: #00FF00; border-radius: 10px; }

    .node-card { background: rgba(255, 255, 255, 0.04); border-radius: 10px; padding: 15px; border-left: 5px solid #00FF00; margin-bottom: 12px; }
    .up { color: #00FF00 !important; font-weight: bold; }
    .down { color: #FF4B4B !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- [CORE ENGINE] ---
@st.cache_data(ttl=60)
def fetch_master_data(ids=None):
    base = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&price_change_percentage=24h,7d,30d,200d"
    url = f"{base}&ids={','.join(ids)}" if ids else f"{base}&order=market_cap_desc&per_page=150"
    try:
        r = requests.get(url, timeout=15)
        return r.json() if r.status_code == 200 else []
    except: return []

def safe_fmt(val):
    v = float(val) if val is not None else 0.0
    arr, cls = ("▲", "up") if v > 0 else (("▼", "down") if v < 0 else ("▬", "white"))
    return f'<span class="{cls}">{arr} {abs(v):.1f}%</span>'

CORE_IDS = ["bitcoin", "ethereum", "polygon-ecosystem-token", "virtual-protocol", "qanplatform", "chaingpt", "velas", "griffain", "vaiot", "everdome", "bloktopia", "sin-city", "robonomics-network", "unmarshal", "layerai", "nftb"]

# --- [DEPLOYMENT] ---
with st.sidebar:
    st.markdown("<h2 class='neon-glow'>🛡️ MASTER OMNI</h2>", unsafe_allow_html=True)
    key = st.text_input("Master Key", type="password")
    h_qty = st.number_input("Holdings (XRT)", 369)

if key == MASTER_KEY:
    top_150 = fetch_master_data()
    sentinel = fetch_master_data(ids=CORE_IDS)

    # 1. TOP 20 TICKER (FIXED)
    if top_150:
        t_html = "".join([f'<div class="t-card">{c["symbol"].upper()} ₹{c["current_price"]:,.0f} {safe_fmt(c.get("price_change_percentage_24h_in_currency"))}</div>' for c in (top_150[:20]*2)])
        st.markdown(f'<div class="ticker-wrap"><div class="ticker">{t_html}</div></div>', unsafe_allow_html=True)

    # 2. HEADER
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="header-box"><span style="font-size:0.7rem;">MARKET MOOD</span><br><span class="neon-glow" style="font-size:1.5rem;">74 | GREED 📈</span></div>', unsafe_allow_html=True)
    with c2: 
        mcap_chg = top_150[0].get('price_change_percentage_24h_in_currency', 0) if top_150 else 0
        st.markdown(f'<div class="header-box"><span style="font-size:0.7rem;">GLOBAL CAP</span><br><span class="neon-glow" style="font-size:1.5rem;">₹215.4T {safe_fmt(mcap_chg)}</span></div>', unsafe_allow_html=True)
    with c3:
        x_coin = next((i for i in sentinel if i["id"] == "robonomics-network"), None)
        val = (x_coin['current_price'] * h_qty) if x_coin else 0
        st.markdown(f'<div class="header-box"><span style="font-size:0.7rem;">XRT RESERVE</span><br><span class="neon-glow" style="font-size:1.5rem;">₹{val:,.2f}</span></div>', unsafe_allow_html=True)

    # 3. RADAR - 11 INDICES
    st.markdown(f"""<div class="radar-grid">
        <div class="radar-box">NIFTY: {safe_fmt(0.8)}</div><div class="radar-box">S&P500: {safe_fmt(1.1)}</div>
        <div class="radar-box">NASDAQ: {safe_fmt(1.4)}</div><div class="radar-box">DAX 40: {safe_fmt(0.9)}</div>
        <div class="radar-box">NIKKEI: {safe_fmt(-0.3)}</div><div class="radar-box">HANG S: {safe_fmt(-0.8)}</div>
        <div class="radar-box">KOSPI: {safe_fmt(0.6)}</div><div class="radar-box">FTSE: {safe_fmt(0.2)}</div>
        <div class="radar-box">DOW J: {safe_fmt(0.5)}</div><div class="radar-box">SENSEX: {safe_fmt(0.7)}</div>
        <div class="radar-box">SHANGHAI: {safe_fmt(0.1)}</div>
    </div>""", unsafe_allow_html=True)

    # 4. SENTINEL ALPHA (STRICT 36vh CHAMBER)
    st.markdown("<h3 class='neon-glow' style='font-size:1rem;'>🛰️ Sentinel Alpha Command</h3>", unsafe_allow_html=True)
    st.markdown('<div class="chamber-lock">', unsafe_allow_html=True)
    cols = st.columns(3)
    for idx, c in enumerate(sentinel):
        with cols[idx % 3]:
            p_24h = float(c.get('price_change_percentage_24h_in_currency') or 0.0)
            whale = "🐋" if abs(p_24h) > 4.5 else ""
            st.markdown(f"""<div class="node-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <b style="color:#00FF00; font-size:1rem;">{c.get('name','').upper()}</b>
                    <img src="{c.get('image','')}" width="25" style="border-radius:50%;"> {whale}
                </div>
                <h2 style="margin:5px 0; font-size:1.2rem;">₹{c.get('current_price',0):,.2f}</h2>
                <div style="display:grid; grid-template-columns: 1fr 1fr; font-size:0.7rem; gap:5px;">
                    <div>24H: {safe_fmt(p_24h)}</div><div>7D: {safe_fmt(c.get('price_change_percentage_7d_in_currency'))}</div>
                    <div>30D: {safe_fmt(c.get('price_change_percentage_30d_in_currency'))}</div><div>90D: {safe_fmt(c.get('price_change_percentage_200d_in_currency'))}</div>
                </div>
            </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 5. GLOBAL MEGA NODE (STRICT 30vh CHAMBER)
    st.markdown("<h3 class='neon-glow' style='font-size:1rem;'>🌍 Global Mega Node (Top 150)</h3>", unsafe_allow_html=True)
    st.markdown('<div class="chamber-lock" style="height:30vh !important;">', unsafe_allow_html=True)
    if top_150:
        df = pd.DataFrame([{
            "Rank": i["market_cap_rank"], "Logo": i["image"], "Asset": i["name"], 
            "Price": f"₹{i['current_price']:,.2f}", 
            "24H": i.get("price_change_percentage_24h_in_currency"),
            "7D": i.get("price_change_percentage_7d_in_currency"),
            "30D": i.get("price_change_percentage_30d_in_currency"),
            "90D": i.get("price_change_percentage_200d_in_currency")
        } for i in top_150])
        st.write(df.to_html(escape=False, formatters={"Logo": lambda x: f'<img src="{x}" width="18">',"24H": safe_fmt, "7D": safe_fmt, "30D": safe_fmt, "90D": safe_fmt}, index=False), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("🔒 Sovereign Master, authentication required to reveal the Singularity.")
        
