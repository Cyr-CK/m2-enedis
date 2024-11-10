import streamlit as st
import pandas as pd

# Titre de la page
st.title("Affichage des Données")

# Charger les données
data_path = "data/processed/data_classification.csv"
@st.cache_data
def load_data(path):
    return pd.read_csv(path, sep=";")

# Afficher les données avec une option de cacher
df = load_data(data_path)
if st.checkbox("Afficher les données originales"):
    # Afficher le dataframe de base
    st.dataframe(df)

# Récupérer les valeurs uniques de 'Type_bâtiment'
type_batiment_options = df['Type_bâtiment'].unique()

# Créer une liste vide pour stocker les types sélectionnés
selected_types = []

# Disposer les checkboxes côte à côte pour le type de bâtiment
st.write("Filtrer par type de bâtiment :")
columns = st.columns(len(type_batiment_options))  # Crée une colonne pour chaque type unique
for i, type_batiment in enumerate(type_batiment_options):
    if columns[i].checkbox(type_batiment):
        selected_types.append(type_batiment)

# Filtre par étiquette DPE (multiselect)
dpe_options = df['Etiquette_DPE'].unique()  # Valeurs uniques de l'étiquette DPE
selected_dpe = st.multiselect("Sélectionner les étiquettes DPE", dpe_options, default=dpe_options)

# Filtre par étiquette DPE (multiselect)
ges_options = df['Etiquette_GES'].unique()  # Valeurs uniques de l'étiquette GES
selected_ges = st.multiselect("Sélectionner les étiquettes DPE", ges_options, default=ges_options)


# Filtre par surface habitable (slider)
min_surface = int(df['Surface_habitable_logement'].min())
max_surface = int(df['Surface_habitable_logement'].max())
surface_habitable = st.slider("Surface habitable minimum (en m²)", min_value=min_surface, max_value=max_surface, value=(min_surface, max_surface))

# Filtre par Hauteur sous plafond  (slider)
min_hauteur = int(df['Hauteur_sous-plafond'].min())
max_hauteur = 2022
hauteur_sous_plafond = st.slider("Hauteur sous plafond (en m²)", min_value=min_hauteur, max_value=max_hauteur, value=(min_hauteur, max_hauteur))


# Appliquer les filtres
df_filtered = df.copy()

# Filtrer par type de bâtiment
if selected_types:
    df_filtered = df_filtered[df_filtered['Type_bâtiment'].isin(selected_types)]

# Filtrer par étiquette DPE
df_filtered = df_filtered[df_filtered['Etiquette_DPE'].isin(selected_dpe)]

# Filtrer par étiquette GES
df_filtered = df_filtered[df_filtered['Etiquette_GES'].isin(selected_ges)]

# Filtrer par surface habitable
df_filtered = df_filtered[(df_filtered['Surface_habitable_logement'] >= surface_habitable[0]) & (df_filtered['Surface_habitable_logement'] <= surface_habitable[1])]

# Filtrer par hateur sous plafond
df_filtered = df_filtered[(df_filtered['Hauteur_sous-plafond'] >= hauteur_sous_plafond[0]) & (df_filtered['Hauteur_sous-plafond'] <= hauteur_sous_plafond[1])]


# Affichage des résultats filtrés
st.write("Données filtrées", df_filtered)


st.markdown("""
    <style>
    .stDownloadButton > button {
        background-color: #4CAF50; /* Change background color */
        color: white;               /* Change text color */
        padding: 10px;              /* Add padding */
        border-radius: 8px;         /* Add rounded corners */
        font-weight: bold;          /* Bold text */
        font-size: 16px;            /* Increase font size */
    }
    .stDownloadButton > button:hover {
        background-color: #45a049; /* Hover color */
        color: white;               /* Hover text color */
    }
    </style>
""", unsafe_allow_html=True)

# Ajouter un bouton pour exporter les données filtrées en CSV
csv = df_filtered.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Exporter les données filtrées en CSV",
    data=csv,
    file_name="données_filtrées.csv",
    mime="text/csv"
)
