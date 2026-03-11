import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go

# --- [1. MASTER CONFIG & NEON WHEEL DESIGN] ---
st.set_page_config(page_title="AiCoincast v3.2 Sovereign", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;500&display=swap');
    .stApp { background: radial-gradient(circle at top, #0d0221 0%, #020105 100%) !important; }
    h1, h2, h3 { font-family: 'Orbitron', sans-serif; color: #00FF00 !important; }
    
    /* WHEEL INDICATOR ANIMATION */
    .wheel-container { position: relative; width: 60px; height: 60px; border-radius: 50%; border: 4px solid rgba(255,255,255,0.1); display: flex; align-items: center; justify-content: center; }
    .wheel-glow-up { border: 4px solid #00FF00; box-shadow: 0 0 15px #00FF00; }
    .wheel-glow-down { border: 4px solid #FF0000; box-shadow: 0 0 15px #FF0000; }

    .node-card {
        background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px; padding: 25px; transition: 0.4s; height: 100%; border-left: 5px solid #00FF00;
    }
    .node-card:hover { transform: translateY(-8px); border-color: #00FF00; box-shadow: 0 15px 35px rgba(0,255,0,0.2); }
    
    .up { color: #00FF00 !important; font-weight: bold; }
    .down { color: #FF0000 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- [CORE ENGINE] ---
def fetch_nexus_data(ids=None):
    base = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&price_change_percentage=24h,7d,30d,200d"
    url = f"{base}&ids={','.join(ids)}" if ids else f"{base}&order=market_cap_desc&per_page=100&page=1"
    try:
        r = requests.get(url, timeout=15)
        return r.json() if r.status_code == 200 else []
    except: return []

def fmt(val):
    v = float(val) if val else 0.0
    arr, cls = ("▲", "up") if v > 0 else (("▼", "down") if v < 0 else ("▬", ""))
    return f'<span class="{cls}">{arr} {abs(v):.1f}%</span>'

CORE_IDS = ["bitcoin", "ethereum", "polygon-ecosystem-token", "virtual-protocol", "qanplatform", "chaingpt", "velas", "griffain", "vaiot", "everdome", "bloktopia", "sin-city", "robonomics-network", "unmarshal", "layerai", "nftb"]

# --- [DEPLOYMENT] ---
with st.sidebar:
    st.title("🛡️ OMNI VAULT v3.2")
    key = st.text_input("Master Key", type="password")
    st.markdown("---")
    h_qty, h_buy = st.number_input("XRT Holdings", 206), st.number_input("XRT Buy", 480)
    st.markdown("---")
    extra = [st.text_input(f"Node #{i}") for i in range(17, 21)]

if key == MASTER_KEY:
    top_data = fetch_nexus_data()
    sentinel_data = fetch_nexus_data(ids=CORE_IDS + [x for x in extra if x])

    # 1. MASTER PORTFOLIO PERFORMANCE
    x_coin = next((i for i in sentinel_data if i["id"] == "robonomics-network"), None)
    if x_coin:
        val = x_coin['current_price'] * h_qty
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.02); border:2px solid #00FF00; border-radius:20px; padding:30px; text-align:center; margin-bottom:30px;">
            <p style="letter-spacing:5px; opacity:0.6;">MASTER ASSET VAULT</p>
            <div style="font-size:3.8rem; color:#00FF00; font-weight:bold; text-shadow:0 0 20px #00FF00;">₹{val:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    # 2. SENTINEL ALPHA WITH WHEEL INDICATORS
    st.header("🛰️ Sentinel Alpha Command")
    cols = st.columns(3)
    for idx, c in enumerate(sentinel_data):
        with cols[idx % 3]:
            name = c['name'].upper() if c['id'] != 'everdome' else "HUM(AI)N (AI)"
            p_24h = c.get('price_change_percentage_24h_in_currency', 0)
            wheel_class = "wheel-glow-up" if p_24h > 0 else "wheel-glow-down"
            
            st.markdown(f"""
            <div class="node-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <b>{name}</b>
                    <div class="wheel-container {wheel_class}">
                        <span style="font-size:0.7rem;">{p_24h:.1f}%</span>
                    </div>
                </div>
                <h2 style="margin:15px 0;">₹{c['current_price']:,.2f}</h2>
                <div style="display:grid; grid-template-columns:1fr 1fr; font-size:0.85rem; gap:10px;">
                    <div>7D: {fmt(c.get('price_change_percentage_7d_in_currency'))}</div>
                    <div>30D: {fmt(c.get('price_change_percentage_30d_in_currency'))}</div>
                </div>
                <div style="margin-top:15px; border-top:1px solid rgba(255,255,255,0.1); padding-top:10px;">
                    <span style="font-size:0.75rem; color:#00FF00; opacity:0.7;">📰 SENTIMENT: {'BULLISH RALLY' if p_24h > 0 else 'BEARISH CONSOLIDATION'}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

    # 3. GLOBAL MEGA NODE (PREMIUM TABLE)
    st.header("🌍 Global Mega Node")
    if top_data:
        df = pd.DataFrame([{
            "Rank": i["market_cap_rank"], "Asset": i["name"], "Price": f"₹{i['current_price']:,.2f}",
            "24H": i.get("price_change_percentage_24h_in_currency"),
            "7D": i.get("price_change_percentage_7d_in_currency"),
            "30D": i.get("price_change_percentage_30d_in_currency")
        } for i in top_data])
        st.write(df.to_html(escape=False, formatters={"24H": fmt, "7D": fmt, "30D": fmt}, index=False), unsafe_allow_html=True)
else:
    st.info("🔒 Sovereign Master, authentication required.")
            
