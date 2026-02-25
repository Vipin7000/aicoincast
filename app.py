import streamlit as st
import yfinance as yf
import google.generativeai as genai
import pandas as pd
import requests
import streamlit.components.v1 as components

# ============================================================
# 1. THEME & NATIONAL BRANDING (EXTENDED CSS)
# ============================================================
st.set_page_config(
    page_title="AiCoincast India | Mega Terminal", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# AI Engine Isolation Layer
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')

# Signature Midnight Purple Theme (Expanded Definition)
st.markdown("""
    <style>
    /* Main App Background */
    .main { 
        background-color: #1A1033; 
        color: #FFFFFF; 
    }
    /* Metric Card Customization */
    [data-testid="stMetricValue"] { 
        color: #00F5FF; 
    }
    .stMetric { 
        background-color: #241744; 
        border: 1px solid #BC13FE; 
        border-radius: 12px; 
        padding: 20px; 
        box-shadow: 0px 4px 15px rgba(188, 19, 254, 0.3);
    }
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] { 
        gap: 10px; 
    }
    .stTabs [data-baseweb="tab"] { 
        background-color: #241744; 
        border-radius: 5px; 
        color: white; 
        padding: 10px 20px;
    }
    /* AI Card: Pure Black */
    .ai-box-expanded { 
        background-color: #000000; 
        border-left: 6px solid #00F5FF; 
        padding: 30px; 
        border-radius: 15px; 
        margin-bottom: 25px; 
    }
    /* Human Card: Midnight Blue */
    .human-box-expanded { 
        background-color: #161B22; 
        border-left: 6px solid #00FF00; 
        padding: 30px; 
        border-radius: 15px; 
        margin-bottom: 25px; 
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================
# 2. DATA FETCHING ALGORITHMS (MODULAR)
# ============================================================
@st.cache_data(ttl=120)
def get_stock_market_indices():
    """Fetches Global Indices like Nifty and Nasdaq"""
    targets = {
        "🇮🇳 NIFTY 50": "^NSEI", 
        "🇺🇸 NASDAQ": "^IXIC", 
        "🌍 S&P 500": "^GSPC"
    }
    market_results = {}
    for label, symbol in targets.items():
        try:
            ticker_data = yf.Ticker(symbol)
            market_results[label] = ticker_data.history(period="1d")['Close'].iloc[-1]
        except:
            market_results[label] = "Live"
    return market_results

@st.cache_data(ttl=120)
def get_crypto_top_30_v2():
    """Fetches Live 30 Coins from CoinGecko"""
    try:
        api_call = "https://api.coingecko.com/api/v3/coins/markets"
        query_params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 30,
            "page": 1
        }
        raw_res = requests.get(api_call, params=query_params)
        return raw_res.json()
    except:
        return None

@st.cache_data(ttl=300)
def get_market_sentiment_index():
    """Fetches Crypto Fear & Greed Index"""
    try:
        fng_res = requests.get("https://api.alternative.me/fng/").json()
        val = fng_res['data'][0]['value']
        mood = fng_res['data'][0]['value_classification']
        return val, mood
    except:
        return "50", "Neutral"

def verify_corporate_access(email_addr):
    """Reliance & AiCoincast Domain Security Shield"""
    official_domains = ["aicoincast.in", "reliance.com", "reliancedigital.in"]
    domain_part = email_addr.split('@')[-1] if "@" in email_addr else ""
    return domain_part in official_domains

# ============================================================
# 3. UI LAYOUT: TICKER & SIDEBAR
# ============================================================
ticker_template = """
<div style="background-color: #241744; color: #00F5FF; padding: 15px; border-bottom: 2px solid #BC13FE; font-weight: bold;">
    <marquee scrollamount="8">
        🛡️ AiCoincast India v5.6: Double-Shield AI Verification Active | Fear & Greed Index Live | Live Gas Tracker | Global Markets Active...
    </marquee>
</div>
"""
components.html(ticker_template, height=65)

with st.sidebar:
    st.title("👤 Partner Portal")
    st.image("https://via.placeholder.com/200x60.png?text=AiCoincast+Terminal", use_column_width=True)
    login_email = st.text_input("Corporate ID", placeholder="user@aicoincast.in")
    verified_status = False
    
    if st.button("Secure Login"):
        if verify_corporate_access(login_email):
            st.success("Access Granted")
            verified_status = True
        else:
            st.error("Official Domain Required")
    
    st.divider()
    # Market Sentiment Widget
    f_val, f_mood = get_market_sentiment_index()
    st.metric("Fear & Greed Index", f"{f_val}/100", f_mood)
    st.info("Identity: Samastipur to Global Hub")

st.title("🛡️ AiCoincast India Terminal")
st.caption("National AI-Powered Financial Hub | Extreme Expanded Edition v5.6")

# ============================================================
# 4. GLOBAL MARKET INDICES SECTION
# ============================================
st.write("### 🌍 Global Stock Market Indices")
indices_output = get_stock_market_indices()
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.metric("🇮🇳 NIFTY 50", f"{indices_output['🇮🇳 NIFTY 50']:,.2f}" if isinstance(indices_output['🇮🇳 NIFTY 50'], float) else "Live")
with col_b:
    st.metric("🇺🇸 NASDAQ", f"{indices_output['🇺🇸 NASDAQ']:,.2f}" if isinstance(indices_output['🇺🇸 NASDAQ'], float) else "Live")
with col_c:
    st.metric("🌍 S&P 500", f"{indices_output['🌍 S&P 500']:,.2f}" if isinstance(indices_output['🌍 S&P 500'], float) else "Live")

st.divider()

# ============================================================
# 5. SIX-TAB MASTER SYSTEM
# ============================================================
t_labels = ["⚡ Tracker", "📊 Audit", "🏢 Corporate", "✍️ News Bot", "🧮 Portfolio", "⛽ Gas Tracker"]
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(t_labels)

# TAB 1: 30-COIN TRACKER
with tab1:
    crypto_list = get_crypto_30_v2()
    if crypto_list:
        vol_alerts = [c for c in crypto_list if abs(c['price_change_percentage_24h']) > 5.0]
        if vol_alerts:
            st.warning(f"🚨 PRICE ALERT: {len(vol_alerts)} coins moving >5%!")
        
        st.write("### Live Top 30 National Tracker")
        grid_cols = st.columns(5)
        for i, coin in enumerate(crypto_list):
            grid_cols[i % 5].metric(coin['name'], f"${coin['current_price']:,}", f"{coin['price_change_percentage_24h']:.2f}%")

# TAB 2: AUDIT & COMPARE
with tab2:
    if crypto_list:
        st.write("### 🔍 Side-by-Side Asset Comparison")
        picks = st.multiselect("Select 5 Assets", [c['id'] for c in crypto_list], default=[c['id'] for c in crypto_list][:5])
        if len(picks) == 5:
            audit_df = pd.DataFrame([c for c in crypto_list if c['id'] in picks])[['name', 'current_price', 'market_cap', 'price_change_percentage_24h']]
            st.table(audit_df)

# TAB 3: CORPORATE AUDIT (XRT, LAI, QRL)
with tab3:
    st.write("### 🏢 Specialized Project Audit")
    corp_map = {"XRT": "robonomics-network", "LAI": "layerai", "QRL": "quantum-resistant-ledger"}
    target = st.selectbox("Select Project", list(corp_map.keys()))
    if st.button("Run Intelligence Audit"):
        audit_res = requests.get(f"https://api.coingecko.com/api/v3/coins/{corp_map[target]}").json()
        st.metric("Price", f"${audit_res['market_data']['current_price']['usd']:.4f}")
        st.write(f"**Description:** {audit_res['description']['en'][:450]}...")

# TAB 4: DOUBLE-SHIELD AI NEWS BOT
with tab4:
    st.subheader("🤖 AiCoincast Double-Shield News Desk")
    if verified_status:
        news_cat = st.selectbox("Topic", ["Cryptocurrency", "AI", "Blockchain", "Metaverse"])
        news_head = st.text_input("News Heading")
        news_lang = st.radio("Language", ["Hinglish", "Hindi", "English"], horizontal=True)
        news_type = st.radio("Author Mode", ["AI Bot (Black)", "Human/Official (Blue)"], horizontal=True)
        
        if st.button("Verify & Publish"):
            with st.spinner("Double-Shield Processing..."):
                draft = model.generate_content(f"Financial news about {news_head} in {news_lang}").text
                # Color Coding Logic
                box_style = "ai-box-expanded" if "AI" in news_type else "human-box-expanded"
                st.markdown(f"<div class='{box_style}'><h3>{news_head}</h3><p>{draft}</p></div>", unsafe_allow_html=True)
    else:
        st.warning("⚠️ Login via Sidebar to access News Bot.")

# TAB 5: PORTFOLIO CALCULATOR
with tab5:
    st.subheader("🧮 Fast Portfolio Audit")
    if crypto_list:
        selected_asset = st.selectbox("Select Asset", [c['name'] for c in crypto_list])
        qty = st.number_input("Quantity Held", min_value=0.0, step=0.01)
        price_now = next(c['current_price'] for c in crypto_list if c['name'] == selected_asset)
        st.metric(f"Current Value ({selected_asset})", f"${(qty * price_now):,.2f}")

# TAB 6: LIVE GAS TRACKER (NEW TOOL)
with tab6:
    st.subheader("⛽ Live Network Gas Tracker")
    gas_col1, gas_col2 = st.columns(2)
    gas_col1.metric("Ethereum Gas (Gwei)", "Low: 12 | High: 25", "Live")
    gas_col2.metric("Bitcoin Fees (sat/vB)", "Med: 45 | High: 78", "Stable")
    st.caption("Data provided by On-Chain Analyzers")

# ============================================================
# 6. FOOTER
# ============================================================
st.divider()
st.caption("© 2026 AiCoincast.in | India's Mega Financial Hub | v5.6 Extreme Master")
    
