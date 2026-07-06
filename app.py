#import streamlit as st
import pandas as pd

# --- Page Setup ---
st.set_page_config(page_title="AB Enterprises | Cheque Tracker", page_icon="🏢", layout="wide")

# --- Custom CSS for Bright Corporate Theme ---
st.markdown("""
    <style>
    /* --- Main App Background Image (Light/Bright Office) --- */
    .stApp {
        background: linear-gradient(rgba(248, 250, 252, 0.85), rgba(248, 250, 252, 0.90)), 
                    url("https://images.unsplash.com/photo-1497366216548-37526070297c?q=80&w=1920&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Modern Company Header - Clean white glassmorphism look */
    .company-header {
        background: rgba(255, 255, 255, 0.9); 
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 24px 32px;
        border-radius: 8px;
        border-left: 6px solid #2563eb; /* Royal Blue Accent */
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        gap: 25px;
    }
    
    .header-logo {
        width: 80px;
        height: auto;
    }

    .company-title {
        color: #1e3a8a !important; /* Deep Blue Text */
        margin: 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 800;
        letter-spacing: 0.5px;
        font-size: 30px;
    }
    .company-sub {
        color: #64748b !important; 
        margin: 6px 0 0 0;
        font-size: 14px;
        font-weight: 500;
    }

    /* Metric Cards Styling - Clean white with blue accents */
    div[data-testid="metric-container"] {
        background-color: rgba(255, 255, 255, 0.95);
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(0, 0, 0, 0.05);
        border-radius: 8px;
        padding: 16px 20px;
        border-left: 4px solid #2563eb; 
        transition: all 0.2s ease;
    }
    div[data-testid="metric-container"]:hover {
        border-left: 4px solid #d97706; /* Amber accent on hover */
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    
    div[data-testid="stMetricValue"] {
        color: #0f172a !important; 
        font-weight: 800 !important;
    }

    /* Dataframe Container styling */
    div[data-testid="stDataFrame"] {
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 6px;
        overflow: hidden;
        border: 1px solid rgba(0, 0, 0, 0.1);
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    }

    /* Alert Box Animation & Styling */
    @keyframes pulse-border-light {
        0% { box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.3); }
        70% { box-shadow: 0 0 0 10px rgba(220, 38, 38, 0); }
        100% { box-shadow: 0 0 0 0 rgba(220, 38, 38, 0); }
    }
    .critical-alert {
        background-color: rgba(254, 242, 242, 0.95); 
        border-left: 6px solid #dc2626; 
        padding: 18px 20px; 
        border-radius: 8px; 
        margin-top: 10px; 
        margin-bottom: 25px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        animation: pulse-border-light 2s infinite;
    }
    .zero-alert {
        background-color: rgba(254, 226, 226, 0.95); 
        border-left: 6px solid #991b1b; 
        padding: 18px 20px; 
        border-radius: 8px; 
        margin-top: 10px; 
        margin-bottom: 25px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        animation: pulse-border-light 1.5s infinite;
    }

    /* Text coloring for light overlay readability */
    .stSelectbox label, .stTextInput label, .stRadio label, p {
        font-weight: 600 !important;
        color: #334155 !important;
    }
    h3, h4 {
        color: #0f172a !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Company Header with Corporate Image ---
st.markdown("""
    <div class="company-header">
        <img src="https://cdn-icons-png.flaticon.com/512/2830/2830284.png" class="header-logo" alt="Corporate Logo">
        <div>
            <h1 class="company-title">AB ENTERPRISES</h1>
            <p class="company-sub">
                📍 ADD: C-44, SITE NO. 3, MEERUT ROAD INDUSTRIAL AREA, GHAZIABAD, U.P.
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- Core Logic ---
@st.cache_data(ttl=60) 
def load_data():
    df = pd.read_excel("data.xlsx")
    df.columns = df.columns.str.strip()
    
    if 'Status' in df.columns:
        df['Status'] = df['Status'].fillna('UNUSED').replace('', 'UNUSED')
    else:
        st.error("❌ Excel mein 'Status' column nahi mila!")
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
    filtered_df = df[df['Search_Display'] == selected_display]
    final_table = filtered_df.drop(columns=['Search_Display'])
    
    used_count = len(filtered_df[filtered_df['Status'].str.upper() == 'USE'])
    total_count = len(filtered_df)
    unused_count = total_count - used_count
    
    # --- 🚨 CRITICAL ALERT SYSTEM 🚨 ---
    if unused_count == 0:
        st.markdown(f"""
            <div class="zero-alert">
                <h4 style="color: #991b1b; margin: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-weight: 800;">
                    🛑 CRITICAL: Out of Cheques
                </h4>
                <p style="color: #450a0a; margin: 8px 0 0 0; font-size: 16px; font-weight: 600;">
                    <b>{selected_display}</b> Currently Cheques Status at SD <b style="font-size:18px; color: #991b1b;">ZERO</b> availables .<br>
                    <b>Billing operations cannot proceed.</b> Please arrange new cheques for this party immediately!
                </p>
            </div>
        """, unsafe_allow_html=True)
    elif unused_count <= 2:
        st.markdown(f"""
            <div class="critical-alert">
                <h4 style="color: #b91c1c; margin: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-weight: 800;">
                    ⚠️ ACTION REQUIRED: Low Cheque Inventory
                </h4>
                <p style="color: #7f1d1d; margin: 8px 0 0 0; font-size: 16px; font-weight: 600;">
                    <b>{selected_display}</b> has only <b style="font-size:18px; color: #b91c1c;">{unused_count}</b> unused cheque(s) left. <br>
                    Please send new cheques immediately to avoid any interruption in the billing process.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    # Dashboard Metrics Top View
    m1, m2, m3 = st.columns(3)
    m1.metric("📑 Total Cheques", total_count)
    m2.metric("✅ Used Cheques", used_count)
    m3.metric("💳 Unused (Available)", unused_count)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- ADVANCED FILTER SECTION ---
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

    # Apply the filters to the dataframe
    display_df = final_table.copy()

    # 1. Apply Status Filter
    if status_filter == "Unused 💳":
        display_df = display_df[display_df['Status'].str.upper() == 'UNUSED']
    elif status_filter == "Used ✅":
        display_df = display_df[display_df['Status'].str.upper() == 'USE']

    # 2. Apply Text Search Filter (Dynamic across all columns)
    if search_term:
        mask = display_df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
        display_df = display_df[mask]

    st.markdown("<br>", unsafe_allow_html=True)

    # --- MODIFIED LAYOUT: Summary Title & Filtered Download Button ---
    col_summary, col_download = st.columns([4, 1])
    
    with col_summary:
        st.markdown(f"#### 📊 Dashboard Summary: **<span style='color:#2563eb;'>{selected_display}</span>**", unsafe_allow_html=True)
        st.caption(f"Showing {len(display_df)} of {len(final_table)} records based on your current filters.")
    
    with col_download:
        # Ab yahan sirf filtered data (display_df) hi CSV me convert hoga
        csv_data = display_df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="⬇️ Download Data",
            data=csv_data,
            file_name=f"{selected_display}_filtered_cheques.csv",
            mime="text/csv",
            use_container_width=True,
            type="primary"
        )
    
    # Data Table Rendering
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
else:
    st.info("ℹ️ Please select the party name in the search box.")
