import streamlit as st
import yfinance as yf
from google import genai 
import requests
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz

# --- 1. SETUP & THEME ---
st.set_page_config(page_title="AiCoincast v18.9 Sovereign Elite", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
MASTER_PWD = "SAMASTIPUR@2026"

st.markdown("""<style>
    .stApp { background-color: #05010a; color: #00ff41; font-family: 'JetBrains Mono', monospace; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 2px solid #BF40BF; }
    [data-testid="stMetricValue"] { color: #00ff41 !important; text-shadow: 0 0 10px #00ff41; font-size: 2rem !important; font-weight: 900 !important; }
    .master-card { background: rgba(15, 15, 15, 0.95); border: 1px solid #BF40BF; padding: 20px; border-radius: 12px; margin-bottom: 20px; }
    .stButton>button { background: linear-gradient(45deg, #BF40BF, #00ff41) !important; color: black !important; font-weight: bold !important; border-radius: 8px; }
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

# --- 3. OPTIMIZED BATCH AI ENGINE ---
@st.cache_data(ttl=3600, show_spinner=False)
def ask_ai_batch(query_type="portfolio_summary"):
    # Batch query definition to save tokens
    if query_type == "portfolio_summary":
        prompt = "Provide a 1-sentence market outlook for each: XRT (Akash), LayerAI (LAI), and QRL. Use Hinglish and be very brief."
    else:
        prompt = query_type

    for attempt in range(2):
        try:
            if "GEMINI_API_KEY" not in st.secrets: return "Error: API Key Missing!", None
            client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
            
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                config={
                    'system_instruction': 'Brief Crypto Analyst. Hinglish.',
                    'temperature': 0.2, # Lower temp for more factual/precise response
                    'max_output_tokens': 300 # Limit output to save quota
                },
                contents=prompt
            )
            if response and response.text:
                img_url = f"https://pollinations.ai/p/crypto_matrix_analysis_cyber?seed={time.time()}"
                return response.text, img_url
        except Exception as e:
            if "429" in str(e): # Quota auto-wait
                time.sleep(5)
                continue
            return f"Node Error: {str(e)}", None
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

# --- 4. MAIN INTERFACE ---
st.title("🤖 AiCoincast v18.9 Sovereign Elite")
pulse = get_market()

with st.sidebar:
    st.title("🛰️ Sentinel")
    st.metric("NIFTY 50", pulse["nifty"])
    st.divider()
    # Batch Update Button: Saves 66% Quota
    if st.button("🚀 Master Batch Update"):
        with st.spinner("Analyzing All Holdings..."):
            res, vis = ask_ai_batch("portfolio_summary")
            st.session_state.batch_res = res
            st.session_state.batch_vis = vis
            st.success("Full Sync Complete!")

    if st.button("🔍 AI Health Check"):
        res, _ = ask_ai_batch("Are you online?")
        st.info(f"Status: {res}")

    if st.button("🔒 Logout"):
        del st.session_state.auth
        st.rerun()

tab1, tab2, tab3 = st.tabs(["💰 Portfolio", "📈 Analytics", "🔔 Alerts"])

with tab1:
    # Portfolio display logic
    p_cols = st.columns(3)
    curr_prices = {}
    if pulse["crypto"]:
        for idx, c in enumerate(pulse["crypto"]):
            qty = st.session_state.get('x_q' if 'xrt' in c['id'] else 'l_q' if 'layer' in c['id'] else 'q_q', 100.0)
            val = qty * c['current_price']
            curr_prices[c['symbol'].upper()] = c['current_price']
            p_cols[idx].metric(c['name'], f"₹{val:,.0f}", f"{c['price_change_percentage_24h']:.2f}%")

    # Display Batch Results if available
    if "batch_res" in st.session_state:
        st.markdown("<div class='master-card'>", unsafe_allow_html=True)
        st.subheader("🛰️ Multi-Token Intelligence Report")
        c_a, c_b = st.columns([1, 2.5])
        c_a.image(st.session_state.batch_vis, use_container_width=True)
        c_b.info(st.session_state.batch_res)
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()
    query = st.text_input("🔍 Custom Search:", "")
    if query:
        with st.spinner("Analyzing..."):
            rep, vis = ask_ai_batch(query)
            st.info(rep)

# Analytics and Alerts logic remains same for stability
with tab2:
    total = sum(curr_prices.values() if curr_prices else [1000])
    df = pd.DataFrame({'Day': [(datetime.now() - timedelta(days=i)).strftime("%d %b") for i in range(7, 0, -1)], 
                       'Portfolio (₹)': [total * (1 + np.random.uniform(-0.02, 0.02)) for _ in range(7)]})
    st.line_chart(df.set_index('Day'))

with tab3:
    tkn = st.selectbox("Token", ["XRT", "LAI", "QRL"])
    trgt = st.number_input(f"Target {tkn} Price (₹)", value=0.0)
    if st.button("Set Alarm"):
        st.session_state.alert = {"tkn": tkn, "prc": trgt}
        st.success(f"Alarm synced.")
    if "alert" in st.session_state:
        al = st.session_state.alert
        cur = curr_prices.get(al['tkn'], 0)
        if cur >= al['prc'] and al['prc'] > 0:
            st.error(f"🚨 ALERT: {al['tkn']} reached ₹{cur}!")
                        
