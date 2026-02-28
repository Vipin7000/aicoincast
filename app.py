import streamlit as st
import yfinance as yf
import pandas as pd
import google.generativeai as genai
import streamlit.components.v1 as components
import plotly.graph_objects as go
import plotly.express as px
from gtts import gTTS
import io
import hashlib
import requests
import numpy as np
from datetime import datetime
import pytz
from sklearn.linear_model import LinearRegression

# --- 1. CORE SETTINGS & IST TIME ---
st.set_page_config(page_title="AiCoincast | Command Center", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
ist_now = datetime.now(IST).strftime('%d %b %Y | %H:%M:%S IST')

# AI Configuration
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')

# Custom CSS for Command Center Look
st.markdown("""
    <style>
    .main { background-color: #0B0E14; color: #FFFFFF; }
    .stMetric { background-color: #161B22; padding: 15px; border-radius: 10px; border: 1px solid #BC13FE; }
    .news-card { background-color: #161B22; padding: 20px; border-radius: 10px; border-left: 5px solid #00F5FF; margin-bottom: 15px; }
    .stButton>button { background: linear-gradient(90deg, #BC13FE, #00F5FF); color: white; border: none; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ADVANCED ALGORITHMS ---

def get_universal_crypto(coin_id):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=inr,usd&include_24hr_change=true&include_market_cap=true"
        res = requests.get(url, timeout=5).json()
        return res.get(coin_id)
    except: return None

def is_company_email(email):
    public_domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]
    domain = email.split('@')[-1] if "@" in email else ""
    return (domain not in public_domains and domain != ""), domain

# --- 3. UI LAYOUT ---

# Scrolling Market Ticker
ticker_text = f"🛡️ SOVEREIGN COMMAND CENTER ACTIVE | 🕒 IST: {ist_now} | 🚀 XRT & LAI MONITORED | 🏢 PARTNER NODE: Samastipur"
components.html(f"""
    <div style="background-color: #161B22; color: #00F5FF; padding: 10px; font-family: sans-serif; border-bottom: 2px solid #BC13FE;">
        <marquee scrollamount="6"><strong>{ticker_text}</strong></marquee>
    </div>
    """, height=50)

# Sidebar: Partner Portal
with st.sidebar:
    st.title("🏢 Command Portal")
    email = st.text_input("Partner Email")
    if st.button("Authorize"):
        valid, dom = is_company_email(email)
        if valid:
            st.success(f"Access Granted: {dom}")
            st.session_state['partner'] = dom
        else: st.error("Business Email Required")
    
    st.markdown("---")
    st.write(f"📡 Node: **Reliance Digital Hub**")
    st.write(f"⏰ {ist_now}")

# Main Header
st.title("🤖 AiCoincast v14.0")
st.subheader("Global Financial Command Center")

# --- 4. NAVIGATION TABS ---
tab_market, tab_news, tab_predict, tab_portfolio = st.tabs([
    "📊 Market Sentiment", "📰 Verified Feed", "📈 AI Forecast", "💰 Portfolio Analytics"
])

# --- TAB 1: MARKET SENTIMENT ---
with tab_market:
    st.subheader("🌍 Global Market Sentiment")
    col1, col2, col3, col4 = st.columns(4)
    
    # Live Data Fetch for Sentiment
    btc = get_universal_crypto("bitcoin")
    xrt = get_universal_crypto("robonomics-network")
    
    if btc: col1.metric("BITCOIN", f"${btc['usd']:,}", f"{btc['usd_24h_change']:.2f}%")
    if xrt: col2.metric("XRT (Robonomics)", f"${xrt['usd']:.2f}", f"{xrt['usd_24h_change']:.2f}%")
    
    # Sentiment Gauge (Mock Logic based on 24h change)
    sentiment_val = "BULLISH 🚀" if btc['usd_24h_change'] > 0 else "BEARISH 📉"
    col3.metric("MARKET MOOD", sentiment_val)
    col4.metric("AI RISK LEVEL", "LOW 🛡️")

# --- TAB 2: VERIFIED FEED (With Audio) ---
with tab_news:
    st.subheader("📰 AI-Verified Intelligence")
    lang = st.radio("Voice Language:", ["Hindi", "English"], horizontal=True)
    report_input = st.text_area("News Input for Verification:", height=100)
    
    if st.button("🔍 Analyze & Verify"):
        if report_input:
            p_lang = "Hindi" if lang == "Hindi" else "English"
            res = model.generate_content(f"Act as a financial analyst. Analyze this news in {p_lang}: {report_input}")
            st.session_state.master_analysis = res.text
            st.session_state.l_code = 'hi' if lang == "Hindi" else 'en'
            st.markdown(f"<div class='news-card'>{res.text}</div>", unsafe_allow_html=True)

    if st.button("🔊 Play Voice Report"):
        if 'master_analysis' in st.session_state:
            tts = gTTS(text=st.session_state.master_analysis, lang=st.session_state.l_code)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            st.audio(fp, format='audio/mp3')

# --- TAB 3: AI FORECAST ---
with tab_predict:
    st.subheader("📈 7-Day AI Prediction Model")
    target = st.selectbox("Select Asset:", ["BTC-USD", "ETH-USD", "^NSEI"])
    if st.button("🚀 Calculate Forecast"):
        df = yf.download(target, period='60d').reset_index()
        df['Day_Num'] = np.arange(len(df))
        model_lr = LinearRegression().fit(df[['Day_Num']], df['Close'])
        future_idx = np.array([len(df) + i for i in range(7)]).reshape(-1, 1)
        preds = model_lr.predict(future_idx)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name="Market", line=dict(color="#00F5FF")))
        future_dates = [df['Date'].iloc[-1] + pd.Timedelta(days=i) for i in range(1, 8)]
        fig.add_trace(go.Scatter(x=future_dates, y=preds, name="AI Prediction", line=dict(dash='dash', color="#BC13FE")))
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

# --- TAB 4: PORTFOLIO ANALYTICS (Visual Pie Chart) ---
with tab_portfolio:
    st.subheader("💰 Portfolio Command & Pie Chart")
    
    col_p1, col_p2 = st.columns([1, 2])
    
    with col_p1:
        st.write("Enter your holdings:")
        val_btc = st.number_input("BTC Value ($)", value=1000)
        val_xrt = st.number_input("XRT Value ($)", value=500)
        val_lai = st.number_input("LAI Value ($)", value=300)
        
    with col_p2:
        # Pie Chart Algorithm
        data_pie = pd.DataFrame({
            "Asset": ["Bitcoin", "XRT", "LayerAI"],
            "Value": [val_btc, val_xrt, val_lai]
        })
        fig_pie = px.pie(data_pie, values='Value', names='Asset', 
                         title="Portfolio Diversification",
                         color_discrete_sequence=px.colors.sequential.RdBu)
        fig_pie.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pie, use_container_width=True)
        
    st.divider()
    # P/L Logic
    buy_p = st.number_input("Average Buy Price ($):", value=1.0)
    current_p = xrt['usd'] if xrt else 1.0
    roi = ((current_p - buy_p) / buy_p) * 100
    st.metric("XRT Performance", f"${current_p:.4f}", f"{roi:.2f}% ROI")

# Footer
st.markdown("---")
st.caption(f"© 2026 AiCoincast | Sovereign Command Center v14.0 | Mass Comm & Digital Excellence")
    
