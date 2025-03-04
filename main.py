import streamlit as st
import SK.head
import SK.importdata   
import SK.nettoyage
import SK.exportation
import SK.analyse
import SK.transformation

# Configuration de la page
st.set_page_config(page_title="Data_convertisseur",
                    page_icon="http://89.86.5.13/img/logo.png",
                    layout="wide",
                    initial_sidebar_state="collapsed",
                    #menu_items={
                    #        'Get Help': 'https://www.extremelycoolapp.com/help',
                    #        'Report a bug': "https://www.extremelycoolapp.com/bug",
                    #        'About': "# This is a header. This is an *extremely* cool app!"
                    #    }
                   )


SK.head.head()

with st.sidebar:
    st.write("Config ver un seveur SFTPS ou SQL")
    with st.expander("conetion en SFTPS."):
        ftp_host = st.text_input("FTP Host")
        ftp_port = st.number_input("FTP Port", min_value=1, max_value=65535, value=21)
        ftp_user = st.text_input("FTP Username")
        ftp_password = st.text_input("FTP Password", type="password")
        ftp_directory = st.text_input("FTP Directory", value="/")
    
    with st.expander("conetion a un serveur SQL."):
        SQL_host = st.text_input("SQL Host")
        SQL_port = st.number_input("SQL Port", min_value=1, max_value=65535, value=3306 )
        SQL_user = st.text_input("SQL Username")
        SQL_password = st.text_input("SQL Password", type="password")
        SQL_bdd = st.text_input("SQL Database name.", value="/")

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
    return df

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
            df = select_DF(key=f"apelle_{onglet}")  # Clé unique par onglet pour éviter les conflits
            if df is not None:  # Vérifier si un DF est sélectionné avant de l'utiliser
                if onglet == "Nettoyage":
                    SK.nettoyage.nettoyage(df)
                elif onglet == "Transformation":
                    SK.transformation.transformation(df)
                elif onglet == "Exportation":
                    SK.exportation.exportation(df, ftp_host, ftp_port, ftp_user, ftp_password, ftp_directory)
                elif onglet == "Analyse de données":
                    SK.analyse.analyse(df)
else:
    # Si aucun DataFrame n'est présent, afficher l'interface d'importation
    SK.importdata.add_df()
