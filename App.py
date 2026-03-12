import streamlit as st
import pandas as pd
import requests
from streamlit_autorefresh import st_autorefresh

# --- [1. MASTER CONFIG & DESIGN] ---
st.set_page_config(page_title="AiCoincast v4.7 Monolith", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"
st_autorefresh(interval=60000, key="monolith_sync")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@400;700&display=swap');
    .stApp { background: #020105 !important; color: white !important; overflow-x: hidden; }
    
    /* 1. TOP 20 SCROLLING TICKER (RESTORED) */
    .ticker-wrap { width: 100%; overflow: hidden; background: #000; border-bottom: 2px solid #00FF00; padding: 12px 0; margin-bottom: 10px; }
    .ticker { display: flex; white-space: nowrap; animation: ticker 25s linear infinite; }
    .t-card { flex-shrink: 0; padding: 0 30px; border-right: 1px solid #333; font-weight: bold; font-size: 1rem; color: #00FF00; }
    @keyframes ticker { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }

    /* 2. HEADER BOXES */
    .header-box { background: rgba(0, 255, 0, 0.05); border: 2px solid #00FF00; border-radius: 12px; padding: 15px; text-align: center; }
    .neon-text { color: #00FF00; text-shadow: 0 0 10px #00FF00; font-family: 'Orbitron'; font-weight: bold; }

    /* 3. RADAR GRID - 11 INDICES (LARGE VISIBILITY) */
    .radar-grid { 
        display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); 
        gap: 15px; padding: 15px; border: 2px solid #00FF00; background: rgba(0,255,0,0.03); 
        border-radius: 12px; margin: 15px 0;
    }
    .radar-box { text-align: center; font-size: 1.1rem; font-weight: bold; border-right: 1px solid #444; color: white; }

    /* 4. SCROLL CHAMBER LOCK (STRICT BOX) */
    .scroll-chamber { 
        height: 420px; overflow-y: auto; overflow-x: hidden;
        border: 1px solid #333; padding: 15px; border-radius: 15px; 
        background: rgba(255,255,255,0.02); margin-bottom: 25px;
    }
    .scroll-chamber::-webkit-scrollbar { width: 5px; }
    .scroll-chamber::-webkit-scrollbar-thumb { background: #00FF00; border-radius: 10px; }

    .node-card { background: rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 20px; border-left: 5px solid #00FF00; margin-bottom: 15px; }
    .up { color: #00FF00 !important; font-weight: bold; }
    .down { color: #FF4B4B !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- [CORE ENGINE - CACHED] ---
@st.cache_data(ttl=60)
def fetch_data(ids=None):
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
if st.sidebar.text_input("Master Key", type="password") == MASTER_KEY:
    top_150 = fetch_data()
    sentinel = fetch_data(ids=CORE_IDS)

    # 1. TOP 20 SCROLLING TICKER
    if top_150:
        t_html = "".join([f'<div class="t-card">{c["symbol"].upper()} ₹{c["current_price"]:,.0f} {safe_fmt(c.get("price_change_percentage_24h_in_currency"))}</div>' for c in (top_150[:20]*2)])
        st.markdown(f'<div class="ticker-wrap"><div class="ticker">{t_html}</div></div>', unsafe_allow_html=True)

    # 2. MOOD & VAULT HEADER
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="header-box"><span style="font-size:0.75rem;">BAZAAR MOOD</span><br><span class="neon-text" style="font-size:1.8rem;">74 | GREED 📈</span></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="header-box"><span style="font-size:0.75rem;">GLOBAL CAP</span><br><span class="neon-text" style="font-size:1.8rem;">₹215.4T</span></div>', unsafe_allow_html=True)
    with c3:
        x_coin = next((i for i in sentinel if i["id"] == "robonomics-network"), None)
        val = (x_coin['current_price'] * 369) if x_coin else 0
        st.markdown(f'<div class="header-box"><span style="font-size:0.75rem;">XRT RESERVE</span><br><span class="neon-text" style="font-size:1.8rem;">₹{val:,.2f}</span></div>', unsafe_allow_html=True)

    # 3. SHARE MARKET RADAR (LARGE DISPLAY)
    st.markdown(f"""<div class="radar-grid">
        <div class="radar-box">🇮🇳 NIFTY: 23,410 {safe_fmt(0.8)}</div><div class="radar-box">🇮🇳 SENSEX: 77,150 {safe_fmt(0.7)}</div>
        <div class="radar-box">🇺🇸 S&P500: 5,120 {safe_fmt(1.1)}</div><div class="radar-box">🇺🇸 NASDAQ: 16,400 {safe_fmt(1.4)}</div>
        <div class="radar-box">🇺🇸 DOW J: 39,200 {safe_fmt(0.5)}</div><div class="radar-box">🇩🇪 DAX 40: 18,100 {safe_fmt(0.9)}</div>
        <div class="radar-box">🇬🇧 FTSE: 8,250 {safe_fmt(0.2)}</div><div class="radar-box">🇯🇵 NIKKEI: 38,700 {safe_fmt(-0.3)}</div>
        <div class="radar-box">🇭🇰 HANG S: 17,400 {safe_fmt(-0.8)}</div><div class="radar-box">🇰🇷 KOSPI: 2,650 {safe_fmt(0.6)}</div>
        <div class="radar-box">🇨🇳 SHANGHAI: 3,050 {safe_fmt(0.1)}</div>
    </div>""", unsafe_allow_html=True)

    # 4. SENTINEL ALPHA (SCROLLABLE CHAMBER)
    st.markdown("### 🛰️ Sentinel Alpha Command")
    st.markdown('<div class="scroll-chamber">', unsafe_allow_html=True)
    cols = st.columns(3)
    for idx, c in enumerate(sentinel):
        with cols[idx % 3]:
            p_24h = float(c.get('price_change_percentage_24h_in_currency') or 0.0)
            whale = "🐋" if abs(p_24h) > 4.0 else ""
            st.markdown(f"""<div class="node-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <b style="font-size:1.2rem; color:#00FF00;">{c.get('name','').upper()}</b> {whale}
                </div>
                <h2 style="margin:10px 0;">₹{c.get('current_price',0):,.2f}</h2>
                <div style="display:grid; grid-template-columns: 1fr 1fr; font-size:0.8rem; gap:10px;">
                    <div>24H: {safe_fmt(p_24h)}</div><div>7D: {safe_fmt(c.get('price_change_percentage_7d_in_currency'))}</div>
                    <div>30D: {safe_fmt(c.get('price_change_percentage_30d_in_currency'))}</div><div>90D: {safe_fmt(c.get('price_change_percentage_200d_in_currency'))}</div>
                </div>
            </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 5. GLOBAL MEGA NODE (TOP 150 SCROLLABLE)
    st.markdown("### 🌍 Global Mega Node (Top 150)")
    st.markdown('<div class="scroll-chamber" style="height:350px;">', unsafe_allow_html=True)
    if top_150:
        df = pd.DataFrame([{
            "Rank": i["market_cap_rank"], "Logo": i["image"], "Asset": i["name"], 
            "Price": f"₹{i['current_price']:,.2f}", 
            "24H": i.get("price_change_percentage_24h_in_currency"),
            "7D": i.get("price_change_percentage_7d_in_currency"),
            "30D": i.get("price_change_percentage_30d_in_currency"),
            "90D": i.get("price_change_percentage_200d_in_currency")
        } for i in top_150])
        st.write(df.to_html(escape=False, formatters={"Logo": lambda x: f'<img src="{x}" width="20">',"24H": safe_fmt, "7D": safe_fmt, "30D": safe_fmt, "90D": safe_fmt}, index=False), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("🔒 Sovereign Master, authentication required.")
    
