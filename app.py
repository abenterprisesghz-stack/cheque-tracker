import streamlit as st
import pandas as pd
from datetime import datetime

# --- Page Setup ---
st.set_page_config(
    page_title="Cheque Dashboard | AB Enterprises", 
    page_icon="💼", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Premium Dashboard CSS (Matching Reference Image) ---
st.markdown("""
    <style>
    /* Import modern sleek font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Main Background (Light Gray/Off-white) */
    .stApp {
        background-color: #F8F9FB; 
    }

    /* Hide Default Header/Footer */
    footer {visibility: hidden;}
    header {background-color: transparent !important;}

    /* -----------------------------------
       SIDEBAR STYLING (Dark Blue Theme)
       ----------------------------------- */
    [data-testid="stSidebar"] {
        background-color: #2C3E50 !important; /* Dark Professional Blue */
        border-right: none;
        padding-top: 1rem;
    }
    /* Sidebar Text Elements */
    [data-testid="stSidebar"] .stMarkdown p, 
    [data-testid="stSidebar"] .stMarkdown h1, 
    [data-testid="stSidebar"] .stMarkdown h2, 
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #FFFFFF !important;
    }
    /* Sidebar Selectbox Label Fix */
    [data-testid="stSidebar"] label {
        color: #A6B4CE !important;
        font-weight: 500 !important;
    }

    /* -----------------------------------
       MAIN CONTENT & CARDS STYLING
       ----------------------------------- */
    /* Welcome Header Text */
    .welcome-header {
        color: #111827;
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 4px;
        margin-top: -20px;
    }
    .welcome-subtext {
        color: #6B7280;
        font-size: 15px;
        margin-bottom: 24px;
    }

    /* Metric Cards (White, Rounded, Soft Shadow) */
    div[data-testid="metric-container"] {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 20px 24px;
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.04);
        border: 1px solid #F3F4F6;
        transition: transform 0.2s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.08);
    }
    div[data-testid="stMetricValue"] {
        color: #1F2937 !important; 
        font-size: 32px !important;
        font-weight: 700 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #6B7280 !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }

    /* Data Table Section Styling */
    .table-title {
        font-size: 18px;
        font-weight: 700;
        color: #111827;
        margin-top: 20px;
        margin-bottom: 15px;
    }
    
    /* Streamlit Dataframe Box styling */
    div[data-testid="stDataFrame"] {
        background-color: #FFFFFF;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.04);
        padding: 10px;
    }

    /* Alerts */
    .alert-box {
        padding: 16px 20px;
        border-radius: 8px;
        margin-bottom: 24px;
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.04);
    }
    </style>
""", unsafe_allow_html=True)

# --- Core Logic & Data Loading ---
@st.cache_data(ttl=60) 
def load_data():
    df = pd.read_excel("data.xlsx")
    df.columns = df.columns.str.strip()
    
    # 1. Clean Status
    if 'Status' in df.columns:
        df['Status'] = df['Status'].fillna('UNUSED').replace('', 'UNUSED')
    else:
        st.error("System Error: 'Status' column missing.")
        st.stop()

    # 2. Search Display Setup
    if 'CITY' in df.columns:
        df['CITY'] = df['CITY'].fillna('Unknown')
        df['Search_Display'] = df['Party Name'].astype(str) + " (" + df['CITY'].astype(str) + ")"
    else:
        df['Search_Display'] = df['Party Name'].astype(str)

    # 3. FIX: Date Formatting (Remove Time, keep only Date)
    for col in df.columns:
        # Check if the column is a datetime type
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.strftime('%d-%m-%Y')
        # Also check if column name contains 'date' but was read as string/object
        elif 'date' in col.lower():
            try:
                # Convert to datetime then format to DD-MM-YYYY
                df[col] = pd.to_datetime(df[col]).dt.strftime('%d-%m-%Y')
            except:
                pass # If it fails to convert, leave it as is
                
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("System Error: 'data.xlsx' database file not found in the directory.")
    st.stop()

# --- Sidebar UI (Dark Theme as per Image) ---
with st.sidebar:
    st.markdown("""
        <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 30px;'>
            <div style='background: #3B82F6; color: white; padding: 8px 12px; border-radius: 8px; font-weight: bold; font-size: 20px;'>AB</div>
            <h2 style='margin: 0; font-size: 20px;'>Enterprises</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Dashboard Menu")
    
    display_list = sorted(list(df['Search_Display'].dropna().unique()))
    selected_display = st.selectbox(
        "Search & Select Party", 
        ["-- Select a Client --"] + display_list
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    status_filter = st.radio(
        "Filter Cheque Status",
        ["All Cheques", "Available (Unused)", "Cleared (Used)"]
    )
    
    st.markdown("<br><hr style='border-color: #4B5563;'>", unsafe_allow_html=True)
    st.caption(f"📅 Last Sync: {datetime.now().strftime('%d-%b-%Y')}")

# --- Main Dashboard UI ---
if selected_display != "-- Select a Client --":
    
    # Filter Data
    filtered_df = df[df['Search_Display'] == selected_display]
    final_table = filtered_df.drop(columns=['Search_Display'])
    
    used_count = len(filtered_df[filtered_df['Status'].str.upper() == 'USE'])
    total_count = len(filtered_df)
    unused_count = total_count - used_count
    
    # --- Top Welcome Header ---
    st.markdown(f"""
        <div class="welcome-header">Client Overview: {selected_display.split('(')[0].strip()}</div>
        <div class="welcome-subtext">Here is a summary of the cheque inventory and recent activity.</div>
    """, unsafe_allow_html=True)
    
    # --- Alerts Engine ---
    if unused_count == 0:
        st.markdown(f"""
            <div class="alert-box" style="border-left: 4px solid #EF4444;">
                <strong style="color: #DC2626; font-size: 16px;">🛑 Action Required: Out of Cheques</strong><br>
                <span style="color: #4B5563; font-size: 14px;">This client has 0 cheques available. Please procure new cheques immediately.</span>
            </div>
        """, unsafe_allow_html=True)
    elif unused_count <= 2:
        st.markdown(f"""
            <div class="alert-box" style="border-left: 4px solid #F59E0b;">
                <strong style="color: #D97706; font-size: 16px;">⚠️ Low Inventory Warning</strong><br>
                <span style="color: #4B5563; font-size: 14px;">Only <b>{unused_count}</b> unused cheque(s) remaining.</span>
            </div>
        """, unsafe_allow_html=True)

    # --- KPI Metric Cards (Like the Image) ---
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Logged", total_count)
    m2.metric("Used / Cleared", used_count)
    m3.metric("Available (Unused)", unused_count)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- Table Section ---
    st.markdown('<div class="table-title">Recent Cheque Logs</div>', unsafe_allow_html=True)
    
    # Apply Filters
    display_df = final_table.copy()
    if status_filter == "Available (Unused)":
        display_df = display_df[display_df['Status'].str.upper() == 'UNUSED']
    elif status_filter == "Cleared (Used)":
        display_df = display_df[display_df['Status'].str.upper() == 'USE']

    # Render Auto-fit Table
    # use_container_width=True ensures ALL COLUMNS AUTOFIT to the screen width
    st.dataframe(
        display_df, 
        use_container_width=True, 
        hide_index=True,
        height=400 # Fixes height to make scrolling smooth like a professional table
    )
    
    # Download Button at bottom right
    st.markdown("<br>", unsafe_allow_html=True)
    d_col1, d_col2 = st.columns([5, 1])
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
    # --- Empty State (When app opens) ---
    st.markdown("""
        <div style="margin-top: 100px; padding: 40px; background-color: #FFFFFF; border-radius: 12px; box-shadow: 0px 4px 12px rgba(0,0,0,0.03); border: 1px solid #E5E7EB;">
            <div class="welcome-header">Welcome to the Dashboard</div>
            <div class="welcome-subtext" style="margin-bottom: 0;">Please open the sidebar on the left and search for a Client to view their cheque summary and details.</div>
        </div>
    """, unsafe_allow_html=True)
