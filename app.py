import streamlit as st
import pandas as pd
from datetime import datetime

# --- Page Setup ---
st.set_page_config(
    page_title="GoApptiv | Online PharmaNET", 
    page_icon="💊", 
    layout="wide",
    initial_sidebar_state="collapsed" # Hide sidebar completely to match image
)

# --- Dynamic Dates for the UI ---
current_date = datetime.now().strftime('%d-%b-%Y')
current_time = datetime.now().strftime('%d-%b-%Y %H:%M:%S')

# --- Custom CSS for Legacy UI Styling ---
st.markdown("""
    <style>
    /* Reset app padding and hide default header */
    .stApp { background-color: #FFFFFF; font-family: Arial, sans-serif; }
    header { visibility: hidden; }
    .block-container { padding-top: 0rem !important; padding-left: 0rem !important; padding-right: 0rem !important; max-width: 100% !important;}
    
    /* Top Brand Bar */
    .brand-bar {
        background-color: #3984C6;
        height: 65px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 20px;
        color: white;
        border-bottom: 2px solid #205C90;
    }
    
    /* Simulate GoApptiv Logo Area */
    .logo-left {
        background-color: white;
        color: #BDBDBD;
        padding: 5px 15px;
        font-size: 28px;
        font-weight: 300;
        letter-spacing: 1px;
        display: flex;
        align-items: center;
        gap: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    }
    .logo-left strong { color: #F5A623; font-size: 32px; font-weight: bold; font-family: "Times New Roman", Times, serif; }
    
    /* Simulate PharmaNET Logo Area */
    .logo-right { text-align: right; line-height: 1.1; }
    .logo-right-top { font-size: 22px; font-style: italic; font-weight: bold; margin-bottom: -5px; }
    .logo-right-bottom { font-size: 26px; font-weight: 900; color: #1B2956; text-shadow: 1px 1px white; }
    
    /* Navigation Menu Bar */
    .nav-bar {
        background: linear-gradient(to bottom, #5DADE2, #2E86C1);
        height: 28px;
        display: flex;
        align-items: center;
        padding: 0 15px;
        font-size: 13px;
        font-weight: bold;
        color: white;
    }
    .nav-links span { margin-right: 20px; cursor: pointer; text-shadow: 1px 1px 1px rgba(0,0,0,0.5); }
    .nav-links span:hover { text-decoration: underline; }
    .nav-search { margin-left: auto; display: flex; align-items: center; gap: 5px; }
    .nav-search input { height: 18px; width: 60px; font-size: 11px; }
    .nav-search button { height: 20px; font-size: 11px; padding: 0 5px; cursor: pointer; }
    
    /* User Info & Icon Tray Section */
    .info-tray-container {
        display: flex;
        justify-content: space-between;
        padding: 5px 15px;
        border-bottom: 1px solid #D0D0D0;
    }
    .user-info { font-size: 12px; color: #333; line-height: 1.6; }
    .user-info span.red-text { color: #CC0000; font-weight: bold; }
    
    /* Horizontal Icons Menu */
    .icon-tray { display: flex; gap: 20px; margin-top: 5px; }
    .icon-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        font-size: 11px;
        color: #333;
        cursor: pointer;
        width: 65px;
        text-align: center;
        font-weight: bold;
    }
    .icon-img { font-size: 26px; margin-bottom: 2px; }
    .icon-item:hover { opacity: 0.7; }
    
    /* Streamlit Selectbox Overrides to match legacy look */
    div[data-testid="stSelectbox"] > div {
        min-height: 25px !important;
    }
    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        font-size: 13px !important;
        border-radius: 2px !important;
        border: 1px solid #A0A0A0 !important;
    }
    /* GO Button Override */
    div[data-testid="stButton"] button {
        border-radius: 0px !important;
        border: 1px solid #000080 !important;
        color: #000080 !important;
        font-weight: bold !important;
        padding: 0px 20px !important;
        height: 32px !important;
        margin-top: 2px;
    }
    
    /* Padding for the filter row container */
    .filter-container { padding: 10px 15px; border-bottom: 1px solid #A0A0A0; }
    </style>
""", unsafe_allow_html=True)

