import streamlit as st
import yfinance as yf
import google.generativeai as genai
import requests
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz

# --- 1. SETUP & THEME (Blur & UI Fixed) ---
st.set_page_config(page_title="AiCoincast v18.6 Pro", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
MASTER_PWD = "SAMASTIPUR@2026"

st.markdown("""<style>
    .main { background-color: #120024; color: #E0B0FF; }
    [data-testid="stSidebar"] { background-color: #080015 !important; border-right: 2px solid #BF40BF; }
    [data-testid="stMetricValue"] { 
        color: #BF40BF !important; 
        font-weight: 800 !important; 
        text-shadow: none !important; 
        font-size: 1.8rem !important;
    }
    .master-card { background: rgba(30, 0, 50, 0.9); border: 2px solid #BF40BF; padding: 20px; border-radius: 15px; margin-top: 10px; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; }
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

# --- 3. THE ULTIMATE AI ENGINE (404 Error Fixed) ---
def ask_ai(query):
    try:
        if "GEMINI_API_KEY" not in st.secrets: 
            return "Error: API Key missing in Secrets!", None
        
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # Fix: Model path defined clearly to avoid 404
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        response = model.generate_content(f"Analyze in Hinglish for crypto investor: {query}")
        
        if response and response.text:
            img_url = f"https://pollinations.ai/p/{query.replace(' ','_')}_purple_cyber?seed={time.time()}"
            return response.text, img_url
        return "AI Node Busy. Try later.", None
    except Exception as e:
        return f"Node Error: {str(e)}", None

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
st.title("🤖 AiCoincast v18.6 Pro")
st.caption(f"Last Updated: {datetime.now(IST).strftime('%H:%M:%S')}")
pulse = get_market()

# HEALTH CHECK SECTION
with st.sidebar:
    st.title("🛰️ Sentinel")
    st.metric("NIFTY 50", pulse["nifty"])
    st.divider()
    
    # New Health Check Feature
    if st.button("🔍 AI Health Check"):
        with st.spinner("Pinging AI Node..."):
            test_res, _ = ask_ai("Hi")
            if "Node Error" in test_res or "Error" in test_res:
                st.error("AI Node: Offline (Check API Key)")
            else:
                st.success("AI Node: Online ✅")
    
    if st.button("🔒 Logout"):
        del st.session_state.auth
        st.rerun()

# Tabs
tab1, tab2, tab3 = st.tabs(["💰 Portfolio & AI", "📈 Analytics", "🔔 Alerts"])

with tab1:
    with st.expander("🛠️ Manage Holdings"):
        c1, c2, c3 = st.columns(3)
        x_q = c1.number_input("XRT Qty", value=st.session_state.get('x_q', 176.0))
        l_q = c2.number_input("LAI Qty", value=st.session_state.get('l_q', 100.0))
        q_q = c3.number_input("QRL Qty", value=st.session_state.get('q_q', 100.0))
        if st.button("Sync Portfolio"):
            st.session_state.update({'x_q':x_q, 'l_q':l_q, 'q_q':q_q})
            st.success("Synced!")
            st.rerun()

    st.subheader("Live Market Status")
    p_cols = st.columns(3)
    curr_prices = {}
    if pulse["crypto"]:
        for idx, c in enumerate(pulse["crypto"]):
            qty = st.session_state.get('x_q' if 'xrt' in c['id'] else 'l_q' if 'layer' in c['id'] else 'q_q', 100.0)
            val = qty * c['current_price']
            curr_prices[c['symbol'].upper()] = c['current_price']
            p_cols[idx].metric(c['name'], f"₹{val:,.0f}", f"{c['price_change_percentage_24h']:.2f}%")

    st.divider()
    query = st.text_input("🔍 Intelligence Search:", "XRT News India Today")
    if query:
        with st.spinner("AI is thinking..."):
            rep, vis = ask_ai(query)
            st.markdown("<div class='master-card'>", unsafe_allow_html=True)
            col_x, col_y = st.columns([1, 2.2])
            if vis: col_x.image(vis, use_container_width=True)
            col_y.subheader("Master Analysis")
            col_y.info(rep)
            st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.subheader("📊 Performance Analytics")
    dates = [(datetime.now() - timedelta(days=i)).strftime("%d %b") for i in range(7, 0, -1)]
    # Simulated Trend based on portfolio
    trend_vals = [sum(curr_prices.values() if curr_prices else [1000]) * (1 + np.random.uniform(-0.04, 0.04)) for _ in range(7)]
    df = pd.DataFrame({'Day': dates, 'Value (₹)': trend_vals})
    st.line_chart(df.set_index('Day'))

with tab3:
    st.subheader("🔔 Risk Alerts")
    a_col1, a_col2 = st.columns(2)
    tkn = a_col1.selectbox("Token", ["XRT", "LAI", "QRL"])
    trgt = a_col2.number_input(f"Alert Price for {tkn}", value=0.0)
    if st.button("Set Price Alarm"):
        st.session_state.alert = {"tkn": tkn, "prc": trgt}
        st.success(f"Alarm set for {tkn} at ₹{trgt}")

    if "alert" in st.session_state:
        al = st.session_state.alert
        cur = curr_prices.get(al['tkn'], 0)
        if cur >= al['prc'] and al['prc'] > 0:
            st.error(f"🚨 TARGET REACHED: {al['tkn']} is at ₹{cur}!")
