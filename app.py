import streamlit as st
import pandas as pd
import requests

# --- [1. CONFIG & OMEGA UI] ---
st.set_page_config(page_title="AiCoincast v33.1 Absolute", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

st.markdown("""
    <style>
    .stApp { background-color: #0A041A !important; }
    h1, h2, h3, h4, p, span, li { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] { background-color: #1A0B35 !important; border-right: 3px solid #00FF00 !important; }
    
    /* Neon Ticker */
    .ticker-wrap { background: #000; padding: 12px; border-bottom: 2px solid #00FF00; margin-bottom: 20px; }
    .ticker-text { color: #00FF00; font-weight: bold; font-size: 17px; }
    
    /* Sovereign Cards */
    .crypto-card { background: #000; padding: 2px; border-radius: 12px; border: 2px solid #41444C; margin-bottom: 10px; }
    .inner-card { display: flex; flex-direction: column; background: #0D47A1; padding: 15px; border-radius: 10px; }
    .price-neon { color: #00FF00 !important; font-size: 22px; font-weight: 900; text-shadow: 0 0 5px #00FF00; }
    </style>
    """, unsafe_allow_html=True)

# [ALGO: ERROR SHIELD]
def safe_float(val):
    try: return float(val) if val is not None else 0.0
    except: return 0.0

def get_indicator(val):
    return "🟢" if val >= 0 else "🔴"

# [MASTER DATA LISTS]
SOVEREIGN_12_IDS = ["bitcoin", "ethereum", "virtual-protocol", "griffin-2", "v-ai-2", "robonomics-network", "velas", "qanplatform", "chaingpt", "sinverse", "matic-network", "nftb"]

@st.cache_data(ttl=60)
def fetch_complete_market():
    # Fetching 50 coins with Sparkline (7d trend) and Price Change (1h, 24h, 7d, 30d)
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_desc&per_page=50&page=1&sparkline=true&price_change_percentage=1h,24h,7d,30d"
    try:
        r = requests.get(url, timeout=15)
        return r.json() if (r.status_code == 200 and isinstance(r.json(), list)) else []
    except: return []

market_data = fetch_complete_market()

# --- [2. TOP 20 LIVE TICKER] ---
if market_data:
    ticker_items = [f"{get_indicator(safe_float(c.get('price_change_percentage_24h')))} {c['symbol'].upper()}: ₹{safe_float(c['current_price']):,.0f}" for c in market_data[:20]]
    st.markdown(f'<div class="ticker-wrap"><marquee class="ticker-text">{" | ".join(ticker_items)}</marquee></div>', unsafe_allow_html=True)

# --- [3. SIDEBAR VAULT: NIFTY & PASSWORD MASKED] ---
with st.sidebar:
    st.title("🔐 OMNI VAULT")
    m_key = st.text_input("Master Key", type="password", placeholder="••••••••")
    if market_data:
        sov_data = [c for c in market_data if c['id'] in SOVEREIGN_12_IDS]
        tmc = sum([safe_float(c.get('market_cap', 0)) for c in sov_data])
        st.info(f"💼 Sovereign 12 MC: ₹{tmc:,.0f}")
        # Global Sentiment logic
        avg_change = sum([safe_float(c.get('price_change_percentage_24h')) for c in market_data]) / 50
        st.metric("Global Sentiment", "BULLISH 🚀" if avg_change > 0 else "BEARISH 📉", f"{avg_change:+.2f}%")

# --- [4. MAIN TERMINAL: FOLDER 1 LOCK] ---
if m_key == MASTER_KEY:
    tab1, tab2, tab3, tab4 = st.tabs(["📊 SENTINEL (LOCKED)", "📈 PERFORMANCE", "📰 BROADCAST", "⚖️ RISK"])
    
    with tab1:
        st.subheader("🛰️ Sentinel Command: Sovereign 12 Intelligence")
        if market_data:
            sov_assets = [c for c in market_data if c['id'] in SOVEREIGN_12_IDS]
            cols = st.columns(4)
            for i, coin in enumerate(sov_assets):
                p = safe_float(coin.get('current_price', 0))
                c24 = safe_float(coin.get('price_change_percentage_24h', 0))
                c7d = safe_float(coin.get('price_change_percentage_7d_in_currency', 0))
                spark_data = coin.get('sparkline_in_7d', {}).get('price', [])
                
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
                            <p style="font-size:11px; color:{color}; margin:0;">24H: {get_indicator(c24)} {abs(c24):.1f}% | 7D: {abs(c7d):.1f}%</p>
                        </div>
                    </div>""", unsafe_allow_html=True)
                    # Fixed Sparkline using native Streamlit chart
                    if spark_data:
                        st.line_chart(spark_data, height=60, use_container_width=True)

        st.divider()
        st.subheader("📈 Global Top 50 Nodes")
        df_final = pd.DataFrame([{
            "Rank": c.get('market_cap_rank'),
            "Logo": c.get('image'),
            "Name": c.get('name'),
            "Price": f"₹{safe_float(c.get('current_price')):,.2f}",
            "24H %": f"{safe_float(c.get('price_change_percentage_24h')):+.2f}%",
            "7D %": f"{safe_float(c.get('price_change_percentage_7d_in_currency')):+.2f}%",
            "30D %": f"{safe_float(c.get('price_change_percentage_30d_in_currency')):+.2f}%"
        } for c in market_data])
        
        st.dataframe(df_final, column_config={"Logo": st.column_config.ImageColumn("Logo")}, use_container_width=True, hide_index=True)

else: st.info("⚠️ Master Key Required for Node Synchronization.")
