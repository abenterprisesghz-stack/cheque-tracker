import streamlit as st
import pandas as pd
from datetime import datetime

# --- Page Setup ---
st.set_page_config(
    page_title="Cheque Management System | AB Enterprises", 
    page_icon="🏢", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Modern Corporate CSS (SaaS UI) ---
st.markdown("""
    <style>
    /* Global App Background */
    .stApp {
        background-color: #f8fafc;
        font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
    }

    /* Hide only default Streamlit footer (Header kept visible for sidebar toggle button) */
    footer {visibility: hidden;}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }

    /* Modern Corporate Header */
    .corporate-header {
        background: #ffffff;
        padding: 24px 32px;
        border-radius: 12px;
        border-top: 5px solid #1e40af; /* Corporate Navy Blue */
        box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 1px 2px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        gap: 20px;
    }
    
    .company-title {
        color: #0f172a;
        margin: 0;
        font-weight: 700;
        letter-spacing: -0.5px;
        font-size: 28px;
    }
    
    .company-sub {
        color: #64748b;
        margin: 4px 0 0 0;
        font-size: 13px;
        font-weight: 500;
    }

    /* KPI Metric Cards */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 20px;
        transition: all 0.2s ease;
    }
    div[data-testid="metric-container"]:hover {
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transform: translateY(-2px);
        border-color: #cbd5e1;
    }
    div[data-testid="stMetricValue"] {
        color: #1e293b !important; 
        font-size: 32px !important;
        font-weight: 700 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Dataframe Container */
    div[data-testid="stDataFrame"] {
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }

    /* Alert Styling - Clean & Professional */
    .alert-box {
        padding: 16px 20px;
        border-radius: 8px;
        margin-bottom: 24px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .alert-critical {
        background-color: #fef2f2;
        border-left: 4px solid #dc2626;
        border-right: 1px solid #fee2e2;
        border-top: 1px solid #fee2e2;
        border-bottom: 1px solid #fee2e2;
    }
    .alert-warning {
        background-color: #fffbeb;
        border-left: 4px solid #d97706;
        border-right: 1px solid #fef3c7;
        border-top: 1px solid #fef3c7;
        border-bottom: 1px solid #fef3c7;
    }
    .alert-title {
        margin: 0;
        font-size: 16px;
        font-weight: 700;
    }
    .alert-text {
        margin: 4px 0 0 0;
        font-size: 14px;
    }

    /* Section Titles */
    h3, h4 {
        color: #1e293b !important;
        font-weight: 600 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Core Logic & Data Loading ---
@st.cache_data(ttl=60) 
def load_data():
    df = pd.read_excel("data.xlsx")
    df.columns = df.columns.str.strip()
    
    # Validation & Cleaning
    if 'Status' in df.columns:
        df['Status'] = df['Status'].fillna('UNUSED').replace('', 'UNUSED')
    else:
        st.error("System Error: 'Status' column missing from data source.")
        st.stop()

    if 'CITY' in df.columns:
        df['CITY'] = df['CITY'].fillna('Unknown')
        df['Search_Display'] = df['Party Name'].astype(str) + " (" + df['CITY'].astype(str) + ")"
    else:
        df['Search_Display'] = df['Party Name'].astype(str)
        
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("System Error: 'data.xlsx' database file not found in the directory.")
    st.stop()

# --- Application UI Layout ---

# 1. Main Header
st.markdown("""
    <div class="corporate-header">
        <div style="background-color: #1e40af; border-radius: 8px; padding: 12px; display: flex; align-items: center; justify-content: center;">
            <span style="font-size: 28px; color: white;">🏢</span>
        </div>
        <div>
            <h1 class="company-title">AB Enterprises</h1>
            <p class="company-sub">
                Cheque Inventory & Financial Tracking System • C-44, Site No. 3, Meerut Road, Ghaziabad
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)

# 2. Sidebar Controls
with st.sidebar:
    st.markdown("### 🎛️ Navigation & Filters")
    st.markdown("---")
    
    display_list = sorted(list(df['Search_Display'].dropna().unique()))
    selected_display = st.selectbox(
        "Select Party / Client", 
        ["-- Select a Client --"] + display_list
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Advanced Filters**")
    status_filter = st.radio(
        "Filter by Cheque Status",
        ["All Records", "Unused (Available)", "Used (Cleared)"]
    )
    
    st.markdown("---")
    st.caption(f"System Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    st.caption("v2.1.0 | Authorized Personnel Only")

# 3. Main Dashboard Area
if selected_display != "-- Select a Client --":
    
    # Filter Data
    filtered_df = df[df['Search_Display'] == selected_display]
    final_table = filtered_df.drop(columns=['Search_Display'])
    
    used_count = len(filtered_df[filtered_df['Status'].str.upper() == 'USE'])
    total_count = len(filtered_df)
    unused_count = total_count - used_count
    
    # --- Alerts Engine ---
    if unused_count == 0:
        st.markdown(f"""
            <div class="alert-box alert-critical">
                <p class="alert-title" style="color: #991b1b;">🛑 CRITICAL: Cheque Inventory Exhausted</p>
                <p class="alert-text" style="color: #7f1d1d;">
                    <b>{selected_display}</b> currently has <b>0</b> cheques available. Billing operations are suspended. Please procure new cheques immediately to resume operations.
                </p>
            </div>
        """, unsafe_allow_html=True)
    elif unused_count <= 2:
        st.markdown(f"""
            <div class="alert-box alert-warning">
                <p class="alert-title" style="color: #92400e;">⚠️ WARNING: Low Inventory Threshold</p>
                <p class="alert-text" style="color: #b45309;">
                    <b>{selected_display}</b> has only <b>{unused_count}</b> unused cheque(s) remaining. Please arrange for a new chequebook to avoid operational delays.
                </p>
            </div>
        """, unsafe_allow_html=True)

    # --- KPI Dashboard ---
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Cheques Logged", total_count)
    m2.metric("Used Cheques", used_count)
    m3.metric("Available Inventory", unused_count)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- Data View Section ---
    col1, col2 = st.columns([3, 1], gap="medium")
    with col1:
        st.markdown("### 📋 Client Ledger")
    with col2:
        search_term = st.text_input("🔍 Quick Search", placeholder="Ref No, Amount, etc...")

    # Apply Sidebar & Search Filters
    display_df = final_table.copy()

    if status_filter == "Unused (Available)":
        display_df = display_df[display_df['Status'].str.upper() == 'UNUSED']
    elif status_filter == "Used (Cleared)":
        display_df = display_df[display_df['Status'].str.upper() == 'USE']

    if search_term:
        mask = display_df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
        display_df = display_df[mask]

    # Render Table & Export
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # Export Button alignment
    csv_data = display_df.to_csv(index=False).encode('utf-8')
    d_col1, d_col2 = st.columns([4, 1])
    with d_col2:
        st.download_button(
            label="⬇️ Export to CSV",
            data=csv_data,
            file_name=f"{selected_display}_Audit_Report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True,
            type="primary"
        )
else:
    # Empty State Configuration
    st.markdown("""
        <div style="text-align: center; margin-top: 100px; color: #64748b;">
            <h2 style="color: #94a3b8; font-weight: 500;">Welcome to the Financial Portal</h2>
            <p>Please select a Client from the sidebar navigation on the left to view their cheque inventory and ledger.</p>
        </div>
    """, unsafe_allow_html=True)
