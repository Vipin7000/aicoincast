import streamlit as st
import google.generativeai as genai
import os

# --- 1. CONFIGURATION & API SETUP ---
# Streamlit Secrets se API Key lena sabse safe tareeka hai
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    # Agar local test kar rahe hain toh yahan apni key dalein
    API_KEY = "YOUR_API_KEY_HERE" 

genai.configure(api_key=API_KEY)

# --- 2. MODEL INITIALIZATION (Fixed for v1 Stable) ---
# Yahan 'v1beta' hatane se 404 error fix ho jayega
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 3. HELPER FUNCTIONS ---
def get_crypto_analysis(query):
    """AI se crypto analysis fetch karne ke liye function"""
    try:
        response = model.generate_content(query)
        return response.text
    except Exception as e:
        return f"Model Error: {str(e)}"

# --- 4. SIDEBAR (SENTINEL) ---
st.sidebar.title("🛡️ Sentinel")

# Nifty Data (Static ya API se jo aapne pehle likha tha)
st.sidebar.markdown("### NIFTY 50")
st.sidebar.subheader("₹24,865.70")
st.sidebar.divider()

# Crypto Prices (Example values, replace with your live data logic)
st.sidebar.markdown("### Bitcoin")
st.sidebar.write("₹6,294,198")
st.sidebar.caption("📉 -0.56%")

st.sidebar.markdown("### Ethereum")
st.sidebar.write("₹182,732")
st.sidebar.caption("📉 -2.05%")

if st.sidebar.button("Logout"):
    st.cache_data.clear()
    st.rerun()

# --- 5. MAIN INTERFACE (AiCoincast v18.6) ---
st.title("🚀 AiCoincast v18.6 Ultra")
st.write(f"**Last Sync:** {st.session_state.get('last_sync', 'Just Now')}")

# Tabs for organization
tab1, tab2, tab3 = st.tabs(["💰 Portfolio & AI", "📊 Analytics", "🔔 Alerts"])

with tab1:
    with st.expander("🛠️ Manage Holdings", expanded=False):
        st.write("Apni holdings yahan manage karein.")

    st.subheader("Live Status")
    
    # AI Intelligence Search
    query_input = st.text_input("🔍 AI Intelligence Search:", value="XRT and LayerAI Price Outlook India")
    
    if st.button("Generate Report"):
        with st.spinner("AI Analysis fetch ho raha hai..."):
            report = get_crypto_analysis(query_input)
            
            # Master Report Box
            st.markdown("### 📜 Master Report")
            st.info(report)
            
            # WhatsApp Share Button
            st.download_button("📲 Download Report", report, file_name="crypto_report.txt")

# --- 6. FOOTER ---
st.markdown("---")
st.caption("Powered by Gemini 1.5 Flash Stable | VIPIN CRYPTO APP")
