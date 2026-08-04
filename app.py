import streamlit as st
import pandas as pd
from datetime import datetime

# --- Page Setup ---
st.set_page_config(
    page_title="Cheque Dashboard | AB Enterprises", 
    page_icon="💼", 
    layout="wide"
)

# --- Enterprise/Legacy Dashboard CSS (Matching Reference Image) ---
st.markdown("""
    <style>
    /* Classic System Fonts for Enterprise Look */
    html, body, [class*="css"] {
        font-family: Arial, Tahoma, Verdana, sans-serif !important;
    }
    
    /* Main Background (Solid White) */
    .stApp {
        background-color: #FFFFFF; 
    }

    /* Hide Default Header/Footer */
    footer {visibility: hidden;}
    header {background-color: transparent !important;}
    
    /* Remove default top padding */
    .block-container {
        padding-top: 1rem !important;
    }

    /* -----------------------------------
       TOP NAVIGATION BAR STYLING
       ----------------------------------- */
    .top-header {
        background-color: #3b86c4; /* Specific blue from the image */
        color: white;
        padding: 12px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 3px solid #285e8e;
        margin-bottom: 15px;
        margin-top: -30px;
    }
    .top-header h2 {
        margin: 0;
        font-size: 18px;
        font-weight: bold;
        color: #FFFFFF;
    }
    .top-header-sub {
        font-size: 11px;
        color: #E0E0E0;
    }
    .top-header-date {
        font-size: 12px;
        text-align: right;
    }
    .top-header-date span {
        color: #FFCCCC; /* Red/pink emphasis like the image date */
        font-weight: bold;
    }

    /* Override Radio Button Font Size */
    div[role="radiogroup"] label p {
        font-size: 14px !important;
    }

    /* -----------------------------------
       MAIN CONTENT & CARDS STYLING
       ----------------------------------- */
    .welcome-header {
        color: #C00000; 
        font-size: 14px;
        font-weight: bold;
        margin-bottom: 2px;
        text-transform: uppercase;
    }
    .welcome-subtext {
        color: #333333;
        font-size: 12px;
        margin-bottom: 24px;
    }

    /* Metric Cards (Flat, Square, Functional) */
    div[data-testid="metric-container"] {
        background-color: #F5F5F5;
        border-radius: 0px; 
        padding: 10px 15px;
        border: 1px solid #CCCCCC;
        box-shadow: none; 
    }
    div[data-testid="stMetricValue"] {
        color: #000000 !important; 
        font-size: 24px !important;
        font-weight: bold !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #003366 !important;
        font-size: 12px !important;
        font-weight: bold !important;
    }

    /* Data Table Section Styling */
    .table-title {
        font-size: 14px;
        font-weight: bold;
        color: #003366;
        margin-top: 10px;
        margin-bottom: 10px;
        border-bottom: 1px solid #003366;
        padding-bottom: 3px;
    }
    
    /* Streamlit Dataframe Box styling */
    div[data-testid="stDataFrame"] {
        background-color: #FFFFFF;
        border-radius: 0px;
        border: 1px solid #999999;
    }

    /* Alerts (Flat and Standard) */
    .alert-box {
        padding: 10px 15px;
        border-radius: 0px;
        margin-bottom: 20px;
        background-color: #FFF9E6;
        border: 1px solid #E6C200;
        font-size: 13px;
    }
    .alert-box.error {
        background-color: #FFEEEE;
        border: 1px solid #CC0000;
    }
    </style>
""", unsafe_allow_html=True)

# --- Core Logic & Data Loading ---
@st.cache_data(ttl=60) 
def load_data():
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
    df = load_data()
except FileNotFoundError:
    st.error("System Error: 'data.xlsx' database file not found in the directory.")
    st.stop()


# --- Top Horizontal Header & Navigation ---
st.markdown(f"""
    <div class="top-header">
        <div>
            <h2>A B ENTERPRISES</h2>
            <div class="top-header-sub">System Administration Panel</div>
        </div>
        <div class="top-header-date">
            Hi There! <br>
            <span>{datetime.now().strftime('%d-%b-%Y %H:%M:%S')}</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Layout for controls (Horizontal Dropdowns & Radios)
ctrl_col1, ctrl_col2 = st.columns([1, 1])

with ctrl_col1:
    display_list = sorted(list(df['Search_Display'].dropna().unique()))
    selected_display = st.selectbox(
        "Select Party Account", 
        ["-- Select a Client --"] + display_list
    )

with ctrl_col2:
    st.markdown("<div style='margin-top: 4px;'></div>", unsafe_allow_html=True)
    status_filter = st.radio(
        "Cheque Status Filter",
        ["All Cheques", "Available (Unused)", "Cleared (Used)"],
        horizontal=True
    )

st.markdown("<hr style='margin-top: 5px; margin-bottom: 20px; border-color: #CCCCCC;'>", unsafe_allow_html=True)


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
        <div class="welcome-header">Welcome {selected_display.split('(')[0].strip()}</div>
        <div class="welcome-subtext">Inventory status and account cheque history.</div>
    """, unsafe_allow_html=True)
    
    # --- Alerts Engine ---
    if unused_count == 0:
        st.markdown(f"""
            <div class="alert-box error">
                <strong style="color: #CC0000;">SYSTEM ALERT: Out of Cheques</strong><br>
                <span style="color: #333333;">This account currently holds 0 unused cheques. Manual intervention required.</span>
            </div>
        """, unsafe_allow_html=True)
    elif unused_count <= 2:
        st.markdown(f"""
            <div class="alert-box">
                <strong style="color: #B38F00;">WARNING: Low Inventory</strong><br>
                <span style="color: #333333;">Only <b>{unused_count}</b> unused cheque(s) remaining in the system.</span>
            </div>
        """, unsafe_allow_html=True)

    # --- KPI Metric Cards ---
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Cheques Logged", total_count)
    m2.metric("Used / Cleared Cheques", used_count)
    m3.metric("Available (Unused)", unused_count)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- Table Section ---
    st.markdown('<div class="table-title">Account Cheque Register</div>', unsafe_allow_html=True)
    
    # Apply Filters
    display_df = final_table.copy()
    if status_filter == "Available (Unused)":
        display_df = display_df[display_df['Status'].str.upper() == 'UNUSED']
    elif status_filter == "Cleared (Used)":
        display_df = display_df[display_df['Status'].str.upper() == 'USE']

    # Render Auto-fit Table
    st.dataframe(
        display_df, 
        use_container_width=True, 
        hide_index=True,
        height=350 
    )
    
    # Download Button at bottom right
    st.markdown("<br>", unsafe_allow_html=True)
    d_col1, d_col2 = st.columns([5, 1])
    with d_col2:
        csv_data = display_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Export Data (CSV)",
            data=csv_data,
            file_name=f"{selected_display}_Cheques.csv",
            mime="text/csv",
            use_container_width=True
        )

else:
    # --- Empty State (When app opens) ---
    st.markdown("""
        <div style="margin-top: 20px; padding: 20px; background-color: #F8F8F8; border: 1px solid #DDDDDD;">
            <div class="welcome-header" style="color: #003366;">A B ENTERPRISES SYSTEM DASHBOARD</div>
            <div class="welcome-subtext" style="margin-bottom: 0;">Please utilize the dropdown menu above to select a Party Account and view the inventory records.</div>
        </div>
    """, unsafe_allow_html=True)
