import streamlit as st
import pandas as pd
import os
import folium
from streamlit_folium import folium_static
from datetime import datetime

# --- FILE SETUP ---
DB_FILE = "exion_database.xlsx"
SALES_FILE = "exion_sales.xlsx"
LOC_FILE = "salesman_tracking.xlsx"

st.set_page_config(page_title="Exion ERP Pro", layout="wide")

# --- HEADER (Banner & Professional Look) ---
if os.path.exists("main_logo.png"):
    st.image("main_logo.png", use_container_width=True)
else:
    st.title("🚀 Exion Lubricants - Live Status")

st.markdown("---")

# --- DATA LOADING ---
def load_data(file, columns):
    if os.path.exists(file):
        return pd.read_excel(file)
    return pd.DataFrame(columns=columns)

inventory_df = load_data(DB_FILE, ["Product Name", "Purchase Price", "Sale Price", "Stock Qty"])
sales_df = load_data(SALES_FILE, ["Date", "Product", "Qty Sold", "Profit"])
loc_df = load_data(LOC_FILE, ["Name", "Shop", "Lat", "Long", "Time"])

# --- SIDEBAR ---
st.sidebar.title("⚙️ Exion Control")
menu = ["📊 Live Dashboard", "📦 Add Stock", "💰 Record Sale", "🛰️ Salesman Tracking"]
choice = st.sidebar.selectbox("Menu", menu)

# --- 1. DASHBOARD ---
if choice == "📊 Live Dashboard":
    c1, c2, c3 = st.columns(3)
    t_profit = sales_df["Profit"].sum() if not sales_df.empty else 0
    c1.metric("Total Stock", int(inventory_df["Stock Qty"].sum()) if not inventory_df.empty else 0)
    c2.metric("Total Profit", f"Rs. {t_profit:,}")
    c3.metric("Salesmen Online", len(loc_df["Name"].unique()) if not loc_df.empty else 0)
    
    st.write("### 📋 Stock Inventory")
    st.dataframe(inventory_df, use_container_width=True)

# --- 2. ADD STOCK ---
elif choice == "📦 Add Stock":
    st.subheader("📥 Add New Product")
    with st.form("add_form"):
        name = st.text_input("Product Name")
        p_price = st.number_input("Purchase Price", min_value=0)
        s_price = st.number_input("Sale Price", min_value=0)
        qty = st.number_input("Quantity", min_value=0)
        if st.form_submit_button("Save"):
            new_row = pd.DataFrame([[name, p_price, s_price, qty]], columns=inventory_df.columns)
            inventory_df = pd.concat([inventory_df, new_row], ignore_index=True)
            inventory_df.to_excel(DB_FILE, index=False)
            st.success("Saved!")
            st.rerun()

# --- 3. RECORD SALE ---
elif choice == "💰 Record Sale":
    st.subheader("💸 Record Sale")
    if not inventory_df.empty:
        with st.form("sale_form"):
            prod = st.selectbox("Select Product", inventory_df["Product Name"])
            q_sold = st.number_input("Quantity Sold", min_value=1)
            if st.form_submit_button("Submit"):
                idx = inventory_df[inventory_df["Product Name"] == prod].index[0]
                if inventory_df.loc[idx, "Stock Qty"] >= q_sold:
                    inventory_df.loc[idx, "Stock Qty"] -= q_sold
                    inventory_df.to_excel(DB_FILE, index=False)
                    prof = (inventory_df.loc[idx, "Sale Price"] - inventory_df.loc[idx, "Purchase Price"]) * q_sold
                    new_sale = pd.DataFrame([[datetime.now().date(), prod, q_sold, prof]], columns=sales_df.columns)
                    sales_df = pd.concat([sales_df, new_sale], ignore_index=True)
                    sales_df.to_excel(SALES_FILE, index=False)
                    st.success(f"Sold! Profit: Rs. {prof}")
                    st.rerun()
                else: st.error("Out of stock!")

# --- 4. SALESMAN TRACKING (App-Ready System) ---
elif choice == "🛰️ Salesman Tracking":
    st.subheader("🛰️ Live Fleet Tracking")
    
    # Refresh Map every 30 seconds
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=30000, key="maprefresh")

    # Map display
    m = folium.Map(location=[33.5158, 73.9018], zoom_start=13)
    if not loc_df.empty:
        for _, row in loc_df.iterrows():
            folium.Marker([row['Lat'], row['Long']], popup=f"{row['Name']} ({row['Time']})").add_to(m)
    
    folium_static(m)
    st.write("### 📜 Location Logs")
    st.dataframe(loc_df.tail(10), use_container_width=True)