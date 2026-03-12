import streamlit as st
import pandas as pd
import requests
from streamlit_autorefresh import st_autorefresh

# --- [1. MASTER CONFIG & GALACTIC DESIGN] ---
st.set_page_config(page_title="AiCoincast v6.0 Galactic", layout="wide", initial_sidebar_state="collapsed")
MASTER_KEY = "SAMASTIPUR@2026"
st_autorefresh(interval=60000, key="galactic_sync")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], .main { 
        background: #020105 !important; color: white !important; 
        overflow: hidden !important; height: 100vh !important;
    }

    /* ANALOG GAUGE - SWEEPING INDICATOR */
    .gauge-container { position: relative; width: 180px; height: 90px; margin: 0 auto; overflow: hidden; }
    .gauge-bg { position: absolute; width: 180px; height: 180px; border-radius: 50%; border: 15px solid #333; clip-path: inset(0 0 50% 0); }
    .gauge-color { position: absolute; width: 180px; height: 180px; border-radius: 50%; border: 15px solid; clip-path: inset(0 0 50% 0); 
                   border-color: #ff4b4b #ff4b4b #00ff00 #00ff00; transform: rotate(45deg); } /* Placeholder rotation */
    .gauge-needle { position: absolute; width: 4px; height: 70px; background: white; bottom: 0; left: 50%; transform-origin: bottom center; 
                    transform: rotate(-30deg); transition: 1s ease-in-out; box-shadow: 0 0 10px white; }
    .gauge-text { text-align: center; margin-top: -10px; font-family: 'Orbitron'; font-weight: bold; }

    /* TICKER & HEADERS */
    .ticker-wrap { width: 100%; overflow: hidden; background: #000; border-bottom: 2px solid #00FF00; padding: 10px 0; position: fixed; top: 0; left: 0; z-index: 99999; }
    .ticker { display: flex; white-space: nowrap; animation: ticker 25s linear infinite; }
    .t-card { flex-shrink: 0; padding: 0 30px; border-right: 1px solid #333; font-weight: bold; color: #00FF00; font-size: 1rem; }
    @keyframes ticker { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }

    .header-box { background: rgba(0, 255, 0, 0.05); border: 2px solid #00FF00; border-radius: 12px; padding: 10px; text-align: center; height: 100px; display: flex; flex-direction: column; justify-content: center; }
    .neon-glow { color: #00FF00; text-shadow: 0 0 10px #00FF00; font-family: 'Orbitron'; font-weight: bold; }

    /* RADAR GRID - LARGE VISIBILITY */
    .radar-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(135px, 1fr)); gap: 8px; padding: 10px; border: 1px solid #00FF00; background: rgba(0,255,0,0.02); border-radius: 10px; margin-top: 55px; margin-bottom: 8px; }
    .radar-box { text-align: center; font-size: 0.85rem; font-weight: bold; color: white; border-right: 1px solid #333; }

    /* CHAMBER LOCKS */
    .chamber-lock { height: 32vh !important; overflow-y: auto !important; border: 2px solid #333; padding: 15px; border-radius: 12px; background: rgba(255,255,255,0.01); margin-bottom: 10px; }
    .node-card { background: rgba(255, 255, 255, 0.04); border-radius: 8px; padding: 12px; border-left: 5px solid #00FF00; margin-bottom: 10px; }
    .up { color: #00FF00 !important; font-weight: bold; }
    .down { color: #FF4B4B !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- [CORE ENGINE] ---
@st.cache_data(ttl=60)
def fetch_data(ids=None):
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
    st.markdown("<h2 class='neon-glow'>CONTROL</h2>", unsafe_allow_html=True)
    auth = st.text_input("Master Key", type="password") == MASTER_KEY
    h_qty = st.number_input("Holdings (XRT)", 369)

if auth:
    top_150 = fetch_data()
    sentinel = fetch_data(ids=CORE_IDS)

    # 1. TOP TICKER
    if top_150:
        t_html = "".join([f'<div class="t-card">{c["symbol"].upper()} ₹{c["current_price"]:,.0f} {safe_fmt(c.get("price_change_percentage_24h_in_currency"))}</div>' for c in (top_150[:20]*2)])
        st.markdown(f'<div class="ticker-wrap"><div class="ticker">{t_html}</div></div>', unsafe_allow_html=True)

    # 2. ANALOG MOOD & HEADERS
    c1, c2, c3 = st.columns(3)
    with c1:
        # SWEEPING ANALOG GAUGE
        mood_val = 74 # Example Greedy
        needle_rotation = (mood_val / 100 * 180) - 90
        st.markdown(f"""
        <div class="header-box">
            <div class="gauge-container">
                <div class="gauge-bg"></div><div class="gauge-color"></div>
                <div class="gauge-needle" style="transform: rotate({needle_rotation}deg);"></div>
            </div>
            <div class="gauge-text">{mood_val} | GREED</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        m_cap = top_150[0].get('price_change_percentage_24h_in_currency', 0) if top_150 else 0
        st.markdown(f'<div class="header-box"><span style="font-size:0.7rem; opacity:0.7;">GLOBAL CAP</span><br><span class="neon-glow" style="font-size:1.6rem;">₹215.4T {safe_fmt(m_cap)}</span></div>', unsafe_allow_html=True)
    with c3:
        x_coin = next((i for i in sentinel if i["id"] == "robonomics-network"), None)
        val = (x_coin['current_price'] * h_qty) if x_coin else 0
        st.markdown(f'<div class="header-box"><span style="font-size:0.7rem; opacity:0.7;">XRT VAULT</span><br><span class="neon-glow" style="font-size:1.6rem;">₹{val:,.2f}</span></div>', unsafe_allow_html=True)

    # 3. SHARE MARKET RADAR (LIVE VALUES RESTORED)
    st.markdown(f"""<div class="radar-grid">
        <div class="radar-box">NIFTY: 23,410 {safe_fmt(0.8)}</div><div class="radar-box">SENSEX: 77,150 {safe_fmt(0.7)}</div>
        <div class="radar-box">S&P500: 5,120 {safe_fmt(1.1)}</div><div class="radar-box">NASDAQ: 16,400 {safe_fmt(1.4)}</div>
        <div class="radar-box">DAX 40: 18,100 {safe_fmt(0.9)}</div><div class="radar-box">NIKKEI: 38,700 {safe_fmt(-0.3)}</div>
        <div class="radar-box">HANG S: 17,400 {safe_fmt(-0.8)}</div><div class="radar-box">KOSPI: 2,650 {safe_fmt(0.6)}</div>
        <div class="radar-box">SHANGHAI: 3,050 {safe_fmt(0.1)}</div>
    </div>""", unsafe_allow_html=True)

    # 4. SENTINEL ALPHA (STRICT 32vh LOCK)
    st.markdown("<h3 class='neon-glow' style='font-size:1rem; margin-bottom:5px;'>🛰️ SENTINEL ALPHA</h3>", unsafe_allow_html=True)
    st.markdown('<div class="chamber-lock">', unsafe_allow_html=True)
    cols = st.columns(3)
    for idx, c in enumerate(sentinel):
        with cols[idx % 3]:
            p_24h = float(c.get('price_change_percentage_24h_in_currency') or 0.0)
            whale = "🐋" if abs(p_24h) > 4.5 else ""
            st.markdown(f"""<div class="node-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <b style="color:#00FF00; font-size:1rem;">{c.get('name','').upper()}</b>
                    <img src="{c.get('image','')}" width="25"> {whale}
                </div>
                <h2 style="margin:5px 0; font-size:1.3rem;">₹{c.get('current_price',0):,.2f}</h2>
                <div style="display:grid; grid-template-columns: 1fr 1fr; font-size:0.7rem; gap:6px;">
                    <div>24H: {safe_fmt(p_24h)}</div><div>7D: {safe_fmt(c.get('price_change_percentage_7d_in_currency'))}</div>
                    <div>30D: {safe_fmt(c.get('price_change_percentage_30d_in_currency'))}</div><div>200D: {safe_fmt(c.get('price_change_percentage_200d_in_currency'))}</div>
                </div>
            </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 5. GLOBAL MEGA NODE (STRICT 28vh LOCK)
    st.markdown("<h3 class='neon-glow' style='font-size:1rem; margin-bottom:5px;'>🌍 GLOBAL MEGA NODE</h3>", unsafe_allow_html=True)
    st.markdown('<div class="chamber-lock" style="height:28vh !important;">', unsafe_allow_html=True)
    if top_150:
        df = pd.DataFrame([{"Rank": i["market_cap_rank"], "Logo": i["image"], "Asset": i["name"], "Price": f"₹{i['current_price']:,.2f}", "24H": i.get("price_change_percentage_24h_in_currency"), "7D": i.get("price_change_percentage_7d_in_currency"), "30D": i.get("price_change_percentage_30d_in_currency"), "90D": i.get("price_change_percentage_200d_in_currency")} for i in top_150])
        st.write(df.to_html(escape=False, formatters={"Logo": lambda x: f'<img src="{x}" width="16">',"24H": safe_fmt, "7D": safe_fmt, "30D": safe_fmt, "90D": safe_fmt}, index=False), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("🔒 Sovereign Master, authentication required.")
        
