import streamlit as st
import pandas as pd
import requests
import time

# --- [1. MASTER CONFIG & UI] ---
st.set_page_config(page_title="AiCoincast v112.0 Eternal", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

st.markdown("""
    <style>
    .stApp { background-color: #0A041A !important; }
    h1, h2, h3, h4, p, span, li { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] { background-color: #1A0B35 !important; border-right: 3px solid #00FF00 !important; }
    
    .ticker-wrap { background: #000; padding: 12px; border-bottom: 2px solid #00FF00; margin-bottom: 25px; }
    .ticker-text { color: #00FF00; font-weight: bold; font-size: 16px; font-family: 'Courier New', monospace; }
    
    [data-testid="stDataFrame"] { border: 1px solid #41444C; border-radius: 12px; transition: all 0.3s ease; }
    [data-testid="stDataFrame"]:hover { border: 1px solid #00FF00; box-shadow: 0 0 15px rgba(0, 255, 0, 0.2); }
    </style>
    """, unsafe_allow_html=True)

# [ALGO: ELITE INDICATORS & PRECISION]
def safe_float(val):
    try: return float(val) if val is not None else 0.0
    except: return 0.0

def format_price(val):
    return f"₹{safe_float(val):,.4f}"

def get_arrow_ind(val):
    val = safe_float(val)
    if val > 0: return f"▲ {abs(val):.1f}%"
    elif val < 0: return f"▼ {abs(val):.1f}%"
    return f"▬ 0.0%"

def get_trend_strength(c24, c7, c30):
    score = sum([1 for x in [c24, c7, c30] if safe_float(x) > 0])
    return "💪 STRONG" if score >= 2 else "📉 WEAK"

def get_depth_score(vol, mc):
    ratio = (safe_float(vol) / safe_float(mc)) if mc else 0
    return "🟢 HIGH" if ratio > 0.10 else "🔴 LOW"

# [MASTER ID LOCK]
MY_12_IDS = [
    "bitcoin", "ethereum", "virtual-protocol", "griffain", 
    "vaiot", "robonomics-network", "velas", "qanplatform", 
    "chaingpt", "sin-city", "polygon-ecosystem-token", "nftb"
]

@st.cache_data(ttl=60)
def fetch_eternal_intelligence():
    all_sov = []
    for coin_id in MY_12_IDS:
        try:
            url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&ids={coin_id}&sparkline=true&price_change_percentage=24h,7d,30d"
            r = requests.get(url, timeout=5).json()
            if isinstance(r, list) and len(r) > 0: all_sov.extend(r)
        except: continue
        
    global_m = []
    for page in [1, 2, 3, 4]:
        try:
            url_g = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_desc&per_page=250&page={page}&sparkline=false&price_change_percentage=24h,7d,30d"
            batch = requests.get(url_g, timeout=10).json()
            if isinstance(batch, list): global_m.extend(batch)
            time.sleep(0.1)
        except: break

    try:
        global_r = requests.get("https://api.coingecko.com/api/v3/global").json()
        total_mc = safe_float(global_r['data']['total_market_cap'].get('inr', 1))
        dominance = global_r['data']['market_cap_percentage']
        fg_r = requests.get("https://api.alternative.me/fng/").json()
        fg_val = fg_r['data'][0]['value']
        fg_class = fg_r['data'][0]['value_classification']
        m_cap_chg = safe_float(global_r['data'].get('market_cap_change_percentage_24h_usd'))
    except: 
        total_mc = 1; dominance = {}; fg_val, fg_class = "N/A", "Stable"; m_cap_chg = 0.0
    
    return all_sov, global_m, dominance, fg_val, fg_class, m_cap_chg, total_mc

# --- [2. SIDEBAR VAULT] ---
with st.sidebar:
    st.title("🔐 OMNI VAULT")
    m_key = st.text_input("Master Key", type="password", placeholder="••••••••")
    sov_data, global_market, dom, fg_v, fg_c, m_cap_chg, total_mc = fetch_eternal_intelligence()
    
    if sov_data:
        tmc = sum([safe_float(c.get('market_cap', 0)) for c in sov_data])
        st.info(f"💼 Sovereign MC: ₹{tmc:,.0f}")
        st.success(f"Verified Nodes: {len(sov_data)}/12")
    
    if dom:
        st.divider()
        st.markdown(f"**Market Intelligence**")
        st.caption(f"BTC Dominance: {dom.get('btc', 0):.1f}%")
        st.caption(f"Fear & Greed: {fg_v} ({fg_c})")

# --- [3. TOP 20 LIVE TICKER] ---
if global_market:
    ticker_parts = [f"{('▲' if safe_float(c.get('price_change_percentage_24h')) > 0 else '▼')} {c['symbol'].upper()}: {format_price(c['current_price'])}" for c in global_market[:20]]
    st.markdown(f'<div class="ticker-wrap"><marquee class="ticker-text">🚀 LIVE OMNI-FEED: {" | ".join(ticker_parts)}</marquee></div>', unsafe_allow_html=True)

# --- [4. MAIN TERMINAL LOGIC] ---
if m_key == MASTER_KEY:
    t1, t2, t3, t4 = st.tabs(["📊 SENTINEL ALPHA", "📈 PERFORMANCE", "📰 BROADCAST", "⚖️ RISK ENGINE"])
    
    with t1:
        # SECTION 1: SOVEREIGN 12 (WITH 15% WHALE ALERT)
        st.subheader("🛰️ Sentinel Command: 12 Sovereign Nodes")
        if sov_data:
            df_sov = []
            for c in sov_data:
                name = "SINVERSE (SIN)" if c.get('id') == "sin-city" else c.get('name').upper()
                df_sov.append({
                    "Logo": c.get('image'), "Asset": name, "Price (INR)": format_price(c.get('current_price')),
                    "24H": get_arrow_ind(c.get('price_change_percentage_24h')),
                    "7D (WEEK)": get_arrow_ind(c.get('price_change_percentage_7d_in_currency')),
                    "30D (MONTH)": get_arrow_ind(c.get('price_change_percentage_30d_in_currency')),
                    "Whale": "🐋" if (safe_float(c.get('total_volume'))/safe_float(c.get('market_cap')) >= 0.15) else "⚪",
                    "Trend": c.get('sparkline_in_7d', {}).get('price', [])
                })
            st.dataframe(pd.DataFrame(df_sov), column_config={"Logo": st.column_config.ImageColumn("Logo"), "Trend": st.column_config.LineChartColumn("Trend")}, use_container_width=True, hide_index=True)

        st.divider()

        # SECTION 2: GLOBAL MEGA INDEX (SEARCH & DEPTH ACTIVE)
        st.subheader(f"🌍 Global Mega Index: Institutional Feed ({len(global_market)} Assets)")
        search_query = st.text_input("🔍 Search Asset Node...", placeholder="e.g. Bitcoin or BTC").strip().lower()
        
        if global_market:
            filtered_market = [c for c in global_market if search_query in c.get('name', '').lower() or search_query in c.get('symbol', '').lower()]
            
            df_g = pd.DataFrame([{
                "Rank": c.get('market_cap_rank'),
                "Logo": c.get('image'),
                "Name": c.get('name'),
                "Depth": get_depth_score(c.get('total_volume'), c.get('market_cap')),
                "Authority (%)": f"{(safe_float(c.get('market_cap')) / total_mc * 100):.2f}%",
                "Trend": get_trend_strength(c.get('price_change_percentage_24h'), c.get('price_change_percentage_7d_in_currency'), c.get('price_change_percentage_30d_in_currency')),
                "Price": format_price(c.get('current_price')),
                "24H Indicator": get_arrow_ind(c.get('price_change_percentage_24h')),
                "1W (WEEKLY)": get_arrow_ind(c.get('price_change_percentage_7d_in_currency')),
                "1M (MONTHLY)": get_arrow_ind(c.get('price_change_percentage_30d_in_currency')),
                "Whale": "🐋 Whale Alert" if (safe_float(c.get('total_volume'))/safe_float(c.get('market_cap')) >= 0.15) else "⚪ Stable"
            } for c in filtered_market])
            
            st.dataframe(df_g, column_config={"Logo": st.column_config.ImageColumn("Logo")}, use_container_width=True, hide_index=True)

else:
    st.info("⚠️ Master Key Required to Unlock Sovereign Terminal Node.")
        
