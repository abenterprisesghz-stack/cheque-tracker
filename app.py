import streamlit as st
import pandas as pd

# --- Page Setup ---
st.set_page_config(page_title="AB Enterprises | Cheque Tracker", page_icon="🏢", layout="wide")

# --- Custom CSS for Professional Dashboard Look ---
st.markdown("""
    <style>
    /* App Background */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Modern Company Header */
    .company-header {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 25px 30px;
        border-radius: 12px;
        border-left: 8px solid #3b82f6; /* Corporate Blue Accent */
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 2rem;
    }
    .company-title {
        color: #ffffff;
        margin: 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 800;
        letter-spacing: 1.5px;
        font-size: 32px;
    }
    .company-sub {
        color: #94a3b8;
        margin: 8px 0 0 0;
        font-size: 14px;
        font-weight: 500;
        letter-spacing: 0.5px;
    }

    /* Metric Cards Styling */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border-top: 4px solid #3b82f6;
        transition: transform 0.2s ease-in-out;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    /* Dataframe Container styling */
    div[data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
    }

    /* Dark Mode Compatibility */
    @media (prefers-color-scheme: dark) {
        .stApp { background-color: #0e1117; }
        div[data-testid="metric-container"] {
            background-color: #1e293b;
            border: 1px solid #334155;
            border-top: 4px solid #3b82f6;
        }
        div[data-testid="stDataFrame"] {
            border: 1px solid #334155;
        }
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

# --- Core Logic ---
@st.cache_data(ttl=60) # Caches data briefly for smoother refreshing
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
col_search, col_btn = st.columns([4, 1], gap="medium")

with col_search:
    display_list = sorted(list(df['Search_Display'].dropna().unique()))
    selected_display = st.selectbox(
        "Search Party Name:", 
        ["Select Party..."] + display_list,
        label_visibility="collapsed"
    )

with col_btn:
    if st.button("🔄 Refresh Data", use_container_width=True, type="primary"):
        st.cache_data.clear() # Clears cache to ensure fresh data
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True) # Adding a bit of space

# --- Display Logic ---
if selected_display != "Select Party...":
    filtered_df = df[df['Search_Display'] == selected_display]
    
    used_count = len(filtered_df[filtered_df['Status'].str.upper() == 'USE'])
    total_count = len(filtered_df)
    unused_count = total_count - used_count
    
    st.markdown(f"#### 📊 Dashboard Summary: **<span style='color:#3b82f6;'>{selected_display}</span>**", unsafe_allow_html=True)
    
    # Dashboard Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("📑 Total Cheques", total_count)
    m2.metric("✅ Used Cheques", used_count)
    m3.metric("💳 Unused (Available)", unused_count)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Data Table
    st.markdown("#### 📝 Cheque Details")
    final_table = filtered_df.drop(columns=['Search_Display'])
    st.dataframe(final_table, use_container_width=True, hide_index=True)
    
else:
    st.info("ℹ️ Please select the party name in the search box")
