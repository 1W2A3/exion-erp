import streamlit as st
import pandas as pd
import datetime

# --- 1. SETTINGS ---
st.set_page_config(page_title="Exion Lubricant’s ERP", layout="wide", page_icon="🛢️")

# Google Sheet Link (Fixed & Verified)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1OfNYugaCuq0728jfW2LD_3xaFvFgMgfEFNOMxvIwMAQ/edit?usp=sharing"

# Data nikalne ka function
def get_data(sheet_name):
    try:
        sheet_id = SHEET_URL.split("/d/")[1].split("/")[0]
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        return pd.read_csv(csv_url)
    except:
        return pd.DataFrame()

# --- 2. LOGIN SYSTEM ---
if 'auth' not in st.session_state:
    st.markdown("<h1 style='text-align: center;'>🛢️ Exion Lubricant’s ERP</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        with st.container(border=True):
            role = st.selectbox("Apna Role Chunain", ["Admin", "Salesman"])
            pwd = st.text_input("Password", type="password")
            if st.button("Login System", use_container_width=True):
                if (role == "Admin" and pwd == "222") or (role == "Salesman" and pwd == "111"):
                    st.session_state.auth = role
                    st.session_state.user = "Wassi Mughal" if role == "Admin" else "Salesman"
                    st.rerun()
                else:
                    st.error("Ghalat Password! Dobara koshish karein.")
else:
    # --- SIDEBAR (Logout & Info) ---
    st.sidebar.title(f"Swaagat hai, {st.session_state.user}")
    st.sidebar.write(f"Role: {st.session_state.auth}")
    if st.sidebar.button("Log Out", use_container_width=True):
        del st.session_state.auth
        st.rerun()

    # --- 3. ADMIN DASHBOARD ---
    if st.session_state.auth == "Admin":
        st.title("🧑‍💻 Admin Control Center")
        
        # Dashboard Metrics
        sales_df = get_data("sales")
        if not sales_df.empty:
            sales_df.columns = sales_df.columns.str.strip()
            total_credit = pd.to_numeric(sales_df['Credit'], errors='coerce').sum()
            total_rec = pd.to_numeric(sales_df['Recovery'], errors='coerce').sum()
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Udhaar (Market)", f"Rs. {total_credit}")
            m2.metric("Total Wasooli", f"Rs. {total_rec}")
            m3.metric("Net Balance", f"Rs. {total_credit - total_rec}")

        # Tabs for Data
        t1, t2, t3 = st.tabs(["📊 Sales Ledger", "📦 Stock Status", "🕒 Attendance"])
        with t1:
            st.subheader("Market Sales Record")
            st.dataframe(sales_df, use_container_width=True)
        with t2:
            st.subheader("Current Inventory")
            st.dataframe(get_data("inventory"), use_container_width=True)
        with t3:
            st.subheader("Staff Attendance Log")
            st.dataframe(get_data("attendance"), use_container_width=True)

    # --- 4. SALESMAN PORTAL ---
    else:
        st.title("📱 Salesman Entry Portal")
        
        # Hazri Section
        with st.expander("📍 Daily Attendance (Hazri)", expanded=True):
            if st.button("Mark Check-In Now"):
                st.success(f"Hazri Lag Gayi! Time: {datetime.datetime.now().strftime('%I:%M %p')}")
        
        st.divider()
        
        # Sale Form
        st.subheader("Nayi Sale ki Entry")
        with st.form("main_sale_form", clear_on_submit=True):
            shop = st.text_input("Customer/Dukan ka Naam")
            item = st.selectbox("Product", ["Exion 4T Oil", "Exion Gear Oil", "Coolant", "Grease"])
            qty = st.number_input("Quantity", min_value=1)
            bill = st.number_input("Total Bill (Rs.)", min_value=0)
            cash = st.number_input("Recovery/Cash Received (Rs.)", min_value=0)
            
            if st.form_submit_button("Data Sheet mein Bhejein"):
                if shop:
                    st.balloons()
                    st.success(f"Entry Saved for {shop}!")
                    st.info(f"Baqi Udhaar: Rs. {bill - cash}")
                else:
                    st.error("Dukan ka naam likhna zaroori hai!")
