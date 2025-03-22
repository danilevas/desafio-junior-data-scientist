import basedosdados as bd
import os
import pandas as pd
import numpy as np
from datetime import date

def puxa_dados():
    id_projeto = "processo-seletivo-pcrj"

    # Pegando só o que precisamos!
    query = """SELECT id_chamado, DATE(data_abertura) as data_abertura, tipo, subtipo, id_bairro
    FROM `datario.adm_central_atendimento_1746.chamado`
    WHERE 
    (DATE(data_abertura) = '2023-04-01'
    OR subtipo = 'Perturbação do sossego'
    OR tipo = 'Perturbação do sossego')
    AND DATE(data_abertura) >= '2022-01-01'
    ORDER BY id_chamado"""
    df_chamados = bd.read_sql(query, billing_project_id=id_projeto)
    df_chamados.to_csv("csvs/analise_python/chamados.csv", encoding="utf-8", index=False)

    query = """SELECT id_bairro, nome, subprefeitura
    FROM `datario.dados_mestres.bairro`
    ORDER BY id_bairro"""
    df_bairros = bd.read_sql(query, billing_project_id=id_projeto)
    df_bairros.to_csv("csvs/analise_python/bairros.csv", encoding="utf-8", index=False)

    query = """SELECT ano, data_inicial, data_final, evento, taxa_ocupacao
    FROM `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos`
    ORDER BY data_inicial"""
    df_eventos = bd.read_sql(query, billing_project_id=id_projeto)
    df_eventos.to_csv("csvs/analise_python/eventos.csv", encoding="utf-8", index=False)

    return df_chamados, df_bairros, df_eventos

# Se os arquivos não existirem, puxa os dados do BigQuery
if not (os.path.exists("csvs/analise_python/chamados.csv") and os.path.exists("csvs/analise_python/bairros.csv") and os.path.exists("csvs/analise_python/eventos.csv")):
    puxa_dados()
    print("Dados puxados do BigQuery")

# Cria o arquivo txt com as respostas_analise_python
with open('respostas_analise_python.txt', 'w', encoding="utf-8") as f: pass

# Carregar o arquivo CSV
chamados = pd.read_csv('csvs/analise_python/chamados.csv')

# Q1.

# Contar os valores nulos na coluna 'id_chamado'
total_nulls_subpref = chamados[chamados['id_chamado'].isnull()].shape[0]

# Não há nenhum.

# Converter a coluna 'data_abertura' para o tipo datetime
chamados['data_abertura'] = pd.to_datetime(chamados['data_abertura'])

# Filtrar para a data específica (01/04/2023)
chamados_01_04_2023 = chamados[chamados['data_abertura'].dt.date == pd.to_datetime('2023-04-01').date()]

# Agrupar por data (somente a data, sem a hora) e contar os 'id_chamado' válidos (não nulos)
chamados_por_data = chamados_01_04_2023[chamados_01_04_2023['id_chamado'].notnull()] \
    .groupby(chamados_01_04_2023['data_abertura'].dt.date)['id_chamado'].count()

chamados_por_data.to_csv("csvs/analise_python/1.2_chamados_01_04_2023.csv", index=False)

with open('respostas_analise_python.txt', 'a', encoding="utf-8") as f: 
    f.write(f"Resposta Questão 1: foram abertos {chamados_por_data.values[0]} chamados no dia 01/04/2023.\n\n")

# Q2.

# Agrupar por tipo de chamado e contar os 'id_chamado' válidos (não nulos)
chamados_por_tipo = chamados_01_04_2023[chamados_01_04_2023['id_chamado'].notnull()] \
    .groupby('tipo')['id_chamado'].count() \
    .reset_index(name='chamados_totais')

# Ordenar pelo número de chamados totais em ordem decrescente
chamados_por_tipo = chamados_por_tipo.sort_values(by='chamados_totais', ascending=False)
chamados_por_tipo.to_csv("csvs/analise_python/2_chamados_por_tipo_01_04_2023.csv", index=False)

with open('respostas_analise_python.txt', 'a', encoding="utf-8") as f: 
    f.write(f"Resposta Questão 2: o tipo de chamado que teve mais chamados abertos no dia 01/04/2023 foi "
            f"{chamados_por_tipo.values[0][0]}, com {chamados_por_tipo.values[0][1]} chamados abertos.\n\n")

