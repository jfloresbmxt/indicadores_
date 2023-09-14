import streamlit as st
from pandas import read_excel
from clases.estados import indicadores_estado

st.header("Vocaciones productivas")

@st.cache_data
def get_estados():
    lista_estados = read_excel("data/estados.xlsx")

    return lista_estados

lista_estados = get_estados()

estado = st.selectbox(
    "Selecciona el estado",
    lista_estados
)

info_estados = indicadores_estado(estado)

df, empresas, sectores, top_sec, top_p = info_estados.get_analytics()
lista_sectores = top_sec.reset_index()

st.write("Empresas únicas", empresas)
st.write("sectores únicos", sectores)
st.dataframe(top_sec)
st.dataframe(top_p)


sector = st.selectbox(
    "Selecciona el estado",
    lista_sectores
)

n_empresas, productos = info_estados.get_analytics_sector(sector)

st.write("Empresas únicas", n_empresas)
st.dataframe(productos)