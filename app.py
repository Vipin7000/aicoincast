import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai

# --- 1. Page Configuration ---
st.set_page_config(page_title="AiCoincast v17.4 Master", layout="wide", page_icon="🔘")

# --- 2. UI Custom Styling ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; border-radius: 10px; padding: 15px; border: 1px solid #30363d; }
    h1 { color: #ff4b4b; text-align: center; }
    h3 { text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. Header ---
st.markdown("<h1>🔘 AiCoincast v17.4 Master</h1>", unsafe_allow_html=True)
st.markdown("<h3>📊 Live Market Intelligence (INR)</h3>", unsafe_allow_html=True)

# --- 4. Data Fetching (CoinGecko) ---
@st.cache_data(ttl=60)
def get_crypto_data():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            'vs_currency': 'inr',
            'order': 'market_cap_desc',
            'per_page': 50,
            'sparkline': False
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

coins_data = get_crypto_data()

# --- 5. Top Metrics Row ---
if coins_data:
    col1, col2, col3, col4 = st.columns(4)
    # Mapping top 20 coins for stability
    m = {coin['id']: coin for coin in coins_data[:20]}
    
    with col1:
        st.metric("Bitcoin", f"₹{m['bitcoin']['current_price']:,}", f"{m['bitcoin']['price_change_percentage_24h']:.2f}%")
    with col2:
        st.metric("Ethereum", f"₹{m['ethereum']['current_price']:,}", f"{m['ethereum']['price_change_percentage_24h']:.2f}%")
    with col3:
        st.metric("Tether", f"₹{m['tether']['current_price']:.2f}", f"{m['tether']['price_change_percentage_24h']:.2f}%")
    with col4:
        st.metric("BNB", f"₹{m['binancecoin']['current_price']:,}", f"{m['binancecoin']['price_change_percentage_24h']:.2f}%")

st.divider()

# --- 6. Section A: Market Table (Line 82 FIXED) ---
st.subheader("📑 Market Overview")

if coins_data is not None:
    # SUCCESSFUL FIX: List ko DataFrame mein convert karna
    df_coins = pd.DataFrame(coins_data)
    
    # Selecting and formatting columns
    display_df = df_coins[['name', 'symbol', 'current_price', 'price_change_percentage_24h', 'market_cap']].copy()
    display_df.columns = ['Name', 'Symbol', 'Price (INR)', '24h Change (%)', 'Market Cap']
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
else:
    st.warning("⚠️ API Limit reached ya internet issue hai. Kripya 1 minute baad refresh karein.")

st.divider()

# --- 7. Section B: AI Search & Analysis ---
st.subheader("🤖 AI Market Analysis")

if "GEMINI_API_KEY" in st.secrets:
    try:
        # Correct Configuration
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        user_query = st.text_input("Kisi bhi coin ke baare mein AI analysis chahiye?", placeholder="e.g. Is Solana a good buy?")
        
        if user_query:
            with st.spinner("AI is thinking..."):
                response = model.generate_content(f"Analyze this for a crypto investor: {user_query}")
                st.info(f"### AI Insight:\n{response.text}")
    except Exception as e:
        st.error(f"AI Setup Error: {e}")
else:
    st.warning("⚠️ Streamlit Secrets mein 'GEMINI_API_KEY' missing hai.")

# --- 8. Footer ---
st.markdown("---")
st.caption("AiCoincast v17.4 Master | Updated March 2026")
                
