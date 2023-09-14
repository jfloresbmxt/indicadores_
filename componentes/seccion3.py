import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from clases.seccion3 import *


def seccion3(e, choice, json_object):
    fig1, ratio = fig_bar_xs(e, choice)
    map1 = gen_map(e, choice, "t2022", json_object)

    st.header("Exportaciones")
    with stylable_container(
            key="container_with_border2",
            css_styles="""
            {
                text-align: center;
                # padding: 0px 0px 0px 30px;
            }
            """
            ): col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(map1,  use_container_width=True)            

    with col2:
        
            st.markdown(f'''
            <p style ='line-height: 1.5rem;'>
            <b>Principales 10 estados exportadores, 2022</b>
            </p>
            <p style ='line-height: 0rem;'>
            {ratio}% de las exportaciones del sector
            <p>
            Millones USD
            ''', unsafe_allow_html=True)
            st.plotly_chart(fig1,  use_container_width=True)