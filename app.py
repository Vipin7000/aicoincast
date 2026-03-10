import streamlit as st
import pandas as pd
import requests

# --- [1. MASTER CONFIG & UI] ---
st.set_page_config(page_title="AiCoincast v52.0 Core", layout="wide")
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

# [MASTER ID LOCK - RE-VERIFIED FOR NFTB & SINVERSE]
MY_12_IDS = [
    "bitcoin", "ethereum", "virtual-protocol", "griffain", 
    "vaiot", "robonomics-network", "velas", "qanplatform", 
    "chaingpt", "sin-city", "polygon-ecosystem-token", "nftb"
]

@st.cache_data(ttl=60)
def fetch_core_intelligence():
    ids_sov = ",".join(MY_12_IDS)
    try:
        # A. Sovereign 12 (Dedicated Node - Force Fetch)
        url_sov = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&ids={ids_sov}&sparkline=true&price_change_percentage=24h,7d,30d"
        r_sov = requests.get(url_sov, timeout=15).json()
        
        # B. Global Market (Ticker & Index Context)
        url_g = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_desc&per_page=250&page=1&sparkline=false&price_change_percentage=24h,7d,30d"
        r_g = requests.get(url_g, timeout=15).json()
        
        return (r_sov if isinstance(r_sov, list) else []), (r_g if isinstance(r_g, list) else [])
    except:
        return [], []

sov_data, global_market = fetch_core_intelligence()

# --- [2. TOP 20 LIVE TICKER] ---
if global_market:
    t_items = [f"{get_ind(safe_float(c.get('price_change_percentage_24h')))} {c['symbol'].upper()}: {format_price(c['current_price'])}" for c in global_market[:20]]
    st.markdown(f'<div class="ticker-wrap"><marquee class="ticker-text">🛰️ OMNI-FEED LIVE: {" | ".join(t_items)}</marquee></div>', unsafe_allow_html=True)

# --- [3. SIDEBAR VAULT - DEFINED FIRST TO AVOID NAMEERROR] ---
with st.sidebar:
    st.title("🔐 OMNI VAULT")
    m_key = st.text_input("Master Key", type="password", placeholder="••••••••")
    if sov_data:
        tmc = sum([safe_float(c.get('market_cap', 0)) for c in sov_data])
        st.info(f"💼 Sovereign MC: ₹{tmc:,.0f}")
        st.success(f"Tracked Assets: {len(sov_data)}/12")

# --- [4. MAIN TERMINAL LOGIC] ---
if m_key == MASTER_KEY:
    t1, t2, t3, t4 = st.tabs(["📊 SENTINEL ALPHA", "📈 PERFORMANCE", "📰 BROADCAST", "⚖️ RISK ENGINE"])
    
    with t1:
        st.subheader("🛰️ Sentinel Command: Sovereign 12 Intelligence")
        if sov_data:
            df_sov = []
            for c in sov_data:
                # Labeling Rebranded Coins correctly for display
                name = "SINVERSE (SIN)" if c.get('id') == "sin-city" else c.get('name').upper()
                c24, c7d, c30d = safe_float(c.get('price_change_percentage_24h')), safe_float(c.get('price_change_percentage_7d_in_currency')), safe_float(c.get('price_change_percentage_30d_in_currency'))
                
                df_sov.append({
                    "Logo": c.get('image'),
                    "Asset": name,
                    "Price (INR)": format_price(c.get('current_price')),
                    "24H": f"{get_ind(c24)} {abs(c24):.1f}%",
                    "7D (WEEK)": f"{get_ind(c7d)} {abs(c7d):.1f}%",
                    "30D (MONTH)": f"{get_ind(c30d)} {abs(c30d):.1f}%",
                    "7D Trend": c.get('sparkline_in_7d', {}).get('price', [])
                })
            st.dataframe(pd.DataFrame(df_sov), column_config={"Logo": st.column_config.ImageColumn("Logo"), "7D Trend": st.column_config.LineChartColumn("7D Trend")}, use_container_width=True, hide_index=True)
        else:
            st.warning("🔄 Re-syncing Sovereign Nodes...")

        st.divider()

        st.subheader(f"🌍 Global Mega Index ({len(global_market)} Assets)")
        if global_market:
            df_g = pd.DataFrame([{
                "Rank": c.get('market_cap_rank'),
                "Logo": c.get('image'),
                "Name": c.get('name'),
                "Price": format_price(c.get('current_price')),
                "24H": f"{get_ind(safe_float(c.get('price_change_percentage_24h')))} {abs(safe_float(c.get('price_change_percentage_24h'))):.1f}%",
                "1W": f"{get_ind(safe_float(c.get('price_change_percentage_7d_in_currency')))} {abs(safe_float(c.get('price_change_percentage_7d_in_currency'))):.1f}%"
            } for c in global_market])
            st.dataframe(df_g, column_config={"Logo": st.column_config.ImageColumn("Logo")}, use_container_width=True, hide_index=True)

else:
    st.info("⚠️ Master Key Required to Access Node.")
                