# Q3.

# Agrupar por id_bairro e contar os 'id_chamado' válidos (não nulos)
chamados_por_id_bairro = chamados_01_04_2023[chamados_01_04_2023['id_chamado'].notnull()] \
    .groupby('id_bairro')['id_chamado'].count() \
    .reset_index(name='chamados_totais')

# Ordenar pelo número de chamados totais em ordem decrescente
chamados_por_id_bairro = chamados_por_id_bairro.sort_values(by='chamados_totais', ascending=False)

# Salvar o resultado
chamados_por_id_bairro.to_csv("csvs/analise_python/3.1_chamados_por_id_bairro_01_04_2023.csv", index=False)

# Carregar o arquivo de bairros
bairros = pd.read_csv('csvs/analise_python/bairros.csv')

# Fazer o join entre 'chamados_por_bairro' e 'bairros' para pegar os nomes dos bairros
chamados_por_bairro = chamados_por_id_bairro.merge(bairros[['id_bairro', 'nome']], on='id_bairro', how='inner')

# Ordenar pelo número de chamados totais em ordem decrescente
chamados_por_bairro = chamados_por_bairro.sort_values(by='chamados_totais', ascending=False)

chamados_por_bairro.to_csv("csvs/analise_python/3.2_chamados_por_bairro_01_04_2023.csv", index=False)

with open('respostas_analise_python.txt', 'a', encoding="utf-8") as f: 
    f.write(f"Resposta Questão 3: Os 3 bairros que mais tiveram chamados abertos nesse dia foram:\n"
            f"    - {chamados_por_bairro.values[0][2]} ({chamados_por_bairro.values[0][1]} chamados)\n"
            f"    - {chamados_por_bairro.values[1][2]} ({chamados_por_bairro.values[1][1]} chamados)\n"
            f"    - {chamados_por_bairro.values[2][2]} ({chamados_por_bairro.values[2][1]} chamados)\n\n")
    
# Q4.

# Fazer o join entre 'chamados_filtrados' e 'bairros' para pegar as subprefeituras
chamados_por_subprefeitura = chamados_01_04_2023[chamados_01_04_2023['id_chamado'].notnull()] \
    .merge(bairros[['id_bairro', 'subprefeitura']], on='id_bairro', how='inner')

# Agrupar pelos nomes das subprefeituras e contar os chamados
chamados_por_subprefeitura = chamados_por_subprefeitura.groupby('subprefeitura')['id_chamado'].count() \
    .reset_index(name='chamados_totais')

# Ordenar pelo número de chamados totais em ordem decrescente
chamados_por_subprefeitura = chamados_por_subprefeitura.sort_values(by='chamados_totais', ascending=False)

chamados_por_subprefeitura.to_csv("csvs/analise_python/4_chamados_por_subprefeitura_01_04_2023.csv", index=False)

with open('respostas_analise_python.txt', 'a', encoding="utf-8") as f:
    f.write(f"Resposta Questão 4: a subprefeitura com mais chamados abertos nesse dia foi a {chamados_por_subprefeitura.values[0][0]}, "
            f"com {chamados_por_subprefeitura.values[0][1]} chamados abertos.\n\n")
    
# Q5.

# Contar quantos valores nulos existem na coluna 'subprefeitura'
total_nulls_subpref = bairros['subprefeitura'].isnull().sum()

# Contar quantos valores nulos existem na coluna 'id_bairro' dentro dos chamados filtrados para 01/04/2023
total_nulls_id_bairro = chamados_01_04_2023['id_bairro'].isnull().sum()

with open('respostas_analise_python.txt', 'a', encoding="utf-8") as f:
    f.write(f"Resposta Questão 5: Temos {total_nulls_id_bairro} chamados com id_bairro = NULL. Os chamados não tem nenhum tipo de dado de localização. Minhas suposições são que o responsável não pediu ou não conseguiu descobrir a localização "
            f"da pessoa que ligou, ou que são chamados para os quais essa informação não era relevante.")

# Q6.

# Filtrar os chamados para o período especificado e para o subtipo "Perturbação do sossego"
chamados_subtipo_perturb_sossego = chamados[
    (chamados['subtipo'] == 'Perturbação do sossego') &
    (chamados['data_abertura'].dt.date.between(pd.to_datetime('2022-01-01').date(), pd.to_datetime('2023-12-31').date()))
]

