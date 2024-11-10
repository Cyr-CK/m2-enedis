import streamlit as st
import pipeline
import pickle as pk
import pandas as pd

Etiquette_GES = st.selectbox('Etiquette_GES', ["A", "B","C","D", "E", "F", "G"])
Logement = st.selectbox('Logement', ["ancien", "neuf"])
Type_bâtiment = st.selectbox('Type_bâtiment', ['appartement', 'maison', 'immeuble'])
Année_construction = st.text_input('Année_construction')
Code_postal = st.text_input('Code_postal_(brut)')
Coût_total_5_usages = st.text_input('Coût_total_5_usages')
Hauteur_sous_plafond = st.text_input('Hauteur_sous-plafond')
Nombre_niveau_logement = st.text_input('Nombre_niveau_logement')
Surface_habitable_logement = st.text_input('Surface_habitable_logement')




data = {
"Etiquette_GES": Etiquette_GES,
"Logement": Logement,
"Type_bâtiment": Type_bâtiment,
"Année_construction": pd.to_numeric(Année_construction, errors='coerce'),
"Code_postal_(brut)": pd.to_numeric(Code_postal, errors='coerce'),
"Coût_total_5_usages": pd.to_numeric(Coût_total_5_usages, errors='coerce'),
"Hauteur_sous-plafond": pd.to_numeric(Hauteur_sous_plafond, errors='coerce'),
"Nombre_niveau_logement": pd.to_numeric(Nombre_niveau_logement, errors='coerce'),
"Surface_habitable_logement": pd.to_numeric(Surface_habitable_logement, errors='coerce')
}

# Convert data to DataFrame
df = pd.DataFrame([data])

st.markdown("""
    <style>
    .stButton > button {
        background-color: #4CAF50;  /* Background color */
        color: white;               /* Text color */
        border-radius: 10px;        /* Rounded corners */
        padding: 8px;              /* Padding */
        font-size: 16px;            /* Font size */
        font-weight: bold;          /* Bold text */
    }
    .stButton > button:hover {
        background-color: #45a049; /* Hover color */
        color: white;               /* Hover text color */
    }
    </style>
""", unsafe_allow_html=True)

if st.button("get result"):  
    result = pipeline.Pipeline_classification(df)
    st.success(result)




