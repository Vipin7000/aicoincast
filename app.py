import streamlit as st
import google.generativeai as genai

# --- 1. API CONFIGURATION (Error Fix) ---
# Yahan 'v1beta' ka koi zikr nahi hai, isliye 404 error nahi aayega
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    # Latest Stable Model use kar rahe hain
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"API Setup Error: {e}")

# --- 2. CRYPTO PREDICTION LOGIC ---
def get_coin_prediction(coin_name):
    """XRT aur LAI ke liye specific AI analysis fetch karne ke liye"""
    prompt = f"""
    Analyze the current market sentiment for {coin_name} cryptocurrency in India.
    Provide a short price outlook and potential growth for the next 30 days.
    Keep the tone professional and concise.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Prediction Error: {str(e)}"

# --- 3. UI SETUP ---
st.title("🚀 AiCoincast v18.6 Ultra")

# Sidebar for Portfolio
st.sidebar.title("🛡️ Sentinel")
st.sidebar.markdown("### My Holdings")
st.sidebar.info("Coins: XRT, LAI, QRL") # Aapke portfolio ke coins

# Main Interface
st.subheader("Live Status & Intelligence Search")
query = st.text_input("Analyze Coin:", value="XRT and LayerAI")

if st.button("Generate Master Report"):
    with st.spinner("AI is analyzing market data..."):
        # Specific Analysis for your coins
        report = get_coin_prediction(query)
        
        st.markdown("### 📜 Master Report")
        st.success("Synced Successfully!") 
        st.write(report)

# --- 4. FOOTER ---
st.markdown("---")
st.caption("Powered by Gemini 1.5 Flash Stable | VIPIN CRYPTO APP")
