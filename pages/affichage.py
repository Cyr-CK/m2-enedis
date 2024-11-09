import streamlit as st
import pandas as pd

# Titre de la page
st.title("Affichage des Données")

# Charger les données
data_path = "processed/full_data_bretagne.csv"
@st.cache_data
def load_data(path):
    return pd.read_csv(path, sep=";")

# Afficher les données avec une option de cacher
data = load_data(data_path)
if st.checkbox("Afficher les données"):
    st.dataframe(data)

# Optionnel : affichage de statistiques descriptives
if st.checkbox("Afficher les statistiques descriptives"):
    st.write(data.describe())
