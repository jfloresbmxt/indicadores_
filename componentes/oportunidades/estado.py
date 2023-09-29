import streamlit as st
from clases.oportunidades9.seccion1 import pipeline_state_s, pipeline_state_partida


def state(ms):
    st.divider()

    usa_states = ms["State"].unique()
    usa = st.selectbox(
        "**Selecciona el estado**",
        usa_states
    )

    imports_usa = (ms[ms["State"] == usa])

    imports_usa_s = pipeline_state_s(imports_usa)
    imports_usa_p = pipeline_state_partida(imports_usa)
    
    st.header("Importaciones por sector")
    st.dataframe(imports_usa_s)

    st.header("Importaciones por partida")
    st.dataframe(imports_usa_p)