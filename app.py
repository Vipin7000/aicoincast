import streamlit as st
import google.generativeai as genai
import requests
import time
from datetime import datetime
import pytz

# --- 1. CONFIG & SYSTEM SETTINGS ---
st.set_page_config(page_title="AiCoincast | Master v16.6", layout="wide")
IST = pytz.timezone('Asia/Kolkata')

# Master Password (Samastipur Node)
MASTER_PASSWORD = "SAMASTIPUR@2026"

# --- 2. AUTHENTICATION GUARD ---
if "password_correct" not in st.session_state:
    st.markdown("<h2 style='text-align: center; color: #BC13FE;'>🛡️ Iron Vault Login</h2>", unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        pwd = st.text_input("Enter Master Key:", type="password")
        if st.button("Unlock Terminal"):
            if pwd == MASTER_PASSWORD:
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("🚫 Access Denied: Invalid Key")
    st.stop()

# --- 3. THEME & UI STYLING ---
st.markdown("""
    <style>
    .main { background-color: #030008; color: #FFFFFF; }
    .news-container { 
        border: 2px solid #BC13FE; padding: 25px; border-radius: 20px; 
        background: rgba(16,0,43,0.95); box-shadow: 0px 0px 20px rgba(188, 19, 254, 0.3);
    }
    .sentinel-box { background: #161B22; border-left: 5px solid #00F5FF; padding: 12px; border-radius: 10px; margin-bottom: 10px; }
    .whatsapp-btn { background-color: #25D366; color: white; border-radius: 10px; padding: 10px; text-align: center; font-weight: bold; text-decoration: none; display: inline-block; width: 100%; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR: MONITORING & TOOLS ---
with st.sidebar:
    st.title("🛰️ System Sentinel")
    st.write(f"User: **Admin (Samastipur)**")
    
    def get_crypto_data(cid):
        try:
            res = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={cid}&vs_currencies=usd,inr&include_24hr_change=true", timeout=5).json()
            return res.get(cid)
        except: return None

    for coin, cid in {"XRT": "robonomics-network", "LAI": "layerai"}.items():
        data = get_crypto_data(cid)
        if data:
            color = "#00FF00" if data['usd_24h_change'] > 0 else "#FF0000"
            st.markdown(f"""
            <div class='sentinel-box'>
                <small style='color:#00F5FF;'>{coin}</small><br>
                <b>₹{data['inr'] if data['inr'] > 1 else f"{data['inr']:.4f}"}</b> 
                <span style='color:{color}'>({data['usd_24h_change']:.2f}%)</span>
            </div>
            """, unsafe_allow_html=True)
    
    if st.button("🔒 Secure Logout"):
        del st.session_state["password_correct"]
        st.rerun()

# --- 5. MAIN DASHBOARD ---
st.title("🤖 AiCoincast v16.6")
st.caption(f"Sovereign Visual Terminal | Node: Reliance Digital | {datetime.now(IST).strftime('%H:%M:%S IST')}")

target_query = st.text_input("📡 Enter Market Target:", "XRT and LayerAI India News")

def get_visual_news(topic):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Provide a 2-line flash news update about {topic} in Hinglish for Indian investors. Sharp and professional."
        res = model.generate_content(prompt)
        img = f"https://pollinations.ai/p/{topic.replace(' ','_')}_futuristic_finance?seed={time.time()}"
        return res.text, img
    except:
        return "⚠️ AI Node busy. Check XRT/LAI status in sidebar.", "https://via.placeholder.com/600x300/10002B/00F5FF?text=Sentinel+Active"

with st.spinner("Executing Master Algorithms..."):
    news_text, visual_url = get_visual_news(target_query)
    
    st.markdown("<div class='news-container'>", unsafe_allow_html=True)
    c_img, c_txt = st.columns([1, 1.2])
    
    with c_img:
        st.image(visual_url, use_container_width=True)
    
    with c_txt:
        st.subheader(f"📢 LIVE NEWS: {target_query.upper()}")
        st.info(news_text)
        
        # WhatsApp Share Integration (v15.3 Feature)
        whatsapp_url = f"https://wa.me/?text=AiCoincast%20Flash%20News%3A%0A{news_text[:500]}..."
        st.markdown(f'<a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">📲 Share News on WhatsApp</a>', unsafe_allow_html=True)
        
        if st.button("🔄 Refresh Pulse"):
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()
st.caption("© 2026 AiCoincast India | v16.6 Final Master Code | Mass Comm & Digital Excellence")
