import pandas as pd

df_2009 = pd.read_excel("final_2009.xlsx")
df_2010 = pd.read_excel("final_2010.xlsx")
df_2016 = pd.read_excel("final_2016.xlsx")
df_2017 = pd.read_excel("final_2017.xlsx")
df_2018 = pd.read_excel("final_2018.xlsx")
df_2019 = pd.read_excel("final_2019.xlsx")

df_mun = pd.read_excel("municipios.xlsx")

df_mun.columns = ['id_MUNICIPIO_digito', 'MUNICIPIO', 'UF', 'id_UF']

df_mun['id_MUNICIPIO']=''
df_mun.id_MUNICIPIO = df_mun.id_MUNICIPIO_digito.apply(lambda x: ''.join(list(str(x))[:-1]))
df_mun.id_MUNICIPIO = df_mun.id_MUNICIPIO.astype(int)


df_2009.id_MUNICIPIO = df_2009.id_MUNICIPIO.astype(int)
df_2010.id_MUNICIPIO = df_2010.id_MUNICIPIO.astype(int)
df_2016.id_MUNICIPIO = df_2016.id_MUNICIPIO.astype(int)
df_2017.id_MUNICIPIO = df_2017.id_MUNICIPIO.astype(int)
df_2018.id_MUNICIPIO = df_2018.id_MUNICIPIO.astype(int)
df_2019.id_MUNICIPIO = df_2019.id_MUNICIPIO.astype(int)


load_final = pd.merge(df_mun, df_2009, on='id_MUNICIPIO', how='left')
load_final = pd.merge(load_final, df_2010, on='id_MUNICIPIO', how='left')
load_final = pd.merge(load_final, df_2016, on='id_MUNICIPIO', how='left')
load_final = pd.merge(load_final, df_2017, on='id_MUNICIPIO', how='left')
load_final = pd.merge(load_final, df_2018, on='id_MUNICIPIO', how='left')
load_final = pd.merge(load_final, df_2019, on='id_MUNICIPIO', how='left')
load_final.fillna('-', inplace=True)
load_final.set_index('id_MUNICIPIO', inplace=True)
load_final.to_excel("load_final.xlsx")