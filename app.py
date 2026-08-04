import streamlit as st
import pandas as pd
from datetime import datetime
import os
import glob
import difflib

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
    [data-testid="stSidebar"] .stMarkdown p, 
    [data-testid="stSidebar"] .stMarkdown h1, 
    [data-testid="stSidebar"] .stMarkdown h2, 
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #202124 !important;
    }
    [data-testid="stSidebar"] label {
        color: #5F6368 !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        margin-bottom: 4px;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label p,
    [data-testid="stSidebar"] div[role="radiogroup"] label div {
        color: #202124 !important;
        font-weight: 400 !important;
        font-size: 14px !important;
    }

    /* Main Content & Cards */
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

    div[data-testid="metric-container"] {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 20px 24px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(0,0,0,0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0px 6px 16px rgba(0, 0, 0, 0.1);
    }
    div[data-testid="stMetricValue"] {
        color: #1A73E8 !important;
        font-size: 32px !important;
        font-weight: 500 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #5F6368 !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Table & Alerts */
    .table-title {
        font-size: 18px;
        font-weight: 500;
        color: #202124;
        margin-top: 24px;
        margin-bottom: 16px;
    }
    div[data-testid="stDataFrame"] {
        background-color: #FFFFFF;
        border-radius: 16px;
        border: none;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
        padding: 8px;
    }
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
    
    /* Custom Download Button */
    [data-testid="baseButton-secondary"] {
        border-radius: 20px !important;
        background-color: #E8F0FE !important;
        color: #1A73E8 !important;
        border: none !important;
        font-weight: 500 !important;
        transition: background-color 0.2s ease;
    }
    [data-testid="baseButton-secondary"]:hover {
        background-color: #D2E3FC !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar UI (Android Drawer Style) ---
with st.sidebar:
    st.markdown("""
        <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 32px; padding-bottom: 16px; border-bottom: 1px solid #F1F3F4;'>
            <div style='background-color: #1A73E8; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-weight: 500; font-size: 18px;'>
                AB
            </div>
            <div>
                <h2 style='margin: 0; font-size: 18px; color: #202124; font-weight: 500;'>Enterprises</h2>
                <div style='color: #5F6368; font-size: 12px;'>Dashboard App</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Global Navigation
    app_mode = st.radio(
        "Select Module",
        ["Cheque Dashboard", "Sales & Invoices Dashboard"]
    )
    st.markdown("<hr style='border-color: #F1F3F4;'>", unsafe_allow_html=True)

# ==========================================
# MODULE 1: CHEQUE DASHBOARD
# ==========================================
if app_mode == "Cheque Dashboard":
    @st.cache_data(ttl=60) 
    def load_cheque_data():
        df = pd.read_excel("data.xlsx")
        df.columns = df.columns.str.strip()
        
        if 'Status' in df.columns:
            df['Status'] = df['Status'].fillna('UNUSED').replace('', 'UNUSED')
        else:
            st.error("System Error: 'Status' column missing in data.xlsx.")
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
        df = load_cheque_data()
    except FileNotFoundError:
        st.error("System Error: 'data.xlsx' file not found in the directory.")
        st.stop()

    with st.sidebar:
        display_list = sorted(list(df['Search_Display'].dropna().unique()))
        selected_display = st.selectbox("Select Party Account", ["-- Select a Client --"] + display_list)
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        status_filter = st.radio("Cheque Status Filter", ["All Cheques", "Available (Unused)", "Cleared (Used)"])
        st.caption(f"🕒 Last Synced: {datetime.now().strftime('%I:%M %p, %d %b')}")

    if selected_display != "-- Select a Client --":
        filtered_df = df[df['Search_Display'] == selected_display]
        final_table = filtered_df.drop(columns=['Search_Display'])
        
        used_count = len(filtered_df[filtered_df['Status'].str.upper() == 'USE'])
        total_count = len(filtered_df)
        unused_count = total_count - used_count
        
        party_name = selected_display.split('(')[0].strip()
        st.markdown(f"""
            <div class="welcome-header">{party_name}</div>
            <div class="welcome-subtext">Client overview and cheque inventory details.</div>
        """, unsafe_allow_html=True)
        
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

        m1, m2, m3 = st.columns(3)
        m1.metric("Total Logged", total_count)
        m2.metric("Used / Cleared", used_count)
        m3.metric("Available", unused_count)
        
        st.markdown('<div class="table-title">Recent Activity</div>', unsafe_allow_html=True)
        
        display_df = final_table.copy()
        if status_filter == "Available (Unused)":
            display_df = display_df[display_df['Status'].str.upper() == 'UNUSED']
        elif status_filter == "Cleared (Used)":
            display_df = display_df[display_df['Status'].str.upper() == 'USE']

        st.dataframe(display_df, use_container_width=True, hide_index=True, height=400)
        
        st.markdown("<br>", unsafe_allow_html=True)
        d_col1, d_col2 = st.columns([5, 1.2]) 
        with d_col2:
            csv_data = display_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=f"{selected_display}_Cheques.csv",
                mime="text/csv",
                use_container_width=True
            )
    else:
        st.markdown("""
            <div style="margin-top: 60px; padding: 40px; background-color: #FFFFFF; border-radius: 16px; box-shadow: 0px 4px 12px rgba(0,0,0,0.05); text-align: center;">
                <div style="background-color: #E8F0FE; width: 64px; height: 64px; border-radius: 50%; display: flex; justify-content: center; align-items: center; margin: 0 auto 20px auto; font-size: 28px;">
                    📝
                </div>
                <div class="welcome-header">Cheque Inventory</div>
                <div class="welcome-subtext">Open the sidebar menu and select a client to view their cheque details.</div>
            </div>
        """, unsafe_allow_html=True)


# ==========================================
# MODULE 2: SALES & INVOICES DASHBOARD
# ==========================================
elif app_mode == "Sales & Invoices Dashboard":
        
    @st.cache_data(ttl=60)
    def auto_load_sales_data():
        all_excel_files = glob.glob("*.xlsx") + glob.glob("*.xls")
        sales_files = [f for f in all_excel_files if f.lower() != 'data.xlsx']
        
        if not sales_files:
            return None
            
        all_dfs = []
        for file in sales_files:
            try:
                df = pd.read_excel(file)
                if 'Doc.Date' in df.columns:
                    df['Doc.Date'] = pd.to_datetime(df['Doc.Date']).dt.strftime('%d-%m-%Y')
                all_dfs.append(df)
            except Exception as e:
                pass
                
        if not all_dfs:
            return None
            
        combined_df = pd.concat(all_dfs, ignore_index=True)
        return combined_df

    sales_df = auto_load_sales_data()
    
    if sales_df is None:
        st.markdown("""
            <div style="margin-top: 60px; padding: 40px; background-color: #FFFFFF; border-radius: 16px; box-shadow: 0px 4px 12px rgba(0,0,0,0.05); text-align: center;">
                <div style="background-color: #FCE8E6; width: 64px; height: 64px; border-radius: 50%; display: flex; justify-content: center; align-items: center; margin: 0 auto 20px auto; font-size: 28px;">
                    ⚠️
                </div>
                <div class="welcome-header">No Sales Data Found</div>
                <div class="welcome-subtext">Please place your daily sales Excel files in the same folder as this script.</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        if 'Division Name' in sales_df.columns:
            divisions = ["All Divisions"] + sorted(sales_df['Division Name'].dropna().unique().tolist())
        else:
            divisions = ["All Divisions"]
            
        if 'Doc.Date' in sales_df.columns:
            dates = ["All Dates"] + sorted(sales_df['Doc.Date'].dropna().unique().tolist())
        else:
            dates = ["All Dates"]
            
        with st.sidebar:
            st.markdown("<div style='color: #202124; font-weight: 500; font-size: 15px; margin-bottom: 10px;'>Search & Filters</div>", unsafe_allow_html=True)
            
            selected_division = st.selectbox("Select Division", divisions)
            customer_search = st.text_input("Search Customer Name", placeholder="e.g., Apolo (spelling mistake OK)")
            selected_date = st.selectbox("Select Date", dates)
            
            st.caption(f"🕒 Last Synced: {datetime.now().strftime('%I:%M %p, %d %b')}")

        # --- Filter Execution Logic ---
        filtered_sales = sales_df.copy()
        
        if selected_division != "All Divisions":
            filtered_sales = filtered_sales[filtered_sales['Division Name'] == selected_division]
            
        if selected_date != "All Dates":
            if 'Doc.Date' in filtered_sales.columns:
                filtered_sales = filtered_sales[filtered_sales['Doc.Date'] == selected_date]

        # Splitting logic for search 
        is_searching = False
        matched_sales = None
        other_sales = filtered_sales.copy()

        if customer_search.strip() != "":
            is_searching = True
            if 'Customer Name' in filtered_sales.columns:
                search_term = customer_search.strip().lower()
                
                def is_fuzzy_match(name):
                    target_str = str(name).lower()
                    if search_term in target_str:
                        return True
                    words = target_str.split()
                    for word in words:
                        if difflib.SequenceMatcher(None, search_term, word).ratio() > 0.75:
                            return True
                    if difflib.SequenceMatcher(None, search_term, target_str).ratio() > 0.60:
                        return True
                    return False
                
                mask = filtered_sales['Customer Name'].apply(is_fuzzy_match)
                
                matched_sales = filtered_sales[mask]
                other_sales = filtered_sales[~mask] # Bacha hua data
                
        # Metric Cards KPI Logic (Show matched KPI if searching)
        kpi_df = matched_sales if is_searching and matched_sales is not None else filtered_sales
        
        total_amount = kpi_df['Net Amount'].sum() if 'Net Amount' in kpi_df.columns else 0
        total_qty = kpi_df['Net Qty'].sum() if 'Net Qty' in kpi_df.columns else 0
        invoice_count = kpi_df['Customer Invoice No'].nunique() if 'Customer Invoice No' in kpi_df.columns else 0

        # Header UI
        st.markdown(f"""
            <div class="welcome-header">Sales & Invoices Overview</div>
            <div class="welcome-subtext">Viewing data for: <b>{selected_division}</b> | Date: <b>{selected_date}</b></div>
        """, unsafe_allow_html=True)

        # Metric Cards
        s1, s2, s3 = st.columns(3)
        s1.metric("Total Net Amount", f"₹ {total_amount:,.2f}")
        s2.metric("Total Net Quantity", f"{total_qty:,.0f}")
        s3.metric("Unique Invoices", invoice_count)
        
        # --- UI DISPLAY (SEPARATED TABLES) ---
        if is_searching:
            st.markdown('<div class="table-title" style="color: #1A73E8;">🔍 Search Results (Matched)</div>', unsafe_allow_html=True)
            if matched_sales is not None and not matched_sales.empty:
                st.dataframe(matched_sales, use_container_width=True, hide_index=True)
            else:
                st.warning("No matches found for your search. Showing other data below.")
                
            st.markdown('<div class="table-title" style="margin-top: 40px;">📂 Other Data</div>', unsafe_allow_html=True)
            st.dataframe(other_sales, use_container_width=True, hide_index=True, height=300)
            
            # Download button downloads ONLY the matched data if searched
            csv_to_download = matched_sales if not matched_sales.empty else other_sales
        else:
            st.markdown('<div class="table-title">Invoice Ledger</div>', unsafe_allow_html=True)
            st.dataframe(filtered_sales, use_container_width=True, hide_index=True, height=500)
            csv_to_download = filtered_sales
            
        # Download Filtered Data
        st.markdown("<br>", unsafe_allow_html=True)
        d_col1, d_col2 = st.columns([5, 1.2]) 
        with d_col2:
            csv_sales = csv_to_download.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv_sales,
                file_name=f"Sales_Filtered_Data.csv",
                mime="text/csv",
                use_container_width=True
            )
            
