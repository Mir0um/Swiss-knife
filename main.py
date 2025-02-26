import streamlit as st
import SK.head
import SK.importdata   
import SK.netoyage
import SK.exportation
import SK.analyse

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



# Créer des onglets pour l'importation et l'exportation
tabsName = ["Importation","Netoyage", "Exportation", "Analyse de données"]
tabs = st.tabs(tabsName)

tabselect = {}
for num, i in enumerate( tabs):
    tabselect[tabsName[num]] = i


with tabselect["Importation"]: 
    df = SK.importdata.importdata()


with tabselect["Netoyage"]:
    df = SK.netoyage.netoyage(df)
    

with tabselect["Exportation"]:
    SK.exportation.exportation(df,ftp_host,ftp_port,ftp_user,ftp_password,ftp_directory)

# Onglet Analyse de données avec Pandas Profiling
with tabselect["Analyse de données"]:
    SK.analyse.analyse(df)