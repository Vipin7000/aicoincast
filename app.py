import streamlit as st
import pandas as pd
import requests
import time

# --- [1. CORE CONFIG & ULTIMATE UI] ---
st.set_page_config(page_title="AiCoincast v37.1 Absolute", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

st.markdown("""
    <style>
    .stApp { background-color: #0A041A !important; }
    h1, h2, h3, h4, p, span, li { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] { background-color: #1A0B35 !important; border-right: 3px solid #00FF00 !important; }
    .ticker-wrap { background: #000; padding: 10px; border-bottom: 2px solid #00FF00; margin-bottom: 20px; }
    .ticker-text { color: #00FF00; font-weight: bold; font-size: 16px; font-family: 'Courier New', monospace; }
    .sov-card { background: #000; padding: 15px; border-radius: 15px; border: 2px solid #41444C; margin-bottom: 15px; }
    .price-neon { color: #00FF00 !important; font-size: 24px; font-weight: 900; text-shadow: 0 0 10px #00FF00; }
    </style>
    """, unsafe_allow_html=True)

# [ALGO: ABSOLUTE TYPE SAFETY]
def safe_float(val):
    try: return float(val) if val is not None else 0.0
    except: return 0.0

# [SOVEREIGN 12 IDS - HARD LOCKED]
MY_12_IDS = ["bitcoin", "ethereum", "virtual-protocol", "griffin-2", "v-ai-2", "robonomics-network", "velas", "qanplatform", "chaingpt", "sinverse", "matic-network", "nftb"]

@st.cache_data(ttl=120)
def fetch_sovereign_intelligence():
    # Dedicated fetch for Personal Tracker only
    ids_sov = ",".join(MY_12_IDS)
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&ids={ids_sov}&sparkline=true&price_change_percentage=24h,7d"
    try:
        r = requests.get(url, timeout=10).json()
        return r if isinstance(r, list) else []
    except: return []

@st.cache_data(ttl=300)
def fetch_global_3000(pages=5): # Fetching top 1250 for optimal speed
    all_data = []
    try:
        for page in range(1, pages + 1):
            url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_desc&per_page=250&page={page}"
            r = requests.get(url, timeout=10).json()
            if isinstance(r, list) and len(r) > 0:
                all_data.extend(r)
            else: break
        return all_data
    except: return []

# Execute Data Fetch
sov_data = fetch_sovereign_intelligence()
global_market = fetch_global_3000()

# --- [2. TOP 20 LIVE TICKER] ---
if global_market:
    t_items = [f"{'🟢' if safe_float(c.get('price_change_percentage_24h')) >=0 else '🔴'} {c['symbol'].upper()}: ₹{safe_float(c['current_price']):,.0f}" for c in global_market[:20]]
    st.markdown(f'<div class="ticker-wrap"><marquee class="ticker-text">🚀 LIVE MARKET FEED: {" | ".join(t_items)}</marquee></div>', unsafe_allow_html=True)

# --- [3. SIDEBAR VAULT: NIFTY & MASKED PASSWORD] ---
with st.sidebar:
    st.title("🔐 OMNI VAULT")
    m_key = st.text_input("Master Key", type="password", placeholder="••••••••")
    if sov_data:
        tmc = sum([safe_float(c.get('market_cap', 0)) for c in sov_data])
        st.info(f"💼 Portfolio MC: ₹{tmc:,.0f}")
        st.markdown("""<div style='background:rgba(0,255,0,0.1); padding:10px; border-radius:8px; border-left:5px solid #00FF00;'>
            <p style='margin:0; font-size:12px; color:#00FF00; font-weight:bold;'>📈 NIFTY 50 INDEX</p>
            <p style='margin:0; font-size:16px;'>22,493.50 (+0.45%)</p>
        </div>""", unsafe_allow_html=True)

# --- [4. MAIN TERMINAL: FOLDER 1 LOCK] ---
if m_key == MASTER_KEY:
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 SOVEREIGN TRACKER", "🌍 GLOBAL MARKET (3000)", "📰 BROADCAST", "⚖️ RISK ENGINE"])
    
    with tab1:
        st.subheader("🛰️ Dedicated Tracker: My 12 Sovereign Assets")
        if sov_data:
            cols = st.columns(3)
            for i, coin in enumerate(sov_data):
                p = safe_float(coin.get('current_price', 0))
                c24 = safe_float(coin.get('price_change_percentage_24h', 0))
                c7d = safe_float(coin.get('price_change_percentage_7d_in_currency', 0))
                color = "#00FF00" if c24 >= 0 else "#FF4B4B"
                with cols[i % 3]:
                    st.markdown(f"""
                    <div class="sov-card" style="border-color: {color};">
                        <div style="display:flex; align-items:center;">
                            <img src="{coin.get('image', '')}" width="35" style="margin-right:12px;">
                            <b style="font-size:17px;">{coin.get('symbol','').upper()}/INR</b>
                        </div>
                        <div class="price-neon">₹{p:,.2f}</div>
                        <div style="display:flex; justify-content:space-between; margin-top:10px;">
                            <span style="color:{color}; font-weight:bold;">24H: {c24:+.1f}%</span>
                            <span style="color:{'#00FF00' if c7d >=0 else '#FF4B4B'};">7D: {c7d:+.1f}%</span>
                        </div>
                    </div>""", unsafe_allow_html=True)
                    spark = coin.get('sparkline_in_7d', {}).get('price', [])
                    if spark: st.line_chart(spark, height=80)
        else: st.warning("🔄 Fetching Sovereign Data Nodes...")

    with tab2:
        st.subheader(f"📈 Global Market Index ({len(global_market)} Assets)")
        if global_market:
            df = pd.DataFrame([{
                "Rank": c.get('market_cap_rank'),
                "Logo": c.get('image'),
                "Name": c.get('name'),
                "Price": f"₹{safe_float(c.get('current_price')):,.2f}",
                "24H %": f"{safe_float(c.get('price_change_percentage_24h')):+.2f}%",
                "Market Cap": f"₹{safe_float(c.get('market_cap')):,.0f}"
            } for c in global_market])
            st.dataframe(df, column_config={"Logo": st.column_config.ImageColumn("Logo")}, use_container_width=True, hide_index=True)

else: st.info("⚠️ Master Key Required to Unlock Terminal.")
                   
