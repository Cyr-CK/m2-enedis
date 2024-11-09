import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import os

import warnings
warnings.filterwarnings("ignore")

# Page setting
st.set_page_config(layout="wide", page_title="Prédiction de la consommation énergétique des logement en Bretagne")

# with open('styles.css') as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)





#############################################
### Préparation data pour dashboard #########
#############################################

#chargement des données
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "processed", "full_data_bretagne.csv")
df = pd.read_csv(file_path, sep=";")

# Utilisation du code postal pour créer une colonne 'Département'
departements_bretagne = {
    22: "Côtes-d'Armor",
    29: "Finistère",
    35: "Ille-et-Vilaine",
    56: "Morbihan"
}



# Filtre sur la surface totale logement (pour retirer les outflyers)
df = df[df['Surface_habitable_logement'] <= 7000]
# Filtre sur l'année de construction (valeurs incohérentes)
df = df[df['Année_construction'] <= 2024]
# Ligne incohérente retirée
df = df[~((df['Coût_total_5_usages'] > 100000) & (df['Type_bâtiment'] == 'maison'))]

df['Département'] = df['Code_postal_(brut)'].astype(str).str[:2].astype(int)
df['Département'] = df['Département'].replace(departements_bretagne)
# Création d'une variable 'Cout/m²'
df['Coût/m²']=df['Coût_total_5_usages']/df['Surface_habitable_logement']



# sidebar menu
with st.sidebar:
    page = option_menu("Menu", ["[contexte du projet]", "Tableau de bord","[cartographie interactive]","[prédictions]"], 
        icons=['book', 'bar-chart-fill','geo-alt','calculator'], 
          menu_icon="house", 
            default_index=1)

##############################
### Contenu de chaque page ### 
##############################




# Page de contexte ===================================================================================================
if page == "[contexte du projet]":
    st.header("Contexte du projet")
    st.write("En France, la maîtrise de la consommation énergétique est devenue un enjeu majeur, tant pour les ménages que pour les fournisseurs d’énergie. Dans un contexte de hausse des coûts et de transition écologique, vos clients cherchent à mieux comprendre et optimiser leurs usages pour réduire leur facture et leur impact environnemental. Greentech vous propose une solution web innovante pour répondre à ces attentes.Notre interface comprend un dashboard interactif qui permet à vos clients de visualiser en temps réel leur consommation énergétique, de l’analyser, et d’identifier les pistes d’économies. En complément, notre outil de prédiction basé sur des algorithmes avancés utilise les données historiques pour anticiper les pics de consommation et proposer des recommandations personnalisées. Grâce à Greentech, offrez à vos clients une expérience enrichie et accompagnez-les vers une gestion énergétique plus responsable et optimisée")




