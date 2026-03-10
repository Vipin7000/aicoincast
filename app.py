import streamlit as st
import pandas as pd
import requests
import time

# --- [1. MASTER CONFIG & UI] ---
st.set_page_config(page_title="AiCoincast v164.0 Unbreakable", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

try:
    import yfinance as yf
    YF_READY = True
except:
    YF_READY = False

st.markdown("""
    <style>
    .stApp { background-color: #0A041A !important; }
    h1, h2, h3, h4, p, span, li { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] { background-color: #1A0B35 !important; border-right: 3px solid #00FF00 !important; }
    .glow-pos { color: #00FF00 !important; text-shadow: 0 0 10px #00FF00; font-weight: bold; }
    .glow-neg { color: #FF0000 !important; text-shadow: 0 0 10px #FF0000; font-weight: bold; }
    
    /* NORMAL SPEED TICKER (15s) */
    .scroller { white-space: nowrap; overflow: hidden; background: #1A0B35; padding: 12px; border-bottom: 2px solid #00FF00; margin-bottom: 20px; }
    .scroller span { display: inline-block; padding-left: 60px; animation: scroll 15s linear infinite; font-weight: bold; font-family: monospace; font-size: 16px; color: #00FF00; }
    @keyframes scroll { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    
    [data-testid="stDataFrame"] { border: 2px solid #00FF00 !important; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- [CORE ALGORITHMS - NULL SAFE] ---
def safe_upper(val):
    if val is None: return "N/A"
    return str(val).upper()

def format_price(val, symbol="₹"):
    try:
        v = float(val) if val is not None else 0.0
        if v == 0: return "₹0.00"
        return f"{symbol}{v:,.6f}" if v < 0.1 else f"{symbol}{v:,.2f}"
    except: return "₹0.00"

def get_glow_ind(val):
    try:
        v = float(val) if val is not None else 0.0
        if v > 0: return f"🟢 ▲ {abs(v):.1f}%"
        elif v < 0: return f"🔴 ▼ {abs(v):.1f}%"
        return f"▬ 0.0%"
    except: return f"▬ 0.0%"

# [ID VAULT - THE 14 SOVEREIGN NODES]
MY_14_IDS = [
    "bitcoin", "ethereum", "polygon-ecosystem-token", "virtual-protocol",
    "qanplatform", "chaingpt", "velas", "griffain",
    "vaiot", "everdome", "sin-city", "layerai", "robonomics-network", "bloktopia"
]

@st.cache_data(ttl=60)
def fetch_unbreakable_intelligence():
    sov_res, g_res, scroll_res, idx_res = [], [], [], []
    base_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&price_change_percentage=24h,7d,30d"
    
    try:
        # 1. Scroller & Alpha Node (Priority)
        scroll_res = requests.get(f"{base_url}&order=market_cap_desc&per_page=25&page=1", timeout=10).json()
        sov_res = requests.get(f"{base_url}&ids={','.join(MY_14_IDS)}", timeout=10).json()
        
        # 2. Global Node - FIXED 250 for instant work & Searchability
        g_res = requests.get(f"{base_url}&order=market_cap_desc&per_page=250&page=1", timeout=10).json()
    except: pass

    if YF_READY:
        for name, ticker in {"SENSEX": "^BSESN", "NIFTY 50": "^NSEI"}.items():
            try:
                stock = yf.Ticker(ticker)
                h = stock.history(period="2d")
                if not h.empty and len(h) >= 2:
                    idx_res.append({"Name": name, "Price": h['Close'].iloc[-1], "Change": ((h['Close'].iloc[-1]-h['Close'].iloc[-2])/h['Close'].iloc[-2])*100})
            except: pass
    return sov_res, g_res, scroll_res, idx_res

# --- [2. EXECUTION] ---
sov_data, g_node, scroll, f2_idx = fetch_unbreakable_intelligence()

with st.sidebar:
    st.title("🔐 OMNI VAULT v164")
    m_key = st.text_input("Master Key", type="password", placeholder="••••••••")
    if isinstance(sov_data, list):
        st.success(f"Verified Nodes: {len(sov_data)}/14")

if m_key == MASTER_KEY:
    # ROW 1: SCROLLER (NORMAL SPEED)
    if isinstance(scroll, list):
        s_html = "".join([f"<span>{safe_upper(c.get('symbol'))}: {format_price(c.get('current_price'))} ({get_glow_ind(c.get('price_change_percentage_24h_in_currency'))})</span>" for c in scroll if c])
        st.markdown(f'<div class="scroller">{s_html}</div>', unsafe_allow_html=True)

    # ROW 2: INDICES
    st.markdown("### 📈 Market Alpha Indices")
    if f2_idx:
        cols = st.columns(len(f2_idx))
        for i, idx in enumerate(f2_idx):
            cols[i].metric(label=idx['Name'], value=f"{idx['Price']:,.2f}", delta=f"{idx['Change']:.2f}%")
    
    st.markdown("---")

    # ROW 3: SENTINEL ALPHA (FIXED & PROTECTED)
    st.header("🛰️ Sentinel Alpha: Sovereign Command")
    if isinstance(sov_data, list):
        df1 = []
        for c in sov_data:
            d_name = safe_upper(c.get('name'))
            if c.get('id') == "everdome": d_name = "HUM(AI)N (AI)"
            if c.get('id') == "polygon-ecosystem-token": d_name = "POL (EX-MATIC)"
            
            df1.append({
                "Logo": c.get('image'), "Asset": d_name,
                "Price": format_price(c.get('current_price')),
                "24H": get_glow_ind(c.get('price_change_percentage_24h_in_currency')),
                "WEEK": get_glow_ind(c.get('price_change_percentage_7d_in_currency')),
                "MONTH": get_glow_ind(c.get('price_change_percentage_30d_in_currency'))
            })
        st.dataframe(pd.DataFrame(df1), column_config={"Logo": st.column_config.ImageColumn()}, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ROW 4: GLOBAL MEGA NODE (RESTORED)
    st.header(f"🌍 Global Mega Node (Pool: {len(g_node) if g_node else 0})")
    q = st.text_input("🔍 Quick Neural Search...", placeholder="Enter asset name...")
    if isinstance(g_node, list):
        filtered = [c for c in g_node if q.lower() in str(c.get('name','')).lower()]
        dfg = []
        for c in filtered[:100]:
            dfg.append({
                "Rank": c.get('market_cap_rank'), "Logo": c.get('image'), "Name": c.get('name'),
                "Price": format_price(c.get('current_price')),
                "24H Change": get_glow_ind(c.get('price_change_percentage_24h_in_currency'))
            })
        st.dataframe(pd.DataFrame(dfg), column_config={"Logo": st.column_config.ImageColumn()}, use_container_width=True, hide_index=True)
else:
    st.info("Enter Master Key to unlock.")
                                                                                            
