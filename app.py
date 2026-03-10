import streamlit as st
import pandas as pd
import requests
import time

# --- [1. MASTER CONFIG & UI] ---
st.set_page_config(page_title="AiCoincast v127.0 Pantheon", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

st.markdown("""
    <style>
    .stApp { background-color: #0A041A !important; }
    h1, h2, h3, h4, p, span, li { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] { background-color: #1A0B35 !important; border-right: 3px solid #00FF00 !important; }
    
    /* Neon Glow Styling */
    .glow-pos { color: #00FF00 !important; text-shadow: 0 0 12px #00FF00; font-weight: bold; }
    .glow-neg { color: #FF0000 !important; text-shadow: 0 0 12px #FF0000; font-weight: bold; }
    
    [data-testid="stDataFrame"] { border: 2px solid #00FF00 !important; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- [ALGO SUITE: v127 LOCKED] ---
def safe_float(val):
    try: return float(val) if val is not None else 0.0
    except: return 0.0

def format_price(val):
    return f"₹{safe_float(val):,.4f}"

def get_glow_ind(val):
    v = safe_float(val)
    if v > 0: return f"🟢 ▲ {abs(v):.1f}%"
    elif v < 0: return f"🔴 ▼ {abs(v):.1f}%"
    return f"▬ 0.0%"

def get_arbitrage_pot(high, low):
    pot = ((safe_float(high) - safe_float(low)) / safe_float(low)) * 100 if safe_float(low) > 0 else 0
    return "🔥 HIGH SWING" if pot >= 10 else "💎 STABLE"

# [MASTER ID VAULT - 15 SOVEREIGN NODES]
MY_15_IDS = [
    "bitcoin", "ethereum", "polygon-ecosystem-token", "virtual-protocol",
    "qanplatform", "chaingpt", "velas", "griffain",
    "vaiot", "sin-city", "layerai", "robonomics-network",
    "unmarshal", "everdome", "bloktopia"
]

@st.cache_data(ttl=60)
def fetch_pantheon_intelligence():
    sov_res, global_res, total_mc = [], [], 1.0
    ids_str = ",".join(MY_15_IDS)
    base_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&price_change_percentage=24h,7d,30d"
    
    try:
        # Layer 1: Force Fetch Sovereign 15
        sov_res = requests.get(f"{base_url}&ids={ids_str}&sparkline=true", timeout=25).json()
        
        # Layer 2: Global Mega Index (Multi-page buffering)
        for p in range(1, 5):
            g_batch = requests.get(f"{base_url}&order=market_cap_desc&per_page=250&page={p}", timeout=25).json()
            if isinstance(g_batch, list): global_res.extend(g_batch)
            time.sleep(0.4)
            
        gr = requests.get("https://api.coingecko.com/api/v3/global").json()
        total_mc = safe_float(gr['data']['total_market_cap'].get('inr', 1))
    except: pass
    return sov_res, global_res, total_mc

# --- [2. EXECUTION] ---
sov_data, global_market, total_mc_global = fetch_pantheon_intelligence()

with st.sidebar:
    st.title("🔐 OMNI VAULT")
    m_key = st.text_input("Master Key", type="password", placeholder="••••••••")
    if sov_data:
        st.success(f"Verified Nodes: {len(sov_data)}/15")
        if "layerai" in [c.get('id') for c in sov_data]:
            st.info("LAI Position Locked ✅")

if m_key == MASTER_KEY:
    # --- SECTION 1: SENTINEL ALPHA (PRIORITY 15) ---
    st.header("🛰️ Sentinel Command: 15 Sovereign Nodes")
    if sov_data:
        df_s = []
        for c in sov_data:
            name = c.get('name').upper()
            if c.get('id') == "sin-city": name = "SINVERSE (SIN)"
            
            df_s.append({
                "Logo": c.get('image'), "Asset": name,
                "Poten": get_arbitrage_pot(c.get('high_24h'), c.get('low_24h')),
                "Price (INR)": format_price(c.get('current_price')),
                "24H": get_glow_ind(c.get('price_change_percentage_24h_in_currency')),
                "WEEK": get_glow_ind(c.get('price_change_percentage_7d_in_currency')),
                "MONTH": get_glow_ind(c.get('price_change_percentage_30d_in_currency')),
                "Whale": "🐋" if (safe_float(c.get('total_volume'))/safe_float(c.get('market_cap')) >= 0.15) else "⚪",
                "Trend": c.get('sparkline_in_7d', {}).get('price', [])
            })
        st.dataframe(pd.DataFrame(df_s), column_config={"Logo": st.column_config.ImageColumn(), "Trend": st.column_config.LineChartColumn()}, use_container_width=True, hide_index=True)

    st.markdown("---")

    # --- SECTION 2: GLOBAL MEGA INDEX ---
    st.header(f"🌍 Global Mega Index ({len(global_market)} Assets)")
    q_search = st.text_input("🔍 Quick Search Node...", placeholder="Search symbols or names globally...")
    if global_market:
        filtered = [c for c in global_market if q_search.lower() in c['name'].lower() or q_search.lower() in c['symbol'].lower()]
        df_g = []
        for c in filtered:
            df_g.append({
                "Rank": c.get('market_cap_rank'), "Logo": c.get('image'), "Name": c.get('name'),
                "Authority": f"{(safe_float(c.get('market_cap'))/total_mc_global*100):.2f}%",
                "Price": format_price(c.get('current_price')),
                "24H": get_glow_ind(c.get('price_change_percentage_24h_in_currency')),
                "7D": get_glow_ind(c.get('price_change_percentage_7d_in_currency')),
                "30D": get_glow_ind(c.get('price_change_percentage_30d_in_currency')),
                "Whale": "🐋 Whale Alert" if (safe_float(c.get('total_volume'))/safe_float(c.get('market_cap')) >= 0.15) else "⚪"
            })
        st.dataframe(pd.DataFrame(df_g), column_config={"Logo": st.column_config.ImageColumn()}, use_container_width=True, hide_index=True)

else:
    st.info("Enter Master Key to Unlock Sovereign Pantheon.")
