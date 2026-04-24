import streamlit as st
import pandas as pd
import datetime
from streamlit_folium import folium_static
import folium

# Theme aur Map ko fix rakhne ke liye settings
st.set_page_config(page_title="Exion ERP Kotli", layout="wide")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None

# --- LOGIN PORTAL (Pehla Screen) ---
if not st.session_state.logged_in:
    st.title("🛡️ Exion Distribution System")
    role = st.selectbox("Apna Role Chunein:", ["Chunein...", "Salesman", "Admin"])
    pwd = st.text_input("Password:", type="password")
    
    if st.button("Login"):
        if role == "Salesman" and pwd == "111":
            st.session_state.logged_in = True
            st.session_state.role = "Salesman"
            st.rerun()
        elif role == "Admin" and pwd == "222":
            st.session_state.logged_in = True
            st.session_state.role = "Admin"
            st.rerun()
        else:
            st.error("Ghalat Password!")

# --- LOGIN KE BAAD KA SYSTEM ---
else:
    # Logout button sidebar mein
    if st.sidebar.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()

    if st.session_state.role == "Admin":
        st.title("👨‍💼 Admin Dashboard (Full Access)")
        
        # AAPKA PURANA MAP YAHAN HAI (Bilkul waisa hi)
        st.subheader("🌍 Kotli Live Map & Tracking")
        m = folium.Map(location=[33.5158, 73.9018], zoom_start=14, tiles="OpenStreetMap")
        folium.Marker([33.5158, 73.9018], popup="Main Office Kotli").add_to(m)
        folium_static(m)
        
        # Baki Reports
        st.markdown("---")
        st.subheader("📊 Sales Data (Digital Khata)")
        st.info("Salesman ki entry yahan nazar aaye gi.")

    elif st.session_state.role == "Salesman":
        st.title("📱 Salesman Portal")
        st.subheader("📍 Attendance & Digital Khata")
        
        shop = st.text_input("Dukan ka Naam:")
        amount = st.number_input("Aaj ki Sale (Rs.):", min_value=0)
        
        if st.button("Record Save Karein"):
            st.success(f"Dukan: {shop} | Raqam: {amount} save ho gayi!")
