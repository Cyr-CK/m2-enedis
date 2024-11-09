import pandas as pd
import os


def select_columns(new_data, relevant_columns):

    new_data = new_data[relevant_columns]

    return new_data


def get_year_of_construct(value):
    year = int(value[:4])
    return year


def create_vars(new_data):
    if (not pd.Series(["Logement"]).isin(new_data.columns)[0]):
        new_data["Logement"] = 'neuf'

    if (not pd.Series(["Année_construction"]).isin(new_data.columns)[0]):
        from datetime import date
        new_data["Année_construction"] = new_data["Date_réception_DPE"].apply(get_year_of_construct)

    return new_data


# Pour les nouvelles données
def clean_and_convert(value):
    if pd.isna(value):  # Vérifie la présence de valeurs NaN ou de chaînes ' NaN'
        return value  # Préserve les NaN en tant que valeur None
    else:
        value = str(value).replace(',', '.')  # Remplace les virgules par des points
        return pd.to_numeric(value, errors='coerce')  # Conversion en valeur numérique
    


def data_split(data, target="Etiquette_DPE", test_size=0.3, stratify=True, seed=0):
    from sklearn.model_selection import train_test_split

    if stratify:
        return train_test_split(data, test_size=test_size, random_state=seed, stratify=data[target])
    else:
        return train_test_split(data, test_size=test_size, random_state=seed)
    


def quali_quanti_preprocessing_classif(original_data, new_data):
    import pandas as pd
    
    # QUALITATIVE PREPROCESSING

    # On remplace des adresses inconnues par la chaîne "inconnu"
    # new_data['Identifiant__BAN'] = new_data['Identifiant__BAN'].fillna('inconnu')
    # new_data['Nom__rue_(BAN)'] = new_data['Nom__rue_(BAN)'].fillna('inconnu')
    # new_data['Adresse_(BAN)'] = new_data['Adresse_(BAN)'].fillna('inconnu')
    # new_data['Adresse_brute'] = new_data['Adresse_brute'].fillna('inconnu')
    
    # Le code est encodé parfois en tant que chaîne ou entier. On uniformise en chaîne de caractères
    # original_data['Code_INSEE_(BAN)'] = original_data['Code_INSEE_(BAN)'].apply(lambda x: str(x) if pd.notna(x) else x)
    # new_data['Code_INSEE_(BAN)'] = new_data['Code_INSEE_(BAN)'].apply(lambda x: str(x) if pd.notna(x) else x)

    quali_data_new = new_data.select_dtypes(include=['object'])
    for column in quali_data_new.columns:
        # Calcul de la proportion (probabilité) des modalités dans chaque variable qualitative
        proportions = original_data[column].value_counts(normalize=True)
        
        # On applique la fonction à la colonne
        filling = proportions.sample(weights=proportions, replace=True).index[0]
        original_data[column] = original_data[column].fillna(filling)
        filling = proportions.sample(weights=proportions, replace=True).index[0]
        quali_data_new[column] = quali_data_new[column].fillna(filling)
        

        # if retrain:
        #     quali_data_orig = original_data.select_dtypes(include=['object'])
        #     quali_data_orig[column] = quali_data_orig.apply(impute_with_proportions, axis=1)
    

    # QUANTITATIVE PREPROCESSING
    ## Missing values
    from sklearn.impute import SimpleImputer
    quanti_data_new = new_data.select_dtypes(exclude=['object'])
    imputer = SimpleImputer(strategy="median")
    original_data[quanti_data_new.columns] = imputer.fit_transform(original_data[quanti_data_new.columns])
    quanti_data_new[quanti_data_new.columns] = imputer.transform(quanti_data_new)

    import pickle as pk
    pk.dump(imputer, open(os.path.join("objects", "median_imputer.pkl"), "wb"))
    
    new_data_processed = pd.concat([quali_data_new, quanti_data_new], axis=1)
    return original_data, new_data_processed




