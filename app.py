import streamlit as st
import pandas as pd
import requests
import yfinance as yf
import time

# --- [1. MASTER CONFIG & UI] ---
st.set_page_config(page_title="AiCoincast v147.0 Overlord", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

st.markdown("""
    <style>
    .stApp { background-color: #0A041A !important; }
    h1, h2, h3, h4, p, span, li { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] { background-color: #1A0B35 !important; border-right: 3px solid #00FF00 !important; }
    
    /* Neon Glow Scaling */
    .glow-pos { color: #00FF00 !important; text-shadow: 0 0 12px #00FF00; font-weight: bold; }
    .glow-neg { color: #FF0000 !important; text-shadow: 0 0 12px #FF0000; font-weight: bold; }
    
    [data-testid="stDataFrame"] { border: 2px solid #00FF00 !important; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- [CORE ALGORITHMS: v147] ---
def safe_float(val):
    try: return float(val) if val is not None else 0.0
    except: return 0.0

def format_price(val, symbol="₹"):
    return f"{symbol}{safe_float(val):,.2f}"

def get_glow_ind(val):
    v = safe_float(val)
    if v > 0: return f"🟢 ▲ {abs(v):.1f}%"
    elif v < 0: return f"🔴 ▼ {abs(v):.1f}%"
    return f"▬ 0.0%"

def get_arbitrage_pot(high, low):
    pot = ((safe_float(high) - safe_float(low)) / safe_float(low)) * 100 if safe_float(low) > 0 else 0
    return "🔥 HIGH SWING" if pot >= 10 else "💎 STABLE"

# [DATA VAULT]
MY_14_IDS = ["bitcoin", "ethereum", "polygon-ecosystem-token", "virtual-protocol", "qanplatform", "chaingpt", "velas", "griffain", "vaiot", "sin-city", "layerai", "robonomics-network", "unmarshal", "bloktopia"]

# Market Indices Tickers
MARKET_INDICES = {"SENSEX": "^BSESN", "NIFTY 50": "^NSEI"}

@st.cache_data(ttl=60)
def fetch_overlord_intelligence():
    # CRYPTO FETCH
    base_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&price_change_percentage=24h,7d,30d"
    sov_res, global_res, total_mc = [], [], 1.0
    
    try:
        sov_res = requests.get(f"{base_url}&ids={','.join(MY_14_IDS)}&sparkline=true", timeout=20).json()
        g_batch = requests.get(f"{base_url}&order=market_cap_desc&per_page=150&page=1", timeout=20).json()
        if isinstance(g_batch, list): global_res = g_batch
        gr = requests.get("https://api.coingecko.com/api/v3/global", timeout=10).json()
        total_mc = safe_float(gr['data']['total_market_cap'].get('inr', 1))
    except: pass

    # EQUITY INDICES FETCH
    index_data = []
    for name, ticker in MARKET_INDICES.items():
        try:
            m_stock = yf.Ticker(ticker)
            hist = m_stock.history(period="2d")
            if not hist.empty and len(hist) >= 2:
                curr = hist['Close'].iloc[-1]
                prev = hist['Close'].iloc[-2]
                chg = ((curr - prev) / prev) * 100
                index_data.append({"Name": name, "Price": curr, "Change": chg})
        except: pass
        
    return sov_res, global_res, total_mc, index_data

# --- [2. EXECUTION] ---
sov_data, g_market, global_mc, index_data = fetch_overlord_intelligence()

with st.sidebar:
    st.title("🔐 OMNI VAULT")
    m_key = st.text_input("Master Key", type="password", placeholder="••••••••")
    if sov_data: st.success(f"Verified Crypto: {len(sov_data)}/14")
    if index_data: st.success(f"Indices: {len(index_data)} Verified")

if m_key == MASTER_KEY:
    tabs = st.tabs(["📊 COMMAND 1: SENTINEL ALPHA", "📈 COMMAND 2: SENSEX & NIFTY"])

    # --- FOLDER 1: CRYPTO UNION ---
    with tabs[0]:
        st.header("🛰️ Sentinel Alpha (Sovereign Crypto Nodes)")
        if sov_data:
            df_s = []
            for c in sov_data:
                df_s.append({
                    "Logo": c.get('image'), "Asset": c.get('name', 'N/A').upper(),
                    "Poten": get_arbitrage_pot(c.get('high_24h'), c.get('low_24h')),
                    "Price (INR)": format_price(c.get('current_price')),
                    "24H": get_glow_ind(c.get('price_change_percentage_24h_in_currency')),
                    "Whale": "🐋" if (safe_float(c.get('total_volume'))/safe_float(c.get('market_cap')) >= 0.15) else "⚪"
                })
            st.dataframe(pd.DataFrame(df_s), column_config={"Logo": st.column_config.ImageColumn()}, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.header("🌍 Global Crypto Mega Node")
        if g_market:
            df_g = []
            for c in g_market:
                df_g.append({
                    "Rank": c.get('market_cap_rank'), "Logo": c.get('image'), "Name": c.get('name'),
                    "Authority": f"{(safe_float(c.get('market_cap'))/global_mc*100):.2f}%",
                    "Price": format_price(c.get('current_price')),
                    "24H": get_glow_ind(c.get('price_change_percentage_24h_in_currency')),
                    "Whale": "🐋" if (safe_float(c.get('total_volume'))/safe_float(c.get('market_cap')) >= 0.15) else "⚪"
                })
            st.dataframe(pd.DataFrame(df_g), column_config={"Logo": st.column_config.ImageColumn()}, use_container_width=True, hide_index=True)

    # --- FOLDER 2: EQUITY INDICES ---
    with tabs[1]:
        st.header("📈 Indian Market Alpha Indices")
        if index_data:
            df_i = []
            for idx in index_data:
                df_i.append({
                    "Market Index": idx['Name'],
                    "Current Level": f"{idx['Price']:,.2f}",
                    "24H Change": get_glow_ind(idx['Change']),
                    "Authority": "BSE/NSE India"
                })
            st.dataframe(pd.DataFrame(df_i), use_container_width=True, hide_index=True)
            st.info("Market data syncs via YFinance Protocol (NSE/BSE).")
else:
    st.info("Sovereign Master, please enter Master Key to unlock.")
                
