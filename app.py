import streamlit as st
import yfinance as yf
import google.generativeai as genai
import pandas as pd
import requests
import streamlit.components.v1 as components

# ==========================================
# 1. EXPANDED THEME & BRANDING
# ==========================================
st.set_page_config(
    page_title="AiCoincast India | Admin Terminal", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# AI Engine Setup
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')

# Signature Midnight Purple Theme (Line-by-Line Expansion)
st.markdown("""
    <style>
    .main { 
        background-color: #1A1033; 
        color: #FFFFFF; 
    }
    .stMetric { 
        background-color: #241744; 
        border: 1px solid #BC13FE; 
        border-radius: 12px; 
        padding: 20px; 
        box-shadow: 0px 4px 10px rgba(188, 19, 254, 0.2);
    }
    .stTab { 
        background-color: #241744; 
        color: white; 
    }
    /* AI Card: Black Background */
    .ai-card-expanded { 
        background-color: #000000; 
        border-left: 6px solid #00F5FF; 
        padding: 25px; 
        border-radius: 12px; 
        margin-bottom: 20px; 
        color: white;
    }
    /* Human Card: Midnight Blue Background */
    .human-card-expanded { 
        background-color: #161B22; 
        border-left: 6px solid #00FF00; 
        padding: 25px; 
        border-radius: 12px; 
        margin-bottom: 20px; 
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. DATA ALGORITHMS (GLOBAL & CRYPTO)
# ==========================================
@st.cache_data(ttl=120)
def get_global_indices():
    indices_map = {
        "🇮🇳 NIFTY 50": "^NSEI", 
        "🇺🇸 NASDAQ": "^IXIC", 
        "🌍 S&P 500": "^GSPC"
    }
    output = {}
    for label, symbol in indices_map.items():
        try:
            ticker_obj = yf.Ticker(symbol)
            output[label] = ticker_obj.history(period="1d")['Close'].iloc[-1]
        except:
            output[label] = "Live"
    return output

@st.cache_data(ttl=120)
def fetch_crypto_top_30():
    try:
        endpoint = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 30,
            "page": 1
        }
        res = requests.get(endpoint, params=params)
        return res.json()
    except:
        return None

def check_partner_domain(email_id):
    # Security Layer for Reliance & AiCoincast
    valid_domains = ["aicoincast.in", "reliance.com", "reliancedigital.in"]
    extracted_domain = email_id.split('@')[-1] if "@" in email_id else ""
    return extracted_domain in valid_domains

# ==========================================
# 3. UI: TICKER & LOGO
# ==========================================
ticker_code = """
<div style="background-color: #241744; color: #00F5FF; padding: 12px; border-bottom: 2px solid #BC13FE; font-family: Arial;">
    <marquee scrollamount="7">
        🚀 AiCoincast India Terminal v5.4 | Double-Shield AI Verification Active | 30+ Global Assets Live | Midnight Purple Edition...
    </marquee>
</div>
"""
components.html(ticker_code, height=60)

with st.sidebar:
    st.title("👤 Partner Portal")
    st.image("https://via.placeholder.com/200x60.png?text=AiCoincast+India", use_column_width=True)
    partner_email = st.text_input("Enter Corporate Email", placeholder="user@aicoincast.in")
    is_verified = False
    
    if st.button("Secure Login"):
        if check_partner_domain(partner_email):
            st.success("Access Granted: Official Partner")
            is_verified = True
        else:
            st.error("Access Denied: Corporate Domain Required")
    
    st.divider()
    st.info("Identity: Samastipur to Global Vision Hub")

st.title("🛡️ AiCoincast India Terminal")
st.caption("National AI-Powered Financial Intelligence Hub | v5.4 Expanded Master")

# ==========================================
# 4. MARKET INDICES (NIFTY/NASDAQ)
# ==========================================
st.write("### 🌍 Global Share Market Indices")
indices_data = get_global_indices()
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🇮🇳 NIFTY 50", f"{indices_data['🇮🇳 NIFTY 50']:,.2f}" if isinstance(indices_data['🇮🇳 NIFTY 50'], float) else "Live")
with col2:
    st.metric("🇺🇸 NASDAQ", f"{indices_data['🇺🇸 NASDAQ']:,.2f}" if isinstance(indices_data['🇺🇸 NASDAQ'], float) else "Live")
with col3:
    st.metric("🌍 S&P 500", f"{indices_data['🌍 S&P 500']:,.2f}" if isinstance(indices_data['🌍 S&P 500'], float) else "Live")

st.divider()

# ==========================================
# 5. MASTER TABS SYSTEM
# ==========================================
tab_list = ["⚡ 30-Coin Tracker", "📊 Audit & Compare", "🏢 Corporate Audit", "✍️ AI News Desk"]
t1, t2, t3, t4 = st.tabs(tab_list)

# TAB 1: 30-COIN TRACKER
with t1:
    market_list = fetch_crypto_top_30()
    if market_list:
        heavy_movers = [c for c in market_list if abs(c['price_change_percentage_24h']) > 5.0]
        if heavy_movers:
            st.warning(f"🚨 PRICE ALERT: {len(heavy_movers)} assets moving >5% today!")
        
        st.write("### Live Top 30 National Tracker")
        grid_cols = st.columns(5)
        for i, coin in enumerate(market_list):
            grid_cols[i % 5].metric(
                coin['name'], 
                f"${coin['current_price']:,}", 
                f"{coin['price_change_percentage_24h']:.2f}%"
            )

# TAB 2: SIDE-BY-SIDE AUDIT
with t2:
    if market_list:
        st.write("### 🔍 Professional 5-Coin Comparison Engine")
        picks = st.multiselect("Select 5 Assets", [c['id'] for c in market_list], default=[c['id'] for c in market_list][:5])
        if len(picks) == 5:
            audit_data = [c for c in market_list if c['id'] in picks]
            audit_df = pd.DataFrame(audit_data)[['name', 'current_price', 'market_cap', 'price_change_percentage_24h']]
            st.table(audit_df)

# TAB 3: CORPORATE ASSET (XRT, LAI, QRL)
with t3:
    st.write("### 🏢 Project Deep-Dive")
    special_map = {"XRT": "robonomics-network", "LAI": "layerai", "QRL": "quantum-resistant-ledger"}
    target_coin = st.selectbox("Select Project", list(special_map.keys()))
    if st.button("Audit Project"):
        res_json = requests.get(f"https://api.coingecko.com/api/v3/coins/{special_map[target_coin]}").json()
        st.metric("Live Price", f"${res_json['market_data']['current_price']['usd']:.4f}")
        st.write(f"**Intel:** {res_json['description']['en'][:450]}...")

# TAB 4: DOUBLE-SHIELD NEWS BOT
with t4:
    st.subheader("🤖 AiCoincast Double-Shield News Desk")
    if is_verified:
        news_cat = st.selectbox("News Category", ["Cryptocurrency", "Crypto Coins", "Crypto Wallets", "AI", "Metaverse", "Blockchain"])
        news_head = st.text_input("Headline")
        news_lang = st.radio("Language Select", ["Hinglish", "Hindi", "English"], horizontal=True)
        news_auth = st.radio("Publisher Type", ["AI Bot (Black Card)", "Human/Official (Blue Card)"], horizontal=True)
        
        if st.button("Generate & Publish Official News"):
            # SHIELD 1: DRAFT
            with st.spinner("Shield 1: Generating Financial Draft..."):
                draft = model.generate_content(f"Financial news about {news_head} in {news_lang}. Category: {news_cat}.").text
            
            # SHIELD 2: VERIFICATION
            with st.spinner("Shield 2: Running Double-Shield Verification..."):
                verify_q = f"Check this for accuracy in {news_lang}: {draft}. Return 'Verified' if okay, or corrected version."
                v_res = model.generate_content(verify_q).text
                final_news = draft if "Verified" in v_res else v_res
            
            # OUTPUT CARDS
            box_style = "ai-card-expanded" if "AI" in news_auth else "human-card-expanded"
            badge_text = f"🤖 AI CRAWLER | {news_cat}" if "AI" in news_auth else f"👤 OFFICIAL SOURCE | {news_cat}"
            
            st.markdown(f"""
            <div class='{box_style}'>
                <span style='font-weight:bold; font-size:12px;'>{badge_text.upper()}</span>
                <h3 style='margin-top:10px;'>{news_head}</h3>
                <p>{final_news}</p>
                <small style='opacity:0.7;'>Verified by AI-Shield 3.0 | AiCoincast.in</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Access Denied: Sidebar se Official Email use karein.")

# ==========================================
# 6. FOOTER & COMPLIANCE
# ==========================================
st.divider()
st.caption("© 2026 AiCoincast.in | India's Digital Hub | v5.4 Unpacked Master")
