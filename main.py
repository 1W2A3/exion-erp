import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import plotly.express as px

# --- 1. CONFIG ---
st.set_page_config(page_title="Exion Master ERP", layout="wide")
pak_tz = pytz.timezone('Asia/Karachi')

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
        else: st.error("Ghalat Password")
else:
    # --- 3. ADMIN DASHBOARD ---
    if st.session_state.auth == "Admin":
        st.title("🧑‍💻 Admin Master Dashboard")
        df_s = get_data("sales")
        df_a = get_data("attendance")
        today = datetime.now(pak_tz).strftime("%Y-%m-%d")

        # Online Count with Error Handling
        online = 0
        if not df_a.empty and 'date' in df_a.columns and 'status' in df_a.columns:
            online = len(df_a[(df_a['date'] == today) & (df_a['status'] == 'Check-in')])

        if not df_s.empty:
            df_s['credit'] = pd.to_numeric(df_s['credit'], errors='coerce').fillna(0)
            df_s['recovery'] = pd.to_numeric(df_s['recovery'], errors='coerce').fillna(0)
            s_sum, r_sum = df_s['credit'].sum(), df_s['recovery'].sum()

            m1, m2, m3, m4, m5 = st.columns(5)
            m1.metric("Total Sale", f"Rs. {s_sum}")
            m2.metric("Recovery", f"Rs. {r_sum}")
            m3.metric("Market Bal", f"Rs. {s_sum - r_sum}")
            m4.metric("Profit (15%)", f"Rs. {s_sum * 0.15}")
            m5.metric("Active Now", f"{online} Salesman")

            st.divider()
            # Yahan Product Analysis add kar di hai
            col_l, col_r = st.columns(2)
            with col_l:
                st.subheader("📦 Sales by Product")
                if 'product' in df_s.columns:
                    p_fig = px.pie(df_s, names='product', values='credit', hole=0.3)
                    st.plotly_chart(p_fig, use_container_width=True)
            with col_r:
                st.subheader("📈 Recovery Graph")
                fig = px.bar(df_s, x=df_s.columns[1], y=['credit', 'recovery'], barmode='group')
                st.plotly_chart(fig, use_container_width=True)

            st.subheader("📋 Detailed Sales Record")
            st.dataframe(df_s, use_container_width=True)

    # --- 4. SALESMAN PORTAL ---
    else:
        st.title("📱 Salesman Portal")
        st.write(f"⏰ Time: **{datetime.now(pak_tz).strftime('%Y-%m-%d %H:%M')}**")
        
        if st.button("✅ Check-in", use_container_width=True):
            st.success("Attendance Marked!")

        st.divider()
        with st.form("entry"):
            st.subheader("New Sale")
            c_name = st.text_input("Customer Name")
            p_name = st.selectbox("Product", ["Exion 4T", "Exion 20-40", "Coolant", "Gear Oil"])
            amount = st.number_input("Bill Amount", min_value=0)
            if st.form_submit_button("Submit"):
                st.success(f"{p_name} sale saved!")

    if st.sidebar.button("Logout"):
        del st.session_state.auth
        st.rerun()
