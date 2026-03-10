import streamlit as st
import pandas as pd
import requests
import time

# --- [SAFE MODULE LOAD] ---
try:
    import yfinance as yf
    YF_READY = True
except ImportError:
    YF_READY = False

# --- [1. MASTER CONFIG & UI] ---
st.set_page_config(page_title="AiCoincast v149.0 Omnipotent", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

st.markdown("""
    <style>
    .stApp { background-color: #0A041A !important; }
    h1, h2, h3, h4, p, span, li { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] { background-color: #1A0B35 !important; border-right: 3px solid #00FF00 !important; }
    
    /* Neon Glow Styling */
    .glow-pos { color: #00FF00 !important; text-shadow: 0 0 10px #00FF00; font-weight: bold; }
    .glow-neg { color: #FF0000 !important; text-shadow: 0 0 10px #FF0000; font-weight: bold; }
    
    [data-testid="stDataFrame"] { border: 2px solid #00FF00 !important; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- [ALGO SUITE: v149 ABSOLUTE LOCK] ---
def safe_float(val):
    try: return float(val) if val is not None else 0.0
    except: return 0.0

def format_price(val, symbol="₹"):
    return f"{symbol}{safe_float(val):,.4f}"

def get_glow_ind(val):
    v = safe_float(val)
    if v > 0: return f"🟢 ▲ {abs(v):.1f}%"
    elif v < 0: return f"🔴 ▼ {abs(v):.1f}%"
    return f"▬ 0.0%"

def get_arbitrage_pot(high, low):
    pot = ((safe_float(high) - safe_float(low)) / safe_float(low)) * 100 if safe_float(low) > 0 else 0
    return "🔥 HIGH SWING" if pot >= 10 else "💎 STABLE"

# [ID VAULT]
MY_14_IDS = ["bitcoin", "ethereum", "polygon-ecosystem-token", "virtual-protocol", "qanplatform", "chaingpt", "velas", "griffain", "vaiot", "sin-city", "layerai", "robonomics-network", "unmarshal", "bloktopia"]
INDICES = {"SENSEX": "^BSESN", "NIFTY 50": "^NSEI"}

@st.cache_data(ttl=60)
def fetch_omnipotent_data():
    sov_res, global_res, total_mc, idx_res = [], [], 1.0, []
    base_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&price_change_percentage=24h,7d,30d"
    
    try:
        # Step 1: Crypto Fetch
        sov_res = requests.get(f"{base_url}&ids={','.join(MY_14_IDS)}&sparkline=true", timeout=20).json()
        global_res = requests.get(f"{base_url}&order=market_cap_desc&per_page=150&page=1", timeout=20).json()
        gr = requests.get("https://api.coingecko.com/api/v3/global", timeout=15).json()
        total_mc = safe_float(gr['data']['total_market_cap'].get('inr', 1))
    except: pass

    # Step 2: Market Indices Fetch
    if YF_READY:
        for name, ticker in INDICES.items():
            try:
                stock = yf.Ticker(ticker)
                h = stock.history(period="2d")
                if len(h) >= 2:
                    cp, pp = h['Close'].iloc[-1], h['Close'].iloc[-2]
                    idx_res.append({"Name": name, "Price": cp, "Change": ((cp-pp)/pp)*100})
            except: pass
    return sov_res, global_res, total_mc, idx_res

# --- [2. EXECUTION] ---
f1, g_node, g_mc, f2_idx = fetch_omnipotent_data()

with st.sidebar:
    st.title("🔐 OMNI VAULT")
    m_key = st.text_input("Master Key", type="password", placeholder="••••••••")
    if f1: st.success(f"Verified Nodes: {len(f1)}/14")
    if not YF_READY: st.warning("Run 'pip install yfinance' for Folder 2.")

if m_key == MASTER_KEY:
    tabs = st.tabs(["📊 SENTINEL ALPHA", "🌍 GLOBAL MEGA NODE", "📈 MARKET INDICES"])
    
    with tabs[0]:
        st.header("🛰️ Sentinel Command: 14 Sovereign Nodes")
        if f1:
            df1 = []
            for c in f1:
                name = "LAYERAI (LAI)" if c.get('id') == "layerai" else c.get('name', 'N/A').upper()
                df1.append({
                    "Logo": c.get('image'), "Asset": name,
                    "Poten": get_arbitrage_pot(c.get('high_24h'), c.get('low_24h')),
                    "Price (INR)": format_price(c.get('current_price')),
                    "24H": get_glow_ind(c.get('price_change_percentage_24h_in_currency')),
                    "WEEK": get_glow_ind(c.get('price_change_percentage_7d_in_currency')),
                    "Whale": "🐋" if (safe_float(c.get('total_volume'))/safe_float(c.get('market_cap')) >= 0.15) else "⚪"
                })
            st.dataframe(pd.DataFrame(df1), column_config={"Logo": st.column_config.ImageColumn()}, use_container_width=True, hide_index=True)

    with tabs[1]:
        st.header("🌍 Global Market Index (150 Assets)")
        q_search = st.text_input("🔍 Quick Search Global Node...")
        if g_node:
            filtered = [c for c in g_node if q_search.lower() in c.get('name','').lower()]
            dfg = []
            for c in filtered:
                dfg.append({
                    "Rank": c.get('market_cap_rank'), "Logo": c.get('image'), "Name": c.get('name'),
                    "Authority": f"{(safe_float(c.get('market_cap'))/g_mc*100):.2f}%",
                    "Price": format_price(c.get('current_price')),
                    "24H": get_glow_ind(c.get('price_change_percentage_24h_in_currency')),
                    "Whale": "🐋" if (safe_float(c.get('total_volume'))/safe_float(c.get('market_cap')) >= 0.15) else "⚪"
                })
            st.dataframe(pd.DataFrame(dfg), column_config={"Logo": st.column_config.ImageColumn()}, use_container_width=True, hide_index=True)

    with tabs[2]:
        st.header("📈 Indian Market Alpha Indices")
        if f2_idx:
            dfi = [{"Index": i['Name'], "Price": f"{i['Price']:,.2f}", "Change": get_glow_ind(i['Change'])} for i in f2_idx]
            st.dataframe(pd.DataFrame(dfi), use_container_width=True, hide_index=True)
        else:
            st.info("Market data syncing or library missing.")
else:
    st.info("Enter Master Key to Unlock.")
