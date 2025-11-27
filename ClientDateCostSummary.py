import pandas as pd

# Load the data from the sheet
data = q.cells('B2:U74', first_row_header=True)

# Create a DataFrame
df = pd.DataFrame(data)

# Convert Date and Cost columns to appropriate types
df['Date '] = pd.to_datetime(df['Date '], errors='coerce')
df['Cost '] = pd.to_numeric(df['Cost '], errors='coerce')

# Remove rows with missing dates or costs
df = df.dropna(subset=['Date ', 'Cost '])

# Select only relevant columns with trainer name first
client_date_cost = df[['Name of Trainer', 'Client Name', 'Region', 'Date ', 'Cost ']]

# Sort by Trainer Name and Date
client_date_cost = client_date_cost.sort_values(['Name of Trainer', 'Date '])

# Reset index
client_date_cost = client_date_cost.reset_index(drop=True)

client_date_cost