import streamlit as st
from clases.oportunidades9.seccion1 import *

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('latin1')

def region(estado, m, rfc_sectors):
    st.divider()

    st.subheader("Importaciones por region de Estados Unidos")
    st.dataframe(data_w(m))
    data2 = convert_df(rfc_sectors)

    st.download_button(
        label="Descargar datos",
        data=data2,
        file_name=f'importacion_regiones_usa_{estado}.csv',
        mime='text/csv',
    )
    st.divider()
    st.subheader("Detalle importaciones por region de Estados Unidos")

    st.dataframe(m, use_container_width=True)
    data3 = convert_df(m)

    st.download_button(
        label="Descargar datos",
        data=data3,
        file_name=f'detalle_importaciones_usa_{estado}.csv',
        mime='text/csv',
    )