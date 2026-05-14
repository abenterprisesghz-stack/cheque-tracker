import streamlit as st
import pandas as pd
import plotly.express as px  

# --- Page Setup ---
st.set_page_config(page_title="AB Enterprises | Cheque Tracker", page_icon="🏢", layout="wide")

# --- Custom CSS for Corporate Slate Minimalistic Theme & Alerts ---
st.markdown("""
    <style>
    /* App Background - Clean Light Slate */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Modern Company Header */
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
        border-left: 4px solid #0ea5e9;
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

    /* Alert Box Animation */
    @keyframes pulse-border {
        0% { box-shadow: 0 0 0 0 rgba(225, 29, 72, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(225, 29, 72, 0); }
        100% { box-shadow: 0 0 0 0 rgba(225, 29, 72, 0); }
    }
    .critical-alert {
        background-color: #fff1f2; 
        border-left: 6px solid #e11d48; 
        padding: 18px 20px; 
        border-radius: 8px; 
        margin-top: 15px; 
        margin-bottom: 25px;
        animation: pulse-border 2s infinite;
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
        .critical-alert {
            background-color: #4c0519;
            border-left: 6px solid #fb7185;
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

letters_in_data = sorted([char for char in df['Search_Display'].str[0].str.upper().unique() if char.isalpha()])
available_letters = ["ALL"] + letters_in_data

selected_letter = st.radio("Select Starting Letter", available_letters, horizontal=True, label_visibility="collapsed")

if selected_letter != "ALL":
    filtered_by_letter = df[df['Search_Display'].str.upper().str.startswith(selected_letter)]
else:
    filtered_by_letter = df

st.markdown("---")

# --- 2. SEARCH SECTION ---
st.markdown("### 🔍 Search Specific Party")

display_list = sorted(list(filtered_by_letter['Search_Display'].dropna().unique()))
selected_display = st.selectbox(
    "Search Party Name:", 
    ["Select Party..."] + display_list,
    label_visibility="collapsed"
)

st.markdown("<br>", unsafe_allow_html=True) 

# --- 3. DISPLAY & DOWNLOAD LOGIC ---
data_to_show = None
display_title = ""
file_name_prefix = ""

if selected_display != "Select Party...":
    data_to_show = filtered_by_letter[filtered_by_letter['Search_Display'] == selected_display]
    display_title = selected_display
    file_name_prefix = selected_display
elif selected_letter != "ALL":
    data_to_show = filtered_by_letter
    display_title = f"All Parties starting with '{selected_letter}'"
    file_name_prefix = f"Parties_List_{selected_letter}"

if data_to_show is not None:
    used_count = len(data_to_show[data_to_show['Status'].str.upper() == 'USE'])
    total_count = len(data_to_show)
    unused_count = total_count - used_count
    
    # 🚨 CRITICAL ALERT LOGIC 🚨
    if selected_display != "Select Party..." and unused_count <= 2:
        st.markdown(f"""
            <div class="critical-alert">
                <h4 style="color: #be123c; margin: 0; font-family: 'Segoe UI', sans-serif;">⚠️ ACTION REQUIRED: Low Cheque Inventory</h4>
                <p style="color: #9f1239; margin: 5px 0 0 0; font-size: 15px;">
                    <b>{selected_display}</b> has only <b style="font-size:18px;">{unused_count}</b> unused cheque(s) left. <br>
                    Please send new cheques immediately to avoid any interruption in the billing process.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    # Dashboard Header & Download
    col_summary, col_download = st.columns([4, 1])
    with col_summary:
        st.markdown(f"#### 📊 Dashboard Summary: **<span style='color:#475569;'>{display_title}</span>**", unsafe_allow_html=True)
    
    with col_download:
        final_table = data_to_show.drop(columns=['Search_Display'])
        csv_data = final_table.to_csv(index=False).encode('utf-8')
        st.download_button(label="⬇️ Download Data", data=csv_data, file_name=f"{file_name_prefix}_cheques.csv", mime="text/csv", use_container_width=True, type="primary")
    
    # Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("📑 Total Cheques", total_count)
    m2.metric("✅ Used Cheques", used_count)
    m3.metric("💳 Unused (Available)", unused_count)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- INFOGRAPHICS & TABLE LAYOUT ---
    col_chart, col_table = st.columns([1.2, 2.8], gap="large")
    
    with col_chart:
        st.markdown("#### 🍩 Status Distribution")
        if total_count > 0:
            chart_data = pd.DataFrame({'Status': ['Used', 'Unused'], 'Count': [used_count, unused_count]})
            custom_colors = {'Used': '#64748b', 'Unused': '#0ea5e9'} 
            
            fig = px.pie(chart_data, values='Count', names='Status', hole=0.5,
                         color='Status', color_discrete_map=custom_colors)
            fig.update_traces(textposition='inside', textinfo='percent+label', 
                              hoverinfo='label+percent+value')
            fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), showlegend=False, height=350)
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("No data available for chart.")

    with col_table:
        st.markdown("#### 📝 Cheque Details")
        st.dataframe(final_table, use_container_width=True, hide_index=True)
    
else:
    st.info("ℹ️ Please select the party name in the search box.")
