import streamlit as st
import pandas as pd
import datetime
from streamlit_folium import folium_static
import folium

st.set_page_config(page_title="Exion ERP | Distribution", layout="wide")

# Persistent Data Setup
if 'sales_ledger' not in st.session_state: st.session_state.sales_ledger = []
if 'inventory' not in st.session_state: st.session_state.inventory = {"Product A": 100, "Product B": 50}

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- LOGIN ---
if not st.session_state.logged_in:
    st.title("🛡️ Exion Distribution Portal")
    role = st.selectbox("Select User Role", ["Admin", "Salesman"])
    pwd = st.text_input("Enter Password", type="password")
    if st.button("Login"):
        if role == "Admin" and pwd == "222":
            st.session_state.logged_in, st.session_state.role = True, "Admin"
            st.rerun()
        elif role == "Salesman" and pwd == "111":
            st.session_state.logged_in, st.session_state.role = True, "Salesman"
            st.rerun()
        else: st.error("Incorrect Password")

# --- DASHBOARD ---
else:
    st.sidebar.title(f"User: {st.session_state.role}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if st.session_state.role == "Admin":
        st.title("👨‍💼 Administrator Control Center")
        
        t1, t2, t3 = st.tabs(["Dashboard & Map", "Inventory Control", "Sales Ledger"])
        
        with t1:
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Credit Sales", f"Rs. {sum(d['Credit'] for d in st.session_state.sales_ledger)}")
            m2.metric("Total Recovery (Cash)", f"Rs. {sum(d['Recovery'] for d in st.session_state.sales_ledger)}")
            m3.metric("Live Staff", "1")
            
            st.subheader("🌍 Field Tracking - Kotli")
            m = folium.Map(location=[33.5158, 73.9018], zoom_start=14)
            folium_static(m)

        with t2:
            st.subheader("Manage Stock")
            item_name = st.text_input("Item Name")
            item_qty = st.number_input("Add Quantity", min_value=0)
            if st.button("Update Inventory"):
                st.session_state.inventory[item_name] = st.session_state.inventory.get(item_name, 0) + item_qty
                st.success("Stock Added!")
            st.write("Current Stock:", st.session_state.inventory)

        with t3:
            st.subheader("Daily Sales & Recovery Report")
            if st.session_state.sales_ledger:
                st.table(pd.DataFrame(st.session_state.sales_ledger))

    elif st.session_state.role == "Salesman":
        st.title("📱 Field Sales App")
        
        with st.form("entry_form"):
            st.subheader("New Entry (Sale + Recovery)")
            shop = st.text_input("Shop Name")
            credit_sale = st.number_input("New Credit Sale (Amount)", min_value=0)
            cash_rec = st.number_input("Cash Recovery (Amount)", min_value=0)
            submit = st.form_submit_button("Submit Entry to Admin")
            
            if submit:
                if shop:
                    st.session_state.sales_ledger.append({
                        "Shop": shop, "Credit": credit_sale, "Recovery": cash_rec, 
                        "Time": datetime.datetime.now().strftime("%I:%M %p")
                    })
                    st.success("Record Sent Successfully!")
