import streamlit as st
import yfinance as yf
import google.generativeai as genai
import requests
import time
import pandas as pd
from datetime import datetime
import pytz
from fpdf import FPDF # New: PDF Generation Algorithm

# --- 1. SETUP & BROADCAST THEME ---
st.set_page_config(page_title="AiCoincast v19.6 Reporter", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
MASTER_PWD = "SAMASTIPUR@2026"

st.markdown("""<style>
    .main { background-color: #05010a; color: #00ff41; font-family: 'JetBrains Mono', monospace; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 2px solid #BF40BF; }
    .broadcast-card { background: rgba(30, 0, 60, 0.95); border-left: 8px solid #BF40BF; padding: 20px; border-radius: 12px; margin-bottom: 15px; }
</style>""", unsafe_allow_html=True)

# --- 2. PDF GENERATION ALGORITHM (v19.6 New) ---
def create_pdf_report(report_text, coins_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="AiCoincast Sovereign Report", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Generated: {datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Sovereign AI Broadcast:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10, txt=report_text)
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Top Market Pulse:", ln=True)
    pdf.set_font("Arial", size=9)
    for c in coins_data[:10]:
        pdf.cell(0, 8, txt=f"{c['name']}: INR {c['current_price']:,} ({c['price_change_percentage_24h']:.2f}%)", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# --- 3. SECURITY & DATA ENGINE (v12.0/v18.0) ---
if "auth" not in st.session_state:
    st.title("🛡️ Partner Sovereign Vault")
    e_in = st.text_input("Corporate Email:")
    p_in = st.text_input("Master Key:", type="password")
    if st.button("Access Terminal"):
        if ("reliance.com" in e_in or "digital.in" in e_in) and p_in == MASTER_PWD:
            st.session_state.auth = True
            st.rerun()
    st.stop()

@st.cache_data(ttl=60)
def fetch_omnipotent_pulse():
    data = {"top30": [], "nifty": "Syncing..."}
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_desc&per_page=30"
        data["top30"] = requests.get(url, timeout=10).json()
        n = yf.Ticker("^NSEI").history(period="1d")['Close'].iloc[-1]
        data["nifty"] = f"₹{n:,.2f}"
    except: pass
    return data

# --- 4. MAIN INTERFACE ---
st.title("🤖 AiCoincast v19.6: Elite Reporter")
pulse = fetch_omnipotent_pulse()

with st.sidebar:
    st.header("🛰️ 30-Coin Sentinel")
    st.metric("NIFTY 50", pulse["nifty"])
    st.divider()
    if pulse["top30"]:
        for c in pulse["top30"]:
            st.caption(f"{c['symbol'].upper()}: ₹{c['current_price']:,} ({c['price_change_percentage_24h']:.1f}%)")

tab1, tab2, tab3, tab4 = st.tabs(["💰 Command Center", "📊 Comparison Table", "🚨 Alerts v4.1", "📢 Sovereign Broadcast"])

with tab4:
    st.subheader("📡 Live Broadcast & Report Generator")
    if st.button("🔄 Force X-Feed Broadcast"):
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content("3-line Hinglish Breaking News for XRT, LAI and QRL.")
        st.session_state.broadcast = res.text

    if "broadcast" in st.session_state:
        st.markdown(f"<div class='broadcast-card'>{st.session_state.broadcast}</div>", unsafe_allow_html=True)
        # PDF DOWNLOAD BUTTON (v19.6 Feature)
        pdf_data = create_pdf_report(st.session_state.broadcast, pulse["top30"])
        st.download_button(label="📥 Download Sovereign PDF Report", data=pdf_data, file_name=f"AiCoincast_Report_{datetime.now().strftime('%d_%m')}.pdf", mime="application/pdf")

with tab2:
    if pulse["top30"]:
        df = pd.DataFrame(pulse["top30"]).head(10)
        st.table(df[['name', 'current_price', 'price_change_percentage_24h', 'market_cap']])

st.caption("© 2026 AiCoincast | v19.6 Sovereign Elite Reporter | PDF Integrated")
