import streamlit as st
import yfinance as yf
import google.generativeai as genai
import pandas as pd
import requests
import streamlit.components.v1 as components
import ccxt 
import time
from web3 import Web3

# ============================================================
# 1. SIGNATURE THEME & BRANDING ENGINE (EXPANDED)
# ============================================================
st.set_page_config(
    page_title="AiCoincast India | Heavyweight Master Terminal", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# AI Engine Isolation Layer (Gemini Pro)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    ai_engine = genai.GenerativeModel('gemini-pro')

# Signature Theme: Midnight Purple & Neon Architecture
st.markdown("""
    <style>
    /* Global Page Body: Midnight Purple Style */
    .main { 
        background-color: #1A1033; 
        color: #FFFFFF; 
        font-family: 'Segoe UI', Tahoma, sans-serif;
    }
    /* Metric Cards: Deep Purple with Neon Purple Glow */
    .stMetric { 
        background-color: #241744; 
        border: 2px solid #BC13FE; 
        border-radius: 15px; 
        padding: 25px; 
        box-shadow: 0px 8px 25px rgba(188, 19, 254, 0.4);
    }
    /* AI Card: Solid Black for Bot Personality */
    .ai-terminal-card { 
        background-color: #000000; 
        border-left: 10px solid #00F5FF; 
        padding: 35px; 
        border-radius: 20px; 
        margin-bottom: 35px; 
        border-top: 1px solid #00F5FF;
        border-right: 1px solid #00F5FF;
    }
    /* Human Card: Midnight Blue for Corporate Identity */
    .human-terminal-card { 
        background-color: #161B22; 
        border-left: 10px solid #00FF00; 
        padding: 35px; 
        border-radius: 20px; 
        margin-bottom: 35px; 
        border-top: 1px solid #00FF00;
        border-right: 1px solid #00FF00;
    }
    /* Web3 Blockchain Portal Styling */
    .web3-block-expanded { 
        background-color: #0D0221; 
        border: 2px solid #00F5FF; 
        padding: 35px; 
        border-radius: 18px;
        box-shadow: 0px 0px 20px rgba(0, 245, 255, 0.3);
    }
    /* Sidebar Customization */
    section[data-testid="stSidebar"] {
        background-color: #110822;
        border-right: 2px solid #BC13FE;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================
# 2. CORE DATA ALGORITHMS (MODULAR & DEEP)
# ============================================================

@st.cache_data(ttl=120)
def fetch_global_stock_indices():
    """Detailed Fetch for Nifty, Nasdaq and S&P 500"""
    index_map = {
        "🇮🇳 NIFTY 50": "^NSEI", 
        "🇺🇸 NASDAQ": "^IXIC", 
        "🌍 S&P 500": "^GSPC"
    }
    results = {}
    for label, sym in index_map.items():
        try:
            ticker_data = yf.Ticker(sym)
            results[label] = ticker_data.history(period="1d")['Close'].iloc[-1]
        except:
            results[label] = "Processing..."
    return results

@st.cache_data(ttl=120)
def fetch_top_30_national_tracker():
    """Crypto Tracker Data for Top 30 Assets"""
    try:
        base_url = "https://api.coingecko.com/api/v3/coins/markets"
        query_params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 30,
            "page": 1
        }
        api_response = requests.get(base_url, params=query_params)
        return api_response.json()
    except:
        return None

def scan_multi_exchange_arbitrage(symbol_pair='BTC/USDT'):
    """Analyzes Price Spreads across Top Global Exchanges"""
    exchange_list = ['binance', 'coinbase', 'kraken', 'okx', 'bybit', 'kucoin']
    master_arb_data = []
    for ex_id in exchange_list:
        try:
            ex_engine = getattr(ccxt, ex_id)()
            ticker_call = ex_engine.fetch_ticker(symbol_pair)
            master_arb_data.append({
                "Exchange": ex_id.upper(), 
                "Live Price": ticker_call['last'], 
                "24h Volume": ticker_call['quoteVolume'],
                "Timestamp": time.strftime('%H:%M:%S')
            })
        except:
            continue
    return pd.DataFrame(master_arb_data)

def audit_decentralized_wallet(hex_address):
    """Direct Blockchain Mainnet Audit Logic"""
    infura_gateway = "https://mainnet.infura.io/v3/YOUR_INFURA_KEY"
    w3_engine = Web3(Web3.HTTPProvider(infura_gateway))
    
    if not w3_engine.is_address(hex_address):
        return "Invalid ERC-20 Public Key"
    
    try:
        raw_wei = w3_engine.eth.get_balance(hex_address)
        ether_val = w3_engine.from_wei(raw_wei, 'ether')
        return f"{ether_val:.5f} ETH"
    except:
        return "Node Connection Failed (Check API)"

@st.cache_data(ttl=300)
def get_fear_greed_sentiment():
    """Fetches Live Market Psychology Index"""
    try:
        fng_api = requests.get("https://api.alternative.me/fng/").json()
        score = fng_api['data'][0]['value']
        status = fng_api['data'][0]['value_classification']
        return score, status
    except:
        return "50", "Neutral"

# ============================================================
# 3. UI ARCHITECTURE: TICKER & SIDEBAR SECURITY
# ============================================================
live_ticker_code = """
<div style="background-color: #241744; color: #00F5FF; padding: 18px; border-bottom: 4px solid #BC13FE; font-weight: bold; font-family: 'Arial Black';">
    <marquee scrollamount="9">
        🛡️ AiCoincast India v6.0 POWER TERMINAL | Double-Shield AI Verification Layer Active | Web3 Blockchain Mainnet Audit Tool Online | Arbitrage Spread Scanner Active...
    </marquee>
</div>
"""
components.html(live_ticker_code, height=75)

with st.sidebar:
    st.title("👤 Partner Portal")
    st.image("https://via.placeholder.com/220x80.png?text=AiCoincast+Terminal", use_column_width=True)
    st.divider()
    
    official_mail = st.text_input("Corporate Auth ID", placeholder="user@aicoincast.in")
    user_authenticated = False
    
    if st.button("Initialize Secure Access"):
        valid_domains = ["aicoincast.in", "reliance.com", "reliancedigital.in"]
        extracted_dom = official_mail.split('@')[-1] if "@" in official_mail else ""
        if extracted_dom in valid_domains:
            st.success("Identity Verified: Welcome Partner")
            user_authenticated = True
        else:
            st.error("Access Denied: Corporate Credential Required")
    
    st.divider()
    # Market Mood Widget
    f_score, f_status = get_fear_greed_sentiment()
    st.metric("Market Sentiment (Fear/Greed)", f"{f_score}/100", f_status)
    st.info("Identity: Samastipur to Global Hub | v6.0 Heavyweight")

st.title("🛡️ AiCoincast India Terminal")
st.caption("National AI-Powered Finance & Blockchain Intelligence Hub | Professional v6.0")

# ============================================================
# 4. GLOBAL MARKET INDICES (NIFTY / NASDAQ)
# ============================================================
st.write("### 🌍 Global Stock Market Indices Monitoring")
global_data = fetch_global_stock_indices()
n_col, q_col, s_col = st.columns(3)

with n_col:
    nifty_val = global_data['🇮🇳 NIFTY 50']
    st.metric("🇮🇳 NIFTY 50", f"{nifty_val:,.2f}" if isinstance(nifty_val, float) else nifty_val)

with q_col:
    nasdaq_val = global_data['🇺🇸 NASDAQ']
    st.metric("🇺🇸 NASDAQ", f"{nasdaq_val:,.2f}" if isinstance(nasdaq_val, float) else nasdaq_val)

with s_col:
    sp_val = global_data['🌍 S&P 500']
    st.metric("🌍 S&P 500", f"{sp_val:,.2f}" if isinstance(sp_val, float) else sp_val)

st.divider()

# ============================================================
# 5. MEGA TERMINAL ECOSYSTEM (8-TAB SYSTEM)
# ============================================================
tabs_mega = ["⚡ Tracker", "📊 Asset Audit", "🏢 Corporate", "✍️ AI News Bot", "🧮 Portfolio Calc", "⛽ Gas Tracker", "⚖️ Arbitrage Scanner", "🔗 Web3 Audit"]
t1, t2, t3, t4, t5, t6, t7, t8 = st.tabs(tabs_mega)

# TAB 1: 30-COIN NATIONAL TRACKER
with t1:
    m_30_data = fetch_top_30_national_tracker()
    if m_30_data:
        heavy_alerts = [c for c in m_30_data if abs(c['price_change_percentage_24h']) > 5.0]
        if heavy_alerts:
            st.warning(f"🚨 PRICE ALERT: {len(heavy_alerts)} assets moving with high volatility (>5%)!")
        
        st.write("### Live Top 30 National Crypto Tracker")
        track_grid = st.columns(5)
        for idx, coin_item in enumerate(m_30_data):
            track_grid[idx % 5].metric(
                coin_item['name'], 
                f"${coin_item['current_price']:,}", 
                f"{coin_item['price_change_percentage_24h']:.2f}%"
            )

# TAB 4: DOUBLE-SHIELD AI NEWS BOT (EXPANDED)
with t4:
    st.subheader("🤖 AiCoincast Double-Shield News Desk")
    if user_authenticated:
        n_cat = st.selectbox("Category Selection", ["Cryptocurrency", "Blockchain", "AI", "Metaverse", "Corporate Tech"])
        n_head = st.text_input("Enter Headline for Official Card")
        n_lang = st.radio("Language Output", ["Hinglish", "Hindi", "English"], horizontal=True)
        n_auth = st.radio("Publisher Personality", ["AI Bot (Black Card)", "Human/Official (Blue Card)"], horizontal=True)
        
        if st.button("Analyze & Publish Verified Report"):
            with st.spinner("Shield Stage 1: Drafting Financial Content..."):
                initial_draft = ai_engine.generate_content(f"Financial news report about {n_head} in {n_lang}.").text
            
            with st.spinner("Shield Stage 2: Running Intelligence Verification Layer..."):
                audit_prompt = f"Verify the tone and accuracy of this news: {initial_draft} in {n_lang}. Respond with 'Verified' if professional, else correct it."
                final_verified_report = ai_engine.generate_content(audit_prompt).text
                if "Verified" in final_verified_report:
                    final_verified_report = initial_draft
            
            # CSS Class Selection
            card_css_selector = "ai-terminal-card" if "AI" in n_auth else "human-terminal-card"
            badge_icon = f"🤖 AI CRAWLER | {n_cat}" if "AI" in n_auth else f"👤 OFFICIAL SOURCE | {n_cat}"
            
            st.markdown(f"""
            <div class='{card_css_selector}'>
                <span style='font-weight:bold; font-size:14px; color:white;'>{badge_icon.upper()}</span>
                <h2 style='color:white; margin-top:15px;'>{n_head}</h2>
                <hr style='border: 1px solid white; opacity: 0.2;'>
                <p style='color:white; font-size:17px; line-height:1.8;'>{final_verified_report}</p>
                <small style='color:white; opacity:0.6;'>Intelligence Authenticated by AiCoincast AI-Shield 4.0</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ AUTHENTICATION REQUIRED: Please login via Sidebar to access News Desk.")

# TAB 7: ARBITRAGE SCANNER (CCXT LOGIC)
with t7:
    st.subheader("⚖️ Multi-Exchange Arbitrage & Liquidity Scanner")
    st.caption("Live Price Audit across Global Hubs: Binance, Coinbase, Kraken, OKX, Bybit, Kucoin")
    u_pair = st.text_input("Trading Pair Input", value="BTC/USDT")
    
    if st.button("Execute Multi-Exchange Scan"):
        with st.spinner(f"Establishing API connections for {u_pair}..."):
            arb_dataframe = scan_multi_exchange_arbitrage(u_pair)
            if not arb_dataframe.empty:
                st.table(arb_dataframe)
                max_price = arb_dataframe['Live Price'].max()
                min_price = arb_dataframe['Live Price'].min()
                spread_val = max_price - min_price
                st.info(f"💡 Spread Detected: ${spread_val:.2f} across analyzed global exchanges.")

# TAB 8: WEB3 WALLET AUDIT (BLOCKCHAIN NODES)
with t8:
    st.subheader("🔗 Decentralized Wallet Balance Auditor")
    st.caption("Audit any Ethereum (ERC-20) wallet directly from the Blockchain Mainnet Nodes.")
    u_address = st.text_input("Enter Public Wallet Address (0x...)", placeholder="0x...")
    
    if st.button("Initialize Deep Blockchain Audit"):
        with st.spinner("Connecting to Ethereum Mainnet Node..."):
            wallet_intel = audit_decentralized_wallet(u_address)
            st.markdown(f"""
            <div class='web3-block-expanded'>
                <h4 style='color: #00F5FF;'>Mainnet Asset Summary</h4>
                <h1 style='color: white;'>{wallet_intel}</h1>
                <p style='color: #00F5FF; opacity: 0.8;'>Target Address: {u_address}</p>
            </div>
            """, unsafe_allow_html=True)

# ============================================================
# 6. FOOTER & COMPLIANCE (EXPANDED)
# ============================================================
st.divider()
st.caption("© 2026 AiCoincast.in | India's National Financial Intelligence Terminal | v6.0 Ultra-Expanded Master")
    
