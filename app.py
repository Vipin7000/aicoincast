import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
import time

# --- SYSTEM CONFIG (Sabhi 10 Coins Map Kar Diye Hain) ---
st.set_page_config(page_title="AiCoincast v19.8 Pro", layout="wide", page_icon="🛰️")

# Sovereign Asset List with correct CoinGecko IDs
COIN_MAP = {
    "virtual-protocol": "VIRTUAL", "griffin": "GRIFFIN", "v-ai": "VAI",
    "robonomics-network": "XRT", "velas": "VLX", "qanplatform": "QANX",
    "chaingpt": "CGPT", "sinverse": "SIN", "matic-network": "POLYGON", "nftb": "NFTB"
}

def fetch_sovereign_data():
    ids = ",".join(COIN_MAP.keys())
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=inr&include_24hr_change=true&include_7d_change=true&include_30d_change=true"
    try:
        response = requests.get(url, timeout=10)
        return response.json()
    except Exception as e:
        return None

# --- UI ARCHITECTURE ---
st.title("🛰️ AiCoincast Terminal v19.8 Pro: Sovereign Hub")
st.markdown("**Location:** Samastipur, Bihar | **Date:** 6 March 2026")

with st.sidebar:
    st.header("🔐 Vault Access")
    m_key = st.text_input("Master Key", type="password")
    api_key = st.text_input("Gemini API Key", type="password")

if m_key == "SAMASTIPUR@2026":
    # 4 TABS RESTORED
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Market Sentinel", "📈 Performance", "📰 News Broadcaster", "⚖️ Risk Calculator"])
    
    data = fetch_sovereign_data()

    with tab1:
        st.subheader("Live Assets & Nifty Monitor")
        if data:
            cols = st.columns(5)
            # ERROR FIX: Checking if each coin ID exists in API response before metric display
            for i, (id, symbol) in enumerate(COIN_MAP.items()):
                if id in data:
                    p = data[id].get('inr', 0)
                    c = data[id].get('inr_24h_change', 0)
                    cols[i % 5].metric(f"{symbol}/INR", f"₹{p:,.4f}", f"{c:.2f}%")
                else:
                    cols[i % 5].warning(f"{symbol} offline")
        else:
            st.error("Global Node Timeout. Please refresh.")

    with tab2:
        st.subheader("Weekly & Monthly Performance Indicators")
        if data:
            perf_list = []
            for id, symbol in COIN_MAP.items():
                if id in data:
                    perf_list.append({
                        "Coin": symbol,
                        "Price": f"₹{data[id]['inr']:,.4f}",
                        "7D Change": f"{data[id].get('inr_7d_change', 0):.2f}%",
                        "30D Change": f"{data[id].get('inr_30d_change', 0):.2f}%"
                    })
            st.table(pd.DataFrame(perf_list))

    with tab3:
        st.subheader("Sovereign News Card (Hinglish)")
        # RESOURCE EXHAUSTED FIX: Added rate limit safety
        if st.button("Generate Today's News"):
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    time.sleep(1) 
                    prompt = f"Hinglish news for {list(COIN_MAP.values())}. Focus on AI tokens recovery."
                    st.info(model.generate_content(prompt).text)
                except Exception as e:
                    st.error("API Limit reached. Wait 60 seconds.")
            else: st.warning("Enter Gemini API in Sidebar")

    with tab4:
        st.subheader("Risk & Profit Calculator")
        coin = st.selectbox("Select Asset", list(COIN_MAP.values()))
        entry = st.number_input("Entry Price", value=1.0)
        target = st.number_input("Target Price", value=2.0)
        if st.button("Calculate Risk:Reward"):
            ratio = (target - entry) / entry * 100
            st.metric("Potential Profit", f"{ratio:.2f}%")
else:
    st.info("Terminal in Standby. Awaiting Master Key...")
        
