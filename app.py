import streamlit as st
import yfinance as yf
import google.generativeai as genai
import requests
import time
from datetime import datetime
import pytz
import streamlit.components.v1 as components

# --- 1. SETTINGS & THEME ---
st.set_page_config(page_title="AiCoincast Omniscient v17.0", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
MASTER_PASSWORD = "SAMASTIPUR@2026"

# Midnight Purple & Cyberpunk Theme
st.markdown("""
    <style>
    .main { background-color: #030008; color: #FFFFFF; }
    .stMetric { background-color: #10002B; padding: 15px; border-radius: 12px; border: 1px solid #BC13FE; }
    .whatsapp-btn { background-color: #25D366; color: white; border-radius: 10px; padding: 12px; text-align: center; font-weight: bold; text-decoration: none; display: inline-block; width: 100%; }
    .news-box { background: rgba(16,0,43,0.9); border: 2px solid #BC13FE; padding: 20px; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CORE ALGORITHMS ---

# Global Share Market Index Engine
def get_market_indices():
    indices = {"NIFTY 50": "^NSEI", "NASDAQ": "^IXIC", "S&P 500": "^GSPC"}
    data = {}
    for name, sym in indices.items():
        try:
            val = yf.Ticker(sym).history(period="1d")['Close'].iloc[-1]
            data[name] = f"{val:,.2f}"
        except: data[name] = "Live"
    return data

# Centralized & Decentralized Crypto Data
def get_crypto_pulse():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=5&page=1"
        return requests.get(url, timeout=5).json()
    except: return []

# --- 3. LOGIN GUARD (Iron Vault + Partner Verification) ---
if "password_correct" not in st.session_state:
    st.markdown("<h2 style='text-align: center; color: #BC13FE;'>🛡️ Sovereign Iron Vault</h2>", unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        pwd = st.text_input("Enter Master Key:", type="password")
        if st.button("Unlock Terminal"):
            if pwd == MASTER_PASSWORD:
                st.session_state["password_correct"] = True
                st.rerun()
            else: st.error("Access Denied")
    st.stop()

# --- 4. TOP TICKER (Purane Code ka Feature) ---
ticker_html = f"""
<div style="background-color: #BC13FE; color: white; padding: 8px; font-family: sans-serif; font-weight: bold;">
    <marquee scrollamount="7">🌐 GLOBAL MARKET: Live | 🇮🇳 RELIANCE DIGITAL NODE: Active | 🛰️ AI BOTS: Writing Reports... | 🛡️ SECURED BY CLOUDFLARE</marquee>
</div>
"""
components.html(ticker_html, height=45)

# --- 5. SIDEBAR: GLOBAL INTELLIGENCE HUB ---
with st.sidebar:
    st.title("🛰️ System Sentinel")
    st.info(f"User: Admin (Samastipur)\nTime: {datetime.now(IST).strftime('%H:%M')}")
    
    st.subheader("📊 Global Indices")
    indices = get_market_indices()
    for name, val in indices.items():
        st.metric(name, val)
    
    st.divider()
    st.subheader("💰 Top Cryptos (CEX/DEX)")
    coins = get_crypto_pulse()
    for coin in coins:
        color = "#00FF00" if coin['price_change_percentage_24h'] > 0 else "#FF0000"
        st.markdown(f"**{coin['symbol'].upper()}**: ${coin['current_price']} (<span style='color:{color}'>{coin['price_change_percentage_24h']:.2f}%</span>)", unsafe_allow_html=True)
    
    if st.button("🔒 Secure Logout"):
        del st.session_state["password_correct"]
        st.rerun()

# --- 6. AI BOT WRITING ENGINE ---
def ai_bot_report(query):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        prompt = f"Act as a Crypto/Market Bot. Write a detailed Hinglish report on '{query}'. Include Global Market context, Indian impact, and XRT/LAI sentiment if relevant."
        res = model.generate_content(prompt)
        img = f"https://pollinations.ai/p/{query.replace(' ','_')}_futuristic_terminal?seed={time.time()}"
        return res.text, img
    except Exception as e:
        return f"Node Calibration Error: {e}", "https://via.placeholder.com/600x300?text=System+Syncing"

# --- 7. MAIN DASHBOARD ---
st.title("🤖 AiCoincast v17.0 Omniscient")
st.caption("All Crypto Data | Share Market Indexes | AI Writing Bots | Samastipur Master Node")

search_q = st.text_input("🔍 Search ANY Market Topic (e.g. Bitcoin Future, Nifty Today, Robonomics Update):", "XRT and LayerAI India")

if search_q:
    with st.spinner("AI Bot is analyzing Global Data..."):
        report, visual = ai_bot_report(search_q)
        
        st.markdown("<div class='news-box'>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1.3])
        with col1:
            st.image(visual, use_container_width=True)
        with col2:
            st.subheader(f"📝 Master Report: {search_q.upper()}")
            st.write(report)
            wa_text = f"AiCoincast Master Report on {search_q}: {report[:200]}..."
            st.markdown(f'<a href="https://wa.me/?text={wa_text}" target="_blank" class="whatsapp-btn">📲 Share Full Report on WhatsApp</a>', unsafe_allow_html=True)
            if st.button("🔄 Refresh Pulse"): st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()
st.caption("© 2026 AiCoincast | v17.0 Omniscient Edition | Integrated Intelligence Hub")
