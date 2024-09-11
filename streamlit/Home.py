"""
This script sets up a Streamlit app for encoding and
decoding images using steganography.
"""
import streamlit as st

st.set_page_config(layout="wide")

st.page_link("Home.py", label="Página inicial", icon="🏠")

st.page_link("pages/Aditivos.py", label="Aditivos")

st.page_link("pages/Contratos.py", label="Contratos")

st.page_link("pages/Folha.py", label="Folha")

st.page_link("pages/Licitacoes.py", label="Licitacoes")

st.page_link("pages/Receita.py", label="Receita")