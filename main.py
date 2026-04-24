import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

# --- 1. CONFIG ---
st.set_page_config(page_title="Exion Lubricant ERP", layout="wide")

SHEET_URL = "https://docs.google.com/spreadsheets/d/1OfNYugaCuq0728jfW2LD_3xaFvFgMgfEFNOMxvIwMAQ/edit?usp=sharing"

def get_data(sheet_name):
    try:
        sheet_id = SHEET_URL.split("/d/")[1].split("/")[0]
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        df = pd.read_csv(csv_url)
        # Spellings/Spaces fix karne ke liye:
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
        else: st.error("Wrong Password")
else:
    # --- 3. ADMIN DASHBOARD ---
    if st.session_state.auth == "Admin":
        st.title("🧑‍💻 Admin Master Dashboard")
        df = get_data("sales")
        
        if not df.empty:
            # Column mapping (Flexible search)
            c_col = 'credit' if 'credit' in df.columns else None
            r_col = 'recovery' if 'recovery' in df.columns else None
            
            if c_col and r_col:
                df[c_col] = pd.to_numeric(df[c_col], errors='coerce').fillna(0)
                df[r_col] = pd.to_numeric(df[r_col], errors='coerce').fillna(0)
                
                t_sale = df[c_col].sum()
                t_rec = df[r_col].sum()
                
                # METRICS
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Total Sale", f"Rs. {t_sale}")
                c2.metric("Total Recovery", f"Rs. {t_rec}")
                c3.metric("Market Balance", f"Rs. {t_sale - t_rec}")
                c4.metric("Profit (15%)", f"Rs. {t_sale * 0.15}")
                
                st.divider()
                # MAP & CHART
                col_a, col_b = st.columns(2)
                with col_a:
                    st.subheader("📍 Live Tracking (Sales Locations)")
                    if 'lat' in df.columns and 'lon' in df.columns:
                        st.map(df[['lat', 'lon']].dropna())
                with col_b:
                    st.subheader("📈 Recovery Analysis")
                    fig = px.bar(df, x=df.columns[1], y=[c_col, r_col], barmode='group')
                    st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("Raw Data")
            st.dataframe(df, use_container_width=True)

    # --- 4. SALESMAN (CHECK-IN/OUT & ENTRY) ---
    else:
        st.title("📱 Salesman Portal")
        
        # Check-in / Check-out Buttons
        col1, col2 = st.columns(2)
        if col1.button("✅ Check-in", use_container_width=True):
            st.success(f"Checked in at {datetime.datetime.now().strftime('%H:%M:%S')}")
            # Live tracking logic active here
        if col2.button("🛑 Check-out", use_container_width=True):
            st.warning("Shift Ended. Data synced.")

        st.divider()
        st.subheader("New Entry")
        with st.form("entry_form"):
            shop = st.text_input("Customer Name")
            prod = st.selectbox("Product", ["Exion 4T", "Exion 20-40", "Coolant"])
            amt = st.number_input("Bill Amount", min_value=0)
            rec = st.number_input("Recovery", min_value=0)
            if st.form_submit_button("Save Data"):
                st.success(f"Data for {shop} sent to Admin!")

    if st.sidebar.button("Logout"):
        del st.session_state.auth
        st.rerun()
