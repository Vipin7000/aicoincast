import streamlit as st
import pandas as pd
import requests

# --- [1. MASTER CONFIG & WORLD-CLASS DESIGN] ---
st.set_page_config(page_title="AiCoincast v2.0 Sovereign", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

st.markdown("""
    <style>
    .stApp { background-color: #04010a !important; }
    h1, h2, h3, h4, p, span, div { color: #FFFFFF !important; font-family: 'Inter', sans-serif; }
    
    /* PREMIUM TICKER */
    .ticker-wrap {
        width: 100%; overflow: hidden; background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(20px); border-bottom: 2px solid #00FF00; padding: 10px 0;
    }
    .ticker { display: flex; white-space: nowrap; animation: ticker 20s linear infinite; }
    .glass-card {
        flex-shrink: 0; background: rgba(255, 255, 255, 0.05);
        padding: 6px 20px; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 0 10px; font-size: 0.9rem;
    }
    @keyframes ticker { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }
    
    /* GLOBAL RADAR STRIP */
    .radar-container {
        display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px;
        background: rgba(26, 11, 53, 0.5); padding: 15px; border-radius: 15px;
        margin: 20px 0; border: 1px solid #00FF00; box-shadow: 0 0 20px rgba(0,255,0,0.1);
    }
    .radar-item { text-align: center; border-right: 1px solid rgba(255,255,255,0.1); padding: 5px; }
    .radar-item:last-child { border-right: none; }
    
    .neon-up { color: #00FF00 !important; font-weight: bold; text-shadow: 0 0 5px #00FF00; }
    .neon-down { color: #FF0000 !important; font-weight: bold; text-shadow: 0 0 5px #FF0000; }
    
    /* TABLE STYLING */
    .styled-table { width: 100%; border-collapse: collapse; margin-top: 10px; }
    th { background: #1a0b35; padding: 12px; text-align: left; border-bottom: 2px solid #00FF00; }
    td { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- [DATA ENGINE] ---
def get_neon_ind(val):
    v = float(val) if val is not None else 0.0
    return f"<span class='neon-up'>▲ +{v:.1f}%</span>" if v > 0 else (f"<span class='neon-down'>▼ {v:.1f}%</span>" if v < 0 else "▬ 0.0%")

def fetch_api(url):
    try:
        r = requests.get(url, timeout=15); return r.json() if r.status_code == 200 else None
    except: return None

CORE_IDS = ["bitcoin", "ethereum", "polygon-ecosystem-token", "virtual-protocol", "qanplatform", "chaingpt", "velas", "griffain", "vaiot", "everdome", "bloktopia", "sin-city", "robonomics-network", "unmarshal", "layerai", "nftb"]

# --- [DEPLOYMENT] ---
with st.sidebar:
    st.title("🛡️ OMNI VAULT v2.0")
    m_key = st.text_input("Master Key", type="password")
    st.markdown("---")
    x_nodes = [st.text_input(f"Node #{i}") for i in range(17, 21)]

if m_key == MASTER_KEY:
    q = st.text_input("🔍 Neural Search Index", placeholder="Search 5000+ Assets...")
    base = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&price_change_percentage=24h,7d,30d,200d"
    top = fetch_api(f"{base}&order=market_cap_desc&per_page=250&page=1")
    sentinel = fetch_api(f"{base}&ids={','.join(CORE_IDS + [x for x in x_nodes if x])}")
    search_res = fetch_api(f"{base}&ids={q.lower().replace(' ', '-')}") if (q and len(q) >= 3) else []

    # TOP TICKER
    if top:
        t_html = "".join([f'<div class="glass-card"><b>{c["symbol"].upper()}</b>: ₹{c["current_price"]:,.0f} {get_neon_ind(c.get("price_change_percentage_24h"))}</div>' for c in (top[:20]*2)])
        st.markdown(f'<div class="ticker-wrap"><div class="ticker">{t_html}</div></div>', unsafe_allow_html=True)

    # NEW GLOBAL RADAR STRIP: TOP 10 ECONOMIES
    st.markdown(f"""
    <div class="radar-container">
        <div class="radar-item">🇮🇳 SENSEX<br>{get_neon_ind(0.5)}</div>
        <div class="radar-item">🇮🇳 NIFTY 50<br>{get_neon_ind(0.6)}</div>
        <div class="radar-item">🇺🇸 S&P 500<br>{get_neon_ind(1.2)}</div>
        <div class="radar-item">🇺🇸 NASDAQ<br>{get_neon_ind(1.5)}</div>
        <div class="radar-item">🇯🇵 NIKKEI 225<br>{get_neon_ind(-0.4)}</div>
        <div class="radar-item">🇨🇳 SHANGHAI<br>{get_neon_ind(0.2)}</div>
        <div class="radar-item">🇬🇧 FTSE 100<br>{get_neon_ind(-0.1)}</div>
        <div class="radar-item">🇩🇪 DAX 40<br>{get_neon_ind(0.8)}</div>
        <div class="radar-item">🇫🇷 CAC 40<br>{get_neon_ind(0.7)}</div>
        <div class="radar-item">🇭🇰 HANG SENG<br>{get_neon_ind(-1.1)}</div>
    </div>
    """, unsafe_allow_html=True)

    # TABLE RENDERER
    def render_table(data, title):
        st.header(title)
        if data:
            df = pd.DataFrame([{
                "Rank": c.get("market_cap_rank"), "Logo": c.get("image"), 
                "Asset": c.get("name").upper() if c.get("id") != "everdome" else "HUM(AI)N (AI)",
                "Price": f"₹{c.get('current_price'):,.2f}",
                "24H": c.get('price_change_percentage_24h_in_currency'),
                "7D": c.get('price_change_percentage_7d_in_currency'),
                "30D": c.get('price_change_percentage_30d_in_currency'),
                "90D": c.get('price_change_percentage_200d_in_currency')
            } for c in data])
            st.write(df.to_html(escape=False, formatters={"Logo": lambda x: f'<img src="{x}" width="28">', "24H": get_neon_ind, "7D": get_neon_ind, "30D": get_neon_ind, "90D": get_neon_ind}, index=False), unsafe_allow_html=True)

    render_table(sentinel, "🛰️ Sentinel Alpha Command")
    st.markdown("---")
    render_table(search_res if (q and search_res) else top[:150], "🌍 Global Mega Node")

else:
    st.warning("🔒 Sovereign Master, authentication required to unlock Global Command.")
    
