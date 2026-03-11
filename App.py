import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go

# --- [1. MASTER CONFIG & DESIGN] ---
st.set_page_config(page_title="AiCoincast v2.0 Omnipotent", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

st.markdown("""
    <style>
    .stApp { background-color: #05010D !important; }
    h1, h2, h3, h4, p, span, div { color: #FFFFFF !important; font-family: 'Inter', sans-serif; }
    
    /* TICKER OPTIMIZATION */
    .ticker-wrap {
        width: 100%; overflow: hidden; background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px); border-bottom: 2px solid #00FF00; padding: 12px 0;
    }
    .ticker {
        display: flex; white-space: nowrap; animation: ticker 18s linear infinite;
    }
    .glass-card {
        flex-shrink: 0; background: rgba(255, 255, 255, 0.07);
        padding: 8px 22px; border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 0 12px;
    }
    @keyframes ticker { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }
    
    /* NEON INDICATORS LIKE NIFTY */
    .neon-up { color: #00FF00 !important; font-weight: bold; text-shadow: 0 0 5px #00FF00; }
    .neon-down { color: #FF0000 !important; font-weight: bold; text-shadow: 0 0 5px #FF0000; }
    
    .radar-strip { background: #1A0B35; padding: 10px; border-radius: 8px; display: flex; justify-content: space-around; margin: 15px 0; border: 1px solid #00FF00; }
    </style>
    """, unsafe_allow_html=True)

# --- [CORE ENGINE] ---
def fetch_api(url):
    try:
        r = requests.get(url, timeout=15)
        return r.json() if r.status_code == 200 else None
    except: return None

def get_neon_ind(val):
    v = float(val) if val is not None else 0.0
    if v > 0: return f"<span class='neon-up'>▲ +{v:.1f}%</span>"
    elif v < 0: return f"<span class='neon-down'>▼ {v:.1f}%</span>"
    return "▬ 0.0%"

CORE_IDS = ["bitcoin", "ethereum", "polygon-ecosystem-token", "qanplatform", "chaingpt", "velas", "griffain", "vaiot", "everdome", "sin-city", "layerai", "robonomics-network", "bloktopia", "nftb", "virtual-protocol", "unmarshal"]

@st.cache_data(ttl=60)
def fetch_omnipotent_data(extras, query):
    base = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&price_change_percentage=24h,7d,30d,200d"
    top_data = fetch_api(f"{base}&order=market_cap_desc&per_page=250&page=1")
    s_ids = ",".join(CORE_IDS + [x for x in extras if x])
    sentinel = fetch_api(f"{base}&ids={s_ids}")
    search = fetch_api(f"{base}&ids={query.lower().replace(' ', '-')}") if (query and len(query) >= 3) else []
    return top_data, sentinel, search

# --- [DEPLOYMENT] ---
with st.sidebar:
    st.title("🛡️ OMNI VAULT v2.0")
    m_key = st.text_input("Master Key", type="password")
    st.markdown("---")
    x_nodes = [st.text_input(f"Node #{i}") for i in range(17, 21)]

if m_key == MASTER_KEY:
    q = st.text_input("🔍 Neural Search Index", placeholder="Search 5000+ Assets...")
    top, sent, s_res = fetch_omnipotent_data(x_nodes, q)

    # UI: TURBO TICKER
    if top:
        t_html = "".join([f'<div class="glass-card"><b>{c["symbol"].upper()}</b>: ₹{c["current_price"]:,.0f} {get_neon_ind(c.get("price_change_percentage_24h"))}</div>' for c in (top[:20] + top[:20])])
        st.markdown(f'<div class="ticker-wrap"><div class="ticker">{t_html}</div></div>', unsafe_allow_html=True)

    # UI: MASTER RADAR
    st.markdown(f'<div class="radar-strip"><span>SENSEX: 74,119 {get_neon_ind(0.5)}</span> <span>NIFTY: 22,490 {get_neon_ind(0.8)}</span> <span>BTC: LIVE ⚡</span> <span>ETH: LIVE ⚡</span></div>', unsafe_allow_html=True)

    # UI: SENTINEL ALPHA (16 NODES)
    st.header("🛰️ Sentinel Alpha Command")
    if sent:
        df_s = pd.DataFrame([{
            "Rank": c.get("market_cap_rank"), "Logo": c.get("image"), 
            "Asset": c.get("name").upper() if c.get("id") != "everdome" else "HUM(AI)N (AI)",
            "Price": f"₹{c.get('current_price'):,.2f}",
            "24H": c.get('price_change_percentage_24h_in_currency'),
            "7D": c.get('price_change_percentage_7d_in_currency'),
            "30D": c.get('price_change_percentage_30d_in_currency'),
            "90D": c.get('price_change_percentage_200d_in_currency')
        } for c in sent])
        st.write(df_s.to_html(escape=False, formatters={"Logo": lambda x: f'<img src="{x}" width="30">', "24H": get_neon_ind, "7D": get_neon_ind, "30D": get_neon_ind, "90D": get_neon_ind}, index=False), unsafe_allow_html=True)

    # UI: GLOBAL MEGA NODE (WITH FULL INDICATORS)
    st.header("🌍 Global Mega Node")
    pool = s_res if (q and s_res) else (top[:150] if top else [])
    if pool:
        df_g = pd.DataFrame([{
            "Rank": i.get("market_cap_rank"), "Logo": i.get("image"), "Name": i.get("name"),
            "Price": f"₹{i.get('current_price', 0):,.2f}",
            "24H": i.get('price_change_percentage_24h_in_currency'),
            "7D": i.get('price_change_percentage_7d_in_currency'),
            "30D": i.get('price_change_percentage_30d_in_currency'),
            "90D": i.get('price_change_percentage_200d_in_currency')
        } for i in pool])
        st.write(df_g.to_html(escape=False, formatters={"Logo": lambda x: f'<img src="{x}" width="25">', "24H": get_neon_ind, "7D": get_neon_ind, "30D": get_neon_ind, "90D": get_neon_ind}, index=False), unsafe_allow_html=True)
else:
    st.warning("🔒 Sovereign Master, authentication required.")
                                                                                    
