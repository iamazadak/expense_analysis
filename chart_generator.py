import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def generate_region_charts(df, color_sequence, template):
    """Generates charts for the Region Analysis tab."""
    charts = {}
    
    # 1. Regional Cost Distribution (Pie/Donut)
    region_summary = df.groupby('Region')['Cost'].sum().reset_index()
    region_summary = region_summary.sort_values('Cost', ascending=False)
    fig_pie = px.pie(
        region_summary, 
        values='Cost', 
        names='Region', 
        hole=0.5,
        color_discrete_sequence=color_sequence,
        template=template,
        title="Regional Cost Distribution"
    )
    fig_pie.update_traces(
        textposition='inside', 
        texttemplate='%{percent}<br>Rs. %{value:.2s}',
        textfont=dict(size=12, color='white', family='Arial')
    )
    fig_pie.update_layout(
        showlegend=True, 
        legend=dict(orientation="v", yanchor="middle", y=0.5),
        margin=dict(l=50, r=50, t=80, b=50)
    )
    charts['region_pie'] = fig_pie

    # 2. Weekly Cost Trends by Region (Line)
    if not df.empty:
        temp_df = df.set_index('Date')
        weekly_costs = temp_df.groupby('Region')['Cost'].resample('W-MON').sum().reset_index()
        
        fig_line = px.line(
            weekly_costs,
            x='Date',
            y='Cost',
            color='Region',
            markers=True,
            labels={'Cost': 'Cost (Rs.)', 'Date': 'Week'},
            color_discrete_sequence=color_sequence,
            template=template,
            text='Cost',
            title="Weekly Cost Trends by Region"
        )
        fig_line.update_traces(
            textposition="top center",
            texttemplate='%{y:.2s}',
            textfont=dict(size=12, color='black', family='Arial'),
            mode='lines+markers+text'
        )
        fig_line.update_layout(
            hovermode="x unified",
            margin=dict(l=50, r=50, t=80, b=50)
        )
        charts['region_trend'] = fig_line

    # 3. Regional Cost Analysis: Total vs Average (Grouped Bar)
    region_agg = df.groupby('Region').agg({
        'Cost': 'sum',
        'Session_ID': 'nunique'
    }).reset_index()
    region_agg['Average Session Cost'] = region_agg['Cost'] / region_agg['Session_ID']
    region_agg.columns = ['Region', 'Total Cost', 'Session Count', 'Average Session Cost']
    region_agg = region_agg.sort_values('Total Cost', ascending=False)
    
    fig_bar_group = px.bar(
        region_agg,
        x='Region',
        y=['Total Cost', 'Average Session Cost'],
        barmode='group',
        text_auto='.2s',
        color_discrete_sequence=color_sequence,
        template=template,
        title="Regional Cost Analysis: Total vs Average"
    )
    fig_bar_group.update_layout(margin=dict(l=50, r=50, t=80, b=50))
    charts['region_bar_group'] = fig_bar_group

    # 4. Regional Activity: Sessions & Clients (Grouped Bar)
    region_activity = df.groupby('Region').agg({
        'Session_ID': 'nunique',
        'Client Name': 'nunique'
    }).reset_index()
    region_activity.columns = ['Region', 'Session Count', 'Client Count']
    region_activity = region_activity.sort_values('Session Count', ascending=False)
    
    fig_region_activity = px.bar(
        region_activity,
        x='Region',
        y=['Session Count', 'Client Count'],
        barmode='group',
        title="Regional Activity: Sessions & Clients",
        color_discrete_sequence=color_sequence,
        template=template,
        text_auto=True
    )
    fig_region_activity.update_layout(margin=dict(l=50, r=50, t=80, b=50))
    charts['region_activity'] = fig_region_activity
    
    return charts

