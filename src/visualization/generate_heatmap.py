import os
import pandas as pd
import folium
from folium.plugins import HeatMap

# Get project root
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dataset_path = os.path.join(base_dir, "datasets", "kenya_emergencies.csv")

df = pd.read_csv(dataset_path)

# Nairobi center
m = folium.Map(location=[-1.286389, 36.817223], zoom_start=11)

# ALL emergencies layer
all_layer = folium.FeatureGroup(name="All Emergencies")

HeatMap(
    df[["latitude", "longitude"]].values.tolist(),
    radius=15
).add_to(all_layer)

all_layer.add_to(m)

# Individual emergency layers
types = df["type"].unique()

for t in types:

    layer = folium.FeatureGroup(name=t.capitalize())

    subset = df[df["type"] == t]

    HeatMap(
        subset[["latitude", "longitude"]].values.tolist(),
        radius=15
    ).add_to(layer)

    layer.add_to(m)
predicted_layer = folium.FeatureGroup(name="Predicted Risk Zones")

predicted_layer = folium.FeatureGroup(name="Predicted Hotspots")

for _, row in df.iterrows():

    folium.Circle(
        location=[row["latitude"], row["longitude"]],
        radius=200,
        color="red",
        fill=True,
        fill_opacity=0.4,
        popup=f"Predicted risk area: {row['area']}"
    ).add_to(predicted_layer)

predicted_layer.add_to(m)



predicted_layer.add_to(m)
# Add layer control
folium.LayerControl().add_to(m)

# Save map
m.save("heatmap.html")

print("Heatmap with layers generated")
