import streamlit as st
import yfinance as yf
import google.generativeai as genai
import requests
import time
from datetime import datetime
import pytz

# 1. SETUP & THEME
st.set_page_config(page_title="AiCoincast v18.3 Ultimate", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
MASTER_PWD = "SAMASTIPUR@2026"

st.markdown("""<style>
    .main { background-color: #120024; color: #E0B0FF; }
    [data-testid="stSidebar"] { background-color: #080015 !important; border-right: 2px solid #BF40BF; }
    [data-testid="stMetricValue"] { color: #BF40BF !important; font-weight: bold !important; text-shadow: 0px 0px 8px #BF40BF; }
    .master-card { background: rgba(30, 0, 50, 0.9); border: 2px solid #BF40BF; padding: 20px; border-radius: 15px; }
</style>""", unsafe_allow_html=True)

# 2. SECURITY
if "auth" not in st.session_state:
    st.markdown("<h2 style='text-align:center;color:#BF40BF;'>🛡️ Sovereign Vault</h2>", unsafe_allow_html=True)
    if st.text_input("Master Key:", type="password") == MASTER_PWD:
        if st.button("Unlock"):
            st.session_state.auth = True
            st.rerun()
    st.stop()

# 3. ENGINES
def ask_ai(query):
    try:
        if "GEMINI_API_KEY" not in st.secrets: return "Missing Key", None
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(f"Analyze in Hinglish: {query}")
        img = f"https://pollinations.ai/p/{query.replace(' ','_')}_cyber?seed={time.time()}"
        return res.text if res else "Node Busy", img
    except: return "Syncing Error", None

@st.cache_data(ttl=60)
def get_market():
    data = {"crypto": [], "nifty": "Offline"}
    try:
        n = yf.Ticker("^NSEI").history(period="1d")['Close'].iloc[-1]
        data["nifty"] = f"₹{n:,.2f}"
        r = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&ids=xrt-token,layerai,the-quantum-resistant-ledger,bitcoin,ethereum", timeout=5)
        if r.status_code == 200: data["crypto"] = r.json()
    except: pass
    return data

# 4. SIDEBAR & PULSE
pulse = get_market()
with st.sidebar:
    st.title("🛰️ Sentinel")
    st.metric("NIFTY 50", pulse["nifty"])
    st.divider()
    for c in pulse["crypto"][:3]:
        st.metric(c['name'], f"₹{c['current_price']:,}", f"{c['price_change_percentage_24h']:.2f}%")
    if st.button("🔒 Logout"):
        del st.session_state.auth
        st.rerun()

# 5. UI HEADER
st.title("🤖 AiCoincast v18.3 Ultimate")
st.markdown('<div style="background:#4B0082;color:white;padding:10px;text-align:center;font-weight:bold;border-radius:10px;">🚀 NIFTY LIVE | AI COMMANDER | PURPLE PROTOCOL</div>', unsafe_allow_html=True)

# 6. PORTFOLIO MANAGER
with st.expander("🛠️ Manage Portfolio (XRT, LAI, QRL)"):
    col_a, col_b, col_c = st.columns(3)
    x_q = col_a.number_input("XRT Qty", value=st.session_state.get('x_q', 0.0))
    x_b = col_a.number_input("XRT Buy", value=st.session_state.get('x_b', 0.0))
    l_q = col_b.number_input("LAI Qty", value=st.session_state.get('l_q', 0.0))
    l_b = col_b.number_input("LAI Buy", value=st.session_state.get('l_b', 0.0))
    q_q = col_c.number_input("QRL Qty", value=st.session_state.get('q_q', 0.0))
    q_b = col_c.number_input("QRL Buy", value=st.session_state.get('q_b', 0.0))
    if st.button("Save Portfolio"):
        st.session_state.update({'x_q':x_q,'x_b':x_b,'l_q':l_q,'l_b':l_b,'q_q':q_q,'q_b':q_b})
        st.success("Synced!")

# Portfolio Display
st.subheader("💰 Live Portfolio")
cols = st.columns(3)
map_hold = {"xrt-token": ('x_q','x_b',0), "layerai": ('l_q','l_b',1), "the-quantum-resistant-ledger": ('q_q','q_b',2)}
for c in pulse["crypto"]:
    if c['id'] in map_hold:
        q_key, b_key, idx = map_hold[c['id']]
        qty, buy = st.session_state.get(q_key, 0), st.session_state.get(b_key, 0)
        if qty > 0:
            val, inv = qty * c['current_price'], qty * buy
            pl = val - inv
            cols[idx].metric(c['name'], f"₹{val:,.0f}", f"{(pl/inv*100):.1f}%" if inv>0 else "0%")

# 7. SEARCH
st.divider()
query = st.text_input("🔍 Intelligence Search:", "XRT and LayerAI India News")
if query:
    with st.spinner("Decoding..."):
        rep, vis = ask_ai(query)
        st.markdown("<div class='master-card'>", unsafe_allow_html=True)
        c1, c2 = st.columns([1, 2])
        if vis: c1.image(vis, use_container_width=True)
        c2.subheader("📝 Master Report")
        c2.info(rep)
        st.markdown(f'<a href="https://wa.me/?text={rep[:200]}" style="background:#25D366;color:white;padding:10px;border-radius:10px;text-decoration:none;display:block;text-align:center;">📲 WhatsApp Share</a>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
