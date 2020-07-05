import pandas as pd
import requests


import time



#load de municipios
df_geral = pd.read_excel("municipios.xlsx")
param = {'groupBy':'localidade' }

#2010
populacao_residente = 25207
#salario_medio_mensal = 29765
densidade_demografica = 29168
idh = 30255
arbo_vias_publicas = 60029
urba_vias_publicas = 60031
esgo_sanitario = 60030
perc_12salario_min = 60037
taxa_escola_6a12 = 60045
lista_indicadores = ['25207','29168', '30255','60029', '60030', '60031', '60037','60045']
cols = ['id_MUNICIPIO', 'Populacao_residente', 'Densid_Demografica', 'IDH', 'Arborizacao_vias_pub', 'Esgoto_sanitario', 'Urbanizacao_vias_pub', 'Percent_1_5_salario_min', 'Taxa_escolar_6a12']

#monta string de municipios
df_mun = df_geral['id_MUNICIPIO']

inicio_count=0
fim_count=10
final_2010 = pd.DataFrame()
while (fim_count <= 5570):
	try:
		municipios_request='|'.join(map(str, df_mun[inicio_count:fim_count]))

		populacao_residente_df = requests.get("https://servicodados.ibge.gov.br/api/v1/pesquisas/-/indicadores/{}/resultados/{}".format('|'.join(lista_indicadores), municipios_request)
									, verify= False, params=param)

		#print(populacao_residente_df.text)


		populacao_residente_df = pd.DataFrame(populacao_residente_df.json())
		try:
			populacao_residente_df.res = populacao_residente_df.res.apply(lambda x: [str(item['res']['2010']) for item in x])
		except Exception as e:
			populacao_residente_df.res = populacao_residente_df.res.apply(lambda x: [str(item['res']['2010']) for item in x])
		populacao_residente_df.localidade = populacao_residente_df.localidade.apply(lambda x: int(x))
		populacao_residente_df.set_index('localidade', inplace=True)
		populacao_residente_df = pd.DataFrame(populacao_residente_df.res.values.tolist(), populacao_residente_df.index).add_prefix('code_')
		populacao_residente_df.reset_index(inplace=True)
		print("Request ate o municipio "+ str(fim_count))
		inicio_count = fim_count
		fim_count += 10

		final_2010 = pd.concat([final_2010, populacao_residente_df])
		#time.sleep(2)
	except Exception as e:
		print(str(e))
		final_2010.to_excel("final_bkp.xlsx")
	#print(final_2010)
final_2010.columns = cols
final_2010.set_index('id_MUNICIPIO', inplace=True)
final_2010.to_excel("final_2010.xlsx")





