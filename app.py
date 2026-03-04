import streamlit as st
import yfinance as yf
from google import genai 
import requests
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz

# --- 1. SETUP & THEME (v18.9 Legacy + v19.0 Fixes) ---
st.set_page_config(page_title="AiCoincast v19.1 Sovereign Elite Pro", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
MASTER_PWD = "SAMASTIPUR@2026"

# Missing Fix: Session State Initialization
for key in ['batch_res', 'batch_vis', 'x_q', 'l_q', 'q_q']:
    if key not in st.session_state:
        if '_q' in key: st.session_state[key] = 100.0 # Default Qty
        else: st.session_state[key] = None

st.markdown("""<style>
    .stApp { background-color: #05010a; color: #00ff41; font-family: 'JetBrains Mono', monospace; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 2px solid #BF40BF; }
    [data-testid="stMetricValue"] { color: #00ff41 !important; text-shadow: 0 0 10px #00ff41; font-size: 2.2rem !important; font-weight: 900 !important; }
    .master-card { background: rgba(15, 15, 15, 0.95); border: 1px solid #BF40BF; padding: 25px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 0 15px rgba(191, 64, 191, 0.2); }
    .stButton>button { background: linear-gradient(45deg, #BF40BF, #00ff41) !important; color: black !important; font-weight: bold !important; border-radius: 8px; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 20px #00ff41; }
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

# --- 3. ADVANCED AI ENGINE (Auto-Retry + Token Optimization) ---
@st.cache_data(ttl=300, show_spinner=False)
def ask_ai_elite(prompt, mode="standard"):
    for attempt in range(2):
        try:
            if "GEMINI_API_KEY" not in st.secrets: return "Error: API Key Missing!", None
            client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
            
            # v18.9 Feature: Specialized MBA/Business logic prompt
            sys_msg = "Professional Analyst. Use Hinglish. Precise."
            if mode == "mba": sys_msg = "Expert Business Consultant for Retail & Operations. Focused on Reliance Digital style analytics."
            
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                config={'system_instruction': sys_msg, 'temperature': 0.3, 'max_output_tokens': 350},
                contents=prompt
            )
            if response and response.text:
                img = f"https://pollinations.ai/p/cyber_tech_analysis?seed={time.time()}"
                return response.text, img
        except Exception as e:
            if "429" in str(e): # Resource Exhausted Fix
                time.sleep(5)
                continue
            return f"Node Error: {str(e)}", None
    return "AI Node Busy.", None

@st.cache_data(ttl=60)
def get_market():
    data = {"crypto": [], "nifty": "₹24,480.50"} 
    try:
        n = yf.Ticker("^NSEI").history(period="1d")['Close'].iloc[-1]
        data["nifty"] = f"₹{n:,.2f}"
        ids = "xrt-token,layerai,the-quantum-resistant-ledger"
        r = requests.get(f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&ids={ids}", timeout=5)
        if r.status_code == 200: data["crypto"] = r.json()
    except: pass
    return data

# --- 4. MAIN INTERFACE ---
st.title("🤖 AiCoincast v19.1 Sovereign Elite Pro")
pulse = get_market()

with st.sidebar:
    st.title("🛰️ Sentinel")
    st.metric("NIFTY 50", pulse["nifty"])
    st.divider()
    
    # Missing v18.9 Button: Master Batch
    if st.button("🚀 Master Batch Update"):
        with st.spinner("Syncing Portfolio Intelligence..."):
            res, vis = ask_ai_elite("Analyze XRT, LAI, and QRL status today briefly.")
            if "Error" not in str(res):
                st.session_state.batch_res, st.session_state.batch_vis = res, vis
                st.rerun()
    
    # MBA Business Mode
    if st.button("🎓 MBA Business Insight"):
        with st.spinner("Loading Retail Analytics..."):
            res, _ = ask_ai_elite("Explain current crypto trends in context of Retail Management.", mode="mba")
            st.session_state.batch_res = res
            st.rerun()

    if st.button("🔍 AI Health Check"):
        st.info(f"Status: {ask_ai_elite('Ping')[0]}")

    if st.button("🔒 Logout"):
        st.session_state.clear()
        st.rerun()

tab1, tab2, tab3 = st.tabs(["💰 Portfolio", "📈 Analytics", "🔔 Alerts"])

with tab1:
    # Portfolio Management (v18.9 Style)
    with st.expander("🛠️ Update Holdings (XRT/LAI/QRL)"):
        c1, c2, c3 = st.columns(3)
        st.session_state.x_q = c1.number_input("XRT", value=st.session_state.x_q)
        st.session_state.l_q = c2.number_input("LAI", value=st.session_state.l_q)
        st.session_state.q_q = c3.number_input("QRL", value=st.session_state.q_q)

    # Market Cards
    p_cols = st.columns(3)
    curr_prices = {}
    if pulse["crypto"]:
        for idx, c in enumerate(pulse["crypto"]):
            qty = st.session_state.x_q if 'xrt' in c['id'] else st.session_state.l_q if 'layer' in c['id'] else st.session_state.q_q
            val = qty * c['current_price']
            curr_prices[c['symbol'].upper()] = c['current_price']
            p_cols[idx].metric(c['name'], f"₹{val:,.0f}", f"{c['price_change_percentage_24h']:.2f}%")

    # Safe Rendering for Batch Report (v19.0 Fix)
    if st.session_state.batch_res:
        st.markdown("<div class='master-card'>", unsafe_allow_html=True)
        st.subheader("🛰️ Intelligence Report")
        c_a, c_b = st.columns([1, 2.5])
        if st.session_state.batch_vis:
            c_a.image(st.session_state.batch_vis, use_container_width=True)
        c_b.info(st.session_state.batch_res)
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()
    query = st.text_input("🔍 Intelligence Search:", "")
    if query:
        res, vis = ask_ai_elite(query)
        st.session_state.batch_res, st.session_state.batch_vis = res, vis
        st.rerun()

# Tabs logic remains consistent for stability
with tab2:
    total = sum(curr_prices.values() if curr_prices else [1000])
    df = pd.DataFrame({'Day': [(datetime.now() - timedelta(days=i)).strftime("%d %b") for i in range(7, 0, -1)], 
                       'Value (₹)': [total * (1 + np.random.uniform(-0.02, 0.02)) for _ in range(7)]})
    st.line_chart(df.set_index('Day'))

with tab3:
    tkn = st.selectbox("Token", ["XRT", "LAI", "QRL"])
    trgt = st.number_input(f"Target ₹", value=0.0)
    if st.button("Set Alarm"):
        st.session_state.alert = {"tkn": tkn, "prc": trgt}
        st.success("Alarm Synced")
    if "alert" in st.session_state:
        al = st.session_state.alert
        cur = curr_prices.get(al['tkn'], 0)
        if cur >= al['prc'] and al['prc'] > 0:
            st.error(f"🚨 TARGET REACHED: {al['tkn']} at ₹{cur}")
            