def generate_trainer_charts(df, color_sequence, template):
    """Generates charts for the Trainer Analysis tab."""
    charts = {}
    
    # 1. Trainer Expenses by Payment Method (Grouped Bar)
    trainer_payment = df.groupby(['Name of Trainer', 'Payment Type'])['Cost'].sum().reset_index()
    trainer_order = df.groupby('Name of Trainer')['Cost'].sum().sort_values(ascending=False).index
    
    fig_grouped = px.bar(
        trainer_payment,
        x='Name of Trainer',
        y='Cost',
        color='Payment Type',
        barmode='group',
        title="Trainer Expenses by Payment Method",
        color_discrete_sequence=color_sequence,
        template=template,
        text_auto='.2s'
    )
    fig_grouped.update_layout(
        xaxis={'categoryorder':'array', 'categoryarray': trainer_order},
        yaxis_title="Cost (Rs.)",
        margin=dict(l=50, r=50, t=80, b=50)
    )
    charts['trainer_payment'] = fig_grouped

    # 2. Regional-Trainer Cost Heatmap
    pivot_table = df.pivot_table(
        index='Region', 
        columns='Name of Trainer', 
        values='Cost', 
        aggfunc='sum',
        fill_value=0
    )
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=pivot_table.values,
        x=pivot_table.columns,
        y=pivot_table.index,
        colorscale='Viridis',
        text=pivot_table.values,
        texttemplate="%{text:.0f}"
    ))
    fig_heatmap.update_layout(
        title="Regional-Trainer Cost Heatmap",
        xaxis_title="Trainers",
        yaxis_title="Regions",
        template=template,
        margin=dict(l=50, r=50, t=80, b=50)
    )
    charts['trainer_heatmap'] = fig_heatmap

    # 3. Trainer Cost Efficiency (Line)
    trainer_stats = df.groupby('Name of Trainer').agg({
        'Cost': 'sum',
        'Session_ID': 'nunique',
        'Date': lambda x: (x.max() - x.min()).days / 7 if (x.max() - x.min()).days > 0 else 1
    })
    trainer_stats.columns = ['Total Cost', 'Session Count', 'Weeks']
    trainer_stats['Average Cost'] = trainer_stats['Total Cost'] / trainer_stats['Session Count']
    trainer_stats['Average Weekly Cost'] = trainer_stats['Total Cost'] / trainer_stats['Weeks']
    trainer_stats_plot = trainer_stats.reset_index()
    
    trainer_melted = trainer_stats_plot.melt(
        id_vars='Name of Trainer',
        value_vars=['Average Cost', 'Average Weekly Cost'],
        var_name='Metric',
        value_name='Cost'
    )
    fig_avg_comp = px.line(
        trainer_melted,
        x='Name of Trainer',
        y='Cost',
        color='Metric',
        markers=True,
        title="Trainer Cost Efficiency: Avg Cost vs Weekly Cost",
        color_discrete_sequence=color_sequence,
        template=template,
        text='Cost'
    )
    fig_avg_comp.update_traces(
        textposition="top center",
        texttemplate='%{y:.2s}',
        textfont=dict(size=12, color='black', family='Arial'),
        mode='lines+markers+text'
    )
    fig_avg_comp.update_layout(margin=dict(l=50, r=50, t=80, b=50))
    charts['trainer_efficiency'] = fig_avg_comp

    # 4. Trainer Expense Distribution (Donut)
    fig_trainer_pie = px.pie(
        trainer_stats_plot,
        values='Total Cost',
        names='Name of Trainer',
        title="Trainer Expense Distribution",
        hole=0.5,
        color_discrete_sequence=color_sequence,
        template=template
    )
    fig_trainer_pie.update_traces(
        textposition='inside',
        texttemplate='%{percent}<br>Rs. %{value:.2s}',
        textfont=dict(size=12, color='white', family='Arial')
    )
    fig_trainer_pie.update_layout(
        showlegend=True, 
        legend=dict(orientation="v", yanchor="middle", y=0.5),
        margin=dict(l=50, r=50, t=80, b=50)
    )
    charts['trainer_pie'] = fig_trainer_pie

    # 5. Weekly Cost Trends by Trainer (Line)
    if not df.empty:
        temp_df = df.set_index('Date')
        weekly_trainer_costs = temp_df.groupby('Name of Trainer')['Cost'].resample('W-MON').sum().reset_index()
        
        fig_trainer_line = px.line(
            weekly_trainer_costs,
            x='Date',
            y='Cost',
            color='Name of Trainer',
            markers=True,
            labels={'Cost': 'Cost (Rs.)', 'Date': 'Week'},
            color_discrete_sequence=color_sequence,
            template=template,
            text='Cost',
            title="Weekly Cost Trends by Trainer",
            height=600
        )
        fig_trainer_line.update_traces(
            textposition="top center",
            texttemplate='%{y:.2s}',
            textfont=dict(size=12, color='black', family='Arial'),
            mode='lines+markers+text'
        )
        fig_trainer_line.update_layout(
            hovermode="x unified",
            margin=dict(l=50, r=50, t=80, b=50)
        )
        charts['trainer_trend'] = fig_trainer_line
        
    return charts

