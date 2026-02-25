import streamlit as st
import yfinance as yf
import google.generativeai as genai
import pandas as pd
import requests
import streamlit.components.v1 as components

# ==========================================
# 1. SIGNATURE MIDNIGHT PURPLE BRANDING
# ==========================================
st.set_page_config(
    page_title="AiCoincast India | Pro Terminal",
    layout="wide",
    initial_sidebar_state="expanded"
)

# AI Engine Setup (Gemini Pro)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')

# Expanded CSS for Midnight Purple & News Colors
st.markdown("""
    <style>
    /* Full Page: Midnight Purple */
    .main { 
        background-color: #1A1033; 
        color: #FFFFFF; 
    }
    /* Metric Cards */
    .stMetric { 
        background-color: #241744; 
        border: 1px solid #BC13FE; 
        border-radius: 12px; 
        padding: 20px; 
    }
    /* Tabs Styling */
    .stTab { 
        background-color: #241744; 
        color: white; 
    }
    /* AI Bot News: Pure Black Background */
    .ai-news-card { 
        background-color: #000000; 
        border-left: 6px solid #00F5FF; 
        padding: 25px; 
        border-radius: 12px; 
        margin-bottom: 20px; 
    }
    /* Human News: Midnight Blue Background */
    .human-news-card { 
        background-color: #161B22; 
        border-left: 6px solid #00FF00; 
        padding: 25px; 
        border-radius: 12px; 
        margin-bottom: 20px; 
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. CORE DATA ALGORITHMS
# ==========================================
@st.cache_data(ttl=120)
def get_global_indices():
    indices = {
        "🇮🇳 NIFTY 50": "^NSEI", 
        "🇺🇸 NASDAQ": "^IXIC", 
        "🌍 S&P 500": "^GSPC"
    }
    results = {}
    for name, sym in indices.items():
        try:
            ticker = yf.Ticker(sym)
            results[name] = ticker.history(period="1d")['Close'].iloc[-1]
        except:
            results[name] = "Live"
    return results

@st.cache_data(ttl=120)
def get_crypto_30():
    try:
        api_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=30&page=1"
        response = requests.get(api_url)
        return response.json()
    except:
        return None

def is_authorized(email):
    # Corporate Domain Security Check
    allowed_list = ["aicoincast.in", "reliance.com", "reliancedigital.in"]
    user_domain = email.split('@')[-1] if "@" in email else ""
    return user_domain in allowed_list

# ==========================================
# 3. UI COMPONENTS (TICKER & SIDEBAR)
# ==========================================
ticker_code = """
<div style="background-color: #241744; color: #00F5FF; padding: 12px; border-bottom: 2px solid #BC13FE;">
    <marquee scrollamount="7">
        🚀 AiCoincast India: Global Indices & 30+ Crypto Assets Live | 🛡️ Official AI News Desk v5.2 | Midnight Purple Edition Active...
    </marquee>
</div>
"""
components.html(ticker_code, height=60)

with st.sidebar:
    st.title("👤 Partner Portal")
    st.caption("Secure Login for News Desk")
    auth_email = st.text_input("Enter Official Email", placeholder="user@aicoincast.in")
    is_admin = False
    if st.button("Login to Dashboard"):
        if is_authorized(auth_email):
            st.success("Access Granted")
            is_admin = True
        else:
            st.error("Corporate Domain Required")
    st.divider()
    st.info("Branding: Samastipur to Global Vision")

st.title("🛡️ AiCoincast India Terminal")
st.caption("National AI-Powered Finance Terminal | Secured by Gemini AI")

# ==========================================
# 4. GLOBAL INDICES SECTION
# ==========================================
st.write("### 🌍 Global Share Market Indices")
market_indices = get_global_indices()
index_cols = st.columns(3)
for i, (name, value) in enumerate(market_indices.items()):
    index_cols[i].metric(
        name, 
        f"{value:,.2f}" if isinstance(value, float) else value
    )

st.divider()

# ==========================================
# 5. THE MASTER TOOLS (4-TAB SYSTEM)
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "⚡ 30-Coin Tracker", 
    "📊 Audit & Compare", 
    "🏢 Corporate Assets", 
    "✍️ AI News Desk"
])

# TAB 1: LIVE 30-COIN TRACKER
with tab1:
    crypto_data = get_crypto_30()
    if crypto_data:
        # Volatility Alerts
        heavy_movers = [c for c in crypto_data if abs(c['price_change_percentage_24h']) > 5.0]
        if heavy_movers:
            st.warning(f"🚨 ALERT: {len(heavy_movers)} assets moving >5%!")
        
        st.write("### Live Top 30 National Tracker")
        c_cols = st.columns(5)
        for i, coin in enumerate(crypto_data):
            c_cols[i % 5].metric(
                coin['name'], 
                f"${coin['current_price']:,}", 
                f"{coin['price_change_percentage_24h']:.2f}%"
            )
    else:
        st.error("API Fetching... Please refresh in 60s.")

# TAB 2: 5-COIN COMPARISON ENGINE
with tab2:
    if crypto_data:
        st.write("### 🔍 Professional 5-Coin Audit Table")
        selected_ids = st.multiselect(
            "Select 5 Assets", 
            [c['id'] for c in crypto_data], 
            default=[c['id'] for c in crypto_data][:5]
        )
        if len(selected_ids) == 5:
            audit_list = [c for c in crypto_data if c['id'] in selected_ids]
            audit_df = pd.DataFrame(audit_list)[['name', 'current_price', 'market_cap', 'price_change_percentage_24h']]
            st.table(audit_df)
        else:
            st.info("Exactly 5 coins select karein.")

# TAB 3: CORPORATE ASSET AUDIT (XRT, LAI, QRL)
with tab3:
    st.write("### 🏢 Specialized Project Deep-Dive")
    projects = {
        "XRT": "robonomics-network", 
        "LAI": "layerai", 
        "QRL": "quantum-resistant-ledger"
    }
    target = st.selectbox("Select Project", list(projects.keys()))
    if st.button("Run On-Chain Audit"):
        res = requests.get(f"https://api.coingecko.com/api/v3/coins/{projects[target]}").json()
        st.metric("Price", f"${res['market_data']['current_price']['usd']:.4f}")
        st.write(f"**Description:** {res['description']['en'][:450]}...")

# TAB 4: MULTI-LANGUAGE NEWS & COLOR CODING
with tab4:
    st.subheader("🤖 AiCoincast AI News Bot")
    if is_admin:
        cat = st.selectbox("Category", ["Cryptocurrency", "Crypto Coins", "Crypto Wallets", "AI", "Metaverse", "Blockchain"])
        title = st.text_input("News Heading")
        lang = st.radio("Language", ["Hinglish", "Hindi", "English"], horizontal=True)
        author = st.radio("Publisher Type", ["AI Bot (Black Card)", "Human/Official (Blue Card)"], horizontal=True)
        
        if st.button("Publish News"):
            with st.spinner("AI Writing..."):
                gen_prompt = f"Write news about {title} in {lang}. Topic: {cat}. Reported by AiCoincast."
                draft = model.generate_content(gen_prompt).text
                
                # COLOR CODED LOGIC
                card_style = "ai-news-card" if "AI Bot" in author else "human-news-card"
                badge = f"🤖 AI CRAWLER | {cat}" if "AI Bot" in author else f"👤 OFFICIAL SOURCE | {cat}"
                
                st.markdown(f"""
                <div class='{card_style}'>
                    <span style='font-weight:bold; font-size:12px; color:white;'>{badge.upper()}</span>
                    <h3 style='color:white; margin-top:10px;'>{title}</h3>
                    <p style='color:white; line-height:1.6;'>{draft}</p>
                    <small style='color:white; opacity:0.6;'>Source: AiCoincast Terminal</small>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Access Denied: Sidebar se Login karein.")

# ==========================================
# 6. FOOTER
# ==========================================
st.divider()
st.caption("© 2026 AiCoincast.in | India's Digital Hub | v5.2 Master Code")
