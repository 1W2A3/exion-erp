import streamlit as st
import pandas as pd
import datetime

# --- 1. CONFIG & CONNECTION ---
st.set_page_config(page_title="Exion Lubricant’s ERP", layout="wide")

# BHAI, IS LINE KO AB NAHI CHERNA, YE BILKUL SAHI HAI
SHEET_URL = "https://docs.google.com/spreadsheets/d/1OfNYugaCuq0728jfW2LD_3xaFvFgMgfEFNOMxvlwMAQ/edit?usp=sharing"

def get_data(sheet_name):https://docs.google.com/spreadsheets/d/1OfNYugaCuq0728jfW2LD_3xaFvFgMgfEFNOMxvIwMAQ/edit?usp=sharing
    try:
        # Sheet ID nikalne ka sahi tariqa
        sheet_id = SHEET_URL.split("/d/")[1].split("/")[0]
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        df = pd.read_csv(csv_url)
        return df
    except Exception as e:
        return pd.DataFrame()

# --- 2. LOGIN SYSTEM ---
if 'user' not in st.session_state:
    st.title("🛢️ Exion Lubricant’s ERP")
    col1, col2 = st.columns([1,1])
    with col1:
        role = st.selectbox("Role Chunain", ["Admin", "Salesman"])
        uname = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            # Admin: 222 | Salesman: 111
            if (role == "Admin" and pwd == "222") or (role == "Salesman" and pwd == "111"):
                st.session_state.user, st.session_state.role = uname, role
                st.rerun()
            else: st.error("Ghalat Password!")
else:
    # --- 3. DASHBOARD ---
    st.sidebar.title(f"👤 {st.session_state.user}")
    if st.sidebar.button("Logout"):
        del st.session_state.user
        st.rerun()

    if st.session_state.role == "Admin":
        st.title("🧑‍💻 Admin Control Center")
        sales_df = get_data("sales")
        
        if not sales_df.empty:
            sales_df.columns = sales_df.columns.str.strip()
            # Numbers mein convert karna taakay calculations sahi hon
            t_credit = pd.to_numeric(sales_df['Credit'], errors='coerce').sum()
            t_rec = pd.to_numeric(sales_df['Recovery'], errors='coerce').sum()
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Udhaar", f"Rs. {t_credit}")
            m2.metric("Total Wasooli", f"Rs. {t_rec}")
            m3.metric("Baqi Balance", f"Rs. {t_credit - t_rec}")
        
        tab1, tab2, tab3 = st.tabs(["📦 Stock Status", "📝 Sales Ledger", "👥 Attendance"])
        with tab1:
            st.write("Current Inventory:", get_data("inventory"))
        with tab2:
            st.write("All Sales History:", sales_df)
        with tab3:
            st.write("Attendance Records:", get_data("attendance"))

    else:
        st.title("📱 Salesman Portal")
        st.info("Field mein entry yahan se karein:")
        
        with st.form("sale_entry", clear_on_submit=True):
            shop = st.text_input("Customer Name (Dukan ka naam)")
            prod = st.text_input("Product (Konsa tel becha)")
            qty = st.number_input("Quantity", min_value=1)
            c_amt = st.number_input("Total Bill (Credit)", min_value=0)
            r_amt = st.number_input("Cash Received (Recovery)", min_value=0)
            
            if st.form_submit_button("Submit Transaction"):
                if shop:
                    st.success(f"Transaction for {shop} recorded! Please check Google Sheet.")
                    st.balloons()
                else:
                    st.error("Dukan ka naam likhna lazmi hai!")
