import streamlit as st
import google.generativeai as genai
import time
from datetime import datetime

# --- API Config ---
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 30 Coins Full List ---
# Aapke invested coins (XRT, LAI, QRL) top par hain
coins_30 = [
    "XRT", "LAI", "QRL", "BTC", "ETH", "SOL", "BNB", "XRP", "ADA", "DOGE",
    "AVAX", "DOT", "TRX", "LINK", "MATIC", "SHIB", "LTC", "BCH", "UNI", "NEAR",
    "ARB", "APT", "OP", "STX", "FIL", "GRT", "RNDR", "INJ", "PEPE", "BONK"
]

# --- UI Setup ---
st.set_page_config(page_title="AiCoincast v19.8", layout="wide")
st.title("🚀 AiCoincast Terminal v19.8 (Lite)")

# Sidebar: Refresh Control
st.sidebar.header("⚙️ Settings")
ref_rate = st.sidebar.slider("Auto-Refresh (Minutes)", 1, 10, 5)

# --- Logic: Auto-Refreshing Grid ---
@st.fragment(run_every=ref_rate * 60)
def show_assets():
    st.subheader(f"📊 Live Monitor [{datetime.now().strftime('%H:%M:%S')}]")
    # 6 Columns for 'Shrinked' view
    cols = st.columns(6) 
    
    for i, coin in enumerate(coins_30):
        with cols[i % 6]:
            # Rate limiting check: Har 10 coins ke baad chota gap
            if i > 0 and i % 10 == 0:
                time.sleep(0.5)
            
            # Yahan aap apna real price logic dal sakte hain
            st.metric(label=coin, value=f"₹{i+1*10.5:.2f}", delta=f"{i%4}%")

# --- Logic: Short News Card ---
def get_short_news():
    try:
        # Strict prompt for shrinking content
        p = "Top 3 crypto news in Hinglish. Max 8 words per point. Bullet points only."
        res = model.generate_content(p)
        return res.text
    except Exception as e:
        if "429" in str(e): return "⚠️ Quota hit! Wait 1 min."
        return "Error loading news."

# --- Layout Execution ---
show_assets()

st.divider()

# Compact News Card
with st.expander("📰 v19.8 News Card (Hinglish)", expanded=True):
    if st.button("Generate Bullet News"):
        with st.spinner("Shortening..."):
            news_data = get_short_news()
            st.markdown(news_data)

st.caption("Auto-refresh active. Optimized for ResourceExhausted errors.")
