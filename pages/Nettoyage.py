
import SK.nettoyage
import SK.head
import streamlit as st

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

df, dfname = select_DF(key=f"apelle_Nettoyage")  # Clé unique par onglet pour éviter les conflits

SK.nettoyage.nettoyage(df, dfname)