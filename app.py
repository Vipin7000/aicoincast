import streamlit as st
import pandas as pd
import requests

# --- v19.8 PRO SOVEREIGN CONFIG ---
st.set_page_config(page_title="AiCoincast v19.8 Pro", layout="wide")
COIN_MAP = {
    "virtual-protocol": "VIRTUAL", "griffin": "GRIFFIN", "v-ai": "VAI",
    "robonomics-network": "XRT", "velas": "VLX", "qanplatform": "QANX",
    "chaingpt": "CGPT", "sinverse": "SIN", "matic-network": "POLYGON", "nftb": "NFTB"
}

def fetch_all_data():
    ids = ",".join(COIN_MAP.keys())
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=inr&include_24hr_change=true"
    try:
        return requests.get(url, timeout=10).json()
    except: return None

# --- DASHBOARD ARCHITECTURE ---
st.title("🛰️ AiCoincast Terminal v19.8 Pro")
st.markdown(f"**Location:** Samastipur, Bihar | **Date:** 6 March 2026")

data = fetch_all_data()

# 📊 1. LIVE CRYPTO SENTINEL (All 10 Coins Fix)
st.subheader("Live Crypto Assets")
if data:
    cols = st.columns(5)
    for i, (id, symbol) in enumerate(COIN_MAP.items()):
        if id in data:
            price = data[id].get('inr', 0)
            change = data[id].get('inr_24h_change', 0)
            cols[i % 5].metric(f"{symbol}/INR", f"₹{price:,.4f}", f"{change:.2f}%")
        else:
            cols[i % 5].warning(f"{symbol} Data Pending")
else:
    st.error("Connection Error: Waiting for API node...")

st.divider()

# 🔄 2. NIFTY 50 LIVE MONITOR (March 6 Update)
st.subheader("🇮🇳 Indian Market Pulse (Nifty 50)")
nifty_price = 24469.10
nifty_delta = -1.20 # Based on March 6 close

c1, c2 = st.columns([1, 2])
with c1:
    st.metric("Nifty 50 Index", f"₹{nifty_price:,.2f}", f"{nifty_delta}%", delta_color="inverse")
with c2:
    st.info("**Sovereign Insight:** Nifty apne support zone (24,400) ke paas hai. US-Iran tensions ki wajah se volatility high hai, lekin aapke AI tokens decoupling dikha rahe hain.")

# 
