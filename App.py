import streamlit as st
import pandas as pd
import requests
from streamlit_autorefresh import st_autorefresh

# --- [1. MASTER CONFIG & SOVEREIGN DESIGN] ---
st.set_page_config(page_title="AiCoincast v4.6 Sovereign", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

# Anti-Crash Ghost Refresh (60 Seconds)
st_autorefresh(interval=60000, key="sovereign_sync")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@400;700&display=swap');
    
    /* THE ABYSS BACKGROUND */
    .stApp { background: #020105 !important; color: #FFFFFF !important; overflow: hidden; }
    h1, h2, h3, b, p, span, div { font-family: 'Inter', sans-serif; color: #FFFFFF !important; }
    
    /* GAUGE & VAULT HEADER */
    .header-box { 
        background: rgba(0, 255, 0, 0.05); border: 2px solid #00FF00; 
        border-radius: 12px; padding: 12px; text-align: center; 
        box-shadow: 0 0 15px rgba(0, 255, 0, 0.2);
    }
    .neon-glow { color: #00FF00; text-shadow: 0 0 10px #00FF00; font-family: 'Orbitron'; font-weight: bold; }

    /* RADAR GRID - 11 INDICES (LARGE & CLEAR) */
    .radar-grid { 
        display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); 
        gap: 12px; padding: 15px; border: 2px solid #00FF00; 
        background: rgba(0,255,0,0.03); border-radius: 12px; margin: 15px 0;
    }
    .radar-box { text-align: center; font-size: 0.95rem; font-weight: bold; border-right: 1px solid #333; }
    .radar-box:last-child { border-right: none; }

    /* KINETIC SCROLL CHAMBERS (STRICT CONTAINER LOCK) */
    .scroll-chamber { 
        height: 400px; overflow-y: auto; overflow-x: hidden;
        border: 1px solid #333; padding: 15px; border-radius: 12px; 
        background: rgba(255,255,255,0.01); margin-bottom: 20px;
    }
    .scroll-chamber::-webkit-scrollbar { width: 5px; }
    .scroll-chamber::-webkit-scrollbar-thumb { background: #00FF00; border-radius: 10px; }

    /* SENTINEL NODES */
    .node-card { 
        background: rgba(255, 255, 255, 0.04); border-radius: 10px; padding: 18px; 
        border-left: 5px solid #00FF00; margin-bottom: 12px; transition: 0.3s;
    }
    .node-card:hover { background: rgba(255, 255, 255, 0.08); transform: translateY(-2px); }
    
    .up { color: #00FF00 !important; font-weight: bold; }
    .down { color: #FF4B4B !important; font-weight: bold; }
    .whale-pulse { color: #00FF00; font-size: 1.2rem; filter: drop-shadow(0 0 5px #00FF00); }
    </style>
    """, unsafe_allow_html=True)

# --- [CORE ENGINE - LAZY LOAD + CACHE] ---
@st.cache_data(ttl=60)
def fetch_sovereign_data(ids=None):
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

# --- [DEPLOYMENT PHASE] ---
with st.sidebar:
    st.markdown("<h2 class='neon-glow'>🛡️ OMNI VAULT</h2>", unsafe_allow_html=True)
    key = st.text_input("Master Key", type="password")
    h_qty = st.number_input("Holdings (XRT)", 369)
    st.markdown("---")
    st.info("System: V4.6 Absolute Sovereign Active")

if key == MASTER_KEY:
    full_market = fetch_sovereign_data()
    sentinel = fetch_sovereign_data(ids=CORE_IDS)

    # 1. MOOD & VAULT HEADER
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1: st.markdown('<div class="header-box"><span style="font-size:0.7rem; opacity:0.7;">BAZAAR MOOD</span><br><span class="neon-glow" style="font-size:1.5rem;">74 | GREED 📈</span></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="header-box"><span style="font-size:0.7rem; opacity:0.7;">GLOBAL CAP</span><br><span class="neon-glow" style="font-size:1.5rem;">₹215.4T</span></div>', unsafe_allow_html=True)
    with c3:
        x_coin = next((i for i in sentinel if i["id"] == "robonomics-network"), None)
        val = (x_coin['current_price'] * h_qty) if x_coin else 0
        st.markdown(f'<div class="header-box"><span style="font-size:0.7rem; opacity:0.7;">XRT RESERVE</span><br><span class="neon-glow" style="font-size:1.5rem;">₹{val:,.2f}</span></div>', unsafe_allow_html=True)

    # 2. RADAR - 11 INDICES (FIXED VALUES)
    st.markdown(f"""<div class="radar-grid">
        <div class="radar-box">🇮🇳 NIFTY: {safe_fmt(0.8)}</div><div class="radar-box">🇮🇳 SENSEX: {safe_fmt(0.7)}</div>
        <div class="radar-box">🇺🇸 S&P500: {safe_fmt(1.1)}</div><div class="radar-box">🇺🇸 NASDAQ: {safe_fmt(1.4)}</div>
        <div class="radar-box">🇺🇸 DOW J: {safe_fmt(0.5)}</div><div class="radar-box">🇩🇪 DAX 40: {safe_fmt(0.9)}</div>
        <div class="radar-box">🇫🇷 CAC 40: {safe_fmt(0.4)}</div><div class="radar-box">🇬🇧 FTSE: {safe_fmt(0.2)}</div>
        <div class="radar-box">🇯🇵 NIKKEI: {safe_fmt(-0.3)}</div><div class="radar-box">🇭🇰 HANG S: {safe_fmt(-0.8)}</div>
        <div class="radar-box">🇰🇷 KOSPI: {safe_fmt(0.6)}</div>
    </div>""", unsafe_allow_html=True)

    # 3. SENTINEL ALPHA (SCROLL CHAMBER)
    st.markdown("<h3 class='neon-glow' style='font-size:1.2rem;'>🛰️ Sentinel Alpha Command</h3>", unsafe_allow_html=True)
    st.markdown('<div class="scroll-chamber">', unsafe_allow_html=True)
    cols = st.columns(3)
    for idx, c in enumerate(sentinel):
        with cols[idx % 3]:
            p_24h = float(c.get('price_change_percentage_24h_in_currency') or 0.0)
            whale = '<span class="whale-pulse">🐋</span>' if abs(p_24h) > 4.0 else ""
            st.markdown(f"""<div class="node-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <b style="font-size:1.1rem; color:#00FF00;">{c.get('name','').upper()}</b>{whale}
                </div>
                <h3 style="margin:10px 0;">₹{c.get('current_price',0):,.2f}</h3>
                <div style="display:grid; grid-template-columns: 1fr 1fr; font-size:0.75rem; gap:8px;">
                    <div>24H: {safe_fmt(p_24h)}</div><div>7D: {safe_fmt(c.get('price_change_percentage_7d_in_currency'))}</div>
                    <div>30D: {safe_fmt(c.get('price_change_percentage_30d_in_currency'))}</div><div>90D: {safe_fmt(c.get('price_change_percentage_200d_in_currency'))}</div>
                </div>
            </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 4. GLOBAL MEGA NODE (150 COINS CHAMBER)
    st.markdown("<h3 class='neon-glow' style='font-size:1.2rem;'>🌍 Global Mega Node (Top 150)</h3>", unsafe_allow_html=True)
    st.markdown('<div class="scroll-chamber" style="height:350px;">', unsafe_allow_html=True)
    if full_market:
        df = pd.DataFrame([{
            "Rank": i["market_cap_rank"], "Logo": i["image"], "Asset": i["name"], 
            "Price": f"₹{i['current_price']:,.2f}", 
            "24H": i.get("price_change_percentage_24h_in_currency"),
            "7D": i.get("price_change_percentage_7d_in_currency"),
            "30D": i.get("price_change_percentage_30d_in_currency"),
            "90D": i.get("price_change_percentage_200d_in_currency")
        } for i in full_market])
        st.write(df.to_html(escape=False, formatters={
            "Logo": lambda x: f'<img src="{x}" width="22">',
            "24H": safe_fmt, "7D": safe_fmt, "30D": safe_fmt, "90D": safe_fmt
        }, index=False), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("🔒 Sovereign Master, authentication required.")
    
