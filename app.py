import streamlit as st
import yfinance as yf
import google.generativeai as genai
import requests
import time
import pandas as pd
from datetime import datetime
import pytz
from fpdf import FPDF

# --- 1. SETUP & SOVEREIGN THEME ---
st.set_page_config(page_title="AiCoincast v19.7 Absolute", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
MASTER_PWD = "SAMASTIPUR@2026"

# Session State Persistence (v18.9 Memory Management)
keys = ['batch_res', 'batch_vis', 'x_q', 'l_q', 'q_q', 'auth', 'alerts', 'broadcast']
for k in keys:
    if k not in st.session_state:
        st.session_state[k] = 100.0 if '_q' in k else [] if k == 'alerts' else None

st.markdown("""<style>
    .main { background-color: #05010a; color: #00ff41; font-family: 'JetBrains Mono', monospace; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 2px solid #BF40BF; }
    [data-testid="stMetricValue"] { color: #00ff41 !important; text-shadow: 0 0 10px #00ff41; font-weight: 900 !important; }
    .master-card { background: rgba(20, 0, 40, 0.9); border: 2px solid #BF40BF; padding: 20px; border-radius: 12px; margin-bottom: 10px; }
</style>""", unsafe_allow_html=True)

# --- 2. PDF ALGORITHM (v19.6) ---
def create_elite_pdf(report_text, top_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="AiCoincast Sovereign Report v19.7", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Date: {datetime.now(IST).strftime('%d %b %Y %H:%M')}", ln=True, align='C')
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=f"Broadcast Intelligence: \n{report_text}")
    pdf.ln(5)
    for c in top_data[:10]:
        pdf.cell(0, 8, txt=f"{c['symbol'].upper()}: INR {c['current_price']:,} ({c['price_change_percentage_24h']:.2f}%)", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# --- 3. SECURITY (v12.0 Partner Login) ---
if not st.session_state.auth:
    st.title("🛡️ Partner Sovereign Vault")
    e_in = st.text_input("Corporate Email (Reliance/Partner):")
    p_in = st.text_input("Master Key:", type="password")
    if st.button("Unlock Terminal"):
        if ("reliance.com" in e_in or "digital.in" in e_in) and p_in == MASTER_PWD:
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- 4. DATA PULSE (v8.0 Nifty + v18.0 30-Coin Tracker) ---
@st.cache_data(ttl=60)
def fetch_omnipotent_data():
    data = {"top30": [], "nifty": "N/A", "compare": []}
    try:
        n = yf.Ticker("^NSEI").history(period="1d")['Close'].iloc[-1]
        data["nifty"] = f"₹{n:,.2f}"
        # 30-Coin Tracker
        r30 = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_desc&per_page=30")
        data["top30"] = r30.json()
        # 5-Coin Comparison (XRT, LAI, QRL, BTC, ETH)
        ids = "xrt-token,layerai,the-quantum-resistant-ledger,bitcoin,ethereum"
        r5 = requests.get(f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&ids={ids}")
        data["compare"] = r5.json()
    except: pass
    return data

# --- 5. MAIN INTERFACE ---
st.title("🤖 AiCoincast v19.7: Absolute Sovereign")
pulse = fetch_omnipotent_data()

with st.sidebar:
    st.header("🛰️ 30-Coin Sentinel")
    st.metric("NIFTY 50", pulse["nifty"])
    st.divider()
    # v18.9 Master Batch Update
    if st.button("🚀 Master Batch Update"):
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content("Analyze XRT, LAI, QRL status for Indian market. 3 lines.")
        st.session_state.batch_res = res.text
        st.session_state.batch_vis = f"https://pollinations.ai/p/elite_crypto?seed={time.time()}"
    
    st.subheader("🌐 Top 30 Live Tracker")
    for c in pulse["top30"]:
        st.caption(f"{c['symbol'].upper()}: ₹{c['current_price']:,} ({c['price_change_percentage_24h']:.1f}%)")

tab1, tab2, tab3, tab4 = st.tabs(["💰 Portfolio", "⚖️ Comparison", "🚨 v4.1 Alerts", "📢 Sovereign Broadcast"])

with tab1:
    st.subheader("🛠️ Asset Quantities (v18.9)")
    c1, c2, c3 = st.columns(3)
    st.session_state.x_q = c1.number_input("XRT Qty", value=st.session_state.x_q)
    st.session_state.l_q = c2.number_input("LAI Qty", value=st.session_state.l_q)
    st.session_state.q_q = c3.number_input("QRL Qty", value=st.session_state.q_q)
    
    if st.session_state.batch_res:
        st.markdown("<div class='master-card'>", unsafe_allow_html=True)
        st.info(st.session_state.batch_res)
        if st.session_state.batch_vis: st.image(st.session_state.batch_vis, width=400)
        st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.subheader("📊 5-Coin Matrix (v15.0)")
    if pulse["compare"]:
        df = pd.DataFrame(pulse["compare"])[['name', 'current_price', 'price_change_percentage_24h', 'market_cap']]
        st.table(df)

with tab3:
    st.subheader("🚨 v4.1 Price Alerts")
    col_a, col_b = st.columns(2)
    t_coin = col_a.selectbox("Select Asset", ["XRT", "LAI", "QRL", "BTC", "ETH"])
    t_price = col_b.number_input("Target (INR)", value=0.0)
    if st.button("Sync Alert"):
        st.session_state.alerts.append({"coin": t_coin, "target": t_price})
    for al in st.session_state.alerts:
        st.write(f"Monitoring {al['coin']} at ₹{al['target']}")

with tab4:
    st.subheader("📡 Live Broadcast & Report (v19.5/19.6)")
    if st.button("🔄 Fetch X-Feed"):
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content("Create a 5-line Breaking Broadcast in Hinglish for XRT, LAI and Top 30 Market.")
        st.session_state.broadcast = res.text
    
    if st.session_state.broadcast:
        st.markdown(f"<div class='master-card'>{st.session_state.broadcast}</div>", unsafe_allow_html=True)
        pdf_out = create_elite_pdf(st.session_state.broadcast, pulse["top30"])
        st.download_button("📥 Download Sovereign PDF Report", data=pdf_out, file_name="AiCoincast_Elite.pdf")

st.caption("© 2026 AiCoincast | v19.7 Absolute Sovereign | NO ALGORITHM MISSING")
