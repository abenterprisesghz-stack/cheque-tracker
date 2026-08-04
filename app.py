import streamlit as st
import pandas as pd
from datetime import datetime

# --- Page Setup ---
st.set_page_config(
    page_title="Dashboard | AB Enterprises", 
    page_icon="📱", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Android OS / Material Design CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif !important;
    }
    
    .stApp {
        background-color: #F8F9FA; 
    }

    footer {visibility: hidden;}
    header {background-color: transparent !important;}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: none;
        box-shadow: 2px 0px 12px rgba(0, 0, 0, 0.08);
        padding-top: 1rem;
    }
    [data-testid="stSidebar"] .stMarkdown p, 
    [data-testid="stSidebar"] .stMarkdown h1, 
    [data-testid="stSidebar"] .stMarkdown h2, 
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #202124 !important;
    }
    [data-testid="stSidebar"] label {
        color: #5F6368 !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        margin-bottom: 4px;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label p,
    [data-testid="stSidebar"] div[role="radiogroup"] label div {
        color: #202124 !important;
        font-weight: 400 !important;
        font-size: 14px !important;
    }

    /* Main Content & Cards */
    .welcome-header {
        color: #202124;
        font-size: 26px;
        font-weight: 500;
        letter-spacing: -0.5px;
        margin-bottom: 4px;
        margin-top: -10px;
    }
    .welcome-subtext {
        color: #5F6368;
        font-size: 14px;
        margin-bottom: 24px;
    }

    div[data-testid="metric-container"] {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 20px 24px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(0,0,0,0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0px 6px 16px rgba(0, 0, 0, 0.1);
    }
    div[data-testid="stMetricValue"] {
        color: #1A73E8 !important;
        font-size: 32px !important;
        font-weight: 500 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #5F6368 !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Table & Alerts */
    .table-title {
        font-size: 18px;
        font-weight: 500;
        color: #202124;
        margin-top: 24px;
        margin-bottom: 16px;
    }
    div[data-testid="stDataFrame"] {
        background-color: #FFFFFF;
        border-radius: 16px;
        border: none;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
        padding: 8px;
    }
    .alert-box {
        padding: 16px 24px;
        border-radius: 12px;
        margin-bottom: 24px;
        background-color: #FFFFFF;
        border-left: 6px solid #F9AB00;
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.1);
        display: flex;
        flex-direction: column;
    }
    .alert-box.error {
        border-left-color: #D93025;
    }
    .alert-title {
        font-weight: 500;
        font-size: 16px;
        margin-bottom: 4px;
    }
    .alert-text {
        color: #5F6368;
        font-size: 14px;
    }
    
    /* Custom Download Button */
    [data-testid="baseButton-secondary"] {
        border-radius: 20px !important;
        background-color: #E8F0FE !important;
        color: #1A73E8 !important;
        border: none !important;
        font-weight: 500 !important;
        transition: background-color 0.2s ease;
    }
    [data-testid="baseButton-secondary"]:hover {
        background-color: #D2E3FC !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar UI (Android Drawer Style) ---
with st.sidebar:
    st.markdown("""
        <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 32px; padding-bottom: 16px; border-bottom: 1px solid #F1F3F4;'>
            <div style='background-color: #1A73E8; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-weight: 500; font-size: 18px;'>
                AB
            </div>
            <div>
                <h2 style='margin: 0; font-size: 18px; color: #202124; font-weight: 500;'>Enterprises</h2>
                <div style='color: #5F6368; font-size: 12px;'>Dashboard App</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Global Navigation
    app_mode = st.radio(
        "Select Module",
        ["Cheque Dashboard", "Sales & Invoices Dashboard"]
    )
    st.markdown("<hr style='border-color: #F1F3F4;'>", unsafe_allow_html=True)

# ==========================================
# MODULE 1: CHEQUE DASHBOARD
# ==========================================
if app_mode == "Cheque Dashboard":
    @st.cache_data(ttl=60) 
    def load_cheque_data():
        df = pd.read_excel("data.xlsx")
        df.columns = df.columns.str.strip()
        
        if 'Status' in df.columns:
            df['Status'] = df['Status'].fillna('UNUSED').replace('', 'UNUSED')
        else:
            st.error("System Error: 'Status' column missing.")
            st.stop()

        if 'CITY' in df.columns:
            df['CITY'] = df['CITY'].fillna('Unknown')
            df['Search_Display'] = df['Party Name'].astype(str) + " (" + df['CITY'].astype(str) + ")"
        else:
            df['Search_Display'] = df['Party Name'].astype(str)

        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].dt.strftime('%d-%m-%Y')
            elif 'date' in col.lower():
                try:
                    df[col] = pd.to_datetime(df[col]).dt.strftime('%d-%m-%Y')
                except:
                    pass 
        return df

    try:
        df = load_cheque_data()
    except FileNotFoundError:
        st.error("System Error: 'data.xlsx' file not found in the directory.")
        st.stop()

    with st.sidebar:
        display_list = sorted(list(df['Search_Display'].dropna().unique()))
        selected_display = st.selectbox("Select Party Account", ["-- Select a Client --"] + display_list)
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        status_filter = st.radio("Cheque Status Filter", ["All Cheques", "Available (Unused)", "Cleared (Used)"])
        st.caption(f"🕒 Last Synced: {datetime.now().strftime('%I:%M %p, %d %b')}")

    if selected_display != "-- Select a Client --":
        filtered_df = df[df['Search_Display'] == selected_display]
        final_table = filtered_df.drop(columns=['Search_Display'])
        
        used_count = len(filtered_df[filtered_df['Status'].str.upper() == 'USE'])
        total_count = len(filtered_df)
        unused_count = total_count - used_count
        
        party_name = selected_display.split('(')[0].strip()
        st.markdown(f"""
            <div class="welcome-header">{party_name}</div>
            <div class="welcome-subtext">Client overview and cheque inventory details.</div>
        """, unsafe_allow_html=True)
        
        if unused_count == 0:
            st.markdown(f"""
                <div class="alert-box error">
                    <span class="alert-title" style="color: #D93025;">Action Required: Out of Cheques</span>
                    <span class="alert-text">This client has 0 cheques available. Please procure new cheques immediately.</span>
                </div>
            """, unsafe_allow_html=True)
        elif unused_count <= 2:
            st.markdown(f"""
                <div class="alert-box">
                    <span class="alert-title" style="color: #F9AB00;">Low Inventory Warning</span>
                    <span class="alert-text">Only <b>{unused_count}</b> unused cheque(s) remaining for this account.</span>
                </div>
            """, unsafe_allow_html=True)

        m1, m2, m3 = st.columns(3)
        m1.metric("Total Logged", total_count)
        m2.metric("Used / Cleared", used_count)
        m3.metric("Available", unused_count)
        
        st.markdown('<div class="table-title">Recent Activity</div>', unsafe_allow_html=True)
        
        display_df = final_table.copy()
        if status_filter == "Available (Unused)":
            display_df = display_df[display_df['Status'].str.upper() == 'UNUSED']
        elif status_filter == "Cleared (Used)":
            display_df = display_df[display_df['Status'].str.upper() == 'USE']

        st.dataframe(display_df, use_container_width=True, hide_index=True, height=400)
        
        st.markdown("<br>", unsafe_allow_html=True)
        d_col1, d_col2 = st.columns([5, 1.2]) 
        with d_col2:
            csv_data = display_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=f"{selected_display}_Cheques.csv",
                mime="text/csv",
                use_container_width=True
            )
    else:
        st.markdown("""
            <div style="margin-top: 60px; padding: 40px; background-color: #FFFFFF; border-radius: 16px; box-shadow: 0px 4px 12px rgba(0,0,0,0.05); text-align: center;">
                <div style="background-color: #E8F0FE; width: 64px; height: 64px; border-radius: 50%; display: flex; justify-content: center; align-items: center; margin: 0 auto 20px auto; font-size: 28px;">
                    📝
                </div>
                <div class="welcome-header">Cheque Inventory</div>
                <div class="welcome-subtext">Open the sidebar menu and select a client to view their cheque details.</div>
            </div>
        """, unsafe_allow_html=True)


# ==========================================
# MODULE 2: SALES & INVOICES DASHBOARD
# ==========================================
elif app_mode == "Sales & Invoices Dashboard":
    with st.sidebar:
        st.markdown("<div class='table-title' style='margin-top:0;'>Upload Daily Data</div>", unsafe_allow_html=True)
        # Added a file uploader so you can upload the file directly on the web app!
        uploaded_file = st.file_uploader("Upload Sales Excel", type=["xlsx", "xls"])
        
    @st.cache_data(ttl=60)
    def load_sales_data(file):
        df = pd.read_excel(file)
        # Format the Date column if it exists
        if 'Doc.Date' in df.columns:
            df['Doc.Date'] = pd.to_datetime(df['Doc.Date']).dt.strftime('%d-%m-%Y')
        return df

    sales_df = None
    try:
        if uploaded_file is not None:
            sales_df = load_sales_data(uploaded_file)
        else:
            # Fallback to backend folder file
            sales_df = load_sales_data("Pfizer Anchor PLUS 29-July-26.xlsx")
            st.sidebar.caption("✅ Auto-loaded: 'Pfizer Anchor PLUS 29-July-26.xlsx' from server.")
    except FileNotFoundError:
        st.error("No Sales Data Found. Please upload your daily Excel file in the sidebar.")
        
    if sales_df is not None and not sales_df.empty:
        # Get Unique Divisions
        if 'Division Name' in sales_df.columns:
            divisions = ["All Divisions"] + sorted(sales_df['Division Name'].dropna().unique().tolist())
        else:
            divisions = ["All Divisions"]
            
        with st.sidebar:
            selected_division = st.selectbox("Select Division", divisions)
            st.caption(f"🕒 Last Synced: {datetime.now().strftime('%I:%M %p, %d %b')}")

        # Filter Logic
        if selected_division != "All Divisions":
            filtered_sales = sales_df[sales_df['Division Name'] == selected_division]
        else:
            filtered_sales = sales_df
            
        # Calculate KPIs based on the specific columns in your file
        total_amount = filtered_sales['Net Amount'].sum() if 'Net Amount' in filtered_sales.columns else 0
        total_qty = filtered_sales['Net Qty'].sum() if 'Net Qty' in filtered_sales.columns else 0
        invoice_count = filtered_sales['Customer Invoice No'].nunique() if 'Customer Invoice No' in filtered_sales.columns else 0

        # Header UI
        st.markdown(f"""
            <div class="welcome-header">Sales & Invoices Overview</div>
            <div class="welcome-subtext">Viewing data for: <b>{selected_division}</b></div>
        """, unsafe_allow_html=True)

        # Metric Cards
        s1, s2, s3 = st.columns(3)
        s1.metric("Total Net Amount", f"₹ {total_amount:,.2f}")
        s2.metric("Total Net Quantity", f"{total_qty:,.0f}")
        s3.metric("Unique Invoices", invoice_count)
        
        st.markdown('<div class="table-title">Invoice Ledger</div>', unsafe_allow_html=True)
        
        # Display Table
        st.dataframe(filtered_sales, use_container_width=True, hide_index=True, height=400)
        
        # Download Filtered Data
        st.markdown("<br>", unsafe_allow_html=True)
        d_col1, d_col2 = st.columns([5, 1.2]) 
        with d_col2:
            csv_sales = filtered_sales.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv_sales,
                file_name=f"Sales_{selected_division}.csv",
                mime="text/csv",
                use_container_width=True
            )
