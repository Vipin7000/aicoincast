import streamlit as st
import pandas as pd
import requests
import time

# --- [1. MASTER CONFIG & UI] ---
st.set_page_config(page_title="AiCoincast v178.0 Rebirth", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

try:
    import yfinance as yf
    YF_READY = True
except:
    YF_READY = False

# Neon Cyberpunk CSS
st.markdown("""
    <style>
    .stApp { background-color: #0A041A !important; }
    h1, h2, h3, h4, p, span, li { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] { background-color: #1A0B35 !important; border-right: 3px solid #00FF00 !important; }
    
    /* READABLE SCROLLER (15s) */
    .scroller { white-space: nowrap; overflow: hidden; background: #1A0B35; padding: 12px; border-bottom: 2px solid #00FF00; margin-bottom: 20px; }
    .scroller span { display: inline-block; padding-left: 60px; animation: scroll 15s linear infinite; font-weight: bold; font-family: monospace; font-size: 16px; color: #00FF00; }
    @keyframes scroll { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    
    [data-testid="stDataFrame"] { border: 2px solid #00FF00 !important; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- [FAIL-SAFE CORE UTILITIES] ---
def safe_get(data, key, default=None):
    return data.get(key, default) if isinstance(data, dict) else default

def format_p(val, sym="₹"):
    try:
        v = float(val) if val else 0.0
        return f"{sym}{v:,.6f}" if v < 0.1 else f"{sym}{v:,.2f}"
    except: return "₹0.00"

def get_glow(val):
    try:
        v = float(val) if val else 0.0
        if v > 0: return f"🟢 ▲ {abs(v):.1f}%"
        elif v < 0: return f"🔴 ▼ {abs(v):.1f}%"
        return "▬ 0.0%"
    except: return "▬ 0.0%"

# [ID VAULT - THE 16 SOVEREIGN NODES (NO VIRTUALS)]
MY_16_IDS = [
    "bitcoin", "ethereum", "polygon-ecosystem-token", "qanplatform", 
    "chaingpt", "velas", "griffain", "vaiot", 
    "everdome", "sin-city", "layerai", "robonomics-network", 
    "bloktopia", "nftb", "virtu", "unmarshal"
]

@st.cache_data(ttl=60)
def fetch_sovereign_intel():
    sov, glob, scroll, idx = [], [], [], []
    base = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&price_change_percentage=24h,7d,30d"
    
    try:
        # 1. Ticker (Top 20)
        s_raw = requests.get(f"{base}&order=market_cap_desc&per_page=20&page=1").json()
        if isinstance(s_raw, list): scroll = s_raw
        
        # 2. Sovereign 16 Nodes
        a_raw = requests.get(f"{base}&ids={','.join(MY_16_IDS)}").json()
        if isinstance(a_raw, list): sov = a_raw
        
        # 3. Global 1000 Engine (Staggered)
        for p in range(1, 5):
            batch = requests.get(f"{base}&order=market_cap_desc&per_page=250&page={p}").json()
            if isinstance(batch, list): glob.extend(batch)
            time.sleep(0.4)
    except: pass

    if YF_READY:
        for n, t in {"SENSEX": "^BSESN", "NIFTY 50": "^NSEI"}.items():
            try:
                h = yf.Ticker(t).history(period="2d")
                if not h.empty:
                    idx.append({"Name": n, "Price": h['Close'].iloc[-1], "Change": ((h['Close'].iloc[-1]-h['Close'].iloc[-2])/h['Close'].iloc[-2])*100})
            except: pass
    return sov, glob, scroll, idx

# --- [2. RENDER ENGINE] ---
sov_data, g_node, scroll_data, indices = fetch_sovereign_intel()

with st.sidebar:
    st.title("🛰️ OMNI VAULT v178")
    key = st.text_input("Master Key", type="password")
    if isinstance(sov_data, list):
        st.success(f"Nodes Active: {len(sov_data)}/16")

if key == MASTER_KEY:
    # TICKER
    if scroll_data:
        s_html = "".join([f"<span>{str(c.get('symbol')).upper()}: {format_p(c.get('current_price'))} ({get_glow(c.get('price_change_percentage_24h_in_currency'))})</span>" for c in scroll_data if isinstance(c, dict)])
        st.markdown(f'<div class="scroller">{s_html}</div>', unsafe_allow_html=True)

    # INDICES
    if indices:
        cols = st.columns(len(indices))
        for i, ix in enumerate(indices):
            cols[i].metric(label=ix['Name'], value=f"{ix['Price']:,.2f}", delta=f"{ix['Change']:.2f}%")
    
    st.markdown("---")

    # SENTINEL ALPHA (16 NODES)
    st.header("🛰️ Sentinel Alpha (16 Sovereign Nodes)")
    if sov_data:
        df1 = []
        for c in sov_data:
            c_id = safe_get(c, 'id')
            name = str(c.get('name')).upper()
            if c_id == "everdome": name = "HUM(AI)N (AI)"
            if c_id == "polygon-ecosystem-token": name = "POL (EX-MATIC)"
            
            df1.append({
                "Logo": c.get('image'), "Asset": name,
                "Price": format_p(c.get('current_price')),
                "24H": get_glow(c.get('price_change_percentage_24h_in_currency')),
                "WEEK": get_glow(c.get('price_change_percentage_7d_in_currency')),
                "MONTH": get_glow(c.get('price_change_percentage_30d_in_currency'))
            })
        st.dataframe(pd.DataFrame(df1), column_config={"Logo": st.column_config.ImageColumn()}, use_container_width=True, hide_index=True)

    st.markdown("---")

    # GLOBAL MEGA NODE (1000 ASSETS)
    st.header(f"🌍 Global Mega Node ({len(g_node)} Assets Searchable)")
    q = st.text_input("🔍 Neural Search Index...", placeholder="Search symbols globally...")
    if g_node:
        filt = [c for c in g_node if isinstance(c, dict) and (q.lower() in str(c.get('name')).lower() or q.lower() in str(c.get('symbol')).lower())]
        dfg = [{"Rank": c.get('market_cap_rank'), "Logo": c.get('image'), "Name": c.get('name'), "Price": format_p(c.get('current_price')), "24H Change": get_glow(c.get('price_change_percentage_24h_in_currency'))} for c in filt[:150]]
        st.dataframe(pd.DataFrame(dfg), column_config={"Logo": st.column_config.ImageColumn()}, use_container_width=True, hide_index=True)
else:
    st.info("Sovereign Master, enter Master Key.")
    
