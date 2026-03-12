import streamlit as st
import pandas as pd
import requests
from streamlit_autorefresh import st_autorefresh

# --- [1. MASTER CONFIG & ORACLE DESIGN] ---
st.set_page_config(page_title="AiCoincast v4.5 Kinetic Oracle", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"
st_autorefresh(interval=45000, key="oracle_sync")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@400;700&display=swap');
    .stApp { background: #020105 !important; color: #FFFFFF !important; overflow: hidden; }
    
    /* MARKET SWEEPING GAUGE */
    .gauge-box { background: rgba(0, 255, 0, 0.05); border: 1px solid #00FF00; border-radius: 15px; padding: 10px; text-align: center; margin-bottom: 10px; }
    .neon-text { color: #00FF00; text-shadow: 0 0 10px #00FF00; font-weight: bold; font-family: 'Orbitron'; }

    /* TICKER & RADAR */
    .ticker-wrap { width: 100%; overflow: hidden; background: #000; border-bottom: 2px solid #00FF00; padding: 8px 0; }
    .ticker { display: flex; white-space: nowrap; animation: ticker 25s linear infinite; }
    .t-card { flex-shrink: 0; padding: 0 25px; font-weight: bold; font-size: 0.9rem; border-right: 1px solid #333; }
    @keyframes ticker { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }

    .radar-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; padding: 12px; border: 1px solid #00FF00; background: rgba(0,255,0,0.02); border-radius: 12px; margin-bottom: 15px; }
    .radar-box { text-align: center; font-size: 1rem; font-weight: bold; color: #FFFFFF !important; }

    /* SCROLL CHAMBERS */
    .scroll-chamber { height: 420px; overflow-y: auto; border: 1px solid #333; padding: 15px; border-radius: 12px; background: rgba(255,255,255,0.01); }
    .scroll-chamber::-webkit-scrollbar { width: 5px; }
    .scroll-chamber::-webkit-scrollbar-thumb { background: #00FF00; border-radius: 10px; }

    .node-card { background: rgba(255, 255, 255, 0.04); border-radius: 10px; padding: 18px; border-left: 5px solid #00FF00; margin-bottom: 12px; transition: 0.3s; }
    .node-card:hover { background: rgba(255, 255, 255, 0.08); transform: scale(1.01); }
    
    .whale-alert { color: #00FF00; font-size: 1.2rem; filter: drop-shadow(0 0 5px #00FF00); }
    .up { color: #00FF00 !important; font-weight: bold; }
    .down { color: #FF4B4B !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- [CORE ENGINE] ---
@st.cache_data(ttl=45)
def fetch_master_data(ids=None):
    base = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&price_change_percentage=24h,7d,30d,90d"
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
if st.sidebar.text_input("Master Key", type="password") == MASTER_KEY:
    full_data = fetch_master_data()
    sentinel = fetch_master_data(ids=CORE_IDS)

    # 1. TOP TICKER
    if full_data:
        t_html = "".join([f'<div class="t-card">{c["symbol"].upper()} ₹{c["current_price"]:,.0f} {safe_fmt(c.get("price_change_percentage_24h_in_currency"))}</div>' for c in (full_data[:20]*2)])
        st.markdown(f'<div class="ticker-wrap"><div class="ticker">{t_html}</div></div>', unsafe_allow_html=True)

    # 2. MARKET SWEEPING GAUGE (PHASE 6)
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown("""<div class="gauge-box"><span style="font-size:0.7rem; opacity:0.7; letter-spacing:2px;">MARKET SENTIMENT</span><br><span class="neon-text" style="font-size:1.5rem;">72 | GREED 📈</span></div>""", unsafe_allow_html=True)
    with c2:
        x_coin = next((i for i in sentinel if i["id"] == "robonomics-network"), None)
        if x_coin:
            st.markdown(f"""<div class="gauge-box" style="border-color:#555;"><span style="font-size:0.7rem; opacity:0.7; letter-spacing:2px;">XRT RESERVE</span><br><span class="neon-text" style="font-size:1.5rem; color:white;">₹{x_coin['current_price']*369:,.2f}</span></div>""", unsafe_allow_html=True)

    # 3. GLOBAL RADAR
    st.markdown(f"""<div class="radar-grid">
        <div class="radar-box">🇮🇳 NIFTY: {safe_fmt(0.8)}</div><div class="radar-box">🇺🇸 S&P 500: {safe_fmt(1.2)}</div>
        <div class="radar-box">🇯🇵 NIKKEI: {safe_fmt(-0.3)}</div><div class="radar-box">🇩🇪 DAX 40: {safe_fmt(0.9)}</div>
        <div class="radar-box">🇨🇳 SHANGHAI: {safe_fmt(0.1)}</div>
    </div>""", unsafe_allow_html=True)

    # 4. SENTINEL ALPHA (WHALE & SIGNAL INTEGRATED)
    st.markdown("### 🛰️ Sentinel Alpha Command")
    st.markdown('<div class="scroll-chamber">', unsafe_allow_html=True)
    cols = st.columns(3)
    for idx, c in enumerate(sentinel):
        with cols[idx % 3]:
            p_24h = float(c.get('price_change_percentage_24h_in_currency') or 0.0)
            whale_icon = '<span class="whale-alert">🐋</span>' if abs(p_24h) > 4.5 else ""
            signal = '<span style="color:#00FF00; font-size:0.7rem;">[STRONG BUY]</span>' if p_24h > 1.5 else '<span style="color:#888; font-size:0.7rem;">[HOLD]</span>'
            
            st.markdown(f"""<div class="node-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <b>{c.get('name','').upper()}</b> {whale_icon}
                </div>
                <h3 style="margin:5px 0;">₹{c.get('current_price',0):,.2f} {signal}</h3>
                <div style="display:grid; grid-template-columns: 1fr 1fr; font-size:0.7rem; gap:5px; opacity:0.8;">
                    <div>24H: {safe_fmt(p_24h)}</div><div>7D: {safe_fmt(c.get('price_change_percentage_7d_in_currency'))}</div>
                    <div>30D: {safe_fmt(c.get('price_change_percentage_30d_in_currency'))}</div><div>90D: {safe_fmt(c.get('price_change_percentage_90d_in_currency'))}</div>
                </div>
            </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 5. GLOBAL MEGA NODE (SCROLLABLE TABLE)
    st.markdown("### 🌍 Global Mega Node (Top 150)")
    st.markdown('<div class="scroll-chamber" style="height:320px;">', unsafe_allow_html=True)
    if full_data:
        df = pd.DataFrame([{"Rank": i["market_cap_rank"], "Logo": i["image"], "Asset": i["name"], "Price": f"₹{i['current_price']:,.2f}", "24H": i.get("price_change_percentage_24h_in_currency"), "7D": i.get("price_change_percentage_7d_in_currency")} for i in full_data])
        st.write(df.to_html(escape=False, formatters={"Logo": lambda x: f'<img src="{x}" width="20">',"24H": safe_fmt, "7D": safe_fmt}, index=False), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("🔒 Sovereign Master, authentication required to reveal the Oracle v4.5.")
    
