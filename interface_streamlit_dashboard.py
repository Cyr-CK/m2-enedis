import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import os

import warnings
warnings.filterwarnings("ignore")

# Page setting
st.set_page_config(layout="wide", page_title="Prédiction de la consommation énergétique des logement en Bretagne")

# with open('styles.css') as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


################################################################################
#################### Préparation data pour dashboard ###########################
################################################################################

#chargement des données
os.chdir("C:/Users/habib/Desktop/Master_SISE/Projets/python_enedis")
nom_fichier = "data_classification.csv"
df = pd.read_csv(nom_fichier,sep=";")

# Utilisation du code postal pour créer une colonne 'Département'
departements_bretagne = {
    22: "Côtes-d'Armor",
    29: "Finistère",
    35: "Ille-et-Vilaine",
    56: "Morbihan"
}
df['Département'] = df['Code_postal_(brut)'].astype(str).str[:2].astype(int)
df['Département'] = df['Département'].replace(departements_bretagne)

# Nettoyage des codes postaux incohérents (hors Bretagne)
departements_a_garder = ["Côtes-d'Armor", "Finistère", "Ille-et-Vilaine", "Morbihan"]
df = df[df['Département'].isin(departements_a_garder)]

# Filtre sur la surface totale logement (pour retirer les outflyers)
df = df[df['Surface_habitable_logement'] <= 7000]

# Filtre sur l'année de construction (valeurs incohérentes)
df = df[df['Année_construction'] <= 2024]

# Ligne incohérente retirée
df = df[~((df['Coût_total_5_usages'] > 100000) & (df['Type_bâtiment'] == 'maison'))]

# Création d'une variable 'Cout/m²'
df['Coût/m²']=df['Coût_total_5_usages']/df['Surface_habitable_logement']



####################################################################################
########### Menu latéral (navigation entre les pages) ##############################
####################################################################################

# sidebar menu
with st.sidebar:
    page = option_menu("Menu", ["[contexte du projet]", "Tableau de bord","Cartographie interactive","[prédictions]"], 
        icons=['book', 'bar-chart-fill','geo-alt','calculator'], 
          menu_icon="house", 
            default_index=1)

#####################################################################################
########################## Contenu de chaque page ################################## 
#####################################################################################


# Page de contexte ===================================================================================================
if page == "[contexte du projet]":
    st.header("Contexte du projet")
    st.write("En France, la maîtrise de la consommation énergétique est devenue un enjeu majeur, tant pour les ménages que pour les fournisseurs d’énergie. Dans un contexte de hausse des coûts et de transition écologique, vos clients cherchent à mieux comprendre et optimiser leurs usages pour réduire leur facture et leur impact environnemental. Greentech vous propose une solution web innovante pour répondre à ces attentes.Notre interface comprend un dashboard interactif qui permet à vos clients de visualiser en temps réel leur consommation énergétique, de l’analyser, et d’identifier les pistes d’économies. En complément, notre outil de prédiction basé sur des algorithmes avancés utilise les données historiques pour anticiper les pics de consommation et proposer des recommandations personnalisées. Grâce à Greentech, offrez à vos clients une expérience enrichie et accompagnez-les vers une gestion énergétique plus responsable et optimisée")




