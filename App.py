import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go

# --- [1. MASTER CONFIG & DESIGN] ---
st.set_page_config(page_title="AiCoincast v2.0 Omnipotent", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

st.markdown("""
    <style>
    .stApp { background-color: #05010D !important; }
    h1, h2, h3, h4, p, span, div { color: #FFFFFF !important; font-family: 'Inter', sans-serif; }
    .scroller-container { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(15px); border-bottom: 2px solid #00FF00; padding: 18px; border-radius: 0 0 30px 30px; overflow: hidden; }
    .glass-card { display: inline-block; background: rgba(255, 255, 255, 0.07); padding: 12px 28px; border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.12); margin-right: 35px; animation: scroll 15s linear infinite; }
    @keyframes scroll { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .radar-strip { background: linear-gradient(90deg, #1A0B35 0%, #05010D 100%); padding: 14px; border-radius: 12px; display: flex; justify-content: space-around; margin: 20px 0; border: 1px solid #00FF00; }
    .glow-up { color: #00FF00 !important; text-shadow: 0 0 12px #00FF00; }
    .glow-down { color: #FF0000 !important; text-shadow: 0 0 12px #FF0000; }
    </style>
    """, unsafe_allow_html=True)

# --- [THE BRAIN: ERROR-FREE ALGORITHMS] ---
def fetch_api(url):
    try:
        r = requests.get(url, timeout=12)
        return r.json() if r.status_code == 200 else None
    except: return None

def get_ind(val):
    v = float(val) if val else 0.0
    return f"🟢 +{v:.1f}%" if v > 0 else (f"🔴 {v:.1f}%" if v < 0 else "▬ 0.0%")

@st.cache_data(ttl=300)
def get_analysis_chart(coin_id):
    data = fetch_api(f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=inr&days=90&interval=daily")
    if data and 'prices' in data:
        df = pd.DataFrame(data['prices'], columns=['time', 'price'])
        df['time'] = pd.to_datetime(df['time'], unit='ms')
        return df
    return None

CORE_IDS = ["bitcoin", "ethereum", "polygon-ecosystem-token", "qanplatform", "chaingpt", "velas", "griffain", "vaiot", "everdome", "sin-city", "layerai", "robonomics-network", "bloktopia", "nftb", "virtual-protocol", "unmarshal"]

@st.cache_data(ttl=60)
def fetch_omnipotent_monolith(extras, query):
    base = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&price_change_percentage=24h,7d,30d,200d"
    top_250 = fetch_api(f"{base}&order=market_cap_desc&per_page=250&page=1")
    s_ids = ",".join(CORE_IDS + [x for x in extras if x])
    sentinel = fetch_api(f"{base}&ids={s_ids}")
    search_data = fetch_api(f"{base}&ids={query.lower().replace(' ', '-')}") if (query and len(query) >= 3) else []
    return top_250, sentinel, search_data

# --- [INTERFACE DEPLOYMENT] ---
with st.sidebar:
    st.title("🛰️ OMNI VAULT v2.0")
    m_key = st.text_input("Sovereign Key", type="password")
    st.markdown("---")
    x_nodes = [st.text_input(f"Node #{i}") for i in range(17, 21)]

# ZERO-ERROR PROTECTION LOGIC
if m_key == MASTER_KEY:
    search_q = st.text_input("🔍 Neural Search Index", placeholder="Search 5000+ Assets...")
    top, sent, s_res = fetch_omnipotent_monolith(x_nodes, search_q)

    # UI: OPTION B TICKER
    if top:
        ticker_html = "".join([f'<div class="glass-card"><b>{c["symbol"].upper()}</b>: ₹{c["current_price"]:,.0f} <span class="{"glow-up" if c["price_change_percentage_24h"] > 0 else "glow-down"}">{get_ind(c["price_change_percentage_24h"])}</span></div>' for c in top[:20]])
        st.markdown(f'<div class="scroller-container"><div class="scroller">{ticker_html}</div></div>', unsafe_allow_html=True)

    # UI: MASTER RADAR
    st.markdown('<div class="radar-strip"><span>SENSEX: 74,119 ▲</span> <span>NIFTY: 22,490 ▲</span> <span>BTC: LIVE ⚡</span> <span>ETH: LIVE ⚡</span></div>', unsafe_allow_html=True)

    # UI: SENTINEL ALPHA
    st.header("🛰️ Sentinel Alpha Command")
    if sent:
        for c in sent:
            col1, col2, col3, col4 = st.columns([1, 4, 3, 2])
            with col1: st.image(c['image'], width=45)
            with col2: st.subheader(f"{c['name'].upper()} ({c['symbol'].upper()})")
            with col3: st.metric("Price", f"₹{c['current_price']:,.2f}", get_ind(c['price_change_percentage_24h_in_currency']))
            with col4:
                if st.button("📈 Analysis", key=f"btn_{c['id']}"):
                    df_chart = get_analysis_chart(c['id'])
                    if df_chart is not None:
                        fig = go.Figure(data=[go.Scatter(x=df_chart['time'], y=df_chart['price'], line=dict(color='#00FF00'))])
                        fig.update_layout(template="plotly_dark", height=250, margin=dict(l=10, r=10, t=10, b=10))
                        st.plotly_chart(fig, use_container_width=True)
            st.markdown("---")

    # UI: GLOBAL MEGA NODE
    st.header("🌍 Global Mega Node")
    pool = s_res if (search_q and s_res) else (top[:150] if top else [])
    if pool:
        g_df = pd.DataFrame([{"Rank": i.get("market_cap_rank"), "Logo": i.get("image"), "Name": i.get("name"), "Price": f"₹{i.get('current_price', 0):,.2f}", "24H": get_ind(i.get('price_change_percentage_24h_in_currency'))} for i in pool])
        st.dataframe(g_df, column_config={"Logo": st.column_config.ImageColumn()}, use_container_width=True, hide_index=True)
else:
    st.warning("🔒 Sovereign Master, please enter the Master Key in the sidebar to activate the Monolith.")
                                                                                        
