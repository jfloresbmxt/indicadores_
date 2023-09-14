import pandas as pd

def get_pib_info_subsector(df, sector):    
    df = df[df["desc"] == sector]

    #Datos del subsector
    x2022 = round(df.loc[:, "x2022"].item()/1000)
    ratio = round(df.loc[:,"ratio"].item(), 1)
    tmac_sub = round(df.loc[:, "crecimiento"].item(), 1)
    tmac_s = round(df.loc[:, "crec_nac"].item(),1)

    return [x2022, str(ratio), str(tmac_sub), str(tmac_s), df]


def get_exports_info_subsector(df, sector):    
    df = df[df["desc"] == sector]

    #Datos del subsector
    x2022 = round(df.loc[:, "x2022"].item())
    ratio = round(df.loc[:,"ratio"].item(), 1)
    tmac_sub = round(df.loc[:, "crecimiento"].item(),1)
    tmac_s = round(df.loc[:, "crec_nac"].item(),1)


    return [x2022, str(tmac_sub), str(ratio), str(tmac_s)]


def top_5(df, sector):

    df = (df[df["desc"] == sector]
          .sort_values("rankn")
          .head(4)
          .loc[:, "estado"]
          .to_list()
          )
    
    if len(df) == 0:
        df = "No aplica"
        return "No aplica"
    else:
        return df


def get_ied_info_subsector(df, ied_estatal, sector):
    df = df[df["desc"] == sector]
    acumulado = round(df.loc[:, "acumulado"].item())
    ratio = round(df.loc[:, "ratio"].item(),1)

    top = top_5(ied_estatal, sector)

    return [acumulado, ratio, top]