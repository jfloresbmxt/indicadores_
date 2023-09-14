import plotly.graph_objects as go
import plotly.express as px

def gen_pib_estados(df, sector):
    df = df[df["desc"] == sector]

    top = (df
           .sort_values("t2021", ascending=False)
           .loc[:,["estado","t2021"]]
        )
    
    tt = df["t2021"].sum()
    ttop = top["t2021"].head(10).sum()
    tt = round((ttop/tt)*100)

    return top, tt

def fig_bar_pib(df, sector):
    df, ratio = gen_pib_estados(df, sector)
    df = df.head(10)
    
    fig = go.Figure(go.Bar(x = df["t2021"], y = df["estado"],
        marker=dict(color = "#D4C19C"),
        texttemplate = "%{x:,.0f}",
        textposition='inside',
        orientation = "h",
        hovertemplate = '%{y}: %{x:$.2f}<extra></extra>',
        showlegend = False
        ))
    fig.update_layout(template="simple_white",
                    autosize = False,
                    width=400,
                    height=300,
                    yaxis=dict(
                        autorange="reversed",
                        tickwidth = 0,
                        tickfont_size = 12
                        ),
                    xaxis = dict(
                        visible = False,
                    ),
                    margin=dict(
                        l=0,
                        r=0,
                        b=0,
                        t=0,
                        pad=3
    )
    ) 
    return fig, ratio


def change_name(df,sector):
    df = gen_pib_estados(df, sector)[0]
    df["estado"] = df["estado"].apply(lambda x: "Michoacán" if x == "Michoacán de Ocampo" else x)
    df["estado"] = df["estado"].apply(lambda x: "Coahuila" if x == "Coahuila de Zaragoza" else x)
    df["estado"] = df["estado"].apply(lambda x: "Veracruz" if x == "Veracruz de Ignacio de la Llave" else x)

    return df

def gen_map(df1, sector, var, json_object):
    df = change_name(df1, sector)

    fig = px.choropleth(df, 
                            geojson= json_object, 
                            locations = 'estado', # nombre de la columna del Dataframe
                            featureidkey= 'properties.name',  # ruta al campo del archivo GeoJSON con el que se hará la relación (nombre de los estados)
                            color = var, #El color depende de las cantidades
                            # color_continuous_scale = ["#d2eee7","#1f5247", "#040b0a"],
                            color_continuous_scale= px.colors.sequential.amp,
                            hover_name = "estado",
                            hover_data = {"estado": False, var:':.2f'},
                            custom_data=['estado', var],
                            center = {'lat': 25, 'lon': -99},
                            labels={var: "PIB estatal"}
                    )
    hovertemp = '<b>%{customdata[0]}<b><br><br>'
    hovertemp += '<b>%{customdata[1]:,.0f} Millones<b><br>'
    fig.update_geos(showcoastlines = False, showland=False, visible = False, fitbounds="locations")
    fig.update_traces(hovertemplate=hovertemp)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(coloraxis=dict(colorbar=dict(orientation='h', y=0.8)))
    fig.update_layout(
        width=300,
        height=400,
    hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        # font_family="Rockwell"
    ))

    return fig