import streamlit as st
import pandas as pd
import requests

# --- [1. CONFIG & OMEGA UI] ---
st.set_page_config(page_title="AiCoincast v27.1 Apex", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

st.markdown("""
    <style>
    .stApp { background-color: #0A041A !important; }
    h1, h2, h3, h4, p, span, li { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] { background-color: #1A0B35 !important; border-right: 3px solid #00FF00 !important; }
    .crypto-card { background: #000000; padding: 2px; border-radius: 12px; margin-bottom: 12px; border: 2px solid #41444C; transition: 0.3s; }
    .inner-card { display: flex; align-items: center; background: #0D47A1; padding: 15px; border-radius: 10px; position: relative; }
    .price-neon { color: #00FF00 !important; font-size: 19px; font-weight: 900; text-shadow: 0 0 5px #00FF00; }
    .algo-badge { position: absolute; top: 5px; right: 5px; background: #FFD700; color: #000; font-size: 9px; padding: 2px 6px; border-radius: 4px; font-weight: bold; }
    .nifty-card { background: rgba(0, 255, 0, 0.1); padding: 10px; border-radius: 8px; border-left: 5px solid #00FF00; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# [FIX: SAFE-CAST ALGO] - Ensures no crash on missing data
def safe_float(val):
    try: return float(val) if val is not None else 0.0
    except: return 0.0

# [MASTER DATA: ALL 12 COINS HARD-MAPPED]
SOVEREIGN_MAP = {
    "bitcoin": "BTC", "ethereum": "ETH", "virtual-protocol": "VIRTUAL", 
    "griffin-2": "GRIFFIN", "v-ai-2": "VAI", "robonomics-network": "XRT", 
    "velas": "VLX", "qanplatform": "QANX", "chaingpt": "CGPT", 
    "sinverse": "SIN", "matic-network": "POL", "nftb": "NFTB"
}

@st.cache_data(ttl=60)
def fetch_intelligence():
    ids = ",".join(SOVEREIGN_MAP.keys())
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&ids={ids}&order=market_cap_desc&sparkline=false&price_change_percentage=24h,7d"
    try:
        r = requests.get(url, timeout=10)
        return r.json() if (r.status_code == 200 and isinstance(r.json(), list)) else []
    except: return []

data = fetch_intelligence()

# --- [2. SIDEBAR VAULT: PASSWORD MASKED + NIFTY 50] ---
with st.sidebar:
    st.title("🔐 OMNI VAULT")
    m_key = st.text_input("Master Key", type="password", placeholder="••••••••")
    if data:
        tmc = sum([safe_float(c.get('market_cap', 0)) for c in data])
        st.info(f"💼 Portfolio MC: ₹{tmc:,.0f}")
        st.markdown(f"""<div class="nifty-card">
            <p style="margin:0; font-size:12px; color:#00FF00; font-weight:bold;">📈 NIFTY 50 INDEX</p>
            <p style="margin:0; font-size:16px;">22,493.50 (+0.45%)</p>
        </div>""", unsafe_allow_html=True)

# --- [3. MAIN TERMINAL LOGIC: ALL FOLDERS RESTORED] ---
if m_key == MASTER_KEY:
    tab1, tab2, tab3, tab4 = st.tabs(["📊 SENTINEL (LIVE)", "📈 PERFORMANCE (TSI)", "📰 BROADCAST FEED", "⚖️ RISK ENGINE"])
    
    with tab1:
        st.subheader("🛰️ Sentinel Alpha: Pump/Dump Monitoring")
        if data:
            cols = st.columns(4)
            for i, coin in enumerate(data):
                p = safe_float(coin.get('current_price', 0))
                c24 = safe_float(coin.get('price_change_percentage_24h', 0))
                vol = safe_float(coin.get('total_volume', 0))
                mc = safe_float(coin.get('market_cap', 1))
                v_to_mc = (vol / mc) * 100 if mc > 0 else 0
                color = "#00FF00" if c24 >= 0 else "#FF4B4B"
                with cols[i % 4]:
                    st.markdown(f"""
                    <div class="crypto-card" style="border-color: {color};">
                        <div class="inner-card">
                            {"<div class='algo-badge'>🔥 VOL SPIKE</div>" if v_to_mc > 15 else ""}
                            <img src="{coin.get('image', '')}" width="35" style="margin-right:12px;">
                            <div>
                                <p style="margin:0; font-size:11px; color:#BBDEFB;">{coin.get('symbol','').upper()}/INR</p>
                                <p class="price-neon">₹{p:,.0f}</p>
                                <p style="margin:0; font-size:10px; color:{color};">V/MC: {v_to_mc:.1f}%</p>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)

    with tab2:
        st.subheader("📈 TSI (Trend Strength Index) Performance")
        if data:
            perf_list = []
            for c in data:
                c24 = safe_float(c.get('price_change_percentage_24h', 0))
                c7d = safe_float(c.get('price_change_percentage_7d_in_currency', 0))
                tsi = (c24 * 0.7) + (c7d * 0.3)
                perf_list.append({
                    "Asset": c['name'],
                    "Price": f"₹{safe_float(c['current_price']):,.2f}",
                    "TSI Strength": f"{tsi:+.2f}",
                    "Status": "🚀 Strong Buy" if tsi > 5 else "⚖️ Neutral"
                })
            st.table(pd.DataFrame(perf_list))

    with tab3:
        st.subheader("📰 Neural Broadcast Intelligence")
        st.success("📡 Samastipur Node: Neural Sentiment Score 8.4/10 (Bullish)")
        st.markdown("""<div style="background:rgba(255,255,255,0.05); padding:15px; border-radius:10px; border-left:5px solid #00FF00;">
            <p style="color:#00FF00; font-weight:bold; margin:0;">🐦 Twitter Alpha Feed:</p>
            <p style="font-size:13px;">Institutional accumulation in $XRT and $VIRTUAL protocols. Polygon ecosystem showing consolidation signals.</p>
        </div>""", unsafe_allow_html=True)

    with tab4:
        st.subheader("⚖️ Sovereign Risk Engine (Fixed)")
        col1, col2 = st.columns(2)
        with col1:
            budget = st.number_input("Capital (INR)", value=50000)
            risk = st.slider("Risk Per Trade (%)", 1, 10, 2)
        with col2:
            entry = st.number_input("Entry Price", value=100.0)
            sl = st.number_input("Stop Loss", value=95.0)
        if st.button("Calculate Optimal Size"):
            risk_amt = budget * (risk/100)
            diff = entry - sl
            if diff > 0:
                qty = risk_amt / diff
                st.success(f"🛒 Recommendation: Buy {qty:.2f} Coins | Total Risk: ₹{risk_amt}")
            else: st.error("Stop Loss entry se niche hona chahiye.")

else: st.info("⚠️ Master Key Required for Node Synchronization.")
