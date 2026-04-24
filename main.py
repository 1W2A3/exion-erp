import streamlit as st
import pandas as pd
from datetime import datetime
import pytz # Sahi time ke liye
import plotly.express as px

# --- 1. SETTINGS & TIMEZONE ---
st.set_page_config(page_title="Exion Master ERP", layout="wide")
pak_tz = pytz.timezone('Asia/Karachi') # Pakistan ka sahi time zone

SHEET_URL = "https://docs.google.com/spreadsheets/d/1OfNYugaCuq0728jfW2LD_3xaFvFgMgfEFNOMxvIwMAQ/edit?usp=sharing"

def get_data(tab_name):
    try:
        sid = SHEET_URL.split("/d/")[1].split("/")[0]
        url = f"https://docs.google.com/spreadsheets/d/{sid}/gviz/tq?tqx=out:csv&sheet={tab_name}"
        df = pd.read_csv(url)
        df.columns = [str(c).strip().lower() for c in df.columns]
        return df
    except: return pd.DataFrame()

# --- 2. LOGIN ---
if 'auth' not in st.session_state:
    st.title("🛢️ Exion Lubricant’s ERP")
    role = st.selectbox("Role", ["Admin", "Salesman"])
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if (role == "Admin" and pwd == "222") or (role == "Salesman" and pwd == "111"):
            st.session_state.auth = role
            st.rerun()
else:
    # --- 3. ADMIN DASHBOARD ---
    if st.session_state.auth == "Admin":
        st.title("🧑‍💻 Admin Master Dashboard")
        
        df_sales = get_data("sales")
        df_attn = get_data("attendance")
        
        now = datetime.now(pak_tz)
        today = now.strftime("%Y-%m-%d")

        # Metrics Calculation
        online_count = 0
        if not df_attn.empty and 'date' in df_attn.columns:
            online_count = len(df_attn[(df_attn['date'] == today) & (df_attn['status'] == 'Check-in')])

        if not df_sales.empty:
            df_sales['credit'] = pd.to_numeric(df_sales['credit'], errors='coerce').fillna(0)
            df_sales['recovery'] = pd.to_numeric(df_sales['recovery'], errors='coerce').fillna(0)
            t_sale, t_rec = df_sales['credit'].sum(), df_sales['recovery'].sum()

            m1, m2, m3, m4, m5 = st.columns(5)
            m1.metric("Total Sale", f"Rs. {t_sale}")
            m2.metric("Recovery", f"Rs. {t_rec}")
            m3.metric("Market Balance", f"Rs. {t_sale - t_rec}")
            m4.metric("Profit (15%)", f"Rs. {t_sale * 0.15}")
            m5.metric("Active Now", f"{online_count} Salesman")

        st.divider()

        # ATTENDANCE RECORD FOR ADMIN
        st.subheader("📋 Salesman Attendance Record")
        if not df_attn.empty:
            st.dataframe(df_attn, use_container_width=True)
        else:
            st.info("Abhi tak koi attendance record nahi mila.")

        st.divider()
        st.subheader("📊 Sales Analysis")
        st.dataframe(df_sales)

    # --- 4. SALESMAN PORTAL ---
    else:
        st.title("📱 Salesman Portal")
        # Pakistan ka current time dikhana
        current_time = datetime.now(pak_tz).strftime("%Y-%m-%d %H:%M:%S")
        st.write(f"⏰ Current Time: **{current_time}**")

        col1, col2 = st.columns(2)
        if col1.button("✅ Check-in", use_container_width=True):
            st.success(f"Checked in at {current_time}")
            # Yahan data sheet mein save honay ka message
        if col2.button("🛑 Check-out", use_container_width=True):
            st.warning(f"Checked out at {current_time}")

        st.divider()
        with st.form("sale_entry"):
            st.subheader("Add New Sale")
            st.text_input("Customer Name")
            st.number_input("Bill Amount", min_value=0)
            if st.form_submit_button("Submit Data"):
                st.balloons()

    if st.sidebar.button("Logout"):
        del st.session_state.auth
        st.rerun()
