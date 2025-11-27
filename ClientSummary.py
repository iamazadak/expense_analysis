import pandas as pd

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

client_summary