# Page de data visualisation ------------------------------------------------------------------------------------------
elif page == "Tableau de bord":
    st.header("Tableau de bord")
    st.write("xxxxxxxxxxxxxxxxxxx")
    
    # CSS pour ajuster la largeur du multiselect
    st.markdown(
    """
    <style>
    /* Ajuste la largeur des widgets Multiselect */
    .stMultiSelect div[data-baseweb="select"] {
        width: 100% !important;
    }
    </style>
    """,
    unsafe_allow_html=True
    )


    # Disposition des graphiques sur la page : on choisit 2 colonnes
    colonnes_dashboard = st.columns([4,3])
  

    # Graphique n°1 - barres empilées ------------------------------------------------------------------------

    # Compter les occurrences de chaque combinaison de 'Département' et 'Etiquette_DPE'
    df_counts = df.groupby(['Département', 'Etiquette_DPE']).size().reset_index(name='Effectifs')

    # Créer un tableau croisé dynamique pour obtenir les effectifs par département et étiquette DPE
    df_pivot = df_counts.pivot_table(index='Département', columns='Etiquette_DPE', values='Effectifs', aggfunc='sum', fill_value=0)

    # Ajouter un widget de sélection multiple pour les départements
    with colonnes_dashboard[0]:
        departements = df_pivot.index.tolist()
        selected_departements = st.multiselect("Sélectionnez les départements à afficher", options=departements, default=departements)

    # Vérifier que la sélection n'est pas vide pour éviter les erreurs
    if selected_departements:
        # Filtrer les données en fonction des départements sélectionnés
        filtered_df_pivot = df_pivot.loc[selected_departements]

        # Définir une palette de couleurs personnalisée pour les étiquettes DPE
        couleurs_DPE = {
        "A": "#5A8C5B",
        "B": "#0AAE00",
        "C": "#C8D900",
        "D": "#FFEF51",
        "E": "#FFC54D",
        "F": "#FF7A01",
        "G": "#FF0028"
        }
       

        # Créer le graphique à barres empilées avec Plotly
        fig_1 = px.bar(
            filtered_df_pivot,
            x=filtered_df_pivot.index,
            y=filtered_df_pivot.columns,
            title="Etiquettes DPE selon les départements de Bretagne",
            labels={'value': 'Total des étiquettes', 'Département': 'Département', 'Etiquette_DPE': 'cliquer pour filtrer<br>les étiquettes DPE'},
            height=400,
            color_discrete_map=couleurs_DPE  # Appliquer les couleurs personnalisées
        )

        # Afficher le graphique dans Streamlit (colonne 0)
        colonnes_dashboard[0].plotly_chart(fig_1)

        # Convertir le graphique en image PNG
        img_bytes_1 = fig_1.to_image(format="png")

        # Créer un bouton de téléchargement pour l'image PNG
        st.download_button(
            label="Télécharger - Etiquettes DPE / département",
            data=img_bytes_1,
            file_name="graphique_dpe.png",
            mime="image/png"
        )

    else:
        st.write("Veuillez sélectionner au moins un département pour afficher le graphique.")

    # Graphique n°2 -   -------------------------------------------------------------------------------------

    fig_2 = px.scatter(
        df,
        x="Surface_habitable_logement",
        y="Coût/m²",
        range_x=(0,500),
        range_y=(0,125),
        color="Etiquette_DPE",
        color_discrete_map=couleurs_DPE,
        title="Coût en euros par m² selon la surface du logement",
        labels={"Surface_habitable_logement":"Surface du logement","Coût/m²":"Coût (en €) par m²",'Etiquette_DPE': 'cliquer pour filtrer<br>les étiquettes DPE'}
        )
    fig_2.update_traces(marker=dict(size=4))

    # Afficher le graphique dans Streamlit (colonne 0)
    colonnes_dashboard[0].plotly_chart(fig_2)

    # Convertir le graphique en image PNG
    img_bytes_2 = fig_2.to_image(format="png")

    # Créer un bouton de téléchargement pour l'image PNG
    st.download_button(
        label="Télécharger - Coût/m² selon la surface",
        data=img_bytes_2,
        file_name="graphique_dpe.png",
        mime="image/png"
    )

    # Graphique n°3 - KPI --------------------------------------------------------------------------------------------
    
    # Calcul du Coût/m² moyen pour chaque classe de 'Etiquette_DPE'
    moyennes = df.groupby("Etiquette_DPE")["Coût/m²"].mean().reset_index()

    # Affichage du KPI pour chaque classe d'Etiquette_DPE
    for index, row in moyennes.iterrows():
        st.metric(
            label=f"Coût/m² moyen pour {row['Etiquette_DPE']}",  # Nom de la classe DPE
            value=f"{row['Coût/m²']:.2f} €",  # Valeur arrondie à 2 décimales
            delta=None  # Pas de différence ici, mais tu peux ajouter un 'delta' si nécessaire
        )
    

    









# Page cartographie ===============================================================================================================
elif page == "[cartographie interactive]":
    st.header("Carte")
    st.write("xxxx")




# Page de prédiction ================================================================================================================
elif page == "[prédictions]":
    st.header("Prédictions de l'étiquette DPE et de la consommation d'énergie")
    st.write("xxxx")
