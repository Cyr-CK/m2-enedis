def Pipeline_classification(new_data):
    import pickle as pk
    import pandas as pd
    import os

       
    with open(os.path.join("objects","OHE_classification.pkl"), "rb") as file:
        encoder = pk.load(file)
    file.close()

    quali_vars = ["Etiquette_GES", "Logement", "Type_bâtiment"]
    quali_OHE = encoder.transform(new_data[quali_vars]).toarray()
    quali_OHE_df = pd.DataFrame(quali_OHE, index=new_data.index, columns=encoder.get_feature_names_out(quali_vars))
    quali_OHE_df = quali_OHE_df.drop(["Etiquette_GES_C","Logement_ancien","Type_bâtiment_appartement"], axis=1, )

    with open(os.path.join("objects","median_imputer_classification.pkl"), "rb") as file:
        imputer = pk.load(file)
    file.close()
    
    quanti_vars = ['Année_construction','Code_postal_(brut)','Coût_total_5_usages',
                   'Hauteur_sous-plafond','Nombre_niveau_logement','Surface_habitable_logement']
    quanti = new_data[quanti_vars]
    quanti_imputed = imputer.transform(quanti)
    quanti_imputed_df = pd.DataFrame(quanti_imputed, index=new_data.index, columns=imputer.get_feature_names_out(quanti_vars))

    new_data = pd.concat([quanti_imputed_df, quali_OHE_df], axis=1)

    with open(os.path.join("models","rf_tuned_classification.pkl"), "rb") as file:
            model = pk.load(file)
    file.close()

    pred = model.predict(new_data)
    print(pred)


def Pipeline_regression(new_data):
    import pickle as pk
    import pandas as pd
    import os

       
    with open(os.path.join("objects","OHE_regression.pkl"), "rb") as file:
        encoder = pk.load(file)
    file.close()

    quali_vars = ["Etiquette_DPE", "Logement", "Type_bâtiment"]
    quali_OHE = encoder.transform(new_data[quali_vars]).toarray()
    quali_OHE_df = pd.DataFrame(quali_OHE, index=new_data.index, columns=encoder.get_feature_names_out(quali_vars))
    quali_OHE_df = quali_OHE_df.drop(["Etiquette_DPE_C","Logement_ancien","Type_bâtiment_appartement"], axis=1)

    with open(os.path.join("objects","median_imputer_regression.pkl"), "rb") as file:
        imputer = pk.load(file)
    file.close()
    
    quanti_vars = ['Année_construction','Code_postal_(brut)',
                   'Hauteur_sous-plafond','Nombre_niveau_logement','Surface_habitable_logement']
    quanti = new_data[quanti_vars]
    quanti_imputed = imputer.transform(quanti)
    quanti_imputed_df = pd.DataFrame(quanti_imputed, index=new_data.index, columns=imputer.get_feature_names_out(quanti_vars))

    new_data = pd.concat([quanti_imputed_df, quali_OHE_df], axis=1)

    with open(os.path.join("models","rf_tuned_regression.pkl"), "rb") as file:
            model = pk.load(file)
    file.close()

    pred = model.predict(new_data)
    print(pred)