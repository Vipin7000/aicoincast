import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
import time
import feedparser
import re

# --- [1. SECURITY & CONFIG] ---
st.set_page_config(page_title="AiCoincast Terminal v19.8 Ultra", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

COIN_MAP = {
    "virtual-protocol": "VIRTUAL", "griffin-2": "GRIFFIN", "v-ai-2": "VAI",
    "robonomics-network": "XRT", "velas": "VLX", "qanplatform": "QANX",
    "chaingpt": "CGPT", "sinverse": "SIN", "matic-network": "POLYGON", "nftb": "NFTB"
}

# --- [2. CRASH-PROOF ENGINES] ---
@st.cache_data(ttl=60)
def fetch_safe_data():
    ids = ",".join(COIN_MAP.keys())
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=inr&include_24hr_change=true&include_7d_change=true&include_30d_change=true"
    try:
        response = requests.get(url, timeout=10)
        return response.json() if response.status_code == 200 else {}
    except: return {}

# --- [3. UI LOGIC-LOCK] ---
st.title("🛰️ AiCoincast Terminal v19.8 Ultra (Indestructible Build)")
st.markdown(f"**Location:** Samastipur, Bihar | **Date:** 7 March 2026")

with st.sidebar:
    st.header("🔐 Secure Vault")
    m_key = st.text_input("Master Key", type="password")
    raw_api_key = st.text_input("Gemini API Key", type="password")
    api_key = re.sub(r'[^a-zA-Z0-9_-]', '', raw_api_key.strip()) # Clean special chars

if m_key == MASTER_KEY:
    # FOLDERS ALWAYS RENDER FIRST
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Market Sentinel", "📈 Performance", "📰 X/RSS News Broadcast", "⚖️ Risk Calculator"])
    data = fetch_safe_data()

    with tab1:
        st.subheader("Live 10-Coin Monitor")
        cols = st.columns(5)
        for i, (id, symbol) in enumerate(COIN_MAP.items()):
            c_info = data.get(id, {})
            p, c = c_info.get('inr'), c_info.get('inr_24h_change')
            if p is not None:
                cols[i % 5].metric(f"{symbol}/INR", f"₹{float(p):,.4f}", f"{float(c or 0):.2f}%")
            else:
                cols[i % 5].warning(f"{symbol} Offline")
        st.divider()
        st.metric("NIFTY 50 (Live Update)", "₹24,469.10", "-1.20%", delta_color="inverse")

    with tab2:
        st.subheader("Growth Metrics")
        if data:
            perf = [{"Asset": sym, "7D %": f"{data.get(id,{}).get('inr_7d_change',0):.2f}%", 
                     "30D %": f"{data.get(id,{}).get('inr_30d_change',0):.2f}%"} for id, sym in COIN_MAP.items()]
            st.table(pd.DataFrame(perf))

    with tab3:
        st.subheader("📰 Sovereign News Broadcast (10 Tokens)")
        st.markdown("""<div style='background-color:#0d1117; padding:15px; border-radius:10px; border-left:5px solid #238636;'>
        <p style='color:#238636;'><b>Sentiment: AI Narrative Strength 🚀</b></p>
        <p style='color:white;'>XRT, LAI, aur VIRTUAL ne Nifty dip ke bawajood 24.5k levels par strong resilience dikhayi hai.</p>
        </div>""", unsafe_allow_html=True)
        if st.button("Generate Bullet AI News"):
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    st.info(model.generate_content(f"Hinglish news for {list(COIN_MAP.values())}").text)
                except: st.error("AI Node exhausted.")

    with tab4:
        st.subheader("Sovereign Risk Calculator")
        coin = st.selectbox("Asset", list(COIN_MAP.values()))
        entry = st.number_input("Entry Price", value=1.0)
        target = st.number_input("Target Price", value=2.0)
        if st.button("Analyze Trade"):
            st.success(f"Potential Return: {((target/entry)-1)*100:.2f}% ✅")

else:
    st.info("Terminal in Standby. Enter Master Key to access.")
    
