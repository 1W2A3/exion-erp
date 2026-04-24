import streamlit as st
import pandas as pd
import datetime
from streamlit_folium import folium_static
import folium

# 1. Page Setup (Wahi purana layout)
st.set_page_config(page_title="Exion ERP Kotli", layout="wide")

# Login Check
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- LOGIN SCREEN ---
if not st.session_state.logged_in:
    st.title("🔐 Exion ERP Login")
    role = st.selectbox("Role:", ["Salesman", "Admin"])
    pwd = st.text_input("Password:", type="password")
    if st.button("Dakhil Hon"):
        if role == "Salesman" and pwd == "111":
            st.session_state.logged_in, st.session_state.role = True, "Salesman"
            st.rerun()
        elif role == "Admin" and pwd == "222":
            st.session_state.logged_in, st.session_state.role = True, "Admin"
            st.rerun()
        else:
            st.error("Ghalat Password!")

# --- LOGGED IN CONTENT ---
else:
    if st.sidebar.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()

    # --- ADMIN VIEW (Aapka Purana Dashboard Wapis) ---
    if st.session_state.role == "Admin":
        st.title("👨‍💼 Admin Control Dashboard")
        
        # 1. Purana Map
        st.subheader("🌍 Kotli Live Map")
        m = folium.Map(location=[33.5158, 73.9018], zoom_start=14)
        folium.Marker([33.5158, 73.9018], popup="Office").add_to(m)
        folium_static(m)

        # 2. Purani Inventory & Sales (Digital Khata)
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📦 Inventory Stock")
            # Yahan aap apna purana inventory wala data dikha sakte hain
            st.info("Stock aur Sales ka record yahan permanent save hoga.")
            
        with col2:
            st.subheader("📅 Salesman Activity")
            st.write("Hazri aur Sales ki report yahan nazar aayegi.")

    # --- SALESMAN VIEW (Simple aur Saaf) ---
    elif st.session_state.role == "Salesman":
        st.title("📱 Salesman Portal")
        st.subheader("📍 Attendance & Sales")
        
        if st.button("Hazri Lagayein ✅", use_container_width=True):
            st.success("Hazri lag gayi!")
            
        st.markdown("---")
        shop = st.text_input("Dukan ka Naam:")
        amt = st.number_input("Sale Raqam:", min_value=0)
        if st.button("Save Karein"):
            st.success(f"Saved: {shop} - {amt}")
