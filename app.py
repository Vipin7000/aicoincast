import streamlit as st
import pandas as pd
import requests
import time

# --- [1. MASTER CONFIG & UI] ---
st.set_page_config(page_title="AiCoincast v177.0 Absolute", layout="wide")
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

# --- [FAIL-SAFE CORE UTILITIES] ---
def safe_get(data, key, default=None):
    if isinstance(data, dict): return data.get(key, default)
    return default

def safe_upper(val):
    return str(val).upper() if val is not None else "N/A"

def format_price(val, symbol="₹"):
    try:
        v = float(val) if val is not None else 0.0
        return f"{symbol}{v:,.6f}" if v < 0.1 else f"{symbol}{v:,.2f}"
    except: return "₹0.00"

def get_glow_ind(val):
    try:
        v = float(val) if val is not None else 0.0
        if v > 0: return f"🟢 ▲ {abs(v):.1f}%"
        elif v < 0: return f"🔴 ▼ {abs(v):.1f}%"
        return f"▬ 0.0%"
    except: return f"▬ 0.0%"

# [ID VAULT - 16 SOVEREIGN NODES]
MY_16_IDS = [
    "bitcoin", "ethereum", "polygon-ecosystem-token", "qanplatform", 
    "chaingpt", "velas", "griffain", "vaiot", 
    "everdome", "sin-city", "layerai", "robonomics-network", 
    "bloktopia", "nftb", "virtu", "unmarshal"
]

@st.cache_data(ttl=60)
def fetch_absolute_intelligence():
    sov_res, g_res, scroll_res, idx_res = [], [], [], []
    base_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&price_change_percentage=24h,7d,30d"
    
    try:
        # 1. Scroller Data (Top 20)
        s_raw = requests.get(f"{base_url}&order=market_cap_desc&per_page=20&page=1").json()
        if isinstance(s_raw, list): scroll_res = s_raw
        
        # 2. Sentinel Alpha (Strict 16 IDs)
        a_raw = requests.get(f"{base_url}&ids={','.join(MY_16_IDS)}").json()
        if isinstance(a_raw, list): sov_res = a_raw
        
        # 3. Global Mega Node (1000 Coins)
        for page in range(1, 5): 
            batch = requests.get(f"{base_url}&order=market_cap_desc&per_page=250&page={page}").json()
            if isinstance(batch, list): g_res.extend(batch)
            else: break
            time.sleep(0.3)
    except: pass

    if YF_READY:
        for name, ticker in {"SENSEX": "^BSESN", "NIFTY 50": "^NSEI"}.items():
            try:
                stock = yf.Ticker(ticker)
                h = stock.history(period="2d")
                if not h.empty:
                    idx_res.append({"Name": name, "Price": h['Close'].iloc[-1], "Change": ((h['Close'].iloc[-1]-h['Close'].iloc[-2])/h['Close'].iloc[-2])*100})
            except: pass
    return sov_res, g_res, scroll_res, idx_res

# --- [2. EXECUTION] ---
sov_data, g_node, scroll, f2_idx = fetch_absolute_intelligence()

if st.sidebar.text_input("Master Key", type="password") == MASTER_KEY:
    # ROW 1: SCROLLER
    if scroll:
        s_html = "".join([f"<span>{safe_upper(safe_get(c, 'symbol'))}: {format_price(safe_get(c, 'current_price'))} ({get_glow_ind(safe_get(c, 'price_change_percentage_24h_in_currency'))})</span>" for c in scroll if isinstance(c, dict)])
        st.markdown(f'<div class="scroller">{s_html}</div>', unsafe_allow_html=True)

    # ROW 2: INDICES
    if f2_idx:
        idx_cols = st.columns(len(f2_idx))
        for i, idx in enumerate(f2_idx):
            idx_cols[i].metric(label=idx['Name'], value=f"{idx['Price']:,.2f}", delta=f"{idx['Change']:.2f}%")
    
    st.markdown("---")

    # ROW 3: SENTINEL ALPHA (16 NODES FIXED)
    st.header("🛰️ Sentinel Alpha: Sovereign Command (16 Nodes)")
    if sov_data:
        df1 = []
        for c in sov_data:
            if not isinstance(c, dict): continue
            c_id = safe_get(c, 'id')
            d_name = safe_upper(safe_get(c, 'name'))
            if c_id == "everdome": d_name = "HUM(AI)N (AI)"
            if c_id == "polygon-ecosystem-token": d_name = "POL (EX-MATIC)"
            
            df1.append({
                "Logo": safe_get(c, 'image'), "Asset": d_name,
                "Price": format_price(safe_get(c, 'current_price')),
                "24H": get_glow_ind(safe_get(c, 'price_change_percentage_24h_in_currency')),
                "WEEK": get_glow_ind(safe_get(c, 'price_change_percentage_7d_in_currency')),
                "MONTH": get_glow_ind(safe_get(c, 'price_change_percentage_30d_in_currency'))
            })
        st.dataframe(pd.DataFrame(df1), column_config={"Logo": st.column_config.ImageColumn()}, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ROW 4: GLOBAL MEGA NODE (1000 ASSETS)
    st.header(f"🌍 Global Mega Node ({len(g_node)} Assets Searchable)")
    q = st.text_input("🔍 Search 1000+ Assets...")
    if g_node:
        f_list = [c for c in g_node if isinstance(c, dict) and (q.lower() in safe_upper(safe_get(c, 'name')).lower() or q.lower() in safe_upper(safe_get(c, 'symbol')).lower())]
        dfg = [{"Rank": safe_get(c, 'market_cap_rank'), "Logo": safe_get(c, 'image'), "Name": safe_get(c, 'name'), "Price": format_price(safe_get(c, 'current_price')), "24H": get_glow_ind(safe_get(c, 'price_change_percentage_24h_in_currency'))} for c in f_list[:150]]
        st.dataframe(pd.DataFrame(dfg), column_config={"Logo": st.column_config.ImageColumn()}, use_container_width=True, hide_index=True)
else:
    st.info("Enter Master Key to unlock.")
                             
