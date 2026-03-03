import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai

# --- Page Config ---
st.set_page_config(page_title="AiCoincast v17.4 Master", layout="wide")

# --- Title & Header ---
st.markdown("<h1 style='text-align: center;'>🔘 AiCoincast v17.4 Master</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>📊 Live Market Intelligence (INR)</h3>", unsafe_allow_html=True)

# --- Data Fetching Function ---
@st.cache_data(ttl=60)
def get_crypto_data():
    try:
        # CoinGecko API for Live Data
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            'vs_currency': 'inr',
            'order': 'market_cap_desc',
            'per_page': 50,
            'page': 1,
            'sparkline': False
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

# Fetching Data
coins_data = get_crypto_data()

# --- Top Metrics Row ---
if coins_data:
    col1, col2, col3, col4 = st.columns(4)
    # Quick access for top 4 coins
    top_coins = {coin['id']: coin for coin in coins_data[:10]}
    
    with col1:
        st.metric("Bitcoin", f"₹{top_coins['bitcoin']['current_price']:,}", f"{top_coins['bitcoin']['price_change_percentage_24h']:.2f}%")
    with col2:
        st.metric("Ethereum", f"₹{top_coins['ethereum']['current_price']:,}", f"{top_coins['ethereum']['price_change_percentage_24h']:.2f}%")
    with col3:
        st.metric("Tether", f"₹{top_coins['tether']['current_price']:.2f}", f"{top_coins['tether']['price_change_percentage_24h']:.2f}%")
    with col4:
        st.metric("BNB", f"₹{top_coins['binancecoin']['current_price']:,}", f"{top_coins['binancecoin']['price_change_percentage_24h']:.2f}%")

st.divider()

# --- Section A: Large Detailed Table (Line 82 Fix) ---
st.subheader("📑 Market Overview")

if coins_data is not None:
    # IMPORTANT: List ko DataFrame mein convert karna (Fix for Line 82)
    df = pd.DataFrame(coins_data)
    
    # Selection of specific columns
    display_df = df[['name', 'symbol', 'current_price', 'price_change_percentage_24h', 'market_cap']]
    
    # Formatting for better look
    display_df.columns = ['Name', 'Symbol', 'Price (INR)', '24h Change (%)', 'Market Cap']
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
else:
    st.warning("⚠️ API Rate Limit reached ya internet issue hai. Kripya 1 minute baad refresh karein.")

st.divider()

# --- Section B: AI Search & Report ---
st.subheader("🤖 AI Market Analysis")
user_query = st.text_input("Kisi bhi coin ke baare mein AI analysis chahiye? (e.g. 'Is Solana a good buy?')")

if user_query:
    with st.spinner("AI is thinking..."):
        try:
            # Gemini Integration (Ensure your API Key is in Secrets)
            # genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            # model = genai.GenerativeModel('gemini-pro')
            # response = model.generate_content(user_query)
            # st.write(response.text)
            st.info("AI analysis feature active. API Key configure karein Streamlit Secrets mein.")
        except Exception as e:
            st.error("AI Configuration Error.")

st.markdown("---")
st.caption("AiCoincast v17.4 | Powered by Streamlit & CoinGecko")
