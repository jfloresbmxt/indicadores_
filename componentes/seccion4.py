import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from clases.seccion4 import *


def seccion4(e, choice):
    fig1 = line_graph(e, choice)

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
        st.plotly_chart(fig1,  use_container_width=True)
        # st.dataframe(fig1)

    with col2:
        st.markdown(f'''
            <p style ='line-height: 1.5rem;'>
            <b>Principales 10 estados exportadores, 2022</b>
            </p>
            ''', unsafe_allow_html=True)
        # st.plotly_chart(fig1,  use_container_width=True)