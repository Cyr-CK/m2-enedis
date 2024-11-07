def generate_map(data):
    import folium
    from folium.plugins import MarkerCluster
    import pandas as pd
    import os

    
    # Extraction des coordonnées géographiques et des indicateurs choisis
    locations = data[['lat', 'lon']]
    indicators = data[['Type_bâtiment','Surface_habitable_logement', 'Etiquette_DPE']]
    colors = {"A":"darkgreen","B":"green","C":"lightgreen","D":"beige","E":"orange","F":"pink","G":"red"}

    # Création d'une carte centrée sur le centre des coordonnées
    map_center = [locations['lat'].mean(), locations['lon'].mean()]
    map = folium.Map(location=map_center, zoom_start=12)

    # Création d'un cluster de marqueurs
    marker_cluster = MarkerCluster().add_to(map)

    # Ajout des marqueurs pour chaque logement avec les indicateurs choisis
    for i, row in data.iterrows():
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=f"Type de bâtiment: {row['Type_bâtiment']}<br>Surface habitable: {row['Surface_habitable_logement']} m²<br>Étiquette DPE : {row['Etiquette_DPE']}",
            icon=folium.Icon(color=colors[row['Etiquette_DPE']], icon='info-sign')
        ).add_to(marker_cluster)

    # Affichage et sauvegarde de la carte
    map.save(os.path.join('objects','map.html'))
    