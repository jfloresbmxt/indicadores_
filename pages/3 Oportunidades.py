import streamlit as st
from polars import read_parquet, col, read_excel, Int64
import pandas as pd
from clases.oportunidades.seccion1 import *
st.header("Oportunidades Nearshoring")

@st.cache_data
def get_data():
    exports_mx = read_parquet("data/masterv3.parquet")

    imports  = read_parquet("data/imports/masterv3.parquet")
    lista_estados = pd.read_excel("data/estados.xlsx")

    return [exports_mx,
            imports,
            lista_estados]

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('latin1')

exports_mx, imports, lista_estados = get_data()

col1, col2, col3 = st.columns(3)

with col1:
    estado = st.selectbox(
        "**Selecciona el estado**",
        lista_estados
    )
    
with col2:
    n = st.radio(
        "**Conjunto de productos**",
        ("Todos", "240 productos")
    )

with col3:
    p = st.radio(
        "**Sectores**",
        ("Todos", "Prioritarios")
    )
    

rango = st.slider('**Rango de exportaciones**', 0, 50000, 50000)

def choice(x):
    if x == "Todos":
        x = 0
        return x
    else:
        x = 1
        return x

st.divider()

rfcs, rfc_sectors, productos  = gen_numeralia(exports_mx, estado, rango, choice(n), choice(p))

ms = (imports.filter(col("partida").is_in(productos))).to_pandas()

m = pipeline(ms)

col3, col4, col5 = st.columns(3)
with col3:
    st.metric(label="**Empresas exportadoras únicas**", value=len(rfcs))

with col4:
    st.metric(label="**Productos exportados**", value=len(productos))

with col5:
    st.metric(label="**Sectores**", value=rfc_sectors["Sector"].nunique())

st.dataframe(rfc_sectors, use_container_width=True)
data1 = convert_df(rfc_sectors)

st.download_button(
        label="Descargar datos",
        data=data1,
        file_name=f'empresas_{estado}.csv',
        mime='text/csv',
    )

group = st.radio(
        "**Filtrar destino por**",
        ("Estado", "Región")
    )



def region():
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



def state():
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


if group == "Estado":
    state()
else:
    region()