import streamlit as st
from pandas import read_excel

st.header("Vocaciones productivas")

@st.cache_data
def get_subsector():
    df = read_excel("data/subsector.xlsx", sheet_name = "SUBSECTOR", skiprows = 1,
                   usecols = ["Código", "Título"], dtype = {"Código": str}).dropna()
    
    df["subsector_nombre"] = df['Título'].str.replace("T", "")
    df = df.drop(columns = {"Título"})
    # df = df.set_index("Código")

    df["subsector_nombre"] = df["Código"] + " - " + df["subsector_nombre"]
    df.drop(columns={"Código"}, inplace=True)

    return df

subsector = get_subsector()

subsector = st.selectbox(
    "Selecciona el sector",
    subsector
)