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

    /* -----------------------------------
       SIDEBAR STYLING (GoApptiv Blue Theme)
       ----------------------------------- */
    [data-testid="stSidebar"] {
        background-color: #3b86c4 !important; /* Specific blue from the image */
        border-right: 2px solid #285e8e;
        padding-top: 1rem;
    }
    
    /* Sidebar Text Elements */
    [data-testid="stSidebar"] .stMarkdown p, 
    [data-testid="stSidebar"] .stMarkdown h1, 
    [data-testid="stSidebar"] .stMarkdown h2, 
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #FFFFFF !important;
    }
    
    /* Sidebar Top-level Labels */
    [data-testid="stSidebar"] label {
        color: #E0E0E0 !important;
        font-weight: bold !important;
        font-size: 13px !important;
    }
    
    /* Force Radio Button Options to be White */
    [data-testid="stSidebar"] div[role="radiogroup"] label p,
    [data-testid="stSidebar"] div[role="radiogroup"] label div {
        color: #FFFFFF !important;
        font-weight: normal !important;
        font-size: 13px !important;
    }

    /* -----------------------------------
       MAIN CONTENT & CARDS STYLING
       ----------------------------------- */
    /* Welcome Header Text (Styled like the red text in image) */
    .welcome-header {
        color: #C00000; /* Red emphasis like "Welcome A B ENTERPRISES" */
        font-size: 14px;
        font-weight: bold;
        margin-bottom: 2px;
        margin-top: -20px;
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
        border-radius: 0px; /* Removed rounded corners */
        padding: 10px 15px;
        border: 1px solid #CCCCCC;
        box-shadow: none; /* Removed shadows */
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
        margin-top: 20px;
        margin-bottom: 10px;
        border-bottom: 1px solid #003366;
        padding-bottom: 3px;
    }
    
    /* Streamlit Dataframe Box styling */
    div[data-testid="stDataFrame"] {
        background-color: #FFFFFF;
        border-radius: 0px;
        border: 1px solid #999999;
        box-shadow: none;
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

# --- Sidebar UI (Legacy Blue Theme as per Image) ---
with st.sidebar:
    # Classic simple text header
    st.markdown("""
        <div style='margin-bottom: 20px; border-bottom: 1px solid #FFFFFF; padding-bottom: 10px;'>
            <h2 style='margin: 0; font-size: 18px; font-weight: bold;'>A B ENTERPRISES</h2>
            <span style='font-size: 11px;'>System Administration</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='font-size: 14px; font-weight: bold; margin-bottom: 10px;'>Main Menu</div>", unsafe_allow_html=True)
    
    display_list = sorted(list(df['Search_Display'].dropna().unique()))
    selected_display = st.selectbox(
        "Select Party Account", 
        ["-- Select a Client --"] + display_list
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    status_filter = st.radio(
        "Cheque Status Filter",
        ["All Cheques", "Available (Unused)", "Cleared (Used)"]
    )
    
    st.markdown("<br><hr style='border-color: #619cd0;'>", unsafe_allow_html=True)
    # Date stylized like the image "PharmaNET Date 04-Aug-2026"
    st.markdown(f"""
        <div style="font-size: 11px;">
            System Date <span style="color: #FFCCCC; font-weight: bold;">{datetime.now().strftime('%d-%b-%Y %H:%M:%S')}</span>
        </div>
    """, unsafe_allow_html=True)

# --- Main Dashboard UI ---
if selected_display != "-- Select a Client --":
    
    # Filter Data
    filtered_df = df[df['Search_Display'] == selected_display]
    final_table = filtered_df.drop(columns=['Search_Display'])
    
    used_count = len(filtered_df[filtered_df['Status'].str.upper() == 'USE'])
    total_count = len(filtered_df)
    unused_count = total_count - used_count
    
    # --- Top Welcome Header (Styled matching the red text in reference) ---
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
        height=400 
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
        <div style="margin-top: 50px; padding: 20px; background-color: #F8F8F8; border: 1px solid #DDDDDD;">
            <div class="welcome-header" style="color: #003366;">A B ENTERPRISES SYSTEM DASHBOARD</div>
            <div class="welcome-subtext" style="margin-bottom: 0;">Please utilize the left navigation menu to select a Party Account and view the inventory records.</div>
        </div>
    """, unsafe_allow_html=True)