def quali_quanti_preprocessing_regression(original_data, new_data, target_column="Coût_total_5_usages"):
    import pandas as pd
    import os
    from sklearn.impute import SimpleImputer
    import pickle as pk
    
    # Séparer la variable cible pour ne pas l'imputer
    target_original = original_data[target_column]
    target_new = new_data[target_column]
    
    # Supprimer la variable cible des datasets temporairement
    original_data = original_data.drop(columns=[target_column])
    new_data = new_data.drop(columns=[target_column])
    
    # Prétraitement des variables qualitatives
    quali_data_new = new_data.select_dtypes(include=['object'])
    for column in quali_data_new.columns:
        proportions = original_data[column].value_counts(normalize=True)
        
        # Imputation des NaN pour les données originales et nouvelles
        original_data[column] = original_data[column].fillna(
            proportions.sample(weights=proportions, replace=True).index[0]
        )
        quali_data_new[column] = quali_data_new[column].fillna(
            proportions.sample(weights=proportions, replace=True).index[0]
        )
    
    # Prétraitement des variables quantitatives
    quanti_data_new = new_data.select_dtypes(exclude=['object'])
    imputer = SimpleImputer(strategy="median")
    
    # Imputation des données originales et nouvelles
    original_data[quanti_data_new.columns] = imputer.fit_transform(original_data[quanti_data_new.columns])
    quanti_data_new[quanti_data_new.columns] = imputer.transform(quanti_data_new)

    # Sauvegarder l'imputer pour une utilisation future
    pk.dump(imputer, open(os.path.join("objects", "median_imputer_regression.pkl"), "wb"))
    
    # Combinaison des données prétraitées
    new_data_processed = pd.concat([quali_data_new, quanti_data_new], axis=1)
    
    # Réintégrer la variable cible
    original_data[target_column] = target_original
    new_data_processed[target_column] = target_new
    
    return original_data, new_data_processed




def define_target(train, test, target="Etiquette_DPE"):
    X_train = train[train.columns.difference([target])]
    y_train = train[target]
    X_test = test[test.columns.difference([target])]
    y_test = test[target]
    return X_train, X_test, y_train, y_test



def to_drop_before_model(case="classification"):
    if case=="classification":
        return ["Adresse_brute","Code_INSEE_(BAN)", "Date_fin_validité_DPE", "Date_réception_DPE", 
           "Date_visite_diagnostiqueur", "Date_établissement_DPE", "Identifiant__BAN", "N°DPE", "_geopoint"]
    elif case=="regression":
        return []
    else:
        print("Error. Only 'classification' or 'regression' supported")
        return
    

def split_type_classif(X_train, X_test, to_drop):
    quali_train = X_train.select_dtypes(include="object")
    quali_train = quali_train.drop(to_drop, axis=1) # Inutile de faire une ACM sur une variable avec autant de modalités possibles
    quali_test = X_test.select_dtypes(include="object")
    quali_test = quali_test.drop(to_drop, axis=1) # Inutile de faire une ACM sur une variable avec autant de modalités possibles

    quantit_train = X_train.select_dtypes(exclude="object")
    quantit_test = X_test.select_dtypes(exclude="object")

    from sklearn.preprocessing import OneHotEncoder

    encoder = OneHotEncoder()

    encoder.fit(pd.concat([quali_train, quali_test], axis=0))
    #print(encoder.get_feature_names_out(quali_train.columns))
    quali_train_encoded = encoder.transform(quali_train).toarray()
    qualit_train = pd.DataFrame(quali_train_encoded, index=quali_train.index, columns=encoder.get_feature_names_out(quali_train.columns))
    quali_test_encoded = encoder.transform(quali_test).toarray()
    qualit_test = pd.DataFrame(quali_test_encoded, index=quali_test.index, columns=encoder.get_feature_names_out(quali_test.columns))
    # print(quali_train.apply(pd.unique).apply(len))

    import pickle as pk
    pk.dump(encoder, open(os.path.join("objects","OHE_classification.pkl"), "wb"))

    return qualit_train, qualit_test, quantit_train, quantit_test



