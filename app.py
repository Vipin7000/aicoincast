import streamlit as st
import pandas as pd
import requests
import time

# --- [1. MASTER CONFIG & UI] ---
st.set_page_config(page_title="AiCoincast v49.0 Omni-Index", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

st.markdown("""
    <style>
    .stApp { background-color: #0A041A !important; }
    h1, h2, h3, h4, p, span, li { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] { background-color: #1A0B35 !important; border-right: 3px solid #00FF00 !important; }
    .ticker-wrap { background: #000; padding: 12px; border-bottom: 2px solid #00FF00; margin-bottom: 25px; }
    .ticker-text { color: #00FF00; font-weight: bold; font-size: 16px; font-family: 'Courier New', monospace; }
    [data-testid="stDataFrame"] { border: 1px solid #41444C; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

# [ALGO: PRECISION ENGINE]
def safe_float(val):
    try: return float(val) if val is not None else 0.0
    except: return 0.0

def format_price(val):
    return f"₹{safe_float(val):,.4f}"

def get_ind(val):
    if val > 0: return "🟢"
    elif val < 0: return "🔴"
    return "⚪"

# [MASTER ID LOCK - RE-VERIFIED MARCH 2026]
# Note: SIN and NFTB have low ranks, hence dedicated fetch is mandatory
MY_12_IDS = [
    "bitcoin", "ethereum", "virtual-protocol", "griffain", 
    "vaiot", "robonomics-network", "velas", "qanplatform", 
    "chaingpt", "sinverse", "polygon-ecosystem-token", "nftb"
]

@st.cache_data(ttl=300) # Increased cache for 3000-coin stability
def fetch_global_mega_data():
    all_global = []
    # 1. Sovereign 12 Dedicated (Force-Fetch)
    ids_sov = ",".join(MY_12_IDS)
    try:
        url_sov = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&ids={ids_sov}&sparkline=true&price_change_percentage=1h,24h,7d,30d"
        r_sov = requests.get(url_sov, timeout=15).json()
        
        # 2. Global 3000 Index (Batch Loading - Fetching 1000 for high-speed stability)
        for p in range(1, 5): 
            url_g = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_desc&per_page=250&page={p}&price_change_percentage=24h,7d,30d"
            r_batch = requests.get(url_g, timeout=15).json()
            if isinstance(r_batch, list): all_global.extend(r_batch)
            else: break
            time.sleep(1.2) # To avoid rate-limit 429 errors
            
        return r_sov, all_global
    except:
        return [], []

sov_data, global_market = fetch_global_mega_data()

# --- [2. TOP 20 LIVE TICKER - 4 DECIMAL] ---
if global_market:
    t_items = [f"{get_ind(safe_float(c.get('price_change_percentage_24h')))} {c['symbol'].upper()}: {format_price(c['current_price'])}" for c in global_market[:20]]
    st.markdown(f'<div class="ticker-wrap"><marquee class="ticker-text">🚀 LIVE MARKET FEED: {" | ".join(t_items)}</marquee></div>', unsafe_allow_html=True)

# --- [3. MAIN TERMINAL LOGIC] ---
if m_key == MASTER_KEY:
    t1, t2, t3, t4 = st.tabs(["📊 SENTINEL ALPHA", "📈 PERFORMANCE", "📰 BROADCAST", "⚖️ RISK ENGINE"])
    
    with t1:
        # --- SECTION 1: MY 12 SOVEREIGN LIST (WITH 1W & 1M) ---
        st.subheader("🛰️ Dedicated Tracker: My 12 Sovereign Assets")
        if sov_data:
            df_sov = []
            for c in sov_data:
                c24, c7d, c30d = safe_float(c.get('price_change_percentage_24h')), safe_float(c.get('price_change_percentage_7d_in_currency')), safe_float(c.get('price_change_percentage_30d_in_currency'))
                df_sov.append({
                    "Logo": c.get('image'),
                    "Asset": c.get('name').upper(),
                    "Price (INR)": format_price(c.get('current_price')),
                    "24H": f"{get_ind(c24)} {abs(c24):.1f}%",
                    "WEEKLY": f"{get_ind(c7d)} {abs(c7d):.1f}%",
                    "MONTHLY": f"{get_ind(c30d)} {abs(c30d):.1f}%",
                    "7D Trend Chart": c.get('sparkline_in_7d', {}).get('price', [])
                })
            # Locking the Sovereign 12 Table
            st.dataframe(
                pd.DataFrame(df_sov),
                column_config={
                    "Logo": st.column_config.ImageColumn("Logo"),
                    "7D Trend Chart": st.column_config.LineChartColumn("7D Trend Chart")
                },
                use_container_width=True, hide_index=True
            )
        else: st.warning("🔄 Sovereign Node Syncing (NFTB/SIN)...")

        st.divider()

        # --- SECTION 2: GLOBAL MEGA INDEX (3000 Scale) ---
        st.subheader(f"🌍 Global Mega Index ({len(global_market)} Assets Tracked)")
        if global_market:
            df_g = pd.DataFrame([{
                "Rank": c.get('market_cap_rank'),
                "Logo": c.get('image'),
                "Name": c.get('name'),
                "Price": format_price(c.get('current_price')),
                "24H": f"{get_ind(safe_float(c.get('price_change_percentage_24h')))} {abs(safe_float(c.get('price_change_percentage_24h'))):.1f}%",
                "1W": f"{get_ind(safe_float(c.get('price_change_percentage_7d_in_currency')))} {abs(safe_float(c.get('price_change_percentage_7d_in_currency'))):.1f}%",
                "1M": f"{get_ind(safe_float(c.get('price_change_percentage_30d_in_currency')))} {abs(safe_float(c.get('price_change_percentage_30d_in_currency'))):.1f}%"
            } for c in global_market])
            
            st.dataframe(
                df_g,
                column_config={"Logo": st.column_config.ImageColumn("Logo")},
                use_container_width=True, hide_index=True
            )

else: st.info("⚠️ Master Key Required to Unlock Sentinel Node.")
                
