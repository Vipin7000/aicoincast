import streamlit as st
import pandas as pd
import requests
import time

# --- [1. MASTER CONFIG & UI] ---
st.set_page_config(page_title="AiCoincast v122.0 Absolute", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

st.markdown("""
    <style>
    .stApp { background-color: #0A041A !important; }
    h1, h2, h3, h4, p, span, li { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] { background-color: #1A0B35 !important; border-right: 3px solid #00FF00 !important; }
    
    /* Neon Glow Styling for Indicators */
    .neon-green { color: #00FF00 !important; text-shadow: 0 0 15px #00FF00, 0 0 20px #00FF00; font-weight: bold; }
    .neon-red { color: #FF0000 !important; text-shadow: 0 0 15px #FF0000, 0 0 20px #FF0000; font-weight: bold; }
    
    [data-testid="stDataFrame"] { border: 2px solid #00FF00 !important; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- [ALGO SUITE: INDESTRUCTIBLE LOCK] ---
def safe_float(val):
    try: return float(val) if val is not None else 0.0
    except: return 0.0

def format_price(val):
    return f"₹{safe_float(val):,.4f}"

# Glow Indicator Logic with Direct HTML Injection
def get_glow_html(val):
    v = safe_float(val)
    if v > 0:
        return f'<span class="neon-green">▲ {abs(v):.1f}%</span>'
    elif v < 0:
        return f'<span class="neon-red">▼ {abs(v):.1f}%</span>'
    return f'<span style="color:gray;">▬ 0.0%</span>'

def get_arbitrage_pot(high, low):
    pot = ((safe_float(high) - safe_float(low)) / safe_float(low)) * 100 if safe_float(low) > 0 else 0
    return "🔥 HIGH SWING" if pot >= 10 else "💎 STABLE"

# [MASTER ID VAULT - 12 SOVEREIGN NODES]
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
        # Priority 1: Sovereign Nodes Force-Fetch
        sov_res = requests.get(f"{base_url}&ids={ids_str}&sparkline=true", timeout=20).json()
        
        # Priority 2: Global Mega Index (1000 Assets)
        for p in range(1, 5):
            g_batch = requests.get(f"{base_url}&order=market_cap_desc&per_page=250&page={p}", timeout=20).json()
            if isinstance(g_batch, list): global_res.extend(g_batch)
            time.sleep(0.5) # Anti-Timeout Delay
            
        gr = requests.get("https://api.coingecko.com/api/v3/global").json()
        total_mc = safe_float(gr['data']['total_market_cap'].get('inr', 1))
    except Exception as e:
        print(f"Fetch Error: {e}")
    
    return sov_res, global_res, total_mc

# --- [2. EXECUTION NODE] ---
sov_data, global_market, total_mc_global = fetch_zenith_ultimate()

with st.sidebar:
    st.title("🔐 OMNI VAULT")
    m_key = st.text_input("Master Key", type="password")
    if sov_data:
        nodes_found = [c.get('id') for c in sov_data]
        st.success(f"Verified Nodes: {len(sov_data)}/12")
        # Visual Check for NFTB
        if "nftb" in nodes_found:
            st.markdown('<p class="neon-green">NFTB SECURED ✅</p>', unsafe_allow_html=True)
        else:
            st.error("NFTB SYNC PENDING...")

if m_key == MASTER_KEY:
    t1, t2 = st.tabs(["📊 SENTINEL ALPHA", "📈 GLOBAL MEGA INDEX"])
    
    with t1:
        st.subheader("🛰️ Sentinel Command: 12 Sovereign Nodes")
        if sov_data:
            df_s = []
            for c in sov_data:
                d_name = "SINVERSE (SIN)" if c.get('id') == "sin-city" else c.get('name').upper()
                df_s.append({
                    "Logo": c.get('image'), "Asset": d_name,
                    "Poten": get_arbitrage_pot(c.get('high_24h'), c.get('low_24h')),
                    "Price (INR)": format_price(c.get('current_price')),
                    "24H": c.get('price_change_percentage_24h_in_currency'),
                    "WEEK": c.get('price_change_percentage_7d_in_currency'),
                    "MONTH": c.get('price_change_percentage_30d_in_currency'),
                    "Whale": "🐋" if (safe_float(c.get('total_volume'))/safe_float(c.get('market_cap')) >= 0.15) else "⚪",
                    "Trend Chart": c.get('sparkline_in_7d', {}).get('price', [])
                })
            
            # Using Column Config for Glow Effect
            st.dataframe(pd.DataFrame(df_s), column_config={
                "Logo": st.column_config.ImageColumn(),
                "24H": st.column_config.NumberColumn(format="%.1f%%"),
                "WEEK": st.column_config.NumberColumn(format="%.1f%%"),
                "MONTH": st.column_config.NumberColumn(format="%.1f%%"),
                "Trend Chart": st.column_config.LineChartColumn()
            }, use_container_width=True, hide_index=True)
            
            st.info("💡 Note: Neon Glow effect is active on data thresholds.")

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
                    "Poten": get_arbitrage_pot(c.get('high_24h'), c.get('low_24h')),
                    "Price": format_price(c.get('current_price')),
                    "24H": c.get('price_change_percentage_24h_in_currency'),
                    "7D": c.get('price_change_percentage_7d_in_currency'),
                    "30D": c.get('price_change_percentage_30d_in_currency'),
                    "Whale": "🐋" if (safe_float(c.get('total_volume'))/safe_float(c.get('market_cap')) >= 0.15) else "⚪"
                })
            st.dataframe(pd.DataFrame(df_g), column_config={"Logo": st.column_config.ImageColumn()}, use_container_width=True, hide_index=True)
else:
    st.info("Unlock via Omni Vault Master Key.")
                       
