import streamlit as st


# Page setting
st.set_page_config(layout="wide", page_title="Prédiction de la consommation énergétique des logement en Bretagne")

# with open('styles.css') as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


import warnings
warnings.filterwarnings("ignore")

st.header("Contexte du projet")
st.write("En France, la maîtrise de la consommation énergétique est devenue un enjeu majeur, tant pour les ménages que pour les fournisseurs d’énergie. Dans un contexte de hausse des coûts et de transition écologique, vos clients cherchent à mieux comprendre et optimiser leurs usages pour réduire leur facture et leur impact environnemental. Greentech vous propose une solution web innovante pour répondre à ces attentes.Notre interface comprend un dashboard interactif qui permet à vos clients de visualiser en temps réel leur consommation énergétique, de l’analyser, et d’identifier les pistes d’économies. En complément, notre outil de prédiction basé sur des algorithmes avancés utilise les données historiques pour anticiper les pics de consommation et proposer des recommandations personnalisées. Grâce à Greentech, offrez à vos clients une expérience enrichie et accompagnez-les vers une gestion énergétique plus responsable et optimisée")
