# ********** affichage complet mais lent 40 secondes *************

# import streamlit as st

# # Path to the saved map.html file
# map_path = "C:/Users/yacin/Desktop/projet_python/map.html"

# # Cache the HTML map file loading function
# @st.cache_resource
# def load_map(path):
#     with open(path, "r") as file:
#         return file.read()

# # Load the cached HTML map content
# html_map = load_map(map_path)

# # Display the HTML map
# st.components.v1.html(html_map, height=600)

import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster

# Path to the data
data_path = "data/processed/data_map.csv"

# Load the dataframe
df = pd.read_csv(data_path, sep=";")

# Function to get a random sample of the data
def generate_sample(df, num_points=100):
    return df.sample(n=num_points, random_state=42)

# Function to generate a folium map with the sample data
def create_map(df_sample):
    # Coordinates of Rennes (Brittany)
    rennes_lat, rennes_lon = 48.1173, -1.6778

    # Create the map centered on Rennes
    carte_bretagne = folium.Map(location=[rennes_lat, rennes_lon], zoom_start=8)

    # Initialize the MarkerCluster object
    marker_cluster = MarkerCluster().add_to(carte_bretagne)

    # Add markers for each property in the sample
    for idx, row in df_sample.iterrows():
        if pd.notna(row['lat']) and pd.notna(row['lon']):
            popup = f"Type de bâtiment: {row['Type_bâtiment']}<br>Surface habitable: {row['Surface_habitable_logement']} m²<br>Étiquette DPE : {row['Etiquette_DPE']}"
            
            # Create a marker for each property and add it to the marker cluster
            folium.Marker(
                location=[row['lat'], row['lon']],
                popup=popup
            ).add_to(marker_cluster)

    return carte_bretagne

# Streamlit interface
st.title("Carte Interactive avec Échantillon de Données")

# Generate a random sample of the data (e.g., 100 points)
df_sample = generate_sample(df, num_points=500)

# Create the map with the sample data
carte_bretagne = create_map(df_sample)

# Display the map in Streamlit
st.write("Voici un échantillon des données sur la carte :")
st.components.v1.html(carte_bretagne._repr_html_(), height=600)
