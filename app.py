import streamlit as st
import pandas as pd
from datetime import datetime

# --- Page Setup ---
st.set_page_config(
    page_title="AB ENTERPRISES | Cheque Tracking Portal", 
    page_icon="🏢", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Premium Corporate CSS (Ultra-Smooth UI) ---
st.markdown("""
    <style>
    /* Import modern sleek font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global App Background & Font */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }
    
    .stApp {
        background-color: #f9fafb; /* Very soft neutral gray */
    }

    /* Hide only default Streamlit footer */
    footer {visibility: hidden;}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #f3f4f6;
    }

    /* Modern Corporate Header */
    .corporate-header {
        background: #ffffff;
        padding: 24px 32px;
        border-radius: 16px;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.02);
        border: 1px solid #f3f4f6;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        gap: 24px;
        transition: all 0.3s ease;
    }
    
    .header-icon {
        background: linear-gradient(135deg, #1e3a8a, #3b82f6);
        border-radius: 14px;
        padding: 16px;
        font-size: 32px;
        color: white;
        box-shadow: 0 8px 16px rgba(59, 130, 246, 0.2);
        display: flex;
        align-items: center;
        justify-content: center;
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
        margin: 6px 0 0 0;
        font-size: 14px;
        font-weight: 400;
        letter-spacing: 0.2px;
    }

    /* KPI Metric Cards - Smoother Hover Effects */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.02);
        border: 1px solid #f3f4f6;
        border-radius: 16px;
        padding: 24px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.05);
        border-color: #e2e8f0;
    }
    div[data-testid="stMetricValue"] {
        color: #0f172a !important; 
        font-size: 36px !important;
        font-weight: 700 !important;
        letter-spacing: -1px;
    }
    div[data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 8px;
    }

    /* Dataframe Container */
    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
        background: #ffffff;
    }

    /* Alert Styling - Softer edges & colors */
    .alert-box {
        padding: 20px 24px;
        border-radius: 12px;
        margin-bottom: 24px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .alert-critical {
        background-color: #fef2f2;
        border-left: 5px solid #ef4444;
        box-shadow: 0 2px 10px rgba(239, 68, 68, 0.05);
    }
    .alert-warning {
        background-color: #fffbeb;
        border-left: 5px solid #f59e0b;
        box-shadow: 0 2px 10px rgba(245, 158, 11, 0.05);
    }
    .alert-title {
        margin: 0;
        font-size: 16px;
        font-weight: 600;
        letter-spacing: -0.2px;
    }
    .alert-text {
        margin: 6px 0 0 0;
        font-size: 14px;
        line-height: 1.5;
    }

    /* Standardizing headings */
    h3, h4 {
        color: #0f172a !important;
        font-weight: 600 !important;
        letter-spacing: -0.3px;
    }
    
    /* Input and Select box styling */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        border-radius: 8px !important;
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
        <div class="header-icon">🏢</div>
        <div>
            <h1 class="company-title">AB Enterprises</h1>
            <p class="company-sub">
                Cheque Tracking & Management Portal • C-44, Site No. 3, Meerut Road, Ghaziabad
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
    st.caption("v2.2.0 | Authorized Personnel Only")

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
                <p class="alert-title" style="color: #b91c1c;">🛑 CRITICAL: Cheque Inventory Exhausted</p>
                <p class="alert-text" style="color: #991b1b;">
                    <b>{selected_display}</b> currently has <b>0</b> cheques available. Operations requiring physical cheques are paused. Please procure a new chequebook immediately.
                </p>
            </div>
        """, unsafe_allow_html=True)
    elif unused_count <= 2:
        st.markdown(f"""
            <div class="alert-box alert-warning">
                <p class="alert-title" style="color: #b45309;">⚠️ WARNING: Low Inventory Threshold</p>
                <p class="alert-text" style="color: #92400e;">
                    <b>{selected_display}</b> has only <b>{unused_count}</b> unused cheque(s) remaining. Please arrange for new cheques to avoid operational delays.
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
        st.markdown("### 📋 Cheque Ledger")
    with col2:
        search_term = st.text_input("🔍 Quick Search", placeholder="Cheque No, Bank, etc...")

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
            label="⬇️ Export Data (CSV)",
            data=csv_data,
            file_name=f"{selected_display}_Cheque_Log_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True,
            type="primary"
        )
else:
    # Empty State Configuration
    st.markdown("""
        <div style="text-align: center; margin-top: 120px; color: #64748b; padding: 40px; background: #ffffff; border-radius: 16px; border: 1px dashed #cbd5e1; max-width: 600px; margin-left: auto; margin-right: auto;">
            <div style="font-size: 48px; margin-bottom: 16px;">📂</div>
            <h2 style="color: #0f172a; font-weight: 600; font-size: 22px; margin-bottom: 8px;">Welcome to the Cheque Tracking Portal</h2>
            <p style="font-size: 15px; line-height: 1.6;">Please select a Client from the sidebar navigation on the left to view their specific cheque inventory and usage history.</p>
        </div>
    """, unsafe_allow_html=True)
