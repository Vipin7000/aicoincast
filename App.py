import streamlit as st
import pandas as pd
import requests
from streamlit_autorefresh import st_autorefresh

# --- [1. MASTER CONFIG & APEX DESIGN] ---
st.set_page_config(page_title="AiCoincast v10.1 Apex", layout="wide", initial_sidebar_state="collapsed")
MASTER_KEY = "SAMASTIPUR@2026"
st_autorefresh(interval=60000, key="apex_sync")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@400;700&display=swap');
    
    /* TOTAL UI OVERRIDE */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main { 
        background: #020105 !important; color: white !important; 
        overflow: hidden !important; height: 100vh !important; margin: 0 !important; padding: 0 !important;
    }

    /* 1. TOP 20 TICKER - CHANGED TO NEON SILVER/WHITE */
    .ticker-wrap { 
        width: 100vw !important; background: #000; border-bottom: 2px solid #444; 
        padding: 10px 0; position: fixed; top: 0 !important; left: 0 !important; z-index: 999999 !important;
    }
    .ticker { display: flex; white-space: nowrap; animation: ticker 25s linear infinite; }
    .t-card { 
        flex-shrink: 0; padding: 0 35px; border-right: 1px solid #333; 
        font-weight: bold; color: #E0E0E0 !important; font-size: 1rem; 
    }
    @keyframes ticker { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }

    /* DYNAMIC ANALOG GAUGE */
    .header-box { background: rgba(255, 255, 255, 0.03); border: 2px solid #00FF00; border-radius: 12px; padding: 10px; text-align: center; height: 135px; display: flex; flex-direction: column; justify-content: center; align-items: center; position: relative; }
    .gauge-container { position: relative; width: 140px; height: 70px; overflow: hidden; margin-bottom: 5px; }
    .gauge-bg { position: absolute; width: 140px; height: 140px; border-radius: 50%; border: 12px solid #333; clip-path: inset(0 0 50% 0); }
    .gauge-color { position: absolute; width: 140px; height: 140px; border-radius: 50%; border: 12px solid; clip-path: inset(0 0 50% 0); transition: 1.5s ease-in-out; }
    .gauge-needle { position: absolute; width: 3px; height: 55px; background: white; bottom: 0; left: 50%; transform-origin: bottom center; transition: 2s; z-index: 200 !important; box-shadow: 0 0 8px white; }
    .mood-label { position: relative; z-index: 300 !important; font-family: 'Orbitron'; font-weight: bold; font-size: 1.1rem; margin-top: 2px; }
    .neon-glow { color: #00FF00; text-shadow: 0 0 10px #00FF00; font-family: 'Orbitron'; font-weight: bold; }

    /* SIDEBAR COLLAPSE ICON & DRAG FIX */
    [data-testid="stSidebar"] { background-color: #0a0a0a !important; }
    [data-testid="stSidebarNav"] { display: block !important; }
    
    /* RADAR GRID */
    .radar-grid { 
        display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); 
        gap: 8px; padding: 10px; border: 1px solid #444; background: rgba(255,255,255,0.02); 
        border-radius: 10px; margin-top: 60px !important; margin-bottom: 10px;
    }
    .radar-box { text-align: center; font-size: 0.85rem; font-weight: bold; color: white; border-right: 1px solid #333; }

    /* THE APEX CHAMBERS */
    .chamber-lock { 
        height: 330px !important; overflow-y: scroll !important; overflow-x: hidden !important;
        border: 1px solid #333; padding: 15px; border-radius: 15px; 
        background: rgba(255,255,255,0.01); display: block; width: 100%; box-sizing: border-box;
    }
    .chamber-lock::-webkit-scrollbar { width: 4px; }
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
    v = float(val or 0.0)
    arr, cls = ("▲", "up") if v > 0 else (("▼", "down") if v < 0 else ("▬", "white"))
    return f'<span class="{cls}">{arr} {abs(v):.1f}%</span>'

CORE_IDS = ["bitcoin", "ethereum", "polygon-ecosystem-token", "virtual-protocol", "qanplatform", "chaingpt", "velas", "griffain", "vaiot", "everdome", "bloktopia", "sin-city", "robonomics-network", "unmarshal", "layerai", "nftb"]

# --- [DEPLOYMENT] ---
with st.sidebar:
    st.markdown("<h3 class='neon-glow'>ZENITH COMMAND</h3>", unsafe_allow_html=True)
    auth = (st.text_input("Master Key", type="password") == MASTER_KEY)
    h_qty = st.number_input("Holdings (XRT)", 369)
    st.markdown("---")
    st.info("Sovereign Master, use the arrow at top left to collapse this panel.")

if auth:
    top_150 = fetch_master_data()
    sentinel = fetch_master_data(ids=CORE_IDS)

    # 1. TOP 20 TICKER (SILVER/WHITE ACCENT)
    if top_150:
        t_html = "".join([f'<div class="t-card">{c["symbol"].upper()} ₹{c["current_price"]:,.0f} {safe_fmt(c.get("price_change_percentage_24h_in_currency"))}</div>' for c in (top_150[:20]*2)])
        st.markdown(f'<div class="ticker-wrap"><div class="ticker">{t_html}</div></div>', unsafe_allow_html=True)

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
            <div style="font-size:0.6rem; opacity:0.6; letter-spacing:1px; margin-bottom:5px;">MARKET SENTIMENT</div>
            <div class="gauge-container">
                <div class="gauge-bg"></div>
                <div class="gauge-color" style="border-color: {mood_col} {mood_col} #333 #333; transform: rotate(45deg);"></div>
                <div class="gauge-needle" style="transform: rotate({n_rot}deg);"></div>
            </div>
            <div class="mood-label" style="color:{mood_col};">{int(mood_score)} | {mood_lab}</div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f'<div class="header-box"><span style="font-size:0.7rem; opacity:0.6;">GLOBAL MARKET CAP</span><br><span class="neon-glow" style="font-size:1.7rem;">₹215.4T {safe_fmt(p_avg)}</span></div>', unsafe_allow_html=True)
    with c3:
        x_coin = next((i for i in sentinel if i["id"] == "robonomics-network"), None)
        val = (x_coin['current_price'] * h_qty) if x_coin else 0
        st.markdown(f'<div class="header-box"><span style="font-size:0.7rem; opacity:0.6;">XRT STRATEGIC VAULT</span><br><span class="neon-glow" style="font-size:1.7rem;">₹{val:,.2f}</span></div>', unsafe_allow_html=True)

    # 3. RADAR Grid
    st.markdown(f"""<div class="radar-grid">
        <div class="radar-box">NIFTY: 23,410<br>{safe_fmt(0.8)}</div><div class="radar-box">SENSEX: 77,150<br>{safe_fmt(0.7)}</div>
        <div class="radar-box">S&P500: 5,120<br>{safe_fmt(1.1)}</div><div class="radar-box">NASDAQ: 16,400<br>{safe_fmt(1.4)}</div>
        <div class="radar-box">DOW J: 39,200<br>{safe_fmt(0.5)}</div><div class="radar-box">DAX 40: 18,100<br>{safe_fmt(0.9)}</div>
        <div class="radar-box">FTSE: 8,250<br>{safe_fmt(0.2)}</div><div class="radar-box">NIKKEI: 38,700<br>{safe_fmt(-0.3)}</div>
        <div class="radar-box">HANG S: 17,400<br>{safe_fmt(-0.8)}</div><div class="radar-box">KOSPI: 2,650<br>{safe_fmt(0.6)}</div>
        <div class="radar-box">SHANGHAI: 3,050<br>{safe_fmt(0.1)}</div>
    </div>""", unsafe_allow_html=True)

    # 4. SENTINEL ALPHA
    st.markdown("<h3 class='neon-glow' style='font-size:1rem; margin-bottom:5px;'>🛰️ SENTINEL ALPHA NODES</h3>", unsafe_allow_html=True)
    st.markdown('<div class="chamber-lock">', unsafe_allow_html=True)
    cols = st.columns(3)
    for idx, c in enumerate(sentinel):
        with cols[idx % 3]:
            p_24h = float(c.get('price_change_percentage_24h_in_currency') or 0.0)
            whale = "🐋" if abs(p_24h) > 4.5 else ""
            st.markdown(f"""<div class="node-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <b style="color:#00FF00; font-size:1.1rem;">{c.get('name','').upper()}</b>
                    <img src="{c.get('image','')}" width="25" style="border-radius:50%;"> {whale}
                </div>
                <h2 style="margin:8px 0; font-size:1.5rem;">₹{c.get('current_price',0):,.2f}</h2>
                <div style="display:grid; grid-template-columns: 1fr 1fr; font-size:0.75rem; gap:8px;">
                    <div>24H: {safe_fmt(p_24h)}</div><div>7D: {safe_fmt(c.get('price_change_percentage_7d_in_currency'))}</div>
                    <div>30D: {safe_fmt(c.get('price_change_percentage_30d_in_currency'))}</div><div>200D: {safe_fmt(c.get('price_change_percentage_200d_in_currency'))}</div>
                </div>
            </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 5. GLOBAL MEGA NODE
    st.markdown("<h3 class='neon-glow' style='font-size:1rem; margin-bottom:5px;'>🌍 GLOBAL MEGA NODE</h3>", unsafe_allow_html=True)
    st.markdown('<div class="chamber-lock" style="height:280px !important;">', unsafe_allow_html=True)
    if top_150:
        df = pd.DataFrame([{"Rank": i["market_cap_rank"], "Logo": i["image"], "Asset": i["name"], "Price": f"₹{i['current_price']:,.2f}", "24H": i.get("price_change_percentage_24h_in_currency"), "7D": i.get("price_change_percentage_7d_in_currency"), "30D": i.get("price_change_percentage_30d_in_currency"), "200D": i.get("price_change_percentage_200d_in_currency")} for i in top_150])
        st.write(df.to_html(escape=False, formatters={"Logo": lambda x: f'<img src="{x}" width="18">',"24H": safe_fmt, "7D": safe_fmt, "30D": safe_fmt, "200D": safe_fmt}, index=False), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("🔒 Sovereign Master, authentication required to reveal the Zenith Apex.")
            
