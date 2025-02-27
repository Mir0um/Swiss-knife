
import streamlit as st
import pandas as pd
import json
import csv
import sqlite3
import requests
from io import StringIO, BytesIO

def importdata():
    uploaded_file = st.file_uploader("Chargez un fichier (CSV, JSON, SQL, ou Excel)", type=["csv", "json", "sql", "xlsx", "xlsm", "xlsb", "odf"])
    file_url = st.text_input("Ou entrez une URL pour charger un fichier (CSV, JSON, SQL, ou Excel)")

    if uploaded_file or file_url:
        if uploaded_file:
            file_type = uploaded_file.name.split('.')[-1]
            file_content = uploaded_file.read()
        else:
            try:
                response = requests.get(file_url)
                response.raise_for_status()
                file_type = file_url.split('.')[-1]
                file_content = response.content
            except requests.exceptions.RequestException as e:
                st.error(f"Erreur lors du téléchargement du fichier : {e}")
                return

        try:
            if file_type == "csv":
                # Détection automatique du séparateur
                decoders = encodings = [
                                        'ascii',        # Encodage ASCII standard
                                        'utf-8',        # Encodage Unicode standard
                                        'utf-16',       # Encodage Unicode sur 2 ou 4 octets
                                        'utf-32',       # Encodage Unicode sur 4 octets
                                        'latin-1',      # Encodage ISO-8859-1 pour les langues d'Europe occidentale
                                        'cp1252',       # Encodage Windows pour les langues d'Europe occidentale
                                        'iso-8859-15',  # Variante de l'ISO-8859-1 avec le symbole de l'euro
                                        'mac-roman',    # Encodage utilisé sur les anciens systèmes Mac
                                        'big5',         # Encodage pour le chinois traditionnel
                                        'gb2312',       # Encodage pour le chinois simplifié
                                        'shift_jis',    # Encodage pour le japonais
                                        'euc-jp',       # Encodage pour le japonais
                                        'euc-kr',       # Encodage pour le coréen
                                        'koi8-r',       # Encodage pour le russe
                                        'cp866',        # Encodage DOS pour le russe
                                        'cp850',        # Encodage DOS pour l'Europe occidentale
                                        'cp437',        # Encodage DOS original
                                        'utf-7',        # Encodage Unicode obsolète
                                        'utf-8-sig',    # UTF-8 avec marque d'ordre d'octet (BOM)
                                        'utf-16-be',    # UTF-16 big-endian
                                        'utf-16-le',    # UTF-16 little-endian
                                        'utf-32-be',    # UTF-32 big-endian
                                        'utf-32-le',    # UTF-32 little-endian
                                    ]

                for decoder in decoders:
                    try:
                        content = file_content.decode(decoder, errors="ignore")
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
                df = pd.read_csv(StringIO(content), sep=sep)
                namedf = file_url.split('/')[-1].split('.')[0] if file_url else uploaded_file.name.split('.')[0]
            elif file_type == "json":
                data = json.loads(file_content)
                df = pd.json_normalize(data)
                namedf = file_url.split('/')[-1].split('.')[0] if file_url else uploaded_file.name.split('.')[0]
            elif file_type in ["xlsx", "xlsm", "xlsb", "odf"]:
                excel_file = pd.ExcelFile(BytesIO(file_content))
                sheet_name = st.selectbox("Sélectionnez une feuille :", excel_file.sheet_names)
                df = pd.read_excel(BytesIO(file_content), sheet_name=sheet_name)
                namedf = f"{file_url.split('/')[-1].split('.')[0]}_{sheet_name}" if file_url else f"{uploaded_file.name.split('.')[0]}_{sheet_name}"
            elif file_type == "sql":
                conn = sqlite3.connect(BytesIO(file_content))
                tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
                table_name = st.selectbox("Sélectionnez une table :", tables['name'])
                df = pd.read_sql(f"SELECT * FROM {table_name};", conn)
                namedf = f"{file_url.split('/')[-1].split('.')[0]}_{table_name}" if file_url else f"{uploaded_file.name.split('.')[0]}_{table_name}"
                conn.close()
            else:
                st.error("Type de fichier non pris en charge.")
                df = None
                namedf = None

            if df is not None:
                # Afficher un aperçu des données
                st.write(f"Nom du DataFrame : {namedf}")
                st.write("Aperçu des données :")
                st.write("nombre de ligne : " , df.shape[0] , " et de colone", df.shape[1])
                st.dataframe(df)
            
            return df
        except Exception as e:
            st.error(f"Erreur lors du traitement : {e}")
    else:
        st.info("Veuillez charger un fichier ou entrer une URL pour commencer.")
