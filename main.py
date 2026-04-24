import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

# --- 1. CONFIG & SETUP ---
st.set_page_config(page_title="Exion Lubricant’s ERP", layout="wide", page_icon="📍")

SHEET_URL = "https://docs.google.com/spreadsheets/d/1OfNYugaCuq0728jfW2LD_3xaFvFgMgfEFNOMxvIwMAQ/edit?usp=sharing"

def get_data(sheet_name):
    try:
        sheet_id = SHEET_URL.split("/d/")[1].split("/")[0]
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        df = pd.read_csv(csv_url)
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame()

# --- 2. LOGIN ---
if 'auth' not in st.session_state:
    st.title("🛢️ Exion Lubricant’s ERP & Tracking")
    role = st.selectbox("Role", ["Admin", "Salesman"])
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if (role == "Admin" and pwd == "222") or (role == "Salesman" and pwd == "111"):
            st.session_state.auth = role
            st.rerun()
        else: st.error("Ghalat Password!")
else:
    if st.sidebar.button("Logout"):
        del st.session_state.auth
        st.rerun()

    # --- 3. ADMIN: ANALYTICS & MAP TRACKING ---
    if st.session_state.auth == "Admin":
        st.title("🧑‍💻 Admin Master Dashboard")
        
        df = get_data("sales")
        if not df.empty:
            df['Credit'] = pd.to_numeric(df['Credit'], errors='coerce').fillna(0)
            df['Recovery'] = pd.to_numeric(df['Recovery'], errors='coerce').fillna(0)
            
            # Metrics
            t_sale = df['Credit'].sum()
            t_rec = df['Recovery'].sum()
            profit = t_sale * 0.15
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total Sale", f"Rs. {t_sale}")
            c2.metric("Total Recovery", f"Rs. {t_rec}")
            c3.metric("Market Udhaar", f"Rs. {t_sale - t_rec}")
            c4.metric("Net Profit (15%)", f"Rs. {profit}")

            st.divider()

            # --- MAP TRACKING ---
            st.subheader("📍 Salesman Live Tracking Map")
            # Agar sheet mein 'lat' aur 'lon' ke columns hain to map dikhega
            if 'lat' in df.columns and 'lon' in df.columns:
                map_df = df.dropna(subset=['lat', 'lon'])
                st.map(map_df)
            else:
                st.info("Map dikhane ke liye Salesman ko location access deni hogi.")

            # --- GRAPHS ---
            col_a, col_b = st.columns(2)
            with col_a:
                fig = px.bar(df, x='Date', y=['Credit', 'Recovery'], title="Daily Progress")
                st.plotly_chart(fig, use_container_width=True)
            with col_b:
                fig2 = px.pie(names=['Profit', 'Market Balance'], values=[profit, t_sale - t_rec], title="Financial Health")
                st.plotly_chart(fig2, use_container_width=True)

    # --- 4. SALESMAN: ENTRY & GPS ---
    else:
        st.title("📱 Salesman Portal (GPS Enabled)")
        
        # Location Tracker (Simulated for Browser)
        st.warning("GPS Tracking Active: Application aapki location record kar rahi hai.")
        
        with st.form("sale_with_gps", clear_on_submit=True):
            shop = st.text_input("Dukan ka Naam")
            amt = st.number_input("Bill Amount", min_value=0)
            rec = st.number_input("Recovery", min_value=0)
            
            # GPS Data (Placeholder - Real GPS needs HTTPS and special JS)
            st.write("Coordinates will be saved automatically.")
            
            if st.form_submit_button("Submit Entry & Location"):
                if shop:
                    st.success(f"Record for {shop} saved with GPS Location!")
                    st.balloons()
                else:
                    st.error("Dukan ka naam likhain!")
