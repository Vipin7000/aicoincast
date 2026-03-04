import streamlit as st
import yfinance as yf
import google.generativeai as genai
import requests
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz

# --- 1. SETUP & THEME ---
st.set_page_config(page_title="AiCoincast v18.5 Ultra", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
MASTER_PWD = "SAMASTIPUR@2026"

st.markdown("""<style>
    .main { background-color: #120024; color: #E0B0FF; }
    [data-testid="stSidebar"] { background-color: #080015 !important; border-right: 2px solid #BF40BF; }
    [data-testid="stMetricValue"] { 
        color: #BF40BF !important; 
        font-weight: 800 !important; 
        text-shadow: none !important; 
        font-size: 1.9rem !important;
    }
    .master-card { background: rgba(30, 0, 50, 0.9); border: 2px solid #BF40BF; padding: 20px; border-radius: 15px; margin-top: 10px; }
</style>""", unsafe_allow_html=True)

# --- 2. SECURITY ---
if "auth" not in st.session_state:
    st.markdown("<h2 style='text-align:center;color:#BF40BF;'>🛡️ Sovereign Vault</h2>", unsafe_allow_html=True)
    pwd_input = st.text_input("Master Key:", type="password")
    if st.button("Unlock"):
        if pwd_input == MASTER_PWD:
            st.session_state.auth = True
            st.rerun()
        else: st.error("Wrong Key!")
    st.stop()

# --- 3. ENGINES ---
def ask_ai(query):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(f"Analyze in Hinglish for crypto investor: {query}")
        img = f"https://pollinations.ai/p/{query.replace(' ','_')}_cyber?seed={time.time()}"
        return response.text, img
    except Exception as e: return f"Node Error: {str(e)}", None

@st.cache_data(ttl=60)
def get_market():
    data = {"crypto": [], "nifty": "Offline"}
    try:
        n = yf.Ticker("^NSEI").history(period="1d")['Close'].iloc[-1]
        data["nifty"] = f"₹{n:,.2f}"
        ids = "xrt-token,layerai,the-quantum-resistant-ledger"
        r = requests.get(f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&ids={ids}")
        if r.status_code == 200: data["crypto"] = r.json()
    except: pass
    return data

# --- 4. MAIN INTERFACE ---
st.title("🤖 AiCoincast v18.5 Ultra")
st.caption(f"Last Sync: {datetime.now(IST).strftime('%H:%M:%S')}")
pulse = get_market()

# Tabs for organization
tab1, tab2, tab3 = st.tabs(["💰 Portfolio & AI", "📈 Analytics", "🔔 Alerts"])

with tab1:
    # Portfolio Manager
    with st.expander("🛠️ Manage Holdings"):
        c1, c2, c3 = st.columns(3)
        x_q = c1.number_input("XRT Qty", value=st.session_state.get('x_q', 176.0))
        l_q = c2.number_input("LAI Qty", value=st.session_state.get('l_q', 100.0))
        q_q = c3.number_input("QRL Qty", value=st.session_state.get('q_q', 100.0))
        if st.button("Sync Data"):
            st.session_state.update({'x_q':x_q, 'l_q':l_q, 'q_q':q_q})
            st.rerun()

    # Live Display
    st.subheader("Live Status")
    p_cols = st.columns(3)
    current_values = {}
    if pulse["crypto"]:
        for idx, c in enumerate(pulse["crypto"]):
            qty = st.session_state.get('x_q' if c['symbol']=='xrt' else 'l_q' if c['symbol']=='lai' else 'q_q', 100.0)
            val = qty * c['current_price']
            current_values[c['symbol'].upper()] = c['current_price']
            p_cols[idx].metric(c['name'], f"₹{val:,.0f}", f"{c['price_change_percentage_24h']:.2f}%")

    # AI Intelligence Search
    st.divider()
    query = st.text_input("🔍 AI Intelligence Search:", "XRT and LayerAI Price Outlook India")
    if query:
        with st.spinner("Decoding..."):
            rep, vis = ask_ai(query)
            st.markdown("<div class='master-card'>", unsafe_allow_html=True)
            col1, col2 = st.columns([1, 2])
            if vis: col1.image(vis, use_container_width=True)
            col2.info(rep)
            st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.subheader("📊 7-Day Performance Outlook")
    dates = [(datetime.now() - timedelta(days=i)).strftime("%d %b") for i in range(7, 0, -1)]
    # Simulated Portfolio Tracking
    trend_data = pd.DataFrame({
        'Day': dates,
        'Value (₹)': [sum(current_values.values()) * (1 + np.random.uniform(-0.03, 0.03)) for _ in range(7)]
    })
    st.line_chart(trend_data.set_index('Day'))
    

with tab3:
    st.subheader("🔔 Price Alert Terminal")
    al_col1, al_col2 = st.columns(2)
    alert_token = al_col1.selectbox("Select Token", ["XRT", "LAI", "QRL"])
    alert_price = al_col2.number_input(f"Target {alert_token} Price (₹)", value=0.0)
    
    if st.button("Set Alert"):
        st.session_state.alert_set = {"token": alert_token, "price": alert_price}
        st.success(f"Alert set for {alert_token} at ₹{alert_price}")

    # Alert Check Logic
    if "alert_set" in st.session_state:
        target = st.session_state.alert_set
        current = current_values.get(target['token'], 0)
        if current >= target['price'] and target['price'] > 0:
            st.warning(f"🚀 ALERT: {target['token']} has reached ₹{current}!")

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛰️ Sentinel")
    st.metric("NIFTY 50", pulse["nifty"])
    st.divider()
    if st.button("🔒 Logout"):
        del st.session_state.auth
        st.rerun()
    