def split_type_regression(X_train, X_test, to_drop):
    quali_train = X_train.select_dtypes(include="object")
    quali_train = quali_train.drop(to_drop, axis=1) # Inutile de faire une ACM sur une variable avec autant de modalités possibles
    quali_test = X_test.select_dtypes(include="object")
    quali_test = quali_test.drop(to_drop, axis=1) # Inutile de faire une ACM sur une variable avec autant de modalités possibles

    quantit_train = X_train.select_dtypes(exclude="object")
    quantit_test = X_test.select_dtypes(exclude="object")

    from sklearn.preprocessing import OneHotEncoder

    encoder = OneHotEncoder()

    encoder.fit(pd.concat([quali_train, quali_test], axis=0))
    #print(encoder.get_feature_names_out(quali_train.columns))
    quali_train_encoded = encoder.transform(quali_train).toarray()
    qualit_train = pd.DataFrame(quali_train_encoded, index=quali_train.index, columns=encoder.get_feature_names_out(quali_train.columns))
    quali_test_encoded = encoder.transform(quali_test).toarray()
    qualit_test = pd.DataFrame(quali_test_encoded, index=quali_test.index, columns=encoder.get_feature_names_out(quali_test.columns))
    # print(quali_train.apply(pd.unique).apply(len))

    import pickle as pk
    pk.dump(encoder, open(os.path.join("objects","OHE_regression.pkl"), "wb"))

    return qualit_train, qualit_test, quantit_train, quantit_test



def chunking_MCA(quali_train, quali_test, n_components, n_iter, seed, chunk_size):
    # Exportation en csv pour le chunking
    quali_train.to_csv(os.path.join('data','processed','quali_train.csv'), index=False, sep=";", encoding="utf-8-sig")
    quali_test.to_csv(os.path.join('data','processed','quali_test.csv'), index=False, sep=";", encoding="utf-8-sig")

    import prince

    mca = prince.MCA(
        n_components=n_components,
        n_iter=n_iter,
        copy=False,
        check_input=False,
        random_state=seed,
        engine="sklearn",
        handle_unknown="error"  # paramètre identique à celui de sklearn.preprocessing.OneHotEncoder
    )

    print("MCA : fitting to train set")
    quali_train_mca_lst = []
    i = 0
    for chunk in pd.read_csv(os.path.join('data','processed','quali_train.csv'), sep=';', chunksize=chunk_size):
        mca = mca.fit(chunk)
        quali_train_mca_lst.append(mca.transform(chunk))
        i += 1
        if i%100==0:
            print((i*chunk_size)/quali_train.shape[0])
    
    quali_train_mca = pd.DataFrame()
    for elem in quali_train_mca_lst:
        quali_train_mca = pd.concat([quali_train_mca, pd.DataFrame(elem)], axis=0, ignore_index=True)

    print("MCA : transforming test set")

    quali_test_mca_lst = []
    i = 0
    for chunk in pd.read_csv(os.path.join('data','processed','quali_test.csv'), sep=';', chunksize=chunk_size):
        quali_test_mca_lst.append(mca.transform(chunk))
        i += 1
        if i%50==0:
            print((i*chunk_size)/quali_test.shape[0])
    
    quali_test_mca = pd.DataFrame()
    for elem in quali_test_mca_lst:
        quali_test_mca = pd.concat([quali_test_mca, pd.DataFrame(elem)], axis=0, ignore_index=True)
    
    os.remove(os.path.join('data','processed','quali_train.csv'))
    os.remove(os.path.join('data','processed','quali_test.csv'))

    return quali_train_mca, quali_test_mca



def merge_type_back(quali_train_mca, quali_test_mca, quanti_train, quanti_test, train_index, test_index):
    # Convert colnames to str
    quali_train_mca.columns = quali_train_mca.columns.astype(str)
    quali_test_mca.columns = quali_test_mca.columns.astype(str)

    quali_train_mca.set_index(train_index, inplace=True)
    quali_test_mca.set_index(test_index, inplace=True)

    # Concaténer, quali_train et quanti_train de même avec test
    X_train_mca = pd.concat([quanti_train, quali_train_mca], axis=1)
    X_test_mca = pd.concat([quanti_test, quali_test_mca], axis=1)

    return X_train_mca, X_test_mca