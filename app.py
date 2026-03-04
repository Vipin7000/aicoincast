import streamlit as st
import yfinance as yf
from google import genai 
import requests
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz

# --- 1. SETUP & THEME (Cyber-Dark Sink) ---
st.set_page_config(page_title="AiCoincast v18.7 Sovereign", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
MASTER_PWD = "SAMASTIPUR@2026"

# CSS SINK: Matrix-Cyber Look
st.markdown("""<style>
    /* Main App Background */
    .stApp { 
        background-color: #05010a; 
        color: #00ff41; 
        font-family: 'JetBrains Mono', monospace; 
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] { 
        background-color: #000000 !important; 
        border-right: 2px solid #BF40BF; 
    }

    /* Metric Values (Neon Glow) */
    [data-testid="stMetricValue"] { 
        color: #00ff41 !important; 
        font-weight: 900 !important; 
        text-shadow: 0 0 10px #00ff41, 0 0 20px #00ff41; 
        font-size: 2.2rem !important;
    }
    
    /* Metrics Label */
    [data-testid="stMetricLabel"] {
        color: #BF40BF !important;
        font-weight: bold !important;
    }

    /* Master Cards */
    .master-card { 
        background: rgba(15, 15, 15, 0.9); 
        border: 1px solid #BF40BF; 
        padding: 25px; 
        border-radius: 12px; 
        box-shadow: 0 0 15px rgba(191, 64, 191, 0.3);
    }

    /* Custom Cyber Buttons */
    .stButton>button { 
        background: linear-gradient(45deg, #BF40BF, #00ff41) !important; 
        color: #000000 !important; 
        border: none !important;
        font-weight: bold !important;
        text-transform: uppercase;
        transition: 0.5s;
    }
    .stButton>button:hover { 
        box-shadow: 0 0 25px #00ff41 !important;
        transform: scale(1.02);
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        color: #BF40BF !important;
        background-color: transparent !important;
    }
    .stTabs [aria-selected="true"] {
        color: #00ff41 !important;
        border-bottom: 3px solid #00ff41 !important;
    }
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

# --- 3. AI ENGINE (v2.0 Flash) ---
def ask_ai(query):
    try:
        if "GEMINI_API_KEY" not in st.secrets: 
            return "Error: API Key missing!", None
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            config={'system_instruction': 'You are a professional crypto expert. Use Hinglish.', 'temperature': 0.7},
            contents=query
        )
        if response and response.text:
            img_url = f"https://pollinations.ai/p/{query.replace(' ','_')}_cyber?seed={time.time()}"
            return response.text, img_url
        return "AI Node Busy.", None
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

# --- 4. INTERFACE ---
st.title("🤖 AiCoincast v18.7 Sovereign")
st.caption(f"Sync Active | {datetime.now(IST).strftime('%H:%M:%S IST')}")
pulse = get_market()

with st.sidebar:
    st.title("🛰️ Sentinel")
    st.metric("NIFTY 50", pulse["nifty"])
    st.divider()
    if st.button("🔍 AI Health Check"):
        res, _ = ask_ai("Hi")
        if "Node Error" in res: st.error("AI Offline")
        else: st.success("AI Online ✅")
    if st.button("🔒 Logout"):
        del st.session_state.auth
        st.rerun()

tab1, tab2, tab3 = st.tabs(["💰 Portfolio", "📈 Analytics", "🔔 Alerts"])

with tab1:
    with st.expander("🛠️ Manage Holdings"):
        c1, c2, c3 = st.columns(3)
        x_q = c1.number_input("XRT Qty", value=st.session_state.get('x_q', 176.0))
        l_q = c2.number_input("LAI Qty", value=st.session_state.get('l_q', 100.0))
        q_q = c3.number_input("QRL Qty", value=st.session_state.get('q_q', 100.0))
        if st.button("Update Sync"):
            st.session_state.update({'x_q':x_q, 'l_q':l_q, 'q_q':q_q})
            st.rerun()

    p_cols = st.columns(3)
    curr_prices = {}
    if pulse["crypto"]:
        for idx, c in enumerate(pulse["crypto"]):
            qty = st.session_state.get('x_q' if 'xrt' in c['id'] else 'l_q' if 'layer' in c['id'] else 'q_q', 100.0)
            val = qty * c['current_price']
            curr_prices[c['symbol'].upper()] = c['current_price']
            p_cols[idx].metric(c['name'], f"₹{val:,.0f}", f"{c['price_change_percentage_24h']:.2f}%")

    st.divider()
    query = st.text_input("🔍 Intelligence Search:", "XRT Trends Today")
    if query:
        with st.spinner("AI v2.0 Thinking..."):
            rep, vis = ask_ai(query)
            st.markdown("<div class='master-card'>", unsafe_allow_html=True)
            col_x, col_y = st.columns([1, 2.2])
            if vis: col_x.image(vis, use_container_width=True)
            col_y.info(rep)
            st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.subheader("📊 Performance Trend")
    dates = [(datetime.now() - timedelta(days=i)).strftime("%d %b") for i in range(7, 0, -1)]
    total_val = sum(curr_prices.values() if curr_prices else [1000])
    df = pd.DataFrame({'Day': dates, 'Portfolio (₹)': [total_val * (1 + np.random.uniform(-0.03, 0.03)) for _ in range(7)]})
    st.line_chart(df.set_index('Day'))

with tab3:
    st.subheader("🔔 Price Alarms")
    tkn = st.selectbox("Select Token", ["XRT", "LAI", "QRL"])
    trgt = st.number_input(f"Target {tkn} Price (₹)", value=0.0)
    if st.button("Set Alarm"):
        st.session_state.alert = {"tkn": tkn, "prc": trgt}
        st.success(f"Alarm synced for {tkn}")

    if "alert" in st.session_state:
        al = st.session_state.alert
        cur = curr_prices.get(al['tkn'], 0)
        if cur >= al['prc'] and al['prc'] > 0:
            st.error(f"🚨 ALERT: {al['tkn']} reached ₹{cur}!")
            
