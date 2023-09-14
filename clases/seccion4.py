import plotly.graph_objects as go
import plotly.express as px


def get_vaem_data(df, sector):
    df = (df[df["desc"] == sector]
          .drop(columns={"sector", "dif", "desc"})
          )
    df.columns = ["tipo","2012", "2013", "2014", "2015", "2016", "2017", "2018",
                  "2019", "2020", "2021"]
    df = df.T.drop("tipo").reset_index()
    df.columns = ["año","total", "nacionales", "mo"]

    return df

def line_graph(df, sector):
    df = get_vaem_data(df, sector)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["año"], y=df["total"],
        mode='lines+markers+text',
        text=df["total"],
        textposition='bottom center',
        name="Total",
        line= dict(color="#D4C19C")
    ))
    fig.add_trace(go.Scatter(
        x=df["año"], y=df["nacionales"],
        text=df["nacionales"],
        mode='lines+markers+text',
        textposition='bottom center',
        name = "Insumos nacionales",
        line= dict(color="#9D2449")
    ))
    fig.add_trace(go.Scatter(
        x=df["año"], y=df["mo"],
        text=df["mo"],
        mode='lines+markers+text',
        textposition='bottom center',
        name="Mano de obra",
        line= dict(color="#13322B")
    ))

    fig.update_yaxes(title_text="Porcentaje", rangemode="tozero")
    fig.update_xaxes(title_text="Año")

    fig.update_layout(template="simple_white",
                  hovermode="x unified",
                  legend=dict(orientation='h', title = "", yanchor='bottom',xanchor='center',y=-0.5,x=0.5)
                  )
    
    fig.update_layout(title_text="<b>Contenido nacional - VAEMG</b><br><sup>%</sup>", title_x=0.5, title_xanchor = "center")
    fig.update_traces(texttemplate='%{text:,.1f}')
    fig.update_traces(hovertemplate = '%{y:,.1f} ')
    
    
    return fig