import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
import time

# --- SYSTEM CONFIG ---
st.set_page_config(page_title="AiCoincast v19.8 Pro", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

# Updated Sovereign Asset List (v19.8)
COIN_MAP = {
    "virtual-protocol": "VIRTUAL", "griffin": "GRIFFIN", "v-ai": "VAI",
    "robonomics-network": "XRT", "velas": "VLX", "qanplatform": "QANX",
    "chaingpt": "CGPT", "sinverse": "SIN", "matic-network": "POLYGON", "nftb": "NFTB"
}

def get_market_data():
    ids = ",".join(COIN_MAP.keys())
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=inr&include_24hr_change=true&include_7d_change=true&include_30d_change=true"
    try:
        return requests.get(url, timeout=10).json()
    except: return None

# --- UI LOGIC ---
st.title("🛰️ AiCoincast Terminal v19.8 Pro: Sovereign Hub")

with st.sidebar:
    st.header("🔐 Vault Access")
    m_key = st.text_input("Master Key", type="password")
    api_key = st.text_input("Gemini API Key", type="password")

if m_key == MASTER_KEY:
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Market Monitor", "📈 Performance", "📰 News Card", "⚖️ Risk Calculator"])
    data = get_market_data()

    with tab1:
        st.subheader("Live Price Node (Real-Time)")
        if data:
            cols = st.columns(5)
            for i, (id, sym) in enumerate(COIN_MAP.items()):
                price, change = data[id]['inr'], data[id]['inr_24h_change']
                cols[i % 5].metric(f"{sym}/INR", f"₹{price:,.4f}", f"{change:.2f}%")

    with tab2:
        st.subheader("Weekly & Monthly Performance Indicators")
        if data:
            perf_data = [{"Asset": COIN_MAP[id], "Price": f"₹{data[id]['inr']:,.4f}", 
                          "7D Change": f"{data[id].get('inr_7d_change', 0):.2f}%", 
                          "30D Change": f"{data[id].get('inr_30d_change', 0):.2f}%"} for id in COIN_MAP]
            st.table(pd.DataFrame(perf_data))

    with tab3:
        st.subheader("Hinglish News Generator")
        if st.button("Generate v19.8 News Card"):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"Provide a witty Hinglish news update for {list(COIN_MAP.values())}. Mention Nifty's 1.2% dip and Crypto Fear Index at 19."
                st.info(model.generate_content(prompt).text)
            except: st.error("AI Node Offline. Check API Key.")

    with tab4:
        st.subheader("Sovereign Risk-to-Reward Calculator")
        coin = st.selectbox("Select Asset", list(COIN_MAP.values()))
        entry = st.number_input("Entry Price (INR)", value=1.0)
        target = st.number_input("Target Price (INR)", value=1.5)
        stoploss = st.number_input("Stop Loss (INR)", value=0.8)
        
        if st.button("Calculate Ratio"):
            risk = entry - stoploss
            reward = target - entry
            ratio = reward / risk if risk > 0 else 0
            st.metric("Risk:Reward Ratio", f"1:{ratio:.2f}")
            if ratio >= 3: st.success("Strong Buy Signal: High Reward Setup ✅")
            else: st.warning("Caution: Risk is high compared to reward. ⚠️")

else:
    st.info("Terminal in Standby. Awaiting Master Key...")
    
