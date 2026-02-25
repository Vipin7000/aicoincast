import streamlit as st
import yfinance as yf
import google.generativeai as genai
import pandas as pd
import requests
import streamlit.components.v1 as components
import re

# ==========================================
# 1. SYSTEM SETTINGS & BHARAT BRANDING
# ==========================================
st.set_page_config(
    page_title="AiCoincast India | Pro Crypto Terminal",
    layout="wide",
    initial_sidebar_state="expanded"
)

# AI Setup with Security Shield
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')

# Cyber Metallic Midnight Theme (Custom CSS)
st.markdown("""
    <style>
    .main { background-color: #050A18; color: #FFFFFF; }
    .stMetric { 
        background-color: #0D1425; 
        border: 1px solid #00F5FF; 
        border-radius: 10px; 
        padding: 15px; 
        box-shadow: 0px 4px 10px rgba(0, 245, 255, 0.1);
    }
    .stTab { background-color: #0D1425; color: white; }
    div[data-testid="stExpander"] { border: 1px solid #BC13FE; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. CORE ALGORITHMS (DATA & SECURITY)
# ==========================================
@st.cache_data(ttl=120)
def get_coingecko_data(coin_id=""):
    try:
        if coin_id:
            url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
            return requests.get(url).json()
        else:
            url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=30&page=1"
            return requests.get(url).json()
    except Exception as e:
        return None

def is_company_email(email):
    public_domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]
    domain = email.split('@')[-1] if "@" in email else ""
    return (domain not in public_domains and domain != ""), domain

def news_card(title, content, source, author_type="AI"):
    bg = "#000000" if author_type == "AI" else "#062c12"
    border = "#00F5FF" if author_type == "AI" else "#00FF00"
    label = "🤖 AI CRAWLER" if author_type == "AI" else "👤 OFFICIAL SOURCE"
    st.markdown(f"""
        <div style='background-color:{bg}; color:white; padding:20px; border-radius:10px; border-left:5px solid {border}; margin-bottom:15px;'>
            <span style='color:{border}; font-weight:bold; font-size:11px;'>{label}</span>
            <h3 style='margin-top:5px;'>{title}</h3>
            <p style='font-size:14px;'>{content}</p>
            <small style='opacity:0.7;'>Source: {source}</small>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# 3. UI COMPONENTS: TICKER & SIDEBAR
# ==========================================
ticker_html = """
<div style="background-color: #0D1425; color: #00F5FF; padding: 10px; font-family: sans-serif; border-bottom: 2px solid #00F5FF;">
    <marquee scrollamount="6">
        🚀 🇮🇳 AiCoincast India: Live Terminal | 30-Coin Tracker Active | 🛡️ AI Price-Alert System Live | Secured by Reliance Digital Experience Logic | Global Market Intelligence v4.3 Live...
    </marquee>
</div>
"""
components.html(ticker_html, height=50)

with st.sidebar:
    st.title("🏢 Partner Portal")
    email = st.text_input("Enter Company Email", placeholder="user@aicoincast.in")
    if st.button("Verify & Login"):
        valid, dom = is_company_email(email)
        if valid:
            st.success(f"Security Verified: {dom}")
        else:
            st.error("Official Corporate Email Required")
    st.divider()
    st.info("Branding: National Crypto Hub")

st.title("🛡️ AiCoincast India")
st.caption("National AI-Powered Financial Terminal | Samastipur to Global Vision")

# ==========================================
# 4. TABBED INTERFACE (THE MAIN TOOLS)
# ==========================================
tab1, tab2, tab3 = st.tabs(["⚡ 30-Coin Tracker", "📊 Analysis & Comparison", "📰 Intelligence Hub"])

# TAB 1: LIVE TRACKER & ALERTS
with tab1:
    market_data = get_coingecko_data()
    if market_data:
        # Price Alert Logic
        alerts = [c for c in market_data if abs(c['price_change_percentage_24h']) > 5.0]
        if alerts:
            st.warning(f"🚨 ALERT: {len(alerts)} coins are showing High Volatility (>5%) in last 24h!")
        
        st.write("### ⚡ Live Top 30 National Tracker")
        cols = st.columns(5)
        for i, coin in enumerate(market_data):
            cols[i % 5].metric(
                coin['name'], 
                f"${coin['current_price']:,}", 
                f"{coin['price_change_percentage_24h']:.2f}%"
            )
    else:
        st.error("Connection Issue. Please refresh in 1 minute.")

# TAB 2: DEEP EXPLORER & 5-COIN TABLE
with tab2:
    if market_data:
        st.write("### 🔍 Select Exactly 5 Coins for Side-by-Side Comparison")
        selected = st.multiselect(
            "Audit/Compare Selection", 
            [c['id'] for c in market_data], 
            default=[c['id'] for c in market_data][:5]
        )
        
        if len(selected) == 5:
            comp_list = [c for c in market_data if c['id'] in selected]
            df = pd.DataFrame(comp_list)[['name', 'current_price', 'market_cap', 'price_change_percentage_24h']]
            df.columns = ['Name', 'Price (USD)', 'Market Cap', '24h Change (%)']
            st.table(df)
            
            if st.button("Generate AI Market Intelligence"):
                if "GEMINI_API_KEY" in st.secrets:
                    with st.spinner("AI is analyzing global sentiment..."):
                        prompt = f"Analyze market sentiment for these 5 coins in Hinglish: {', '.join(selected)}"
                        resp = model.generate_content(prompt)
                        st.info(resp.text)
        else:
            st.info("Pro Tip: 5 coins select karein detailed table dekhne ke liye.")

# TAB 3: LEGACY NEWS & CORPORATE AUDIT
with tab3:
    col_a, col_b = st.columns([2, 1])
    
    with col_a:
        st.subheader("📰 Verified Intelligence Feed")
        news_card("National Tech Surge", "Indian crypto adoption hits new highs in Q1 2026.", "Bloomberg India", "AI")
        news_card("Security Protocol Active", "AI-Shield 3.0 successfully protecting terminal assets.", "AiCoincast Ops", "Human")
        
    with col_b:
        st.subheader("🏢 Corporate Asset Audit")
        asset_dict = {
            "XRT": "robonomics-network", 
            "LAI": "layerai", 
            "QRL": "quantum-resistant-ledger"
        }
        choice = st.selectbox("Select Asset to Audit", list(asset_dict.keys()))
        
        if st.button("Fetch Deep Intel"):
            res = get_coingecko_data(asset_dict[choice])
            if res:
                st.metric("Live Price", f"${res['market_data']['current_price']['usd']:.4f}")
                st.metric("Global Ranking", f"#{res['market_cap_rank']}")
                st.write(f"**Asset Intel:** {res['description']['en'][:400]}...")
            else:
                st.warning("Fetching on-chain data... please wait.")

# ==========================================
# 5. FOOTER & COMPLIANCE
# ==========================================
st.divider()
st.caption("© 2026 AiCoincast.in | India's Premier Crypto Terminal | Secured by Gemini AI | Digital Excellence")
            
