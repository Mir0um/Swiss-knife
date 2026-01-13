import streamlit as st
def head():
    st.html(f"<style>{open('style/style.css', 'r').read()}</style>")

    if st.session_state.get("session") is not None:
        with st.sidebar:
            if st.button("se deconnecter"): 
                st.session_state["session"] = None
                st.rerun()
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

    # Titre principal
    col1, col2 = st.columns([1,12])

    with col1:
        st.image("http://sartoris.dscloud.mobi/img/logo.png", width=120)
    with col2:
        st.header("Swiss-knife")