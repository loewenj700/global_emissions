import pandas as pd
import plotly.graph_objects as go

# Load the dataset
df = pd.read_csv("global_emissions.csv")

# Filter for the years 1980–2020
df_filtered = df[(df['Year'] >= 1980) & (df['Year'] <= 2020)]

# Calculate average per-capita emissions per country over the period
top_countries_pc = df_filtered.groupby("Country")["Per Capita"].mean().nlargest(10).index.tolist()

# Filter data for these top countries
df_top10_pc = df_filtered[df_filtered["Country"].isin(top_countries_pc)]

# Pivot the data for line chart plotting
df_pivot_pc = df_top10_pc.pivot_table(index="Year", columns="Country", values="Per Capita", aggfunc="mean").fillna(0)

# Create the Plotly line chart
fig = go.Figure()

for country in df_pivot_pc.columns:
    fig.add_trace(go.Scatter(
        x=df_pivot_pc.index,
        y=df_pivot_pc[country],
        mode='lines',
        name=country
    ))

fig.update_layout(
    title="Top 10 Countries by Per-Capita Emissions (1980–2020)",
    xaxis_title="Year",
    yaxis_title="Per-Capita Emissions (Metric Tons per Person)",
    legend_title="Country",
    hovermode="x unified"
)

fig.show()
