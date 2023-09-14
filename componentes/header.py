import streamlit as st
from PIL import Image
from streamlit_extras.stylable_container import stylable_container

def header(sector):
    # Header
    col1, col2 = st.columns(2)
    with col1:
        with stylable_container(
            key="container_header",
            css_styles="""
            h2 {
                background-color: rgb(55, 91, 78);
                color: white;
                border-radius: 0.1rem;
                text-align: center;
                margin:0px 0px 10px;
            }
            header {
                padding: 0px;
                font-size: 1.5rem;
                font-weight: 800;
            }
            """,
        ): st.header(sector)

    with col2:
        image = Image.open('./Imagen1.png')
        st.image(image)

def subheader():
    with stylable_container(
            key="container_subheader",
            css_styles="""
            h3 {
                background-color: rgb(212, 193, 156);
                color: black;
                border-radius: 0.1rem;
                text-align: center;
                font-size: 1.1rem;
                padding: calc(0.5em - 1px);
                }
            """,
        ): st.subheader("Panorama general del sector")