import streamlit as st
import yfinance as yf
import google.generativeai as genai
import pandas as pd
import streamlit.components.v1 as components
import re

# --- 1. SETTINGS & NATIONAL BRANDING ---
st.set_page_config(page_title="AiCoincast India | Global Crypto Intel", layout="wide")

# API Key Security
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')

# Midnight Purple & Cyber Blue Theme
st.markdown("""
    <style>
    .main { background-color: #0A0E14; color: #FFFFFF; }
    .stMetric { background-color: #161B22; padding: 15px; border-radius: 10px; border: 1px solid #00F5FF; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. FAST ALGORITHMS (TRACKING & SECURITY) ---
@st.cache_data(ttl=60)
def get_crypto_data(coins):
    data = {}
    for name, sym in coins.items():
        try:
            ticker = yf.Ticker(sym).history(period="1d")
            data[name] = ticker['Close'].iloc[-1]
        except: data[name] = "Live"
    return data

def is_company_email(email):
    public_domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]
    domain = email.split('@')[-1] if "@" in email else ""
    return (domain not in public_domains and domain != ""), domain

# 20-Coin Tracker List
top_20_coins = {
    "Bitcoin": "BTC-USD", "Ethereum": "ETH-USD", "Solana": "SOL-USD", "Cardano": "ADA-USD",
    "Ripple": "XRP-USD", "Polkadot": "DOT-USD", "Polygon": "MATIC-USD", "Dogecoin": "DOGE-USD",
    "Shiba Inu": "SHIB-USD", "Litecoin": "LTC-USD", "Avalanche": "AVAX-USD", "Chainlink": "LINK-USD",
    "Uniswap": "UNI-USD", "Cosmos": "ATOM-USD", "Stellar": "XLM-USD", "Monero": "XMR-USD",
    "ETC": "ETC-USD", "Near": "NEAR-USD", "Algorand": "ALGO-USD", "Quant": "QNT-USD"
}

# --- 3. UI LAYOUT & TICKER ---
ticker_html = """
<div style="background-color: #161B22; color: #00F5FF; padding: 10px; font-family: sans-serif; border-bottom: 2px solid #00F5FF;">
    <marquee scrollamount="6">🚀 🇮🇳 AiCoincast India: Tracking 20+ Assets | 🛡️ AI-Shield Active | 🌎 Global Market Intelligence Live...</marquee>
</div>
"""
components.html(ticker_html, height=50)

with st.sidebar:
    st.title("🏢 Partner Login")
    email = st.text_input("Company Email")
    if st.button("Login"):
        valid, dom = is_company_email(email)
        if valid:
            st.success(f"Verified: {dom}")
        else:
            st.error("Official Email Required")

st.title("🛡️ AiCoincast India")
st.caption("India's Premier AI-Powered Crypto Terminal | Samastipur to Global Vision")

# --- 4. 20-COIN LIVE TRACKER GRID ---
st.write("### ⚡ Live 20-Coin Tracker")
live_prices = get_crypto_data(top_20_coins)
cols = st.columns(5)
for i, (name, val) in enumerate(live_prices.items()):
    cols[i % 5].metric(name, f"${val:,.2f}" if isinstance(val, float) else val)

st.divider()

# --- 5. THE "BIG 5" COMPARISON ENGINE ---
st.write("### 📊 Deep Compare (Select 5 Coins)")
selected_coins = st.multiselect("Pick 5 coins to analyze side-by-side", list(top_20_coins.keys()), default=list(top_20_coins.keys())[:5])

if len(selected_coins) == 5:
    comp_data = []
    for c in selected_coins:
        t = yf.Ticker(top_20_coins[c]).info
        comp_data.append({
            "Coin": c,
            "Price": f"${t.get('currentPrice', 0):,.2f}",
            "Market Cap": f"${t.get('marketCap', 0):,.0f}",
            "24h Volume": f"${t.get('totalVolume', 0):,.0f}"
        })
    st.table(pd.DataFrame(comp_data))
else:
    st.info("Exactly 5 coins select karein deep comparison ke liye.")

st.divider()

# --- 6. NEWS & CORPORATE INTEL (XRT, LAI, QRL) ---
def news_card(title, content, source, author_type="AI"):
    bg = "#000000" if author_type == "AI" else "#062c12"
    border = "#00F5FF" if author_type == "AI" else "#00FF00"
    label = "🤖 AI CRAWLER" if author_type == "AI" else "👤 OFFICIAL SOURCE"
    st.markdown(f"""
        <div style="background-color: {bg}; color: white; padding: 20px; border-radius: 10px; 
                    border-left: 5px solid {border}; margin-bottom: 15px;">
            <span style="color: {border}; font-weight: bold; font-size: 11px;">{label}</span>
            <h3 style="margin-top: 5px;">{title}</h3>
            <p style="font-size: 14px; opacity: 0.9;">{content}</p>
            <p style="font-size: 11px; opacity: 0.6;">Source: {source}</p>
        </div>
    """, unsafe_allow_html=True)

c1, c2 = st.columns([2, 1])
with c1:
    st.subheader("📰 Verified Intelligence")
    news_card("Market Analytics Update", "Institutional interest rising in Indian crypto projects.", "Bloomberg API", "AI")
    # Corporate Expanders for XRT, LAI, QRL
    with st.expander("🏢 Corporate Asset Deep-Dive"):
        asset = st.selectbox("Select Asset", ["XRT", "LAI", "QRL"])
        if st.button("Get One-Click Info"):
            st.write(f"Fetching Blockchain data for {asset}...")

with c2:
    st.subheader("🤖 AI Assistant")
    ask = st.chat_input("Ask about market...")
    if ask and "GEMINI_API_KEY" in st.secrets:
        st.info(model.generate_content(f"Answer in Hinglish: {ask}").text)

st.markdown("---")
st.caption("© 2026 AiCoincast.in | Secured by AI | India's Digital Excellence")
