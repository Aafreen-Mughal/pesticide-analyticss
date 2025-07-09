# generate_graphs.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import pycountry

df = pd.read_csv("pesticides.csv")
df = df.dropna(subset=['Value'])
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

# Global usage
total_by_year = df.groupby('Year')['Value'].sum().reset_index()
plt.figure(figsize=(12, 6))
sns.lineplot(x='Year', y='Value', data=total_by_year)
plt.title("Global Pesticide Usage Over Years")
plt.xlabel("Year")
plt.ylabel("Total Usage (tonnes)")
plt.grid(True)
plt.tight_layout()
plt.savefig("global_pesticide_trend.png")
plt.close()

# Heatmap
pivot = df.pivot_table(values='Value', index='Area', columns='Year', aggfunc='sum').fillna(0)
plt.figure(figsize=(14, 10))
sns.heatmap(pivot, cmap='YlGnBu')
plt.title("Pesticide Usage by Country (Heatmap)")
plt.tight_layout()
plt.savefig("pesticide_usage_heatmap.png")
plt.close()

# Folium map
latest = df[df['Year'] == df['Year'].max()].copy()
def get_iso(name):
    try:
        return pycountry.countries.lookup(name).alpha_3
    except:
        return None
latest['ISO'] = latest['Area'].apply(get_iso)
m = folium.Map(location=[20, 0], zoom_start=2)
for _, row in latest.iterrows():
    tooltip = f"{row['Area']}: {row['Value']} tonnes"
    folium.CircleMarker(location=[0, 0], popup=tooltip, radius=4, color='blue', fill=True).add_to(m)
m.save("latest_year_map.html")
