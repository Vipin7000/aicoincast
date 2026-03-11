import streamlit as st
import pandas as pd
import requests

# --- [1. MASTER CONFIG & DESIGN] ---
st.set_page_config(page_title="AiCoincast v2.0 Sovereign", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

st.markdown("""
    <style>
    .stApp { background-color: #04010a !important; }
    h1, h2, h3, h4, p, span, div { color: #FFFFFF !important; font-family: 'Inter', sans-serif; }
    
    .vault-main {
        background: linear-gradient(135deg, rgba(26, 11, 53, 0.9) 0%, rgba(5, 1, 13, 1) 100%);
        padding: 30px; border-radius: 20px; border: 2px solid #00FF00;
        text-align: center; margin: 20px 0; box-shadow: 0 0 40px rgba(0, 255, 0, 0.2);
    }
    .neon-up { color: #00FF00 !important; font-weight: bold; text-shadow: 0 0 5px #00FF00; }
    .neon-down { color: #FF0000 !important; font-weight: bold; text-shadow: 0 0 5px #FF0000; }
    
    .radar-grid {
        display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px;
        background: rgba(255, 255, 255, 0.03); padding: 15px; border-radius: 12px; margin-bottom: 20px;
    }
    .radar-box { background: rgba(255,255,255,0.02); padding: 8px; border-radius: 8px; text-align: center; border: 1px solid rgba(255,255,255,0.05); }
    
    .ticker-wrap { width: 100%; overflow: hidden; border-bottom: 1px solid #00FF00; padding: 10px 0; background: #000; }
    .ticker { display: flex; white-space: nowrap; animation: ticker 20s linear infinite; }
    .glass-card { flex-shrink: 0; padding: 0 25px; border-right: 1px solid rgba(0,255,0,0.3); font-size: 0.9rem; }
    @keyframes ticker { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }
    </style>
    """, unsafe_allow_html=True)

# --- [CORE ENGINE] ---
def get_neon_ind(val):
    try:
        v = float(val) if val is not None else 0.0
        if v > 0: return f"<span class='neon-up'>▲ +{v:.1f}%</span>"
        if v < 0: return f"<span class='neon-down'>▼ {v:.1f}%</span>"
        return "▬ 0.0%"
    except: return "▬"

def fetch_api(url):
    try:
        r = requests.get(url, timeout=15)
        return r.json() if r.status_code == 200 else None
    except: return None

CORE_IDS = ["bitcoin", "ethereum", "polygon-ecosystem-token", "virtual-protocol", "qanplatform", "chaingpt", "velas", "griffain", "vaiot", "everdome", "bloktopia", "sin-city", "robonomics-network", "unmarshal", "layerai", "nftb"]

# --- [DEPLOYMENT] ---
with st.sidebar:
    st.title("🛡️ OMNI VAULT v2.0")
    m_key = st.text_input("Enter Master Key", type="password")
    st.markdown("---")
    st.subheader("💰 Portfolio Config")
    h_qty = st.number_input("Holdings (XRT)", value=206)
    h_buy = st.number_input("Buy Price (₹)", value=480)
    st.markdown("---")
    x_nodes = [st.text_input(f"Node #{i}") for i in range(17, 21)]

if m_key == MASTER_KEY:
    q = st.text_input("🔍 Neural Search Index", placeholder="Search 5000+ Assets...")
    
    # Force Multi-Interval Percentages
    base_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&price_change_percentage=24h,7d,30d,200d"
    
    top = fetch_api(f"{base_url}&order=market_cap_desc&per_page=200&page=1")
    sentinel = fetch_api(f"{base_url}&ids={','.join(CORE_IDS + [x for x in x_nodes if x])}")
    s_res = fetch_api(f"{base_url}&ids={q.lower().replace(' ', '-')}") if (q and len(q) >= 3) else []

    # 1. TOP TICKER
    if top:
        t_html = "".join([f'<div class="glass-card"><b>{c["symbol"].upper()}</b> ₹{c["current_price"]:,.0f} {get_neon_ind(c.get("price_change_percentage_24h"))}</div>' for c in (top[:20]*2)])
        st.markdown(f'<div class="ticker-wrap"><div class="ticker">{t_html}</div></div>', unsafe_allow_html=True)

    # 2. MASTER PORTFOLIO VAULT
    if sentinel:
        x_coin = next((i for i in sentinel if i["id"] == "robonomics-network"), None)
        if x_coin:
            curr_total = x_coin['current_price'] * h_qty
            prof = curr_total - (h_buy * h_qty)
            st.markdown(f"""
            <div class="vault-main">
                <div style="font-size:1.1rem; letter-spacing:3px; color:#00FF00; opacity:0.7;">MASTER PORTFOLIO COMMAND</div>
                <div style="font-size:3rem; font-weight:800; margin:10px 0; text-shadow:0 0 20px #00FF00;">₹{curr_total:,.2f}</div>
                <div style="font-size:1.3rem;">Total Profit: {get_neon_ind(prof)}</div>
            </div>
            """, unsafe_allow_html=True)

    # 3. GLOBAL RADAR GRID
    st.markdown(f"""
    <div class="radar-grid">
        <div class="radar-box">🇮🇳 SENSEX<br>{get_neon_ind(0.5)}</div>
        <div class="radar-box">🇮🇳 NIFTY 50<br>{get_neon_ind(0.7)}</div>
        <div class="radar-box">🇺🇸 S&P 500<br>{get_neon_ind(1.1)}</div>
        <div class="radar-box">🇺🇸 NASDAQ<br>{get_neon_ind(1.4)}</div>
        <div class="radar-box">🇯🇵 NIKKEI<br>{get_neon_ind(-0.3)}</div>
        <div class="radar-box">🇨🇳 SHANGHAI<br>{get_neon_ind(0.1)}</div>
        <div class="radar-box">🇬🇧 FTSE 100<br>{get_neon_ind(-0.2)}</div>
        <div class="radar-box">🇩🇪 DAX 40<br>{get_neon_ind(0.6)}</div>
        <div class="radar-box">🇫🇷 CAC 40<br>{get_neon_ind(0.4)}</div>
        <div class="radar-box">🇭🇰 HANG SENG<br>{get_neon_ind(-0.9)}</div>
    </div>
    """, unsafe_allow_html=True)

    # 4. TABLES (SENTINEL & GLOBAL)
    def draw_table(data, head):
        st.subheader(head)
        if data:
            rows = []
            for c in data:
                rows.append({
                    "Rank": c.get("market_cap_rank"),
                    "Logo": c.get("image"),
                    "Asset": (c.get("name") if c.get("id") != "everdome" else "HUM(AI)N (AI)").upper(),
                    "Price": f"₹{c.get('current_price',0):,.2f}",
                    "24H": c.get('price_change_percentage_24h_in_currency'),
                    "7D": c.get('price_change_percentage_7d_in_currency'),
                    "30D": c.get('price_change_percentage_30d_in_currency'),
                    "90D": c.get('price_change_percentage_200d_in_currency')
                })
            df = pd.DataFrame(rows)
            st.write(df.to_html(escape=False, formatters={
                "Logo": lambda x: f'<img src="{x}" width="25">',
                "24H": get_neon_ind, "7D": get_neon_ind, "30D": get_neon_ind, "90D": get_neon_ind
            }, index=False), unsafe_allow_html=True)
        else:
            st.warning("Data fetch in progress or Node ID incorrect...")

    draw_table(sentinel, "🛰️ Sentinel Alpha Command")
    st.markdown("<br>", unsafe_allow_html=True)
    draw_table(s_res if (q and s_res) else top[:100], "🌍 Global Mega Node")

else:
    st.info("🔒 Sovereign Master, authentication required to reveal the Vault.")
                      
