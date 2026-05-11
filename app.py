import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="AB Enterprises | Cheque Tracker", layout="wide")

# --- Company Header ---
st.markdown("""
    <div style="background-color:#262730;padding:20px;border-radius:10px;border-left: 8px solid #ff4b4b;">
        <h1 style="color:white;margin:0;">AB ENTERPRISES</h1>
        <p style="color:#cfcfcf;margin:0;font-size:16px;">
            ADD: C-44, SITE NO. 3, MEERUT ROAD INDUSTRIAL AREA, GHAZIABAD, U.P.
        </p>
    </div>
    <br>
    """, unsafe_allow_html=True)

def load_data():
    df = pd.read_excel("data.xlsx")
    df.columns = df.columns.str.strip()
    
    if 'Status' in df.columns:
        df['Status'] = df['Status'].fillna('UNUSED').replace('', 'UNUSED')
    else:
        st.error("Excel mein 'Status' column nahi mila!")
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
    st.error("Data file not found. Kripya 'data.xlsx' check karein.")
    st.stop()

# --- Search Section ---
col_search, col_btn = st.columns([4, 1])

with col_search:
    display_list = sorted(list(df['Search_Display'].dropna().unique()))
    selected_display = st.selectbox(
        "Search Party Name:", 
        ["Select Party..."] + display_list,
        label_visibility="collapsed"
    )

with col_btn:
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()

# --- Display Logic ---
if selected_display != "Select Party...":
    filtered_df = df[df['Search_Display'] == selected_display]
    
    used_count = len(filtered_df[filtered_df['Status'].str.upper() == 'USE'])
    total_count = len(filtered_df)
    unused_count = total_count - used_count
    
    st.markdown(f"### 📊 Summary: **{selected_display}**")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Cheques", total_count)
    m2.metric("Used Cheques", used_count)
    m3.metric("Unused (Pending)", unused_count)
    
    st.markdown("---")
    final_table = filtered_df.drop(columns=['Search_Display'])
    st.dataframe(final_table, use_container_width=True, hide_index=True)
else:
    st.info("Kripya search box mein Party ka naam select karein.")