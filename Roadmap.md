# Roadmap

### Extraction des données
- Choix de l'échelle du lieu dont on veut récupérer les données
- Requête API

### Exploratory Data Analysis (EDA)

### Prétraitement des données
- Gestion des valeurs manquantes
- Gestion des valeurs aberrantes
- Gestion des variables qualitatives
- Définition du problème de ML : classification binaire ou multi-classe ?
- ...

### Modélisation
- Préparation des données
	- Split des variables explicatives et de la variable cible
- Choix des modèles
- Entraînement
	- Tuning des hyperparamètres via cross-validation et GridSearchCV
	- Split des données en échantillon train et test
	- Ré-entraînement du modèle avec les meilleurs hyperparamètres sur les données train
- Evaluation
	- Choix des métriques
	- Scoring
	- Comparaison des modèles

### Mise en production (MLOps)
- Exportation des modèles (format .pkl, .pmml ou autres)
- Codage du fichier source de l'application Web
	- Choix de la technologie (Dash, Streamlit, Shiny)
	- Définition de l'architecture de l'application
	- A chaque page, coder les fonctionnalités (graphiques, importation du modèle + prédiction, etc.)