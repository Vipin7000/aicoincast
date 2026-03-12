import streamlit as st
import pandas as pd
import requests
from streamlit_autorefresh import st_autorefresh

# --- [1. MASTER CONFIG & APEX DESIGN] ---
st.set_page_config(page_title="AiCoincast v11.5 Apex", layout="wide", initial_sidebar_state="expanded")
MASTER_KEY = "SAMASTIPUR@2026"
st_autorefresh(interval=60000, key="apex_sync")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@400;700&display=swap');
    
    /* TOTAL UI LOCKDOWN - PREVENTS VERTICAL LEAKS */
    html, body, [data-testid="stAppViewContainer"], .main { 
        background: #020105 !important; color: white !important; 
        overflow: hidden !important; height: 100vh !important; margin: 0 !important; padding: 0 !important;
    }

    /* 1. TOP 20 TICKER - THE SILVER STEAL LOCK */
    .ticker-wrap { 
        width: 100% !important; background: #000; border-bottom: 2px solid #444; 
        padding: 10px 0; position: fixed; top: 0 !important; left: 0 !important; z-index: 99999 !important;
    }
    .ticker { display: flex; white-space: nowrap; animation: ticker 25s linear infinite; }
    .t-card { flex-shrink: 0; padding: 0 35px; border-right: 1px solid #333; font-weight: bold; color: #D1D1D1 !important; font-size: 1rem; }
    @keyframes ticker { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }

    /* HEADER BOXES - PREDATOR COLORS */
    .header-box { background: rgba(255, 255, 255, 0.02); border: 2px solid #444; border-radius: 12px; padding: 10px; text-align: center; height: 120px; display: flex; flex-direction: column; justify-content: center; align-items: center; }
    .neon-gold { color: #FFD700; text-shadow: 0 0 10px #FFD700; font-family: 'Orbitron'; font-weight: bold; }
    .neon-silver { color: #C0C0C0; text-shadow: 0 0 10px #C0C0C0; font-family: 'Orbitron'; font-weight: bold; }

    /* RADAR GRID - FIXED 11 INDICES */
    .radar-grid { 
        display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); 
        gap: 8px; padding: 10px; border: 1px solid #00FF00; background: rgba(0,255,0,0.02); 
        border-radius: 10px; margin-top: 65px !important; margin-bottom: 10px;
    }
    .radar-box { text-align: center; font-size: 0.85rem; font-weight: bold; color: white; border-right: 1px solid #333; }

    /* CHAMBER LOCK - ABSOLUTE PIXEL JAIL */
    .chamber-lock { 
        height: 320px !important; overflow-y: scroll !important; overflow-x: hidden !important;
        border: 2px solid #333; padding: 15px; border-radius: 15px; 
        background: rgba(255,255,255,0.01); display: block; width: 100%; box-sizing: border-box;
    }
    .chamber-lock::-webkit-scrollbar { width: 5px; }
    .chamber-lock::-webkit-scrollbar-thumb { background: #00FF00; border-radius: 10px; }

    .node-card { background: rgba(255, 255, 255, 0.04); border-radius: 10px; padding: 15px; border-left: 5px solid #00FF00; margin-bottom: 12px; width: 98% !important; }
    
    [data-testid="stSidebar"] { z-index: 100000 !important; background-color: #0a0a0a !important; }
    
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
    st.markdown("<h3 style='color:#00FF00; font-family:Orbitron;'>ZENITH CMD</h3>", unsafe_allow_html=True)
    auth = (st.text_input("Master Key", type="password") == MASTER_KEY)
    h_qty = st.number_input("Holdings (XRT)", 369)
    st.markdown("---")
    st.info("Sovereign Master, terminal status: APEX ACTIVE")

if auth:
    top_150 = fetch_master_data()
    sentinel = fetch_master_data(ids=CORE_IDS)

    # 1. TOP 20 TICKER (SILVER LOCK)
    if top_150:
        t_html = "".join([f'<div class="t-card">{c["symbol"].upper()} ₹{c["current_price"]:,.0f} {safe_fmt(c.get("price_change_percentage_24h_in_currency"))}</div>' for c in (top_150[:20]*2)])
        st.markdown(f'<div class="ticker-wrap"><div class="ticker">{t_html}</div></div>', unsafe_allow_html=True)

    # 2. DYNAMIC HEADER
    c1, c2, c3 = st.columns(3)
    with c1:
        p_avg = sum([float(c.get('price_change_percentage_24h_in_currency') or 0) for c in top_150[:10]]) / 10 if top_150 else 0
        mood = "GREED" if p_avg > 0 else "FEAR"
        st.markdown(f"""<div class="header-box">
            <span style="font-size:0.7rem; opacity:0.6;">MOOD</span>
            <div style="font-size:1.6rem; font-weight:bold; color:#00FF00;">{mood}</div>
            <div style="font-size:0.9rem;">{safe_fmt(p_avg)}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="header-box"><span style="font-size:0.7rem; opacity:0.6;">GLOBAL CAP</span><br><span class="neon-gold" style="font-size:1.6rem;">₹215.4T</span><br>{safe_fmt(p_avg)}</div>', unsafe_allow_html=True)
    with c3:
        x_coin = next((i for i in sentinel if i["id"] == "robonomics-network"), None)
        val = (x_coin['current_price'] * h_qty) if x_coin else 0
        st.markdown(f'<div class="header-box"><span style="font-size:0.7rem; opacity:0.6;">XRT RESERVE</span><br><span class="neon-silver" style="font-size:1.6rem;">₹{val:,.0f}</span></div>', unsafe_allow_html=True)

    # 3. RADAR Grid - FIXED 11 INDICES
    st.markdown(f"""<div class="radar-grid">
        <div class="radar-box">NIFTY: 23,410<br>{safe_fmt(0.8)}</div><div class="radar-box">SENSEX: 77,150<br>{safe_fmt(0.7)}</div>
        <div class="radar-box">S&P500: 5,120<br>{safe_fmt(1.1)}</div><div class="radar-box">NASDAQ: 16,400<br>{safe_fmt(1.4)}</div>
        <div class="radar-box">DAX 40: 18,100<br>{safe_fmt(0.9)}</div><div class="radar-box">NIKKEI: 38,700<br>{safe_fmt(-0.3)}</div>
        <div class="radar-box">HANG S: 17,400<br>{safe_fmt(-0.8)}</div><div class="radar-box">KOSPI: 2,650<br>{safe_fmt(0.6)}</div>
        <div class="radar-box">SHANGHAI: 3,050<br>{safe_fmt(0.1)}</div><div class="radar-box">DOW J: 39,200<br>{safe_fmt(0.5)}</div><div class="radar-box">FTSE: 8,250<br>{safe_fmt(0.2)}</div>
    </div>""", unsafe_allow_html=True)

    # 4. SENTINEL ALPHA (STRICT PIXEL LOCK)
    st.markdown("<h3 style='color:#00FF00; font-family:Orbitron; font-size:1rem; margin-bottom:5px;'>🛰️ ALPHA COMMAND</h3>", unsafe_allow_html=True)
    st.markdown('<div class="chamber-lock">', unsafe_allow_html=True)
    cols = st.columns(3)
    for idx, c in enumerate(sentinel):
        with cols[idx % 3]:
            st.markdown(f"""<div class="node-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <b style="color:#00FF00; font-size:1rem;">{c.get('name','').upper()}</b>
                    <img src="{c.get('image','')}" width="25" style="border-radius:50%;">
                </div>
                <h2 style="margin:5px 0; font-size:1.4rem;">₹{c.get('current_price',0):,.2f}</h2>
                <div style="display:grid; grid-template-columns: 1fr 1fr; font-size:0.75rem; gap:8px;">
                    <div>24H: {safe_fmt(c.get('price_change_percentage_24h_in_currency'))}</div>
                    <div>7D: {safe_fmt(c.get('price_change_percentage_7d_in_currency'))}</div>
                </div>
            </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 5. GLOBAL MEGA NODE (STRICT PIXEL LOCK)
    st.markdown("<h3 style='color:#00FF00; font-family:Orbitron; font-size:1rem; margin-bottom:5px;'>🌍 GLOBAL NODE (TOP 150)</h3>", unsafe_allow_html=True)
    st.markdown('<div class="chamber-lock" style="height:250px !important;">', unsafe_allow_html=True)
    if top_150:
        df = pd.DataFrame([{"Rank": i["market_cap_rank"], "Asset": i["name"], "Price": f"₹{i['current_price']:,.2f}", "24H": i.get("price_change_percentage_24h_in_currency"), "7D": i.get("price_change_percentage_7d_in_currency")} for i in top_150])
        st.write(df.to_html(escape=False, formatters={"24H": safe_fmt, "7D": safe_fmt}, index=False), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("🔒 Sovereign Master, authentication required to reveal the Singularity Apex.")
                           
