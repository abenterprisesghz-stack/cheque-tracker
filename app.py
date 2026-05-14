import streamlit as st
import pandas as pd

# --- Page Setup ---
st.set_page_config(page_title="AB Enterprises | Cheque Tracker", page_icon="🏢", layout="wide")

# --- Custom CSS for Corporate Slate Theme (Fully Auto-Responsive to Light/Dark Mode) ---
st.markdown("""
    <style>
    .company-header {
        background-color: #1e293b; 
        padding: 24px 32px;
        border-radius: 8px;
        border-left: 6px solid #64748b; 
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    .company-title {
        color: #f8fafc !important; 
        margin: 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
        letter-spacing: 0.5px;
        font-size: 30px;
    }
    .company-sub {
        color: #94a3b8 !important; 
        margin: 6px 0 0 0;
        font-size: 14px;
        font-weight: 400;
    }
    div[data-testid="metric-container"] {
        background-color: var(--secondary-background-color);
        border: 1px solid var(--faded-text-10);
        border-radius: 8px;
        padding: 16px 20px;
        border-left: 4px solid #64748b; 
        transition: all 0.2s ease;
    }
    div[data-testid="metric-container"]:hover {
        border-left: 4px solid #e11d48; 
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    div[data-testid="stMetricValue"] {
        color: var(--text-color) !important;
        font-weight: 700 !important;
    }
    div[data-testid="stDataFrame"] {
        border-radius: 6px;
        overflow: hidden;
        border: 1px solid var(--faded-text-10);
    }
    @keyframes pulse-border {
        0% { box-shadow: 0 0 0 0 rgba(225, 29, 72, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(225, 29, 72, 0); }
        100% { box-shadow: 0 0 0 0 rgba(225, 29, 72, 0); }
    }
    .critical-alert {
        background-color: rgba(225, 29, 72, 0.1); 
        border-left: 6px solid #e11d48; 
        padding: 18px 20px; 
        border-radius: 8px; 
        margin-top: 10px; 
        margin-bottom: 25px;
        animation: pulse-border 2s infinite;
    }
    .zero-alert {
        background-color: rgba(185, 28, 28, 0.15); 
        border-left: 6px solid #b91c1c; 
        padding: 18px 20px; 
        border-radius: 8px; 
        margin-top: 10px; 
        margin-bottom: 25px;
        animation: pulse-border 1.5s infinite;
    }
    .stSelectbox label, .stTextInput label, .stRadio label {
        font-weight: 600 !important;
        color: var(--text-color) !important;
    }
    h3, h4 {
        color: var(--text-color) !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Company Header ---
st.markdown("""
    <div class="company-header">
        <h1 class="company-title">AB ENTERPRISES</h1>
        <p class="company-sub">
            📍 ADD: C-44, SITE NO. 3, MEERUT ROAD INDUSTRIAL AREA, GHAZIABAD, U.P.
        </p>
    </div>
""", unsafe_allow_html=True)

# --- FAST Core Logic ---
# Cache TTL increased to 5 mins (300s) for better performance
@st.cache_data(ttl=300) 
def load_data():
    df = pd.read_excel("data.xlsx")
    df.columns = df.columns.str.strip()
    
    if 'Status' in df.columns:
        # Pre-format to uppercase once, saves processing power during filtering
        df['Status'] = df['Status'].fillna('UNUSED').astype(str).str.strip().str.upper()
        df['Status'] = df['Status'].replace('', 'UNUSED')
    else:
        st.error("❌ Excel mein 'Status' column nahi mila!")
        st.stop()

    if 'CITY' in df.columns:
        df['CITY'] = df['CITY'].fillna('Unknown')
        df['Search_Display'] = df['Party Name'].astype(str) + " (" + df['CITY'].astype(str) + ")"
    else:
        df['Search_Display'] = df['Party Name'].astype(str)
    
    # 🔥 SUPER FAST SEARCH OPTIMIZATION 🔥
    # Pre-combining all row data into a single lowercase string column for instant text searching
    df['_Search_Index'] = df.astype(str).agg(' '.join, axis=1).str.lower()
        
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("⚠️ Data file not found. Kripya 'data.xlsx' check karein.")
    st.stop()

# --- Search Section ---
st.markdown("### 🔍 Search & Filter")

display_list = sorted(list(df['Search_Display'].dropna().unique()))
selected_display = st.selectbox(
    "Search Party Name:", 
    ["Select Party..."] + display_list,
    label_visibility="collapsed"
)

st.markdown("<br>", unsafe_allow_html=True) 

# --- Display Logic ---
if selected_display != "Select Party...":
    # Filter for selected party
    filtered_df = df[df['Search_Display'] == selected_display]
    
    # Status calculation is now faster because 'Status' is already uppercase
    used_count = len(filtered_df[filtered_df['Status'] == 'USE'])
    total_count = len(filtered_df)
    unused_count = total_count - used_count
    
    # --- 🚨 CRITICAL ALERT SYSTEM 🚨 ---
    if unused_count == 0:
        st.markdown(f"""
            <div class="zero-alert">
                <h4 style="color: #b91c1c; margin: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-weight: 700;">
                    🛑 CRITICAL: Out of Cheques
                </h4>
                <p style="color: var(--text-color); margin: 8px 0 0 0; font-size: 16px; font-weight: 500;">
                    <b>{selected_display}</b> Currently Cheques in SD <b style="font-size:18px; color: #b91c1c;">ZERO</b> available cheques.<br>
                    <b>Billing operations cannot proceed.</b> Please arrange new cheques for this party immediately!
                </p>
            </div>
        """, unsafe_allow_html=True)
    elif unused_count <= 2:
        st.markdown(f"""
            <div class="critical-alert">
                <h4 style="color: #e11d48; margin: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-weight: 700;">
                    ⚠️ ACTION REQUIRED: Low Cheque Inventory
                </h4>
                <p style="color: var(--text-color); margin: 8px 0 0 0; font-size: 16px; font-weight: 500;">
                    <b>{selected_display}</b> has only <b style="font-size:18px; color: #e11d48;">{unused_count}</b> unused cheque(s) left. <br>
                    Please send new cheques immediately to avoid any interruption in the billing process.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    # Drop backend processing columns for UI
    final_table = filtered_df.drop(columns=['Search_Display'])
    
    # Header and Download Button aligned
    col_summary, col_download = st.columns([4, 1])
    
    with col_summary:
        st.markdown(f"#### 📊 Dashboard Summary: **<span style='color:#64748b;'>{selected_display}</span>**", unsafe_allow_html=True)
    
    with col_download:
        csv_data = final_table.drop(columns=['_Search_Index']).to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Data",
            data=csv_data,
            file_name=f"{selected_display}_cheques.csv",
            mime="text/csv",
            use_container_width=True,
            type="primary"
        )
    
    # Dashboard Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("📑 Total Cheques", total_count)
    m2.metric("✅ Used Cheques", used_count)
    m3.metric("💳 Unused (Available)", unused_count)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- FAST ADVANCED FILTER SECTION ---
    st.markdown("#### 📝 Cheque Details & Filters")
    
    f_col1, f_col2 = st.columns([2, 2])
    
    with f_col1:
        status_filter = st.radio(
            "Filter by Status:",
            ["All", "Unused 💳", "Used ✅"],
            horizontal=True
        )
        
    with f_col2:
        search_term = st.text_input("🔍 Search (Cheque No, Bank, Amount, etc.):", placeholder="Type to filter...")

    # Apply filters dynamically 
    display_df = final_table

    # 1. Fast Status Filter (Direct equality check)
    if status_filter == "Unused 💳":
        display_df = display_df[display_df['Status'] == 'UNUSED']
    elif status_filter == "Used ✅":
        display_df = display_df[display_df['Status'] == 'USE']

    # 2. Fast Text Search Filter (Searching single pre-computed index)
    if search_term:
        display_df = display_df[display_df['_Search_Index'].str.contains(search_term.lower(), na=False)]

    # Remove the hidden search index column before showing in the UI
    ui_display_table = display_df.drop(columns=['_Search_Index'])

    st.caption(f"Showing {len(ui_display_table)} of {len(final_table)} records for this party.")
    st.dataframe(ui_display_table, use_container_width=True, hide_index=True)
    
else:
    st.info("ℹ️ Please select the party name in the search box.")
