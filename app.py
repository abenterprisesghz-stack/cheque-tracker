import streamlit as st
import pandas as pd

# --- Page Setup ---
st.set_page_config(page_title="AB Enterprises | Cheque Tracker", page_icon="🏢", layout="wide")

# --- Custom CSS for Corporate Slate Minimalistic Theme ---
st.markdown("""
    <style>
    /* App Background - Clean Light Slate */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Modern Company Header - Solid & Professional */
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

    /* Metric Cards Styling */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px 20px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
        border-left: 4px solid #475569;
        transition: all 0.2s ease;
    }
    div[data-testid="metric-container"]:hover {
        border-left: 4px solid #0f172a;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    /* Metric Values */
    div[data-testid="stMetricValue"] {
        color: #0f172a !important;
        font-weight: 700 !important;
    }

    /* Dataframe Container styling */
    div[data-testid="stDataFrame"] {
        border-radius: 6px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
    }

    /* Radio Buttons (Alphabet Filter) Styling */
    div.row-widget.stRadio > div {
        flex-direction: row;
        flex-wrap: wrap;
        gap: 10px;
    }

    /* Dark Mode Compatibility */
    @media (prefers-color-scheme: dark) {
        .stApp { background-color: #0f172a; }
        .company-header {
            background-color: #0b1120;
            border-left: 6px solid #475569;
        }
        div[data-testid="metric-container"] {
            background-color: #1e293b;
            border: 1px solid #334155;
            border-left: 4px solid #64748b;
        }
        div[data-testid="stMetricValue"] {
            color: #f8fafc !important;
        }
        div[data-testid="stDataFrame"] {
            border: 1px solid #334155;
        }
    }
    
    .stSelectbox label {
        font-weight: 600 !important;
        color: #334155;
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


# --- 1. ALPHABET FILTER SECTION ---
st.markdown("### 🔠 Filter by Alphabet")

# Get unique starting letters from the data (A, B, C...)
letters_in_data = sorted([char for char in df['Search_Display'].str[0].str.upper().unique() if char.isalpha()])
available_letters = ["ALL"] + letters_in_data

# Radio buttons for A-Z
selected_letter = st.radio("Select Starting Letter", available_letters, horizontal=True, label_visibility="collapsed")

# Filter DataFrame based on selected letter
if selected_letter != "ALL":
    filtered_by_letter = df[df['Search_Display'].str.upper().str.startswith(selected_letter)]
else:
    filtered_by_letter = df

st.markdown("---")

# --- 2. SEARCH SECTION ---
st.markdown("### 🔍 Search Specific Party")

# Dropdown list dynamically updates based on the Alphabet selected above
display_list = sorted(list(filtered_by_letter['Search_Display'].dropna().unique()))
selected_display = st.selectbox(
    "Search Party Name:", 
    ["Select Party..."] + display_list,
    label_visibility="collapsed"
)

st.markdown("<br>", unsafe_allow_html=True) 


# --- 3. DISPLAY & DOWNLOAD LOGIC ---
# Determine which data to show (Specific Party OR Entire Alphabet group)
data_to_show = None
display_title = ""
file_name_prefix = ""

if selected_display != "Select Party...":
    # User selected a specific party from dropdown
    data_to_show = filtered_by_letter[filtered_by_letter['Search_Display'] == selected_display]
    display_title = selected_display
    file_name_prefix = selected_display
elif selected_letter != "ALL":
    # User selected an Alphabet, but hasn't picked a specific party yet
    data_to_show = filtered_by_letter
    display_title = f"All Parties starting with '{selected_letter}'"
    file_name_prefix = f"Parties_List_{selected_letter}"

# Render the Dashboard if there is data to show
if data_to_show is not None:
    used_count = len(data_to_show[data_to_show['Status'].str.upper() == 'USE'])
    total_count = len(data_to_show)
    unused_count = total_count - used_count
    
    col_summary, col_download = st.columns([4, 1])
    
    with col_summary:
        st.markdown(f"#### 📊 Dashboard Summary: **<span style='color:#475569;'>{display_title}</span>**", unsafe_allow_html=True)
    
    with col_download:
        # Prepare CSV for Download
        final_table = data_to_show.drop(columns=['Search_Display'])
        csv_data = final_table.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="⬇️ Download Data",
            data=csv_data,
            file_name=f"{file_name_prefix}_cheques.csv",
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
    
    # Data Table
    st.markdown("#### 📝 Cheque Details")
    st.dataframe(final_table, use_container_width=True, hide_index=True)
    
else:
    # Default info state
    st.info("ℹ️ Please select the party name in the search box.")
