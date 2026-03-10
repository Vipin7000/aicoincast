import streamlit as st
import pandas as pd
import requests
import time

# --- [1. MASTER CONFIG & UI] ---
st.set_page_config(page_title="AiCoincast v155.0 Singularity", layout="wide")
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
    
    /* Neon Glow Scaling */
    .glow-pos { color: #00FF00 !important; text-shadow: 0 0 15px #00FF00; font-weight: bold; }
    .glow-neg { color: #FF0000 !important; text-shadow: 0 0 15px #FF0000; font-weight: bold; }
    
    /* Advanced Scroller */
    .scroller { white-space: nowrap; overflow: hidden; background: linear-gradient(90deg, #1A0B35, #0A041A); padding: 15px; border-bottom: 2px solid #00FF00; margin-bottom: 25px; }
    .scroller span { display: inline-block; padding-left: 60px; animation: scroll 35s linear infinite; font-weight: bold; font-family: 'Courier New', monospace; font-size: 18px; color: #00FF00; }
    @keyframes scroll { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    
    [data-testid="stDataFrame"] { border: 2px solid #00FF00 !important; border-radius: 15px; background-color: #0D0628 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- [CORE ALGORITHMS: SINGULARITY VERSION] ---
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

def get_whale_status(vol, mcap):
    v, m = safe_float(vol), safe_float(mcap)
    if m > 0 and (v / m) >= 0.15: return "🐋 WHALE ALERT"
    return "⚪ STABLE"

def get_poten(high, low):
    h, l = safe_float(high), safe_float(low)
    pot = ((h - l) / l) * 100 if l > 0 else 0
    return "🔥 HIGH SWING" if pot >= 10 else "💎 LOW VOL"

# [ID VAULT: THE 14 SOVEREIGN NODES]
MY_14_IDS = [
    "bitcoin", "ethereum", "polygon-ecosystem-token", "virtual-protocol",
    "qanplatform", "chaingpt", "velas", "griffain",
    "vaiot", "sin-city", "layerai", "robonomics-network",
    "everdome", "bloktopia"
]
INDICES = {"SENSEX": "^BSESN", "NIFTY 50": "^NSEI", "NIFTY NEXT 50": "^NSMIDCP50"}

@st.cache_data(ttl=180)
def fetch_singularity_data():
    sov_res, global_res, scroll_res, idx_res, total_mc = [], [], [], [], 1.0
    base_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&price_change_percentage=24h"
    
    try:
        # Step 1: Priority Fetch
        scroll_res = requests.get(f"{base_url}&order=market_cap_desc&per_page=25&page=1", timeout=12).json()
        sov_res = requests.get(f"{base_url}&ids={','.join(MY_14_IDS)}", timeout=12).json()
        
        # Step 2: Recursive Global Engine (3000 Coins)
        for p in range(1, 13):
            batch = requests.get(f"{base_url}&order=market_cap_desc&per_page=250&page={p}", timeout=10).json()
            if isinstance(batch, list) and len(batch) > 0:
                global_res.extend(batch)
            else: break
            time.sleep(0.4) # API Breathing Room
            
        gr = requests.get("https://api.coingecko.com/api/v3/global").json()
        total_mc = safe_float(gr['data']['total_market_cap'].get('inr', 1))
    except: pass

    if YF_READY:
        for name, ticker in INDICES.items():
            try:
                stock = yf.Ticker(ticker)
                h = stock.history(period="2d")
                if len(h) >= 2:
                    idx_res.append({"Name": name, "Price": h['Close'].iloc[-1], "Change": ((h['Close'].iloc[-1]-h['Close'].iloc[-2])/h['Close'].iloc[-2])*100})
            except: pass
            
    return sov_res, global_res, scroll_res, idx_res, total_mc

# --- [2. EXECUTION NODE] ---
f1_sov, g_node, scroll, f2_idx, g_mc = fetch_singularity_data()

with st.sidebar:
    st.title("🔐 OMNI VAULT v155")
    m_key = st.text_input("Master Key", type="password", placeholder="••••••••")
    if f1_sov: st.success(f"Verified Nodes: {len(f1_sov)}/14")
    if g_node: st.info(f"Global Pool: {len(g_node)} Assets")

if m_key == MASTER_KEY:
    # --- ROW 1: SCROLLER ---
    if scroll:
        s_html = "".join([f"<span>{c['symbol'].upper()}: {format_price(c['current_price'])} ({get_glow_ind(c['price_change_percentage_24h'])})</span>" for c in scroll])
        st.markdown(f'<div class="scroller">{s_html}</div>', unsafe_allow_html=True)

    # --- ROW 2: INDICES HUB ---
    st.markdown("### 📈 Market Alpha Indices")
    if f2_idx:
        cols = st.columns(len(f2_idx))
        for i, x in enumerate(f2_idx):
            cols[i].metric(label=x['Name'], value=f"{x['Price']:,.2f}", delta=f"{x['Change']:.2f}%")

    st.markdown("---")

    # --- ROW 3: SENTINEL ALPHA (14 NODES) ---
    st.header("🛰️ Sentinel Alpha: Sovereign Command")
    if f1_sov:
        df1 = []
        for c in f1_sov:
            raw_n = c.get('name', 'Syncing...')
            disp_n = raw_n.upper()
            if c.get('id') == "everdome": disp_n = "HUM(AI)N (AI)"
            
            df1.append({
                "Logo": c.get('image'), "Asset": disp_n,
                "Poten": get_poten(c.get('high_24h'), c.get('low_24h')),
                "Price": format_price(c.get('current_price')),
                "24H": get_glow_ind(c.get('price_change_percentage_24h_in_currency')),
                "Whale Alert": get_whale_status(c.get('total_volume'), c.get('market_cap'))
            })
        st.dataframe(pd.DataFrame(df1), column_config={"Logo": st.column_config.ImageColumn()}, use_container_width=True, hide_index=True)

    st.markdown("---")

    # --- ROW 4: GLOBAL MEGA NODE (3000 ASSETS) ---
    st.header(f"🌍 Global Mega Node (Pool Size: {len(g_node)})")
    q = st.text_input("🔍 Neural Search Index...", placeholder="Search symbols, names, or ranks...")
    if g_node:
        f_list = [c for c in g_node if q.lower() in c.get('name','').lower() or q.lower() in c.get('symbol','').lower()]
        dfg = []
        for c in f_list[:250]: # Optimized display buffer
            dfg.append({
                "Rank": c.get('market_cap_rank'), "Logo": c.get('image'), "Name": c.get('name', 'N/A'),
                "Authority": f"{(safe_float(c.get('market_cap'))/g_mc*100):.4f}%",
                "Price": format_price(c.get('current_price')),
                "24H": get_glow_ind(c.get('price_change_percentage_24h_in_currency')),
                "Status": get_whale_status(c.get('total_volume'), c.get('market_cap'))
            })
        st.dataframe(pd.DataFrame(dfg), column_config={"Logo": st.column_config.ImageColumn()}, use_container_width=True, hide_index=True)

else:
    st.info("Sovereign Master, enter Master Key to unlock Singularity.")
    
