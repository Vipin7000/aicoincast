import streamlit as st
import yfinance as yf
import google.generativeai as genai
import streamlit.components.v1 as components
import re

# --- SETTINGS & SECURITY ---
st.set_page_config(page_title="AiCoincast | Global Intelligence", layout="wide")

# API Key Security
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-pro')
    else:
        st.info("💡 AI Assistant offline hai. Streamlit Secrets mein Key add karein.")
except Exception as e:
    st.error(f"Security Alert: {e}")

# Midnight Purple Theme
st.markdown("""
    <style>
    .main { background-color: #1A1033; color: #FFFFFF; }
    .stMetric { background-color: #241744; padding: 15px; border-radius: 10px; border: 1px solid #BC13FE; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCTIONS ---
def is_company_email(email):
    public_domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]
    domain = email.split('@')[-1] if "@" in email else ""
    return (domain not in public_domains and domain != ""), domain

def news_card(title, content, source, author_type="AI"):
    bg = "#000000" if author_type == "AI" else "#062c12"
    border = "#00F5FF" if author_type == "AI" else "#00FF00"
    label = "🤖 AI CRAWLER" if author_type == "AI" else "👤 OFFICIAL SOURCE"
    st.markdown(f"""
        <div style="background-color: {bg}; color: white; padding: 20px; border-radius: 10px; 
                    border-left: 5px solid {border}; margin-bottom: 15px;">
            <span style="color: {border}; font-weight: bold; font-size: 11px;">{label}</span>
            <h3 style="margin-top: 5px;">{title}</h3>
            <p style="font-size: 14px; opacity: 0.9;">{content}</p>
            <p style="font-size: 11px; opacity: 0.6;">Source: {source}</p>
        </div>
    """, unsafe_allow_html=True)

# --- UI ---
ticker_html = """
<div style="background-color: #241744; color: #00F5FF; padding: 10px; font-family: sans-serif; border-bottom: 2px solid #BC13FE;">
    <marquee scrollamount="6">🚀 BTC: Live | 🇮🇳 NIFTY: Live | 🛡️ AiCoincast AI-Shield Active | 🌎 Market Analysis Live...</marquee>
</div>
"""
components.html(ticker_html, height=50)

with st.sidebar:
    st.title("🏢 Partner Login")
    email = st.text_input("Company Email")
    if st.button("Login"):
        valid, dom = is_company_email(email)
        if valid:
            st.success(f"Verified: {dom}")
        else:
            st.error("Official Email Required")

st.title("🤖 AiCoincast Intelligence")
st.caption("AI-Powered Financial Hub | Samastipur to Global")

# Market Grid
cols = st.columns(4)
indices = {"NIFTY 50": "^NSEI", "NASDAQ": "^IXIC", "S&P 500": "^GSPC", "BITCOIN": "BTC-USD"}
for i, (name, sym) in enumerate(indices.items()):
    try:
        val = yf.Ticker(sym).history(period="1d")['Close'].iloc[-1]
        cols[i].metric(name, f"{val:,.2f}")
    except:
        cols[i].metric(name, "Live")

st.divider()

c1, c2 = st.columns([2, 1])
with c1:
    st.subheader("📰 Verified News")
    news_card("AI Demand Drives Tech Stocks", "Nvidia leads global chip market surge.", "Financial API", "AI")
    news_card("Official Blockchain Update", "New security protocols live on mainnet.", "Verified Rep", "Human")

with c2:
    st.subheader("🤖 AI Chatbot")
    ask = st.chat_input("Ask about market...")
    if ask and "GEMINI_API_KEY" in st.secrets:
        resp = model.generate_content(f"Briefly answer in Hinglish: {ask}")
        st.info(resp.text)

st.markdown("---")
st.caption("© 2026 AiCoincast | Secured by AI | Digital Excellence")
