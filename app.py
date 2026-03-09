import streamlit as st
import pandas as pd
import requests

# --- [1. CORE CONFIG & UI] ---
st.set_page_config(page_title="AiCoincast v38.1 Mega-Engine", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

st.markdown("""
    <style>
    .stApp { background-color: #0A041A !important; }
    h1, h2, h3, h4, p, span, li { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] { background-color: #1A0B35 !important; border-right: 3px solid #00FF00 !important; }
    .ticker-wrap { background: #000; padding: 12px; border-bottom: 2px solid #00FF00; margin-bottom: 20px; }
    .ticker-text { color: #00FF00; font-weight: bold; font-size: 16px; font-family: 'Courier New', monospace; }
    </style>
    """, unsafe_allow_html=True)

# [ALGO: ABSOLUTE ERROR SHIELD]
def safe_float(val):
    try: return float(val) if val is not None else 0.0
    except: return 0.0

def get_ind(val):
    return "🟢" if val >= 0 else "🔴"

# [SOVEREIGN 12 IDS]
MY_12_IDS = ["bitcoin", "ethereum", "virtual-protocol", "griffin-2", "v-ai-2", "robonomics-network", "velas", "qanplatform", "chaingpt", "sinverse", "matic-network", "nftb"]

# --- [2. MEGA DATA ENGINE: BATCH LOADING] ---
@st.cache_data(ttl=120)
def fetch_mega_market():
    all_data = []
    ids_sov = ",".join(MY_12_IDS)
    try:
        # A. Sovereign 12 Dedicated Node (Snapshot 1000620217 Fix)
        sov_url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&ids={ids_sov}&sparkline=true&price_change_percentage=24h,7d"
        r_sov = requests.get(sov_url, timeout=15).json()
        
        # B. Global Mega Node (Limited to 500 for high-speed stability first)
        for p in range(1, 3): 
            url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_desc&per_page=250&page={p}&sparkline=false&price_change_percentage=24h,7d"
            r_g = requests.get(url, timeout=15).json()
            if isinstance(r_g, list): all_data.extend(r_g)
        return r_sov, all_data
    except: return [], []

sov_data, global_market = fetch_mega_market()

# --- [3. TOP 20 LIVE TICKER RESTORED] ---
if global_market:
    t_items = [f"{get_ind(safe_float(c.get('price_change_percentage_24h')))} {c['symbol'].upper()}: ₹{safe_float(c['current_price']):,.0f}" for c in global_market[:20]]
    st.markdown(f'<div class="ticker-wrap"><marquee class="ticker-text">🚀 LIVE MARKET FEED: {" | ".join(t_items)}</marquee></div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="ticker-wrap"><marquee class="ticker-text">🔄 RECONNECTING TO GLOBAL MARKET NODES...</marquee></div>', unsafe_allow_html=True)

# --- [4. SIDEBAR VAULT] ---
with st.sidebar:
    st.title("🔐 OMNI VAULT")
    m_key = st.text_input("Master Key", type="password", placeholder="••••••••")
    if sov_data:
        tmc = sum([safe_float(c.get('market_cap', 0)) for c in sov_data])
        st.info(f"💼 Sovereign MC: ₹{tmc:,.0f}")
        st.metric("Global Assets Tracked", len(global_market))
        st.success("📈 NIFTY 50: 22,493.50 (+0.45%)")

# --- [5. MAIN TERMINAL LOGIC] ---
if m_key == MASTER_KEY:
    tab1, tab2, tab3, tab4 = st.tabs(["📊 SENTINEL ALPHA", "📈 PERFORMANCE", "📰 BROADCAST", "⚖️ RISK ENGINE"])
    
    with tab1:
        # SECTION 1: MY 12 SOVEREIGN LIST (Snapshot 1000620217 Fix)
        st.subheader("🛰️ Dedicated Tracker: My 12 Sovereign Assets")
        if sov_data:
            df_sov = []
            for c in sov_data:
                c24 = safe_float(c.get('price_change_percentage_24h'))
                c7d = safe_float(c.get('price_change_percentage_7d_in_currency'))
                df_sov.append({
                    "Logo": c.get('image'),
                    "Name": c.get('name'),
                    "Price (INR)": f"₹{safe_float(c.get('current_price')):,.2f}",
                    "24H %": f"{get_ind(c24)} {abs(c24):.2f}%",
                    "7D %": f"{get_ind(c7d)} {abs(c7d):.2f}%",
                    "Trend (7D)": c.get('sparkline_in_7d', {}).get('price', [])
                })
            st.dataframe(pd.DataFrame(df_sov), column_config={"Logo": st.column_config.ImageColumn("Logo"), "Trend (7D)": st.column_config.LineChartColumn("Trend (7D)")}, use_container_width=True, hide_index=True)
        else: st.error("❌ ERROR: Sovereign Nodes Offline. Re-fetching...")

        st.divider()

        # SECTION 2: GLOBAL MEGA INDEX (Snapshot 84667c72 Fix)
        st.subheader(f"🌍 Global Mega Index: Top {len(global_market)} Assets")
        if global_market:
            df_global = pd.DataFrame([{
                "Rank": c.get('market_cap_rank'),
                "Logo": c.get('image'),
                "Name": c.get('name'),
                "Price": f"₹{safe_float(c.get('current_price')):,.2f}",
                "24H %": f"{get_ind(safe_float(c.get('price_change_percentage_24h')))} {abs(safe_float(c.get('price_change_percentage_24h'))):.2f}%",
                "Market Cap": f"₹{safe_float(c.get('market_cap')):,.0f}"
            } for c in global_market])
            st.dataframe(df_global, column_config={"Logo": st.column_config.ImageColumn("Logo")}, use_container_width=True, hide_index=True)
        else: st.warning("⚠️ Global Index loading... Please wait for Node Sync.")

else: st.info("⚠️ Master Key Required to Unlock Terminal.")
        
