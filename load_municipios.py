import pandas as pd
import requests

todos_mun = requests.get("https://servicodados.ibge.gov.br/api/v1/localidades/municipios")

df_mun = pd.DataFrame(todos_mun.json())
df_mun['UF'] = df_mun.microrregiao.apply(lambda x: x['mesorregiao']['UF']['sigla'])
df_mun['id_UF'] = df_mun.microrregiao.apply(lambda x: x['mesorregiao']['UF']['id'])
df_mun.drop(['microrregiao'], axis=1, inplace=True)
df_mun.columns = ['id_MUNICIPIO', 'MUNICIPIO', 'UF', 'id_UF']
df_mun.set_index('id_MUNICIPIO', inplace=True)

df_mun.to_excel("municipios.xlsx")
