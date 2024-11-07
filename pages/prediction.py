import streamlit as st


def prediction_page():

    tab1, tab2 = st.tabs(["Etiquette DPE", "COnsommation énergétique"])

    with tab1: 
        with st.form("form-classif"):
            annee = st.number_input("Année construction")
            surface = st.number_input("Surface habitable")
            cout_total = st.number_input("Cout total 5 usage")
            hauteur = st.number_input("Hauteur sous-plafond")
            nb_logement = st.number_input("Nombre niveau logement")

            type_batiment = st.selectbox(
                "Type bâtiment",
                ("maison", "immeuble"),
            )
            etiquette_dpe = st.selectbox(
                "Etiquette GES",
                ("A", "B", "C", "D", "E", "F", "G")
        
            )
            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")
            if submitted:
                st.write("submitted")

    with tab2: 
        with st.form("form-regression"):
            annee = st.number_input("Année construction")
            surface = st.number_input("Surface habitable")
            deperditions_enveloppe = st.number_input("Deperditions_enveloppe")
            deperditions_renouvellement_air = st.number_input("Déperditions_renouvellement_air")

            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")
            if submitted:
                st.write("submitted")
