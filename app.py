import streamlit as st
import yfinance as yf
import google.generativeai as genai
import requests
import time
from datetime import datetime
import pytz

# --- 1. SETUP & THEME (Blur & Visibility Fixed) ---
st.set_page_config(page_title="AiCoincast v18.4 Ultimate", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
MASTER_PWD = "SAMASTIPUR@2026"

# CSS: धुंधलेपन (Blur) को खत्म करने के लिए shadow हटाया गया है
st.markdown("""<style>
    .main { background-color: #120024; color: #E0B0FF; }
    [data-testid="stSidebar"] { background-color: #080015 !important; border-right: 2px solid #BF40BF; }
    /* No more blur: Clean, sharp and bold text */
    [data-testid="stMetricValue"] { 
        color: #BF40BF !important; 
        font-weight: 800 !important; 
        text-shadow: none !important; 
        font-size: 1.9rem !important;
    }
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

# --- 3. ULTIMATE AI ENGINE (Error 404 & Syncing Fixed) ---
def ask_ai(query):
    try:
        if "GEMINI_API_KEY" not in st.secrets: 
            return "Error: API Key missing in Secrets!", None
        
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        
        # मॉडल को स्पष्ट पैरामीटर्स के साथ कॉल करना ताकि 404 एरर न आए
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            generation_config={"temperature": 0.7, "top_p": 0.95, "max_output_tokens": 1024}
        )
        
        response = model.generate_content(f"Analyze in Hinglish for a crypto investor: {query}")
        
        if response and response.text:
            img_url = f"https://pollinations.ai/p/{query.replace(' ','_')}_purple_cyber?seed={time.time()}"
            return response.text, img_url
        else:
            return "AI Node Busy. Please try again.", None
            
    except Exception as e:
        # असली एरर मैसेज दिखाने के लिए ताकि डिबगिंग आसान हो
        return f"Node Error: {str(e)}", None

@st.cache_data(ttl=60)
def get_market():
    data = {"crypto": [], "nifty": "Offline"}
    try:
        # Nifty Price
        n = yf.Ticker("^NSEI").history(period="1d")['Close'].iloc[-1]
        data["nifty"] = f"₹{n:,.2f}"
        
        # Portfolio specific IDs
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
        # टॉप 3 मार्केट लीडर्स
        for c in pulse["crypto"][:3]:
            st.metric(c['name'], f"₹{c['current_price']:,}", f"{c['price_change_percentage_24h']:.2f}%")
    
    if st.button("🔒 Logout"):
        del st.session_state.auth
        st.rerun()

# --- 5. UI HEADER ---
st.title("🤖 AiCoincast v18.4 Final")
st.caption(f"Sovereign Node Active | {datetime.now(IST).strftime('%H:%M:%S IST')}")
st.markdown('<div style="background:#4B0082;color:white;padding:10px;text-align:center;font-weight:bold;border-radius:10px;">🚀 NIFTY LIVE | AI COMMANDER | PURPLE PROTOCOL</div>', unsafe_allow_html=True)

# --- 6. PORTFOLIO MANAGER ---
st.markdown("---")
with st.expander("🛠️ Manage Portfolio (XRT, LAI, QRL)"):
    col_a, col_b, col_c = st.columns(3)
    # Persisting values using session state
    x_q = col_a.number_input("XRT Qty", value=st.session_state.get('x_q', 176.0))
    x_b = col_a.number_input("XRT Buy", value=st.session_state.get('x_b', 15.0))
    
    l_q = col_b.number_input("LAI Qty", value=st.session_state.get('l_q', 100.0))
    l_b = col_b.number_input("LAI Buy", value=st.session_state.get('l_b', 0.01))
    
    q_q = col_c.number_input("QRL Qty", value=st.session_state.get('q_q', 100.0))
    q_b = col_c.number_input("QRL Buy", value=st.session_state.get('q_b', 0.20))
    
    if st.button("Save & Sync Portfolio"):
        st.session_state.update({'x_q': x_q, 'x_b': x_b, 'l_q': l_q, 'l_b': l_b, 'q_q': q_q, 'q_b': q_b})
        st.success("Synced!")
        st.rerun()

# Portfolio Display
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
                val = qty * c['current_price']
                pl = val - (qty * buy)
                p_cols[idx].metric(c['name'], f"₹{val:,.0f}", f"₹{pl:,.0f}")
else:
    st.info("Market data syncing... Portfolio updating.")

# --- 7. INTELLIGENCE HUB ---
st.markdown("---")
st.subheader("🔍 AI Intelligence Hub")

if st.button("📰 Get Latest XRT News"):
    st.session_state.query_val = "Latest news and price trends for XRT Akash Network India today"
else:
    if 'query_val' not in st.session_state: 
        st.session_state.query_val = "XRT and LayerAI India News"

query = st.text_input("🔍 Intelligence Search:", value=st.session_state.query_val)

if query:
    with st.spinner("Analyzing Sovereign Data..."):
        report, visual = ask_ai(query)
        st.markdown("<div class='master-card'>", unsafe_allow_html=True)
        res_col1, res_col2 = st.columns([1, 1.8])
        
        with res_col1:
            if visual: 
                st.image(visual, use_container_width=True, caption="AI Analysis Visual")
        
        with res_col2:
            st.subheader(f"📝 Master Report: {query.upper()[:20]}...")
            st.info(report)
            
            # WhatsApp Share
            st.markdown(f'''
                <a href="https://wa.me/?text=AiCoincast Update: {report[:200]}..." target="_blank" 
                style="background:#25D366;color:white;padding:12px;border-radius:10px;text-decoration:none;display:inline-block;width:100%;text-align:center;font-weight:bold;margin-top:20px;">
                📲 Share Analysis on WhatsApp
                </a>''', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
