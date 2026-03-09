import streamlit as st
import pandas as pd
import requests

# --- [1. CORE CONFIG & UI] ---
st.set_page_config(page_title="AiCoincast v40.0 Final", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

st.markdown("""
    <style>
    .stApp { background-color: #0A041A !important; }
    h1, h2, h3, h4, p, span, li { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] { background-color: #1A0B35 !important; border-right: 3px solid #00FF00 !important; }
    
    /* Neon Ticker Fixed */
    .ticker-wrap { background: #000; padding: 12px; border-bottom: 2px solid #00FF00; margin-bottom: 20px; }
    .ticker-text { color: #00FF00; font-weight: bold; font-size: 16px; font-family: 'Courier New', monospace; }
    
    /* Sovereign Grid */
    .sov-card { background: #000; padding: 15px; border-radius: 12px; border: 2px solid #41444C; margin-bottom: 10px; }
    .price-neon { color: #00FF00 !important; font-size: 22px; font-weight: 900; text-shadow: 0 0 5px #00FF00; }
    </style>
    """, unsafe_allow_html=True)

# [ALGO: ABSOLUTE ERROR SHIELD]
def safe_float(val):
    try: return float(val) if val is not None else 0.0
    except: return 0.0

def get_ind(val):
    return "🟢" if val >= 0 else "🔴"

# [MASTER ID LOCK - ALL 12 VERIFIED]
MY_12_IDS = [
    "bitcoin", "ethereum", "virtual-protocol", "griffain", 
    "vaiot", "robonomics-network", "velas", "qanplatform", 
    "chaingpt", "sinverse", "polygon-ecosystem-token", "nftb"
]

@st.cache_data(ttl=60)
def fetch_terminal_data():
    ids_sov = ",".join(MY_12_IDS)
    try:
        # 1. Force Fetch Sovereign 12 (Personal Tracker)
        url_sov = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&ids={ids_sov}&sparkline=true&price_change_percentage=24h,7d"
        r_sov = requests.get(url_sov, timeout=15).json()
        
        # 2. Fetch Global Top 50 (Ticker & Global List)
        url_global = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_desc&per_page=250&page=1&sparkline=false&price_change_percentage=24h"
        r_global = requests.get(url_global, timeout=15).json()
        
        return r_sov if isinstance(r_sov, list) else [], r_global if isinstance(r_global, list) else []
    except:
        return [], []

sov_data, global_market = fetch_terminal_data()

# --- [2. TOP 20 LIVE TICKER - RESTORED] ---
if global_market:
    t_items = [f"{get_ind(safe_float(c.get('price_change_percentage_24h')))} {c['symbol'].upper()}: ₹{safe_float(c['current_price']):,.0f}" for c in global_market[:20]]
    st.markdown(f'<div class="ticker-wrap"><marquee class="ticker-text">🚀 LIVE MARKET NODES: {" | ".join(t_items)}</marquee></div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="ticker-wrap"><marquee class="ticker-text">🔄 RECONNECTING TO NODES...</marquee></div>', unsafe_allow_html=True)

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
    tab1, tab2, tab3, tab4 = st.tabs(["📊 SENTINEL ALPHA", "📈 PERFORMANCE", "📰 BROADCAST", "⚖️ RISK ENGINE"])
    
    with tab1:
        # SECTION 1: MY 12 SOVEREIGN LIST (Snapshot 1000620217 Fix)
        st.subheader("🛰️ Sentinel Alpha: My 12 Assets (Full List)")
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
            
            st.dataframe(
                pd.DataFrame(df_sov),
                column_config={
                    "Logo": st.column_config.ImageColumn("Logo"),
                    "Trend (7D)": st.column_config.LineChartColumn("Trend (7D)")
                },
                use_container_width=True, hide_index=True
            )
        else:
            st.warning("🔄 Samastipur Node Re-syncing... Check API Connection.")

        st.divider()

        # SECTION 2: GLOBAL MEGA INDEX (3000 Assets Target)
        st.subheader(f"🌍 Global Mega Index: Real-Time List ({len(global_market)} Assets)")
        if global_market:
            df_global = pd.DataFrame([{
                "Rank": c.get('market_cap_rank'),
                "Logo": c.get('image'),
                "Name": c.get('name'),
                "Price": f"₹{safe_float(c.get('current_price')):,.2f}",
                "24H %": f"{get_ind(safe_float(c.get('price_change_percentage_24h')))} {abs(safe_float(c.get('price_change_percentage_24h'))):.2f}%",
                "Market Cap": f"₹{safe_float(c.get('market_cap')):,.0f}"
            } for c in global_market])
            
            st.dataframe(
                df_global,
                column_config={"Logo": st.column_config.ImageColumn("Logo")},
                use_container_width=True, hide_index=True
            )

else:
    st.info("⚠️ Master Key Required to Access Node.")
    
