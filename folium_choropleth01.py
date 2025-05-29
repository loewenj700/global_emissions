import pandas as pd
import folium
import json

# Load emissions dataset
df = pd.read_csv("global_emissions.csv")

# Filter for 1970–2020
df_pc = df[(df['Year'] >= 1970) & (df['Year'] <= 2020)]

# Compute average per-capita emissions by country
avg_pc_emissions = df_pc.groupby('Country')['Per Capita'].mean().reset_index()
avg_pc_emissions.columns = ['Country', 'Avg_Per_Capita_Emissions']

# Rename mismatched country names to match GeoJSON
rename_map = {
    'USA': 'United States of America'
}
avg_pc_emissions['Country'] = avg_pc_emissions['Country'].replace(rename_map)

# Load GeoJSON for world countries
with open("world-countries.json", "r", encoding="utf-8") as f:
    world_geo = json.load(f)

# Create Folium map
m = folium.Map(location=[20, 0], zoom_start=2, tiles="cartodbpositron")

# Add choropleth layer
choropleth = folium.Choropleth(
    geo_data=world_geo,
    data=avg_pc_emissions,
    columns=["Country", "Avg_Per_Capita_Emissions"],
    key_on="feature.properties.name",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Average Per-Capita Emissions (Metric Tons, 1970–2020)",
    nan_fill_color="gray"
).add_to(m)

# Tooltip for country names
folium.GeoJsonTooltip(fields=["name"]).add_to(choropleth.geojson)

# Save to HTML file
m.save("avg_per_capita_emissions_map.html")
