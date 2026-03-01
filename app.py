import streamlit as st
import yfinance as yf
import google.generativeai as genai
import requests
import time
from datetime import datetime
import pytz
import streamlit.components.v1 as components

# --- 1. SYSTEM CONFIG & THEME ---
st.set_page_config(page_title="AiCoincast v17.1 Master", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
MASTER_PASSWORD = "SAMASTIPUR@2026"

# Midnight Purple & Cyberpunk Styling (v13.0 - v17.0 Styles)
st.markdown("""
    <style>
    .main { background-color: #030008; color: #FFFFFF; }
    .stMetric { background-color: #10002B; padding: 15px; border-radius: 12px; border: 1px solid #BC13FE; }
    .whatsapp-btn { background-color: #25D366; color: white; border-radius: 10px; padding: 12px; text-align: center; font-weight: bold; text-decoration: none; display: inline-block; width: 100%; margin-top: 10px; }
    .news-box { background: rgba(16,0,43,0.95); border: 2px solid #BC13FE; padding: 25px; border-radius: 20px; box-shadow: 0px 0px 15px #BC13FE; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SECURITY GATEWAY (v16.3 Iron Vault) ---
if "password_correct" not in st.session_state:
    st.markdown("<h2 style='text-align: center; color: #BC13FE;'>🛡️ Sovereign Iron Vault</h2>", unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        pwd = st.text_input("Enter Master Key:", type="password")
        if st.button("Unlock Terminal"):
            if pwd == MASTER_PASSWORD:
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("🚫 Access Denied")
    st.stop() # v16.5 Fix

# --- 3. DATA HARVESTING ALGORITHMS (v8.1 - v17.0) ---

# Folder: Global Indices (yfinance)
def fetch_global_indices():
    indices = {"NIFTY 50": "^NSEI", "NASDAQ": "^IXIC", "S&P 500": "^GSPC"}
    results = {}
    for name, sym in indices.items():
        try:
            val = yf.Ticker(sym).history(period="1d")['Close'].iloc[-1]
            results[name] = f"{val:,.2f}"
        except: results[name] = "Syncing..."
    return results

# Folder: CEX/DEX Pulse (CoinGecko)
def fetch_crypto_pulse():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=5&page=1"
        return requests.get(url, timeout=5).json()
    except: return []

# Folder: AI News Writing (Gemini 1.5)
def ai_bot_report_v17(query):
    try:
        if "GEMINI_API_KEY" not in st.secrets:
            return "❌ API Key Missing in Secrets!", None
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash') # v17.1 Stable Model
        prompt = f"Act as a Crypto/Market Bot. Write a professional Hinglish report on '{query}'. Focus on Global & Indian impact."
        res = model.generate_content(prompt)
        img = f"https://pollinations.ai/p/{query.replace(' ','_')}_futuristic_finance?seed={time.time()}"
        return res.text, img
    except Exception as e:
        return f"⚠️ Node Recalibrating. Error: {str(e)}", "https://via.placeholder.com/600x300/10002B/00F5FF?text=AI+Recalibrating"

# --- 4. TERMINAL UI DISPLAY ---

# Scrolling Ticker (v12.0 Feature)
ticker_html = """<div style="background-color: #BC13FE; color: white; padding: 10px; font-weight: bold;"><marquee scrollamount="8">🌐 GLOBAL MARKET LIVE | RELIANCE DIGITAL NODE: ACTIVE | AI BOTS WRITING... | SAMASTIPUR MASTER NODE ONLINE</marquee></div>"""
components.html(ticker_html, height=50)

# Sidebar Monitor (v16.2 Sentinel)
with st.sidebar:
    st.title("🛰️ System Sentinel")
    st.success("Sovereign Node v17.1 Active")
    st.divider()
    
    st.subheader("📊 Global Market Indices")
    indices_data = fetch_global_indices()
    for n, v in indices_data.items():
        st.metric(n, v)
    
    st.divider()
    st.subheader("💰 Top Crypto Pulse")
    coins = fetch_crypto_pulse()
    for c in coins:
        change = c['price_change_percentage_24h']
        color = "#00FF00" if change > 0 else "#FF0000"
        st.markdown(f"**{c['symbol'].upper()}**: ${c['current_price']} (<span style='color:{color}'>{change:.2f}%</span>)", unsafe_allow_html=True)
    
    if st.button("🔒 Secure Logout"):
        del st.session_state["password_correct"]
        st.rerun()

# Main Search & Report (v17.0 Omniscient Search)
st.title("🤖 AiCoincast v17.1 Omniscient")
search_q = st.text_input("🔍 Search ANY Market Topic (e.g. Nifty 50, XRT News, Bitcoin Future):", "XRT and LayerAI India")

if search_q:
    with st.spinner("Decoding Satellite Data..."):
        report, visual = ai_bot_report_v17(search_q)
        
        st.markdown("<div class='news-box'>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1.3])
        
        with col1:
            if visual: st.image(visual, caption=f"AI Visual: {search_q}")
        
        with col2:
            st.subheader(f"📝 Master Report: {search_q.upper()}")
            st.info(report)
            
            # WhatsApp Share (v15.3 Feature)
            wa_text = f"AiCoincast Report: {report[:300]}..."
            st.markdown(f'<a href="https://wa.me/?text={wa_text}" target="_blank" class="whatsapp-btn">📲 Share Full Report on WhatsApp</a>', unsafe_allow_html=True)
            
            if st.button("🔄 Refresh Data Pulse"):
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()
st.caption("© 2026 AiCoincast India | v17.1 Master Integrated Node | Mass Comm & Digital Excellence")
