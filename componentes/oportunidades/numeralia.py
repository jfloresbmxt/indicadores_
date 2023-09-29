import streamlit as st
import plotly.express as px
from clases.oportunidades9.seccion1 import *

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('latin1')


def mapa_estados(df, ab):
    final = df.groupby("State").agg({"Importaciones del mundo":"sum",
                        "Importaciones RCEP": "sum",
                        "Importaciones México": "sum",
                        "Mercado RCEP (%)": "mean",
                        "Mercado México (%)": "mean"
                        }
                        ).reset_index()
    final = final.merge(ab)


    fig2 = px.choropleth(
        final,
        locationmode ="USA-states",
        locations="Abbreviation",
        color="Mercado México (%)",
        color_continuous_scale=["rgb(246, 243, 235)", "rgb(205, 191, 167)",
                                "rgb(175, 137, 84)","rgb(143, 114, 70)", 
                                "rgb(93, 71, 43)"],
        hover_name = "State",
        hover_data = {"State": False,"Abbreviation": False, "Importaciones del mundo":':,.0f'},
        custom_data=['State', "Importaciones del mundo", "Mercado RCEP (%)", "Mercado México (%)"],
        labels={"Importaciones del mundo": "Importaciones<br>Mundo"}
    )
    hovertemp = '<b>%{customdata[0]}<b><br><br>'
    hovertemp += '<b>Importaciones %{customdata[1]:,.0f}<b><br>'
    hovertemp += '<b>Mercado RCEP: %{customdata[2]:,.0f}%<b><br>'
    hovertemp += '<b>Mercado México: %{customdata[3]:,.0f}%<b><br>'
    fig2.update_geos(showcoastlines = False, showland=False, visible = False, scope="usa")
    fig2.update_traces(hovertemplate=hovertemp)
    fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig2.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Montserrat"
        ))
    
    return fig2

def numeralia(estado, ms, ab, rfcs, rfc_sectors, productos):
    st.divider()

    col3, col4, col5 = st.columns(3)
    with col3:
        st.metric(label="**Empresas exportadoras únicas**", value=len(rfcs))

    with col4:
        st.metric(label="**Productos exportados**", value=len(productos))

    with col5:
        st.metric(label="**Sectores**", value=rfc_sectors["Sector"].nunique())
    

    st.plotly_chart(mapa_estados(ms, ab), use_container_width =True)

    st.dataframe(rfc_sectors, use_container_width=True)
    data1 = convert_df(rfc_sectors)

    st.download_button(
            label="Descargar datos",
            data=data1,
            file_name=f'empresas_{estado}.csv',
            mime='text/csv',
        )