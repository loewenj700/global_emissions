import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import folium
import json
from streamlit_folium import st_folium

# Load data
df = pd.read_csv("global_emissions.csv")
with open("world-countries.json", "r", encoding="utf-8") as f:
    world_geo = json.load(f)

st.set_page_config(layout="wide")
st.title("Global Emissions Dashboard (1980–2020)")

# --- STACKED AREA CHART (Top 10 by Total Emissions, 1980–2020) ---
df_total = df[(df['Year'] >= 1980) & (df['Year'] <= 2020)]
top_total = df_total.groupby("Country")["Total"].sum().nlargest(10).index.tolist()
df_top_total = df_total[df_total["Country"].isin(top_total)]
df_pivot_total = df_top_total.pivot_table(index="Year", columns="Country", values="Total", aggfunc="sum").fillna(0)

fig_area = go.Figure()
for country in df_pivot_total.columns:
    fig_area.add_trace(go.Scatter(
        x=df_pivot_total.index,
        y=df_pivot_total[country],
        mode='lines',
        stackgroup='one',
        name=country
    ))
fig_area.update_layout(
    title="Top 10 Countries by Total Emissions (1980–2020)",
    xaxis_title="Year",
    yaxis_title="Total Emissions (Million Metric Tons)",
    hovermode="x unified"
)

# --- LINE CHART (Top 10 by Per-Capita Emissions, 1980–2020) ---
df_pc = df[(df['Year'] >= 1980) & (df['Year'] <= 2020)]
top_pc = df_pc.groupby("Country")["Per Capita"].mean().nlargest(10).index.tolist()
df_top_pc = df_pc[df_pc["Country"].isin(top_pc)]
df_pivot_pc = df_top_pc.pivot_table(index="Year", columns="Country", values="Per Capita", aggfunc="mean").fillna(0)

fig_line = go.Figure()
for country in df_pivot_pc.columns:
    fig_line.add_trace(go.Scatter(
        x=df_pivot_pc.index,
        y=df_pivot_pc[country],
        mode='lines',
        name=country
    ))
fig_line.update_layout(
    title="Top 10 Countries by Per-Capita Emissions (1980–2020)",
    xaxis_title="Year",
    yaxis_title="Per-Capita Emissions (Metric Tons per Person)",
    hovermode="x unified"
)

# --- DISPLAY CHARTS SIDE-BY-SIDE ---
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_area, use_container_width=True)
with col2:
    st.plotly_chart(fig_line, use_container_width=True)

# --- FOLIUM CHOROPLETH MAP (Average Per-Capita Emissions, 1980–2020) ---
df_pc_map = df[(df['Year'] >= 1980) & (df['Year'] <= 2020)]
df_avg_pc = df_pc_map.groupby('Country')['Per Capita'].mean().reset_index()
df_avg_pc.columns = ['Country', 'Avg_Per_Capita_Emissions']

# Name alignment
rename_map = {
    'USA': 'United States of America',
}
df_avg_pc['Country'] = df_avg_pc['Country'].replace(rename_map)

# Build map
m = folium.Map(location=[20, 0], zoom_start=2, tiles="cartodbpositron")
choropleth = folium.Choropleth(
    geo_data=world_geo,
    data=df_avg_pc,
    columns=["Country", "Avg_Per_Capita_Emissions"],
    key_on="feature.properties.name",
    fill_color="OrRd",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Avg Per-Capita Emissions (1980–2020)",
    nan_fill_color="gray"
).add_to(m)
folium.GeoJsonTooltip(fields=["name"]).add_to(choropleth.geojson)

st.subheader("Average Per-Capita Emissions Map (1980–2020)")
st_folium(m, width=1200, height=600)
