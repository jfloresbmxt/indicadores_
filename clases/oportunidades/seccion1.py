import polars as pl
from polars import col
import pandas as pd


def gen_numeralia(exports_mx, estado:str, cota:int, n, p):
    # Generamos lista de rfcs que exportan mas de 50k al año
    rfcs =  (exports_mx
            .filter(col("d_estado") == estado)
            .filter((col("d_240") == 1) | (col("d_240") == n))
            .filter((col("prioritario") == 1) | (col("prioritario") == p))
            .groupby(["rfc"])
            .agg(col("val_usd").sum())
            .filter(col("val_usd") > cota)
            .unique()
            .to_series()
            .to_list()
    )

    # Generamos listado de empresas por sector y numero de productos
    rfcs_sector =  (exports_mx
                    .filter(col("d_estado") == estado)
                    .filter((col("d_240") == 1) | (col("d_240") == n))
                    .filter((col("prioritario") == 1) | (col("prioritario") == p))
                    .filter((col("rfc").is_in(rfcs)))
                    .groupby(["sector", "descripcion"])
                    .agg(col("val_usd").sum(),
                         col("rfc").n_unique(),
                         col("fraccion").n_unique()
                         )
                    .to_pandas()
    )
    rfcs_sector.columns = ["Sector", "Descripción", "Exportaciones",
                            "Empresas", "Productos"]

    # Generamos listado de los productos que exportan esas empresas sin importar si son mayores a 50k
    productos = (exports_mx
                .filter((col("rfc").is_in(rfcs)) & 
                        ((col("d_240") == 1) | (col("d_240") == n)) &
                        ((col("prioritario") == 1) | (col("prioritario") == p)) &
                        (col("d_estado") == estado)
                        )
                .select(col("fraccion"))
                .unique()
                .to_series()
                .to_list()
                )
    

    return [rfcs, rfcs_sector, productos]       



def pipeline(total):
    sectores = pd.read_excel("data/subsectores.xlsx", dtype={"sector":str})
    sectores["subsector_nombre"] = sectores["subsector_nombre"].str[6:]
    sectores.rename(columns={"subsector_nombre": "Descripción"}, inplace=True)

    rcep = ["AUSTRALIA", "BRUNEI", "CAMBODIA", "CHINA", "KOREA, SOUTH", "PHILIPPINES", "INDONESIA",
        "JAPAN", "LAOS", "MALAYSIA", "BURMA", "NEW ZEALAND", "SINGAPORE", "THAILAND", "VIETNAM"]

    all_c = (total
    .query("country_name == 'TOTAL FOR ALL COUNTRIES'")
    .query("val_gen >0")
    .groupby(["region", "sector"])
    .agg({"val_gen":"sum", "partida":"nunique"})
    .reset_index()
    .drop(columns={"partida"})
    .rename(columns={"val_gen":"total"})
    )

    df_rcep = (total
    .query(f"country_name.isin({rcep})")
    .query("val_gen >0")
    .groupby(["region", "sector"])
    .agg({"val_gen":"sum", "partida":"nunique"})
    .reset_index()
    .drop(columns={"partida"})
    .rename(columns={"val_gen":"rcep"})
    )

    mexico = (total
        .query("country_name == 'MEXICO'")
        .query("val_gen > 0")
        .groupby(["region", "sector"])
        .agg({"val_gen":"sum", "partida":"nunique"})
        .reset_index()
        .rename(columns={"val_gen":"mexico"})
        )
    
    m = all_c.merge(mexico, how= "left", on=["region", "sector"])
    m = m.merge(df_rcep, how="left", on=["region", "sector"])
    m = m.fillna(0)
    m = m[["region", "sector", "total", "rcep", "mexico", "partida"]]
    m["total"] = round(m["total"]/1000000, 0)
    m["rcep"] = round(m["rcep"]/1000000, 0)
    m["mexico"] = round(m["mexico"]/1000000, 0)
    
    m["Gap RCEP"] = m["total"] - m["rcep"]
    m["Gap México"] = m["total"] - m["mexico"]

    m["Mercado RCEP (%)"] =  round((m["rcep"]/m["total"])*100, 2)
    m["Mercado México (%)"] =  round((m["mexico"]/m["total"])*100,2)
    m.columns = ["Región", "Sector", "Importaciones del mundo",
                  "Importaciones RCEP", "Importaciones México", "Productos",
                  "GAP RCEP", "GAP México", "Mercado RCEP (%)", "Mercado México (%)"]
    
    m = pd.merge(sectores, m, left_on="sector", right_on="Sector").drop(columns={"sector"})

    m = m[["Región", "Sector", "Descripción","Importaciones del mundo",
         "Importaciones RCEP", "Importaciones México", "Productos",
         "GAP RCEP", "GAP México", "Mercado RCEP (%)", "Mercado México (%)"]]
    
    return m

