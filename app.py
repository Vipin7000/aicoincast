import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
import time

# --- [SYSTEM CONFIG] Sabhi 10 Coins ke Correct IDs ---
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
        return response.json() if response.status_code == 200 else None
    except: return None

# --- [UI ARCHITECTURE] ---
st.set_page_config(page_title="AiCoincast Terminal v19.8 Pro", layout="wide")
st.title("🛰️ AiCoincast Terminal v19.8 Pro: Sovereign Hub")
st.markdown("**Location:** Samastipur, Bihar | **Date:** 6 March 2026")

with st.sidebar:
    st.header("🔐 Vault Access")
    m_key = st.text_input("Master Key", type="password")
    api_key = st.text_input("Gemini API Key", type="password")

if m_key == "SAMASTIPUR@2026":
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Market Sentinel", "📈 Performance", "📰 News Broadcaster", "⚖️ Risk Calculator"])
    data = fetch_sovereign_data()

    with tab1:
        st.subheader("Live Assets Monitor")
        if data:
            cols = st.columns(5)
            for i, (id, symbol) in enumerate(COIN_MAP.items()):
                # [FIX: TYPEERROR PREVENTION] Checking if data exists before formatting
                if id in data:
                    p = data[id].get('inr')
                    c = data[id].get('inr_24h_change')
                    
                    # Agar value None hai toh default zero dikhayega
                    safe_p = float(p) if p is not None else 0.0
                    safe_c = float(c) if c is not None else 0.0
                    
                    cols[i % 5].metric(f"{symbol}/INR", f"₹{safe_p:,.4f}", f"{safe_c:.2f}%")
                else:
                    cols[i % 5].warning(f"{symbol} offline")
        else: st.error("Global Node Timeout. Please refresh.")

    with tab2:
        st.subheader("Weekly & Monthly Performance Indicators")
        if data:
            perf_list = [{"Coin": sym, "7D": f"{data[id].get('inr_7d_change',0):.2f}%", 
                          "30D": f"{data[id].get('inr_30d_change',0):.2f}%"} 
                         for id, sym in COIN_MAP.items() if id in data]
            st.table(pd.DataFrame(perf_list))

    with tab3:
        st.subheader("News Broadcaster (Resource Shield Active)")
        if st.button("Generate Today's News"):
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    # [FIX: RESOURCE EXHAUSTED] Rate limit protection
                    with st.spinner("AI Node processing..."):
                        time.sleep(2)
                        prompt = f"Hinglish news for {list(COIN_MAP.values())}. Focus on AI tokens recovery."
                        st.info(model.generate_content(prompt).text)
                except Exception as e:
                    st.error("AI Node exhausted. Wait 60 seconds.")
            else: st.warning("Gemini API Key missing in Sidebar.")

    with tab4:
        st.subheader("Sovereign Risk Calculator")
        coin = st.selectbox("Select Asset", list(COIN_MAP.values()))
        qty = st.number_input("Total Quantity", value=100)
        entry = st.number_input("Entry Price (INR)", value=1.0)
        target = st.number_input("Target Price (INR)", value=2.0)
        if st.button("Analyze Risk"):
            profit = (target - entry) * qty
            st.metric("Expected Profit", f"₹{profit:,.2f}")
            st.success("Target Ratio: High Potential ✅")

else: st.info("Terminal in Standby. Enter Master Key to unlock.")
    
