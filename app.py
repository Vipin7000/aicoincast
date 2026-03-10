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
st.set_page_config(page_title="AiCoincast v150.0 Monolith", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

st.markdown("""
    <style>
    .stApp { background-color: #0A041A !important; }
    h1, h2, h3, h4, p, span, li { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] { background-color: #1A0B35 !important; border-right: 3px solid #00FF00 !important; }
    
    /* Neon Glow Styling */
    .glow-pos { color: #00FF00 !important; text-shadow: 0 0 10px #00FF00; font-weight: bold; }
    .glow-neg { color: #FF0000 !important; text-shadow: 0 0 10px #FF0000; font-weight: bold; }
    
    /* Scroller Styling */
    .scroller { white-space: nowrap; overflow: hidden; background: #1A0B35; padding: 10px; border-bottom: 2px solid #00FF00; }
    .scroller span { display: inline-block; padding-left: 50px; animation: scroll 20s linear infinite; font-weight: bold; }
    @keyframes scroll { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    
    [data-testid="stDataFrame"] { border: 2px solid #00FF00 !important; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- [CORE UTILITIES] ---
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

# [ID VAULT]
MY_14_IDS = [
    "bitcoin", "ethereum", "polygon-ecosystem-token", "virtual-protocol",
    "qanplatform", "chaingpt", "velas", "griffain",
    "vaiot", "sin-city", "layerai", "robonomics-network",
    "everdome", "bloktopia"
]
INDICES = {"SENSEX": "^BSESN", "NIFTY 50": "^NSEI"}

@st.cache_data(ttl=60)
def fetch_monolith_intelligence():
    sov_res, global_res, scroll_res, idx_res = [], [], [], []
    base_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&price_change_percentage=24h"
    
    try:
        # 1. Scroll Data (Top 20)
        scroll_res = requests.get(f"{base_url}&order=market_cap_desc&per_page=20&page=1", timeout=15).json()
        # 2. Sentinel Alpha (14 Nodes)
        sov_res = requests.get(f"{base_url}&ids={','.join(MY_14_IDS)}&sparkline=false", timeout=15).json()
        # 3. Global Node (Top 100)
        global_res = requests.get(f"{base_url}&order=market_cap_desc&per_page=100&page=1", timeout=15).json()
    except: pass

    if YF_READY:
        for name, ticker in INDICES.items():
            try:
                stock = yf.Ticker(ticker)
                h = stock.history(period="2d")
                if len(h) >= 2:
                    cp, pp = h['Close'].iloc[-1], h['Close'].iloc[-2]
                    idx_res.append({"Name": name, "Price": cp, "Change": ((cp-pp)/pp)*100})
            except: pass
    return sov_res, global_res, scroll_res, idx_res

# --- [2. EXECUTION & LAYOUT] ---
sov_data, g_node, scroll_data, f2_idx = fetch_monolith_intelligence()

with st.sidebar:
    st.title("🔐 OMNI VAULT")
    m_key = st.text_input("Master Key", type="password", placeholder="••••••••")

if m_key == MASTER_KEY:
    # --- ROW 1: TOP 20 SCROLLING MARQUEE ---
    if scroll_data:
        scroll_html = "".join([f"<span>{c['symbol'].upper()}: {format_price(c['current_price'])} ({get_glow_ind(c['price_change_percentage_24h'])})</span>" for c in scroll_data])
        st.markdown(f'<div class="scroller">{scroll_html}</div>', unsafe_allow_html=True)

    # --- ROW 2: MARKET INDICES LINE ---
    st.markdown("### 📈 Market Indices")
    if f2_idx:
        cols = st.columns(len(f2_idx))
        for i, idx in enumerate(f2_idx):
            cols[i].metric(label=idx['Name'], value=f"{idx['Price']:,.2f}", delta=f"{idx['Change']:.2f}%")
    else:
        st.info("Indices data syncing...")

    st.markdown("---")

    # --- ROW 3: SENTINEL ALPHA (14 NODES) ---
    st.header("🛰️ Sentinel Alpha: Sovereign Nodes")
    if sov_data:
        df1 = []
        for c in sov_data:
            name = c.get('name', 'N/A').upper()
            if c.get('id') == "everdome": name = "HUM(AI)N (AI)"
            if c.get('id') == "layerai": name = "LAYERAI (LAI)"
            
            df1.append({
                "Logo": c.get('image'), "Asset": name,
                "Price (INR)": format_price(c.get('current_price')),
                "24H Change": get_glow_ind(c.get('price_change_percentage_24h_in_currency'))
            })
        st.dataframe(pd.DataFrame(df1), column_config={"Logo": st.column_config.ImageColumn()}, use_container_width=True, hide_index=True)

    st.markdown("---")

    # --- ROW 4: GLOBAL MEGA NODE (NO ALGORITHM) ---
    st.header("🌍 Global Mega Node (Top 100 Index)")
    if g_node:
        dfg = []
        for c in g_node:
            dfg.append({
                "Rank": c.get('market_cap_rank'),
                "Logo": c.get('image'),
                "Name": c.get('name'),
                "Symbol": c.get('symbol','').upper(),
                "Price": format_price(c.get('current_price')),
                "24H Change": get_glow_ind(c.get('price_change_percentage_24h_in_currency'))
            })
        st.dataframe(pd.DataFrame(dfg), column_config={"Logo": st.column_config.ImageColumn()}, use_container_width=True, hide_index=True)

else:
    st.info("Enter Master Key to Unlock Sovereign Monolith.")
    
