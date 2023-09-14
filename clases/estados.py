import pandas as pd
import polars as pl

class indicadores_estado:

    #Contructor
    def __init__(self, token):
        self.__token = token
    
    def __get_cinta_aduanas(self):
        df = pl.read_parquet("data/master_dp.parquet")
        df = df.with_columns(
            pl.col("scian").str.slice(0,3).alias("sector")
        )
        
        if self.__token != "Nacional":
            df = df.filter(pl.col("d_estado") == self.__token)
        
        df = df.to_pandas()

        return df
    
    
    def __gen_analytics(self, df):
        empresas_unicas = df["rfc"].nunique()
        sectores_unicos = (df["scian"].str.slice(0,3)).nunique()

        top_sectores = pd.DataFrame(df.groupby(df["scian"].str.slice(0,3))
                        .agg({"val_usd":"sum", "rfc": "nunique"})
                        .sort_values("val_usd", ascending=False)
                        )
        
        top_productos = pd.DataFrame(df.groupby("Descripción del producto")
                        .agg({"val_usd":"sum", "rfc": "nunique"})
                        .sort_values("val_usd", ascending=False)
                        .iloc[:5]
                        )

        return [df, empresas_unicas, sectores_unicos, top_sectores, top_productos]
    

    def __gen_analytics_sector(self, df):
        empresas_unicas = df["rfc"].nunique()

        top_productos = pd.DataFrame(df.groupby("Descripción del producto")
                        .agg({"val_usd":"sum", "rfc": "nunique"})
                        .sort_values("val_usd", ascending=False)
                        .iloc[:10]
                        )

        return [empresas_unicas,top_productos]


    def get_analytics(self):
        df = self.__get_cinta_aduanas()
        df = self.__gen_analytics(df)

        return df


    def get_analytics_nearshoring(self):
        df = self.__get_cinta_aduanas()
        df = df[df["d_240"] == 1]
        df = self.__gen_analytics(df)

        return df
    

    def get_analytics_sector(self, sector):
        df = self.__get_cinta_aduanas()
        df = df[df["sector"] == sector]
        df = self.__gen_analytics_sector(df)

        return df