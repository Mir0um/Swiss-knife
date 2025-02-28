import streamlit as st
import pandasql as ps

def transformation(df):
    if 'df' in locals() and df is not None:

        with st.expander("Assistant de Création de Requête SQL"):
            st.title("Assistant SQL sans Connaissances en SQL")
            st.write("Construisez votre requête en cliquant sur les options ci-dessous.")

            # Récupération de la table principale et de son DataFrame
            main_table = st.session_state.dfname  
            df_main = st.session_state.dfs[main_table]

            # Onglets pour structurer la démarche
            tab_jointure, tab_colonnes, tab_filtres, tab_aggregations, tab_group_order = st.tabs([
                "Jointure",
                "Colonnes",
                "Filtres",
                "Agrégations",
                "Group By & Order By"
            ])

            # ----- Onglet Jointure -----
            with tab_jointure:
                st.header("Configuration de la Jointure")
                available_tables = list(st.session_state.dfs.keys())
                if main_table in available_tables:
                    available_tables.remove(main_table)
                join_table = st.selectbox("Choisissez une table de jointure", ["Aucune"] + available_tables, key="join_table")
                join_clause = ""
                if join_table != "Aucune":
                    join_type = st.selectbox("Type de jointure", ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL JOIN"], key="join_type")
                    # Récupérer les colonnes de la table de jointure
                    df_join = st.session_state.dfs[join_table]
                    join_col_main = st.selectbox("Colonne de la table principale pour la jointure", df_main.columns.tolist(), key="join_col_main")
                    join_col_join = st.selectbox("Colonne de la table de jointure", df_join.columns.tolist(), key="join_col_join")
                    join_clause = f"{join_type} {join_table} ON {main_table}.[{join_col_main}] = {join_table}.[{join_col_join}]"
                    st.info("Clause de jointure : " + join_clause)
                else:
                    st.info("Aucune jointure sélectionnée.")
                    

            # ----- Onglet Filtres -----
            with tab_filtres:
                st.header("Ajouter des Filtres")
                num_filters = st.multiselect("Nombre de filtres à appliquer",df_main.columns.tolist(), key="num_filters")
                filters = []
                operators = ["=", "!=", ">", "<", ">=", "<=", "LIKE"]
                for i in num_filters:
                    st.subheader(f"Filtre {i}")
                    op_filter = st.selectbox(f"Opérateur pour le filtre {i}", operators, key=f"filter_op_{i}")
                    val_filter = st.text_input(f"Valeur pour le filtre {i}", key=f"filter_val_{i}")
                    if val_filter != "":
                        # On entoure toujours la valeur de quotes pour éviter toute erreur
                        condition = f"\"{i}\" {op_filter} '{val_filter}'"
                        filters.append(condition)
                    if filters:
                        st.info("Conditions de filtre : " + " AND ".join(filters))
                    else:
                        st.info("Aucun filtre ajouté.")

            # ----- Onglet Agrégations -----
            with tab_aggregations:
                st.header("Ajouter des Agrégations")
                num_aggs = st.multiselect("Nombre d'agrégations à appliquer",df_main.columns.tolist(), key="num_aggs")
                aggregates = []
                agg_functions = ["Aucune","COUNT", "SUM", "AVG", "MIN", "MAX"]
                
                for i in num_aggs: #range(int(num_aggs)):
                    st.subheader(f"Agrégation {i}")
                    agg_func = st.selectbox(f"Fonction d'agrégation {i}", agg_functions, key=f"agg_func_{i}")
                    agg_alias = st.text_input(f"Alias (optionnel) pour l'agrégation {i}", key=f"agg_alias_{i}")
                    
                    if agg_func == "Aucune":
                        agg_func = ""
                        if agg_alias:
                            aggregates.append(f"\"{i}\" AS {agg_alias}")
                            
                    else:
                        if agg_alias:
                            aggregates.append(f"{agg_func}(\"{i}\") AS {agg_alias}")
                        else:
                            if not agg_func == "":
                                aggregates.append(f"{agg_func}(\"{i}\")")

                    if agg_alias != "" or agg_func != "":
                        st.info(f"Agrégations : {aggregates[-1]}")
                    else:
                        st.info("Aucune agrégation ajoutée.")

            # ----- Onglet Colonnes -----
            with tab_colonnes:
                st.header("Sélection des Colonnes")
                selected_columns = st.multiselect(
                    "Choisissez les colonnes à afficher",
                    df_main.columns.tolist(),
                    key="select_columns"
                )
                
                # Construction de la clause SELECT                
                if selected_columns:
                    select_clause = "\",\n\t\"".join(selected_columns)
                    select_clause = '"' + select_clause + '"'
                else:
                    select_clause = "*"
                if aggregates:
                    # Si l'utilisateur a sélectionné des colonnes ET des agrégations, on affiche les deux
                    if select_clause != "*":
                        select_clause +=  ",\n\t " + ", ".join(aggregates)
                    else:
                        select_clause = ", ".join(aggregates)
                
                select_clause = "SELECT " + select_clause

                st.info("Colonnes sélectionnées : " + select_clause)
                
            # ----- Onglet Group By & Order By -----
            with tab_group_order:
                st.header("Group By & Order By")
                group_by_cols = st.multiselect("Sélectionnez les colonnes pour GROUP BY", df_main.columns.tolist(), key="group_by")
                order_by_col = st.selectbox("Sélectionnez la colonne pour ORDER BY", ["Aucune"] + df_main.columns.tolist(), key="order_by")
                order_direction = "ASC"
                if order_by_col != "Aucune":
                    order_direction = st.selectbox("Direction", ["ASC", "DESC"], key="order_dir")
                if group_by_cols:
                    st.info("GROUP BY : " + ", ".join(group_by_cols))
                else:
                    st.info("Aucun GROUP BY ajouté.")
                if order_by_col != "Aucune":
                    st.info(f"ORDER BY : {order_by_col} {order_direction}")
                else:
                    st.info("Aucun ORDER BY ajouté.")

            # ----- Onglet Exécuter -----
            
            st.write("---")
            st.header("Exécuter la Requête")
            
            # Assemblage de la requête
            query = f"{select_clause}\nFROM {main_table}"
            if join_clause:
                query += f"\n{join_clause}"
            if filters:
                query += "\nWHERE " + " AND ".join(filters)
            if group_by_cols:
                query += "\nGROUP BY \"" + "\",\n\t\" ".join(group_by_cols) + "\""
            if order_by_col != "Aucune":
                query += f"\nORDER BY \"{order_by_col}\" {order_direction}"

            st.subheader("Requête SQL Générée")
            tabsqlgauche, tabsqldroit  = st.columns([1,1])
            
            query = tabsqlgauche.text_area("Requête SQL", value=query, height=150, key="sql_generated")
            tabsqldroit.text("aide vusuele.")
            tabsqldroit.code(query, language="sql")

            if st.button("Exécuter la requête"):
                try:
                    dfs = st.session_state.dfs  # Tous les DataFrames disponibles en session
                    result = ps.sqldf(query, dfs)
                    st.success("Requête exécutée avec succès !")
                    st.dataframe(result)
                except Exception as e:
                    st.error(f"Erreur lors de l'exécution de la requête SQL : {str(e)}")

        with st.expander("Expression régulière (regex)"):
            st.text("en cour de dev")
    else:
        st.info("Veuillez importer des données dans l'onglet 'Importation' pour générer un rapport de profilage.")
