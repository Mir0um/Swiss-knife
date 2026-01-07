# =================================================================================
# ███████╗██╗    ██╗██╗███████╗███████╗      ██╗  ██╗███╗   ██╗██╗███████╗███████╗
# ██╔════╝██║    ██║██║██╔════╝██╔════╝      ██║ ██╔╝████╗  ██║██║██╔════╝██╔════╝
# ███████╗██║ █╗ ██║██║███████╗███████╗█████╗█████╔╝ ██╔██╗ ██║██║█████╗  █████╗  
# ╚════██║██║███╗██║██║╚════██║╚════██║╚════╝██╔═██╗ ██║╚██╗██║██║██╔══╝  ██╔══╝  
# ███████║╚███╔███╔╝██║███████║███████║      ██║  ██╗██║ ╚████║██║██║     ███████╗
# ╚══════╝ ╚══╝╚══╝ ╚═╝╚══════╝╚══════╝      ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝
#                           main.py fichier principal
# =================================================================================
                                                                                
import os
import SK.head
from db import db 
import SK.analyse
import SK.nettoyage
import SK.importdata  
import SK.exportation
import streamlit as st
import SK.transformation

# pour la gestion des mal automatique
import logging
logging.getLogger("streamlit").setLevel(logging.WARNING) 

# =================================================
# maitre a jour streamlit a la version 1.52.2
# puis otomiser avec les nouvele fonctionnalité d'optimisation
# avec les fonction st.cache_data, st.cache_resource, pages, st.sqlite
# et ameliore le style avec du css
# et ajotue une base de donée pour la gestion des utilisateur
# =================================================


# Configuration de la page
st.set_page_config(page_title="Data_convertisseur",
                    page_icon="http://sartoris.dscloud.mobi/img/logo.png",
                    layout="wide",
                    initial_sidebar_state="collapsed",
                    menu_items={
                        'Get Help': 'https://github.com/Mir0um/Swiss-knife/help',
                        'Report a bug': "https://github.com/Mir0um/Swiss-knife/issues",
                        'About': """Nom du projet : **Swiss-knife** 
                            \r\rVersion : **1.3.0** 
                            \r\rCollaborateurs : **GregTic**, **Laien WU**, **n-popy**, **Mir0um** 
                            \r\r Ce projet est pour une formation, notre du formateur : **Gaetan C**."""
                    }
                   )

# CSS personnalisé pour améliorer l'apparence
SK.head.head()

if st.session_state.get("session") is None and True:
    st.session_state["session"] = None
    st.title("Bienvenue sur Swiss-Knife, veuillez vous connecter")
    st.markdown("<h3>Une solution tout-en-un pour vos données</h3>", unsafe_allow_html=True)
    st.write("Swiss-Knife est une application Web réalisée en Python (compatible avec Python 3.9.12) qui offre une solution tout-en-un pour l'importation, la conversion, l'exportation et l'analyse de fichiers de données.")
    st.markdown("<p style='color: #008000;'>Grâce à une interface utilisateur construite avec Streamlit, l’application permet de charger différents formats de fichiers (CSV, JSON, SQL, Excel), de les convertir en divers formats et de générer des rapports de profilage de données détaillés.</p>", unsafe_allow_html=True)
    
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Авторизоваться"):
        user = db.verify_user(username, password)
        if user:
            st.session_state["session"] = {"username": user[0], "role": user[1]}
            st.success(f"Connecté en tant que {user[0]} avec le rôle {user[1]}")
            st.rerun()
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")
    
    st.text("...", help="admin/password, toto/ddsf16SDFSD5, Чиполлино/пароль")
else:

    def select_DF(key):
        """Permet à l'utilisateur de sélectionner un DataFrame stocké en session."""
        dfs = st.session_state.get("dfs", {})
        if not dfs:
            st.warning("Aucun DataFrame disponible. Veuillez importer des données.")
            return None
        
        dfname = st.selectbox("Sélectionnez votre dataset :", list(dfs.keys()), 0, key=key)
        st.session_state.dfname = dfname
        df = dfs[dfname]
        st.write("---")
        return df, dfname

    if 'dfs' in st.session_state and st.session_state['dfs']:
        # Création des onglets
        onglets = ["Importation", "Nettoyage", "Transformation", "Exportation", "Analyse de données"]
        tabs = st.tabs(onglets)
        
        # Association des onglets à leurs noms
        onglets_dict = {nom: tab for nom, tab in zip(onglets, tabs)}

        # Onglet Importation (pas de sélection de DataFrame ici)
        with onglets_dict["Importation"]:
            SK.importdata.importdata()

        # Appliquer la sélection du DataFrame dans les autres onglets
        for onglet in ["Nettoyage", "Transformation", "Exportation", "Analyse de données"]:
            with onglets_dict[onglet]:
                df, dfname = select_DF(key=f"apelle_{onglet}")  # Clé unique par onglet pour éviter les conflits
                if df is not None:  # Vérifier si un DF est sélectionné avant de l'utiliser
                    if onglet == "Nettoyage":
                        SK.nettoyage.nettoyage(df, dfname)
                    elif onglet == "Transformation":
                        SK.transformation.transformation(df, dfname)
                    elif onglet == "Exportation":
                        st.text("fonconnalité en cour de devlopement")
                        # SK.exportation.exportation(df, ftp_host, ftp_port, ftp_user, ftp_password, ftp_directory, dfname)
                    elif onglet == "Analyse de données":
                        SK.analyse.analyse(df, dfname)
    else:
        # Si aucun DataFrame n'est présent, afficher l'interface d'importation
        st.title(f"Bienvenue `{st.session_state['session']['username']}` sur Swiss-Knife, vous etes `{st.session_state['session']['role']}`")
        st.markdown("<h3 style='color: #000080;'>Une solution tout-en-un pour vos données</h3>", unsafe_allow_html=True)
        st.write("Swiss-Knife est une application Web réalisée en Python (compatible avec Python 3.9.12) qui offre une solution tout-en-un pour l'importation, la conversion, l'exportation et l'analyse de fichiers de données.")
        st.markdown("<p style='color: #008000;'>Grâce à une interface utilisateur construite avec Streamlit, l’application permet de charger différents formats de fichiers (CSV, JSON, SQL, Excel), de les convertir en divers formats et de générer des rapports de profilage de données détaillés.</p>", unsafe_allow_html=True)
        SK.importdata.add_df()
