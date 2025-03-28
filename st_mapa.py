import pandas as pd
import geojson
import sys
import csv
sys.path.append('../..')
import folium
print (folium.__file__)
print (folium.__version__)
import streamlit as st
from streamlit_folium import folium_static
import branca

def ajeita_geojson(data_geojson, coluna_cat):
    for feature in data_geojson['features']:
        while feature['properties'][coluna_cat][-1] == " ":
            feature['properties'][coluna_cat] = feature['properties'][coluna_cat][:-1]
    return data_geojson

def fator_mapa(valor, minimo, maximo, lim_inf, lim_sup):
    # Retorna o ponto médio se não houver variação
    if maximo == minimo:
        return (lim_sup + lim_inf) / 2

    # Normaliza o valor para o intervalo [0,1]
    normalizado = (valor - minimo) / (maximo - minimo)
    
    # Escala para o novo intervalo [lim_inf, lim_sup]
    return lim_inf + normalizado * (lim_sup - lim_inf)

def escolhe_cor(fator_mapa, paleta):
    n = len(paleta)  # Número de cores disponíveis

    # Garante que fator_mapa esteja dentro do intervalo [0.5, 1]
    fator_mapa = max(0.5, min(1, fator_mapa))

    # Mapeia fator_mapa para um índice de cor
    indice = int((fator_mapa - 0.5) / 0.5 * (n - 1))

    return paleta[indice]

def cores(df, feature, paleta, coluna_cat):
    if isinstance(paleta, str):
        return paleta
    df_indexed = df.set_index(coluna_cat)
    # st.write(feature)
    regiao_name = feature['properties'][coluna_cat]
    if regiao_name in list(df_indexed.index):
        fator_mapa = df_indexed.loc[regiao_name, 'Fator Mapa']
        # st.write(fator_mapa)
        if fator_mapa == 0:
            return '#ffffff'
        else:
            cor = branca.colormap.LinearColormap(colors=paleta, vmin=0.5, vmax=1)(fator_mapa)
            return cor
    else:
        # print(regiao_name)
        return 'Black'

def display_map(df, data_geo_json, paleta, coluna_cat, coluna_valor, nome_coluna_valor):
    m = folium.Map(location=[-22.91798994895881, -43.42464638599411], zoom_start=11, scrollWheelZoom=False, tiles='CartoDB positron')

    camada = folium.GeoJson(
        data_geo_json,
        style_function=lambda feature: {
            'fillColor': cores(df, feature, paleta, coluna_cat),
            'color' : 'black',
            'weight' : 1,
            'fillOpacity' : 0.72,
            # 'dashArray' : '5, 5'
            }
        ).add_to(m)

    df_indexed = df.set_index(coluna_cat)
    for feature in camada.data['features']:
        regiao_name = feature['properties'][coluna_cat]
        if regiao_name in list(df_indexed.index):
            feature['properties']['chamados'] = f'{nome_coluna_valor}: ' + '{:,}'.format(df_indexed.loc[regiao_name, coluna_valor])
        else:
            feature['properties']['chamados'] = ''

    camada.add_child(
        folium.features.GeoJsonTooltip([coluna_cat, 'chamados'], labels=False),
    )

    # Adiciona legenda
    # macro = legenda_estatica.legenda(quant_results)
    # m.get_root().add_child(macro)

    st_map = folium_static(m, width=1920, height=600)
    
    return

def mostra_mapa(df, paleta, coluna_cat, coluna_valor, nome_coluna_valor, arquivo_geojson):
    # Abre arquivo GeoJSON
    with open(arquivo_geojson, 'r', encoding='utf-8') as file:
        data_geojson = geojson.load(file)

    maximo = df[coluna_valor].max()
    minimo = df[coluna_valor].min()

    # Cria o fator mapa, uma normalização entre 0.5 e 1 do valor medido no mapa para facilitar a coloração
    df["Fator Mapa"] = df[coluna_valor].apply(lambda x: fator_mapa(x, minimo, maximo, 0.5, 1))

    # Ajeita o geoJSON para que os nomes das regiões não tenham espaços no final
    data_geojson = ajeita_geojson(data_geojson, coluna_cat)

    # Cria e mostra o mapa
    display_map(df, data_geojson, paleta, coluna_cat, coluna_valor, nome_coluna_valor)

# Teste
if __name__ == "__main__":
    st.write("Banana")

    data = {
        "Bairro" : ["Leblon", "Tijuca", "Botafogo", "Bangu", "Campo Grande"],
        "Chamados Totais" : [23, 27, 50, 8, 42]
    }

    df_teste = pd.DataFrame(data)

    mostra_mapa(df_teste)