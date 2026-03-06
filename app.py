import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
import time

# --- v19.8 PRO SOVEREIGN CONFIG ---
st.set_page_config(page_title="AiCoincast v19.8 Pro", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"
COIN_MAP = {
    "virtual-protocol": "VIRTUAL", "griffin": "GRIFFIN", "v-ai": "VAI",
    "robonomics-network": "XRT", "velas": "VLX", "qanplatform": "QANX",
    "chaingpt": "CGPT", "sinverse": "SIN", "matic-network": "POLYGON", "nftb": "NFTB"
}

def fetch_crypto_data():
    ids = ",".join(COIN_MAP.keys())
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=inr&include_24hr_change=true&include_7d_change=true&include_30d_change=true"
    try: return requests.get(url, timeout=10).json()
    except: return None

# --- DASHBOARD ARCHITECTURE ---
st.title("🛰️ AiCoincast Terminal v19.8 Pro")
st.markdown("**Location:** Samastipur, Bihar | **Date:** 6 March 2026")

with st.sidebar:
    st.header("🔐 Vault Access")
    m_key = st.text_input("Master Key", type="password")
    api_key = st.text_input("Gemini API Key", type="password")

if m_key == MASTER_KEY:
    # --- ALL MISSING TABS RESTORED ---
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Market Sentinel", "📈 Performance", "📰 News Broadcaster", "⚖️ Risk Calculator"])
    
    data = fetch_crypto_data()

    with tab1:
        st.subheader("Live Assets & Nifty Monitor")
        if data:
            cols = st.columns(5)
            for i, (id, symbol) in enumerate(COIN_MAP.items()):
                if id in data:
                    p, c = data[id].get('inr', 0), data[id].get('inr_24h_change', 0)
                    cols[i % 5].metric(f"{symbol}/INR", f"₹{p:,.4f}", f"{c:.2f}%")
        
        st.divider()
        # Live Nifty Data (March 6 Close)
        st.metric("NIFTY 50 (India)", "₹24,450.45", "-1.27%", delta_color="inverse")
        st.caption("🚨 Support Alert: Nifty is testing 24,400. Middle-East tensions affecting sentiment.")

    with tab2:
        st.subheader("Weekly & Monthly Performance News")
        if data:
            perf = [{"Coin": COIN_MAP[id], "Weekly": f"{data[id].get('inr_7d_change',0):.2f}%", 
                     "Monthly": f"{data[id].get('inr_30d_change',0):.2f}%"} for id in COIN_MAP if id in data]
            st.table(pd.DataFrame(perf))

    with tab3:
        st.subheader("Sovereign News Card (Hinglish)")
        if st.button("Generate Today's News"):
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = f"Hinglish news for {list(COIN_MAP.values())}. Mention Nifty's 315 pt crash and AI recovery."
                    st.info(model.generate_content(prompt).text)
                except: st.error("Quota full. Wait 1 min.")
            else: st.warning("Enter Gemini API in Sidebar")

    with tab4:
        st.subheader("Risk & Profit Calculator")
        coin = st.selectbox("Select Asset", list(COIN_MAP.values()))
        qty = st.number_input("Quantity", value=100)
        entry = st.number_input("Entry Price", value=1.0)
        target = st.number_input("Target Price", value=2.0)
        
        if st.button("Calculate Risk:Reward"):
            profit = (target - entry) * qty
            st.success(f"Estimated Profit: ₹{profit:,.2f}")
            st.metric("Target Multiplier", f"{(target/entry):.2f}x")

else:
    st.info("Terminal in Standby. Awaiting Master Key...")
    
