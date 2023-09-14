import streamlit as st
# from metrics import metrics
from streamlit_extras.stylable_container import stylable_container

def metrics(sline, i, iconname):
    fontsize = 16

    htmlstr = f"""<p style='color:rgb(0, 0, 0, 0.9);
                            font-size: {fontsize}px;
                            margin: 10px 10px;
                            border-width: 1px;
                            border-style: solid;
                            border-color: rgb(221, 201, 163);
                            border-radius: 7px;
                            padding-left: 0px; 
                            padding-top: 0px;
                            padding-bottom: 8px;
                            text-align: center;'>
                            <span style='font-size: 20px;
                            font-weight: bold;'
                            >{sline}</style></span>
                            <br>
                            {i}
                            <br>
                            <span style='font-size: 10px;
                            font-weight: bold;
                            padding: 0px;
                            margin: 0px;'>________________________</style></span>
                            <br>
                            <span style='font-size: 16px;
                            padding: 0px;
                            margin: 0px;'>{iconname}</style></span>
                            </style></p>"""
    
    return htmlstr

def html(a,b,c):
    htmlstr = f"""<ol style =
                            '
                            color:rgb(0, 0, 0, 0.9);
                            font-size: 16px;
                            margin: 10px 10px;
                            list-style-position: inside;
                            border-width: 1px;
                            border-style: solid;
                            border-color: rgb(221, 201, 163);
                            border-radius: 7px;
                            padding: 7px 0px;
                            text-align: center;
                            '>
                            <li style ='margin: 0px;
                            padding: 0px 0px;'
                            >{a}</style></li>
                            <li style ='margin: 0px;
                            padding: 0px 0px;'>{b}</li>
                            <li style ='margin: 0px;
                            padding: 0px 0px;'>{c}</li>
                            </style></ol>"""
    
    return htmlstr

def html2():
    fontsize = 16

    htmlstr = f"""<p style='color:rgb(0, 0, 0, 0.9);
                            font-size: {fontsize}px;
                            margin: 10px 10px;
                            border-width: 1px;
                            border-style: solid;
                            border-color: rgb(221, 201, 163);
                            border-radius: 7px;
                            padding-left: 0px; 
                            padding-top: 0px;
                            padding-bottom: 8px;
                            text-align: center;'>
                            <span style='font-size: 20px;
                            font-weight: bold;'
                            ></style></span>
                            <br>
                            No aplica
                            <br>
                            <br>
                            <br>
                            <span style='font-size: 16px;
                            padding: 0px;
                            margin: 0px;'></style></span>
                            </style></p>"""
    
    return htmlstr

def metrics2(params):
    if params != "No aplica":
        return html(params[0],params[1],params[2])
    if params == "No aplica":
        return html2()
    

def seccion1(pib: list, xs: list, ied: list):
    pib_22, ratio, tmac_sub, tmac_s, df = pib
    xs_22, xs_tmac, xs_ratio, xs_tmac_s = xs
    acumulado, ied_ratio, top = ied


    col1, col2, col3 = st.columns(3)
    with stylable_container(
        key="container_with_border1",
        css_styles="""
            {
                border: 2px dashed rgb(221, 201, 163);
                border-radius: 0.5rem;
                padding: calc(1em - 1px);
                text-align: center;
            }
            
            """,
    ):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Producto Interno Bruto, 2022**")
            col4,col5 = st.columns(2)
            with col4:
                st.markdown(metrics(format(pib_22, ',d'), "Mil millones MXN",f"{ratio}% PIB manuf"), unsafe_allow_html=True)
            with col5:
                st.markdown(metrics(f"{tmac_sub} %", "TMAC 2018-2022",f"{tmac_s}% TMAC manuf"), unsafe_allow_html=True)

        with col2:
            st.markdown("**Exportaciones, 2022**")
            col6,col7 = st.columns(2)
            with col6:
                st.markdown(metrics(format(xs_22, ',d'), "Millones USD",f"{xs_ratio}% Xs totales"), unsafe_allow_html=True)
            with col7:
                st.markdown(metrics(f"{xs_tmac}%", "TMAC 2018-2022",f"{xs_tmac_s}% TMAC Xs totales"), unsafe_allow_html=True)

        with col3:
            st.markdown("**IED, 2018-2022**")
            col8,col9 = st.columns(2)
            with col8:
                st.markdown(metrics(format(acumulado, ",d"), "Millones USD", f"{ied_ratio}% IED total"), unsafe_allow_html=True)
            with col9:
                st.markdown(metrics2(top), unsafe_allow_html=True)