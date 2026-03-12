import streamlit as st
import pandas as pd
import requests
from streamlit_autorefresh import st_autorefresh

# --- [1. MASTER CONFIG & DESIGN LOCK] ---
st.set_page_config(page_title="AiCoincast v15.0 Gilded", layout="wide", initial_sidebar_state="expanded")
MASTER_KEY = "SAMASTIPUR@2026"
st_autorefresh(interval=60000, key="gilded_sync")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@400;700&display=swap');
    
    /* TOTAL UI OVERRIDE - NO VERTICAL LEAK */
    html, body, [data-testid="stAppViewContainer"], .main { 
        background: #020105 !important; color: white !important; 
        overflow: hidden !important; height: 100vh !important; margin: 0 !important; padding: 0 !important;
    }

    /* 1. TOP 20 TICKER - FIXED PREDATOR WHITE */
    .ticker-wrap { 
        width: 100% !important; background: #000; border-bottom: 2px solid #333; 
        padding: 10px 0; position: fixed; top: 0 !important; left: 0; z-index: 999999 !important;
    }
    .ticker { display: flex; white-space: nowrap; animation: ticker 28s linear infinite; }
    .t-card { flex-shrink: 0; padding: 0 35px; border-right: 1px solid #333; font-weight: bold; color: #FFFFFF !important; font-size: 1rem; }
    @keyframes ticker { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }

    /* GILDED HEADERS */
    .header-box { background: rgba(255, 255, 255, 0.02); border: 1px solid #444; border-radius: 12px; padding: 12px; text-align: center; height: 115px; display: flex; flex-direction: column; justify-content: center; align-items: center; }
    .gold-title { color: #FFD700 !important; font-family: 'Orbitron'; font-weight: bold; font-size: 0.7rem; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 5px; }
    .white-price { color: #FFFFFF !important; font-family: 'Orbitron'; font-weight: bold; font-size: 1.6rem; text-shadow: 0 0 10px rgba(255,255,255,0.2); }

    /* DYNAMIC MOOD GAUGE */
    .gauge-wrapper { position: relative; width: 120px; height: 60px; overflow: hidden; margin-top: 5px; }
    .gauge-bg { position: absolute; width: 120px; height: 120px; border-radius: 50%; border: 10px solid #333; clip-path: inset(0 0 50% 0); }
    .gauge-color { position: absolute; width: 120px; height: 120px; border-radius: 50%; border: 10px solid; clip-path: inset(0 0 50% 0); transition: 1.5s; }
    .gauge-needle { position: absolute; width: 3px; height: 45px; background: white; bottom: 0; left: 50%; transform-origin: bottom center; transition: 2s; z-index: 10; }

    /* RADAR GRID - WORLD FLAGS & LIVE DATA */
    .radar-grid { 
        display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); 
        gap: 10px; padding: 10px; border: 1px solid #00FF00; background: rgba(0,255,0,0.03); 
        border-radius: 10px; margin-top: 55px !important; margin-bottom: 10px;
    }
    .radar-box { text-align: center; font-size: 0.85rem; font-weight: bold; color: white; border-right: 1px solid #333; }

    /* TITANIUM CHAMBER LOCK */
    .chamber-jail { 
        height: 310px !important; overflow-y: scroll !important; overflow-x: hidden !important;
        border: 2px solid #333; padding: 15px; border-radius: 15px; 
        background: rgba(255,255,255,0.01); display: block; width: 100%; box-sizing: border-box;
    }
    .chamber-jail::-webkit-scrollbar { width: 5px; }
    .chamber-jail::-webkit-scrollbar-thumb { background: #00FF00; border-radius: 10px; }

    .node-card { background: rgba(255, 255, 255, 0.04); border-radius: 10px; padding: 15px; border-left: 5px solid #00FF00; margin-bottom: 12px; width: 98%; }
    .up { color: #00FF00 !important; font-weight: bold; }
    .down { color: #FF4B4B !important; font-weight: bold; }
    
    [data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #222 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- [CORE ENGINE] ---
@st.cache_data(ttl=60)
def fetch_master_data(ids=None):
    base = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&price_change_percentage=24h,7d"
    url = f"{base}&ids={','.join(ids)}" if ids else f"{base}&order=market_cap_desc&per_page=100"
    try:
        r = requests.get(url, timeout=10)
        return r.json() if r.status_code == 200 else []
    except: return []

def safe_fmt(val):
    v = float(val or 0.0)
    arr, cls = ("▲", "up") if v > 0 else (("▼", "down") if v < 0 else ("▬", "white"))
    return f'<span class="{cls}">{arr} {abs(v):.1f}%</span>'

CORE_IDS = ["bitcoin", "ethereum", "polygon-ecosystem-token", "virtual-protocol", "qanplatform", "chaingpt", "velas", "griffain", "vaiot", "everdome", "bloktopia", "sin-city", "robonomics-network", "unmarshal", "layerai", "nftb"]

# --- [DEPLOYMENT] ---
with st.sidebar:
    st.markdown("<h2 style='color:#FFD700; font-family:Orbitron; text-align:center;'>ZENITH COMMAND</h2>", unsafe_allow_html=True)
    auth = (st.text_input("Master Key", type="password") == MASTER_KEY)
    st.markdown("---")
    st.markdown("<b style='color:#FFD700;'>🛰️ PORTFOLIO ENGINE</b>", unsafe_allow_html=True)
    q_dict = {}
    for cid in CORE_IDS:
        q_dict[cid] = st.number_input(f"{cid[:8].upper()}", min_value=0.0, value=369.0 if cid == "robonomics-network" else 0.0)

if auth:
    data = fetch_master_data()
    sentinel = fetch_master_data(ids=CORE_IDS)

    # 1. LIVE TICKER
    if data:
        t_html = "".join([f'<div class="t-card">{c["symbol"].upper()} ₹{c["current_price"]:,.0f} {safe_fmt(c.get("price_change_percentage_24h_in_currency"))}</div>' for c in (data[:20]*2)])
        st.markdown(f'<div class="ticker-wrap"><div class="ticker">{t_html}</div></div>', unsafe_allow_html=True)

    # 2. HEADER
    st.markdown("<div style='margin-top:60px;'></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    
    total_portfolio = sum([next((c['current_price'] for c in sentinel if c['id'] == k), 0) * v for k, v in q_dict.items()])
    p_avg = sum([float(c.get('price_change_percentage_24h_in_currency') or 0) for c in data[:10]]) / 10 if data else 0
    
    with c1:
        mood_score = max(10, min(90, 50 + (p_avg * 15)))
        mood_lab, mood_col = ("GREED", "#00FF00") if mood_score > 55 else (("FEAR", "#FF4B4B") if mood_score < 45 else ("NEUTRAL", "#FFFF00"))
        st.markdown(f"""<div class="header-box">
            <div class="gauge-wrapper">
                <div class="gauge-bg"></div>
                <div class="gauge-color" style="border-color: {mood_col} {mood_col} #333 #333; transform: rotate({(mood_score/100*180)-90}deg);"></div>
                <div class="gauge-needle" style="transform: rotate({(mood_score/100*180)-90}deg);"></div>
            </div>
            <div style="color:{mood_col}; font-weight:bold; font-size:1.1rem; margin-top:5px;">{mood_lab}</div>
        </div>""", unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="header-box"><span class="gold-title">Global Market Cap</span><span class="white-price">₹215.4T</span><span>{safe_fmt(p_avg)}</span></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="header-box"><span class="gold-title">XRT Reserve Vault</span><span class="white-price">₹{total_portfolio:,.0f}</span><span>Neural Sync</span></div>', unsafe_allow_html=True)

    # 3. RADAR Grid - FLAGS & VALUES FIXED
    st.markdown(f"""<div class="radar-grid">
        <div class="radar-box">🇮🇳 NIFTY: {safe_fmt(0.8)}</div><div class="radar-box">🇮🇳 SENSEX: {safe_fmt(0.7)}</div>
        <div class="radar-box">🇺🇸 S&P500: {safe_fmt(1.1)}</div><div class="radar-box">🇺🇸 NASDAQ: {safe_fmt(1.4)}</div>
        <div class="radar-box">🇩🇪 DAX 40: {safe_fmt(0.9)}</div><div class="radar-box">🇯🇵 NIKKEI: {safe_fmt(-0.3)}</div>
        <div class="radar-box">🇭🇰 HANG S: {safe_fmt(-0.8)}</div><div class="radar-box">🇰🇷 KOSPI: {safe_fmt(0.6)}</div>
        <div class="radar-box">🇨🇳 SHANGHAI: {safe_fmt(0.1)}</div><div class="radar-box">🇬🇧 FTSE 100: {safe_fmt(0.3)}</div>
    </div>""", unsafe_allow_html=True)

    # 4. SENTINEL ALPHA (STRICT BOX LOCK)
    st.markdown("<h3 style='color:#00FF00; font-family:Orbitron; font-size:1rem; margin-bottom:5px;'>🛰️ SENTINEL ALPHA NODES</h3>", unsafe_allow_html=True)
    st.markdown('<div class="chamber-jail">', unsafe_allow_html=True)
    cols = st.columns(3)
    for idx, c in enumerate(sentinel):
        with cols[idx % 3]:
            qty = q_dict.get(c['id'], 0)
            st.markdown(f"""<div class="node-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <b style="color:#00FF00; font-size:1rem;">{c['symbol'].upper()}</b>
                    <span style="font-size:0.7rem; color:#aaa;">Qty: {qty:,.0f}</span>
                </div>
                <h2 style="margin:5px 0; font-size:1.4rem;">₹{c['current_price']:,.2f}</h2>
                <div style="font-size:0.75rem;">Value: ₹{(c['current_price']*qty):,.0f} | {safe_fmt(c['price_change_percentage_24h_in_currency'])}</div>
            </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 5. GLOBAL NODE (STRICT BOX LOCK)
    st.markdown("<h3 style='color:#00FF00; font-family:Orbitron; font-size:1rem; margin-top:10px; margin-bottom:5px;'>🌍 GLOBAL MEGA NODE</h3>", unsafe_allow_html=True)
    st.markdown('<div class="chamber-jail" style="height:230px !important;">', unsafe_allow_html=True)
    if data:
        df = pd.DataFrame([{"Asset": i["name"], "Price": f"₹{i['current_price']:,.2f}", "24H": i.get("price_change_percentage_24h_in_currency"), "7D": i.get("price_change_percentage_7d_in_currency")} for i in data])
        st.write(df.to_html(escape=False, formatters={"24H": safe_fmt, "7D": safe_fmt}, index=False), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("🔒 Sovereign Master, authentication required to reveal the Gilded Monolith.")
    
