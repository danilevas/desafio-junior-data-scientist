import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Dashboard Daniel Levacov", page_icon=":brain:", layout="wide")

st.title("Visualizações Daniel Levacov")

st.header("Parte 1: Dados sobre os chamados do 1746")
st.subheader("Capítulo 1.1: Dados sobre os chamados no dia 01/04/2023")

# Carregar os dados do CSV 
df1 = pd.read_csv('csvs/analise_sql/2_chamados_por_tipo_01_04_2023.csv')

# Invertendo a ordem dos dados
df1 = df1.sort_values(by='chamados_totais', ascending=True).tail(10)

fig1 = px.bar(df1, 
             y='tipo', 
             x='chamados_totais', 
             title="Tipos de chamado mais abertos no dia 01/04/2023", 
             labels={'tipo': 'Tipo de Chamado', 'chamados_totais': 'Chamados Totais'},
             color='chamados_totais', 
             color_continuous_scale='Viridis', 
             orientation='h')

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

# Invertendo a ordem dos dados
df2 = df2.sort_values(by='chamados_totais', ascending=True).tail(10)

fig2 = px.bar(df2, 
             y='nome', 
             x='chamados_totais', 
             title="Bairros com mais chamados abertos no dia 01/04/2023", 
             labels={'nome': 'Bairro', 'chamados_totais': 'Chamados Totais'},
             color='chamados_totais', 
             color_continuous_scale='Viridis', 
             orientation='h')

fig2.update_layout(
    height=600,
    width=800,
    margin={'t': 50, 'b': 50, 'l': 50, 'r': 50},
    xaxis=dict(showgrid=True),
    yaxis=dict(showgrid=True),
    autosize=True,
)

c1, c2 = st.columns(2)
with c1:
    st.plotly_chart(fig1, use_container_width=False)
with c2:
    st.plotly_chart(fig2, use_container_width=False)

df3 = pd.read_csv('csvs/analise_sql/4_chamados_por_subprefeitura_01_04_2023.csv')

# Invertendo a ordem dos dados
df3 = df3.sort_values(by='chamados_totais', ascending=True).tail(10)

fig3 = px.bar(df3, 
             y='subprefeitura', 
             x='chamados_totais',
             title="Subprefeituras com mais chamados abertos no dia 01/04/2023", 
             labels={'subprefeitura': 'Subprefeitura', 'chamados_totais': 'Chamados Totais'},
             color='chamados_totais', 
             color_continuous_scale='Viridis', 
             orientation='h')

fig3.update_layout(
    height=600,
    width=800,
    margin={'t': 50, 'b': 50, 'l': 50, 'r': 50},
    xaxis=dict(showgrid=True),
    yaxis=dict(showgrid=True),
    autosize=True,
)

st.plotly_chart(fig3, use_container_width=False)

st.write("---")
st.subheader("Capítulo 1.2: Perturbação do Sossego: Tipo vs Subtipo")

df4 = pd.read_csv('csvs/analise_sql/6.2_chamados_subtipo_perturb_sossego_por_data.csv')

# Convertendo a coluna 'data' para o tipo datetime
df4['data'] = pd.to_datetime(df4['data'])

# Agregando os dados por mês
df_mensal = df4.groupby(pd.Grouper(key='data', freq='ME')).agg({'total_chamados': 'sum'}).reset_index()

fig4 = px.bar(df_mensal, 
             x='data',
             y='total_chamados',
             title="Quantidade de chamados do subtipo \"Perturbação do Sossego\" abertos por mês", 
             labels={'data': 'Mês', 'total_chamados': 'Chamados Totais'},
             color='total_chamados', 
             color_continuous_scale='Viridis')

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

df5 = pd.read_csv('csvs/analise_sql/6.5_chamados_tipo_perturb_sossego_por_data.csv')

# Convertendo a coluna 'data' para o tipo datetime
df5['data'] = pd.to_datetime(df5['data'])

# Agregando os dados por mês
df_mensal = df5.groupby(pd.Grouper(key='data', freq='ME')).agg({'total_chamados': 'sum'}).reset_index()

fig5 = px.bar(df_mensal, 
             x='data',
             y='total_chamados',
             title="Quantidade de chamados do tipo \"Perturbação do Sossego\" abertos por mês", 
             labels={'data': 'Mês', 'total_chamados': 'Chamados Totais'},
             color='total_chamados', 
             color_continuous_scale='Viridis')

