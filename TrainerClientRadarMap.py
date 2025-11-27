import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the original data
data = q.cells('B2:U74', first_row_header=True)
df = pd.DataFrame(data)

# Convert Cost column to numeric
df['Cost '] = pd.to_numeric(df['Cost '], errors='coerce')

# Remove rows with missing costs
df = df.dropna(subset=['Cost '])

# Group by Region and Trainer to get total cost
region_trainer_summary = df.groupby(['Region', 'Name of Trainer']).agg({
    'Cost ': 'sum'
}).reset_index()

# Create a pivot table for the heatmap
pivot_table = region_trainer_summary.pivot(index='Region', columns='Name of Trainer', values='Cost ').fillna(0)

# Create heatmap
fig = go.Figure(data=go.Heatmap(
    z=pivot_table.values,
    x=pivot_table.columns,
    y=pivot_table.index,
    colorscale='Viridis',
    hoverongaps=False,
    text=pivot_table.values,
    texttemplate="%{text:.0f}",
    textfont={"size": 12}
))

# Update layout
fig.update_layout(
    title="Cost Distribution Heatmap: Regions vs Trainers",
    xaxis_title="Trainers",
    yaxis_title="Regions",
    plot_bgcolor='white'
)

fig.show()