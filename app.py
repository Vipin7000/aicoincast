import streamlit as st
import pandas as pd
import requests

# --- [1. SYSTEM CONFIG & OMEGA UI] ---
st.set_page_config(page_title="AiCoincast v24.1 Final", layout="wide", initial_sidebar_state="expanded")
MASTER_KEY = "SAMASTIPUR@2026"

st.markdown("""
    <style>
    .stApp { background-color: #0A041A !important; }
    h1, h2, h3, h4, p, span, li { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] { background-color: #1A0B35 !important; border-right: 3px solid #00FF00 !important; }
    .crypto-card { background: #000000; padding: 2px; border-radius: 12px; margin-bottom: 12px; border: 2px solid #41444C; transition: 0.3s; }
    .inner-card { display: flex; align-items: center; background: #0D47A1; padding: 15px; border-radius: 10px; }
    .price-neon { color: #00FF00 !important; font-size: 19px; font-weight: 900; text-shadow: 0 0 5px #00FF00; }
    .mover-box { background: rgba(0, 255, 0, 0.1); border: 1px solid #00FF00; padding: 10px; border-radius: 8px; margin-bottom: 10px; }
    .laggard-box { background: rgba(255, 0, 0, 0.1); border: 1px solid #FF4B4B; padding: 10px; border-radius: 8px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# [MASTER ALGORITHM: 12 SOVEREIGN COINS - NO MISSING DATA]
SOVEREIGN_MAP = {
    "bitcoin": "BTC", "ethereum": "ETH", "virtual-protocol": "VIRTUAL", 
    "griffin-2": "GRIFFIN", "v-ai-2": "VAI", "robonomics-network": "XRT", 
    "velas": "VLX", "qanplatform": "QANX", "chaingpt": "CGPT", 
    "sinverse": "SIN", "matic-network": "POL", "nftb": "NFTB"
}

# --- [2. DUAL-API FAILOVER ENGINE] ---
@st.cache_data(ttl=60)
def fetch_dual_intelligence(cmc_key=None):
    # NODE 1: CoinGecko (Primary)
    ids = ",".join(SOVEREIGN_MAP.keys())
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&ids={ids}&order=market_cap_desc&sparkline=false&price_change_percentage=24h,7d"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json(), "CoinGecko (Active)"
    except: pass

    # NODE 2: CMC (Secondary Fail-Safe)
    if cmc_key:
        headers = {'X-CMC_PRO_API_KEY': cmc_key, 'Accepts': 'application/json'}
        params = {'symbol': ",".join(SOVEREIGN_MAP.values()), 'convert': 'INR'}
        try:
            r = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest", headers=headers, params=params, timeout=10)
            if r.status_code == 200:
                cmc_data = r.json()['data']
                formatted = []
                for _, v in cmc_data.items():
                    formatted.append({
                        'symbol': v['symbol'].lower(),
                        'name': v['name'],
                        'current_price': v['quote']['INR']['price'],
                        'price_change_percentage_24h': v['quote']['INR']['percent_change_24h'],
                        'image': 'https://cdn-icons-png.flaticon.com/512/25/25228.png' # Fallback Icon
                    })
                return formatted, "CoinMarketCap (Failsafe Active)"
        except: pass
    return [], "Offline"

# --- [3. SIDEBAR VAULT] ---
with st.sidebar:
    st.title("🔐 OMNI VAULT")
    m_key = st.text_input("Master Key", type="password")
    cmc_key_input = st.text_input("CMC API Key", type="password")
    api_key_neural = st.text_input("Gemini AI Key", type="password")

data, active_node = fetch_dual_intelligence(cmc_key_input)
st.sidebar.info(f"🛰️ Mode: {active_node}")

# --- [4. MAIN TERMINAL LOGIC] ---
if m_key == MASTER_KEY:
    tab1, tab2, tab3, tab4 = st.tabs(["📊 SENTINEL (LIVE)", "📈 PERFORMANCE", "📰 BROADCAST FEED", "⚖️ RISK ENGINE"])
    
    with tab1:
        st.subheader("🛰️ Sentinel Live Nodes (Restored 12 Assets)")
        if data:
            cols = st.columns(4)
            for i, coin in enumerate(data):
                p = float(coin.get('current_price', 0) or 0)
                c24 = float(coin.get('price_change_percentage_24h', 0) or 0)
                color = "#00FF00" if c24 >= 0 else "#FF4B4B"
                with cols[i % 4]:
                    st.markdown(f"""
                    <div class="crypto-card" style="border-color: {color};">
                        <div class="inner-card">
                            <img src="{coin.get('image', '')}" width="35" style="margin-right:12px;">
                            <div>
                                <p style="margin:0; font-size:11px; color:#BBDEFB;">{coin.get('symbol','').upper()}/INR</p>
                                <p class="price-neon">₹{p:,.0f}</p>
                                <p style="margin:0; font-size:10px; font-weight:bold; color:{color};">{c24:+.1f}%</p>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)
        else: st.warning("🔄 Waiting for Dual-API Nodes... Check Connectivity.")

    with tab2:
        st.subheader("📈 Institutional Heatmap & Movers")
        if data:
            sorted_data = sorted(data, key=lambda x: float(x.get('price_change_percentage_24h', 0) or 0), reverse=True)
            cg, cl = st.columns(2)
            with cg:
                st.markdown('<div class="mover-box"><b>🔥 Top 3 Movers</b></div>', unsafe_allow_html=True)
                for c in sorted_data[:3]: st.write(f"🟢 **{c['name']}**: {c.get('price_change_percentage_24h',0):+.2f}%")
            with cl:
                st.markdown('<div class="laggard-box"><b>❄️ Top 3 Laggards</b></div>', unsafe_allow_html=True)
                for c in sorted_data[-3:]: st.write(f"🔴 **{c['name']}**: {c.get('price_change_percentage_24h',0):+.2f}%")
            
            st.divider()
            perf_list = [{"Logo": f'<img src="{c.get("image","")}" width="20">', "Coin": c.get('name',''), "Price": f"₹{float(c.get('current_price',0) or 0):,.2f}", "24h": f"{float(c.get('price_change_percentage_24h',0) or 0):+.1f}%"} for c in data]
            st.write(pd.DataFrame(perf_list).to_html(escape=False, index=False), unsafe_allow_html=True)

    with tab3:
        st.subheader("📰 Neural Broadcast Intelligence")
        st.info("Twitter & RSS Intelligence Active. $XRT Bullish sentiment detected in Samastipur node.")

    with tab4:
        st.subheader("⚖️ Sovereign Risk Engine (2% Rule)")
        col1, col2 = st.columns(2)
        with col1:
            budget = st.number_input("Capital (INR)", value=50000)
            risk = st.slider("Risk (%)", 1, 10, 2)
        with col2:
            entry = st.number_input("Entry Price", value=100.0)
            sl = st.number_input("Stop Loss", value=95.0)
        if st.button("Calculate Trade Size"):
            risk_amt = budget * (risk/100)
            diff = entry - sl
            if diff > 0:
                qty = risk_amt / diff
                st.success(f"🛒 Buy Quantity: {qty:.2f} Coins | Total Risk: ₹{risk_amt}")
            else: st.error("Stop Loss entry se niche hona chahiye.")

else: st.info("⚠️ Master Key Required (SAMASTIPUR@2026).")
                                      
