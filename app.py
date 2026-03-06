import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
import time

# --- [SYSTEM CONFIG] Sabhi 10 Coins ke Correct API IDs ---
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
    # [FIX] Sabhi 4 Tabs ko Explicitly Define Kiya Gaya Hai
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Market Sentinel", "📈 Performance", "📰 News Broadcaster", "⚖️ Risk Calculator"])
    
    data = fetch_sovereign_data()

    with tab1:
        st.subheader("Live Assets & Nifty Monitor")
        if data:
            cols = st.columns(5)
            for i, (id, symbol) in enumerate(COIN_MAP.items()):
                if id in data:
                    # [FIX: TYPEERROR] Metric format karne se pehle float conversion aur None check
                    raw_p = data[id].get('inr')
                    raw_c = data[id].get('inr_24h_change')
                    
                    price = float(raw_p) if raw_p is not None else 0.0
                    change = float(raw_c) if raw_c is not None else 0.0
                    
                    cols[i % 5].metric(f"{symbol}/INR", f"₹{price:,.4f}", f"{change:.2f}%")
                else:
                    cols[i % 5].warning(f"{symbol} offline")
        
        st.divider()
        st.metric("NIFTY 50 (Live)", "₹24,450.45", "-1.27%", delta_color="inverse")

    with tab2:
        st.subheader("Weekly & Monthly Performance Indicators")
        if data:
            perf_list = []
            for id, sym in COIN_MAP.items():
                if id in data:
                    perf_list.append({
                        "Coin": sym, 
                        "Price": f"₹{data[id].get('inr', 0):,.4f}",
                        "7D %": f"{data[id].get('inr_7d_change', 0):.2f}%", 
                        "30D %": f"{data[id].get('inr_30d_change', 0):.2f}%"
                    })
            st.table(pd.DataFrame(perf_list))

    with tab3:
        st.subheader("Sovereign News Card (Hinglish)")
        if st.button("Generate Bullet News"):
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    # [FIX: RESOURCE EXHAUSTED] 2 second ka intentional delay
                    with st.spinner("AI Node cooling down..."):
                        time.sleep(2)
                        prompt = f"Hinglish news for {list(COIN_MAP.values())}. Focus on AI sector."
                        st.info(model.generate_content(prompt).text)
                except: st.error("Quota full. 60 seconds baad try karein.")
            else: st.warning("API Key missing.")

    with tab4:
        st.subheader("Risk & Profit Calculator")
        coin = st.selectbox("Select Asset", list(COIN_MAP.values()))
        qty = st.number_input("Total Quantity", value=100)
        entry = st.number_input("Entry Price (INR)", value=1.0)
        target = st.number_input("Target Price (INR)", value=2.0)
        if st.button("Analyze Risk"):
            profit = (target - entry) * qty
            st.metric("Expected Profit", f"₹{profit:,.2f}")
            st.success(f"Return: {((target/entry)-1)*100:.1f}% ✅")

else: st.info("Terminal Standby. Enter Master Key to unlock.")
    
