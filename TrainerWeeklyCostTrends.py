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

# Resample by week (starting Monday) and sum costs by trainer
weekly_costs = df.groupby('Name of Trainer')['Cost '].resample('W-MON').sum().reset_index()

# Create line chart with data labels
fig = px.line(
    weekly_costs, 
    x='Date ', 
    y='Cost ',
    color='Name of Trainer',
    title='Weekly Cost Trends by Trainer',
    markers=True,
    text='Cost ',
    color_discrete_sequence=px.colors.qualitative.Set2
)

# Format data labels
fig.update_traces(
    textposition="middle left",
    texttemplate="%{text:.0f}",
    textfont=dict(size=9)
)

# ✅ Y-axis starts at 0
y_max = weekly_costs['Cost '].max() * 1.1
fig.update_yaxes(range=[0, y_max])

# ✅ Add bigger padding on X-axis (10% instead of 5%)
x_min = weekly_costs['Date '].min()
x_max = weekly_costs['Date '].max()
padding = (x_max - x_min) * 0.1   # 10% padding on both sides
fig.update_xaxes(
    range=[x_min - padding, x_max + padding],
    automargin=True,              # auto space for labels
    mirror=False,
    zeroline=False,
    showline=True,
    linecolor="black",
    linewidth=1
)

# Update layout
fig.update_layout(
    xaxis_title='Week',
    yaxis_title='Cost (₹)',
    plot_bgcolor='white',
    legend_title_text='Trainer'
)

fig.show()
