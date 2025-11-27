# 💰 Expense Analysis Dashboard

A comprehensive Streamlit-based web application for analyzing and visualizing expense data from L&D (Learning & Development) onsite visit plans. This tool provides powerful insights into regional costs, trainer performance, client expenses, and payment distributions through interactive dashboards and customizable PDF reports.

---

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Application Structure](#-application-structure)
- [Data Requirements](#-data-requirements)
- [Dashboard Tabs](#-dashboard-tabs)
- [PDF Report Generation](#-pdf-report-generation)
- [Technical Details](#-technical-details)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

---

## ✨ Features

### 📊 Interactive Dashboards
- **Regional Analysis**: Visualize cost distribution, trends, and activity across different regions
- **Trainer Performance**: Track trainer expenses, efficiency metrics, and payment methods
- **Client Insights**: Analyze client-specific costs and session patterns
- **Payment Analysis**: Monitor payment method distribution and regional payment preferences
- **Raw Data View**: Access and download filtered datasets

### 📈 Advanced Visualizations
- Pie/Donut charts for distribution analysis
- Line charts for trend tracking over time
- Grouped and stacked bar charts for comparative analysis
- Heatmaps for regional-trainer cost correlation
- Scatter plots for session analysis
- Interactive Plotly charts with zoom, pan, and hover capabilities

### 🎯 Smart Filtering
- Date range selection
- Multi-select filters for regions, clients, and trainers
- Real-time data updates based on filter selections
- Session-based analysis (unique Date + Client Name combinations)

### 📄 Customizable PDF Reports
- Multiple page sizes (A0-A6, Letter, Legal)
- Portrait or Landscape orientation
- Optional cover page with key metrics
- Selective table inclusion (KPI, Regional, Trainer, Client, Payment)
- Embedded charts and visualizations
- Professional styling with custom fonts and colors

### 💾 Data Export
- Download filtered data as CSV
- Export individual summary tables (Region, Trainer, Client, Payment)
- Generate comprehensive PDF reports with charts

---

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Clone or Download the Repository
```bash
cd "Expense Analysis App"
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Required Packages
The application requires the following Python packages:
- `streamlit` - Web application framework
- `pandas` - Data manipulation and analysis
- `plotly` - Interactive visualization library
- `reportlab` - PDF generation
- `kaleido` - Static image export for Plotly charts

---

## 💻 Usage

### Starting the Application

Run the following command in your terminal:

```bash
python -m streamlit run app.py
```

Or, if `streamlit` is in your PATH:

```bash
streamlit run app.py
```

The application will start and automatically open in your default web browser at:
- **Local URL**: http://localhost:8501
- **Network URL**: http://[your-ip]:8501

### Uploading Data

1. Click the **"Upload your CSV file"** button in the sidebar
2. Select your expense data CSV file
3. The dashboard will automatically load and display the analysis

---

## 📁 Application Structure

```
Expense Analysis App/
│
├── app.py                          # Main Streamlit application
├── chart_generator.py              # Chart generation module
├── pdf_generator.py                # PDF report generation module
├── requirements.txt                # Python dependencies
│
├── ClientCostComparison.py         # Legacy chart scripts
├── ClientCostVisualization.py
├── ClientDateCostSummary.py
├── ClientSummary.py
├── RegionSummary.py
├── TrainerClientRadarMap.py
├── TrainerSummary.py
├── TrainerWeeklyCostTrends.py
└── WeeklyCostTrends.py
```

### Core Modules

#### `app.py`
The main application file that:
- Configures the Streamlit page
- Handles file uploads and data preprocessing
- Manages sidebar filters (date range, region, client, trainer)
- Orchestrates chart generation
- Renders tabbed dashboard interface
- Provides data export functionality
- Integrates PDF report generation

#### `chart_generator.py`
Modular chart generation with four main functions:
- `generate_region_charts()` - Regional analysis visualizations
- `generate_trainer_charts()` - Trainer performance charts
- `generate_client_charts()` - Client expense visualizations
- `generate_payment_charts()` - Payment method analysis

#### `pdf_generator.py`
PDF report generation with:
- Font registration (Arial with Unicode support)
- Styled table creation
- Plotly figure to image conversion
- Customizable report sections
- Professional formatting and layout

---

## 📊 Data Requirements

### Expected CSV Format

The application expects a CSV file with the following columns:

| Column Name       | Data Type | Description                          |
|-------------------|-----------|--------------------------------------|
| Date              | Date      | Date of the expense (DD/MM/YYYY)     |
| Region            | Text      | Geographic region name               |
| Client Name       | Text      | Name of the client organization      |
| Cost              | Numeric   | Expense amount in currency           |
| Name of Trainer   | Text      | Name of the trainer                  |
| Payment Type      | Text      | Payment method (e.g., Cash, Online)  |

### Data Preprocessing

The application automatically:
- Strips whitespace from column names
- Handles metadata rows (skips first row if empty)
- Converts dates to datetime format (supports mixed formats)
- Converts cost values to numeric
- Drops rows with missing Date or Cost values
- Creates Session IDs (Date + Client Name combinations)

### Sample Data Structure

```csv
Date,Region,Client Name,Cost,Name of Trainer,Payment Type
01/09/2025,North,ABC Corp,15000,John Doe,Online
05/09/2025,South,XYZ Ltd,12000,Jane Smith,Cash
10/09/2025,East,PQR Inc,18000,John Doe,Online
```

---

## 🎨 Dashboard Tabs

### 1. 📈 Trends & Regional

**Regional Summary Table**
- Session Count
- Number of Clients
- Total Cost
- Average Cost per Session
- Average Weekly Cost
- Average Daily Cost
- Average Client Cost

**Visualizations**
- Regional Cost Distribution (Donut Chart)
- Weekly Cost Trends by Region (Line Chart)
- Regional Cost Analysis: Total vs Average (Grouped Bar Chart)
- Regional Activity Overview: Sessions & Clients (Grouped Bar Chart)

### 2. 👨‍🏫 Trainer Analysis

**Trainer Summary Table**
- Session Count
- Total Cost
- Average Cost per Session
- Average Weekly Cost

**Visualizations**
- Trainer Expenses by Payment Method (Grouped Bar Chart)
- Regional-Trainer Cost Heatmap
- Trainer Cost Efficiency Analysis (Line Chart)
- Trainer Cost Share (Donut Chart)
- Weekly Cost Trends by Trainer (Line Chart)

### 3. 🏢 Client Analysis

**Client Summary Table**
- Region
- Client Name
- Session Count
- Total Cost
- Average Cost per Session

**Visualizations**
- Client Cost Overview (Line Chart)
- Client Session Analysis (Scatter Plot with bubble size = Total Cost)

### 4. 💳 Payment Analysis

**Payment Pivot Table**
- Trainers vs Payment Types
- Grand totals for rows and columns

**Visualizations**
- Payment Method Distribution (Donut Chart)
- Payment Methods by Region (Stacked Bar Chart)

### 5. 📋 Detailed Data

- Complete filtered dataset in tabular format
- Download option for filtered data as CSV

---

## 📄 PDF Report Generation

### Configuration Options

#### Page Settings
- **Page Size**: A0, A1, A2, A3, A4 (default), A5, A6, Letter, Legal
- **Orientation**: Portrait (default) or Landscape

#### Content Options
- **Include Cover Page**: Yes (default) / No
  - Cover page includes generation timestamp, record count, and key metrics summary

#### Table Selection
- **Select All Tables**: Quick toggle for all sections
- **Individual Sections**:
  - KPI Summary
  - Regional Summary
  - Trainer Summary
  - Client Summary (Top 15)
  - Payment Analysis

### Report Contents

#### Cover Page (Optional)
- Report title
- Generation date and time
- Total records count
- Key metrics table (Total Cost, Total Sessions, Average Cost/Session)

#### KPI Summary
- Total Cost
- Total Sessions
- Average Cost per Session

#### Regional Summary
- Table: Region, Total Cost, Sessions, Clients
- Charts: Regional Cost Distribution, Weekly Trends, Cost Analysis

#### Trainer Summary
- Table: Top 10 Trainers by Total Cost
- Charts: Trainer Cost Share, Efficiency Analysis, Payment Methods

#### Client Summary
- Table: Top 15 Clients by Total Cost
- Charts: Client Cost Overview, Session Analysis

#### Payment Analysis
- Table: Payment Type Distribution with Percentages
- Charts: Payment Method Distribution, Payment Methods by Region

### Generating a PDF Report

1. Upload and filter your data as desired
2. Scroll to the **"📄 PDF Export Options"** section in the sidebar
3. Configure page size, orientation, and content options
4. Click **"Generate PDF Report"**
5. Wait for the success message
6. Click **"📥 Download PDF"** to save the report

---

## 🔧 Technical Details

### Session Logic

A **Session** is defined as a unique combination of:
- **Date**: The date of the expense
- **Client Name**: The name of the client

This allows for accurate session counting and average cost calculations.

**Session ID Format**: `YYYY-MM-DD_ClientName`

### Chart Configuration

- **Color Scheme**: Plotly qualitative palette
- **Template**: `plotly_white` for clean, professional appearance
- **Interactivity**: All charts support zoom, pan, hover, and legend toggling

### Font Support

The PDF generator uses:
- **Primary**: Arial (with Unicode support for special characters)
- **Fallback**: Helvetica (if Arial is unavailable)

### Performance Considerations

- Charts are generated once and reused for both UI display and PDF export
- Large datasets may take longer to process
- PDF generation with all charts typically takes 5-10 seconds

---

## 🐛 Troubleshooting

### Issue: "streamlit is not recognized"

**Solution**: Use the full Python module syntax:
```bash
python -m streamlit run app.py
```

### Issue: Missing columns error

**Solution**: Ensure your CSV has all required columns:
- Date
- Region
- Client Name
- Cost
- Name of Trainer
- Payment Type

### Issue: Date parsing errors

**Solution**: The app supports multiple date formats, but ensure dates are in a consistent format (DD/MM/YYYY or MM/DD/YYYY).

### Issue: PDF generation fails

**Solution**: 
1. Ensure `kaleido` is installed: `pip install kaleido`
2. Check that Arial font is available (Windows: C:\Windows\Fonts\arial.ttf)
3. Try generating with fewer chart options

### Issue: Charts not displaying

**Solution**:
1. Verify data is loaded correctly
2. Check that filters haven't excluded all data
3. Ensure Plotly is properly installed: `pip install plotly --upgrade`

### Issue: Application runs slowly

**Solution**:
1. Filter data to smaller date ranges
2. Reduce the number of selected regions/clients/trainers
3. Close other browser tabs to free up memory

---

## 📝 Best Practices

### Data Preparation
- Clean your CSV data before uploading
- Ensure consistent date formats
- Remove duplicate entries
- Verify numeric values in the Cost column

### Using Filters
- Start with broad filters and narrow down
- Use date ranges to focus on specific periods
- Combine multiple filters for detailed analysis

### PDF Reports
- Use Landscape orientation for wider tables and charts
- Select only necessary sections to reduce file size
- Include cover page for formal reports

### Performance
- For large datasets (>10,000 rows), consider pre-filtering in Excel
- Close unused browser tabs while running the app
- Restart the app if it becomes unresponsive

---

## 🔄 Future Enhancements

Potential features for future versions:
- Database integration for persistent storage
- User authentication and multi-user support
- Automated email reports
- Budget vs. Actual comparison
- Forecasting and trend prediction
- Mobile-responsive design
- Dark mode theme
- Export to Excel with multiple sheets
- Scheduled report generation

---

## 👥 Support

For issues, questions, or feature requests:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Review the [Data Requirements](#-data-requirements)
3. Verify all dependencies are installed correctly

---

## 📜 License

This project is provided as-is for internal use. All rights reserved.

---

## 🙏 Acknowledgments

Built with:
- [Streamlit](https://streamlit.io/) - The fastest way to build data apps
- [Plotly](https://plotly.com/python/) - Interactive graphing library
- [Pandas](https://pandas.pydata.org/) - Data analysis toolkit
- [ReportLab](https://www.reportlab.com/) - PDF generation library

---

**Version**: 1.0.0  
**Last Updated**: November 2025  
**Author**: Expense Analysis Team
