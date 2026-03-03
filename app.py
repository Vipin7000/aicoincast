import streamlit as st
import yfinance as yf
import google.generativeai as genai
import requests
import time
from datetime import datetime
import pytz

# --- 1. SETUP & THEME ---
st.set_page_config(page_title="AiCoincast v18.3 Ultimate", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
MASTER_PWD = "SAMASTIPUR@2026"

st.markdown("""<style>
    .main { background-color: #120024; color: #E0B0FF; }
    [data-testid="stSidebar"] { background-color: #080015 !important; border-right: 2px solid #BF40BF; }
    [data-testid="stMetricValue"] { color: #BF40BF !important; font-weight: bold !important; text-shadow: 0px 0px 8px #BF40BF; }
    .master-card { background: rgba(30, 0, 50, 0.9); border: 2px solid #BF40BF; padding: 20px; border-radius: 15px; margin-top: 10px; }
    div[data-testid="stVerticalBlock"] > div:empty { display: none !important; }
</style>""", unsafe_allow_html=True)

# --- 2. SECURITY ---
if "auth" not in st.session_state:
    st.markdown("<h2 style='text-align:center;color:#BF40BF;'>🛡️ Sovereign Vault</h2>", unsafe_allow_html=True)
    pwd_input = st.text_input("Master Key:", type="password")
    if st.button("Unlock"):
        if pwd_input == MASTER_PWD:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Wrong Key!")
    st.stop()

# --- 3. ROBUST ENGINES ---
def ask_ai(query):
    try:
        if "GEMINI_API_KEY" not in st.secrets: 
            return "Error: API Key missing in Streamlit Secrets!", None
        
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Enhanced Generation logic
        response = model.generate_content(f"Analyze in Hinglish for a crypto investor: {query}")
        
        if response and response.text:
            img_url = f"https://pollinations.ai/p/{query.replace(' ','_')}_purple_cyber?seed={time.time()}"
            return response.text, img_url
        else:
            return "AI Node Busy. Please try a different query.", None
            
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg:
            return "Error: Invalid API Key. Please check your Google AI Studio key.", None
        elif "429" in error_msg:
            return "Error: API Rate Limit reached. Wait 60 seconds.", None
        return f"Technical Error: {error_msg}", None

@st.cache_data(ttl=60)
def get_market():
    data = {"crypto": [], "nifty": "Offline"}
    try:
        # Nifty Price
        n = yf.Ticker("^NSEI").history(period="1d")['Close'].iloc[-1]
        data["nifty"] = f"₹{n:,.2f}"
        
        # Specific Crypto Prices for Portfolio
        ids = "xrt-token,layerai,the-quantum-resistant-ledger,bitcoin,ethereum"
        url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&ids={ids}&order=market_cap_desc"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data["crypto"] = r.json()
    except:
        pass
    return data

# --- 4. SIDEBAR & LIVE PULSE ---
pulse = get_market()
with st.sidebar:
    st.title("🛰️ Sentinel")
    st.metric("NIFTY 50", pulse["nifty"])
    st.divider()
    if pulse["crypto"]:
        # Sidebar top 3 (BTC, ETH, etc)
        for c in pulse["crypto"][:3]:
            st.metric(c['name'], f"₹{c['current_price']:,}", f"{c['price_change_percentage_24h']:.2f}%")
    
    if st.button("🔒 Logout"):
        del st.session_state.auth
        st.rerun()

# --- 5. UI HEADER ---
st.title("🤖 AiCoincast v18.3 Ultimate")
st.caption(f"Sovereign Node Active | {datetime.now(IST).strftime('%H:%M:%S IST')}")
st.markdown('<div style="background:#4B0082;color:white;padding:10px;text-align:center;font-weight:bold;border-radius:10px;">🚀 NIFTY LIVE | AI COMMANDER | PURPLE PROTOCOL</div>', unsafe_allow_html=True)

# --- 6. PORTFOLIO MANAGER ---
st.markdown("---")
with st.expander("🛠️ Manage Portfolio (XRT, LAI, QRL)"):
    col_a, col_b, col_c = st.columns(3)
    # Using session state to persist values
    x_q = col_a.number_input("XRT Qty", value=st.session_state.get('x_q', 0.0))
    x_b = col_a.number_input("XRT Buy Price (₹)", value=st.session_state.get('x_b', 0.0))
    
    l_q = col_b.number_input("LAI Qty", value=st.session_state.get('l_q', 0.0))
    l_b = col_b.number_input("LAI Buy Price (₹)", value=st.session_state.get('l_b', 0.0))
    
    q_q = col_c.number_input("QRL Qty", value=st.session_state.get('q_q', 0.0))
    q_b = col_c.number_input("QRL Buy Price (₹)", value=st.session_state.get('q_b', 0.0))
    
    if st.button("Save & Sync Portfolio"):
        st.session_state.update({'x_q': x_q, 'x_b': x_b, 'l_q': l_q, 'l_b': l_b, 'q_q': q_q, 'q_b': q_b})
        st.success("Portfolio Synced Successfully!")
        st.rerun()

# Live Portfolio Display
st.subheader("💰 Live Sovereign Portfolio")
p_cols = st.columns(3)
map_hold = {
    "xrt-token": ('x_q', 'x_b', 0), 
    "layerai": ('l_q', 'l_b', 1), 
    "the-quantum-resistant-ledger": ('q_q', 'q_b', 2)
}

if pulse["crypto"]:
    for c in pulse["crypto"]:
        if c['id'] in map_hold:
            q_key, b_key, idx = map_hold[c['id']]
            qty = st.session_state.get(q_key, 0.0)
            buy = st.session_state.get(b_key, 0.0)
            
            if qty > 0:
                current_val = qty * c['current_price']
                invested = qty * buy
                pl_val = current_val - invested
                pl_per = (pl_val / invested * 100) if invested > 0 else 0
                
                with p_cols[idx]:
                    st.metric(c['name'], f"₹{current_val:,.0f}", f"{pl_per:.2f}% (₹{pl_val:,.0f})")
else:
    st.info("Market data syncing... Portfolio will appear shortly.")

# --- 7. INTELLIGENCE HUB (Search & Direct News) ---
st.markdown("---")
st.subheader("🔍 AI Intelligence Hub")

# Quick Access Button
if st.button("📰 Get Latest XRT News"):
    st.session_state.query_val = "Latest breaking news and price trends for XRT (Akash Network) in India today. Explain in Hinglish."
else:
    if 'query_val' not in st.session_state:
        st.session_state.query_val = "XRT and LayerAI India News"

query = st.text_input("🔍 Intelligence Search:", value=st.session_state.query_val)

if query:
    with st.spinner("Decoding Sovereign Data..."):
        report, visual = ask_ai(query)
        
        st.markdown("<div class='master-card'>", unsafe_allow_html=True)
        res_col1, res_col2 = st.columns([1, 1.8])
        
        with res_col1:
            if visual: 
                st.image(visual, use_container_width=True, caption="AI Analysis Visual")
        
        with res_col2:
            st.subheader(f"📝 Master Report: {query.upper()[:30]}...")
            st.info(report)
            
            # WhatsApp Share
            clean_rep = report.replace('\n', ' ')[:200]
            st.markdown(f'''
                <a href="https://wa.me/?text=AiCoincast Update: {clean_rep}..." target="_blank" 
                style="background:#25D366;color:white;padding:12px;border-radius:10px;text-decoration:none;display:inline-block;width:100%;text-align:center;font-weight:bold;margin-top:20px;">
                📲 Share Analysis on WhatsApp
                </a>''', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
