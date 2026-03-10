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
st.set_page_config(page_title="AiCoincast v153.0 Monolith", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

st.markdown("""
    <style>
    .stApp { background-color: #0A041A !important; }
    h1, h2, h3, h4, p, span, li { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] { background-color: #1A0B35 !important; border-right: 3px solid #00FF00 !important; }
    .glow-pos { color: #00FF00 !important; text-shadow: 0 0 10px #00FF00; font-weight: bold; }
    .glow-neg { color: #FF0000 !important; text-shadow: 0 0 10px #FF0000; font-weight: bold; }
    .scroller { white-space: nowrap; overflow: hidden; background: #1A0B35; padding: 12px; border-bottom: 2px solid #00FF00; margin-bottom: 20px; }
    .scroller span { display: inline-block; padding-left: 50px; animation: scroll 30s linear infinite; font-weight: bold; font-family: monospace; font-size: 16px; }
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
    return f"{symbol}{v:,.4f}" if v < 1 else f"{symbol}{v:,.2f}"

def get_glow_ind(val):
    v = safe_float(val)
    if v > 0: return f"🟢 ▲ {abs(v):.1f}%"
    elif v < 0: return f"🔴 ▼ {abs(v):.1f}%"
    return f"▬ 0.0%"

# [ID VAULT]
MY_14_IDS = ["bitcoin", "ethereum", "polygon-ecosystem-token", "virtual-protocol", "qanplatform", "chaingpt", "velas", "griffain", "vaiot", "sin-city", "layerai", "robonomics-network", "everdome", "bloktopia"]
INDICES = {"SENSEX": "^BSESN", "NIFTY 50": "^NSEI"}

@st.cache_data(ttl=120)
def fetch_monolith_data():
    sov_res, global_res, scroll_res, idx_res, total_mc = [], [], [], [], 1.0
    base_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&price_change_percentage=24h"
    
    try:
        # 1. Top 20 Scroll
        scroll_res = requests.get(f"{base_url}&order=market_cap_desc&per_page=20&page=1").json()
        # 2. Sentinel Alpha (Forced 14)
        sov_res = requests.get(f"{base_url}&ids={','.join(MY_14_IDS)}").json()
        # 3. Global Node Loop (Up to 3000 Assets with Safety)
        for p in range(1, 13):
            batch = requests.get(f"{base_url}&order=market_cap_desc&per_page=250&page={p}").json()
            if isinstance(batch, list):
                global_res.extend(batch)
            else: break # Stop if rate limit hit
            time.sleep(0.3)
        # 4. Global Market Authority
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

# --- [2. EXECUTION] ---
f1_sov, g_node, scroll, f2_idx, g_mc = fetch_monolith_data()

with st.sidebar:
    st.title("🔐 OMNI VAULT")
    m_key = st.text_input("Master Key", type="password")
    if f1_sov: st.success(f"Sentinel: {len(f1_sov)}/14 Verified")
    if g_node: st.info(f"Global Index: {len(g_node)} Nodes")

if m_key == MASTER_KEY:
    # ROW 1: SCROLLER
    if scroll:
        s_html = "".join([f"<span>{c['symbol'].upper()}: {format_price(c['current_price'])} ({get_glow_ind(c['price_change_percentage_24h'])})</span>" for c in scroll])
        st.markdown(f'<div class="scroller">{s_html}</div>', unsafe_allow_html=True)

    # ROW 2: INDICES
    st.markdown("### 📈 Market Alpha Indices")
    if f2_idx:
        cols = st.columns(len(f2_idx))
        for i, x in enumerate(f2_idx):
            cols[i].metric(label=x['Name'], value=f"{x['Price']:,.2f}", delta=f"{x['Change']:.2f}%")

    st.markdown("---")

    # ROW 3: SENTINEL ALPHA
    st.header("🛰️ Sentinel Alpha (Sovereign 14)")
    if f1_sov:
        df1 = []
        for c in f1_sov:
            name = "HUM(AI)N (AI)" if c.get('id') == "everdome" else c.get('name', 'N/A').upper()
            df1.append({
                "Logo": c.get('image'), "Asset": name,
                "Price": format_price(c.get('current_price')),
                "24H Change": get_glow_ind(c.get('price_change_percentage_24h_in_currency')),
                "Whale": "🐋" if (safe_float(c.get('total_volume'))/safe_float(c.get('market_cap')) >= 0.15) else "⚪"
            })
        st.dataframe(pd.DataFrame(df1), column_config={"Logo": st.column_config.ImageColumn()}, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ROW 4: GLOBAL MEGA NODE
    st.header(f"🌍 Global Mega Node ({len(g_node)} Assets)")
    q = st.text_input("🔍 Search 3000+ Assets...")
    if g_node:
        filtered = [c for c in g_node if q.lower() in c.get('name','').lower() or q.lower() in c.get('symbol','').lower()]
        dfg = []
        for c in filtered[:200]:
            dfg.append({
                "Rank": c.get('market_cap_rank'), "Logo": c.get('image'), "Name": c.get('name'),
                "Authority": f"{(safe_float(c.get('market_cap'))/g_mc*100):.4f}%",
                "Price": format_price(c.get('current_price')),
                "24H": get_glow_ind(c.get('price_change_percentage_24h_in_currency')),
                "Whale": "🐋" if (safe_float(c.get('total_volume'))/safe_float(c.get('market_cap')) >= 0.15) else "⚪"
            })
        st.dataframe(pd.DataFrame(dfg), column_config={"Logo": st.column_config.ImageColumn()}, use_container_width=True, hide_index=True)
else:
    st.info("Enter Master Key to Unlock.")
            else:
    st.info("Enter Master Key to Unlock Sovereign Monolith.")
    
