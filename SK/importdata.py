import streamlit as st
import pandas as pd
import json
import csv
import sqlite3
import SK.savedf

def add_df():
    st.header("Ajouter un nouveau jeux de donner")
    uploaded_file = st.file_uploader("Chargez un fichier (CSV, JSON, SQL, ou Excel)", type=["csv", "json", "sql", "xlsx", "xlsm", "xlsb", "odf"])
    if uploaded_file:
        file_type = uploaded_file.name.split('.')[-1]
        try:            
            dfName = getattr(uploaded_file, 'name', 'DF').split('.')[0]

            if file_type == "csv":
                # Détection automatique du séparateur
                decoders = [
                    'ascii', 'utf-8', 'utf-16', 'utf-32', 'latin-1', 'cp1252',
                    'iso-8859-15', 'mac-roman', 'big5', 'gb2312', 'shift_jis',
                    'euc-jp', 'euc-kr', 'koi8-r', 'cp866', 'cp850', 'cp437',
                    'utf-7', 'utf-8-sig', 'utf-16-be', 'utf-16-le', 'utf-32-be', 'utf-32-le'
                ]
                for decoder in decoders:
                    try:
                        content = uploaded_file.read().decode(decoder, errors="ignore")
                        break
                    except UnicodeDecodeError:
                        continue
                try:
                    sniffer = csv.Sniffer()
                    dialect = sniffer.sniff(content[:1024])
                    sep = dialect.delimiter
                    st.success(f"Séparateur détecté automatiquement : '{sep}'")
                except Exception:
                    sep = st.text_input("Séparateur non détecté, entrez-le manuellement (par ex. ',' ou ';') :", value=",")
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, sep=sep)
                # Pour un CSV, le dfName est défini à partir du nom du fichier
                dfName = getattr(uploaded_file, 'name', 'CSV').split('.')[0]

            elif file_type == "json":
                data = json.load(uploaded_file)
                df = pd.json_normalize(data)
                # Pour un JSON, le dfName est également défini à partir du nom du fichier
                dfName = getattr(uploaded_file, 'name', 'JSON').split('.')[0]

            elif file_type in ["xlsx", "xlsm", "xlsb", "odf"]:
                excel_file = pd.ExcelFile(uploaded_file)
                sheet_name = st.selectbox("Sélectionnez une feuille :", excel_file.sheet_names)
                df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
                # Ici, le dfName correspond à la feuille sélectionnée
                dfName = sheet_name

            elif file_type == "sql":
                conn = sqlite3.connect(uploaded_file)
                tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
                table_name = st.selectbox("Sélectionnez une table :", tables['name'])
                df = pd.read_sql(f"SELECT * FROM {table_name};", conn)
                conn.close()
                # Pour SQL, le dfName correspond à la table sélectionnée
                dfName = table_name

            else:
                st.error("Type de fichier non pris en charge.")
                df = None

            if df is not None:
                # Afficher un aperçu des données
                st.write("Nombre de lignes :", df.shape[0], " et de colonnes :", df.shape[1])
                st.write("Aperçu des données :")
                st.dataframe(df, height=200, hide_index=True)
                # Stocker le DataFrame dans la session pour le garder lors d'un rafraîchissement
            
            SK.savedf.savedf(df, dfName, rerun=True)
        
        except Exception as e:
            st.error(f"Erreur lors du traitement : {e}")
    else:
        st.info("Veuillez charger un fichier pour commencer.")

def importdata():

    # On vérifie si le DataFrame a déjà été chargé
    if 'dfs' in st.session_state and not st.session_state['dfs'] == {} :
        col1, col2 = st.columns([1,1])
        dfs = st.session_state.dfs

        with col1:
            for _, keyname in enumerate(st.session_state.dfs):
                df = st.session_state.dfs
                col11, col12 = st.columns([1,1])
                with col11:
                        st.write("Nombre de lignes :", df[keyname].shape[0], " et de colonnes :", df[keyname].shape[1])
                
                
                with col12:
                    if st.button(f"Supirimer '{keyname}'"):
                        dfs.pop(keyname)
                        st.text(type(dfs))
                        st.rerun()
                
                st.dataframe(df[keyname])
        
        with col2:
            add_df()