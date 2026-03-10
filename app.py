import streamlit as st
import pandas as pd
import requests
import time

# --- [1. MASTER CONFIG & UI] ---
st.set_page_config(page_title="AiCoincast v136.0 Dual-Protocol", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

st.markdown("""
    <style>
    .stApp { background-color: #0A041A !important; }
    h1, h2, h3, h4, p, span, li { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] { background-color: #1A0B35 !important; border-right: 3px solid #00FF00 !important; }
    
    /* Neon Glow Styling */
    .glow-pos { color: #00FF00 !important; text-shadow: 0 0 10px #00FF00; font-weight: bold; }
    .glow-neg { color: #FF0000 !important; text-shadow: 0 0 10px #FF0000; font-weight: bold; }
    
    [data-testid="stDataFrame"] { border: 2px solid #00FF00 !important; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- [ALGO SUITE: v136 ABSOLUTE LOCK] ---
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

# [MASTER ID VAULT - SPLIT INTO TWO FOLDERS]
FOLDER_1_IDS = [
    "bitcoin", "ethereum", "polygon-ecosystem-token", "virtual-protocol",
    "qanplatform", "chaingpt", "velas", "griffain",
    "vaiot", "sin-city", "robonomics-network", "unmarshal", "bloktopia"
]
# Folder 2: LayerAI and NFTB (Alpha Spec Nodes)
FOLDER_2_IDS = ["layerai", "nftb", "everdome"] # Added everdome here for stable tracking

@st.cache_data(ttl=60)
def fetch_sovereign_intelligence():
    f1_res, f2_res, global_res = [], [], []
    base_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&price_change_percentage=24h,7d,30d"
    
    try:
        # Fetch Folder 1
        f1_res = requests.get(f"{base_url}&ids={','.join(FOLDER_1_IDS)}&sparkline=true", timeout=20).json()
        
        # Fetch Folder 2 (High-Priority Force-Fetch)
        f2_res = requests.get(f"{base_url}&ids={','.join(FOLDER_2_IDS)}&sparkline=true", timeout=20).json()
        
        # Global Mega Index
        g_batch = requests.get(f"{base_url}&order=market_cap_desc&per_page=100&page=1").json()
        if isinstance(g_batch, list): global_res = g_batch
    except: pass
    return f1_res, f2_res, global_res

# --- [2. EXECUTION] ---
f1_data, f2_data, g_data = fetch_sovereign_intelligence()

with st.sidebar:
    st.title("🔐 OMNI VAULT")
    m_key = st.text_input("Master Key", type="password", placeholder="••••••••")
    if f1_data and f2_data:
        total_nodes = len(f1_data) + len(f2_data)
        st.success(f"Verified Nodes: {total_nodes}/15")
        st.info("Folder 2 (LAI & NFTB): LOCKED ✅")

if m_key == MASTER_KEY:
    tabs = st.tabs(["📊 FOLDER 1: SENTINEL", "💎 FOLDER 2: ALPHA SPEC", "🌍 GLOBAL INDEX"])
    
    # --- FOLDER 1 ---
    with tabs[0]:
        st.header("🛰️ Sentinel Command (13 Nodes)")
        if f1_data:
            df1 = []
            for c in f1_data:
                df1.append({
                    "Logo": c.get('image'), "Asset": c.get('name').upper(),
                    "Price (INR)": format_price(c.get('current_price')),
                    "24H": get_glow_ind(c.get('price_change_percentage_24h_in_currency')),
                    "WEEK": get_glow_ind(c.get('price_change_percentage_7d_in_currency')),
                    "Whale": "🐋" if (safe_float(c.get('total_volume'))/safe_float(c.get('market_cap')) >= 0.15) else "⚪"
                })
            st.dataframe(pd.DataFrame(df1), column_config={"Logo": st.column_config.ImageColumn()}, use_container_width=True, hide_index=True)

    # --- FOLDER 2: LAI & NFTB ---
    with tabs[1]:
        st.header("💎 Folder 2: Alpha Spec (LAI & NFTB)")
        if f2_data:
            df2 = []
            for c in f2_data:
                name = c.get('name').upper()
                if c.get('id') == "layerai": name = "LAYERAI (LAI)"
                if c.get('id') == "everdome": name = "HUM(AI)N (AI)"
                if c.get('id') == "nftb": name = "NFTB (NFTB)"
                
                df2.append({
                    "Logo": c.get('image'), "Asset": name,
                    "Price (INR)": format_price(c.get('current_price')),
                    "24H": get_glow_ind(c.get('price_change_percentage_24h_in_currency')),
                    "WEEK": get_glow_ind(c.get('price_change_percentage_7d_in_currency')),
                    "MONTH": get_glow_ind(c.get('price_change_percentage_30d_in_currency')),
                    "Whale": "🐋" if (safe_float(c.get('total_volume'))/safe_float(c.get('market_cap')) >= 0.15) else "⚪"
                })
            st.dataframe(pd.DataFrame(df2), column_config={"Logo": st.column_config.ImageColumn()}, use_container_width=True, hide_index=True)
            st.success("Folder 2 nodes are being fetched via priority bypass.")

    # --- GLOBAL INDEX ---
    with tabs[2]:
        st.header("🌍 Global Market Index")
        if g_data:
            dfg = [{"Rank": c['market_cap_rank'], "Name": c['name'], "Price": format_price(c['current_price']), "24H": get_glow_ind(c['price_change_percentage_24h_in_currency'])} for c in g_data]
            st.dataframe(pd.DataFrame(dfg), use_container_width=True, hide_index=True)

else:
    st.info("Enter Master Key to Unlock Sovereign Access.")
    
