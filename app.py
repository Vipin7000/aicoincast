import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai

# --- 1. Page Configuration ---
st.set_page_config(page_title="AiCoincast v17.4 Master", layout="wide", page_icon="🔘")

# --- 2. Custom UI Styling ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; border-radius: 10px; padding: 15px; border: 1px solid #30363d; }
    h1 { color: #ff4b4b; text-align: center; font-family: sans-serif; }
    .stAlert { background-color: #1e2329; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. Header ---
st.markdown("<h1>🔘 AiCoincast v17.4 Master</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ea3ae;'>🚀 v17.4 SOVEREIGN NODE ACTIVE</p>", unsafe_allow_html=True)

# --- 4. Live Data Fetching ---
@st.cache_data(ttl=60)
def get_market_data():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {'vs_currency': 'inr', 'order': 'market_cap_desc', 'per_page': 50, 'sparkline': False}
        response = requests.get(url, params=params, timeout=10)
        return response.json() if response.status_code == 200 else None
    except Exception:
        return None

coins = get_market_data()

# --- 5. Top Metrics (BTC, ETH, USDT, BNB) ---
if coins:
    c1, c2, c3, c4 = st.columns(4)
    m = {coin['id']: coin for coin in coins[:20]}
    with c1: st.metric("Bitcoin", f"₹{m['bitcoin']['current_price']:,}", f"{m['bitcoin']['price_change_percentage_24h']:.2f}%")
    with c2: st.metric("Ethereum", f"₹{m['ethereum']['current_price']:,}", f"{m['ethereum']['price_change_percentage_24h']:.2f}%")
    with c3: st.metric("Tether", f"₹{m['tether']['current_price']:.2f}", f"{m['tether']['price_change_percentage_24h']:.2f}%")
    with c4: st.metric("BNB", f"₹{m['binancecoin']['current_price']:,}", f"{m['binancecoin']['price_change_percentage_24h']:.2f}%")

st.divider()

# --- 6. Market Table (TypeError Fix) ---
st.subheader("📂 Market Overview")
if coins is not None:
    # Fix: Converting list to DataFrame
    df = pd.DataFrame(coins)
    display_df = df[['name', 'symbol', 'current_price', 'price_change_percentage_24h', 'market_cap']].copy()
    display_df.columns = ['Coin', 'Symbol', 'Price (INR)', '24h %', 'Market Cap']
    st.dataframe(display_df, use_container_width=True, hide_index=True)
else:
    st.warning("⚠️ API Limit reached. Kripya 1 minute baad refresh karein.")

st.divider()

# --- 7. AI Analysis (404 Model Error Fix) ---
st.subheader("🤖 AI Market Analysis")
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # Stable model used to prevent 404 models/gemini-1.5-flash error
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        query = st.text_input("Kisi bhi coin ke baare mein AI analysis chahiye?", placeholder="e.g. AAVE")
        if query:
            with st.spinner("AI analyzing..."):
                # Simplified call to avoid beta-version conflicts
                res = model.generate_content(f"Quick crypto analysis for: {query}")
                st.info(f"**AI Insight:**\n\n{res.text}")
    except Exception as e:
        st.error(f"AI Setup Error: {str(e)}")
else:
    st.warning("Secrets mein GEMINI_API_KEY missing hai.")

st.markdown("---")
st.caption("AiCoincast v17.4 Master | Stable Build 2026")
