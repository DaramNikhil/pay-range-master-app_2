import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.io as pio

def create_salary_structure_bar_chart(df_results):
    # Sort by Grade ascending
    df_plot = df_results.sort_values('Grade', ascending=True).reset_index(drop=True)
    
    # Ensure that 'Range Min' and 'Range Max' are numeric
    df_plot['Range Min'] = pd.to_numeric(df_plot['Range Min'], errors='coerce')
    df_plot['Range Max'] = pd.to_numeric(df_plot['Range Max'], errors='coerce')

    # Grades as integers
    grades = df_plot['Grade'].astype(int)
    
    # Extract the Range Min, Mid, Max
    range_min = df_plot['Range Min']
    range_mid = df_plot['Range Mid']
    range_max = df_plot['Range Max']

    # Create figure with 'Simple White' template
    fig = go.Figure(layout=go.Layout(template='simple_white'))

    # Add invisible bars from 0 to Range Min (dummy bars)
    fig.add_trace(go.Bar(
        x=grades,
        y=range_min,
        marker_color='rgba(0,0,0,0)',  # Invisible bars
        hoverinfo='skip',              # Exclude from tooltip
        showlegend=False
    ))

    # Add bars from Range Min to Range Max (actual salary range)
    fig.add_trace(go.Bar(
        x=grades,
        y=range_max - range_min,
        base=range_min,
        marker_color='rgba(119, 152, 191, 0.7)',  # Light blue
        name='Pay Range',
        customdata=np.stack((range_mid,), axis=-1),
        hovertemplate='Min: %{base:,.0f}<br>Mid: %{customdata[0]:,.0f}<br>Max: %{y:,.0f}<extra></extra>'
    ))

    # Add midpoints as a line connecting markers
    fig.add_trace(go.Scatter(
        x=grades,
        y=range_mid,
        mode='lines+markers',
        line=dict(color='green', width=2),
        marker=dict(color='green', size=8),
        name='Midpoint',
        hoverinfo='skip'  # Hover info is included in the bar's tooltip
    ))

    # Update hover label styling
    fig.update_traces(hoverlabel=dict(
        bgcolor='rgba(255,255,204,0.9)',  # Light yellow background
        font_size=12,
        font_color='black'
    ))

    # Update layout
    fig.update_layout(
        title='Pay Progression',
        xaxis_title='Grade',
        yaxis_title='Base Pay',
        yaxis_tickformat=',.0f',
        xaxis=dict(
            tickmode='linear',
            tick0=grades.min(),
            dtick=1,
            categoryorder='array',
            categoryarray=grades
        ),
        legend_title='',
        hovermode='x',
        barmode='stack'  # Stack the bars
    )

    # Show the figure
    fig.show()



def create_salary_structure_bar_chart_2(df_results_2):
    df = st.session_state.row_data
    merged_df = pd.merge(df, df_results_2[['Grade', 'Range_Min', 'Mid', 'Range_Max']], on='Grade', how='left')

    # Ensure that the grades are in ascending order for plotting
    df_results_2 = df_results_2.sort_values('Grade')

    # Create the figure
    fig = go.Figure()

    # Prepare customdata array for the salary data points
    customdata = np.stack((
    merged_df['Employee ID'],
    merged_df['Base Pay'],
    merged_df['Range_Min'],
    merged_df['Mid'],
    merged_df['Range_Max']
    ), axis=-1)

    # Add individual salary data points with merged tooltips
    fig.add_trace(go.Scatter(
    x=merged_df['Grade'],
    y=merged_df['Base Pay'],
    mode='markers',
    name='Salaries',
    marker=dict(color='blue', size=6, opacity=0.6),
    customdata=customdata,
    hovertemplate=(
        '<b>Employee ID</b>: %{customdata[0]}<br>'
        '<b>Base Pay</b>: %{customdata[1]:,}<br>'
        '<b>Range Min</b>: %{customdata[2]:,}<br>'
        '<b>Mid</b>: %{customdata[3]:,}<br>'
        '<b>Range Max</b>: %{customdata[4]:,}<extra></extra>'
    ),
    hoverlabel=dict(
        bgcolor="rgba(255, 255, 255, 0.9)",  # Light background with less transparency
        bordercolor="rgba(0, 0, 0, 0)",       # No border
        font=dict(color='black')              # Black text for visibility
    )
    ))

    # Get unique grades in ascending order
    grades = sorted(df_results_2['Grade'].unique())

    # Prepare horizontal lines for Range_Min, Mid, and Range_Max
    for idx, grade in enumerate(grades):
        # Define the x-range for the horizontal lines around each grade
        x_start = grade - 0.3
        x_end = grade + 0.3
        x_vals = np.linspace(x_start, x_end, num=10)  # Increase number of points

        # Extract the Range Min, Mid, and Max for the current grade
        range_min = df_results_2.loc[df_results_2['Grade'] == grade, 'Range_Min'].values[0]
        mid = df_results_2.loc[df_results_2['Grade'] == grade, 'Mid'].values[0]
        range_max = df_results_2.loc[df_results_2['Grade'] == grade, 'Range_Max'].values[0]

        # Add horizontal line for Range Min (green, solid line)
        fig.add_trace(go.Scatter(
            x=x_vals,
            y=[range_min]*len(x_vals),
            mode='lines',
            line=dict(color='green', width=1),  # Green solid line
            name='Range Min' if idx == 0 else None,  # Show legend only once
            hoverinfo='skip',
            showlegend=(idx == 0)
        ))

    # Add horizontal line for Mid (orange, dotted line)
    fig.add_trace(go.Scatter(
        x=x_vals,
        y=[mid]*len(x_vals),
        mode='lines',
        line=dict(color='orange', dash='dot', width=1),  # Dotted line
        name='Mid' if idx == 0 else None,
        hoverinfo='skip',
        showlegend=(idx == 0)
    ))

    # Add horizontal line for Range Max (green, solid line)
    fig.add_trace(go.Scatter(
        x=x_vals,
        y=[range_max]*len(x_vals),
        mode='lines',
        line=dict(color='green', width=1),  # Green solid line
        name='Range Max' if idx == 0 else None,
        hoverinfo='skip',
        showlegend=(idx == 0)
    ))

    # Update layout
    fig.update_layout(
    title='Employee Distribution Across Pay Ranges',
    xaxis_title='Grade',
    yaxis_title='Base Pay',
    xaxis=dict(
        tickmode='array',
        tickvals=grades,
        ticktext=[str(grade) for grade in grades],
        dtick=1,
        gridcolor='lightgrey',
        zerolinecolor='lightgrey'
    ),
    yaxis=dict(
        gridcolor='lightgrey',
        zerolinecolor='lightgrey'
    ),
    legend=dict(
        title='Legend',
        bordercolor='black',
        borderwidth=.5
    ),
    hovermode='closest',
    width=900,
    height=600,
    font=dict(
        family='Arial',
        size=10
    )
    )

    # Show the plot
    fig.show()

