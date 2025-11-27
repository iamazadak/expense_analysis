import pandas as pd
import plotly.express as px

# Load the client summary data
data = q.cells("AK2:AO5", first_row_header=True)
df = pd.DataFrame(data)

# Rename columns to ensure they are unique
df.columns = ['Region', 'Total_Cost', 'Average_Client_Cost', 'Number_of_Clients', 'Total_Sessions']

# Create a bar chart comparing regions
fig = px.bar(df, 
             x='Region', 
             y=['Total_Cost', 'Average_Client_Cost'],
             title='Client Cost Comparison by Region',
             barmode='group')

# Update layout
fig.update_layout(
    xaxis_title='Region',
    yaxis_title='Cost (₹)',
    plot_bgcolor='white',
    legend_title_text='Cost Type'
)

fig.show()