# Page de data visualisation =================================================================================================================
    st.header("Tableau de bord")
    st.markdown("Cette page propose une visualisation interactive de différentes données d'intérêt sur la région Bretagne.\n\nDes filtres sont applicables, et il est possible de télécharger les graphiques une fois filtrés.")
    
    # Disposition des graphiques sur la page : on choisit 2 colonnes
    colonnes_dashboard = st.columns([1,1])
  
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
    
    # Graphique n°1 - barres empilées ---------------------------------------------------------------------------------------------------------

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

    # Graphique n°2 - scatter plot  -------------------------------------------------------------------------------------

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
        file_name="graphique_euros par m² selon surface.png",
        mime="image/png"
    )

    # Graphique n°3 - line plot --------------------------------------------------------------------------------------------
    
    with colonnes_dashboard[1]:   
        # Widget de sélection multiple pour la classe DPE
        etiquette_dpe_3 = st.multiselect(
        "Sélectionnez les classes DPE",
        options=["A", "B", "C", "D", "E", "F", "G"],
        default=["A", "B", "C", "D", "E", "F", "G"],
        label_visibility="hidden"
        )

        # Filtrer les données en fonction de la sélection
        df_filtre_3 = df[df['Etiquette_DPE'].isin(etiquette_dpe_3)]

        # Calculer le coût moyen par année de construction pour la classe sélectionnée
        df_agg_3 = df_filtre_3.groupby(['Année_construction', 'Etiquette_DPE']).agg({'Coût/m²': 'mean'}).reset_index()

        # Créer un histogramme avec Plotly Express
        fig_3 = px.line(
            df_agg_3, 
            x="Année_construction", 
            y="Coût/m² moyen",
            color='Etiquette_DPE',
            range_x=[1900,2024], 
            title=f"Dépenses énergétiques par mêtre² (en €) en fonction de l'année de construction",
            labels={"Année_construction": "Année de Construction", "Coût/m²": "Coût/m²"},
            )

        # Appliquer les couleurs personnalisées des classes DPE sélectionnées
        for trace in fig_3.data:
            # Appliquer la couleur à chaque trace (ligne) basée sur l'étiquette DPE
            trace.line.color = couleurs_DPE[trace.name]

        # Afficher le graphique dans la deuxième colonne
        st.plotly_chart(fig_3)  

        # Convertir le graphique en image PNG
        img_bytes_3 = fig_3.to_image(format="png")

        # Créer un bouton de téléchargement pour l'image PNG
        st.download_button(
            label="Télécharger - Dépense €/m² selon l'année de construction",
            data=img_bytes_3,
            file_name="graphique_Euros par m² selon l'année.png",
            mime="image/png"
        )

    # Graphique n°4 - Treemap ------------------------------------------------------------------------------------------------

        # Calcul de la moyenne de 'Coût/m²' par 'Etiquette_DPE' et 'Département'
        df_agg_4 = df.groupby(['Etiquette_DPE', 'Département']).agg({'Coût/m²': 'mean'}).reset_index()
        # Ajouter une colonne de couleurs basée sur 'Etiquette_DPE'
        df_agg_4['Couleur'] = df_agg_4['Etiquette_DPE'].map(couleurs_DPE)
        # Créer un treemap avec Plotly Express
        fig_4 = px.treemap(
            df_agg_4, 
            path=['Etiquette_DPE', 'Département'],  # Catégories principales et sous-catégories
            values='Coût/m²',  # Taille des rectangles basée sur la moyenne du Coût/m²
            title="Coût/m² moyen par Etiquette DPE et Département",
            color='Etiquette_DPE',  # Utilisation de la colonne Etiquette_DPE pour la coloration
            color_discrete_map=couleurs_DPE  # Appliquer le dictionnaire de couleurs personnalisé
            )
        # Afficher le graphique dans la deuxième colonne
        st.plotly_chart(fig_4)
    
        # Convertir le graphique en image PNG
        img_bytes_4 = fig_4.to_image(format="png")

        # Créer un bouton de téléchargement pour l'image PNG
        st.download_button(
            label="Télécharger - Dépense €/m² moyenne selon DPE",
            data=img_bytes_4,
            file_name="graphique_Euros par m² selon DPE.png",
            mime="image/png"
        )


# Page cartographie ===============================================================================================================
elif page == "Cartographie interactive":
    st.header("Carte")
    st.write("xxxx")















# Page de prédiction ================================================================================================================
elif page == "[prédictions]":
    st.header("Prédictions de l'étiquette DPE et de la consommation d'énergie")
    st.write("xxxx")
