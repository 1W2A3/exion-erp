import streamlit as st
import pandas as pd
import datetime
from streamlit_folium import folium_static
import folium

# Professional Page Setup
st.set_page_config(page_title="Exion ERP | Kotli", layout="wide")

# Custom CSS for Professional Look
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- LOGIN INTERFACE ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>Exion Distribution System</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.subheader("Login to your account")
        role = st.selectbox("Select Role", ["Admin", "Salesman"])
        pwd = st.text_input("Password", type="password")
        if st.button("Access Dashboard"):
            if role == "Admin" and pwd == "222":
                st.session_state.logged_in, st.session_state.role = True, "Admin"
                st.rerun()
            elif role == "Salesman" and pwd == "111":
                st.session_state.logged_in, st.session_state.role = True, "Salesman"
                st.rerun()
            else:
                st.error("Invalid Credentials!")

# --- AUTHENTICATED DASHBOARD ---
else:
    # Sidebar
    st.sidebar.title("Exion ERP")
    st.sidebar.write(f"Logged in as: **{st.session_state.role}**")
    if st.sidebar.button("Sign Out"):
        st.session_state.logged_in = False
        st.rerun()

    if st.session_state.role == "Admin":
        st.title("👨‍💼 Administrator Control Center")
        
        # Professional Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Daily Sales", "Rs. 45,000", "+5%")
        m2.metric("Active Salesman", "1", "Online")
        m3.metric("Pending Recoveries", "Rs. 12,800", "-2%")

        # Map Section
        st.markdown("### 🌍 Live Fleet Tracking (Kotli, AK)")
        m = folium.Map(location=[33.5158, 73.9018], zoom_start=14)
        folium.Marker([33.5158, 73.9018], popup="Head Office").add_to(m)
        folium_static(m)

        # Inventory Table (Sample)
        st.markdown("### 📦 Inventory Status")
        inventory_data = pd.DataFrame({
            "Item": ["Product A", "Product B", "Product C"],
            "Stock": [120, 45, 89],
            "Price": [1200, 850, 400]
        })
        st.table(inventory_data)

    elif st.session_state.role == "Salesman":
        st.title("📱 Field Sales Portal")
        
        tab1, tab2 = st.tabs(["📍 Attendance", "📝 Digital Khata"])
        
        with tab1:
            st.info("Log your daily attendance here.")
            if st.button("Check-In Now"):
                st.success(f"Attendance marked at {datetime.datetime.now().strftime('%H:%M')}")
        
        with tab2:
            st.subheader("New Sale Entry")
            shop = st.text_input("Shop Name")
            amt = st.number_input("Bill Amount (Rs.)", min_value=0)
            if st.button("Submit Sale"):
                st.balloons()
                st.success(f"Invoice saved for {shop}")
