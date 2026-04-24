import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

# --- 1. SETTINGS & CONNECTION ---
st.set_page_config(page_title="Exion Lubricant’s ERP", layout="wide")

SHEET_URL = "https://docs.google.com/spreadsheets/d/1OfNYugaCuq0728jfW2LD_3xaFvFgMgfEFNOMxvIwMAQ/edit?usp=sharing"

# Data Read karne ka function
def get_data(sheet_name):
    try:
        sheet_id = SHEET_URL.split("/d/")[1].split("/")[0]
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        return pd.read_csv(csv_url)
    except:
        return pd.DataFrame()

# --- 2. LOGIN SYSTEM ---
if 'auth' not in st.session_state:
    st.title("🛢️ Exion Lubricant’s ERP")
    role = st.selectbox("Apna Role Chunain", ["Admin", "Salesman"])
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if (role == "Admin" and pwd == "222") or (role == "Salesman" and pwd == "111"):
            st.session_state.auth = role
            st.rerun()
        else: st.error("Ghalat Password!")
else:
    # --- 3. ADMIN DASHBOARD ---
    if st.session_state.auth == "Admin":
        st.title("🧑‍💻 Admin Dashboard")
        sales_df = get_data("sales")
        if not sales_df.empty:
            sales_df['Credit'] = pd.to_numeric(sales_df['Credit'], errors='coerce').fillna(0)
            sales_df['Recovery'] = pd.to_numeric(sales_df['Recovery'], errors='coerce').fillna(0)
            
            total_cr = sales_df['Credit'].sum()
            total_rc = sales_df['Recovery'].sum()
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Sales", f"Rs. {total_cr}")
            c2.metric("Total Recovery", f"Rs. {total_rc}")
            c3.metric("Profit (15%)", f"Rs. {total_cr * 0.15}")
            
            # Graph
            fig = px.bar(x=['Credit', 'Recovery'], y=[total_cr, total_rc], color=['Credit', 'Recovery'])
            st.plotly_chart(fig)
            st.dataframe(sales_df)

    # --- 4. SALESMAN PORTAL (RECORD SAVING) ---
    else:
        st.title("📱 Salesman Portal")
        with st.form("sale_entry", clear_on_submit=True):
            shop = st.text_input("Dukan ka Naam")
            item = st.selectbox("Product", ["Exion 4T", "Gear Oil", "Coolant"])
            bill = st.number_input("Total Bill", min_value=0)
            cash = st.number_input("Cash Recovery", min_value=0)
            
            if st.form_submit_button("Data Save Karein"):
                if shop:
                    # Yahan hum Data Save karne ka asmaan logic lagayenge
                    today = datetime.datetime.now().strftime("%Y-%m-%d")
                    st.success(f"Shabaash! {shop} ka record register ho gaya.")
                    st.balloons()
                    st.info(f"Baqi Udhaar: Rs. {bill - cash}")
                else:
                    st.error("Dukan ka naam likhain!")
