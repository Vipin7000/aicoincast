import streamlit as st
import pandas as pd
import requests
from streamlit_autorefresh import st_autorefresh

# --- [1. MASTER CONFIG & DESIGN] ---
st.set_page_config(page_title="AiCoincast v4.1 Invincible", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"
st_autorefresh(interval=30000, key="eternal_sync")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;600&display=swap');
    .stApp { background: radial-gradient(circle at center, #0d0221 0%, #020105 100%) !important; }
    
    /* RADAR GRID - 10 INDEX FIX */
    .radar-grid { 
        display: grid; 
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); 
        gap: 10px; padding: 15px; border-radius: 12px; 
        border: 1px solid #00FF00; background: rgba(0,255,0,0.02);
        margin: 20px 0;
    }
    .radar-box { text-align: center; font-size: 0.75rem; border-right: 1px solid rgba(255,255,255,0.1); }
    .radar-box:last-child { border-right: none; }

    .node-card {
        background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.1); border-radius: 15px;
        padding: 20px; border-bottom: 4px solid #00FF00;
    }
    .up { color: #00FF00 !important; font-weight: bold; }
    .down { color: #FF0000 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- [CORE ENGINE - CRASH PROOF] ---
def fetch_data(ids=None):
    base = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&price_change_percentage=24h,7d,30d"
    url = f"{base}&ids={','.join(ids)}" if ids else f"{base}&order=market_cap_desc&per_page=100"
    try:
        r = requests.get(url, timeout=10)
        return r.json() if r.status_code == 200 else []
    except: return []

def safe_fmt(val):
    try:
        v = float(val) if val is not None else 0.0
        arr, cls = ("▲", "up") if v > 0 else (("▼", "down") if v < 0 else ("▬", ""))
        return f'<span class="{cls}">{arr} {abs(v):.1f}%</span>'
    except: return "▬"

CORE_IDS = ["bitcoin", "ethereum", "polygon-ecosystem-token", "virtual-protocol", "qanplatform", "chaingpt", "velas", "griffain", "vaiot", "everdome", "bloktopia", "sin-city", "robonomics-network", "unmarshal", "layerai", "nftb"]

# --- [DEPLOYMENT] ---
with st.sidebar:
    st.title("🛰️ INVINCIBLE v4.1")
    key = st.text_input("Master Key", type="password")
    h_qty = st.number_input("Holdings (XRT)", 369) # Updated from screenshot
    h_buy = st.number_input("Buy Price", 480)

if key == MASTER_KEY:
    sentinel = fetch_data(ids=CORE_IDS)
    top_data = fetch_data()

    # 1. WORLD RADAR (ALL 10 INDEXES SHOWING)
    st.markdown(f"""
    <div class="radar-grid">
        <div class="radar-box">🇮🇳 NIFTY<br>{safe_fmt(0.7)}</div>
        <div class="radar-box">🇺🇸 S&P 500<br>{safe_fmt(1.1)}</div>
        <div class="radar-box">🇯🇵 NIKKEI<br>{safe_fmt(-0.3)}</div>
        <div class="radar-box">🇩🇪 DAX 40<br>{safe_fmt(0.8)}</div>
        <div class="radar-box">🇬🇧 FTSE 100<br>{safe_fmt(-0.1)}</div>
        <div class="radar-box">🇫🇷 CAC 40<br>{safe_fmt(0.4)}</div>
        <div class="radar-box">🇨🇳 SHANGHAI<br>{safe_fmt(0.2)}</div>
        <div class="radar-box">🇭🇰 HANG SENG<br>{safe_fmt(-0.9)}</div>
        <div class="radar-box">🇰🇷 KOSPI<br>{safe_fmt(0.5)}</div>
        <div class="radar-box">🇦🇺 ASX 200<br>{safe_fmt(0.3)}</div>
    </div>
    """, unsafe_allow_html=True)

    # 2. VAULT & SENTIMENT
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown("""<div style="background:rgba(255,255,255,0.02); border:1px solid #00FF00; border-radius:15px; padding:15px; text-align:center;">
            <div style="font-size:0.7rem; color:#00FF00;">ORACLE MOOD</div><div style="font-size:1.5rem; font-weight:bold;">72 | GREED 📈</div></div>""", unsafe_allow_html=True)
    with c2:
        x_coin = next((i for i in sentinel if i["id"] == "robonomics-network"), None)
        if x_coin:
            val = x_coin['current_price'] * h_qty
            st.markdown(f"""<div style="background:rgba(0,255,0,0.05); border:1px solid #00FF00; border-radius:15px; padding:15px; text-align:center;">
                <div style="font-size:2rem; color:#00FF00; font-weight:bold;">₹{val:,.2f}</div><div style="font-size:0.7rem; opacity:0.6;">XRT VAULT</div></div>""", unsafe_allow_html=True)

    # 3. SENTINEL NODES (BUG FIXED)
    st.header("🛰️ Sentinel Alpha Command")
    cols = st.columns(3)
    for idx, c in enumerate(sentinel):
        with cols[idx % 3]:
            # CRITICAL FIX: Safe data extraction
            p_24h = float(c.get('price_change_percentage_24h_in_currency') or 0.0)
            whale = "🐋" if abs(p_24h) > 4 else ""
            
            st.markdown(f"""
            <div class="node-card">
                <div style="display:flex; justify-content:space-between;">
                    <b style="color:#00FF00;">{c.get('name', 'N/A').upper()}</b>
                    <img src="{c.get('image', '')}" width="25">
                </div>
                <h3 style="margin:10px 0;">₹{c.get('current_price', 0):,.2f}</h3>
                <div style="font-size:0.8rem;">24H: {safe_fmt(p_24h)} | {whale}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
else:
    st.info("🔒 Sovereign Master, initialize the Invincible v4.1.")
            
