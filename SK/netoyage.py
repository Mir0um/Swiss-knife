        
import streamlit as st
import pandas as pd
from collections import Counter
import numpy as np


def netoyage(df):
    if isinstance(df, pd.DataFrame) and not df.empty:

        st.subheader("Rognage (tranchage) des lignes")
        # Choix des indices pour conserver une tranche de lignes
        start_row = st.number_input("Indice de départ", min_value=0, max_value=len(df)-1, value=0, step=1)
        end_row = st.number_input("Indice de fin", min_value=0, max_value=len(df), value=len(df), step=1)
        df_clean = df.iloc[start_row:end_row].copy()  # On crée une copie pour éviter les modifications sur l'original
    

        st.subheader("Nettoyage des espaces (Trim)")
        if st.checkbox("Appliquer le trim sur les colonnes de type chaîne"):
            # Appliquer le trim uniquement sur les colonnes de type object (chaînes)
            for col in df_clean.select_dtypes(include=['object']).columns:
                # Utiliser .astype(str) pour convertir les valeurs en chaînes, tout en préservant les NaN
                df_clean[col] = df_clean[col].astype(str).str.strip()
                # Remplacer les 'nan' résultants de la conversion par des valeurs NaN réelles
                df_clean[col].replace('nan', np.nan, inplace=True)
            

        st.subheader("Transformer la première ligne en noms de colonnes")
        if st.checkbox("Transformer la première ligne en noms de colonnes"):
            # Extraire la première ligne pour l'utiliser comme noms de colonnes
            new_columns = df_clean.iloc[0].fillna("Colonne_Inconnue").astype(str).tolist()
            
            # Compter les occurrences de chaque nom de colonne
            
            counts = Counter(new_columns)
            
            # Renommer les colonnes en doublon en ajoutant un suffixe numérique
            for i, col in enumerate(new_columns):
                if counts[col] > 1:
                    counts[col] -= 1
                    new_columns[i] = f"{col}_{counts[col]}"
            
            # Appliquer les nouveaux noms de colonnes
            df_clean.columns = new_columns
            
            # Supprimer la première ligne et réindexer
            df_clean = df_clean[1:].reset_index(drop=True)
            

        st.subheader("Rognage des colonnes")
        # Sélection des colonnes à conserver
        colonnes = df_clean.columns.tolist()
        colonnes_a_conserver = st.multiselect("Sélectionnez les colonnes à conserver", colonnes, default=colonnes)
        df_clean = df_clean[colonnes_a_conserver].copy()

        st.subheader("Changement des types de colonnes")
        # Pour chaque colonne, possibilité de choisir le type
        # Vérifier si le DataFrame est vide
        with st.expander("Pour chaque colonne, possibilité de choisir le type"):
            for col in df_clean.columns:
                type_actuel = df_clean[col].dtype
                col_type = st.selectbox(
                    f"'{col}' (actuel: {type_actuel})",
                    options=["None", "str", "int", "float", "bool"],
                    key=f"type_{col}"
                )
                
                if col_type != "None":
                    try:
                        if col_type == "str":
                            df_clean[col] = df_clean[col].astype(str)
                        elif col_type == "int":
                            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').astype("Int64")
                        elif col_type == "float":
                            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
                        elif col_type == "bool":
                            df_clean[col] = df_clean[col].astype(bool)
                    except Exception as e:
                        st.error(f"Erreur lors de la conversion de la colonne {col} en {col_type} : {e}")



        st.subheader("Suppression des doublons")
        if st.checkbox("Supprimer les doublons"):
            df_clean = df_clean.drop_duplicates()
            #st.success("Doublons supprimés.")

        st.subheader("Suppression des lignes avec valeurs nulles")
        if st.checkbox("Supprimer les lignes nulles"):
            colonnes_a_conserver = st.multiselect("Sélectionnez les colonnes à conserver", df_clean.columns.tolist())
            if colonnes_a_conserver:
                df_clean = df_clean.dropna(subset=colonnes_a_conserver)
                #st.success("Lignes avec valeurs nulles supprimées.")
            else:
                st.warning("Veuillez sélectionner au moins une colonne.")

        st.subheader("Aperçu du DataFrame nettoyé")


        # Display the captured output as preformatted text
        st.text("ligne retiré :" + str(df.shape[0]-df_clean.shape[0]) + "  colone retiré :" + str(df.shape[1]-df_clean.shape[1]))
        st.write("nombre de ligne : " , df_clean.shape[0] , " et de colone", df_clean.shape[1])

        st.write(df_clean)
        
        df = df_clean
        return df
    else:
        st.info("Veuillez importer des données dans l'onglet 'Importation' pour commencer l'exportation.")