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
        response = model.generate_content(f"Analyze in Hinglish: {query}")
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
pulse = get_market()

# Tabs for organization
tab1, tab2 = st.tabs(["💰 Portfolio & AI", "📈 7-Day Analytics"])

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
    for idx, c in enumerate(pulse["crypto"]):
        qty = st.session_state.get(f"{c['symbol']}_q", 100.0 if idx > 0 else 176.0)
        p_cols[idx].metric(c['name'], f"₹{qty * c['current_price']:,.0f}", f"{c['price_change_percentage_24h']:.2f}%")

    # Intelligence Search
    st.divider()
    query = st.text_input("🔍 AI Intelligence Search:", "XRT News India")
    if query:
        with st.spinner("Decoding..."):
            rep, vis = ask_ai(query)
            st.markdown("<div class='master-card'>", unsafe_allow_html=True)
            if vis: st.image(vis, width=300)
            st.info(rep)
            st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.subheader("📊 7-Day Performance Outlook")
    # Generating dummy historical data for visualization
    dates = [(datetime.now() - timedelta(days=i)).strftime("%d %b") for i in range(7, 0, -1)]
    # Simulated trend based on current portfolio value
    base_val = sum([st.session_state.get('x_q', 176.0) * 15.0]) # Example base
    trend_data = pd.DataFrame({
        'Day': dates,
        'Portfolio Value (₹)': [base_val * (1 + np.random.uniform(-0.05, 0.05)) for _ in range(7)]
    })
    st.line_chart(trend_data.set_index('Day'))
    st.caption("Note: Chart shows simulated trend based on your current holdings.")

# --- SIDEBAR ---
with st.sidebar:
    st.metric("NIFTY 50", pulse["nifty"])
    if st.button("🔒 Logout"):
        del st.session_state.auth
        st.rerun()
        