# --- 1. Render Top Header, Nav, and Info Tray (HTML/CSS) ---
header_html = f"""
<div class="brand-bar">
    <div class="logo-left">
        <strong>A</strong> GoApptiv
    </div>
    <div class="logo-right">
        <div class="logo-right-top">Online</div>
        <div class="logo-right-bottom">💊 PharmaNET</div>
    </div>
</div>

<div class="nav-bar">
    <div class="nav-links">
        <span><u>Setup</u></span>
        <span>Orders</span>
        <span>Inventory</span>
        <span>Accounts</span>
        <span>Supply Chain</span>
        <span>Reports</span>
        <span>Utilities</span>
    </div>
    <div class="nav-search">
        <input type="text" />
        <button>Go</button>
        <span style="margin-left: 15px; cursor: pointer; text-shadow: 1px 1px 1px rgba(0,0,0,0.5);">Logout</span>
    </div>
</div>

<div class="info-tray-container">
    <div class="user-info">
        Welcome <span class="red-text">A B ENTERPRISES</span><br>
        PharmaNET Date <span class="red-text">{current_date}</span><br>
        Login Time <span class="red-text">{current_time}</span>
    </div>
    
    <div class="icon-tray">
        <div class="icon-item"><div class="icon-img">📈</div>Collection<br>Tracker</div>
        <div class="icon-item"><div class="icon-img">🛒</div>Stock<br>Movement</div>
        <div class="icon-item"><div class="icon-img">✔️</div>Order<br>Approval</div>
        <div class="icon-item"><div class="icon-img">📝</div>Memo<br>Approval</div>
        <div class="icon-item"><div class="icon-img">📦</div>Material<br>Status</div>
        <div class="icon-item" style="background:#E0E0E0; border:1px solid #CCC; border-radius:3px;"><div class="icon-img">👤</div>Customer<br>Status</div>
        <div class="icon-item"><div class="icon-img">💵</div>Collection</div>
        <div class="icon-item"><div class="icon-img">📊</div>Sales<br>Trend</div>
        <div class="icon-item"><div class="icon-img">📉</div>Work<br>Tracker</div>
    </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# --- 2. Render Filter Section (Native Streamlit Components) ---
# We use a container to apply the proper margins and spacing
st.markdown('<div class="filter-container">', unsafe_allow_html=True)

# Define exact column widths to match the inline look of the image
col1, col2, col3, col4, col5 = st.columns([2.5, 2.5, 2.5, 2.5, 1])

with col1:
    enterprise = st.selectbox("Enterprise", ["A B ENTERPRISES [617]"], label_visibility="collapsed")
with col2:
    customer = st.selectbox("Customer", ["All Customer"], label_visibility="collapsed")
with col3:
    division = st.selectbox("Division", ["All Division"], label_visibility="collapsed")
with col4:
    date_type = st.selectbox("Date Type", ["OutStanding As On Date"], label_visibility="collapsed")
with col5:
    go_clicked = st.button("GO")

st.markdown('</div>', unsafe_allow_html=True)

# --- 3. Main Data Area (Placeholder for data table execution) ---
if go_clicked:
    # --- Example: Where your data logic would run after clicking 'GO' ---
    st.markdown("<br><p style='padding: 0 20px; font-family: Arial; font-size: 14px; color: #333;'>Loading outstanding data for <b>A B ENTERPRISES [617]</b>...</p>", unsafe_allow_html=True)
    
    # Dummy dataframe injection to simulate table rendering
    df_dummy = pd.DataFrame({
        "Invoice No": ["INV-001", "INV-002", "INV-003"],
        "Date": ["01-Aug-2026", "02-Aug-2026", "03-Aug-2026"],
        "Amount": ["₹45,000", "₹12,500", "₹9,200"],
        "Status": ["Pending", "Overdue", "Pending"]
    })
    
    # We apply specific dataframe styling to match legacy systems (smaller fonts)
    st.markdown("""
        <style>
        div[data-testid="stDataFrame"] { padding: 0 20px; }
        </style>
    """, unsafe_allow_html=True)
    st.dataframe(df_dummy, use_container_width=True, hide_index=True)
