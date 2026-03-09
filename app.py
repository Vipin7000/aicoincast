import streamlit as st
import pandas as pd
import requests

# --- [1. CONFIG & UI] ---
st.set_page_config(page_title="AiCoincast v33.5 Apex", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

st.markdown("""
    <style>
    .stApp { background-color: #0A041A !important; }
    h1, h2, h3, h4, p, span, li { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] { background-color: #1A0B35 !important; border-right: 3px solid #00FF00 !important; }
    .ticker-wrap { background: #000; padding: 10px; border-bottom: 2px solid #00FF00; margin-bottom: 20px; }
    .ticker-text { color: #00FF00; font-weight: bold; font-size: 16px; }
    .crypto-card { background: #000; padding: 2px; border-radius: 12px; border: 2px solid #41444C; margin-bottom: 10px; }
    .inner-card { display: flex; flex-direction: column; background: #0D47A1; padding: 15px; border-radius: 10px; }
    .price-neon { color: #00FF00 !important; font-size: 22px; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

# [FIX: DATA SAFETY]
def safe_float(val):
    try: return float(val) if val is not None else 0.0
    except: return 0.0

# [MASTER 12 COINS IDS]
MY_12_COINS = ["bitcoin", "ethereum", "virtual-protocol", "griffin-2", "v-ai-2", "robonomics-network", "velas", "qanplatform", "chaingpt", "sinverse", "matic-network", "nftb"]

@st.cache_data(ttl=60)
def fetch_terminal_data():
    # 1. Fetch Sovereign 12 specifically (Fix for missing coins)
    sov_ids = ",".join(MY_12_COINS)
    url_sov = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&ids={sov_ids}&sparkline=true&price_change_percentage=24h,7d,30d"
    
    # 2. Fetch Global Top 50
    url_top = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_desc&per_page=50&page=1&sparkline=false&price_change_percentage=24h,7d,30d"
    
    try:
        r1 = requests.get(url_sov, timeout=12).json()
        r2 = requests.get(url_top, timeout=12).json()
        return r1 if isinstance(r1, list) else [], r2 if isinstance(r2, list) else []
    except: return [], []

sov_data, top_50_data = fetch_terminal_data()

# --- [2. LIVE TICKER: TOP 20] ---
if top_50_data:
    t_list = [f"{'🟢' if safe_float(c.get('price_change_percentage_24h')) >=0 else '🔴'} {c['symbol'].upper()}: ₹{safe_float(c['current_price']):,.0f}" for c in top_50_data[:20]]
    st.markdown(f'<div class="ticker-wrap"><marquee class="ticker-text">{" | ".join(t_list)}</marquee></div>', unsafe_allow_html=True)

# --- [3. SIDEBAR VAULT] ---
with st.sidebar:
    st.title("🔐 OMNI VAULT")
    m_key = st.text_input("Master Key", type="password")
    if sov_data:
        tmc = sum([safe_float(c.get('market_cap', 0)) for c in sov_data])
        st.info(f"💼 Sovereign 12 MC: ₹{tmc:,.0f}")
        st.success("📈 Nifty 50: 22,493.50 (+0.45%)")

# --- [4. MAIN TERMINAL: FOLDER 1] ---
if m_key == MASTER_KEY:
    t1, t2, t3, t4 = st.tabs(["📊 SENTINEL (LOCKED)", "📈 PERFORMANCE", "📰 BROADCAST", "⚖️ RISK"])
    
    with t1:
        # SECTION 1: MY 12 COINS (FORCE LOADED)
        st.subheader("🛰️ Sentinel Alpha: My 12 Assets (Restored)")
        if sov_data:
            cols = st.columns(4)
            for i, coin in enumerate(sov_data):
                p = safe_float(coin.get('current_price', 0))
                c24 = safe_float(coin.get('price_change_percentage_24h', 0))
                c7d = safe_float(coin.get('price_change_percentage_7d_in_currency', 0))
                color = "#00FF00" if c24 >= 0 else "#FF4B4B"
                with cols[i % 4]:
                    st.markdown(f"""
                    <div class="crypto-card" style="border-color: {color};">
                        <div class="inner-card">
                            <div style="display:flex; align-items:center; margin-bottom:5px;">
                                <img src="{coin.get('image', '')}" width="25" style="margin-right:10px;">
                                <b>{coin.get('symbol','').upper()}/INR</b>
                            </div>
                            <div class="price-neon">₹{p:,.0f}</div>
                            <p style="font-size:11px; color:{color}; margin:0;">24H: {c24:+.1f}% | 7D: {c7d:+.1f}%</p>
                        </div>
                    </div>""", unsafe_allow_html=True)
                    # Fixed Graph Lock
                    spark = coin.get('sparkline_in_7d', {}).get('price', [])
                    if spark: st.line_chart(spark, height=60, use_container_width=True)
        else: st.error("⚠️ Error: My 12 Coins node failed to load. Re-checking API.")

        st.divider()
        
        # SECTION 2: GLOBAL TOP 50
        st.subheader("📈 Global Top 50 Nodes")
        if top_50_data:
            df = pd.DataFrame([{
                "Rank": c.get('market_cap_rank'),
                "Logo": c.get('image'),
                "Name": c.get('name'),
                "Price": f"₹{safe_float(c.get('current_price')):,.2f}",
                "24H %": f"{safe_float(c.get('price_change_percentage_24h')):+.2f}%",
                "7D %": f"{safe_float(c.get('price_change_percentage_7d_in_currency')):+.2f}%"
            } for c in top_50_data])
            st.dataframe(df, column_config={"Logo": st.column_config.ImageColumn("Logo")}, use_container_width=True, hide_index=True)

else: st.info("⚠️ Master Key Required.")