def pipeline_state_s(total):
    rcep = ["AUSTRALIA", "BRUNEI", "CAMBODIA", "CHINA", "KOREA, SOUTH", "PHILIPPINES", "INDONESIA",
        "JAPAN", "LAOS", "MALAYSIA", "BURMA", "NEW ZEALAND", "SINGAPORE", "THAILAND", "VIETNAM"]

    all_c = (total
    .query("country_name == 'TOTAL FOR ALL COUNTRIES'")
    .query("val_gen >0")
    .groupby(["State", "sector"])
    .agg({"val_gen":"sum", "partida":"nunique"})
    .reset_index()
    .drop(columns={"partida"})
    .rename(columns={"val_gen":"total"})
    )

    df_rcep = (total
    .query(f"country_name.isin({rcep})")
    .query("val_gen >0")
    .groupby(["State", "sector"])
    .agg({"val_gen":"sum", "partida":"nunique"})
    .reset_index()
    .drop(columns={"partida"})
    .rename(columns={"val_gen":"rcep"})
    )

    mexico = (total
        .query("country_name == 'MEXICO'")
        .query("val_gen > 0")
        .groupby(["State", "sector"])
        .agg({"val_gen":"sum", "partida":"nunique"})
        .reset_index()
        .rename(columns={"val_gen":"mexico"})
        )
    
    m = all_c.merge(mexico, how= "left", on=["State", "sector"])
    m = m.merge(df_rcep, how="left", on=["State", "sector"])
    m = m.fillna(0)
    m = m[["sector", "total", "rcep", "mexico", "partida"]]
    
    m["Gap RCEP"] = m["total"] - m["rcep"]
    m["Gap México"] = m["total"] - m["mexico"]

    m["Mercado RCEP (%)"] =  (m["rcep"]/m["total"])*100
    m["Mercado México (%)"] =  (m["mexico"]/m["total"])*100
    m.columns = ["Sector", "Importaciones del mundo",
                  "Importaciones RCEP", "Importaciones México", "Productos",
                  "GAP RCEP", "GAP México", "Mercado RCEP (%)", "Mercado México (%)"]    

    return m

def pipeline_state_partida(total):
    rcep = ["AUSTRALIA", "BRUNEI", "CAMBODIA", "CHINA", "KOREA, SOUTH", "PHILIPPINES", "INDONESIA",
        "JAPAN", "LAOS", "MALAYSIA", "BURMA", "NEW ZEALAND", "SINGAPORE", "THAILAND", "VIETNAM"]

    all_c = (total
    .query("country_name == 'TOTAL FOR ALL COUNTRIES'")
    .query("val_gen >0")
    .groupby(["State", "partida"])
    .agg({"val_gen":"sum"})
    .reset_index()
    .rename(columns={"val_gen":"total"})
    )

    df_rcep = (total
    .query(f"country_name.isin({rcep})")
    .query("val_gen >0")
    .groupby(["State", "partida"])
    .agg({"val_gen":"sum"})
    .reset_index()
    .rename(columns={"val_gen":"rcep"})
    )

    mexico = (total
        .query("country_name == 'MEXICO'")
        .query("val_gen > 0")
        .groupby(["State", "partida"])
        .agg({"val_gen":"sum"})
        .reset_index()
        .rename(columns={"val_gen":"mexico"})
        )
    
    m = all_c.merge(mexico, how= "left", on=["State", "partida"])
    m = m.merge(df_rcep, how="left", on=["State", "partida"])
    m = m.fillna(0)
    m = m[["partida","total", "rcep", "mexico"]]
    m["total"] = m["total"]/1000000
    m["rcep"] = m["rcep"]/1000000
    m["mexico"] = m["mexico"]/1000000
    
    m["Gap RCEP"] = m["total"] - m["rcep"]
    m["Gap México"] = m["total"] - m["mexico"]

    m["Mercado RCEP (%)"] =  round((m["rcep"]/m["total"])*100, 2)
    m["Mercado México (%)"] =  round((m["mexico"]/m["total"])*100, 2)
    m.columns = ["Partida", "Importaciones del mundo",
                  "Importaciones RCEP", "Importaciones México",
                  "GAP RCEP", "GAP México", "Mercado RCEP (%)", "Mercado México (%)"]    

    return m

def data_w(df):
    df = df.groupby("Región").agg({"Importaciones del mundo":"sum",
                                      "Importaciones RCEP":"sum",
                                      "Importaciones México":"sum",
                                      "Productos": "sum"
                                      })
    
    df["GAP RCEP"] = df["Importaciones del mundo"] - df["Importaciones RCEP"]
    df["GAP México"] = df["Importaciones del mundo"] - df["Importaciones México"]

    df["Mercado RCEP (%)"] = round((df["Importaciones RCEP"] / df["Importaciones del mundo"])*100, 2)
    df["Mercado México (%)"] = round((df["Importaciones México"] / df["Importaciones del mundo"])*100, 2)
    
    return df

