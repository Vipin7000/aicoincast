import streamlit as st
import pandas as pd
import requests
import time

# --- [1. MASTER CONFIG & UI] ---
st.set_page_config(page_title="AiCoincast v144.0 Zenith", layout="wide")
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

# --- [ALGO SUITE: v144 ABSOLUTE] ---
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

# [MASTER ID VAULT - THE 16 SOVEREIGN NODES]
MY_16_IDS = [
    "bitcoin", "ethereum", "polygon-ecosystem-token", "virtual-protocol",
    "qanplatform", "chaingpt", "velas", "griffain",
    "vaiot", "sin-city", "layerai", "robonomics-network",
    "unmarshal", "everdome", "bloktopia", "nftb"
]

@st.cache_data(ttl=60)
def fetch_zenith_intelligence():
    sov_res, global_res, total_mc = [], [], 1.0
    ids_str = ",".join(MY_16_IDS)
    base_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&price_change_percentage=24h,7d,30d"
    
    try:
        # Step 1: Force Fetch All 16 (Bypass Rank Filtering)
        sov_res = requests.get(f"{base_url}&ids={ids_str}&sparkline=true", timeout=25).json()
        
        # Step 2: Global Node (Buffer 250 Assets)
        g_batch = requests.get(f"{base_url}&order=market_cap_desc&per_page=250&page=1", timeout=25).json()
        if isinstance(g_batch, list): global_res = g_batch
        
        # Market Authority
        gr = requests.get("https://api.coingecko.com/api/v3/global", timeout=15).json()
        total_mc = safe_float(gr['data']['total_market_cap'].get('inr', 1))
    except: pass
    return sov_res, global_res, total_mc

# --- [2. EXECUTION] ---
sov_data, g_market, global_mc = fetch_zenith_intelligence()

with st.sidebar:
    st.title("🔐 OMNI VAULT")
    m_key = st.text_input("Master Key", type="password", placeholder="••••••••")
    if isinstance(sov_data, list):
        st.success(f"Verified Nodes: {len(sov_data)}/16")

if m_key == MASTER_KEY:
    tabs = st.tabs(["📊 SENTINEL ALPHA (16)", "🌍 GLOBAL MEGA NODE"])
    
    with tabs[0]:
        st.header("🛰️ Sentinel Command: 16 Sovereign Nodes")
        if sov_data:
            df_s = []
            # Order Lock
            sorted_sov = sorted(sov_data, key=lambda x: MY_16_IDS.index(x['id']) if x['id'] in MY_16_IDS else 99)
            
            for c in sorted_sov:
                # Rebrand & Display Mappings
                name = c.get('name', 'Syncing...').upper()
                if c.get('id') == "sin-city": name = "SINVERSE (SIN)"
                if c.get('id') == "layerai": name = "LAYERAI (LAI)"
                if c.get('id') == "everdome": name = "HUM(AI)N (AI)"
                
                df_s.append({
                    "Logo": c.get('image'), "Asset": name,
                    "Poten": get_arbitrage_pot(c.get('high_24h'), c.get('low_24h')),
                    "Price (INR)": format_price(c.get('current_price')),
                    "24H": get_glow_ind(c.get('price_change_percentage_24h_in_currency')),
                    "WEEK": get_glow_ind(c.get('price_change_percentage_7d_in_currency')),
                    "MONTH": get_glow_ind(c.get('price_change_percentage_30d_in_currency')),
                    "Whale": "🐋" if (safe_float(c.get('total_volume'))/safe_float(c.get('market_cap')) >= 0.15) else "⚪"
                })
            st.dataframe(pd.DataFrame(df_s), column_config={"Logo": st.column_config.ImageColumn()}, use_container_width=True, hide_index=True)

    with tabs[1]:
        st.header("🌍 Global Market Sentinel")
        q_search = st.text_input("🔍 Quick Search Asset...", placeholder="Enter name or symbol...")
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
    st.info("Unlock via Master Key.")
                
