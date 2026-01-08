```   
███████╗██╗    ██╗██╗███████╗███████╗      ██╗  ██╗███╗   ██╗██╗███████╗███████╗ 
██╔════╝██║    ██║██║██╔════╝██╔════╝      ██║ ██╔╝████╗  ██║██║██╔════╝██╔════╝
███████╗██║ █╗ ██║██║███████╗███████╗█████╗█████╔╝ ██╔██╗ ██║██║█████╗  █████╗  
╚════██║██║███╗██║██║╚════██║╚════██║╚════╝██╔═██╗ ██║╚██╗██║██║██╔══╝  ██╔══╝  
███████║╚███╔███╔╝██║███████║███████║      ██║  ██╗██║ ╚████║██║██║     ███████╗
╚══════╝ ╚══╝╚══╝ ╚═╝╚══════╝╚══════╝      ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝
```

# Swiss-Knife

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

Swiss-Knife est une application Web réalisée en Python (compatible avec Python 3.9.12) qui offre une solution tout-en-un pour l'importation, la conversion, l'exportation et l'analyse de fichiers de données. Grâce à une interface utilisateur construite avec Streamlit, l’application permet de charger différents formats de fichiers (CSV, JSON, SQL, Excel), de les convertir en divers formats et de générer des rapports de profilage de données détaillés.

## Table des matières

- [Fonctionnalités](#fonctionnalités)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
  - [Importation de données](#importation-de-données)
  - [Exportation et conversion](#exportation-et-conversion)
  - [Analyse de données](#analyse-de-données)
  - [Exportation via FTPS](#exportation-via-ftps)
  - [Configuration SQL](#configuration-sql)
- [Architecture du projet](#architecture-du-projet)
- [Dépendances](#dépendances)
- [Contribuer](#contribuer)
- [Licence](#licence)

## Fonctionnalités

- **Interface intuitive avec Streamlit** : Interface web moderne et interactive pour une prise en main rapide.
- **Importation multi-format** : Prise en charge des fichiers CSV, JSON, SQL et Excel, avec détection automatique des séparateurs pour les CSV.
- **Conversion et exportation** : Conversion de données en formats CSV, JSON, Excel, SQL (génération de scripts d'insertion) et bases de données SQLite.
- **Analyse de données** : Intégration de [Pandas Profiling](https://pandas-profiling.ydata.ai/) pour générer des rapports d’analyse détaillés.
- **Exportation via FTPS** : Possibilité d’envoyer vos fichiers convertis vers un serveur FTP sécurisé.
- **Configuration SQL** : Options de configuration pour se connecter à un serveur SQL externe et réaliser des exports directs.
- **Personnalisation et extensibilité** : Code structuré et modulaire, permettant d’ajouter de nouvelles fonctionnalités selon les besoins.

## Prérequis

- Python 3.9.12 ou supérieur
- Un environnement virtuel recommandé pour gérer les dépendances

## Installation

1. **Cloner le dépôt :**

   ```bash
   git clone https://github.com/Mir0um/Swiss-knife.git
   cd swiss-knife
   ```

2. **Créer et activer un environnement virtuel :**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Sous Windows: venv\Scripts\activate
   ```

3. **Installer les dépendances :**

   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

### Lancer l'application

Pour démarrer l'application, utilisez le script `run.py` qui lance Streamlit sur un port personnalisé :

```bash
python run.py
```

Par défaut, l'application sera accessible via `http://localhost:8509`.

### Importation de données

- **Formats supportés** : CSV, JSON, SQL, et Excel (XLSX, XLSM, etc.).
- Lors du téléchargement d'un fichier CSV, le programme tente de détecter automatiquement le séparateur (ex. `,` ou `;`). Si la détection échoue, vous pouvez le spécifier manuellement.
- Pour les fichiers Excel, vous pouvez choisir la feuille à importer.

### Exportation et conversion

Une fois les données importées, vous pouvez choisir le format de conversion :

- **CSV** : Conversion avec choix du séparateur.
- **JSON** : Export en format JSON avec une mise en forme indentée.
- **Excel** : Génération d'un fichier Excel.
- **SQL** : Génération d'un script SQL pour insérer les données dans une table.
- **DB (SQLite)** : Création d’une base de données SQLite contenant vos données.

Un bouton de téléchargement vous permet de récupérer directement le fichier converti.

### Analyse de données

- Utilisez l’onglet dédié pour générer un rapport de profilage à l’aide de [Pandas Profiling](https://pandas-profiling.ydata.ai/).
- Le rapport peut être visualisé directement dans l’application et téléchargé au format HTML pour une analyse approfondie.

### Exportation via FTPS

- Configurez vos identifiants FTP dans l’onglet "Configuration".
- L’application propose une option pour exporter directement les fichiers convertis vers un serveur FTP sécurisé via FTPS.
- Assurez-vous de renseigner l’hôte FTP, le port, le nom d’utilisateur, le mot de passe et le répertoire de destination.

### Configuration SQL

- Dans l’onglet "Configuration", vous pouvez également configurer une connexion à un serveur SQL.
- Cela permet d’exporter les données dans une base de données externe en plus des autres formats.

## Architecture du projet

- **main.py** : Point d'entrée principal de l'application Streamlit.
- **run.py** : Script pour lancer l'application avec Streamlit sur un port défini.
- **requirements.txt** : Liste des dépendances nécessaires pour faire fonctionner le projet.
- **README.md** : Documentation du projet.
- **Dockerfile** : Configuration pour conteneuriser l'application avec Docker.
- **LICENSE** : Fichier de licence du projet.
- **data/** : Dossier contenant les fichiers de données exemple (e.g., data.csv).
- **db/** : Module pour la gestion des bases de données (db.py).
- **pages/** : Pages supplémentaires de l'application Streamlit (e.g., Nettoyage.py).
- **SK/** : Module principal contenant la logique métier :
  - **analyse.py** : Fonctions d'analyse de données.
  - **exportation.py** : Logique d'exportation des données.
  - **head.py** : Fonctions pour afficher l'en-tête ou aperçu des données.
  - **importdata.py** : Logique d'importation des données.
  - **nettoyage.py** : Fonctions de nettoyage des données.
  - **savedf.py** : Sauvegarde des DataFrames.
  - **transformation.py** : Transformations des données.
- **style/** : Fichiers de style CSS (style.css) pour personnaliser l'interface.

## Dépendances

Le projet s'appuie sur plusieurs bibliothèques clés, notamment :

- [Streamlit](https://streamlit.io/) : Pour la création de l'interface web interactive.
- [Pandas](https://pandas.pydata.org/) : Pour la manipulation et l'analyse des données.
- [ydata-profiling](https://pandas-profiling.ydata.ai/) : Pour générer des rapports de profilage.
- [ftplib](https://docs.python.org/3/library/ftplib.html) : Pour la gestion de la connexion FTPS.
- [SQLite3](https://docs.python.org/3/library/sqlite3.html) : Pour la manipulation des bases de données SQLite.

Pour consulter la liste complète des packages, référez-vous au fichier [requirements.txt](requirements.txt).

## Contribuer

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le dépôt.
2. Créez une branche pour votre fonctionnalité ou correction (`git checkout -b feature/nouvelle-fonctionnalité`).
3. Commitez vos modifications (`git commit -m 'Ajout d'une nouvelle fonctionnalité'`).
4. Poussez votre branche (`git push origin feature/nouvelle-fonctionnalité`).
5. Ouvrez une Pull Request.

Merci de suivre le guide de contribution et de respecter le code de conduite du projet.

## Licence

Ce projet est sous licence [MIT](LICENSE).
