import streamlit as st
import json
import pandas as pd
from streamlit_extras.stylable_container import stylable_container
from componentes.header import header, subheader
from componentes.seccion1 import seccion1
from clases.seccion1 import *
from componentes.seccion2 import *
from componentes.seccion3 import *
from componentes.seccion4 import *

st.set_page_config(
    page_title="Información estatal",
    layout="wide"
)

@st.cache_data
def get_info():
    sectores = pd.read_excel("../sectorial/sectorial_pib_v2.xlsx", dtype={"sector":str})
    sectores = sectores[["sector","desc"]]
    sectores_prioritarios = ["111", "112", "311", "314", "321", "322", "325", "326", "327",
                        "331", "332", "333", "334", "335", "336", "337", "339"]
    sectores = sectores[sectores.sector.isin(sectores_prioritarios)]
    
    pib = pd.read_excel("../sectorial/sectorial_pib_v2.xlsx").fillna(0)

    xs = pd.read_excel("../sectorial/sectorial_xs_v2.xlsx")
    xs = xs.merge(sectores, on="sector", how = "right").fillna(0)

    ied = pd.read_excel("../sectorial/sectorial_ied_v2.xlsx", dtype={"sector":str})
    ied = ied.merge(sectores, on="sector")

    ied_estatal = pd.read_excel("../estatal/estatales_ied.xlsx")
    ied_estatal = ied_estatal.merge(sectores, on="sector")

    estatal = pd.read_excel("../estatal/estatales_pib.xlsx").fillna(0)
    estatal["sector"] =  estatal["sector"].apply(lambda x: x.replace("-",""))
    estatal = estatal.merge(sectores, on="sector", how="left").drop(columns={"desc_x"}).rename(columns={"desc_y": "desc"})

    xs_estatal = pd.read_excel("../estatal/estatales_xs.xlsx")
    xs_estatal = xs_estatal.merge(sectores, on="sector", how="left")

    with open('./data/mx_geojson.json', 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)
    
    vaemg = pd.read_excel("../sectorial/sectorial_vaemg_v2.xlsx", dtype={"sector":str})
    vaemg =vaemg.merge(sectores, on="sector")

    return [pib, xs, ied, ied_estatal, sectores, estatal, xs_estatal, json_object, vaemg]

pib, xs, ied, ied_estatal, sectores, estatal, xs_estatal, json_object, vaemg = get_info()

choice = st.selectbox("Selecciona sector", sectores["desc"])

# # Header
header(choice)
subheader()

## Secccion 1
pib_params = get_pib_info_subsector(pib, choice)
xs_params = get_exports_info_subsector(xs, choice)
ied_params = get_ied_info_subsector(ied, ied_estatal, choice)

seccion1(pib_params, xs_params, ied_params)

##  Seccion 2
seccion2(estatal, choice, json_object)

##  Seccion 3
seccion3(xs_estatal, choice, json_object)

## Seccion4
seccion4(vaemg, choice)