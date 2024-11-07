import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards
import pandas as pd
import os



# def visualisation_page():
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "processed", "full_data_bretagne.csv")
data = pd.read_csv(file_path, sep=";")


col1, col2, col3 = st.columns(3)

col1.metric(label="Nombre logements", value=data.shape[0])
col2.metric(label="Moyenne consommation énergétique", value=data["Coût_total_5_usages"].mean())
col3.metric(label="Moyenne surface habitable", value=data["Surface_habitable_logement"].mean())

style_metric_cards(background_color="#b84916", border_radius_px=0, border_left_color=None, border_color=None)

pie_etiquette, graph_conso = st.columns(2)
with pie_etiquette:
    if 'Etiquette_DPE' in data.columns:
            # Calcul des proportions
            counts = data['Etiquette_DPE'].value_counts().reset_index()
            counts.columns = ['Etiquette_DPE', 'Nombre']
            
            # Créer un pie chart avec Plotly
            fig = px.pie(
                counts,
                values='Nombre',
                names='Etiquette_DPE',
                title='Répartition des Etiquettes DPE',
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            
            # Afficher le pie chart
            st.plotly_chart(fig)
        
with graph_conso:
    if 'Coût_total_5_usages' in data.columns and 'Surface_habitable_logement' in data.columns:
        
        # Créer un scatter plot avec Plotly
        fig = px.scatter(
            data,
            x='Surface_habitable_logement',
            y='Coût_total_5_usages',
            title="Coût total des 5 usages par Surface habitable",
            labels={'Surface_habitable_logement': 'Surface Habitable (m²)', 
                    'Coût_total_5_usages': 'Coût Total des 5 Usages (€)'},
            trendline="ols",  # Ajoute une ligne de tendance
            color_discrete_sequence=["#636EFA"]
        )

        st.plotly_chart(fig)