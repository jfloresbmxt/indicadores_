import streamlit as st
from polars import read_parquet, col, read_excel, Int64
import pandas as pd
from clases.oportunidades.seccion1 import *
st.header("Oportunidades Nearshoring")

@st.cache_data
def get_data():
    exports_mx = read_parquet("data/master.parquet")

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

col1, col2 = st.columns(2)

with col1:
    estado = st.selectbox(
        "**Selecciona el estado**",
        lista_estados
    )
    

with col2:
    st.markdown("**Conjuto de productos**")
    agree = st.checkbox('240 productos', value=True)
    

rango = st.slider('**Rango de exportaciones**', 0, 50000, 50000)

def choice(agree):
    if agree:
        n = 1
        return n
    else:
        n = 0
        return n

st.divider()
rfcs, rfc_sectors, productos  = gen_numeralia(exports_mx, estado, rango, choice(agree))

ms = (imports.filter(col("partida").is_in(productos))).to_pandas()

m = pipeline(ms)


col3, col4 = st.columns(2)
with col3:
    st.metric(label="**Empresas exportadoras únicas**", value=len(rfcs))

with col4:
    st.metric(label="**Productos exportados**", value=len(productos))

st.dataframe(rfc_sectors, use_container_width=True)
data1 = convert_df(rfc_sectors)

st.download_button(
    label="Descargar datos",
    data=data1,
    file_name=f'empresas_{estado}.csv',
    mime='text/csv',
)

st.divider()
def data_w(df):
    df = df.groupby("Región").agg({"Importaciones del mundo":"sum",
                                      "Importaciones RCEP":"sum",
                                      "Importaciones México":"sum",
                                      "Productos": "sum"
                                      })
    
    df["GAP RCEP"] = df["Importaciones del mundo"] - df["Importaciones RCEP"]
    df["GAP México"] = df["Importaciones del mundo"] - df["Importaciones México"]

    df["Mercado RCEP (%)"] = (df["Importaciones RCEP"] / df["Importaciones del mundo"])*100
    df["Mercado México (%)"] = (df["Importaciones México"] / df["Importaciones del mundo"])*100
    
    return df

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
data3 = convert_df(rfc_sectors)

st.download_button(
    label="Descargar datos",
    data=data3,
    file_name=f'detalle_importaciones_usa_{estado}.csv',
    mime='text/csv',
)