# Contar o total de chamados por subtipo
total_subtipo = chamados_subtipo_perturb_sossego['id_chamado'].count()

# Como o total de chamados com esse subtipo nesse período é 0, vamos tentar olhar os chamados com o TIPO "Perturbação do sossego".

# Filtrar os chamados para o período especificado e para o tipo "Perturbação do sossego"
chamados_tipo_perturb_sossego = chamados[
    (chamados['tipo'] == 'Perturbação do sossego') &
    (chamados['data_abertura'].dt.date.between(pd.to_datetime('2022-01-01').date(), pd.to_datetime('2023-12-31').date()))
]

chamados_tipo_perturb_sossego.to_csv("csvs/analise_python/6.5_chamados_tipo_perturb_sossego_por_data_2022_2023.csv", index=False)

# Contar o total de chamados por tipo
total_tipo = chamados_tipo_perturb_sossego['id_chamado'].count()

with open('respostas_analise_python.txt', 'a', encoding="utf-8") as f:
    f.write(f"Resposta Questão 6: nenhum chamado com o subtipo \"Perturbação do sossego\" foi aberto desde 01/01/2022 até 31/12/2023 (incluindo extremidades), "
            f"porém, neste período, foram abertos {total_tipo} chamados com o TIPO \"Perturbação do sossego\".\n\n")
    
# Q7.

# Carregar o arquivo de eventos
eventos = pd.read_csv('csvs/analise_python/eventos.csv')

# Converter a coluna 'taxa_ocupacao' para string e padronizar valores inválidos como NaN
eventos['taxa_ocupacao'] = eventos['taxa_ocupacao'].astype(str).str.lower().replace({'nan': np.nan, '': np.nan})

# Filtrar para remover eventos nulos ou inválidos
eventos_limpos = eventos[(eventos['evento'].notnull()) & (eventos['evento'] != '') & (eventos['evento'].str.lower() != 'nan')]

# Ordenar pelo campo 'data_inicial' e pelo nome do evento
eventos_limpos = eventos_limpos.sort_values(by=['data_inicial', 'evento'])

# Atualizando a primeira parte do Rock in Rio 2024
eventos_limpos.loc[
    (eventos_limpos['evento'] == 'Rock in Rio') & 
    (eventos_limpos['ano'] == '13/09 a 15/09 / 19/09 a 22/09 de 2024'),
    ['ano', 'data_inicial', 'data_final']
] = ['13/09 a 15/09 de 2024', '2024-09-13', '2024-09-15']

# Atualizando o Réveillon 2024-2025
eventos_limpos.loc[
    (eventos_limpos['evento'] == 'Réveillon') & 
    (eventos_limpos['ano'] == '29-31/12 e 01/01 (2024-2025)'),
    ['data_inicial', 'data_final']
] = ['2024-12-29', '2025-01-01']

# Inserindo a segunda parte do Rock in Rio 2024
nova_linha = pd.DataFrame([{
    'ano': '19/09 a 22/09 de 2024',
    'data_inicial': '2024-09-19',
    'data_final': '2024-09-22',
    'evento': 'Rock in Rio',
    'taxa_ocupacao': np.nan
}])

eventos_limpos = pd.concat([eventos_limpos, nova_linha], ignore_index=True)

# Ordenar os eventos pela data_inicial antes de gerar o evento_id
eventos_limpos = eventos_limpos.sort_values(by=['data_inicial', 'evento'])

# Adicionar uma coluna 'evento_id' numerando os eventos ordenados
eventos_limpos['evento_id'] = eventos_limpos.reset_index(drop=True).index + 1

# Reordenar as colunas para manter o mesmo formato da SQL
eventos_limpos = eventos_limpos[['evento_id', 'ano', 'data_inicial', 'data_final', 'evento', 'taxa_ocupacao']]

eventos_limpos.to_csv("csvs/analise_python/7.1_eventos_tratados.csv", index=False)

# Filtrar os chamados com subtipo "Perturbação do sossego"
chamados_subtipo_perturb_sossego = chamados[chamados['subtipo'] == 'Perturbação do sossego']

# Filtrar os eventos dentro do intervalo de data de cada evento
eventos_chamados = []

