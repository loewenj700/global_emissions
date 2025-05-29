import pandas as pd
import plotly.graph_objects as go

# Load dataset
df = pd.read_csv("global_emissions.csv")

# Filter years 1980–2020
df_filtered = df[(df['Year'] >= 1980) & (df['Year'] <= 2020)]

# Sum total emissions per country across the selected years
top_countries = df_filtered.groupby("Country")["Total"].sum().nlargest(10).index.tolist()

# Filter data for top 10 countries
df_top10 = df_filtered[df_filtered["Country"].isin(top_countries)]

# Pivot data: rows = Year, columns = Country, values = Total emissions
df_pivot = df_top10.pivot_table(index="Year", columns="Country", values="Total", aggfunc="sum").fillna(0)

# Build stacked area chart
fig = go.Figure()

for country in df_pivot.columns:
    fig.add_trace(go.Scatter(
        x=df_pivot.index,
        y=df_pivot[country],
        mode='lines',
        stackgroup='one',
        name=country
    ))

fig.update_layout(
    title="Top 10 Countries by Total Emissions (1980–2020)",
    xaxis_title="Year",
    yaxis_title="Total Emissions (Million Metric Tons)",
    hovermode="x unified",
    legend_title="Country"
)

fig.show()
