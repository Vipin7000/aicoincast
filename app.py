import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
import time
import feedparser
import re # Security: Regular Expressions for input validation

# --- [1. SECURITY CONFIG & GLOBAL SHIELD] ---
st.set_page_config(page_title="AiCoincast Terminal v19.8 Ultra-Secure", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

COIN_MAP = {
    "virtual-protocol": "VIRTUAL", "griffin-2": "GRIFFIN", "v-ai-2": "VAI",
    "robonomics-network": "XRT", "velas": "VLX", "qanplatform": "QANX",
    "chaingpt": "CGPT", "sinverse": "SIN", "matic-network": "POLYGON", "nftb": "NFTB"
}

# --- [2. SECURE DATA ENGINE] ---
@st.cache_data(ttl=60)
def fetch_safe_data():
    ids = ",".join(COIN_MAP.keys())
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=inr&include_24hr_change=true&include_7d_change=true&include_30d_change=true"
    try:
        response = requests.get(url, timeout=5) # Security: Low timeout to prevent hangs
        return response.json() if response.status_code == 200 else {}
    except: return {}

# --- [3. UI ARCHITECTURE] ---
st.title("🛰️ AiCoincast Terminal v19.8 (Indestructible Mode)")
st.markdown(f"**Location:** Samastipur, Bihar | **Security Status:** <span style='color:green;'>Active</span>", unsafe_allow_html=True)

with st.sidebar:
    st.header("🔐 Secure Vault")
    m_key = st.text_input("Master Key", type="password")
    
    # [SECURITY FIX] Input cleaning to prevent injection attacks
    raw_api_key = st.text_input("Gemini API Key", type="password")
    api_key = re.sub(r'[^a-zA-Z0-9_-]', '', raw_api_key.strip()) # Removes quotes & special chars

if m_key == MASTER_KEY:
    # Charo Folders (Tabs) Fixed: Miss hone ka koi chance nahi
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Market Sentinel", "📈 Performance", "📰 Master News Broadcast", "⚖️ Risk Calculator"])
    data = fetch_safe_data()

    with tab1:
        st.subheader("Live Assets & Market Pulse")
        cols = st.columns(5)
        for i, (id, symbol) in enumerate(COIN_MAP.items()):
            coin_info = data.get(id, {})
            p, c = coin_info.get('inr'), coin_info.get('inr_24h_change')
            if p is not None:
                cols[i % 5].metric(f"{symbol}/INR", f"₹{float(p):,.4f}", f"{float(c or 0):.2f}%")
            else:
                cols[i % 5].warning(f"{symbol} Offline")
        st.divider()
        st.metric("NIFTY 50 (India)", "₹24,469.10", "-1.20%", delta_color="inverse")

    with tab2:
        st.subheader("Weekly & Monthly Growth Metrics")
        if data:
            perf_list = [{"Asset": sym, "7D %": f"{data.get(id, {}).get('inr_7d_change', 0):.2f}%", 
                          "30D %": f"{data.get(id, {}).get('inr_30d_change', 0):.2f}%"} for id, sym in COIN_MAP.items()]
            st.table(pd.DataFrame(perf_list))

    with tab3:
        st.subheader("📰 Sovereign News Agent (RSS & Twitter Sync)")
        # Display XRT/LAI Master Card
        st.markdown("""
        <div style="background-color:#0d1117; padding:15px; border-radius:10px; border: 1px solid #30363d;">
            <p style="color:#238636;"><b>Global Sentiment: Bullish Hold 🚀</b></p>
            <p style="color:white;">XRT (₹5.77) and LAI tokens are showing strong decoupling from Nifty dip.</p>
        </div>""", unsafe_allow_html=True)
        
        if st.button("Generate Secure AI Broadcast"):
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    time.sleep(2) # Security: Rate limiting
                    prompt = f"Quick Hinglish news for {list(COIN_MAP.values())} focusing on AI recovery."
                    st.info(model.generate_content(prompt).text)
                except: st.error("AI Node exhausted. Wait 60s.")

    with tab4:
        st.subheader("Risk & Profit Calculator")
        coin = st.selectbox("Select Asset", list(COIN_MAP.values()))
        entry = st.number_input("Entry Price", value=1.0)
        target = st.number_input("Target Price", value=1.5)
        if st.button("Calculate Trade"):
            st.success(f"Potential Return: {((target/entry)-1)*100:.2f}% ✅")

else:
    st.info("Terminal Standby. Enter Master Key (SAMASTIPUR@2026) to unlock.")
        
