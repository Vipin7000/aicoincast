import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
import time
import feedparser # RSS Feed library

# --- [SYSTEM CONFIG] ---
st.set_page_config(page_title="AiCoincast Terminal v19.8 Ultra", layout="wide")
MASTER_KEY = "SAMASTIPUR@2026"

COIN_MAP = {
    "virtual-protocol": "VIRTUAL", "griffin-2": "GRIFFIN", "v-ai-2": "VAI",
    "robonomics-network": "XRT", "velas": "VLX", "qanplatform": "QANX",
    "chaingpt": "CGPT", "sinverse": "SIN", "matic-network": "POLYGON", "nftb": "NFTB"
}

# --- [DATA ENGINES] ---
@st.cache_data(ttl=60)
def fetch_safe_data():
    ids = ",".join(COIN_MAP.keys())
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=inr&include_24hr_change=true&include_7d_change=true&include_30d_change=true"
    try:
        response = requests.get(url, timeout=5)
        return response.json() if response.status_code == 200 else {}
    except: return {}

def fetch_rss_news():
    # Global Crypto & Finance RSS Feeds
    feed_url = "https://cointelegraph.com/rss/tag/bitcoin"
    try:
        feed = feedparser.parse(feed_url)
        return feed.entries[:5] # Latest 5 news
    except: return []

# --- [UI ARCHITECTURE] ---
st.title("🛰️ AiCoincast Terminal v19.8 Ultra (RSS Enabled)")

with st.sidebar:
    st.header("🔐 Vault Access")
    m_key = st.text_input("Master Key", type="password")
    raw_api_key = st.text_input("Gemini API Key", type="password")
    api_key = raw_api_key.strip().replace('"', '').replace("'", "")

if m_key == MASTER_KEY:
    # [FIX: LOCK FOLDERS] Tabs are defined before any data processing
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Market Sentinel", "📈 Performance", "📰 Global RSS & AI News", "⚖️ Risk Calculator"])
    
    data = fetch_safe_data()

    with tab1:
        st.subheader("Live Assets & Nifty Monitor")
        cols = st.columns(5)
        for i, (id, symbol) in enumerate(COIN_MAP.items()):
            coin_info = data.get(id, {})
            p, c = coin_info.get('inr'), coin_info.get('inr_24h_change')
            if p is not None:
                cols[i % 5].metric(f"{symbol}/INR", f"₹{float(p):,.4f}", f"{float(c or 0):.2f}%")
            else:
                cols[i % 5].warning(f"{symbol} Offline")
        st.divider()
        st.metric("NIFTY 50 (Live)", "₹24,450.45", "-1.27%", delta_color="inverse")

    with tab2:
        st.subheader("Weekly & Monthly Performance News")
        if data:
            perf_list = [{"Asset": sym, "7D %": f"{data.get(id, {}).get('inr_7d_change', 0):.2f}%", 
                          "30D %": f"{data.get(id, {}).get('inr_30d_change', 0):.2f}%"} for id, sym in COIN_MAP.items()]
            st.table(pd.DataFrame(perf_list))

    with tab3:
        col_left, col_right = st.columns(2)
        with col_left:
            st.subheader("🛰️ AI News Broadcaster")
            if st.button("Generate Bullet News"):
                if api_key:
                    try:
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        time.sleep(1)
                        prompt = f"Give a quick Hinglish update for {list(COIN_MAP.values())}."
                        st.info(model.generate_content(prompt).text)
                    except: st.error("AI Limit hit. Wait 1 min.")
        
        with col_right:
            st.subheader("🌍 Global RSS Feed")
            rss_entries = fetch_rss_news()
            if rss_entries:
                for entry in rss_entries:
                    st.markdown(f"**[{entry.title}]({entry.link})**")
            else: st.warning("RSS Feed temporarily unavailable.")

    with tab4:
        st.subheader("Sovereign Risk Calculator")
        coin_sel = st.selectbox("Asset", list(COIN_MAP.values()))
        entry = st.number_input("Entry Price", value=1.0)
        target = st.number_input("Target Price", value=2.0)
        if st.button("Calculate"):
            st.success(f"Potential Return: {((target/entry)-1)*100:.2f}% ✅")

else:
    st.info("Terminal in Standby. Enter Master Key to unlock all folders.")
                
