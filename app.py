import streamlit as st
import pandas as pd
import requests
import time

# --- [1. MASTER CONFIG & UI] ---
st.set_page_config(page_title="AiCoincast v115.0 Absolute", layout="wide")
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

# --- [ALGO SUITE: RE-INTEGRATED] ---
def safe_float(val):
    try: return float(val) if val is not None else 0.0
    except: return 0.0

def format_price(val):
    return f"₹{safe_float(val):,.4f}"

def get_arrow_ind(val):
    v = safe_float(val)
    if v > 0: return f"▲ {abs(v):.1f}%"
    elif v < 0: return f"▼ {abs(v):.1f}%"
    return f"▬ 0.0%"

def get_trend_strength(c24, c7, c30):
    score = sum([1 for x in [c24, c7, c30] if safe_float(x) > 0])
    return "💪 STRONG" if score >= 2 else "📉 WEAK"

def get_arbitrage_pot(high, low):
    pot = ((safe_float(high) - safe_float(low)) / safe_float(low)) * 100 if low else 0
    return "🔥 HIGH SWING" if pot >= 10 else "💎 STABLE"

def get_depth_score(vol, mc):
    return "🟢 HIGH" if (safe_float(vol) / safe_float(mc)) > 0.10 if mc else "🔴 LOW"

# [MASTER ID LOCK]
MY_12_IDS = ["bitcoin", "ethereum", "virtual-protocol", "griffain", "vaiot", "robonomics-network", "velas", "qanplatform", "chaingpt", "sin-city", "polygon-ecosystem-token", "nftb"]

@st.cache_data(ttl=60)
def fetch_zenith_data():
    sov_res, global_res, total_mc = [], [], 1.0
    ids_str = ",".join(MY_12_IDS)
    base_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&price_change_percentage=24h,7d,30d"
    
    try:
        sov_res = requests.get(f"{base_url}&ids={ids_str}&sparkline=true", timeout=15).json()
        for p in range(1, 5):
            g_batch = requests.get(f"{base_url}&order=market_cap_desc&per_page=250&page={p}", timeout=15).json()
            if isinstance(g_batch, list): global_res.extend(g_batch)
            time.sleep(0.3)
        gr = requests.get("https://api.coingecko.com/api/v3/global").json()
        total_mc = safe_float(gr['data']['total_market_cap'].get('inr', 1))
    except: pass
    return sov_res, global_res, total_mc

# --- [2. EXECUTION] ---
sov_data, global_market, total_market_cap = fetch_zenith_data()

with st.sidebar:
    st.title("🔐 OMNI VAULT")
    m_key = st.text_input("Master Key", type="password")
    if sov_data:
        st.success(f"Verified Nodes: {len(sov_data)}/12")
        st.info(f"Sovereign MC: ₹{sum([safe_float(c.get('market_cap')) for c in sov_data]):,.0f}")

if m_key == MASTER_KEY:
    t1, t2 = st.tabs(["📊 SENTINEL ALPHA", "📈 GLOBAL MEGA INDEX"])
    
    with t1:
        st.subheader("🛰️ Sentinel Command: 12 Sovereign Nodes")
        if sov_data:
            df_sov = []
            for c in sov_data:
                c24, c7, c30 = c.get('price_change_percentage_24h_in_currency'), c.get('price_change_percentage_7d_in_currency'), c.get('price_change_percentage_30d_in_currency')
                df_sov.append({
                    "Logo": c.get('image'), "Asset": c.get('name').upper(),
                    "Price (INR)": format_price(c.get('current_price')),
                    "24H": get_arrow_ind(c24), "WEEK": get_arrow_ind(c7), "MONTH": get_arrow_ind(c30),
                    "Whale": "🐋" if (safe_float(c.get('total_volume'))/safe_float(c.get('market_cap')) >= 0.15) else "⚪",
                    "Trend": c.get('sparkline_in_7d', {}).get('price', [])
                })
            st.dataframe(pd.DataFrame(df_sov), column_config={"Logo": st.column_config.ImageColumn(), "Trend": st.column_config.LineChartColumn()}, use_container_width=True, hide_index=True)

    with t2:
        st.subheader(f"🌍 Global Mega Index ({len(global_market)} Assets)")
        q = st.text_input("🔍 Search Node...")
        if global_market:
            filtered = [c for c in global_market if q.lower() in c['name'].lower() or q.lower() in c['symbol'].lower()]
            df_g = []
            for c in filtered:
                c24, c7, c30 = c.get('price_change_percentage_24h_in_currency'), c.get('price_change_percentage_7d_in_currency'), c.get('price_change_percentage_30d_in_currency')
                df_g.append({
                    "Rank": c.get('market_cap_rank'), "Logo": c.get('image'), "Name": c.get('name'),
                    "Authority": f"{(safe_float(c.get('market_cap'))/total_market_cap*100):.2f}%",
                    "Poten": get_arbitrage_pot(c.get('high_24h'), c.get('low_24h')),
                    "Depth": get_depth_score(c.get('total_volume'), c.get('market_cap')),
                    "Trend": get_trend_strength(c24, c7, c30),
                    "Price": format_price(c.get('current_price')),
                    "24H": get_arrow_ind(c24), "7D": get_arrow_ind(c7), "30D": get_arrow_ind(c30),
                    "Whale": "🐋" if (safe_float(c.get('total_volume'))/safe_float(c.get('market_cap')) >= 0.15) else "⚪"
                })
            st.dataframe(pd.DataFrame(df_g), column_config={"Logo": st.column_config.ImageColumn()}, use_container_width=True, hide_index=True)
else:
    st.info("Enter Master Key.")
    
