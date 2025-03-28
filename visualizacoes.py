import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from st_mapa import mostra_mapa

# Configuração da página
st.set_page_config(page_title="Dashboard Daniel Levacov", page_icon=":brain:", layout="wide")

# Paleta de cores frio-quente
calor = ["#264653", "#2a9d8f", "#e9c46a", "#f4a261", "#e76f51", "#e63946"]
cor_divisorias = "#000000"

st.markdown(
    """
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap" rel="stylesheet">
    </head>
    <h1 style="text-align: center; font-size: 45px; color: #1b3454; font-family: 'Montserrat', sans-serif;">
        Visualizações Desafio Cientista de Dados Júnior
    </h1>
    <h2 style="text-align: center; font-size: 45px; color: #1b3454; font-family: 'Montserrat', sans-serif;">
        Daniel Levacov
    </h2>
    """, 
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <hr style="border: 2px solid {cor_divisorias}; margin: 40px 0;">
    """, 
    unsafe_allow_html=True
)

st.header("Parte 1: Dados sobre os chamados do 1746")
st.write("---")
st.subheader("Capítulo 1.1: Dados sobre os chamados no dia 01/04/2023")

# Carregar os dados do CSV 
df1 = pd.read_csv('csvs/analise_sql/2_chamados_por_tipo_01_04_2023.csv')

# Invertendo a ordem dos dados e pegando o Top 10
df1 = df1.sort_values(by='chamados_totais', ascending=True).tail(10)

fig1 = px.bar(df1, 
             y='tipo', 
             x='chamados_totais', 
             title="<span style='font-size:24px; font-weight: 600;'>Tipos de chamado mais abertos no dia 01/04/2023</span>", 
             labels={'tipo': 'Tipo de Chamado', 'chamados_totais': 'Chamados Totais'},
             color='chamados_totais', 
             color_continuous_scale=calor, 
             orientation='h')

# Ajustes do tooltip
fig1.update_traces(
    hovertemplate='<b>Tipo de Chamado:</b> %{y}<br>' +
                  '<b>Chamados Totais:</b> %{x}<br>' +
                  '<extra></extra>'
)


fig1.update_layout(
    height=600,
    width=800,
    margin={'t': 50, 'b': 50, 'l': 50, 'r': 50},
    xaxis=dict(showgrid=True),
    yaxis=dict(showgrid=True),
    autosize=True,
)

# Carregar os dados do CSV
df2 = pd.read_csv('csvs/analise_sql/3.2_chamados_por_bairro_01_04_2023.csv')

# # Invertendo a ordem dos dados e pegando o Top 10
# df2_cortado = df2.sort_values(by='chamados_totais', ascending=True).tail(10)

# fig2 = px.bar(df2_cortado, 
#              y='nome', 
#              x='chamados_totais', 
#              title="<span style='font-size:24px; font-weight: 600;'>Bairros com mais chamados abertos no dia 01/04/2023</span>", 
#              labels={'nome': 'Bairro', 'chamados_totais': 'Chamados Totais'},
#              color='chamados_totais', 
#              color_continuous_scale=calor, 
#              orientation='h')

# # Ajustes do tooltip
# fig2.update_traces(
#     hovertemplate='<b>Bairro:</b> %{y}<br>' +
#                   '<b>Chamados Totais:</b> %{x}<br>' +
#                   '<extra></extra>'
# )

# fig2.update_layout(
#     height=600,
#     width=800,
#     margin={'t': 50, 'b': 50, 'l': 50, 'r': 50},
#     xaxis=dict(showgrid=True),
#     yaxis=dict(showgrid=True),
#     autosize=True,
# )

# Carregar os dados do CSV
df3 = pd.read_csv('csvs/analise_sql/4_chamados_por_subprefeitura_01_04_2023.csv')

# # Invertendo a ordem dos dados e pegando o Top 10
# df3 = df3.sort_values(by='chamados_totais', ascending=True).tail(10)

# fig3 = px.bar(df3, 
#              y='subprefeitura', 
#              x='chamados_totais',
#              title="<span style='font-size:24px; font-weight: 600;'>Subprefeituras com mais chamados abertos no dia 01/04/2023</span>", 
#              labels={'subprefeitura': 'Subprefeitura', 'chamados_totais': 'Chamados Totais'},
#              color='chamados_totais', 
#              color_continuous_scale=calor, 
#              orientation='h')

# # Ajustes do tooltip
# fig3.update_traces(
#     hovertemplate='<b>Subprefeitura:</b> %{y}<br>' +
#                   '<b>Chamados Totais:</b> %{x}<br>' +
#                   '<extra></extra>'
# )

# fig3.update_layout(
#     height=600,
#     width=800,
#     margin={'t': 50, 'b': 50, 'l': 50, 'r': 50},
#     xaxis=dict(showgrid=True),
#     yaxis=dict(showgrid=True),
#     autosize=True,
# )

# st.plotly_chart(fig3, use_container_width=False)

c1, c2 = st.columns(2)
with c1:
    st.plotly_chart(fig1, use_container_width=False)
# with c2:
#     st.plotly_chart(fig3, use_container_width=False)

# Aqui eu fiz um mapa Choropleth do Rio de Janeiro para representar os chamados no dia 01/04/2023 por bairro
# Eu peguei o GeoJSON com as referências poligonais dos bairros no site do datario, nesse link:
# https://www.data.rio/datasets/PCRJ::limite-de-bairros/explore 

# Mapeando nomes dos bairros de `datario.dados_mestres.bairro` com os nomes no GeoJSON usado para gerar o mapa
# Só para os que eu reparei que estão diferentes
dicionario_bairros = {
    "Turiaçú" : "Turiaçu",
    "Osvaldo Cruz" : "Oswaldo Cruz",
    "Quintino Bocaiúva" : "Quintino Bocaiuva"
}

# Substituindo nomes de bairros que estão diferentes dos nomes do GeoJSON
df2["nome"] = df2["nome"].replace(dicionario_bairros)

st.markdown("""
<p style="font-size: 24px; font-weight: 600;">
    <strong>Bairros com mais chamados abertos no dia 01/04/2023</strong>
</p>
""", unsafe_allow_html=True)

# Cria mapa!
fig2_mapa = mostra_mapa(df2, calor, "nome", "chamados_totais", "Chamados Totais", "arquivos_mapas/Limite_de_Bairros.geojson")

st.markdown("""
<p style="font-size: 20px;">
    Passe o mouse em cima do bairro para ver quantos chamados ele teve no dia!
</p>
""", unsafe_allow_html=True)

# Aqui eu fiz um mapa Choropleth do Rio de Janeiro para representar os chamados no dia 01/04/2023 por subprefeitura
# Eu peguei o GeoJSON com as referências poligonais das subprefeituras no site do datario, nesse link:
# https://www.data.rio/datasets/PCRJ::limites-coordenadorias-especiais-dos-bairros-subprefeituras/explore

# Mapeando nomes das subprefeituras em `datario.dados_mestres.bairro` com os nomes no GeoJSON usado para gerar o mapa
# Só para os que eu reparei que estão diferentes
dicionario_subprefeituras = {
    "Grande Tijuca" : "Tijuca",
    "Centro" : "Centro e Centro Histórico",
    "Ilhas" : "Ilhas do Governador/Fundão/Paquetá"
}

# Substituindo nomes de bairros que estão diferentes dos nomes do GeoJSON
df3["subprefeitura"] = df3["subprefeitura"].replace(dicionario_subprefeituras)

st.markdown("""
<p style="font-size: 24px; font-weight: 600;">
    <strong>Subprefeituras com mais chamados abertos no dia 01/04/2023</strong>
</p>
""", unsafe_allow_html=True)

# Cria mapa!
fig3_mapa = mostra_mapa(df3, calor, "subprefeitura", "chamados_totais", "Chamados Totais",
                         "arquivos_mapas/Limites_Coordenadorias_Especiais_dos_Bairros_-_Subprefeituras.geojson")

st.markdown("""
<p style="font-size: 20px;">
    Passe o mouse em cima da subprefeitura para ver quantos chamados ela teve no dia!
</p>
""", unsafe_allow_html=True)

st.write("---")
st.subheader("Capítulo 1.2: Análise do subtipo \"Perturbação do Sossego\" (id_subtipo 5071)")

df4 = pd.read_csv('csvs/analise_sql/8.2_num_chamados_subtipo_perturb_sossego_por_dia.csv')

# Convertendo a coluna 'data' para o tipo datetime
df4['data'] = pd.to_datetime(df4['data'])

# Agregando os dados por mês
df_mensal = df4.groupby(pd.Grouper(key='data', freq='ME')).agg({'total_chamados': 'sum'}).reset_index()

fig4 = px.bar(df_mensal, 
             x='data',
             y='total_chamados',
             title="<span style='font-size:24px; font-weight: 600;'>Quantidade de chamados do subtipo \"Perturbação do Sossego\" abertos por mês</span>", 
             labels={'data': 'Mês', 'total_chamados': 'Chamados Totais'},
             color='total_chamados', 
             color_continuous_scale=calor)

# Ajustes do tooltip
fig4.update_traces(
    hovertemplate='<b>Mês:</b> %{x}<br>' +
                  '<b>Chamados Totais:</b> %{y}<br>' +
                  '<extra></extra>'
)

fig4.update_layout(
    height=600,
    margin={'t': 50, 'b': 50, 'l': 50, 'r': 50},
    xaxis=dict(
        showgrid=True,
        tickmode='array',  # Permite definir os valores e rótulos do eixo X
        tickfont=dict(size=18)
    ),
    yaxis=dict(showgrid=True),
    autosize=True,
)

st.plotly_chart(fig4, use_container_width=False)

# df5 = pd.read_csv('csvs/analise_sql/8.2_num_chamados_subtipo_perturb_sossego_por_dia.csv')

# # Convertendo a coluna 'data' para o tipo datetime
# df5['data'] = pd.to_datetime(df5['data'])

# # Agregando os dados por mês
# df_mensal = df5.groupby(pd.Grouper(key='data', freq='ME')).agg({'total_chamados': 'sum'}).reset_index()

# fig5 = px.bar(df_mensal, 
#              x='data',
#              y='total_chamados',
#              title="Quantidade de chamados do tipo \"Perturbação do Sossego\" abertos por mês", 
#              labels={'data': 'Mês', 'total_chamados': 'Chamados Totais'},
#              color='total_chamados', 
#              color_continuous_scale=calor)

# fig5.update_layout(
#     height=600,
#     margin={'t': 50, 'b': 50, 'l': 50, 'r': 50},
#     xaxis=dict(
#         showgrid=True,
#         tickmode='array',  # Permite definir os valores e rótulos do eixo X
#         tickfont=dict(size=18)
#     ),
#     yaxis=dict(showgrid=True),
#     autosize=True,
# )

# st.plotly_chart(fig5, use_container_width=False)

st.markdown("""
    <p style="font-size: 18px;">
        Percebe-se aqui que os chamados com id_subtipo = 5071 (subtipo \"Perturbação do sossego\") começam a aparecer com quantidades escassas
        em meados de 2013, até que em meados de 2019 eles aumentam significativamente em quantidade. Esse aumento continua, até atingir um pico em Julho de 2022,
        e depois as quantidades de chamados desse subtipo começam a diminuir até que em Dezembro de 2023 elas caem significativamente. Entre Abril e Agosto de 2024,
        não há nenhum chamado do subtipo. A partir de Setembro de 2024 eles voltam a quantidades comparáveis ao período Julho de 2019 - Novembro de 2023.
    </p>
""", unsafe_allow_html=True)

st.markdown("""
    <p style="font-size: 18px; font-weight: 600;">
        Por isso, não temos chamados desse id_subtipo durante os eventos Réveillon 2023-2024, Carnaval 2024, e Rock in Rio 2024 (parte 1 e 2).
    </p>
""", unsafe_allow_html=True)

st.write("---")
st.subheader("Capítulo 1.3: Dados sobre os chamados entre 01/01/2022 e 31/12/2024")

df6 = pd.read_csv('csvs/analise_sql/8.2_num_chamados_subtipo_perturb_sossego_por_dia.csv')

# Convertendo a coluna 'data' para o tipo datetime
df6['data'] = pd.to_datetime(df6['data'])

# Recortando o período que queremos
df6 = df6[(df6['data'].dt.date.between(pd.to_datetime('2022-01-01').date(), pd.to_datetime('2024-12-31').date()))]

fig6 = px.bar(df6, 
             x='data',
             y='total_chamados',
             title="<span style='font-size:24px; font-weight: 600;'>Quantidade de chamados do subtipo \"Perturbação do Sossego\" abertos por dia entre 2022 e 2024</span>", 
             labels={'data': 'Dia', 'total_chamados': 'Chamados Totais'},
             color='total_chamados', 
             color_continuous_scale=calor)

# Ajustes do tooltip
fig6.update_traces(
    hovertemplate='<b>Dia:</b> %{x}<br>' +
                  '<b>Chamados Totais:</b> %{y}<br>' +
                  '<extra></extra>'
)

fig6.update_layout(
    height=600,
    margin={'t': 50, 'b': 50, 'l': 50, 'r': 50},
    xaxis=dict(
        showgrid=True,
        tickmode='array',  # Permite definir os valores e rótulos do eixo X
        tickfont=dict(size=18)
    ),
    yaxis=dict(showgrid=True),
    autosize=True,
)

st.plotly_chart(fig6, use_container_width=False)

st.write("---")
st.subheader("Capítulo 1.4: Dados sobre os chamados em grandes eventos")

cores = {
    'Carnaval': '#5ccb5f',
    'Réveillon': '#1b3454',
    'Rock in Rio': '#FFA500'
}

df7 = pd.read_csv('csvs/visualizacoes/chamados_eventos.csv')

fig7 = px.bar(df7, 
             x='evento',
             y='total_chamados',
             title="<span style='font-size:24px; font-weight: 600;'>Quantidade de chamados do subtipo \"Perturbação do Sossego\" abertos em grandes eventos</span>", 
             labels={'evento': 'Evento', 'total_chamados': 'Chamados Totais'},
             color='categoria',
             color_discrete_map=cores)

# Formatação para o tooltip
x2 = [evento.replace('*', ' ') for evento in df7['evento']]

# Ajustes do tooltip
fig7.update_traces(
    customdata=x2,  # Passando os valores personalizados
    hovertemplate='<b>Evento:</b> %{customdata}<br>' +
                  '<b>Chamados Totais:</b> %{y}<br>' +
                  '<extra></extra>'
)


fig7.update_layout(
    height=600,
    margin={'t': 50, 'b': 50, 'l': 50, 'r': 50},
    xaxis=dict(
        showgrid=True,
        tickmode='array',  # Permite definir os valores e rótulos do eixo X
        tickvals=df7['evento'],  # As labels dos eventos
        ticktext=[evento.replace('*', '<br>') for evento in df7['evento']],  # Quebra de linha entre as palavras do evento
        tickfont=dict(size=14)
    ),
    yaxis=dict(showgrid=True),
    autosize=True,
    legend=dict(
        font=dict(
            size=18
        )
    )
)

st.plotly_chart(fig7, use_container_width=False)

fig7_1 = px.bar(df7, 
             x='evento',
             y='media_diaria',
             title="<span style='font-size:24px; font-weight: 600;'>Média de chamados do subtipo \"Perturbação do Sossego\" abertos por dia em grandes eventos</span>", 
             labels={'evento': 'Evento', 'media_diaria': 'Média de Chamados por Dia'},
             color='categoria',
             color_discrete_map=cores)

# Ajustes do tooltip
fig7_1.update_traces(
    customdata=x2,  # Passando os valores personalizados
    hovertemplate='<b>Evento:</b> %{customdata}<br>' +
                  '<b>Média de Chamados por Dia:</b> %{y:.2f}<br>' +
                  '<extra></extra>'
)

fig7_1.update_layout(
    height=600,
    margin={'t': 50, 'b': 50, 'l': 50, 'r': 50},
    xaxis=dict(
        showgrid=True,
        tickmode='array',  # Permite definir os valores e rótulos do eixo X
        tickvals=df7['evento'],  # As labels dos eventos
        ticktext=[evento.replace('*', '<br>') for evento in df7['evento']],  # Quebra de linha entre as palavras do evento
        tickfont=dict(size=14)
    ),
    yaxis=dict(showgrid=True),
    autosize=True,
    legend=dict(
        font=dict(
            size=18
        )
    )
)

st.plotly_chart(fig7_1, use_container_width=False)

df8 = pd.read_csv('csvs/analise_python/7.2_chamados_subtipo_perturb_sossego_dias_de_evento.csv')

# Garantir que 'data_abertura' está no formato datetime
df8['data_abertura'] = pd.to_datetime(df8['data_abertura'])

# Agrupar por 'evento' e 'data_abertura' e contar os chamados
tabela_resumo = df8.groupby(['evento_id', 'evento', 'data_abertura']).size().reset_index(name='quantidade_chamados')

# Agrupar por 'evento' e 'data_abertura' e contar os chamados
# df8_1 = tabela_resumo.drop('evento_id', axis=1)
# Agrupar por 'evento' e calcular a média de 'quantidade_chamados' por evento
df8_1 = tabela_resumo.groupby('evento')['quantidade_chamados'].mean().reset_index(name='media_diaria_chamados')

fig8 = px.bar(df8_1, 
             x='evento',
             y='media_diaria_chamados',
             title="<span style='font-size:24px; font-weight: 600;'>Média de chamados do subtipo \"Perturbação do Sossego\" abertos por dia<br></span>"
                "<span style='font-size:24px; font-weight: 600;'>em grandes eventos por categoria de evento<br></span>"
                "<span style='font-size:16px; font-weight:normal;'>(entre os dias que tiveram algum chamado do subtipo)</span>",
             labels={'evento': 'Evento', 'media_diaria_chamados': '>Média de Chamados por Dia'},
             color='evento',
             color_discrete_map=cores)

# Ajustes do tooltip
fig8.update_traces(
    hovertemplate='<b>Categoria de Evento:</b> %{x}<br>' +
                  '<b>Média de Chamados por Dia:</b> %{y:.2f}<br>' +
                  '<extra></extra>'
)

fig8.update_layout(
    height=600,
    width=800,
    margin={'t': 150, 'b': 50, 'l': 50, 'r': 50},
    xaxis=dict(
        showgrid=True,
        tickmode='array',  # Permite definir os valores e rótulos do eixo X
        tickvals=df8_1['evento'],  # As labels dos eventos
        ticktext=[evento.replace('*', '<br>') for evento in df8_1['evento']],  # Quebra de linha entre as palavras do evento
        tickfont=dict(size=14)
    ),
    yaxis=dict(showgrid=True),
    autosize=True,
    legend=dict(
        font=dict(
            size=18
        )
    )
)

st.plotly_chart(fig8, use_container_width=False)

st.markdown(
    f"""
    <hr style="border: 2px solid {cor_divisorias}; margin: 40px 0;">
    """, 
    unsafe_allow_html=True
)

st.header("Parte 2: Dados de integração com APIs: Feriados e Tempo")
st.write("---")
st.subheader("Capítulo 2.1: Feriados de 2024")

df9 = pd.read_csv('csvs/visualizacoes/feriados_por_mes.csv')

fig9 = px.bar(df9, 
             x='Mês',
             y='Feriados',
             title="<span style='font-size:24px; font-weight: 600;'>Quantidade de feriados por mês no ano de 2024 no Brasil</span>", 
             labels={'Mês': 'Mês', 'Feriados': 'Feriados'},
             color='Mês',
             color_discrete_sequence=["#5c7aa3"],
             text='Feriados')

# Ajustes para aumentar o tamanho dos valores e movê-los para baixo
fig9.update_traces(
    textfont=dict(size=22),  
    textposition='inside',  
    insidetextanchor='end',
    hovertemplate='<b>Mês:</b> %{x}<br>' +
                  '<b>Feriados:</b> %{y}<br>' +
                  '<extra></extra>'
)

fig9.update_layout(
    height=600,
    margin={'t': 50, 'b': 50, 'l': 50, 'r': 50},
    xaxis=dict(
        showgrid=True,
        tickmode='array',  # Permite definir os valores e rótulos do eixo X
        tickvals=df9['Mês'],  # As labels dos meses
        tickfont=dict(size=18)
    ),
    yaxis=dict(showgrid=True),
    autosize=True,
    showlegend=False
)

st.plotly_chart(fig9, use_container_width=False)

st.write("---")

st.subheader("Capítulo 2.2: Clima")

df9 = pd.read_csv('csvs/analise_api/4.2_temperaturas_diarias.csv')

# Convertendo a coluna 'data' para o tipo datetime
df9['Dia'] = pd.to_datetime(df9['Dia'])

fig9 = px.bar(df9,
             x='Dia',
             y='Temperatura Média',
             title="<span style='font-size:24px; font-weight: 600;'>Temperaturas médias diárias entre 01/01/2024 e 01/08/2024 no Rio de Janeiro</span>", 
             labels={'Dia': 'Dia', 'Temperatura Média': 'Temperatura Média'},
             color='Temperatura Média', 
             color_continuous_scale=calor)

# Ajustes para aumentar o tamanho dos valores e movê-los para baixo
fig9.update_traces(
    textfont=dict(size=22),
    textposition='inside',
    insidetextanchor='end',
    hovertemplate='<b>Dia:</b> %{x}<br>' +
                  '<b>Temperatura Média:</b> %{y:.2f}°C<br>' +
                  '<extra></extra>'
)

fig9.update_layout(
    height=600,
    margin={'t': 50, 'b': 50, 'l': 50, 'r': 50},
    xaxis=dict(
        showgrid=True,
        tickmode='array',  # Permite definir os valores e rótulos do eixo X
        tickfont=dict(size=18)
    ),
    yaxis=dict(showgrid=True),
    autosize=True,
    showlegend=False
)

st.plotly_chart(fig9, use_container_width=False)

df10 = pd.read_csv('csvs/visualizacoes/temperaturas_mensais.csv')

fig10 = px.bar(df10,
             x='Mês',
             y='Temperatura Média',
             title="<span style='font-size:24px; font-weight: 600;'>Temperaturas médias mensais entre 01/01/2024 e 01/08/2024 no Rio de Janeiro</span>", 
             labels={'Mês': 'Mês', 'Temperatura Média': 'Temperatura Média'},
             color='Temperatura Média', 
             color_continuous_scale=calor,
             text=df10['Temperatura Média'].apply(lambda x: f"{x:.2f}°C")) # Formatar os rótulos dentro das barras

# Ajustes para aumentar o tamanho dos valores
fig10.update_traces(
    textfont=dict(size=22),
    textposition='inside',
    insidetextanchor='end',
    hovertemplate='<b>Mês:</b> %{x}<br>' +
                  '<b>Temperatura Média:</b> %{y:.2f}°C<br>' +
                  '<extra></extra>'
)

fig10.update_layout(
    height=600,
    margin={'t': 50, 'b': 50, 'l': 50, 'r': 50},
    xaxis=dict(
        showgrid=True,
        tickmode='array',  # Permite definir os valores e rótulos do eixo X
        tickvals=df10['Mês'],  # As labels dos meses
        tickfont=dict(size=18)
    ),
    yaxis=dict(showgrid=True),
    autosize=True,
    showlegend=False
)

st.plotly_chart(fig10, use_container_width=False)

st.markdown("""
    <p style="font-size: 18px;">
        <strong>Obs:</strong> como foi especificado que só deveriam ser extraídos os dados de um dia de Agosto (o dia 1º), o mês não foi considerado nas análises mensais de clima,
        pois as informações estariam gravemente incompletas, e a comparação com os outros meses seria irreal.
    </p>
""", unsafe_allow_html=True)

st.write("---")

df11 = pd.read_csv('csvs/analise_api/5_clima_mensal.csv')