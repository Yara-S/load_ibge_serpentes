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


#2018
salario_medio_mensal = 29765
docentes_ef = 5929
docentes_em = 5934
n_escolas_ef = 5950
n_escolas_em = 5955
matriculas_em = 5913
matriculas_ef = 5908
pessoal_ocupado = 29763

#2010 --------------
densidade_demografica = 29168
idh = 30255
arbo_vias_publicas = 60029
urba_vias_publicas = 60031
esgo_sanitario = 60030
perc_12salario_min = 60037
taxa_escola_6a12 = 60045

#2019
pop_estimada = 29171
area_territorial=29167
bioma = 77861
sistema_costeiro = 82270

lista_indicadores = ['29167','29171', '77861', '82270']
cols = ['id_MUNICIPIO','Area_Territorial' ,'Populacao_Estimada','Bioma', 'Sistema_Costeiro']
#monta string de municipios
df_mun = df_geral['id_MUNICIPIO']

inicio_count=0
fim_count=10
final_2019 = pd.DataFrame()
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
			populacao_residente_df.res = populacao_residente_df.res.apply(lambda x: [str(item['res']['2019']) for item in x])
		except Exception as e:
			try:
				populacao_residente_df.res = populacao_residente_df.res.apply(lambda x: [str(item['res']['2019'])  if '2019' in item['res'] else  '-' for item in x])
			except Exception as e:
				print("dado inexistente")
		populacao_residente_df.localidade = populacao_residente_df.localidade.apply(lambda x: int(x))
		#print("passei")
		populacao_residente_df.set_index('localidade', inplace=True)
		populacao_residente_df = pd.DataFrame(populacao_residente_df.res.values.tolist(), populacao_residente_df.index).add_prefix('code_')
		populacao_residente_df.reset_index(inplace=True)
		#print("aqui")
		print("Request ate o municipio "+ str(fim_count))
		inicio_count = fim_count
		fim_count += 10

		final_2019 = pd.concat([final_2019, populacao_residente_df])
		#time.sleep(2)
	except Exception as e:
		print(str(e))
		#print(populacao_residente_df.res[0])
		final_2019.to_excel("final_bkp.xlsx")
	#print(final_2019)

final_2019.columns = cols
final_2019.set_index('id_MUNICIPIO', inplace=True)
final_2019.to_excel("final_2019.xlsx")





