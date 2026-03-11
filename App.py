import streamlit as st
import pandas as pd
import requests
import time
import plotly.graph_objects as go

# --- [1. MASTER CONFIG & DESIGN ARCHITECTURE] ---
st.set_page_config(page_title="AiCoincast v2.0 Omnipotent", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

st.markdown("""
    <style>
    .stApp { background-color: #05010D !important; }
    h1, h2, h3, h4, p, span, div { color: #FFFFFF !important; font-family: 'Inter', sans-serif; }
    
    /* OPTION B: GLASSMORPHISM UI - THE VISUAL PULSE */
    .scroller-container { 
        background: rgba(255, 255, 255, 0.03); 
        backdrop-filter: blur(15px); 
        border-bottom: 2px solid #00FF00; 
        padding: 18px; 
        border-radius: 0 0 30px 30px; 
        position: relative;
        overflow: hidden;
    }
    .scroller { white-space: nowrap; display: flex; align-items: center; }
    .glass-card { 
        display: inline-block; 
        background: rgba(255, 255, 255, 0.07); 
        padding: 12px 28px; 
        border-radius: 16px; 
        border: 1px solid rgba(255, 255, 255, 0.12); 
        margin-right: 35px; 
        animation: scroll 15s linear infinite;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    @keyframes scroll { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    
    /* MASTER RADAR STRIP */
    .radar-strip { 
        background: linear-gradient(90deg, #1A0B35 0%, #05010D 100%); 
        padding: 14px; 
        border-radius: 12px; 
        display: flex; 
        justify-content: space-around; 
        margin: 20px 0; 
        border: 1px solid #00FF00; 
        box-shadow: 0 0 20px rgba(0,255,0,0.15);
    }
    .glow-up { color: #00FF00 !important; text-shadow: 0 0 12px #00FF00; font-weight: bold; }
    .glow-down { color: #FF0000 !important; text-shadow: 0 0 12px #FF0000; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- [THE BRAIN: CORE ALGORITHMS] ---
def fetch_api(url):
    try:
        r = requests.get(url, timeout=12)
        return r.json() if r.status_code == 200 else None
    except: return None

def get_ind(val):
    v = float(val) if val else 0.0
    if v > 0: return f"🟢 +{v:.1f}%"
    elif v < 0: return f"🔴 {v:.1f}%"
    return "▬ 0.0%"

@st.cache_data(ttl=300)
def get_analysis_chart(coin_id):
    # Phase 4: On-Demand Historical Intelligence
    data = fetch_api(f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=inr&days=90&interval=daily")
    if data and 'prices' in data:
        df = pd.DataFrame(data['prices'], columns=['time', 'price'])
        df['time'] = pd.to_datetime(df['time'], unit='ms')
        return df
    return None

# SOVEREIGN ID VAULT
CORE_IDS = ["bitcoin", "ethereum", "polygon-ecosystem-token", "qanplatform", "chaingpt", "velas", "griffain", "vaiot", "everdome", "sin-city", "layerai", "robonomics-network", "bloktopia", "nftb", "virtual-protocol", "unmarshal"]

@st.cache_data(ttl=60)
def fetch_omnipotent_monolith(extras, query):
    base = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&price_change_percentage=24h,7d,30d,200d"
    # Tier 1 & 2: Hot Load
    top_250 = fetch_api(f"{base}&order=market_cap_desc&per_page=250&page=1")
    s_ids = ",".join(CORE_IDS + [x for x in extras if x])
    sentinel = fetch_api(f"{base}&ids={s_ids}")
    # Tier 3: Neural Shadow Search
    search_data = []
    if query and len(query) >= 3:
        search_data = fetch_api(f"{base}&ids={query.lower().replace(' ', '-')}")
    return top_250, sentinel, search_data

# --- [INTERFACE DEPLOYMENT] ---
with st.sidebar:
    st.title("🛰️ OMNI VAULT v2.0")
    m_key = st.text_input("Enter Sovereign Key", type="password")
    st.markdown("---")
    st.subheader("⚙️ Expansion Slots")
    x_nodes = [st.text_input(f"Node #{i} (Coin ID)") for i in range(17, 21)]
    if st.button("Reset Session Cache"): st.cache_data.clear()

if m_key == MASTER_KEY:
    # 5000-COIN SHADOW INDEX INPUT
    search_q = st.text_input("🔍 Neural Search Index", placeholder="Search 5000+ Assets (e.g. 'solana')")
    top, sent, s_res = fetch_omnipotent_monolith(x_nodes, search_q)

    # UI: OPTION B TICKER
    if top:
        ticker_html = "".join([f'<div class="glass-card"><b>{c["symbol"].upper()}</b>: ₹{c["current_price"]:,.0f} <span class="{"glow-up" if c["price_change_percentage_24h"] > 0 else "glow-down"}">{get_ind(c["price_change_percentage_24h"])}</span></div>' for c in top[:20]])
        st.markdown(f'<div class="scroller-container"><div class="scroller">{ticker_html}</div></div>', unsafe_allow_html=True)

    # UI: THE MASTER RADAR STRIP
    st.markdown('<div class="radar-strip"><span>SENSEX: 74,119 <b class="glow-up">▲</b></span> <span>NIFTY: 22,490 <b class="glow-up">▲</b></span> <span>BTC: LIVE ⚡</span> <span>ETH: LIVE ⚡</span></div>', unsafe_allow_html=True)

    # UI: SENTINEL ALPHA COMMAND (16+4)
    st.header("🛰️ Sentinel Alpha Command")
    if sent:
        for c in sent:
            with st.container():
                col1, col2, col3, col4 = st.columns([1, 4, 3, 2])
                with col1: st.image(c['image'], width=45)
                with col2: 
                    name = c['name'].upper() if c['id'] != "everdome" else "HUM(AI)N (AI)"
                    st.subheader(f"{name} ({c['symbol'].upper()})")
                with col3: 
                    st.metric("Price", f"₹{c['current_price']:,.2f}", get_ind(c['price_change_percentage_24h_in_currency']))
                with col4:
                    if st.button("📈 Analysis", key=f"btn_{c['id']}"):
                        df_chart = get_analysis_chart(c['id'])
                        if df_chart is not None:
                            fig = go.Figure(data=[go.Scatter(x=df_chart['time'], y=df_chart['price'], line=dict(color='#00FF00', width=2))])
                            fig.update_layout(template="plotly_dark", height=300, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                            st.plotly_chart(fig, use_container_width=True)
                st.write(f"**Performance:** 7D: {get_ind(c.get('price_change_percentage_7d_in_currency'))} | 30D: {get_ind(c.get('price_change_percentage_30d_in_currency'))} | 200D Trend: {get_ind(c.get('price_change_percentage_200d_in_currency'))}")
                st.markdown("---")

    # UI: GLOBAL MEGA NODE
    st.header("🌍 Global Mega Node")
    pool = s_res if search_q and s_res else top[:150]
    if pool:
        g_df = pd.DataFrame([{
            "Rank": i.get("market_cap_rank"), "Logo": i.get("image"), "Name": i.get("name"),
            "Price": f"₹{i.get('current_price', 0):,.2f}", "24H": get_ind(i.get('price_change_percentage_24h_in_currency'))
        } for i in pool if isinstance(i, dict)])
        st.dataframe(g_df, column_config={"Logo": st.column_config.ImageColumn()}, use_container_width=True, hide_index=True)
else:
    st.info("Sovereign Master, authentication required to initialize the Monolith.")
      
