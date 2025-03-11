import streamlit as st
def head():
    # Titre principal
    col1, col2 = st.columns([1,12])

    with col1:
        st.image("http://sartoris.dscloud.mobi/img/logo.png", width=120)
    with col2:
        st.header("Swiss-knife")