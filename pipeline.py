def Pipeline(new_data):
    import pickle as pk
    import pandas as pd
    import os

       
    with open(os.path.join("objects","OHE.pkl"), "rb") as file:
        encoder = pk.load(file)
    file.close()

    quali_vars = ["Etiquette_GES", "Logement", "Type_bâtiment"]
    quali_OHE = encoder.transform(new_data[quali_vars]).toaray()
    quali_OHE_df = pd.DataFrame(quali_OHE, index=new_data.index, columns=encoder.get_feature_names_out(quali_vars))

    quanti = new_data[new_data.columns.difference(quali_vars)]

    new_data = pd.concat([quanti, quali_OHE_df], axis=1)

    with open(os.path.join("models","rf_tuned_classification.pkl"), "rb") as file:
            model = pk.load(file)
    file.close()

    pred = model.predict(new_data)
    print(pred)