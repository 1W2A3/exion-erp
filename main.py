import streamlit as st
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="Exion Lubricant’s ERP", layout="wide")

# LINE 8: ISAY BILKUL NAHI CHERNA
SHEET_URL = "https://docs.google.com/spreadsheets/d/1OfNYugaCuq0728jfW2LD_3xaFvFgMgfEFNOMxvIwMAQ/edit?usp=sharing"

def get_data(sheet_name):
    try:
        sheet_id = SHEET_URL.split(""https://docs.google.com/spreadsheets/d/1OfNYugaCuq0728jfW2LD_3xaFvFgMgEFNOMxvlwMAQ/edit?usp=sharing"")[1].split("/")[0]
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        return pd.read_csv(csv_url)
    except:
        return pd.DataFrame()

# --- APP START ---
st.title("🛢️ Exion Lubricant’s ERP")

if 'logged_in' not in st.session_state:
    role = st.selectbox("Role", ["Admin", "Salesman"])
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if (role == "Admin" and pwd == "222") or (role == "Salesman" and pwd == "111"):
            st.session_state.logged_in = True
            st.session_state.role = role
            st.rerun()
        else:
            st.error("Ghalat Password!")
else:
    st.sidebar.success(f"Logged in: {st.session_state.role}")
    if st.sidebar.button("Logout"):
        del st.session_state.logged_in
        st.rerun()

    if st.session_state.role == "Admin":
        st.header("Admin Dashboard")
        st.info("Loading Data from Google Sheets...")
        # Sales Data View
        df = get_data("sales")
        if not df.empty:
            st.dataframe(df)
        else:
            st.warning("Sheet khali hai ya connect nahi ho rahi.")
    else:
        st.header("Salesman App")
        with st.form("sale_entry"):
            cust = st.text_input("Customer Name")
            prod = st.text_input("Product")
            amt = st.number_input("Amount", min_value=0)
            if st.form_submit_button("Submit"):
                st.success(f"Entry for {cust} Done!")
                st.balloons()
