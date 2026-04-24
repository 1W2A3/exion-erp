import streamlit as st
import pandas as pd
import datetime
from streamlit_folium import folium_static
import folium
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Exion ERP | Kotli", layout="wide")

# 2. Permanent Data Logic (Session based)
if 'sales_ledger' not in st.session_state: st.session_state.sales_ledger = []
if 'inventory' not in st.session_state: st.session_state.inventory = {"Product A": 100}
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- 3. LOGIN INTERFACE ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>🛡️ Exion Distribution Portal</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        role = st.selectbox("Select User Role", ["Admin", "Salesman"])
        pwd = st.text_input("Enter Password", type="password")
        if st.button("Login", use_container_width=True):
            if role == "Admin" and pwd == "222":
                st.session_state.logged_in, st.session_state.role = True, "Admin"
                st.rerun()
            elif role == "Salesman" and pwd == "111":
                st.session_state.logged_in, st.session_state.role = True, "Salesman"
                st.rerun()
            else:
                st.error("Invalid Credentials!")

# --- 4. DASHBOARD SYSTEM ---
else:
    st.sidebar.title("Exion ERP")
    st.sidebar.write(f"Logged as: **{st.session_state.role}**")
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    # --- ADMIN VIEW ---
    if st.session_state.role == "Admin":
        st.title("👨‍💼 Administrator Control Center")
        
        # Calculation for Profit/Loss & Recovery
        t_credit = sum(d['Credit'] for d in st.session_state.sales_ledger)
        t_recovery = sum(d['Recovery'] for d in st.session_state.sales_ledger)
        # Assuming 20% average margin for Profit calculation
        est_profit = (t_credit + t_recovery) * 0.20

        # Metrics Row
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Credit", f"Rs. {t_credit}")
        m2.metric("Total Recovery", f"Rs. {t_recovery}")
        m3.metric("Estimated Profit", f"Rs. {est_profit}")
        m4.metric("Net Status", "Stable", delta="100%")

        # Graph Section
        st.markdown("### 📊 Business Analytics")
        if st.session_state.sales_ledger:
            df_graph = pd.DataFrame([
                {"Category": "Credit Sales", "Amount": t_credit},
                {"Category": "Cash Recovery", "Amount": t_recovery}
            ])
            fig = px.bar(df_graph, x="Category", y="Amount", color="Category", height=350)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Waiting for Salesman entries to generate graph...")

        # Tabs for Admin Functions
        tab1, tab2, tab3 = st.tabs(["🌍 Market Map", "📦 Inventory Control", "📝 Full Ledger"])
        
        with tab1:
            st.subheader("Kotli Live Fleet Map")
            m = folium.Map(location=[33.5158, 73.9018], zoom_start=14)
            folium.Marker([33.5158, 73.9018], popup="Exion Office").add_to(m)
            folium_static(m)

        with tab2:
            st.subheader("Manage Product Stock")
            with st.form("inv_management", clear_on_submit=True):
                i_name = st.text_input("Product Name")
                i_qty = st.number_input("Quantity to Add", min_value=1)
                if st.form_submit_button("Update Inventory Table"):
                    if i_name.strip(): # Error Fix: Prevent empty line error
                        st.session_state.inventory[i_name] = st.session_state.inventory.get(i_name, 0) + i_qty
                        st.success(f"Stock added for {i_name}")
                    else:
                        st.error("Please enter a valid Product Name")
            
            # Clean display of inventory
            clean_inv = {k: v for k, v in st.session_state.inventory.items() if k.strip()}
            if clean_inv:
                st.table(pd.DataFrame(list(clean_inv.items()), columns=['Product Name', 'Current Stock']))

        with tab3:
            st.subheader("Daily Sales & Recovery Record")
            if st.session_state.sales_ledger:
                st.table(pd.DataFrame(st.session_state.sales_ledger))
            else:
                st.write("No transactions recorded today.")

    # --- SALESMAN VIEW ---
    elif st.session_state.role == "Salesman":
        st.title("📱 Field Sales Application")
        
        with st.form("salesman_entry", clear_on_submit=True):
            st.subheader("Submit Daily Entry")
            s_name = st.text_input("Shop Name")
            s_credit = st.number_input("New Sale (Credit)", min_value=0)
            s_cash = st.number_input("Recovery (Cash)", min_value=0)
            
            if st.form_submit_button("Submit Data to Admin", use_container_width=True):
                if s_name:
                    st.session_state.sales_ledger.append({
                        "Shop": s_name, 
                        "Credit": s_credit, 
                        "Recovery": s_cash, 
                        "Time": datetime.datetime.now().strftime("%I:%M %p")
                    })
                    st.balloons()
                    st.success(f"Data for {s_name} sent successfully!")
                else:
                    st.error("Shop Name is required!")
