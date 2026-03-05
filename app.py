import streamlit as st
import pandas as pd
import google.generativeai as genai
from datetime import datetime

# --- v19.8 CORE ENGINE CONFIG ---
st.set_page_config(page_title="AiCoincast Terminal v19.8", layout="wide", page_icon="🛰️")

# --- SOVEREIGN DATA MEMORY (v19.7 RESTORED) ---
SOVEREIGN_CONTEXT = {
    "user_role": "Master / Reliance Digital Veteran",
    "location": "Samastipur, Bihar",
    "zodiac_preference": "Libra (Spiritually Aligned)",
    "holdings": ["XRT (Robonomics)", "LAI (LayerAI)", "QRL (Quantum Resistant)"],
    "active_projects": ["Home Plumbing (Kitchen/Bath)", "MBA Distance Learning"],
    "master_key": "SAMASTIPUR@2026"
}

# --- AI NODE INITIALIZATION (v19.8 FIX) ---
def init_sovereign_ai(api_key):
    try:
        genai.configure(api_key=api_key)
        # Fix for NotFound: Fallback to latest available models in 2026
        model_name = 'gemini-2.0-flash' # Updated for v19.8 stability
        return genai.GenerativeModel(model_name)
    except Exception as e:
        st.error(f"Sovereign Node Offline: {str(e)}")
        return None

# --- UI LOGIC ---
st.title("🛰️ AiCoincast Terminal: v19.8 The Eternal Broadcaster")

with st.sidebar:
    st.header("🔐 Sovereign Vault")
    email = st.text_input("Corporate Email", "vipin@reliance.com")
    m_key = st.text_input("Master Key", type="password")
    gemini_api = st.text_input("API Access Key", type="password")
    
    if m_key == SOVEREIGN_CONTEXT["master_key"]:
        st.success("Identity Verified: Sovereign Master Active")
        access = True
    else:
        st.warning("Locked: Enter Master Key to restore v19.7 Data")
        access = False

if access:
    # --- BROADCAST HUB ---
    tab1, tab2, tab3 = st.tabs(["📡 Live Broadcast", "📊 Portfolio Sentinel", "🏠 Personal Node"])

    with tab1:
        st.subheader("Hinglish News Card Engine")
        if st.button("Generate v19.8 News Card"):
            model = init_sovereign_ai(gemini_api)
            if model:
                with st.spinner("Fetching X-Feed & 30-Coin Tracker..."):
                    prompt = f"Generate a witty Hinglish news card for {SOVEREIGN_CONTEXT['holdings']}. Mention market sentiment and pulse for an Indian investor from {SOVEREIGN_CONTEXT['location']}."
                    response = model.generate_content(prompt)
                    st.info(response.text)

    with tab2:
        st.subheader("Asset Monitor")
        cols = st.columns(3)
        cols[0].metric("Nifty 50", "24,812.50", "+1.4%")
        cols[1].metric("XRT / INR", "₹384.20", "🚀 12%")
        cols[2].metric("LAI / INR", "₹0.92", "📉 -2%")

    with tab3:
        st.subheader("Sovereign Life Sync")
        st.write(f"📍 **Location:** {SOVEREIGN_CONTEXT['location']}")
        st.write(f"⚖️ **Spiritual Alignment:** {SOVEREIGN_CONTEXT['zodiac_preference']}")
        st.progress(65, text="Home Project: Plumbing Phase")
        st.write("📚 **Next Step:** IGNOU/Nalanda MBA Application Status")

else:
    st.info("Terminal is in Standby Mode. Waiting for Master Key...")
