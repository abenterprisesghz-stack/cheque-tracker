import streamlit as st
import pandas as pd
from datetime import datetime
import os

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
    [data-testid="stSidebar"] label {
        color: #5F6368 !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        margin-bottom: 4px;
    }

    /* Main Content & Cards */
    .welcome-header {
        color: #202124;
        font-size: 26px;
        font-weight: 600;
        letter-spacing: -0.5px;
        margin-bottom: 4px;
        margin-top: -10px;
    }
    .welcome-subtext {
        color: #5F6368;
        font-size: 15px;
        margin-bottom: 24px;
    }

    div[data-testid="metric-container"] {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 20px 24px;
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.04);
        border: 1px solid rgba(0,0,0,0.04);
        border-left: 4px solid #1A73E8;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0px 6px 16px rgba(0, 0, 0, 0.08);
    }
    div[data-testid="stMetricValue"] {
        color: #202124 !important;
        font-size: 32px !important;
        font-weight: 600 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #5F6368 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Table & Alerts */
    .table-title {
        font-size: 18px;
        font-weight: 600;
        color: #202124;
        margin-top: 32px;
        margin-bottom: 16px;
        border-bottom: 2px solid #E8EAED;
        padding-bottom: 8px;
    }
    div[data-testid="stDataFrame"] {
        background-color: #FFFFFF;
        border-radius: 12px;
        border: 1px solid rgba(0,0,0,0.05);
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.03);
        padding: 4px;
    }
    .alert-box {
        padding: 16px 24px;
        border-radius: 12px;
        margin-bottom: 24px;
        background-color: #FFF8E1;
        border-left: 6px solid #F9AB00;
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.05);
        display: flex;
        flex-direction: column;
    }
    .alert-box.error {
        background-color: #FCE8E6;
        border-left-color: #D93025;
    }
    .alert-title {
        font-weight: 600;
        font-size: 16px;
        margin-bottom: 4px;
        color: #202124;
    }
    .alert-text {
        color: #3C4043;
        font-size: 14px;
    }
    
    /* Custom Download Button */
    [data-testid="baseButton-secondary"] {
        border-radius: 8px !important;
        background-color: #1A73E8 !important;
        color: #FFFFFF !important;
        border: none !important;
        font-weight: 500 !important;
        padding: 4px 16px !important;
        transition: background-color 0.2s ease, box-shadow 0.2s ease;
    }
    [data-testid="baseButton-secondary"]:hover {
        background-color: #1557B0 !important;
        box-shadow: 0px 2px 6px rgba(26, 115, 232, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar UI ---
with st.sidebar:
    st.markdown("""
        <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 32px; padding-bottom: 16px; border-bottom: 1px solid #F1F3F4;'>
            <div style='background-color: #1A73E8; color: white; width: 44px; height: 44px; border-radius: 12px; display: flex; justify-content: center; align-items: center; font-weight: 600; font-size: 20px; box-shadow: 0px 4px 8px rgba(26, 115, 232, 0.2);'>
                AB
            </div>
            <div>
                <h2 style='margin: 0; font-size: 18px; color: #202124; font-weight: 600;'>Enterprises</h2>
                <div style='color: #5F6368; font-size: 12px; font-weight: 500;'>Cheque Dashboard</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# DATA LOADING LOGIC
# ==========================================
@st.cache_data(ttl=60) 
def load_cheque_data():
    df = pd.read_excel("data.xlsx")
    df.columns = df.columns.str.strip()
    
    if 'Status' in df.columns:
        df['Status'] = df['Status'].fillna('UNUSED')
        df['Status'] = df['Status'].astype(str).str.strip().str.upper()
        df['Status'] = df['Status'].replace(['NAN', 'NONE', 'NULL', ''], 'UNUSED')
    else:
        st.error("System Error: 'Status' column missing in data.xlsx.")
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

# --- Table Coloring Function ---
def color_status(val):
    if val == 'UNUSED':
        return 'background-color: #E6F4EA; color: #137333; font-weight: 600;' # Green
    elif val == 'USE':
        return 'background-color: #FCE8E6; color: #D93025; font-weight: 600;' # Red Highlight
    return ''

# --- UI Controls ---
with st.sidebar:
    display_list = sorted(list(df['Search_Display'].dropna().unique()))
    selected_display = st.selectbox("Select Party Account", ["-- Global Overview --"] + display_list)
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    status_filter = st.radio("Cheque Status Filter", ["All Cheques", "Available (Unused)", "Cleared (Used)"])
    st.caption(f"🕒 Last Synced: {datetime.now().strftime('%I:%M %p, %d %b')}")

# ==========================================
# MAIN ROUTING
# ==========================================
if selected_display != "-- Global Overview --":
    # --- INDIVIDUAL CLIENT VIEW ---
    filtered_df = df[df['Search_Display'] == selected_display]
    final_table = filtered_df.drop(columns=['Search_Display'])
    
    used_count = len(filtered_df[filtered_df['Status'] == 'USE'])
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
                <span class="alert-title">🚨 Action Required: Out of Cheques</span>
                <span class="alert-text">This client has 0 cheques available. Please procure new cheques immediately.</span>
            </div>
        """, unsafe_allow_html=True)
    elif unused_count <= 2:
        st.markdown(f"""
            <div class="alert-box">
                <span class="alert-title">⚠️ Low Inventory Warning</span>
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
        display_df = display_df[display_df['Status'] == 'UNUSED']
    elif status_filter == "Cleared (Used)":
        display_df = display_df[display_df['Status'] == 'USE']

    # Apply styling to the dataframe
    styled_df = display_df.style.map(color_status, subset=['Status'])
    st.dataframe(styled_df, use_container_width=True, hide_index=True, height=400)
    
    st.markdown("<br>", unsafe_allow_html=True)
    d_col1, d_col2 = st.columns([5, 1.2]) 
    with d_col2:
        csv_data = display_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download CSV",
            data=csv_data,
            file_name=f"{selected_display}_Cheques.csv",
            mime="text/csv",
            use_container_width=True
        )

else:
    # --- GLOBAL OVERVIEW (HOME SCREEN) ---
    st.markdown("""
        <div class="welcome-header">Global Inventory Overview</div>
        <div class="welcome-subtext">A macro-level view of all cheques across your organization.</div>
    """, unsafe_allow_html=True)
    
    global_total = len(df)
    global_used = len(df[df['Status'] == 'USE'])
    global_unused = global_total - global_used
    
    g1, g2, g3 = st.columns(3)
    g1.metric("Total Cheques in System", global_total)
    g2.metric("Total Used Cheques", global_used)
    g3.metric("Total Available Cheques", global_unused)
    
    st.markdown('<div class="table-title">🚨 Clients Requiring Attention (Low Stock)</div>', unsafe_allow_html=True)
    
    # Calculate available cheques per client
    inventory_summary = df.groupby('Search_Display')['Status'].apply(
        lambda x: (x == 'UNUSED').sum()
    ).reset_index(name='Available Cheques')
    
    # Filter for clients with <= 2 cheques
    low_stock_clients = inventory_summary[inventory_summary['Available Cheques'] <= 2].sort_values('Available Cheques')
    low_stock_clients = low_stock_clients.rename(columns={'Search_Display': 'Client Name & City'})
    
    if low_stock_clients.empty:
        st.success("✅ All clients have healthy cheque inventory (3 or more available).")
    else:
        st.markdown("""
            <div style='color: #5F6368; font-size: 14px; margin-bottom: 12px;'>
                The following clients have 2 or fewer unused cheques. Please arrange for new cheque books.
            </div>
        """, unsafe_allow_html=True)
        
        # Color code the low stock alerts (0 = Red, 1-2 = Orange)
        styled_low_stock = low_stock_clients.style.map(
            lambda x: 'background-color: #FCE8E6; color: #C5221F; font-weight: bold;' if x == 0 else 'background-color: #FFF8E1; color: #F29900; font-weight: bold;',
            subset=['Available Cheques']
        )
        st.dataframe(styled_low_stock, use_container_width=True, hide_index=True)
        