fig5.update_layout(
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

st.plotly_chart(fig5, use_container_width=False)

st.write(f"Aqui percebemos a diferença clara entre a utilização do subtipo e do tipo \"Perturbação do Sossego\"."
         f" Por algum motivo, o subtipo \"Perturbação do Sossego\" era pouquíssimo utilizado antes de 2020, passou a ser utilizado extensivamente em 2020 e depois"
         f" caiu em desuso, sendo usado novamente apenas ligeiramente em Março de 2024.\n\n"
         f"Enquanto isso, o tipo \"Perturbação do Sossego\" só passou a ser usado a partir de 2021, e desde então tem sido usado extensivamente,"
         f" com seu uso diminuindo apenas no período entre Janeiro e Setembro de 2024.")

st.write("---")
st.subheader("Capítulo 1.3: Dados sobre os chamados entre 01/01/2022 e 31/12/2023")

df6 = pd.read_csv('csvs/analise_sql/6.5_chamados_tipo_perturb_sossego_por_data.csv')

# Convertendo a coluna 'data' para o tipo datetime
df6['data'] = pd.to_datetime(df6['data'])

# Recortando o período que queremos
df6 = df6[(df6['data'].dt.date.between(pd.to_datetime('2022-01-01').date(), pd.to_datetime('2023-12-31').date()))]

fig6 = px.bar(df6, 
             x='data',
             y='total_chamados',
             title="Quantidade de chamados do tipo \"Perturbação do Sossego\" abertos por dia em 2022 e 2023", 
             labels={'data': 'Dia', 'total_chamados': 'Chamados Totais'},
             color='total_chamados', 
             color_continuous_scale='Viridis')

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
             title="Quantidade de chamados do tipo \"Perturbação do Sossego\" abertos em grandes eventos", 
             labels={'evento': 'Evento', 'total_chamados': 'Chamados Totais'},
             color='tipo',
             color_discrete_map=cores)

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
             title="Média de chamados do tipo \"Perturbação do Sossego\" abertos por dia em grandes eventos", 
             labels={'evento': 'Evento', 'media_diaria': 'Chamados Totais'},
             color='tipo',
             color_discrete_map=cores)

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

df8 = pd.read_csv('csvs/analise_python/7.2_chamados_tipo_perturb_sossego_dias_de_evento.csv')

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
             title="Média de chamados do tipo \"Perturbação do Sossego\" abertos por dia<br>em grandes eventos por categoria de evento", 
             labels={'evento': 'Evento', 'media_diaria_chamados': 'Chamados Totais'},
             color='evento',
             color_discrete_map=cores)

fig8.update_layout(
    height=600,
    width=600,
    margin={'t': 50, 'b': 50, 'l': 50, 'r': 50},
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

st.write("---")

st.header("Parte 2: Dados de integração com APIs: Feriados e Tempo")
st.subheader("Capítulo 2.1: Feriados de 2024")

df9 = pd.read_csv('csvs/visualizacoes/feriados_por_mes.csv')

fig9 = px.bar(df9, 
             x='Mês',
             y='Feriados',
             title="Quantidade de feriados por mês no ano de 2024 no Brasil", 
             labels={'Mês': 'Mês', 'Feriados': 'Feriados'},
             color='Mês',
             color_discrete_sequence=["#5c7aa3"],
             text='Feriados')  # Adiciona os valores em cima das barras

# Ajustes para aumentar o tamanho dos valores e movê-los para baixo
fig9.update_traces(
    textfont=dict(size=22),  
    textposition='inside',  
    insidetextanchor='end'  
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

df9 = pd.read_csv('csvs/analise_api/temperaturas_diarias.csv')

# Convertendo a coluna 'data' para o tipo datetime
df9['Dia'] = pd.to_datetime(df9['Dia'])

fig9 = px.bar(df9,
             x='Dia',
             y='Temperatura Média',
             title="Temperaturas médias diárias entre 01/01/2024 e 01/08/2024 no Rio de Janeiro", 
             labels={'Dia': 'Dia', 'Temperatura Média': 'Temperatura Média'},
             color='Temperatura Média', 
             color_continuous_scale=["#264653", "#2a9d8f", "#e9c46a", "#f4a261", "#e76f51", "#e63946"])  # Adiciona os valores em cima das barras

# Ajustes para aumentar o tamanho dos valores e movê-los para baixo
fig9.update_traces(
    textfont=dict(size=22),
    textposition='inside',
    insidetextanchor='end'
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
             title="Temperaturas médias mensais entre 01/01/2024 e 01/08/2024 no Rio de Janeiro", 
             labels={'Mês': 'Mês', 'Temperatura Média': 'Temperatura Média'},
             color='Temperatura Média', 
             color_continuous_scale=["#264653", "#2a9d8f", "#e9c46a", "#f4a261", "#e76f51", "#e63946"])  # Adiciona os valores em cima das barras

# Ajustes para aumentar o tamanho dos valores
fig10.update_traces(
    textfont=dict(size=22),
    textposition='inside',
    insidetextanchor='end'
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

df11 = pd.read_csv('csvs/analise_api/clima_mensal.csv')