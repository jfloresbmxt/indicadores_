import streamlit as st
from PIL import Image
from streamlit_extras.stylable_container import stylable_container

def metrics(sline, i, iconname):
    fontsize = 16

    htmlstr = f"""<p style='color:rgb(0, 0, 0, 0.9);
                            font-size: {fontsize}px;
                            margin: 10px;
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