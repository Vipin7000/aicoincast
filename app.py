import streamlit as st
import yfinance as yf
from google import genai 
import requests
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz

# --- 1. SETUP ---
st.set_page_config(page_title="AiCoincast v19.0 Elite", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
MASTER_PWD = "SAMASTIPUR@2026"

# Session State Initialization (Fixes AttributeError)
if "batch_res" not in st.session_state: st.session_state.batch_res = None
if "batch_vis" not in st.session_state: st.session_state.batch_vis = None

st.markdown("""<style>
    .stApp { background-color: #05010a; color: #00ff41; font-family: 'JetBrains Mono', monospace; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 2px solid #BF40BF; }
    [data-testid="stMetricValue"] { color: #00ff41 !important; text-shadow: 0 0 10px #00ff41; font-size: 2rem !important; }
    .master-card { background: rgba(15, 15, 15, 0.95); border: 1px solid #BF40BF; padding: 20px; border-radius: 12px; }
</style>""", unsafe_allow_html=True)

# --- 2. SECURITY ---
if "auth" not in st.session_state:
    pwd_input = st.text_input("🛡️ Vault Key:", type="password")
    if st.button("Unlock"):
        if pwd_input == MASTER_PWD:
            st.session_state.auth = True
            st.rerun()
        else: st.error("Wrong Key!")
    st.stop()

# --- 3. ROBUST AI ENGINE ---
@st.cache_data(ttl=300, show_spinner=False)
def ask_ai_batch(prompt):
    try:
        if "GEMINI_API_KEY" not in st.secrets: return "API Key Missing!", None
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config={'system_instruction': 'Brief Analyst. Hinglish.', 'temperature': 0.2, 'max_output_tokens': 300},
            contents=prompt
        )
        if response and response.text:
            img = f"https://pollinations.ai/p/crypto_matrix?seed={time.time()}"
            return response.text, img
    except Exception as e:
        if "429" in str(e): return "QUOTA_FULL", None
        return f"Node Error: {str(e)}", None
    return None, None

@st.cache_data(ttl=60)
def get_market():
    data = {"crypto": [], "nifty": "₹24,480.50"} # Default for display
    try:
        n = yf.Ticker("^NSEI").history(period="1d")['Close'].iloc[-1]
        data["nifty"] = f"₹{n:,.2f}"
        ids = "xrt-token,layerai,the-quantum-resistant-ledger"
        r = requests.get(f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&ids={ids}", timeout=5)
        if r.status_code == 200: data["crypto"] = r.json()
    except: pass
    return data

# --- 4. MAIN INTERFACE ---
st.title("🤖 AiCoincast v19.0 Elite")
pulse = get_market()

with st.sidebar:
    st.metric("NIFTY 50", pulse["nifty"])
    if st.button("🚀 Master Batch Update"):
        res, vis = ask_ai_batch("Market summary for XRT, LAI, QRL")
        if res == "QUOTA_FULL":
            st.error("Quota Exhausted! Please wait 1 min.")
        else:
            st.session_state.batch_res = res
            st.session_state.batch_vis = vis
            st.rerun()

# Display Intelligence Report (AttributeError Fixed here)
if st.session_state.batch_res:
    st.markdown("<div class='master-card'>", unsafe_allow_html=True)
    st.subheader("🛰️ Multi-Token Intelligence Report")
    c_a, c_b = st.columns([1, 2.5])
    # Safe rendering
    if st.session_state.batch_vis:
        c_a.image(st.session_state.batch_vis, use_container_width=True)
    c_b.info(st.session_state.batch_res)
    st.markdown("</div>", unsafe_allow_html=True)

# Rest of the app (Portfolio, Tabs) goes here...
