import streamlit as st
import pandas as pd
import requests

# --- [1. MASTER CONFIG & UI] ---
st.set_page_config(page_title="AiCoincast v43.0 Zenith", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

st.markdown("""
    <style>
    .stApp { background-color: #0A041A !important; }
    h1, h2, h3, h4, p, span, li { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] { background-color: #1A0B35 !important; border-right: 3px solid #00FF00 !important; }
    
    /* Neon Ticker Design */
    .ticker-wrap { background: #000; padding: 12px; border-bottom: 2px solid #00FF00; margin-bottom: 25px; }
    .ticker-text { color: #00FF00; font-weight: bold; font-size: 16px; font-family: 'Courier New', monospace; }
    
    /* Global Table Customization */
    [data-testid="stDataFrame"] { border: 1px solid #41444C; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

# [ALGO: ABSOLUTE ERROR SHIELD]
def safe_float(val):
    try:
        if val is None or val == "": return 0.0
        return float(val)
    except: return 0.0

def get_ind(val):
    if val > 0: return "🟢"
    elif val < 0: return "🔴"
    return "⚪"

# [MASTER ID LOCK - SIN RESTORED]
MY_12_IDS = [
    "bitcoin", "ethereum", "virtual-protocol", "griffain", 
    "vaiot", "robonomics-network", "velas", "qanplatform", 
    "chaingpt", "sin-city", "polygon-ecosystem-token", "nftb"
]

@st.cache_data(ttl=60)
def fetch_zenith_data():
    ids_sov = ",".join(MY_12_IDS)
    try:
        # A. Sovereign 12 Dedicated (Including SIN-City Re-mapping)
        url_sov = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&ids={ids_sov}&sparkline=true&price_change_percentage=24h,7d,30d"
        r_sov = requests.get(url_sov, timeout=15).json()
        
        # B. Global Market (Ticker & Index)
        url_g = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_desc&per_page=250&page=1&sparkline=false&price_change_percentage=24h,7d,30d"
        r_g = requests.get(url_g, timeout=15).json()
        
        return (r_sov if isinstance(r_sov, list) else []), (r_g if isinstance(r_g, list) else [])
    except:
        return [], []

sov_data, global_market = fetch_zenith_data()

# --- [2. TOP 20 LIVE TICKER - RESTORED] ---
if global_market:
    t_items = [f"{get_ind(safe_float(c.get('price_change_percentage_24h')))} {c['symbol'].upper()}: ₹{safe_float(c['current_price']):,.0f}" for c in global_market[:20]]
    st.markdown(f'<div class="ticker-wrap"><marquee class="ticker-text">🚀 LIVE MARKET NODES: {" | ".join(t_items)}</marquee></div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="ticker-wrap"><marquee class="ticker-text">🔄 RECONNECTING TO GLOBAL NODES...</marquee></div>', unsafe_allow_html=True)

# --- [3. SIDEBAR VAULT] ---
with st.sidebar:
    st.title("🔐 OMNI VAULT")
    m_key = st.text_input("Master Key", type="password", placeholder="••••••••")
    if sov_data:
        tmc = sum([safe_float(c.get('market_cap', 0)) for c in sov_data])
        st.info(f"💼 Sovereign MC: ₹{tmc:,.0f}")
        st.success("📈 NIFTY 50: 22,493.50 (+0.45%)")

# --- [4. MAIN TERMINAL LOGIC] ---
if m_key == MASTER_KEY:
    t1, t2, t3, t4 = st.tabs(["📊 SENTINEL ALPHA", "📈 PERFORMANCE", "📰 BROADCAST", "⚖️ RISK ENGINE"])
    
    with t1:
        # SECTION 1: MY 12 SOVEREIGN TRACKER (SIN RESTORED)
        st.subheader("🛰️ Sentinel Command: 12-Asset Sovereign Tracker")
        if sov_data:
            df_sov = []
            for c in sov_data:
                # Mapping display names correctly
                display_name = "SINVERSE" if c.get('id') == "sin-city" else c.get('name')
                
                c24 = safe_float(c.get('price_change_percentage_24h'))
                c7d = safe_float(c.get('price_change_percentage_7d_in_currency'))
                c30d = safe_float(c.get('price_change_percentage_30d_in_currency'))
                
                df_sov.append({
                    "Logo": c.get('image'),
                    "Asset": display_name,
                    "Price (INR)": f"₹{safe_float(c.get('current_price')):,.2f}",
                    "24H": f"{get_ind(c24)} {abs(c24):.1f}%",
                    "7D (WEEKLY)": f"{get_ind(c7d)} {abs(c7d):.1f}%",
                    "30D (MONTHLY)": f"{get_ind(c30d)} {abs(c30d):.1f}%",
                    "7D Trend Chart": c.get('sparkline_in_7d', {}).get('price', [])
                })
            
            # Rendering exactly 12 assets as per Master's list
            st.dataframe(pd.DataFrame(df_sov), column_config={"Logo": st.column_config.ImageColumn("Logo"), "7D Trend Chart": st.column_config.LineChartColumn("7D Trend Chart")}, use_container_width=True, hide_index=True)
        else:
            st.warning("🔄 Fetching Sovereign Data Nodes...")

        st.divider()

        # SECTION 2: GLOBAL MEGA INDEX
        st.subheader(f"🌍 Global Mega Index: Institutional List ({len(global_market)} Assets)")
        if global_market:
            df_g = pd.DataFrame([{
                "Rank": c.get('market_cap_rank'),
                "Logo": c.get('image'),
                "Name": c.get('name'),
                "Price": f"₹{safe_float(c.get('current_price')):,.2f}",
                "24H": f"{get_ind(safe_float(c.get('price_change_percentage_24h')))} {abs(safe_float(c.get('price_change_percentage_24h'))):.1f}%",
                "1W": f"{get_ind(safe_float(c.get('price_change_percentage_7d_in_currency')))} {abs(safe_float(c.get('price_change_percentage_7d_in_currency'))):.1f}%",
                "1M": f"{get_ind(safe_float(c.get('price_change_percentage_30d_in_currency')))} {abs(safe_float(c.get('price_change_percentage_30d_in_currency'))):.1f}%"
            } for c in global_market])
            st.dataframe(df_g, column_config={"Logo": st.column_config.ImageColumn("Logo")}, use_container_width=True, hide_index=True)

else:
    st.info("⚠️ Master Key Required to Access Node.")
    
