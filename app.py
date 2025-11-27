import streamlit as st
import os
from reportlab.platypus import Image
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4, landscape, portrait
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pdf_generator import generate_expense_report
from chart_generator import generate_region_charts, generate_trainer_charts, generate_client_charts, generate_payment_charts

# Set page configuration
st.set_page_config(
    page_title="Expense Analysis Dashboard",
    page_icon="💰",
    layout="wide"
)

# --- Constants & Configuration ---
color_sequence = px.colors.qualitative.Plotly
chart_template = "plotly_white"

# Title and Introduction
st.title("💰 Expense Analysis Dashboard")
st.markdown("""
This dashboard allows you to analyze expense data. 
Upload your CSV file to get started.
""")

# File Uploader
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=['csv'])

# Initialize session state for data storage
if 'filtered_df' not in st.session_state:
    st.session_state.filtered_df = None
if 'total_cost' not in st.session_state:
    st.session_state.total_cost = 0
if 'total_sessions' not in st.session_state:
    st.session_state.total_sessions = 0
if 'avg_cost' not in st.session_state:
    st.session_state.avg_cost = 0
if 'pdf_data' not in st.session_state:
    st.session_state.pdf_data = None





if uploaded_file is not None:
    try:
        # Load data - Try reading with header=1 first (skipping the first metadata row)
        # We read the first few lines to check the structure
        uploaded_file.seek(0)
        first_line = uploaded_file.readline().decode('utf-8')
        uploaded_file.seek(0)
        
        if first_line.startswith(',,,,,'):
            # If the first line looks like metadata (mostly empty), skip it
            df = pd.read_csv(uploaded_file, header=1)
        else:
            df = pd.read_csv(uploaded_file)
        
        # Data Cleaning: Strip whitespace from column names
        df.columns = df.columns.str.strip()
        
        # Validate required columns
        # Note: The user's CSV has 'Date ' with a space, which we stripped above.
        required_columns = ['Date', 'Region', 'Client Name', 'Cost', 'Name of Trainer', 'Payment Type']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            st.error(f"The uploaded file is missing the following required columns: {', '.join(missing_columns)}")
            st.write("Available columns:", df.columns.tolist())
        else:
            # Data Preprocessing
            # Handle potential mixed formats in Date column
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce', dayfirst=True)
            df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce')
            
            # Drop rows with missing essential data
            df = df.dropna(subset=['Date', 'Cost'])
            
            # --- Session Logic Refinement ---
            # A "Session" is defined as a unique combination of Date and Client Name.
            # As per user request, we use Client Name & Date parameters.
            df['Session_ID'] = df['Date'].astype(str) + "_" + df['Client Name']
            
            # --- Sidebar Filters ---
            st.sidebar.header("Filters")
            
            # Date Range Filter
            if not df['Date'].empty:
                min_date = df['Date'].min().date()
                max_date = df['Date'].max().date()
                
                date_range = st.sidebar.date_input(
                    "Select Date Range",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date
                )
                
                # Filter data by date
                if len(date_range) == 2:
                    start_date, end_date = date_range
                    mask = (df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)
                    filtered_df = df.loc[mask]
                else:
                    filtered_df = df
            else:
                filtered_df = df
            
            # Region Filter
            regions = sorted(filtered_df['Region'].dropna().unique())
            selected_regions = st.sidebar.multiselect("Select Region", regions, default=regions)
            
            if selected_regions:
                filtered_df = filtered_df[filtered_df['Region'].isin(selected_regions)]
                
            # Client Filter
            clients = sorted(filtered_df['Client Name'].dropna().unique())
            selected_clients = st.sidebar.multiselect("Select Client", clients, default=clients)
            
            if selected_clients:
                filtered_df = filtered_df[filtered_df['Client Name'].isin(selected_clients)]

            # Trainer Filter
            trainers = sorted(filtered_df['Name of Trainer'].dropna().unique())
            selected_trainers = st.sidebar.multiselect("Select Trainer", trainers, default=trainers)
            
            if selected_trainers:
                filtered_df = filtered_df[filtered_df['Name of Trainer'].isin(selected_trainers)]
            
            # --- Generate Charts ---
            # Generate all charts once to be used in both UI and PDF
            charts = {}
            charts.update(generate_region_charts(filtered_df, color_sequence, chart_template))
            charts.update(generate_trainer_charts(filtered_df, color_sequence, chart_template))
            charts.update(generate_client_charts(filtered_df, color_sequence, chart_template))
            charts.update(generate_payment_charts(filtered_df, color_sequence, chart_template))

            # --- PDF Export in Sidebar ---
            st.sidebar.markdown("---")
            st.sidebar.markdown("### 📄 PDF Export Options")
            
            # Page Size Selection (A0 to A6, Letter, Legal)
            page_size = st.sidebar.selectbox(
                "Page Size",
                options=["A0", "A1", "A2", "A3", "A4", "A5", "A6", "Letter", "Legal"],
                index=4  # Default to A4
            )
            
            # Page Orientation
            orientation = st.sidebar.radio(
                "Orientation",
                options=["Portrait", "Landscape"],
                index=0  # Default to Portrait
            )
            
            # Cover Page Option
            include_cover = st.sidebar.checkbox("Include Cover Page", value=True)
            
            # Table Selection with Select All
            st.sidebar.markdown("**Include Tables:**")
            
            # Select All checkbox
            select_all = st.sidebar.checkbox("Select All Tables", value=True)
            
            # Individual table checkboxes
            include_kpi = st.sidebar.checkbox("KPI Summary", value=select_all, key="kpi_check")
            include_region = st.sidebar.checkbox("Regional Summary", value=select_all, key="region_check")
            include_trainer = st.sidebar.checkbox("Trainer Summary", value=select_all, key="trainer_check")
            include_client = st.sidebar.checkbox("Client Summary", value=select_all, key="client_check")
            include_payment = st.sidebar.checkbox("Payment Analysis", value=select_all, key="payment_check")
            
            if st.sidebar.button("Generate PDF Report", key="generate_pdf"):
                with st.spinner("Generating PDF report..."):
                    try:
                        # Collect options
                        options = {
                            'page_size': page_size,
                            'orientation': orientation,
                            'include_cover': include_cover,
                            'include_kpi': include_kpi,
                            'include_region': include_region,
                            'include_trainer': include_trainer,
                            'include_client': include_client,
                            'include_payment': include_payment
                        }
                        
                        # Generate PDF
                        pdf_bytes = generate_expense_report(filtered_df, options, charts)
                        
                        # Store in session state
                        st.session_state.pdf_data = pdf_bytes
                        st.sidebar.success("✅ PDF Generated!")
                        
                    except Exception as e:
                        st.sidebar.error(f"PDF Generation Error: {str(e)}")
                        st.session_state.pdf_data = None
            
            # Show download button if PDF data is available
            if st.session_state.pdf_data:
                st.sidebar.download_button(
                    label="📥 Download PDF",
                    data=st.session_state.pdf_data,
                    file_name=f"expense_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    key='download-pdf-report'
                )
            

            # Compute total cost and session count
            total_cost = filtered_df['Cost'].sum()
            total_sessions = filtered_df['Session_ID'].nunique()
            # Average Cost per Session
            avg_cost = total_cost / total_sessions if total_sessions > 0 else 0
            
            # Store in session state for export functionality
            st.session_state.filtered_df = filtered_df
            st.session_state.total_cost = total_cost
            
            # --- Tabs for Visualizations ---
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Trends & Regional", "👨‍🏫 Trainer Analysis", "🏢 Client Analysis", "💳 Payment Analysis", "📋 Detailed Data"])
            
            with tab1:
                st.subheader("Region Summary")
                
                region_stats = filtered_df.groupby('Region').agg({
                    'Cost': ['sum', 'mean'],
                    'Client Name': 'nunique',
                    'Date': 'nunique',
                    'Session_ID': 'nunique'
                })
                region_stats.columns = ['Total Cost', 'Average Cost (Row)', 'Number of Clients', 'Unique Days', 'Session Count']
                
                # Recalculate Average Cost based on Sessions
                region_stats['Average Cost'] = region_stats['Total Cost'] / region_stats['Session Count']
                
                # Average Weekly Cost
                weeks_per_region = filtered_df.groupby('Region')['Date'].apply(lambda x: (x.max() - x.min()).days / 7 if (x.max() - x.min()).days > 0 else 1)
                region_stats['Average Weekly Cost'] = region_stats['Total Cost'] / weeks_per_region
                
                # Average Daily Cost
                region_stats['Average Daily Cost'] = region_stats['Total Cost'] / region_stats['Unique Days']
                
                # Average Client Cost
                region_stats['Average Client Cost'] = region_stats['Total Cost'] / region_stats['Number of Clients']
                
                # Reorder and Format
                region_stats = region_stats[[
                    'Session Count', 'Number of Clients', 'Total Cost', 'Average Cost', 
                    'Average Weekly Cost', 'Average Daily Cost', 'Average Client Cost'
                ]].round(2)
                
                # Sorting: Sort by Total Cost descending as requested
                region_stats = region_stats.sort_values('Total Cost', ascending=False)
                
                st.data_editor(region_stats, use_container_width=True, disabled=True, hide_index=False)
                
                # Download button for Region Summary
                csv_region = region_stats.to_csv(index=True).encode('utf-8')
                st.download_button(
                    label="📥 Download Region Summary",
                    data=csv_region,
                    file_name="region_summary.csv",
                    mime="text/csv",
                    key='download-region-summary'
                )
                
                st.markdown("---")
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.subheader("Regional Cost Distribution")
                    if 'region_pie' in charts:
                        st.plotly_chart(charts['region_pie'], use_container_width=True)
                    
                with col_b:
                    st.subheader("Weekly Cost Trends by Region")
                    if 'region_trend' in charts:
                        st.plotly_chart(charts['region_trend'], use_container_width=True)
                    else:
                        st.info("No data available for trends.")
                
                st.subheader("Regional Cost Analysis")
                if 'region_bar_group' in charts:
                    st.plotly_chart(charts['region_bar_group'], use_container_width=True)
                
                st.markdown("---")
                st.subheader("Regional Activity Overview")
                
                if 'region_activity' in charts:
                    st.plotly_chart(charts['region_activity'], use_container_width=True)

            with tab2:
                st.subheader("Trainer Summary")
                
                trainer_stats = filtered_df.groupby('Name of Trainer').agg({
                    'Cost': 'sum',
                    'Session_ID': 'nunique',
                    'Date': lambda x: (x.max() - x.min()).days / 7 if (x.max() - x.min()).days > 0 else 1
                })
                trainer_stats.columns = ['Total Cost', 'Session Count', 'Weeks']
                
                trainer_stats['Average Cost'] = trainer_stats['Total Cost'] / trainer_stats['Session Count']
                trainer_stats['Average Weekly Cost'] = trainer_stats['Total Cost'] / trainer_stats['Weeks']
                
                trainer_stats = trainer_stats[['Session Count', 'Total Cost', 'Average Cost', 'Average Weekly Cost']].round(2)
                trainer_stats = trainer_stats.sort_values('Total Cost', ascending=False)
                
                st.data_editor(trainer_stats, use_container_width=True, disabled=True, hide_index=False)
                
                # Download button for Trainer Summary
                csv_trainer = trainer_stats.to_csv(index=True).encode('utf-8')
                st.download_button(
                    label="📥 Download Trainer Summary",
                    data=csv_trainer,
                    file_name="trainer_summary.csv",
                    mime="text/csv",
                    key='download-trainer-summary'
                )
                
                st.markdown("---")
                
                col_t1, col_t2 = st.columns(2)
                
                with col_t1:
                    st.markdown("#### Trainer Expenses by Payment Method")
                    if 'trainer_payment' in charts:
                        st.plotly_chart(charts['trainer_payment'], use_container_width=True)
                        
                with col_t2:
                    st.markdown("#### Regional-Trainer Cost Heatmap")
                    if 'trainer_heatmap' in charts:
                        st.plotly_chart(charts['trainer_heatmap'], use_container_width=True)
                
                st.markdown("---")
                
                col_t3, col_t4 = st.columns(2)
                
                with col_t3:
                    st.markdown("#### Trainer Cost Efficiency Analysis")
                    if 'trainer_efficiency' in charts:
                        st.plotly_chart(charts['trainer_efficiency'], use_container_width=True)
                    
                with col_t4:
                    st.markdown("#### Trainer Cost Share")
                    if 'trainer_pie' in charts:
                        st.plotly_chart(charts['trainer_pie'], use_container_width=True)
                
                st.markdown("---")
                
                st.markdown("#### Weekly Cost Trends by Trainer")
                if 'trainer_trend' in charts:
                    st.plotly_chart(charts['trainer_trend'], use_container_width=True)

            with tab3:
                st.subheader("Client Summary")
                
                client_summary = filtered_df.groupby(['Region', 'Client Name']).agg({
                    'Cost': 'sum',
                    'Session_ID': 'nunique'
                }).reset_index()
                
                client_summary['Average Cost'] = client_summary['Cost'] / client_summary['Session_ID']
                client_summary.columns = ['Region', 'Client Name', 'Total Cost', 'Session Count', 'Average Cost']
                
                # Reorder columns
                client_summary = client_summary[['Region', 'Client Name', 'Session Count', 'Total Cost', 'Average Cost']].round(2)
                # Sort by Total Cost Descending
                client_summary = client_summary.sort_values('Total Cost', ascending=False)
                
                st.data_editor(client_summary, use_container_width=True, disabled=True, hide_index=False)
                
                # Download button for Client Summary
                csv_client = client_summary.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Client Summary",
                    data=csv_client,
                    file_name="client_summary.csv",
                    mime="text/csv",
                    key='download-client-summary'
                )
                
                st.subheader("Client Cost Overview")
                if 'client_cost' in charts:
                    st.plotly_chart(charts['client_cost'], use_container_width=True)
            
                st.subheader("Client Session Analysis")
                if 'client_scatter' in charts:
                    st.plotly_chart(charts['client_scatter'], use_container_width=True)
            
            with tab4:
                st.subheader("Payment Analysis")
                
                payment_pivot = filtered_df.pivot_table(
                    index='Name of Trainer',
                    columns='Payment Type',
                    values='Cost',
                    aggfunc='sum',
                    fill_value=0,
                    margins=True,
                    margins_name='Grand Total'
                ).round(2)
                
                st.markdown("#### Payment by Trainer")
                st.data_editor(payment_pivot, use_container_width=True, disabled=True, hide_index=False)
                
                # Download button for Payment Pivot
                csv_payment = payment_pivot.to_csv(index=True).encode('utf-8')
                st.download_button(
                    label="📥 Download Payment Summary",
                    data=csv_payment,
                    file_name="payment_by_trainer.csv",
                    mime="text/csv",
                    key='download-payment-pivot'
                )
                
                st.markdown("---")
                
                col_p1, col_p2 = st.columns(2)
                
                with col_p1:
                    st.markdown("#### Payment Method Distribution")
                    if 'payment_pie' in charts:
                        st.plotly_chart(charts['payment_pie'], use_container_width=True)
                    
                with col_p2:
                    st.markdown("#### Payment Methods by Region")
                    if 'payment_stack' in charts:
                        st.plotly_chart(charts['payment_stack'], use_container_width=True)

            with tab5:
                st.subheader("Raw Data")
                st.dataframe(filtered_df)
                
                # Download Button
                csv = filtered_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "Download Filtered Data",
                    csv,
                    "filtered_data.csv",
                    "text/csv",
                    key='download-csv'
                )
            


    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info("Please upload a CSV file to view the dashboard.")
    
    # Show sample data format
    st.markdown("### Expected CSV Format")
    st.markdown("""
    The app is designed to work with your 'L&D Onsite Visit Plan' files.
    It expects columns like:
    - **Date**: Date of the expense
    - **Region**: Region name
    - **Client Name**: Name of the client
    - **Cost**: Numeric cost value
    """)
