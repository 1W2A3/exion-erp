import streamlit as st
import pandas as pd
import datetime
from streamlit_folium import folium_static
import folium

# Professional Page Setup
st.set_page_config(page_title="Exion ERP | Distribution", layout="wide")

# Theme Styling
st.markdown("""<style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>""", unsafe_allow_html=True)

# Fake Database (Temporary - Refresh par ud jayega)
if 'sales_record' not in st.session_state: st.session_state.sales_record = []
if 'attendance_log' not in st.session_state: st.session_state.attendance_log = []
if 'inventory_db' not in st.session_state: 
    st.session_state.inventory_db = [{"Item": "Sample Product", "Stock": 100}]

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- LOGIN ---
if not st.session_state.logged_in:
    st.title("🛡️ Exion Distribution Portal")
    col1, col2 = st.columns([1,1])
    with col1:
        role = st.selectbox("Select Role", ["Admin", "Salesman"])
        pwd = st.text_input("Password", type="password")
        if st.button("Login"):  # Aapki demand par 'Login' likh diya hai
            if role == "Admin" and pwd == "222":
                st.session_state.logged_in, st.session_state.role = True, "Admin"
                st.rerun()
            elif role == "Salesman" and pwd == "111":
                st.session_state.logged_in, st.session_state.role = True, "Salesman"
                st.rerun()
            else: st.error("Wrong Password")

# --- AUTHENTICATED DASHBOARD ---
else:
    st.sidebar.title(f"User: {st.session_state.role}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if st.session_state.role == "Admin":
        st.title("👨‍💼 Administrator Control Panel")
        
        tab1, tab2, tab3 = st.tabs(["📊 Reports & Map", "📦 Inventory Management", "👥 Attendance"])
        
        with tab1:
            m1, m2 = st.columns(2)
            m1.metric("Live Daily Sales", f"Rs. {sum(d['Amount'] for d in st.session_state.sales_record)}")
            m2.metric("Total Recovery", f"Rs. {sum(d['Recovery'] for d in st.session_state.sales_record)}")
            
            st.subheader("🌍 Kotli Market Tracking")
            m = folium.Map(location=[33.5158, 73.9018], zoom_start=14)
            folium_static(m)
            
            st.subheader("📝 Sales & Recovery Ledger")
            st.table(pd.DataFrame(st.session_state.sales_record))

        with tab2:
            st.subheader("Add New Stock")
            new_item = st.text_input("Item Name")
            new_qty = st.number_input("Quantity", min_value=0)
            if st.button("Add to Inventory"):
                st.session_state.inventory_db.append({"Item": new_item, "Stock": new_qty})
                st.success("Stock Updated!")
            st.table(pd.DataFrame(st.session_state.inventory_db))

    elif st.session_state.role == "Salesman":
        st.title("📱 Field Sales App")
        
        tab_a, tab_b = st.tabs(["📍 Attendance", "📝 Entry & Recovery"])
        
        with tab_a:
            if st.button("Mark Attendance"):
                st.session_state.attendance_log.append({"Time": datetime.datetime.now()})
                st.success("Attendance Marked!")
        
        with tab_b:
            st.subheader("New Sale / Recovery Entry")
            s_shop = st.text_input("Shop Name")
            s_amt = st.number_input("Sale Amount (Credit)", min_value=0)
            s_rec = st.number_input("Recovery Amount (Cash)", min_value=0)
            
            if st.button("Submit Entry"):
                if s_shop:
                    st.session_state.sales_record.append({
                        "Shop": s_shop, "Amount": s_amt, "Recovery": s_rec, 
                        "Time": datetime.datetime.now().strftime("%I:%M %p")
                    })
                    st.balloons()
                    st.success("Data Sent to Admin!")
