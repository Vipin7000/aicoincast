import streamlit as st
import yfinance as yf
import google.generativeai as genai
import requests
import time
import pandas as pd
from datetime import datetime
import pytz

# --- 1. SETUP & SOVEREIGN THEME (v19.4) ---
st.set_page_config(page_title="AiCoincast v19.4 Omnipotent", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
MASTER_PWD = "SAMASTIPUR@2026"

# Session State Persistence (v18.9 Memory Management)
keys = ['batch_res', 'batch_vis', 'x_q', 'l_q', 'q_q', 'auth', 'alerts']
for k in keys:
    if k not in st.session_state:
        st.session_state[k] = 100.0 if '_q' in k else [] if k == 'alerts' else None

st.markdown("""<style>
    .main { background-color: #05010a; color: #00ff41; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 2px solid #BF40BF; }
    [data-testid="stMetricValue"] { color: #00ff41 !important; text-shadow: 0 0 10px #00ff41; font-weight: 900 !important; }
    .master-card { background: rgba(20, 0, 40, 0.9); border: 1px solid #BF40BF; padding: 20px; border-radius: 12px; }
</style>""", unsafe_allow_html=True)

# --- 2. PARTNER LOGIN ALGORITHM (v12.0 + v19.0 Security) ---
def validate_partner(email):
    partners = ["reliance.com", "google.com", "digital.in"]
    return any(p in email for p in partners)

if not st.session_state.auth:
    st.title("🛡️ Partner Sovereign Vault")
    e_in = st.text_input("Corporate Email:")
    p_in = st.text_input("Master Key:", type="password")
    if st.button("Unlock Terminal"):
        if validate_partner(e_in) and p_in == MASTER_PWD:
            st.session_state.auth = True
            st.rerun()
        else: st.error("Access Denied: Partner Credentials Required")
    st.stop()

# --- 3. DATA HARVESTING ENGINE (v18.0 30-Coin Tracker) ---
@st.cache_data(ttl=60)
def fetch_omnipotent_data():
    data = {"top30": [], "compare": [], "nifty": "N/A"}
    try:
        # Nifty 50 Live
        n = yf.Ticker("^NSEI").history(period="1d")['Close'].iloc[-1]
        data["nifty"] = f"₹{n:,.2f}"
        # 30-Coin Tracker (v18.0)
        r30 = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_desc&per_page=30")
        data["top30"] = r30.json() if r30.status_code == 200 else []
        # 5-Coin Comparison IDs
        ids = "xrt-token,layerai,the-quantum-resistant-ledger,bitcoin,ethereum"
        r5 = requests.get(f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&ids={ids}")
        data["compare"] = r5.json() if r5.status_code == 200 else []
    except: pass
    return data

# --- 4. MAIN INTERFACE ---
st.title("🤖 AiCoincast v19.4: Omnipotent Node")
pulse = fetch_omnipotent_data()

with st.sidebar:
    st.header("🛰️ 30-Coin Sentinel")
    st.metric("NIFTY 50", pulse["nifty"])
    st.divider()
    # v18.9 Master Batch Button
    if st.button("🚀 Master Batch Update"):
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content("Analyze XRT, LAI, QRL status for Indian market. 3 lines.")
        st.session_state.batch_res = res.text
        st.session_state.batch_vis = f"https://pollinations.ai/p/crypto_elite?seed={time.time()}"
    
    st.subheader("🌐 Top 30 Live Tracker")
    for c in pulse["top30"]:
        st.caption(f"{c['symbol'].upper()}: ₹{c['current_price']:,} ({c['price_change_percentage_24h']:.1f}%)")

tab1, tab2, tab3 = st.tabs(["💰 Command Center", "⚖️ 5-Coin Comparison", "🚨 v4.1 Price Alerts"])

with tab1:
    # Portfolio Management
    c1, c2, c3 = st.columns(3)
    st.session_state.x_q = c1.number_input("XRT Qty", value=st.session_state.x_q)
    st.session_state.l_q = c2.number_input("LAI Qty", value=st.session_state.l_q)
    st.session_state.q_q = c3.number_input("QRL Qty", value=st.session_state.q_q)
    
    st.divider()
    # Batch Report Display
    if st.session_state.batch_res:
        st.markdown("<div class='master-card'>", unsafe_allow_html=True)
        ca, cb = st.columns([1, 2.5])
        if st.session_state.batch_vis: ca.image(st.session_state.batch_vis)
        cb.info(st.session_state.batch_res)
        st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    # 5-Coin Comparison Table (v15.0)
    st.subheader("📊 Comparison Matrix (XRT, LAI, QRL, BTC, ETH)")
    if pulse["compare"]:
        df = pd.DataFrame(pulse["compare"])[['name', 'current_price', 'price_change_percentage_24h', 'market_cap']]
        st.table(df)

with tab3:
    # Price Alert Algorithm (v4.1)
    st.subheader("🚨 v4.1 Active Alerts")
    col_a, col_b = st.columns(2)
    t_coin = col_a.selectbox("Select Asset", ["XRT", "LAI", "QRL", "BTC", "ETH"])
    t_price = col_b.number_input("Target (INR)", value=0.0)
    if st.button("Sync Alert"):
        st.session_state.alerts.append({"coin": t_coin, "target": t_price})
        st.success(f"Alert set for {t_coin} at ₹{t_price}")
    
    # Alert Trigger Logic
    for c in pulse["compare"]:
        for al in st.session_state.alerts:
            if al['coin'].lower() in c['id'] and c['current_price'] >= al['target'] and al['target'] > 0:
                st.error(f"⚠️ TARGET HIT: {c['name']} at ₹{c['current_price']:,}")

st.caption("© 2026 AiCoincast | v19.4 Sovereign Elite Integration | No Algorithm Missing")
        
