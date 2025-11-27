import pandas as pd
import plotly.express as px

# Load the data from the sheet
data = q.cells("B2:U74", first_row_header=True)

# Create a DataFrame
df = pd.DataFrame(data)

# Convert Date and Cost columns to appropriate types
df['Date '] = pd.to_datetime(df['Date '], errors='coerce')
df['Cost '] = pd.to_numeric(df['Cost '], errors='coerce')

# Remove rows with missing dates or costs
df = df.dropna(subset=['Date ', 'Cost '])

# Set Date as index
df.set_index('Date ', inplace=True)

# Resample by week (starting Monday) and sum costs by region
weekly_costs = df.groupby('Region')['Cost '].resample('W-MON').sum().reset_index()

# Create line chart with data labels
fig = px.line(
    weekly_costs,
    x='Date ',
    y='Cost ',
    color='Region',
    title='Weekly Cost Trends by Region',
    markers=True,
    text='Cost '   # 👈 Add labels from the Cost column
)

# Format data labels
fig.update_traces(
    textposition="top center",     # Position above points
    texttemplate="%{text:.0f}"     # Format labels (no decimals)
)

# Update layout
fig.update_layout(
    xaxis_title='Week',
    yaxis_title='Cost (₹)',
    plot_bgcolor='white',
    legend_title_text='Region'
)

fig.show()
