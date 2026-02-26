import streamlit as st
import google.generativeai as genai
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from gtts import gTTS
import io
import hashlib
import requests
from datetime import datetime
import pytz
from sklearn.linear_model import LinearRegression

# --- 1. CORE CONFIGURATION & IST TIME ---
st.set_page_config(page_title="AiCoincast India: Master Terminal", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
ist_now = datetime.now(IST).strftime('%d %b %Y | %H:%M:%S IST')

# --- 2. SECURITY: BOT AUTHENTICATION ALGORITHM ---
def generate_bot_token(bot_id):
    return f"AIC-{hashlib.sha256(bot_id.encode()).hexdigest()[:12].upper()}"

# --- 3. DATA: UNIVERSAL CRYPTO FETCHING ---
def get_universal_crypto(coin_id):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=inr,usd&include_24hr_change=true"
        response = requests.get(url, timeout=5)
        return response.json().get(coin_id)
    except: return None

# --- 4. PREDICTION: 7-DAY FORECAST ALGORITHM ---
def get_ai_forecast(symbol):
    try:
        data = yf.download(symbol, period='60d', interval='1d')
        if data.empty: return None
        df = data[['Close']].reset_index()
        df['Day_Num'] = np.arange(len(df))
        model = LinearRegression().fit(df[['Day_Num']], df['Close'])
        future_days = np.array([len(df) + i for i in range(7)]).reshape(-1, 1)
        preds = model.predict(future_days)
        future_dates = [df['Date'].iloc[-1] + pd.Timedelta(days=i) for i in range(1, 8)]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name='Market', line=dict(color='#00ffcc')))
        fig.add_trace(go.Scatter(x=future_dates, y=preds, name='AI Forecast', line=dict(dash='dash', color='#ffcc00')))
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,t=30,b=0))
        return fig
    except: return None

# --- 5. UI BRANDING ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #1e2130; border-radius: 5px; padding: 10px; }
    .verified-card { border-left: 5px solid #138808; background: #1a1c24; padding: 15px; border-radius: 5px; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- 6. SIDEBAR & API ---
st.sidebar.title("🛡️ Master Control")
st.sidebar.info(f"🕒 **IST:** {ist_now}")
api_key = st.secrets.get("GEMINI_API_KEY", "")
if api_key: genai.configure(api_key=api_key)

# --- 7. MAIN INTERFACE ---
st.title("🛡️ AiCoincast India: Sovereign Master Node")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["🤝 Bot Alliance", "📈 AI Prediction", "🌍 Universal Crypto", "👨‍💻 API Docs"])

# --- TAB 1: BOT ALLIANCE (GUEST BOTS & SOUND) ---
with tab1:
    st.subheader("🤖 Invite & Verify AI Bots")
    c1, c2 = st.columns(2)
    with c1: guest_id = st.text_input("Bot Name", "CryptoX-Bot")
    with c2: guest_token = st.text_input("Auth Token", type="password")
    
    news_payload = st.text_area("Guest Bot News Feed:", height=150)
    lang = st.radio("Output Language:", ["Hindi", "English"], horizontal=True)

    if st.button("⚡ Authenticate & Generate Master Report"):
        if guest_token == generate_bot_token(guest_id):
            st.success(f"Verified: {guest_id} connection secure.")
            with st.spinner("Sovereign Master is processing..."):
                model = genai.GenerativeModel('gemini-pro')
                p_lang = "Hindi" if lang == "Hindi" else "English"
                res = model.generate_content(f"Verify and rewrite this news from {guest_id} for India in {p_lang}: {news_payload}")
                st.session_state.final_output = res.text
                st.session_state.lang_code = 'hi' if lang == "Hindi" else 'en'
                st.markdown(f"<div class='verified-card'>{res.text}</div>", unsafe_allow_html=True)
        else: st.error("Access Denied: Invalid Token.")

    if st.button("🔊 Play Verified Audio"):
        if 'final_output' in st.session_state:
            tts = gTTS(text=st.session_state.final_output, lang=st.session_state.lang_code)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            st.audio(fp, format='audio/mp3')

# --- TAB 2: AI PREDICTION ---
with tab2:
    st.subheader("🚀 7-Day Trend Forecasting")
    coin_p = st.selectbox("Select Asset", ["BTC-USD", "ETH-USD", "SOL-USD", "MATIC-USD"])
    if st.button("📈 Run AI Prediction"):
        fig = get_ai_forecast(coin_p)
        if fig: st.plotly_chart(fig, use_container_width=True)

# --- TAB 3: UNIVERSAL CRYPTO (XRT, LAI, QRL FIX) ---
with tab3:
    st.subheader("🌍 Universal Coin Tracker")
    user_coin = st.text_input("Enter Coin ID (e.g. robonomics-network-xrt, layerai, quantum-resistant-ledger)", "bitcoin")
    if st.button("🔍 Fetch Global Data"):
        data = get_universal_crypto(user_coin)
        if data:
            st.metric(f"{user_coin.upper()} Price (USD)", f"${data['usd']:.4f}", f"{data['usd_24h_change']:.2f}%")
            st.metric(f"{user_coin.upper()} Price (INR)", f"₹{data['inr']:.2f}")
        else: st.error("Coin not found. Use CoinGecko ID.")

# --- TAB 4: DEVELOPER API ---
with tab4:
    st.subheader("👨‍💻 Alliance Documentation")
    st.write("Invitation to External AI Bots: Generate your token here.")
    dev_name = st.text_input("Your Bot Name:")
    if dev_name:
        st.code(f"Your Token: {generate_bot_token(dev_name)}")
    st.markdown("---")
    st.info("Sovereign Protocol v11.0 Active")

# --- NATIONAL MARKET PULSE (Footer) ---
st.markdown("---")
nifty = yf.Ticker("^NSEI").history(period="1d")['Close'].iloc[-1]
st.sidebar.metric("NSE NIFTY 50", f"₹{nifty:,.2f}")
            
