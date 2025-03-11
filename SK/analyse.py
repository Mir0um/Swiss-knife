import streamlit as st
from streamlit_pandas_profiling import st_profile_report
from ydata_profiling import ProfileReport

def analyse(df, dfname):
    if 'df' in locals() and df is not None:
        if st.button("Générer le rapport de profilage", key=f"analyse_{dfname}"):
            profile = ProfileReport(df, title=dfname)
            st_profile_report(profile, navbar=False)

            # Ajouter un bouton pour télécharger le rapport de profilage au format HTML
            html_report = profile.to_html()
            st.download_button(label="Télécharger le rapport de profilage en HTML", data=html_report, file_name=f"{dfname}_profiling_report.html", mime="text/html")
    else:
        st.info("Veuillez importer des données dans l'onglet 'Importation' pour générer un rapport de profilage.")
