import streamlit as st
import pandas as pd
import datetime
from streamlit_folium import folium_static
import folium

st.set_page_config(page_title="Exion ERP Kotli", layout="wide")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None

# --- LOGIN PORTAL ---
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

# --- LOGGED IN CONTENT ---
else:
    if st.sidebar.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()

    if st.session_state.role == "Salesman":
        st.title("📱 Salesman Portal")
        
        # Section 1: Attendance
        with st.expander("📍 Attendance (Hazri Lagayein)", expanded=True):
            if st.button("Aaj ki Hazri Mark Karein", use_container_width=True):
                waqt = datetime.datetime.now().strftime("%I:%M %p")
                st.success(f"Shukriya! Aapki hazri {waqt} par lag gayi hai.")

        # Section 2: Digital Khata
        with st.expander("📝 Digital Khata (Sale Entry)", expanded=True):
            shop = st.text_input("Dukan ka Naam:")
            amount = st.number_input("Aaj ki Sale (Rs.):", min_value=0)
            if st.button("Sale Record Save Karein", use_container_width=True):
                if shop and amount > 0:
                    st.balloons()
                    st.success(f"Saved: {shop} - Rs.{amount}")
                else:
                    st.error("Dukan ka naam aur raqam likhna lazmi hai.")

    elif st.session_state.role == "Admin":
        st.title("👨‍💼 Admin Dashboard")
        st.subheader("🌍 Kotli Live Map")
        # Aapka purana map
        m = folium.Map(location=[33.5158, 73.9018], zoom_start=14)
        folium.Marker([33.5158, 73.9018], popup="Office").add_to(m)
        folium_static(m)
