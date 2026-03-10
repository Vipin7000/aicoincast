import streamlit as st
import pandas as pd
import requests
import time

# --- [1. MASTER CONFIG & UI] ---
st.set_page_config(page_title="AiCoincast v124.0 Final", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

st.markdown("""
    <style>
    .stApp { background-color: #0A041A !important; }
    h1, h2, h3, h4, p, span, li { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] { background-color: #1A0B35 !important; border-right: 3px solid #00FF00 !important; }
    [data-testid="stDataFrame"] { border: 2px solid #00FF00 !important; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- [ALGO SUITE: LOCKED] ---
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

# [MASTER ID VAULT - RE-VERIFIED 12]
MY_12_IDS = [
    "bitcoin", "ethereum", "polygon-ecosystem-token", "virtual-protocol",
    "qanplatform", "chaingpt", "velas", "griffain",
    "vaiot", "sin-city", "nftb", "robonomics-network"
]

@st.cache_data(ttl=60)
def fetch_zenith_ultimate():
    sov_res, global_res, total_mc = [], [], 1.0
    ids_str = ",".join(MY_12_IDS)
    base_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&price_change_percentage=24h,7d,30d"
    
    try:
        # Layer 1: Force Fetch Sovereign (Including NFTB)
        sov_res = requests.get(f"{base_url}&ids={ids_str}&sparkline=true", timeout=20).json()
        
        # Layer 2: Global 1000 Assets
        for p in range(1, 5):
            g_batch = requests.get(f"{base_url}&order=market_cap_desc&per_page=250&page={p}", timeout=20).json()
            if isinstance(g_batch, list): global_res.extend(g_batch)
            time.sleep(0.4)
            
        gr = requests.get("https://api.coingecko.com/api/v3/global").json()
        total_mc = safe_float(gr['data']['total_market_cap'].get('inr', 1))
    except: pass
    return sov_res, global_res, total_mc

# --- [2. EXECUTION] ---
sov_data, global_market, total_mc_global = fetch_zenith_ultimate()

with st.sidebar:
    st.title("🔐 OMNI VAULT")
    m_key = st.text_input("Master Key", type="password")
    if sov_data:
        # Final Force Validation
        st.success(f"Verified Nodes: {len(sov_data)}/12")
        found_ids = [c.get('id') for c in sov_data]
        if "nftb" in found_ids:
            st.info("NFTB Node: SECURED ✅")

if m_key == MASTER_KEY:
    t1, t2 = st.tabs(["📊 SENTINEL ALPHA", "📈 GLOBAL MEGA INDEX"])
    
    with t1:
        st.subheader("🛰️ Sentinel Command: 12 Sovereign Nodes")
        if sov_data:
            df_s = []
            for c in sov_data:
                name = "SINVERSE (SIN)" if c.get('id') == "sin-city" else c.get('name').upper()
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

    with t2:
        st.subheader(f"🌍 Global Mega Index ({len(global_market)} Assets)")
        q_search = st.text_input("🔍 Search Node...")
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
    st.info("Enter Master Key to Unlock.")
