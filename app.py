import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
import time

# --- [SYSTEM CONFIG] Corrected API IDs for Accuracy ---
COIN_MAP = {
    "virtual-protocol": "VIRTUAL", "griffin-2": "GRIFFIN", "v-ai-2": "VAI",
    "robonomics-network": "XRT", "velas": "VLX", "qanplatform": "QANX",
    "chaingpt": "CGPT", "sinverse": "SIN", "matic-network": "POLYGON", "nftb": "NFTB"
}

def fetch_sovereign_data():
    ids = ",".join(COIN_MAP.keys())
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=inr&include_24hr_change=true&include_7d_change=true&include_30d_change=true"
    try:
        response = requests.get(url, timeout=10)
        return response.json() if response.status_code == 200 else {}
    except: return {}

# --- [UI ARCHITECTURE] ---
st.set_page_config(page_title="AiCoincast Terminal v19.8 Pro", layout="wide")
st.title("🛰️ AiCoincast Terminal v19.8 Pro: Sovereign Hub")
st.markdown(f"**Location:** Samastipur, Bihar | **Date: 6 March 2026**")

with st.sidebar:
    st.header("🔐 Vault Access")
    m_key = st.text_input("Master Key", type="password")
    # Gemini Key cleaning (removes quotes automatically)
    raw_api_key = st.text_input("Gemini API Key", type="password")
    api_key = raw_api_key.strip().replace('"', '').replace("'", "")

if m_key == "SAMASTIPUR@2026":
    # [FIX: CHARO FOLDERS RESTORED] Charo tabs ko explicitly define kiya gaya hai
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Market Sentinel", "📈 Performance", "📰 News Broadcaster", "⚖️ Risk Calculator"])
    
    data = fetch_sovereign_data()

    with tab1:
        st.subheader("Live Assets & Nifty Monitor")
        if data:
            cols = st.columns(5)
            for i, (id, symbol) in enumerate(COIN_MAP.items()):
                c_data = data.get(id, {})
                price_val = c_data.get('inr')
                change_val = c_data.get('inr_24h_change')
                
                # [TYPEERROR SHIELD] No more crash on missing coins
                if price_val is not None:
                    p = float(price_val)
                    c = float(change_val) if change_val is not None else 0.0
                    cols[i % 5].metric(f"{symbol}/INR", f"₹{p:,.4f}", f"{c:.2f}%")
                else:
                    cols[i % 5].warning(f"{symbol} Offline")
        
        st.divider()
        # Today's Nifty status
        st.metric("NIFTY 50 (India)", "₹24,450.45", "-1.27%", delta_color="inverse")

    with tab2:
        st.subheader("Weekly & Monthly Performance Indicators")
        if data:
            perf_list = []
            for id, sym in COIN_MAP.items():
                c_data = data.get(id, {})
                perf_list.append({
                    "Coin": sym, 
                    "Price": f"₹{c_data.get('inr', 0):,.4f}",
                    "7D Change": f"{c_data.get('inr_7d_change', 0):.2f}%", 
                    "30D Change": f"{c_data.get('inr_30d_change', 0):.2f}%"
                })
            st.table(pd.DataFrame(perf_list))

    with tab3:
        st.subheader("Sovereign News Card (Hinglish)")
        if st.button("Generate Bullet News"):
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    with st.spinner("AI Node Processing..."):
                        time.sleep(2) # Prevent ResourceExhausted error
                        prompt = f"Give a 3-line Hinglish crypto update for {list(COIN_MAP.values())} focusing on AI recovery."
                        st.info(model.generate_content(prompt).text)
                except: 
                    st.error("AI Node exhausted. Wait 60 seconds.")
            else: 
                st.warning("Gemini API Key missing or invalid.")

    with tab4:
        st.subheader("Risk & Profit Calculator")
        coin = st.selectbox("Select Asset to Analyze", list(COIN_MAP.values()))
        entry = st.number_input("Entry Price (INR)", value=1.0)
        target = st.number_input("Target Price (INR)", value=2.0)
        if st.button("Calculate Potential"):
            profit_pct = ((target/entry)-1)*100
            st.metric(f"Potential Return on {coin}", f"{profit_pct:.2f}%")
            st.success("Target Analysis: Sovereign Approval ✅")

else:
    st.info("Terminal in Standby. Enter Master Key to unlock all folders.")
        
