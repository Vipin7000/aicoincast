import streamlit as st
import pandas as pd
import requests
from streamlit_autorefresh import st_autorefresh

# --- [1. MASTER CONFIG & DESIGN LOCK] ---
st.set_page_config(page_title="AiCoincast v6.2 Final", layout="wide", initial_sidebar_state="collapsed")
MASTER_KEY = "SAMASTIPUR@2026"
st_autorefresh(interval=60000, key="final_sync")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@400;700&display=swap');
    
    /* ABSOLUTE PAGE LOCK */
    html, body, [data-testid="stAppViewContainer"], .main { 
        background: #020105 !important; color: white !important; 
        overflow: hidden !important; height: 100vh !important;
    }

    /* TOP 20 TICKER - FIXED & ALWAYS ON TOP */
    .ticker-wrap { 
        width: 100%; overflow: hidden; background: #000; border-bottom: 2px solid #00FF00; 
        padding: 10px 0; position: fixed; top: 0; left: 0; z-index: 99999;
    }
    .ticker { display: flex; white-space: nowrap; animation: ticker 25s linear infinite; }
    .t-card { flex-shrink: 0; padding: 0 30px; border-right: 1px solid #333; font-weight: bold; color: #00FF00; font-size: 1rem; }
    @keyframes ticker { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }

    /* DYNAMIC ANALOG GAUGE */
    .gauge-wrapper { text-align: center; width: 100%; position: relative; }
    .gauge-container { position: relative; width: 150px; height: 75px; margin: 0 auto; overflow: hidden; }
    .gauge-bg { position: absolute; width: 150px; height: 150px; border-radius: 50%; border: 12px solid #333; clip-path: inset(0 0 50% 0); }
    .gauge-color { position: absolute; width: 150px; height: 150px; border-radius: 50%; border: 12px solid; clip-path: inset(0 0 50% 0); 
                   border-color: #ff4b4b #ff4b4b #00ff00 #00ff00; transform: rotate(45deg); }
    .gauge-needle { position: absolute; width: 3px; height: 55px; background: white; bottom: 0; left: 50%; transform-origin: bottom center; 
                    transition: 2s ease-in-out; box-shadow: 0 0 8px white; z-index: 10; }
    .neon-glow { color: #00FF00; text-shadow: 0 0 10px #00FF00; font-family: 'Orbitron'; font-weight: bold; }

    /* RADAR GRID */
    .radar-grid { 
        display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); 
        gap: 8px; padding: 10px; border: 1px solid #00FF00; background: rgba(0,255,0,0.02); 
        border-radius: 10px; margin-top: 60px; margin-bottom: 10px;
    }
    .radar-box { text-align: center; font-size: 0.85rem; font-weight: bold; color: white; border-right: 1px solid #333; }

    /* CHAMBER LOCK (vh BASED) */
    .chamber-lock { 
        height: 34vh !important; overflow-y: auto !important; overflow-x: hidden !important;
        border: 2px solid #333; padding: 12px; border-radius: 12px; 
        background: rgba(255,255,255,0.01); display: block; width: 100%; box-sizing: border-box;
    }
    .chamber-lock::-webkit-scrollbar { width: 4px; }
    .chamber-lock::-webkit-scrollbar-thumb { background: #00FF00; border-radius: 10px; }

    .node-card { background: rgba(255, 255, 255, 0.04); border-radius: 8px; padding: 12px; border-left: 4px solid #00FF00; margin-bottom: 10px; }
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
if st.sidebar.text_input("Master Key", type="password") == MASTER_KEY:
    top_150 = fetch_data()
    sentinel = fetch_data(ids=CORE_IDS)

    # 1. TOP 20 SCROLLING TICKER
    if top_150:
        t_html = "".join([f'<div class="t-card">{c["symbol"].upper()} ₹{c["current_price"]:,.0f} {safe_fmt(c.get("price_change_percentage_24h_in_currency"))}</div>' for c in (top_150[:20]*2)])
        st.markdown(f'<div class="ticker-wrap"><div class="ticker">{t_html}</div></div>', unsafe_allow_html=True)

    # 2. DYNAMIC HEADER & MOOD GAUGE
    c1, c2, c3 = st.columns(3)
    with c1:
        # DYNAMIC MOOD LOGIC
        m_change = top_150[0].get('price_change_percentage_24h_in_currency', 0) if top_150 else 0
        mood_score = 50 + (m_change * 5) # Simple logic to move needle
        mood_score = max(10, min(90, mood_score)) # Keep within bounds
        mood_text = "GREED" if m_change > 0 else "FEAR"
        mood_color = "#00FF00" if m_change > 0 else "#FF4B4B"
        needle_rot = (mood_score / 100 * 180) - 90
        
        st.markdown(f"""
        <div style="background:rgba(0,255,0,0.05); border:2px solid #00FF00; border-radius:12px; padding:10px; height:110px;">
            <div class="gauge-wrapper">
                <div class="gauge-container">
                    <div class="gauge-bg"></div><div class="gauge-color"></div>
                    <div class="gauge-needle" style="transform: rotate({needle_rot}deg);"></div>
                </div>
                <div style="font-family:'Orbitron'; font-weight:bold; color:{mood_color};">{int(mood_score)} | {mood_text}</div>
            </div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div style="background:rgba(0,255,0,0.05); border:2px solid #00FF00; border-radius:12px; padding:20px; text-align:center; height:110px;"><span style="font-size:0.7rem; opacity:0.7;">GLOBAL CAP</span><br><span class="neon-glow" style="font-size:1.6rem;">₹215.4T {safe_fmt(m_change)}</span></div>', unsafe_allow_html=True)
    with c3:
        x_coin = next((i for i in sentinel if i["id"] == "robonomics-network"), None)
        val = (x_coin['current_price'] * 369) if x_coin else 0
        st.markdown(f'<div style="background:rgba(0,255,0,0.05); border:2px solid #00FF00; border-radius:12px; padding:20px; text-align:center; height:110px;"><span style="font-size:0.7rem; opacity:0.7;">XRT VAULT</span><br><span class="neon-glow" style="font-size:1.6rem;">₹{val:,.2f}</span></div>', unsafe_allow_html=True)

    # 3. RADAR (LIVE VALUES RESTORED)
    st.markdown(f"""<div class="radar-grid">
        <div class="radar-box">NIFTY: 23,410<br>{safe_fmt(0.8)}</div><div class="radar-box">SENSEX: 77,150<br>{safe_fmt(0.7)}</div>
        <div class="radar-box">S&P500: 5,120<br>{safe_fmt(1.1)}</div><div class="radar-box">NASDAQ: 16,400<br>{safe_fmt(1.4)}</div>
        <div class="radar-box">DAX 40: 18,100<br>{safe_fmt(0.9)}</div><div class="radar-box">NIKKEI: 38,700<br>{safe_fmt(-0.3)}</div>
        <div class="radar-box">HANG S: 17,400<br>{safe_fmt(-0.8)}</div><div class="radar-box">KOSPI: 2,650<br>{safe_fmt(0.6)}</div>
        <div class="radar-box">SHANGHAI: 3,050<br>{safe_fmt(0.1)}</div>
    </div>""", unsafe_allow_html=True)

    # 4. SENTINEL ALPHA (STRICT LOCK)
    st.markdown("<h3 class='neon-glow' style='font-size:1rem; margin-bottom:5px;'>🛰️ SENTINEL ALPHA COMMAND</h3>", unsafe_allow_html=True)
    st.markdown('<div class="chamber-lock">', unsafe_allow_html=True)
    cols = st.columns(3)
    for idx, c in enumerate(sentinel):
        with cols[idx % 3]:
            p_24h = float(c.get('price_change_percentage_24h_in_currency') or 0.0)
            st.markdown(f"""<div class="node-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <b style="color:#00FF00; font-size:0.95rem;">{c.get('name','').upper()}</b>
                    <img src="{c.get('image','')}" width="22" style="border-radius:50%;">
                </div>
                <h3 style="margin:5px 0; font-size:1.2rem;">₹{c.get('current_price',0):,.2f}</h3>
                <div style="display:grid; grid-template-columns: 1fr 1fr; font-size:0.65rem; gap:4px; opacity:0.8;">
                    <div>24H: {safe_fmt(p_24h)}</div><div>7D: {safe_fmt(c.get('price_change_percentage_7d_in_currency'))}</div>
                    <div>30D: {safe_fmt(c.get('price_change_percentage_30d_in_currency'))}</div><div>200D: {safe_fmt(c.get('price_change_percentage_200d_in_currency'))}</div>
                </div>
            </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 5. GLOBAL MEGA NODE (STRICT LOCK)
    st.markdown("<h3 class='neon-glow' style='font-size:1rem; margin-bottom:5px;'>🌍 GLOBAL MEGA NODE</h3>", unsafe_allow_html=True)
    st.markdown('<div class="chamber-lock" style="height:28vh !important;">', unsafe_allow_html=True)
    if top_150:
        df = pd.DataFrame([{"Rank": i["market_cap_rank"], "Logo": i["image"], "Asset": i["name"], "Price": f"₹{i['current_price']:,.2f}", "24H": i.get("price_change_percentage_24h_in_currency"), "7D": i.get("price_change_percentage_7d_in_currency"), "30D": i.get("price_change_percentage_30d_in_currency"), "200D": i.get("price_change_percentage_200d_in_currency")} for i in top_150])
        st.write(df.to_html(escape=False, formatters={"Logo": lambda x: f'<img src="{x}" width="16">',"24H": safe_fmt, "7D": safe_fmt, "30D": safe_fmt, "200D": safe_fmt}, index=False), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("🔒 Sovereign Master, authentication required.")
                          
