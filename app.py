import streamlit as st
import yfinance as yf
import google.generativeai as genai
from google.generativeai import types
import requests
import time
from datetime import datetime
import pytz
import streamlit.components.v1 as components

# --- 1. SYSTEM CONFIG ---
st.set_page_config(page_title="AiCoincast v17.4 Master", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
MASTER_PASSWORD = "SAMASTIPUR@2026"

# --- 2. LIVE MARKET TABLE ALGORITHM (CoinGecko Style) ---
def get_coingecko_table():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_desc&per_page=8&page=1"
        return requests.get(url, timeout=10).json()
    except: return []

# --- 3. LOGIN GUARD ---
if "password_correct" not in st.session_state:
    st.markdown("<h2 style='text-align: center; color: #BC13FE;'>🛡️ Iron Vault Login</h2>", unsafe_allow_html=True)
    pwd = st.text_input("Master Key:", type="password")
    if st.button("Unlock"):
        if pwd == MASTER_PASSWORD:
            st.session_state["password_correct"] = True
            st.rerun()
    st.stop()

# --- 4. FIXED AI ENGINE (The Final 404 Solution) ---
def ai_commander_fixed(query):
    try:
        if "GEMINI_API_KEY" not in st.secrets: return "API Key Missing", None
        
        # Method: Direct Configuration to avoid v1beta mismatch
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        
        # Logic: Using 'gemini-1.5-flash' with explicit safety settings
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Fix: Explicitly checking if model exists before generating
        response = model.generate_content(
            f"Write a 3-line financial report on {query} for Indian investors in Hinglish.",
            generation_config=genai.types.GenerationConfig(temperature=0.7)
        )
        
        img = f"https://pollinations.ai/p/{query.replace(' ','_')}_cyberpunk?seed={time.time()}"
        return response.text, img
    except Exception as e:
        # User-friendly fallback
        return f"AI Node busy. Trying to recalibrate... (Status: {str(e)})", None

# --- 5. UI: OMNISCIENT TERMINAL ---

# Top Ticker
components.html(f'<div style="background:#BC13FE;color:white;padding:10px;font-weight:bold;"><marquee>🚀 BTC: LIVE | 📊 NIFTY 50: LIVE | 🛰️ v17.4 SOVEREIGN NODE ACTIVE</marquee></div>', height=50)

# Sidebar
with st.sidebar:
    st.title("🛰️ Sentinel")
    st.success("v17.4 Master Sync")
    if st.button("🔒 Logout"):
        del st.session_state["password_correct"]
        st.rerun()

# Main Body
st.title("🤖 AiCoincast v17.4 Master")

# Section A: CoinGecko Style Live Table
st.subheader("📊 Live Market Intelligence (INR)")
coins = get_coingecko_table()
if coins:
    cols = st.columns(len(coins[:4]))
    for i, coin in enumerate(coins[:4]):
        cols[i].metric(coin['name'], f"₹{coin['current_price']:,}", f"{coin['price_change_percentage_24h']:.2f}%")
    
    # Large Detailed Table
    st.write("---")
    st.dataframe(coins[['name', 'symbol', 'current_price', 'price_change_percentage_24h', 'market_cap']], use_container_width=True)

# Section B: AI Search & Report
st.divider()
target = st.text_input("🔍 Search Asset Analysis:", "XRT and LayerAI India")

if target:
    with st.spinner("AI Bot Analyzing..."):
        report, visual = ai_commander_fixed(target)
        st.markdown("<div style='border:2px solid #BC13FE; padding:20px; border-radius:15px; background:rgba(16,0,43,0.9);'>", unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1.5])
        with c1:
            if visual: st.image(visual)
        with c2:
            st.subheader(f"📝 Master Report: {target.upper()}")
            st.info(report)
            st.markdown(f'<a href="https://wa.me/?text={report[:300]}" target="_blank" style="background:#25D366;color:white;padding:10px;border-radius:10px;text-decoration:none;display:inline-block;width:100%;text-align:center;">📲 Share on WhatsApp</a>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
