import streamlit as st
import pandas as pd
import requests
import time

# --- [1. MASTER CONFIG & UI] ---
st.set_page_config(page_title="AiCoincast v161.0 Zenith", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

# --- [SAFE MODULE LOAD] ---
try:
    import yfinance as yf
    YF_READY = True
except ImportError:
    YF_READY = False

st.markdown("""
    <style>
    .stApp { background-color: #0A041A !important; }
    h1, h2, h3, h4, p, span, li { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] { background-color: #1A0B35 !important; border-right: 3px solid #00FF00 !important; }
    
    /* Neon Glow Styling */
    .glow-pos { color: #00FF00 !important; text-shadow: 0 0 10px #00FF00; font-weight: bold; }
    .glow-neg { color: #FF0000 !important; text-shadow: 0 0 10px #FF0000; font-weight: bold; }
    
    /* Unified Scroller */
    .scroller { white-space: nowrap; overflow: hidden; background: #1A0B35; padding: 12px; border-bottom: 2px solid #00FF00; margin-bottom: 20px; }
    .scroller span { display: inline-block; padding-left: 50px; animation: scroll 30s linear infinite; font-weight: bold; font-family: monospace; font-size: 16px; color: #00FF00; }
    @keyframes scroll { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    
    [data-testid="stDataFrame"] { border: 2px solid #00FF00 !important; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- [CORE ALGORITHMS] ---
def safe_float(val):
    try: return float(val) if val is not None else 0.0
    except: return 0.0

def format_price(val, symbol="₹"):
    v = safe_float(val)
    if v == 0: return "₹0.00"
    return f"{symbol}{v:,.4f}" if v < 1 else f"{symbol}{v:,.2f}"

def get_glow_ind(val):
    v = safe_float(val)
    if v > 0: return f"🟢 ▲ {abs(v):.1f}%"
    elif v < 0: return f"🔴 ▼ {abs(v):.1f}%"
    return f"▬ 0.0%"

# [ID VAULT - THE 14 SOVEREIGN NODES]
MY_14_IDS = [
    "bitcoin", "ethereum", "polygon-ecosystem-token", "virtual-protocol",
    "qanplatform", "chaingpt", "velas", "griffain",
    "vaiot", "sin-city", "layerai", "robonomics-network",
    "everdome", "bloktopia"
]
INDICES = {"SENSEX": "^BSESN", "NIFTY 50": "^NSEI"}

@st.cache_data(ttl=60)
def fetch_zenith_monolith_v161():
    sov_res, g_res, scroll_res, idx_res = [], [], [], []
    # Explicitly asking for multiple timeframes
    base_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&price_change_percentage=24h,7d,30d"
    
    try:
        # 1. Scroller Data (Top 20)
        scroll_res = requests.get(f"{base_url}&order=market_cap_desc&per_page=20&page=1").json()
        
        # 2. Sentinel Alpha (Forced 14)
        sov_res = requests.get(f"{base_url}&ids={','.join(MY_14_IDS)}").json()
        
        # 3. Global Mega Node (Batch 1 - searchable pool)
        g_res = requests.get(f"{base_url}&order=market_cap_desc&per_page=250&page=1").json()
    except Exception as e:
        print(f"Data Fetch Error: {e}")

    if YF_READY:
        for name, ticker in INDICES.items():
            try:
                stock = yf.Ticker(ticker)
                h = stock.history(period="2d")
                if not h.empty and len(h) >= 2:
                    idx_res.append({"Name": name, "Price": h['Close'].iloc[-1], "Change": ((h['Close'].iloc[-1]-h['Close'].iloc[-2])/h['Close'].iloc[-2])*100})
            except: pass
    return sov_res, g_res, scroll_res, idx_res

# --- [2. EXECUTION NODE] ---
sov_data, g_node, scroll, f2_idx = fetch_zenith_monolith_v161()

with st.sidebar:
    st.title("🔐 OMNI VAULT v161")
    m_key = st.text_input("Master Key", type="password", placeholder="••••••••")
    if isinstance(sov_data, list):
        # Precise Node Verification
        st.success(f"Verified Nodes: {len(sov_data)}/14")
        if any(c.get('id') == 'everdome' for c in sov_data):
            st.info("HUM(AI)N Node: ACTIVE ✅")

if m_key == MASTER_KEY:
    # --- ROW 1: TOP 20 SCROLLER ---
    if scroll:
        s_html = "".join([f"<span>{c['symbol'].upper()}: {format_price(c['current_price'])} ({get_glow_ind(c.get('price_change_percentage_24h_in_currency', 0))})</span>" for c in scroll])
        st.markdown(f'<div class="scroller">{s_html}</div>', unsafe_allow_html=True)

    # --- ROW 2: MARKET INDICES LINE ---
    st.markdown("### 📈 Market Alpha Indices")
    if f2_idx:
        idx_cols = st.columns(len(f2_idx))
        for i, idx in enumerate(f2_idx):
            idx_cols[i].metric(label=idx['Name'], value=f"{idx['Price']:,.2f}", delta=f"{idx['Change']:.2f}%")
    
    st.markdown("---")

    # --- ROW 3: SENTINEL ALPHA (FIXED 14/14 + WEEK/MONTH) ---
    st.header("🛰️ Sentinel Alpha: Sovereign Command")
    if sov_data:
        df1 = []
        for c in sov_data:
            # Atomic Name Mapping for Rebrands
            raw_n = c.get('name', 'N/A')
            disp_n = raw_n.upper() if raw_n else "N/A"
            if c.get('id') == "everdome": disp_n = "HUM(AI)N (AI)"
            if c.get('id') == "sin-city": disp_n = "SINVERSE (SIN)"
            
            df1.append({
                "Logo": c.get('image'), "Asset": disp_n,
                "Price": format_price(c.get('current_price')),
                "24H": get_glow_ind(c.get('price_change_percentage_24h_in_currency')),
                "WEEK": get_glow_ind(c.get('price_change_percentage_7d_in_currency')),
                "MONTH": get_glow_ind(c.get('price_change_percentage_30d_in_currency'))
            })
        st.dataframe(pd.DataFrame(df1), column_config={"Logo": st.column_config.ImageColumn()}, use_container_width=True, hide_index=True)

    st.markdown("---")

    # --- ROW 4: GLOBAL MEGA NODE ---
    st.header("🌍 Global Mega Node (Unified Database)")
    q = st.text_input("🔍 Quick Neural Search...", placeholder="Search symbols or names globally...")
    if g_node:
        filtered = [c for c in g_node if q.lower() in c.get('name', '').lower() or q.lower() in c.get('symbol', '').lower()]
        dfg = []
        for c in filtered[:100]:
            dfg.append({
                "Rank": c.get('market_cap_rank'), "Logo": c.get('image'), "Name": c.get('name', 'N/A'),
                "Price": format_price(c.get('current_price')),
                "24H Change": get_glow_ind(c.get('price_change_percentage_24h_in_currency'))
            })
        st.dataframe(pd.DataFrame(dfg), column_config={"Logo": st.column_config.ImageColumn()}, use_container_width=True, hide_index=True)
else:
    st.info("Sovereign Master, enter Master Key to unlock the Monolith.")
    
