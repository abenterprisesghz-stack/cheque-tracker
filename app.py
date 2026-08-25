import plotly.express as px
import plotly.graph_objects as go

# ... (Aapka baki code same rahega) ...

else:
    # --- GLOBAL OVERVIEW (HOME SCREEN) ---
    st.markdown("""
        <div class="welcome-header">Global Inventory Overview</div>
        <div class="welcome-subtext">A macro-level real-time view of all cheques across your organization.</div>
    """, unsafe_allow_html=True)
    
    global_total = len(df)
    global_used = len(df[df['Status'] == 'USE'])
    global_unused = global_total - global_used
    utilization_pct = round((global_used / global_total * 100), 1) if global_total > 0 else 0
    
    # --- KPI Cards ---
    g1, g2, g3, g4 = st.columns(4)
    g1.metric("Total Cheques", f"{global_total:,}")
    g2.metric("Used / Cleared", f"{global_used:,}")
    g3.metric("Available", f"{global_unused:,}")
    g4.metric("Utilization Rate", f"{utilization_pct}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- LIVE VISUAL ANALYTICS ---
    col_chart1, col_chart2 = st.columns([1, 1.2])

    with col_chart1:
        st.markdown('<div class="table-title">Stock Ratio</div>', unsafe_allow_html=True)
        # Interactive Donut Chart
        fig_donut = go.Figure(data=[go.Pie(
            labels=['Available', 'Used'],
            values=[global_unused, global_used],
            hole=.65,
            marker_colors=['#34A853', '#EA4335'],
            textinfo='percent+label',
            insidetextorientation='radial'
        )])
        fig_donut.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            showlegend=False,
            height=280,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_chart2:
        st.markdown('<div class="table-title">City-wise Cheque Distribution</div>', unsafe_allow_html=True)
        if 'CITY' in df.columns:
            city_df = df.groupby(['CITY', 'Status']).size().reset_index(name='Count')
            fig_bar = px.bar(
                city_df, 
                x='CITY', 
                y='Count', 
                color='Status',
                barmode='group',
                color_discrete_map={'UNUSED': '#34A853', 'USE': '#EA4335'}
            )
            fig_bar.update_layout(
                margin=dict(t=10, b=10, l=10, r=10),
                height=280,
                xaxis_title="",
                yaxis_title="Total Cheques",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_bar, use_container_width=True)

    # --- RECENT ACTIVITY & LOW STOCK SECTION ---
    st.markdown('<div class="table-title">🚨 Clients Requiring Attention (Low Stock)</div>', unsafe_allow_html=True)
    
    inventory_summary = df.groupby('Search_Display')['Status'].apply(
        lambda x: (x == 'UNUSED').sum()
    ).reset_index(name='Available Cheques')
    
    low_stock_clients = inventory_summary[inventory_summary['Available Cheques'] <= 2].sort_values('Available Cheques')
    low_stock_clients = low_stock_clients.rename(columns={'Search_Display': 'Client Name & City'})
    
    if low_stock_clients.empty:
        st.success("✅ All clients have healthy cheque inventory (3 or more available).")
    else:
        styled_low_stock = low_stock_clients.style.map(
            lambda x: 'background-color: #FCE8E6; color: #C5221F; font-weight: bold;' if x <= 2 else '',
            subset=['Available Cheques']
        )
        st.dataframe(styled_low_stock, use_container_width=True, hide_index=True)
