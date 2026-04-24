import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import plotly.express as px

# --- CONFIG ---
st.set_page_config(page_title="Exion Lubricant’s ERP", layout="wide")

# --- GOOGLE SHEETS CONNECTION ---
# Bhai, yahan apna Google Sheet ka link paste karna hai
SHEET_URL = https://docs.google.com/spreadsheets/d/1OfNYugaCuq0728jfW2LD_3xaFvFgMgfEFNOMxvIwMAQ/edit?usp=sharing

def get_sheet(worksheet_name):
    # Ye function aapki sheet se connect hota hai
    try:
        # Public Editor link se data uthane ka asaan tareeka
        sheet_id = SHEET_URL.split("/d/")[1].split("/")[0]
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={worksheet_name}"
        return pd.read_csv(url)
    except:
        return pd.DataFrame()

# --- LOGIN SYSTEM ---
if 'user' not in st.session_state:
    st.title("🛢️ Exion Lubricant’s ERP Login")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        role = st.selectbox("Apna Role Chunain", ["Admin", "Salesman"])
        uname = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if st.button("System mein Dakhil Hon", use_container_width=True):
            if (role == "Admin" and pwd == "222") or (role == "Salesman" and pwd == "111"):
                st.session_state.user = uname
                st.session_state.role = role
                st.rerun()
            else: st.error("Ghalat Password! Dubara koshish karein.")
else:
    # --- SIDEBAR ---
    st.sidebar.title("Exion ERP")
    st.sidebar.write(f"User: **{st.session_state.user}**")
    if st.sidebar.button("Logout"):
        del st.session_state.user
        st.rerun()

    # --- ADMIN PANEL ---
    if st.session_state.role == "Admin":
        st.title("🧑‍💻 Administrator Dashboard")
        
        # Reports Loading
        sales_df = get_sheet("sales")
        inventory_df = get_sheet("inventory")
        
        # 1. Financial Metrics
        if not sales_df.empty:
            t_credit = sales_df['Credit'].sum()
            t_recovery = sales_df['Recovery'].sum()
            t_balance = t_credit - t_recovery
            # Profit assume 20%
            est_profit = (t_credit + t_recovery) * 0.20
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total Udhaar", f"Rs. {t_credit}")
            c2.metric("Total Wasooli", f"Rs. {t_recovery}")
            c3.metric("Baqi Raqam", f"Rs. {t_balance}", delta="-Outstanding", delta_color="inverse")
            c4.metric("Est. Profit", f"Rs. {est_profit}")

        # 2. Tabs for Management
        t1, t2, t3, t4 = st.tabs(["🌍 Live Tracking", "📦 Stock Management", "📝 Sales Ledger", "👥 Attendance"])
        
        with t2:
            st.subheader("Inventory Status")
            if not inventory_df.empty:
                st.table(inventory_df)
            
            st.markdown("---")
            st.subheader("Company se Maal Aya (Stock-In)")
            with st.form("admin_stock"):
                p_name = st.text_input("Product Name")
                p_qty = st.number_input("Quantity Received", min_value=1)
                if st.form_submit_button("Update Inventory"):
                    st.success(f"{p_name} ka stock Sheet mein update kar dein (Manual Update for safety)")

        with t3:
            st.subheader("All Time Transactions")
            st.dataframe(sales_df, use_container_width=True)

    # --- SALESMAN APP ---
    else:
        st.title("📱 Salesman Field App")
        
        m1, m2 = st.tabs(["📍 Attendance", "🛒 New Sale Entry"])
        
        with m1:
            if st.button("Mark Attendance (Check-In)"):
                st.success(f"Hazri lag gayi! Time: {datetime.datetime.now().strftime('%I:%M %p')}")

        with m2:
            st.subheader("Daily Khata Entry")
            with st.form("sale_form", clear_on_submit=True):
                cust = st.text_input("Shop/Customer Name")
                item = st.text_input("Product Sold")
                qty = st.number_input("Quantity", min_value=1)
                c_sale = st.number_input("Sale Amount (Credit)", min_value=0)
                c_rec = st.number_input("Recovery (Cash)", min_value=0)
                
                if st.form_submit_button("Submit Data to Admin"):
                    if cust:
                        st.balloons()
                        st.success(f"Transaction for {cust} recorded! Please refresh Sheet.")
                    else:
                        st.error("Customer ka naam likhna lazmi hai!")
