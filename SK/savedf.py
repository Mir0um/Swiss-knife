import streamlit as st
from unidecode import unidecode
import re

def _nettoyer_chaine(chaine):
    # Remplacer les espaces par des underscores
    chaine = chaine.replace(' ', '_')
    # Supprimer les accents
    chaine = unidecode(chaine)
    # Supprimer les caractères non alphanumériques et les underscores
    chaine = re.sub(r'[^a-zA-Z0-9_]', '', chaine)
    return chaine


def savedf(df, dfName: str, rerun: bool = False):
    col21, col22 = st.columns([1,2])

    dfName = col22.text_input("Nom du DataFrame: (Si le nom est identique a un autre DataFrame, il sera remplacé)" , _nettoyer_chaine(dfName))
    with col21:
        if dfName == _nettoyer_chaine(dfName):
            st.text("enregistrement du DataFrame")
            if st.button("valider les donner pour paser a la suit",key=f"enregistrement_{dfName}"):
                if 'dfs' in st.session_state:    
                    dfs = st.session_state.dfs
                    dfs[dfName] = df
                    st.session_state.dfs = dfs                
                else:                    
                    st.session_state.dfs = {dfName : df}
                st.success("DataFrame enregistré avec succès")
                
                if rerun:
                    st.rerun()
        else:
            st.info("Veuillez n'utiliser que des lettres, des chiffres, des traits d'union (-) et des underscores (_) dans les noms de fichiers ou de dossiers. Les caractères spéciaux tels que < > : \" / \ | ? * ainsi que les accents (é, è, à, etc.) ne sont pas autorisés.")
