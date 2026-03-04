import streamlit as st
import yfinance as yf
from google import genai  # Modern SDK
import requests
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz

# --- 1. SETUP & THEME (Cyber-Dark Sovereign) ---
st.set_page_config(page_title="AiCoincast v18.7.1 Sovereign Pro", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
MASTER_PWD = "SAMASTIPUR@2026"

st.markdown("""<style>
    .stApp { background-color: #05010a; color: #00ff41; font-family: 'JetBrains Mono', monospace; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 2px solid #BF40BF; }
    [data-testid="stMetricValue"] { 
        color: #00ff41 !important; 
        text-shadow: 0 0 10px #00ff41; 
        font-size: 2.2rem !important;
        font-weight: 900 !important;
    }
    .master-card { 
        background: rgba(15, 15, 15, 0.9); 
        border: 1px solid #BF40BF; 
        padding: 20px; 
        border-radius: 12px; 
        box-shadow: 0 0 15px rgba(191, 64, 191, 0.2);
    }
    .stButton>button { 
        background: linear-gradient(45deg, #BF40BF, #00ff41) !important; 
        color: black !important; font-weight: bold !important;
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

# --- 3. SMART AI ENGINE (v18.7.1 Auto-Retry & Connection Test) ---
def ask_ai(query):
    # SMART RETRY: 429 Quota Issue ko handle karne ke liye
    for attempt in range(2):
        try:
            if "GEMINI_API_KEY" not in st.secrets: 
                return "Error: API Key Missing!", None
            
            client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
            
            # Use latest v2.0 Flash for speed
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                config={'system_instruction': 'Professional Crypto Analyst in Hinglish.', 'temperature': 0.7},
                contents=query
            )
            
            if response and response.text:
                img_url = f"https://pollinations.ai/p/{query.replace(' ','_')}_cyber?seed={time.time()}"
                return response.text, img_url
            
        except Exception as e:
            err = str(e)
            if "429" in err or "RESOURCE_EXHAUSTED" in err: # Quota Error
                if attempt == 0:
                    st.warning("⚠️ Quota Full! 5 Sec Wait...")
                    time.sleep(5)
                    continue
                return "Error: Quota Exhausted. Try in 1 min.", None
            return f"Node Error: {err}", None
    return "AI Node Busy.", None

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
st.title("🤖 AiCoincast v18.7.1 Sovereign Pro")
pulse = get_market()

with st.sidebar:
    st.title("🛰️ Sentinel")
    st.metric("NIFTY 50", pulse["nifty"])
    st.divider()
    
    # Smart Connection Test Button
    if st.button("🔍 AI Health Check"):
        with st.spinner("Pinging API Node..."):
            res, _ = ask_ai("API Connection Test: Say 'Online'")
            if "Error" in res or "Node Error" in res:
                st.error(f"AI Node: Offline\n({res})")
            else:
                st.success(f"AI Node: {res} (v2.0 Flash) ✅")
    
    if st.button("🔒 Logout"):
        del st.session_state.auth
        st.rerun()

tab1, tab2, tab3 = st.tabs(["💰 Portfolio", "📈 Analytics", "🔔 Alerts"])

with tab1:
    with st.expander("🛠️ Manage Portfolio"):
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
    query = st.text_input("🔍 Intelligence Search:", "XRT and LayerAI Outlook")
    if query:
        with st.spinner("AI Analysis in Progress..."):
            rep, vis = ask_ai(query)
            st.markdown("<div class='master-card'>", unsafe_allow_html=True)
            col_x, col_y = st.columns([1, 2.2])
            if vis: col_x.image(vis, use_container_width=True)
            col_y.info(rep)
            st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.subheader("📊 Portfolio Trend (7D)")
    dates = [(datetime.now() - timedelta(days=i)).strftime("%d %b") for i in range(7, 0, -1)]
    total = sum(curr_prices.values() if curr_prices else [1000])
    df = pd.DataFrame({'Day': dates, 'Portfolio (₹)': [total * (1 + np.random.uniform(-0.02, 0.02)) for _ in range(7)]})
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
    
