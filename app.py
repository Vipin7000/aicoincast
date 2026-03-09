import streamlit as st
import pandas as pd
import requests

# --- [1. CONFIG & OMEGA UI] ---
st.set_page_config(page_title="AiCoincast v36.0 Apex", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

st.markdown("""
    <style>
    .stApp { background-color: #0A041A !important; }
    h1, h2, h3, h4, p, span, li { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] { background-color: #1A0B35 !important; border-right: 3px solid #00FF00 !important; }
    
    /* Neon Ticker Enhanced */
    .ticker-wrap { background: #000; padding: 12px; border-bottom: 2px solid #00FF00; margin-bottom: 20px; }
    .ticker-text { color: #00FF00; font-weight: bold; font-size: 16px; font-family: 'Courier New', monospace; }
    
    /* Sovereign Cards with Glow Alert */
    .crypto-card { background: #000; padding: 2px; border-radius: 12px; border: 2px solid #41444C; margin-bottom: 15px; position: relative; }
    .inner-card { display: flex; flex-direction: column; background: #0D47A1; padding: 15px; border-radius: 10px; }
    .price-neon { color: #00FF00 !important; font-size: 24px; font-weight: 900; text-shadow: 0 0 10px #00FF00; }
    .whale-alert { position: absolute; top: 8px; right: 10px; font-size: 18px; }
    
    /* Glow effect for high volatility */
    .glow-up { box-shadow: 0 0 15px #00FF00; border: 2px solid #00FF00 !important; }
    .glow-down { box-shadow: 0 0 15px #FF4B4B; border: 2px solid #FF4B4B !important; }
    </style>
    """, unsafe_allow_html=True)

# [ALGO: DATA SANITY SHIELD]
def safe_float(val):
    try: return float(val) if val is not None else 0.0
    except: return 0.0

def get_ind(val):
    return "🟢" if val >= 0 else "🔴"

# [SOVEREIGN 12 IDS]
MY_12_IDS = ["bitcoin", "ethereum", "virtual-protocol", "griffin-2", "v-ai-2", "robonomics-network", "velas", "qanplatform", "chaingpt", "sinverse", "matic-network", "nftb"]

@st.cache_data(ttl=60)
def fetch_apex_data():
    # Fetching 250 coins to cover global market + Sovereign 12
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_desc&per_page=250&page=1&sparkline=true&price_change_percentage=24h,7d"
    try:
        r = requests.get(url, timeout=15)
        data = r.json() if (r.status_code == 200 and isinstance(r.json(), list)) else []
        return data
    except: return []

market_data = fetch_apex_data()

# --- [2. TOP 20 LIVE TICKER] ---
if market_data:
    ticker_items = [f"{get_ind(safe_float(c.get('price_change_percentage_24h')))} {c['symbol'].upper()}: ₹{safe_float(c['current_price']):,.0f}" for c in market_data[:20]]
    st.markdown(f'<div class="ticker-wrap"><marquee class="ticker-text">{" | ".join(ticker_items)}</marquee></div>', unsafe_allow_html=True)

# --- [3. SIDEBAR VAULT: NIFTY & SENTIMENT] ---
with st.sidebar:
    st.title("🔐 OMNI VAULT")
    m_key = st.text_input("Master Key", type="password", placeholder="••••••••")
    if market_data:
        sov_data = [c for c in market_data if c['id'] in MY_12_IDS]
        tmc = sum([safe_float(c.get('market_cap', 0)) for c in sov_data])
        st.info(f"💼 Portfolio MC: ₹{tmc:,.0f}")
        # Market Mood Gauge
        avg_24h = sum([safe_float(c.get('price_change_percentage_24h')) for c in market_data[:100]]) / 100
        st.metric("Global Sentiment", "BULLISH 🚀" if avg_24h > 0 else "BEARISH 📉", f"{avg_24h:+.2f}%")

# --- [4. MAIN TERMINAL: FOLDER 1 COMMAND] ---
if m_key == MASTER_KEY:
    tab1, tab2, tab3, tab4 = st.tabs(["📊 SOVEREIGN COMMAND", "📈 GLOBAL MARKET (3000)", "📰 BROADCAST", "⚖️ RISK"])
    
    with tab1:
        st.subheader("🛰️ Sentinel Command: Sovereign 12 Intelligence")
        if market_data:
            sov_assets = [c for c in market_data if c['id'] in MY_12_IDS]
            cols = st.columns(4)
            for i, coin in enumerate(sov_assets):
                p = safe_float(coin.get('current_price', 0))
                c24 = safe_float(coin.get('price_change_percentage_24h', 0))
                c7d = safe_float(coin.get('price_change_percentage_7d_in_currency', 0))
                spark = coin.get('sparkline_in_7d', {}).get('price', [])
                
                # GLOW LOGIC: Highlight if 24h change > 5%
                glow_class = ""
                if c24 > 5: glow_class = "glow-up"
                elif c24 < -5: glow_class = "glow-down"
                
                # WHALE LOGIC: Mock indicator based on high volume/MC ratio
                vol_mc_ratio = safe_float(coin.get('total_volume')) / safe_float(coin.get('market_cap', 1))
                whale_icon = "🐋" if vol_mc_ratio > 0.15 else ""
                
                with cols[i % 4]:
                    st.markdown(f"""
                    <div class="crypto-card {glow_class}">
                        <div class="whale-alert">{whale_icon}</div>
                        <div class="inner-card">
                            <div style="display:flex; align-items:center; margin-bottom:10px;">
                                <img src="{coin.get('image', '')}" width="25" style="margin-right:10px;">
                                <b>{coin.get('symbol', '').upper()}/INR</b>
                            </div>
                            <div class="price-neon">₹{p:,.0f}</div>
                            <p style="font-size:12px; margin-top:5px;">
                                <span style="color:{'#00FF00' if c24 >=0 else '#FF4B4B'}">24H: {c24:+.1f}%</span> | 
                                <span style="color:{'#00FF00' if c7d >=0 else '#FF4B4B'}">7D: {c7d:+.1f}%</span>
                            </p>
                        </div>
                    </div>""", unsafe_allow_html=True)
                    if spark: st.line_chart(spark, height=70)

        st.divider()
        st.subheader("🌍 Global Market Pulse (Top 250 Assets)")
        df = pd.DataFrame([{
            "Rank": c.get('market_cap_rank'),
            "Logo": c.get('image'),
            "Name": c.get('name'),
            "Price": f"₹{safe_float(c.get('current_price')):,.2f}",
            "24H %": safe_float(c.get('price_change_percentage_24h')),
            "7D %": safe_float(c.get('price_change_percentage_7d_in_currency'))
        } for c in market_data])
        
        st.dataframe(df, column_config={"Logo": st.column_config.ImageColumn("Logo"), "24H %": st.column_config.NumberColumn(format="%.2f%%")}, use_container_width=True, hide_index=True)

else: st.info("⚠️ Master Key Required to Access Commander Node.")