def generate_client_charts(df, color_sequence, template):
    """Generates charts for the Client Analysis tab."""
    charts = {}
    
    client_summary = df.groupby(['Region', 'Client Name']).agg({
        'Cost': 'sum',
        'Session_ID': 'nunique'
    }).reset_index()
    client_summary.columns = ['Region', 'Client Name', 'Total Cost', 'Session Count']
    client_summary = client_summary.sort_values('Total Cost', ascending=False)
    
    # 1. Client Cost Overview (Line)
    fig_line_client = px.line(
        client_summary,
        x='Client Name',
        y='Total Cost',
        markers=True,
        title="Client Cost Overview",
        color_discrete_sequence=color_sequence,
        template=template,
        text='Total Cost',
        height=600
    )
    fig_line_client.update_traces(
        textposition="top center",
        texttemplate='%{y:.2s}',
        textfont=dict(size=12, color='black', family='Arial'),
        mode='lines+markers+text'
    )
    fig_line_client.update_layout(margin=dict(l=50, r=50, t=80, b=50))
    charts['client_cost'] = fig_line_client

    # 2. Client Session Analysis (Scatter)
    fig_scatter_client = px.scatter(
        client_summary,
        x='Client Name',
        y='Session Count',
        size='Total Cost',
        color='Region',
        title="Client Session Analysis",
        color_discrete_sequence=color_sequence,
        template=template,
        height=600,
        text='Session Count'
    )
    fig_scatter_client.update_traces(
        textposition='top center',
        textfont=dict(size=12, color='black', family='Arial'),
        mode='markers+text'
    )
    fig_scatter_client.update_layout(margin=dict(l=50, r=50, t=80, b=50))
    charts['client_scatter'] = fig_scatter_client
    
    return charts

def generate_payment_charts(df, color_sequence, template):
    """Generates charts for the Payment Analysis tab."""
    charts = {}
    
    # 1. Payment Method Distribution (Pie)
    payment_dist = df.groupby('Payment Type')['Cost'].sum().reset_index()
    payment_dist = payment_dist.sort_values('Cost', ascending=False)
    
    fig_payment = px.pie(
        payment_dist,
        values='Cost',
        names='Payment Type',
        title='Payment Method Distribution',
        hole=0.5,
        color_discrete_sequence=color_sequence,
        template=template
    )
    fig_payment.update_traces(
        textposition='inside',
        texttemplate='%{percent}<br>Rs. %{value:.2s}',
        textfont=dict(size=12, color='white', family='Arial')
    )
    fig_payment.update_layout(
        showlegend=True, 
        legend=dict(orientation="v", yanchor="middle", y=0.5),
        margin=dict(l=50, r=50, t=80, b=50)
    )
    charts['payment_pie'] = fig_payment

    # 2. Payment Methods by Region (Stacked Bar)
    region_payment = df.groupby(['Region', 'Payment Type'])['Cost'].sum().reset_index()
    
    fig_pay_stack = px.bar(
        region_payment,
        x='Region',
        y='Cost',
        color='Payment Type',
        title="Payment Methods by Region",
        barmode='stack',
        color_discrete_sequence=color_sequence,
        template=template,
        text_auto='.2s'
    )
    fig_pay_stack.update_layout(margin=dict(l=50, r=50, t=80, b=50))
    charts['payment_stack'] = fig_pay_stack
    
    return charts
