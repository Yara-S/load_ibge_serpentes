import pandas as pd
import requests


import time



#load de municipios
df_geral = pd.read_excel("municipios.xlsx")
param = {'groupBy':'localidade' }

#2009
estabelecimentos_sus = 28242
#2017
pib_per_capita = 47001
despesas_emp = 29749
total_receitas = 28141
ideb_anos_iniciais = 78187
ideb_ano_finais = 78192
mortalidade_inf = 30279

#salario_medio_mensal = 29765
#2010 --------------
densidade_demografica = 29168
idh = 30255
arbo_vias_publicas = 60029
urba_vias_publicas = 60031
esgo_sanitario = 60030
perc_12salario_min = 60037
taxa_escola_6a12 = 60045

#2016
diarreia=60032
lista_indicadores = ['60032']
cols = ['id_MUNICIPIO',  'Internacoes_Diarreia']

#monta string de municipios
df_mun = df_geral['id_MUNICIPIO']

inicio_count=0
fim_count=10
final_2016 = pd.DataFrame()
while (fim_count <= 5570):
	try:
		municipios_request='|'.join(map(str, df_mun[inicio_count:fim_count]))

		populacao_residente_df = requests.get("https://servicodados.ibge.gov.br/api/v1/pesquisas/-/indicadores/{}/resultados/{}".format('|'.join(lista_indicadores), municipios_request)
									, verify= False, params=param)

		#print(populacao_residente_df.text)
		#print('|'.join(lista_indicadores))


		populacao_residente_df = pd.DataFrame(populacao_residente_df.json())

		#print(populacao_residente_df.res[0])
		try:
			populacao_residente_df.res = populacao_residente_df.res.apply(lambda x: str(x[0]['res']['2016']))
		except Exception as e:
			try:
				populacao_residente_df.res = populacao_residente_df.res.apply(lambda x: '-')
			except Exception as e:
				print("dado inexistente")
				print(str(e))
		populacao_residente_df.localidade = populacao_residente_df.localidade.apply(lambda x: int(x))
		#print("passei")
		populacao_residente_df.set_index('localidade', inplace=True)
		populacao_residente_df = pd.DataFrame(populacao_residente_df.res.values.tolist(), populacao_residente_df.index).add_prefix('code_')
		populacao_residente_df.reset_index(inplace=True)
		#print("aqui")
		print("Request ate o municipio "+ str(fim_count))
		inicio_count = fim_count
		fim_count += 10

		final_2016 = pd.concat([final_2016, populacao_residente_df])
		#time.sleep(2)
	except Exception as e:
		print(str(e))
		#print(populacao_residente_df.res[0])
		final_2016.to_excel("final_bkp.xlsx")
	#print(final_2009)
final_2016.columns = cols
final_2016.set_index('id_MUNICIPIO', inplace=True)
final_2016.to_excel("final_2016.xlsx")





