import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go

# --- [1. MASTER CONFIG & DESIGN ARCHITECTURE] ---
st.set_page_config(page_title="AiCoincast v2.0 Omnipotent", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

st.markdown("""
    <style>
    .stApp { background-color: #05010D !important; }
    h1, h2, h3, h4, p, span, div { color: #FFFFFF !important; font-family: 'Inter', sans-serif; }
    
    /* FIX 1: HORIZONTAL SCROLLER (TICKER) */
    .ticker-wrap {
        width: 100%; overflow: hidden; background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px); border-bottom: 2px solid #00FF00; padding: 15px 0;
    }
    .ticker {
        display: flex; white-space: nowrap; animation: ticker 25s linear infinite;
    }
    .ticker:hover { animation-play-state: paused; }
    .glass-card {
        flex-shrink: 0; background: rgba(255, 255, 255, 0.07);
        padding: 10px 25px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.12);
        margin: 0 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    @keyframes ticker {
        0% { transform: translateX(0); }
        100% { transform: translateX(-50%); }
    }
    
    .radar-strip { background: #1A0B35; padding: 12px; border-radius: 10px; display: flex; justify-content: space-around; margin: 20px 0; border: 1px solid #00FF00; }
    .glow-up { color: #00FF00 !important; font-weight: bold; }
    .glow-down { color: #FF0000 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- [THE BRAIN: CORE DATA ENGINE] ---
def fetch_api(url):
    try:
        r = requests.get(url, timeout=15)
        return r.json() if r.status_code == 200 else None
    except: return None

def get_ind(val):
    v = float(val) if val is not None else 0.0
    return f"🟢 +{v:.1f}%" if v > 0 else (f"🔴 {v:.1f}%" if v < 0 else "▬ 0.0%")

# CORE 16 IDs (FIXED & LOCKED)
CORE_IDS = ["bitcoin", "ethereum", "polygon-ecosystem-token", "qanplatform", "chaingpt", "velas", "griffain", "vaiot", "everdome", "sin-city", "layerai", "robonomics-network", "bloktopia", "nftb", "virtual-protocol", "unmarshal"]

@st.cache_data(ttl=60)
def fetch_master_monolith(extras, query):
    # Fetching with explicit percentage change for all intervals
    base = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&price_change_percentage=24h,7d,30d,200d"
    
    top_250 = fetch_api(f"{base}&order=market_cap_desc&per_page=250&page=1")
    
    s_ids = ",".join(CORE_IDS + [x for x in extras if x])
    sentinel = fetch_api(f"{base}&ids={s_ids}")
    
    search_data = []
    if query and len(query) >= 3:
        search_data = fetch_api(f"{base}&ids={query.lower().replace(' ', '-')}")
        
    return top_250, sentinel, search_data

# --- [INTERFACE DEPLOYMENT] ---
with st.sidebar:
    st.title("🛰️ OMNI VAULT v2.0")
    m_key = st.text_input("Master Key", type="password")
    st.markdown("---")
    x_nodes = [st.text_input(f"Node #{i}") for i in range(17, 21)]

if m_key == MASTER_KEY:
    q = st.text_input("🔍 Neural Search Index", placeholder="Search 5000+ Assets...")
    top, sent, s_res = fetch_master_monolith(x_nodes, q)

    # UI: TOP 20 TICKER (FIX 1: Horizontal Scroll)
    if top:
        t_cards = ""
        # Doubling the list for a seamless infinite loop
        loop_top = top[:20] + top[:20]
        for c in loop_top:
            p_change = c.get('price_change_percentage_24h', 0)
            color = "glow-up" if p_change > 0 else "glow-down"
            t_cards += f'''<div class="glass-card"><b>{c["symbol"].upper()}</b>: ₹{c["current_price"]:,.0f} <span class="{color}">{get_ind(p_change)}</span></div>'''
        st.markdown(f'<div class="ticker-wrap"><div class="ticker">{t_cards}</div></div>', unsafe_allow_html=True)

    # UI: MASTER RADAR
    st.markdown('<div class="radar-strip"><span>SENSEX: 74,119 ▲</span> <span>NIFTY: 22,490 ▲</span> <span>BTC: LIVE ⚡</span> <span>ETH: LIVE ⚡</span></div>', unsafe_allow_html=True)

    # UI: SENTINEL ALPHA (FIX 2 & 3: 16 Coins & All Price Indicators)
    st.header("🛰️ Sentinel Alpha Command")
    if sent:
        s_data = []
        for c in sent:
            s_data.append({
                "Rank": c.get("market_cap_rank"),
                "Logo": c.get("image"),
                "Asset": c.get("name").upper() if c.get("id") != "everdome" else "HUM(AI)N (AI)",
                "Price": f"₹{c.get('current_price'):,.2f}",
                "24H": get_ind(c.get('price_change_percentage_24h_in_currency')),
                "7D": get_ind(c.get('price_change_percentage_7d_in_currency')),
                "30D": get_ind(c.get('price_change_percentage_30d_in_currency')),
                "90D Trend": get_ind(c.get('price_change_percentage_200d_in_currency'))
            })
        st.dataframe(pd.DataFrame(s_data), column_config={"Logo": st.column_config.ImageColumn()}, use_container_width=True, hide_index=True)

    # UI: GLOBAL MEGA NODE
    st.header("🌍 Global Mega Node")
    pool = s_res if (q and s_res) else (top[:150] if top else [])
    if pool:
        g_df = pd.DataFrame([{
            "Rank": i.get("market_cap_rank"), "Logo": i.get("image"), "Name": i.get("name"),
            "Price": f"₹{i.get('current_price', 0):,.2f}", "24H": get_ind(i.get('price_change_percentage_24h_in_currency'))
        } for i in pool if isinstance(i, dict)])
        st.dataframe(g_df, column_config={"Logo": st.column_config.ImageColumn()}, use_container_width=True, hide_index=True)
else:
    st.warning("🔒 Sovereign Master, authentication required.")
            