for _, evento in eventos_limpos.iterrows():
    data_inicial_evento = evento['data_inicial']
    data_final_eventp = evento['data_final']
    
    # Selecionar os chamados que ocorreram entre as datas do evento
    chamados_evento = chamados_subtipo_perturb_sossego[(chamados_subtipo_perturb_sossego['data_abertura'] >= data_inicial_evento) &
                                           (chamados_subtipo_perturb_sossego['data_abertura'] <= data_final_eventp)]
    
    # Adicionar o evento_id e evento ao DataFrame de chamados
    chamados_evento['evento_id'] = evento['evento_id']
    chamados_evento['evento'] = evento['evento']
    chamados_evento['data_inicial'] = evento['data_inicial']
    chamados_evento['data_final'] = evento['data_final']
    
    eventos_chamados.append(chamados_evento)

# Concatenar todos os DataFrames de chamados por evento
resultado = pd.concat(eventos_chamados)

# Ordenar pelo evento_id e id_chamado
resultado = resultado[['evento_id', 'evento', 'data_inicial', 'data_final', 'id_chamado']].sort_values(by=['evento_id', 'id_chamado'])

# Exibir o resultado
print(resultado)

# O dataframe retornado está vazio, logo não houveram chamados do subtipo "Perturbação do sossego" nos dias dos eventos.
# Vamos checar chamados com o tipo de mesmo nome.

# Filtrar os chamados com tipo "Perturbação do sossego"
chamados_subtipo_perturb_sossego = chamados[chamados['tipo'] == 'Perturbação do sossego']

# Filtrar os eventos dentro do intervalo de data de cada evento
eventos_chamados = []

for _, evento in eventos_limpos.iterrows():
    data_inicial_evento = evento['data_inicial']
    data_final_eventp = evento['data_final']
    
    # Selecionar os chamados que ocorreram entre as datas do evento
    chamados_evento = chamados_subtipo_perturb_sossego[(chamados_subtipo_perturb_sossego['data_abertura'] >= data_inicial_evento) &
                                           (chamados_subtipo_perturb_sossego['data_abertura'] <= data_final_eventp)]
    
    # Adicionar o evento_id e evento ao DataFrame de chamados
    chamados_evento['evento_id'] = evento['evento_id']
    chamados_evento['evento'] = evento['evento']
    chamados_evento['data_inicial'] = evento['data_inicial']
    chamados_evento['data_final'] = evento['data_final']
    
    eventos_chamados.append(chamados_evento)

# Concatenar todos os DataFrames de chamados por evento
resultado = pd.concat(eventos_chamados)

# Ordenar pelo evento_id e id_chamado (aqui estou colocando a data de abertura do chamado também, diferentemente da versão em SQL,
# porque irá me economizar retrabalho quando eu for separar os chamados por dia de evento posteriormente.)
resultado = resultado[['evento_id', 'evento', 'data_inicial', 'data_final', 'data_abertura', 'id_chamado']].sort_values(by=['evento_id', 'id_chamado'])

resultado.to_csv("csvs/analise_python/7.2_chamados_tipo_perturb_sossego_dias_de_evento.csv", index=False)

# Contar o número de linhas do DataFrame resultado
num_linhas = resultado.shape[0]

# Exibir a quantidade de linhas
print(f"Quantidade de linhas: {num_linhas}")

with open('respostas_analise_python.txt', 'a', encoding="utf-8") as f:
    f.write(f"Resposta Questão 7: não temos nenhum chamado com o subtipo \"Perturbação do sossego\" aberto durante os eventos "
            f"contidos na tabela de eventos (Reveillon, Carnaval e Rock in Rio), porém temos {num_linhas} chamados com o subtipo \"Perturbação do sossego\" "
            f"abertos durante esses períodos.\n\n"
            f"A tabela dos eventos tratada está no arquivo \"csvs/analise_python/7.1_eventos_tratados.csv\" "
            f"e a tabela com os chamados de tipo \"Perturbação do sossego\" abertos durante os eventos selecionados pelo id_chamado, "
            f"juntamente com o evento a qual estão associados (caracterizado pelo evento_id), "
            f"está no arquivo \"csvs/analise_python/7.2_chamados_tipo_perturb_sossego_dias_de_evento.csv\".\n"
            f"Coloquei também nesse arquivo as datas de início e fim dos eventos para diferenciar os de mesmo nome sem ter que consultar duas tabelas.\n\n")

