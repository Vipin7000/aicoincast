import streamlit as st
import pandas as pd
import requests
import yfinance as yf # NEW: Stock Market Bridge

# --- [1. MASTER CONFIG & ULTRA-PREMIUM DESIGN] ---
st.set_page_config(page_title="AiCoincast v2.0 - Sovereign Edition", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

st.markdown("""
    <style>
    .stApp { background-color: #030008 !important; }
    h1, h2, h3, h4, p, span, div { color: #FFFFFF !important; font-family: 'Inter', sans-serif; }
    
    /* TURBO NEON TICKER */
    .ticker-wrap { width: 100%; overflow: hidden; background: rgba(0, 255, 0, 0.02); backdrop-filter: blur(25px); border-bottom: 2px solid #00FF00; padding: 10px 0; }
    .ticker { display: flex; white-space: nowrap; animation: ticker 15s linear infinite; }
    .glass-card { flex-shrink: 0; background: rgba(255, 255, 255, 0.05); padding: 5px 20px; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.1); margin: 0 10px; font-size: 0.85rem; }
    @keyframes ticker { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }
    
    /* RADAR COMMAND CENTER */
    .radar-container { display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; background: #0c051a; padding: 12px; border-radius: 12px; border: 1px solid #00FF00; margin: 15px 0; }
    .radar-item { text-align: center; border-right: 1px solid rgba(255,255,255,0.05); padding: 4px; font-size: 0.8rem; }
    .neon-up { color: #00FF00 !important; font-weight: bold; text-shadow: 0 0 8px #00FF00; }
    .neon-down { color: #FF0000 !important; font-weight: bold; text-shadow: 0 0 8px #FF0000; }
    
    /* PORTFOLIO VAULT DESIGN */
    .vault-box { background: linear-gradient(135deg, #1A0B35 0%, #030008 100%); padding: 20px; border-radius: 15px; border: 2px solid #00FF00; text-align: center; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- [CORE ENGINE FUNCTIONS] ---
def get_neon_ind(val):
    v = float(val) if val is not None else 0.0
    return f"<span class='neon-up'>▲ +{v:.1f}%</span>" if v > 0 else (f"<span class='neon-down'>▼ {v:.1f}%</span>" if v < 0 else "▬ 0.0%")

def fetch_api(url):
    try:
        r = requests.get(url, timeout=15); return r.json() if r.status_code == 200 else None
    except: return None

CORE_IDS = ["bitcoin", "ethereum", "polygon-ecosystem-token", "virtual-protocol", "qanplatform", "chaingpt", "velas", "griffain", "vaiot", "everdome", "bloktopia", "sin-city", "robonomics-network", "unmarshal", "layerai", "nftb"]

# --- [DEPLOYMENT & SIDEBAR VAULT] ---
with st.sidebar:
    st.title("🛡️ OMNI VAULT v2.0")
    m_key = st.text_input("Master Key", type="password")
    st.markdown("---")
    st.subheader("💰 Secret Portfolio")
    xrt_holdings = st.number_input("XRT Coins", value=206)
    xrt_buy_price = st.number_input("Buy Price (₹)", value=480)
    st.markdown("---")
    x_nodes = [st.text_input(f"Node #{i}") for i in range(17, 21)]

if m_key == MASTER_KEY:
    q = st.text_input("🔍 Neural Search Index", placeholder="Search 5000+ Assets...")
    base = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&price_change_percentage=24h,7d,30d,200d"
    top = fetch_api(f"{base}&order=market_cap_desc&per_page=250&page=1")
    sentinel = fetch_api(f"{base}&ids={','.join(CORE_IDS + [x for x in x_nodes if x])}")
    
    # 1. LIVE PORTFOLIO CALCULATION
    if sentinel:
        xrt_data = next((item for item in sentinel if item["id"] == "robonomics-network"), None)
        if xrt_data:
            curr_val = xrt_data['current_price'] * xrt_holdings
            profit = curr_val - (xrt_buy_price * xrt_holdings)
            st.markdown(f"""
            <div class="vault-box">
                <h4 style="margin:0;">MASTER PORTFOLIO (XRT)</h4>
                <h2 style="color:#00FF00; margin:5px 0;">₹{curr_val:,.2f}</h2>
                <p>Live Profit: <b class="neon-up">₹{profit:,.2f}</b></p>
            </div>
            """, unsafe_allow_html=True)

    # 2. TICKER
    if top:
        t_html = "".join([f'<div class="glass-card"><b>{c["symbol"].upper()}</b>: ₹{c["current_price"]:,.0f} {get_neon_ind(c.get("price_change_percentage_24h"))}</div>' for c in (top[:20]*2)])
        st.markdown(f'<div class="ticker-wrap"><div class="ticker">{t_html}</div></div>', unsafe_allow_html=True)

    # 3. GLOBAL RADAR COMMAND (10 Nations)
    st.markdown(f"""
    <div class="radar-container">
        <div class="radar-item">🇮🇳 SENSEX<br>{get_neon_ind(0.5)}</div>
        <div class="radar-item">🇮🇳 NIFTY 50<br>{get_neon_ind(0.7)}</div>
        <div class="radar-item">🇺🇸 S&P 500<br>{get_neon_ind(1.1)}</div>
        <div class="radar-item">🇺🇸 NASDAQ<br>{get_neon_ind(1.4)}</div>
        <div class="radar-item">🇯🇵 NIKKEI 225<br>{get_neon_ind(-0.3)}</div>
        <div class="radar-item">🇨🇳 SHANGHAI<br>{get_neon_ind(0.1)}</div>
        <div class="radar-item">🇬🇧 FTSE 100<br>{get_neon_ind(-0.2)}</div>
        <div class="radar-item">🇩🇪 DAX 40<br>{get_neon_ind(0.6)}</div>
        <div class="radar-item">🇫🇷 CAC 40<br>{get_neon_ind(0.4)}</div>
        <div class="radar-item">🇭🇰 HANG SENG<br>{get_neon_ind(-0.9)}</div>
    </div>
    """, unsafe_allow_html=True)

    # 4. TABLES (Sentinel & Global)
    def render_pro_table(data, title):
        st.header(title)
        if data:
            df = pd.DataFrame([{
                "Rank": c.get("market_cap_rank"), "Logo": c.get("image"), 
                "Asset": c.get("name").upper() if c.get("id") != "everdome" else "HUM(AI)N (AI)",
                "Price": f"₹{c.get('current_price',0):,.2f}",
                "24H": c.get('price_change_percentage_24h_in_currency'),
                "7D": c.get('price_change_percentage_7d_in_currency'),
                "30D": c.get('price_change_percentage_30d_in_currency'),
                "90D": c.get('price_change_percentage_200d_in_currency')
            } for c in data])
            st.write(df.to_html(escape=False, formatters={"Logo": lambda x: f'<img src="{x}" width="25">', "24H": get_neon_ind, "7D": get_neon_ind, "30D": get_neon_ind, "90D": get_neon_ind}, index=False), unsafe_allow_html=True)

    render_pro_table(sentinel, "🛰️ Sentinel Alpha Command")
    st.markdown("---")
    render_pro_table(top[:150], "🌍 Global Mega Node")

else:
    st.warning("🔒 Sovereign Master, authentication required to activate Phase 5.")
        
