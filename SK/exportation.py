import streamlit as st
import ftplib
import sqlite3
from io import StringIO, BytesIO

def _generate_sql(df, table_name="exported_table"):
                    sql_statements = []
                    for _, row in df.iterrows():
                        values = ', '.join(f"'{str(v)}'" for v in row)
                        sql_statements.append(f"INSERT INTO {table_name} VALUES ({values});")
                    return '\n'.join(sql_statements)

def exportation(df,ftp_host,ftp_port,ftp_user,ftp_password,ftp_directory):
    if 'df' in locals() and df is not None:
        # Sélection du format de conversion
        export_format = st.selectbox("Choisissez un format de conversion :", ["CSV", "JSON", "SQL", "DB", "Excel"])

        if export_format:
            if export_format == "CSV":
                # Choix du séparateur pour l'exportation
                export_sep = st.text_input("Choisissez un séparateur pour l'exportation (par ex. ',' ou ';') :",
                                            value=",")
                buffer = StringIO()
                df.to_csv(buffer, index=False, sep=export_sep)
                file_data = buffer.getvalue().encode('utf-8')
                filename = "converted_file.csv"
            elif export_format == "JSON":
                buffer = StringIO()
                df.to_json(buffer, orient="records", indent=2)
                file_data = buffer.getvalue().encode('utf-8')
                filename = "converted_file.json"
            elif export_format == "Excel":
                buffer = BytesIO()
                df.to_excel(buffer, index=False, engine='openpyxl')
                file_data = buffer.getvalue()
                filename = "converted_file.xlsx"
            elif export_format == "DB":
                conn = sqlite3.connect("converted_file.db")
                table_name = st.text_input("Nom de la table pour l'export :", "exported_table")
                df.to_sql(table_name, conn, if_exists="replace", index=False)
                conn.close()
                with open("converted_file.db", "rb") as f:
                    file_data = f.read()
                filename = "converted_file.db"

            elif export_format == "SQL":
                buffer = StringIO()
                table_name = st.text_input("Nom de la table pour l'export :", "exported_table")
                buffer.write(_generate_sql(df, table_name))
                file_data = buffer.getvalue().encode('utf-8')
                filename = "converted_file.sql"

            

            # Section de téléchargements basiques
            st.header("Téléchargement basique")
            mime_type = 'text/csv' if export_format == "CSV" else 'application/json' if export_format == "JSON" else 'application/x-sqlite3' if export_format == "SQL" else 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            st.download_button(label=f"Télécharger le fichier {filename}", data=file_data, file_name=filename, mime=mime_type)

            # Section d'exportation en FTPS
            st.header("Exportation via FTPS")
            if ftp_host and ftp_user and ftp_password:
                if st.button("Exporter via FTPS"):
                    print("[LOG] Connexion au serveur FTP...")
                    try:
                        with ftplib.FTP_TLS() as ftp:
                            ftp.connect(host=ftp_host, port=ftp_port)
                            ftp.login(user=ftp_user, passwd=ftp_password)
                            ftp.prot_p()  # Activer le mode de protection
                            ftp.cwd(ftp_directory)
                            ftp.storbinary(f'STOR {filename}', BytesIO(file_data))
                            st.success(f"Fichier sauvegardé sur le serveur FTP : {ftp_directory}/{filename}")
                            print(f"[LOG] Fichier uploadé avec succès sur le serveur FTP : {ftp_directory}/{filename}")
                    except Exception as e:
                        st.error(f"Erreur lors de l'upload FTP : {e}")
                        print(f"[LOG] Erreur lors de l'upload FTP : {e}")
            else:
                st.warning("Veuillez configurer les identifiants FTP dans l'onglet 'Configuration FTPS' pour utiliser l'exportation FTPS.")
    else:
        st.info("Veuillez importer des données dans l'onglet 'Importation' pour commencer l'exportation.")