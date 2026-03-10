import streamlit as st
import pandas as pd
import requests
import time

# --- [1. MASTER CONFIG & UI] ---
st.set_page_config(page_title="AiCoincast v142.0 Final", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

st.markdown("""
    <style>
    .stApp { background-color: #0A041A !important; }
    h1, h2, h3, h4, p, span, li { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] { background-color: #1A0B35 !important; border-right: 3px solid #00FF00 !important; }
    
    /* Absolute Neon Glow Styling */
    .glow-pos { color: #00FF00 !important; text-shadow: 0 0 12px #00FF00; font-weight: bold; }
    .glow-neg { color: #FF0000 !important; text-shadow: 0 0 12px #FF0000; font-weight: bold; }
    
    [data-testid="stDataFrame"] { border: 2px solid #00FF00 !important; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- [CORE ALGORITHMS: v142 ABSOLUTE] ---
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

# [MASTER ID VAULT]
F1_IDS = ["bitcoin", "ethereum", "polygon-ecosystem-token", "virtual-protocol", "qanplatform", "chaingpt", "velas", "griffain", "vaiot", "sin-city", "robonomics-network", "unmarshal"]
F2_IDS = ["layerai", "nftb", "everdome", "bloktopia"]

@st.cache_data(ttl=60)
def fetch_zenith_final():
    f1_res, f2_res, g_res, total_mc = [], [], [], 1.0
    base_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&price_change_percentage=24h,7d,30d"
    
    try:
        f1_res = requests.get(f"{base_url}&ids={','.join(F1_IDS)}&sparkline=true", timeout=15).json()
        f2_res = requests.get(f"{base_url}&ids={','.join(F2_IDS)}&sparkline=true", timeout=15).json()
        
        # Global Mega Index (Buffer 200)
        g_batch = requests.get(f"{base_url}&order=market_cap_desc&per_page=200&page=1", timeout=15).json()
        if isinstance(g_batch, list): g_res = g_batch
        
        gr_data = requests.get("https://api.coingecko.com/api/v3/global", timeout=10).json()
        total_mc = safe_float(gr_data['data']['total_market_cap'].get('inr', 1))
    except: pass
    return f1_res, f2_res, g_res, total_mc

# --- [2. EXECUTION] ---
f1, f2, g_market, global_mc = fetch_zenith_final()

with st.sidebar:
    st.title("🔐 OMNI VAULT")
    m_key = st.text_input("Master Key", type="password", placeholder="••••••••")
    if isinstance(f1, list) and isinstance(f2, list):
        st.success(f"Verified Nodes: {len(f1) + len(f2)}/16")

if m_key == MASTER_KEY:
    tabs = st.tabs(["📊 FOLDER 1: SENTINEL", "💎 FOLDER 2: ALPHA SPEC", "🌍 GLOBAL NODE"])
    
    with tabs[0]:
        st.header("🛰️ Sentinel Command: Primary Alpha")
        if f1:
            df1 = []
            for c in f1:
                df1.append({
                    "Logo": c.get('image'), "Asset": c.get('name', 'N/A').upper(),
                    "Poten": get_arbitrage_pot(c.get('high_24h'), c.get('low_24h')),
                    "Price (INR)": format_price(c.get('current_price')),
                    "24H": get_glow_ind(c.get('price_change_percentage_24h_in_currency')),
                    "WEEK": get_glow_ind(c.get('price_change_percentage_7d_in_currency')),
                    "Whale": "🐋" if (safe_float(c.get('total_volume'))/safe_float(c.get('market_cap')) >= 0.15) else "⚪"
                })
            st.dataframe(pd.DataFrame(df1), column_config={"Logo": st.column_config.ImageColumn()}, use_container_width=True, hide_index=True)

    with tabs[1]:
        st.header("💎 Folder 2: Alpha Spec (LAI & NFTB Focus)")
        if f2:
            df2 = []
            for c in f2:
                name = "HUM(AI)N (AI)" if c.get('id') == "everdome" else c.get('name', 'N/A').upper()
                df2.append({
                    "Logo": c.get('image'), "Asset": name,
                    "Price (INR)": format_price(c.get('current_price')),
                    "24H": get_glow_ind(c.get('price_change_percentage_24h_in_currency')),
                    "WEEK": get_glow_ind(c.get('price_change_percentage_7d_in_currency')),
                    "MONTH": get_glow_ind(c.get('price_change_percentage_30d_in_currency')),
                    "Whale": "🐋" if (safe_float(c.get('total_volume'))/safe_float(c.get('market_cap')) >= 0.15) else "⚪"
                })
            st.dataframe(pd.DataFrame(df2), column_config={"Logo": st.column_config.ImageColumn()}, use_container_width=True, hide_index=True)

    with tabs[2]:
        st.header("🌍 Global Market Index")
        q_search = st.text_input("🔍 Search Global Node...")
        if g_market:
            filtered = [c for c in g_market if q_search.lower() in c.get('name', '').lower() or q_search.lower() in c.get('symbol', '').lower()]
            df_g = []
            for c in filtered:
                df_g.append({
                    "Rank": c.get('market_cap_rank'), "Logo": c.get('image'), "Name": c.get('name', 'N/A'),
                    "Authority": f"{(safe_float(c.get('market_cap'))/global_mc*100):.2f}%",
                    "Price": format_price(c.get('current_price')),
                    "24H": get_glow_ind(c.get('price_change_percentage_24h_in_currency')),
                    "Whale": "🐋" if (safe_float(c.get('total_volume'))/safe_float(c.get('market_cap')) >= 0.15) else "⚪"
                })
            st.dataframe(pd.DataFrame(df_g), column_config={"Logo": st.column_config.ImageColumn()}, use_container_width=True, hide_index=True)
else:
    st.info("Sovereign Master, please enter Master Key to unlock.")
            
