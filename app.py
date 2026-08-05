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
    
    /* Headers & Text */
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
    .table-title {
        font-size: 18px;
        font-weight: 500;
        color: #202124;
        margin-top: 24px;
        margin-bottom: 16px;
    }
    
    /* Alerts */
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
    </style>
""", unsafe_allow_html=True)

# --- Helper Functions ---
FILE_NAME = "data.xlsx"

@st.cache_data(ttl=60) 
def load_cheque_data():
    df = pd.read_excel(FILE_NAME)
    df.columns = df.columns.str.strip()
    
    if 'Status' in df.columns:
        df['Status'] = df['Status'].fillna('UNUSED').replace('', 'UNUSED')
    else:
        st.error(f"System Error: 'Status' column missing in {FILE_NAME}.")
        st.stop()

    if 'CITY' in df.columns:
        df['CITY'] = df['CITY'].fillna('Unknown')
        df['Search_Display'] = df['Party Name'].astype(str) + " (" + df['CITY'].astype(str) + ")"
    else:
        df['Search_Display'] = df['Party Name'].astype(str)

    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.strftime('%d-%m-%Y')
    return df

def save_data(new_df):
    """Saves dataframe back to Excel and clears cache to refresh view."""
    try:
        save_df = new_df.drop(columns=['Search_Display'], errors='ignore')
        save_df.to_excel(FILE_NAME, index=False)
        st.cache_data.clear()
        st.success("✅ Changes saved successfully!")
    except Exception as e:
        st.error(f"Error saving file: {e}")

# --- Data Loading ---
try:
    df = load_cheque_data()
except FileNotFoundError:
    st.error(f"System Error: '{FILE_NAME}' file not found in the directory.")
    st.stop()

# --- Sidebar UI ---
with st.sidebar:
    st.markdown("""
        <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 32px; padding-bottom: 16px; border-bottom: 1px solid #F1F3F4;'>
            <div style='background-color: #1A73E8; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-weight: 500; font-size: 18px;'>
                AB
            </div>
            <div>
                <h2 style='margin: 0; font-size: 18px; color: #202124; font-weight: 500;'>Enterprises</h2>
                <div style='color: #5F6368; font-size: 12px;'>Cheque Dashboard</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    global_search = st.text_input("🔍 Search Database", placeholder="Cheque No, Bank, etc.")
    st.markdown("<hr style='border-color: #F1F3F4; margin: 10px 0;'>", unsafe_allow_html=True)
    
    display_list = sorted(list(df['Search_Display'].dropna().unique()))
    selected_display = st.selectbox("Select Party Account", ["-- Select a Client --"] + display_list)
    
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    status_filter = st.radio("Cheque Status Filter", ["All Cheques", "Available (Unused)", "Cleared (Used)"])
    st.caption(f"🕒 Last Synced: {datetime.now().strftime('%I:%M %p, %d %b')}")

# ==========================================
# ROUTING LOGIC
# ==========================================
if global_search.strip() != "":
    # --- VIEW 1: GLOBAL SEARCH RESULTS ---
    st.markdown(f"""
        <div class="welcome-header">Search Results</div>
        <div class="welcome-subtext">Searching all records for: <b>"{global_search}"</b></div>
    """, unsafe_allow_html=True)
    
    mask = df.astype(str).apply(lambda x: x.str.contains(global_search, case=False, na=False)).any(axis=1)
    search_results = df[mask].drop(columns=['Search_Display'])
    
    if search_results.empty:
        st.warning("No matches found. Please try a different search term.")
    else:
        st.success(f"Found {len(search_results)} matching record(s).")
        st.dataframe(search_results, use_container_width=True, hide_index=True)

elif selected_display != "-- Select a Client --":
    # --- VIEW 2: INDIVIDUAL CLIENT DASHBOARD ---
    party_name = selected_display.split('(')[0].strip()
    st.markdown(f"""
        <div class="welcome-header">{party_name}</div>
        <div class="welcome-subtext">Manage inventory and update status.</div>
    """, unsafe_allow_html=True)

    filtered_df = df[df['Search_Display'] == selected_display]
    used_count = len(filtered_df[filtered_df['Status'].str.upper() == 'USE'])
    total_count = len(filtered_df)
    unused_count = total_count - used_count
    
    # --- Visual Inventory Health ONLY ---
    if total_count > 0:
        health_percentage = unused_count / total_count
        st.progress(health_percentage, text=f"Inventory Health: {unused_count} of {total_count} available")

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
    
    st.markdown('<div class="table-title">Interactive Cheque Ledger</div>', unsafe_allow_html=True)
    st.caption("💡 Tip: Double-click the 'Status' column to change a cheque from UNUSED to USE, then click Save.")
    
    display_df = filtered_df.copy()
    if status_filter == "Available (Unused)":
        display_df = display_df[display_df['Status'].str.upper() == 'UNUSED']
    elif status_filter == "Cleared (Used)":
        display_df = display_df[display_df['Status'].str.upper() == 'USE']

    edited_df = st.data_editor(
        display_df.drop(columns=['Search_Display']),
        column_config={
            "Status": st.column_config.SelectboxColumn(
                "Status",
                help="Mark cheque as used",
                options=["UNUSED", "USE"],
                required=True
            )
        },
        disabled=[col for col in display_df.columns if col not in ['Status', 'Search_Display']],
        use_container_width=True,
        hide_index=True,
        key="editor"
    )

    if not display_df.drop(columns=['Search_Display']).equals(edited_df):
        if st.button("💾 Save Status Updates", type="primary"):
            df.update(edited_df)
            save_data(df)
            st.rerun()
            
else:
    # --- VIEW 3: GLOBAL HEALTH OVERVIEW ---
    st.markdown("""
        <div class="welcome-header">Global Inventory Health</div>
        <div class="welcome-subtext">Review clients with critically low cheque inventory below.</div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="table-title">🚨 Action Required: Low Cheque Inventory</div>', unsafe_allow_html=True)
    
    inventory_summary = df.groupby('Search_Display')['Status'].apply(
        lambda x: (x.str.upper() == 'UNUSED').sum()
    ).reset_index(name='Available Cheques')
    
    low_stock_clients = inventory_summary[inventory_summary['Available Cheques'] <= 2].sort_values('Available Cheques')
    low_stock_clients = low_stock_clients.rename(columns={'Search_Display': 'Party Name (City)'})
    
    if low_stock_clients.empty:
        st.success("✅ All clients have healthy cheque inventory (3 or more available).")
    else:
        st.dataframe(
            low_stock_clients.style.map(  # Fixed: changed applymap to map
                lambda x: 'color: #D93025; font-weight: bold;' if x == 0 else 'color: #F9AB00; font-weight: bold;',
                subset=['Available Cheques']
            ),
            use_container_width=True, 
            hide_index=True
        )
