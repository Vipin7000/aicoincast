import streamlit as st
import pandas as pd
import requests
from streamlit_autorefresh import st_autorefresh

# --- [1. MASTER CONFIG & FINAL DESIGN] ---
st.set_page_config(page_title="AiCoincast v11.0 Eternal", layout="wide", initial_sidebar_state="collapsed")
MASTER_KEY = "SAMASTIPUR@2026"
st_autorefresh(interval=60000, key="eternal_sync")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@400;700&display=swap');
    
    /* TOTAL UI RECOVERY - PREVENTS BLANK SCREEN */
    html, body, [data-testid="stAppViewContainer"], .main { 
        background: #020105 !important; color: white !important; 
        overflow: hidden !important; height: 100vh !important; margin: 0 !important; padding: 0 !important;
    }

    /* 1. TOP 20 TICKER - FIXED SILVER NEON */
    .ticker-wrap { 
        width: 100vw !important; background: #000; border-bottom: 1px solid #444; 
        padding: 10px 0; position: fixed; top: 0 !important; left: 0 !important; z-index: 999999 !important;
    }
    .ticker { display: flex; white-space: nowrap; animation: ticker 25s linear infinite; }
    .t-card { flex-shrink: 0; padding: 0 35px; border-right: 1px solid #333; font-weight: bold; color: #D1D1D1 !important; font-size: 1rem; }
    @keyframes ticker { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }

    /* DYNAMIC ANALOG GAUGE - FIXED VISIBILITY */
    .header-box { background: rgba(255, 255, 255, 0.02); border: 1px solid #00FF00; border-radius: 12px; padding: 10px; text-align: center; height: 130px; display: flex; flex-direction: column; justify-content: center; align-items: center; position: relative; }
    .gauge-container { position: relative; width: 140px; height: 70px; overflow: hidden; }
    .gauge-bg { position: absolute; width: 140px; height: 140px; border-radius: 50%; border: 12px solid #333; clip-path: inset(0 0 50% 0); }
    .gauge-color { position: absolute; width: 140px; height: 140px; border-radius: 50%; border: 12px solid; clip-path: inset(0 0 50% 0); transition: 1.5s; }
    .gauge-needle { position: absolute; width: 3px; height: 50px; background: white; bottom: 0; left: 50%; transform-origin: bottom center; transition: 2s; z-index: 200 !important; }
    .mood-label { font-family: 'Orbitron'; font-weight: bold; font-size: 1.1rem; z-index: 300 !important; margin-top: 5px; }
    .neon-glow { color: #00FF00; text-shadow: 0 0 10px #00FF00; font-family: 'Orbitron'; font-weight: bold; }

    /* SIDEBAR LOCK - PREVENTS GAYAB OPTION */
    [data-testid="stSidebar"] { width: 300px !important; background-color: #0a0a0a !important; border-right: 1px solid #333 !important; }
    
    /* CONTENT SPACING TO PREVENT BLANK SCREEN */
    .main-content { margin-top: 60px !important; }

    /* RADAR GRID */
    .radar-grid { 
        display: grid; grid-template-columns: repeat(auto-fit, minmax(125px, 1fr)); 
        gap: 8px; padding: 10px; border: 1px solid #333; background: rgba(255,255,255,0.02); 
        border-radius: 10px; margin-bottom: 10px;
    }
    .radar-box { text-align: center; font-size: 0.85rem; font-weight: bold; color: white; border-right: 1px solid #222; }

    /* THE ETERNAL CHAMBERS */
    .chamber-lock { 
        height: 320px !important; overflow-y: scroll !important; overflow-x: hidden !important;
        border: 1px solid #333; padding: 12px; border-radius: 12px; 
        background: rgba(0,0,0,0.5); display: block; width: 100%; box-sizing: border-box;
    }
    .chamber-lock::-webkit-scrollbar { width: 4px; }
    .chamber-lock::-webkit-scrollbar-thumb { background: #00FF00; border-radius: 10px; }

    .node-card { background: rgba(255, 255, 255, 0.03); border-radius: 10px; padding: 12px; border-left: 4px solid #00FF00; margin-bottom: 10px; }
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
    v = float(val or 0.0)
    arr, cls = ("▲", "up") if v > 0 else (("▼", "down") if v < 0 else ("▬", "white"))
    return f'<span class="{cls}">{arr} {abs(v):.1f}%</span>'

CORE_IDS = ["bitcoin", "ethereum", "polygon-ecosystem-token", "virtual-protocol", "qanplatform", "chaingpt", "velas", "griffain", "vaiot", "everdome", "bloktopia", "sin-city", "robonomics-network", "unmarshal", "layerai", "nftb"]

# --- [DEPLOYMENT] ---
with st.sidebar:
    st.markdown("<h2 class='neon-glow'>ZENITH COMMAND</h2>", unsafe_allow_html=True)
    auth = (st.text_input("Master Key", type="password") == MASTER_KEY)
    h_qty = st.number_input("Holdings (XRT)", 369)
    st.markdown("---")
    st.info("Sovereign Master, sidebar is locked for stability.")

if auth:
    top_150 = fetch_master_data()
    sentinel = fetch_master_data(ids=CORE_IDS)

    # 1. TOP 20 TICKER (SILVER/WHITE)
    if top_150:
        t_html = "".join([f'<div class="t-card">{c["symbol"].upper()} ₹{c["current_price"]:,.0f} {safe_fmt(c.get("price_change_percentage_24h_in_currency"))}</div>' for c in (top_150[:20]*2)])
        st.markdown(f'<div class="ticker-wrap"><div class="ticker">{t_html}</div></div>', unsafe_allow_html=True)

    # MAIN CONTENT WRAPPER
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # 2. HEADER
    c1, c2, c3 = st.columns(3)
    with c1:
        p_avg = sum([float(c.get('price_change_percentage_24h_in_currency') or 0) for c in top_150[:10]]) / 10
        mood_score = 50 + (p_avg * 15)
        mood_score = max(10, min(90, mood_score))
        
        if mood_score < 42: mood_lab, mood_col = "FEAR", "#FF4B4B"
        elif mood_score > 58: mood_lab, mood_col = "GREED", "#00FF00"
        else: mood_lab, mood_col = "NEUTRAL", "#FFFF00"
        
        n_rot = (mood_score / 100 * 180) - 90
        
        st.markdown(f"""
        <div class="header-box">
            <div class="gauge-container">
                <div class="gauge-bg"></div>
                <div class="gauge-color" style="border-color: {mood_col} {mood_col} #333 #333; transform: rotate(45deg);"></div>
                <div class="gauge-needle" style="transform: rotate({n_rot}deg);"></div>
            </div>
            <div class="mood-label" style="color:{mood_col};">{mood_lab}</div>
        </div>""", unsafe_allow_html=True)

    with c2: st.markdown(f'<div class="header-box"><span style="font-size:0.7rem; opacity:0.6;">GLOBAL CAP</span><br><span class="neon-glow" style="font-size:1.7rem;">₹215.4T {safe_fmt(p_avg)}</span></div>', unsafe_allow_html=True)
    with c3:
        x_coin = next((i for i in sentinel if i["id"] == "robonomics-network"), None)
        val = (x_coin['current_price'] * h_qty) if x_coin else 0
        st.markdown(f'<div class="header-box"><span style="font-size:0.7rem; opacity:0.6;">XRT VAULT</span><br><span class="neon-glow" style="font-size:1.7rem;">₹{val:,.2f}</span></div>', unsafe_allow_html=True)

    # 3. RADAR Grid
    st.markdown(f"""<div class="radar-grid">
        <div class="radar-box">NIFTY: {safe_fmt(0.8)}</div><div class="radar-box">SENSEX: {safe_fmt(0.7)}</div>
        <div class="radar-box">S&P500: {safe_fmt(1.1)}</div><div class="radar-box">NASDAQ: {safe_fmt(1.4)}</div>
        <div class="radar-box">DAX 40: {safe_fmt(0.9)}</div><div class="radar-box">NIKKEI: {safe_fmt(-0.3)}</div>
        <div class="radar-box">HANG S: {safe_fmt(-0.8)}</div><div class="radar-box">KOSPI: {safe_fmt(0.6)}</div>
        <div class="radar-box">SHANGHAI: {safe_fmt(0.1)}</div>
    </div>""", unsafe_allow_html=True)

    # 4. SENTINEL ALPHA
    st.markdown("<span style='font-size:0.9rem; font-weight:bold; color:#00FF00; font-family:Orbitron;'>🛰️ ALPHA COMMAND</span>", unsafe_allow_html=True)
    st.markdown('<div class="chamber-lock">', unsafe_allow_html=True)
    cols = st.columns(3)
    for idx, c in enumerate(sentinel):
        with cols[idx % 3]:
            st.markdown(f"""<div class="node-card">
                <div style="display:flex; justify-content:space-between;">
                    <b style="color:#00FF00;">{c.get('name','').upper()}</b>
                    <img src="{c.get('image','')}" width="20">
                </div>
                <h3 style="margin:5px 0;">₹{c.get('current_price',0):,.2f}</h3>
                <div style="display:grid; grid-template-columns: 1fr 1fr; font-size:0.65rem; gap:4px;">
                    <div>24H: {safe_fmt(c.get('price_change_percentage_24h_in_currency'))}</div><div>7D: {safe_fmt(c.get('price_change_percentage_7d_in_currency'))}</div>
                </div>
            </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 5. GLOBAL MEGA NODE
    st.markdown("<span style='font-size:0.9rem; font-weight:bold; color:#00FF00; font-family:Orbitron;'>🌍 GLOBAL NODE</span>", unsafe_allow_html=True)
    st.markdown('<div class="chamber-lock" style="height:220px !important;">', unsafe_allow_html=True)
    if top_150:
        df = pd.DataFrame([{"Rank": i["market_cap_rank"], "Asset": i["name"], "Price": f"₹{i['current_price']:,.2f}", "24H": i.get("price_change_percentage_24h_in_currency"), "7D": i.get("price_change_percentage_7d_in_currency")} for i in top_150])
        st.write(df.to_html(escape=False, formatters={"24H": safe_fmt, "7D": safe_fmt}, index=False), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("🔒 Sovereign Master, authentication required.")
    
