import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import plotly.express as px

import warnings
warnings.filterwarnings("ignore")

# 1. as sidebar menu
with st.sidebar:
    page = option_menu("Menu", ["Contexte du projet", "Dashboard","Cartographie interactive","Prédictions"], 
        icons=['book', 'bar-chart-fill','geo-alt','calculator'], 
          menu_icon="house", 
            default_index=1)


### Contenu de chaque page ### -----------------------------------

# Page de contexte
if page == "Contexte du projet":
    st.header("Contexte du projet")
    st.write("En France, la maîtrise de la consommation énergétique est devenue un enjeu majeur, tant pour les ménages que pour les fournisseurs d’énergie. Dans un contexte de hausse des coûts et de transition écologique, vos clients cherchent à mieux comprendre et optimiser leurs usages pour réduire leur facture et leur impact environnemental. Greentech vous propose une solution web innovante pour répondre à ces attentes.Notre interface comprend un dashboard interactif qui permet à vos clients de visualiser en temps réel leur consommation énergétique, de l’analyser, et d’identifier les pistes d’économies. En complément, notre outil de prédiction basé sur des algorithmes avancés utilise les données historiques pour anticiper les pics de consommation et proposer des recommandations personnalisées. Grâce à Greentech, offrez à vos clients une expérience enrichie et accompagnez-les vers une gestion énergétique plus responsable et optimisée")





# Page de data visualisation
elif page == "Dashboard":
    st.header("Dashboard interactif")
    st.write("xxxxx")
    
    # Données pour le graphique
    labels = ['Catégorie A', 'Catégorie B', 'Catégorie C', 'Catégorie D']
    sizes = [25, 35, 20, 20]

    # Créer le graphique pie chart avec Plotly
    fig = px.pie(values=sizes, names=labels, title='Répartition des catégories')

    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig)
    



# Page cartographie
elif page == "Cartographie interactive":
    st.header("Carte")
    st.write("xxxx")



# Page de prédiction
elif page == "Prédictions":
    st.header("Prédictions de l'étiquette DPE et de la consommation d'énergie")
    st.write("xxxx")
