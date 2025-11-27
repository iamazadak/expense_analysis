import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the data from the sheet
data = q.cells('B2:U74', first_row_header=True)

# Create a DataFrame
df = pd.DataFrame(data)

# Convert Cost column to numeric
df['Cost '] = pd.to_numeric(df['Cost '], errors='coerce')

# Group by Region and Client and calculate summary statistics
client_summary = df.groupby(['Region', 'Client Name']).agg({
    'Cost ': ['count', 'sum', 'mean'],
}).round(2)

# Flatten column names
client_summary.columns = ['Session Count', 'Total Cost', 'Average Cost']

# Reset index to make Region and Client columns
client_summary = client_summary.reset_index()

# Sort by Total Cost descending
client_summary = client_summary.sort_values('Total Cost', ascending=False)

# Create a summary table by region
region_client_summary = client_summary.groupby('Region').agg({
    'Total Cost': ['sum', 'mean', 'count'],
    'Session Count': 'sum'
}).round(2)

# Flatten column names
region_client_summary.columns = ['Total Cost', 'Average Client Cost', 'Number of Clients', 'Total Sessions']

# Reset index to make Region a column
region_client_summary = region_client_summary.reset_index()

# Sort by Total Cost descending
region_client_summary = region_client_summary.sort_values('Total Cost', ascending=False)

region_client_summary