# Q8.

# Contar a quantidade de chamados por evento já filtrado com o tipo "Perturbação do sossego" e a data dos eventos
resultado2 = resultado \
    .groupby(['evento_id', 'evento', 'data_inicial', 'data_final']) \
    .size() \
    .reset_index(name='total_chamados') \
    .sort_values(by='evento_id')

resultado2.to_csv("csvs/analise_python/8.2_num_chamados_tipo_perturb_sossego_por_evento.csv", index=False)

with open('respostas_analise_python.txt', 'a', encoding="utf-8") as f:
    f.write(f"Resposta Questão 8: 0 chamados com o subtipo \"Perturbação do sossego\" foram abertos nos dias dos eventos da tabela de eventos, "
            f"mas {num_linhas} chamados com o TIPO \"Perturbação do sossego\" foram abertos nesses dias.\n"
            f"Para ver quantos chamados foram abertos nos dias de cada evento, consulte o arquivo "
            f"\"csvs/analise_python/8.2_num_chamados_tipo_perturb_sossego_por_evento\"\n\n")

# Q9.

# Calculando a quantidade de dias de cada evento
resultado['data_inicial'] = pd.to_datetime(resultado['data_inicial'])
resultado['data_final'] = pd.to_datetime(resultado['data_final'])

# Calculando a quantidade de dias de cada evento
resultado['dias_evento'] = (resultado['data_final'] - resultado['data_inicial']).dt.days + 1

# Agora, contamos o número de chamados por evento
chamados_por_evento = resultado.groupby(['evento_id', 'evento', 'data_inicial', 'data_final'])['id_chamado'].nunique()

# Calculando a média diária
media_diaria = (chamados_por_evento / resultado.groupby(['evento_id', 'evento', 'data_inicial', 'data_final'])['dias_evento'].first()).reset_index(name='media_diaria')

# Ordenando pela média diária
media_diaria = media_diaria.sort_values(by='media_diaria', ascending=False)

# Arredondando os valores para 2 casas decimais
media_diaria["media_diaria"] = media_diaria["media_diaria"].apply(lambda x: round(x, 2))

media_diaria.to_csv("csvs/analise_python/9.2_medias_diarias_chamados_tipo_perturb_sossego_eventos.csv", index=False)

with open('respostas_analise_python.txt', 'a', encoding="utf-8") as f:
    f.write(f"Resposta Questão 9: o evento com a maior média diária de chamados com o tipo \"Perturbação do sossego\" foi o "
    f"{media_diaria.values[0][1]} que ocorreu entre os dias {media_diaria.values[0][2].date()} e {media_diaria.values[0][3].date()}, "
    f"com uma média de {round(media_diaria.values[0][4], 2)} chamados por dia de evento.\n\n")

# Q10.

def diferenca_percentual(valor1, valor2):
    return f"{str(round(((valor1 - valor2)/valor2) * 100, 2))}%"

# Calculando a quantidade de dias entre as datas especificadas
dias_entre = (date(2023, 12, 31) - date(2022, 1, 1)).days + 1

# Calculando a média diária de chamados do tipo "Perturbação do sossego" no periódo especificado
media_diaria_22_23 = round(total_tipo/dias_entre, 2)

# Aplicando a fórmula para calcular a diferença percentual entre os valores da coluna "media_diaria" e a média diária de 2022 e 2023
media_diaria["pct_diferenca"] = media_diaria["media_diaria"].apply(lambda x: diferenca_percentual(x, media_diaria_22_23))

media_diaria.to_csv("csvs/analise_python/10.2_compara_medias_diarias_chamados_tipo_perturb_sossego_eventos_vs_2022_2023.csv", index=False)

with open('respostas_analise_python.txt', 'a', encoding="utf-8") as f:
    f.write(f"Resposta Questão 10. As comparações das médias diárias de chamados com o tipo \"Perturbação do sossego\" nos períodos de cada evento da tabela de eventos "
            f"e no período de 01/01/2022 até 31/12/2023 estão no arquivo \"csvs/analise_sql/10.2_compara_medias_diarias_chamados_tipo_perturb_sossego_eventos_vs_2022_2023\"")