import json
import requests
import datetime
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

def extrai_mes(data):
    return data[5:7]

def extrai_dia_semana(data):
    # Definir a data desejada (ano, mês, dia)
    data = datetime.date(int(data[0:4]), int(data[5:7]), int(data[8:10]))

    # Retorna o dia da semana (0 = Segunda, 6 = Domingo)
    return data.weekday()

# Cria o arquivo txt com as respostas
with open('respostas_analise_api.md', 'w', encoding="utf-8") as f: 
    f.write("# Respostas das Questões sobre Integração com APIs: Feriados e Tempo\n\n")

response = requests.get('https://date.nager.at/api/v3/publicholidays/2024/BR')
public_holidays = json.loads(response.content)

# Q1.
with open('respostas_analise_api.md', 'a', encoding="utf-8") as f: 
    f.write(f"**Resposta Questão 1:** Há {len(public_holidays)} feriados no Brasil em 2024\n\n")

# Q2.
meses = [f"{m:02d}" for m in range(1, 13)]
feriados_por_mes = {}
for feriado in public_holidays:
    mes = extrai_mes(feriado['date'])
    if mes not in feriados_por_mes.keys():
        feriados_por_mes[mes] = 1
    else:
        feriados_por_mes[mes] += 1

with open('respostas_analise_api.md', 'a', encoding="utf-8") as f: 
    f.write(f"**Resposta Questão 2:** O mês com mais feriados no Brasil em 2024 é o mês {max(feriados_por_mes, key=feriados_por_mes.get)}\n\n")

# Q3.
feriados_em_dias_de_semana = 0
for feriado in public_holidays:
    dia_semana = extrai_dia_semana(feriado['date'])
    if dia_semana < 5:
        # É dia de semana
        feriados_em_dias_de_semana += 1

with open('respostas_analise_api.md', 'a', encoding="utf-8") as f: 
    f.write(f"**Resposta Questão 3:** Há {feriados_em_dias_de_semana} feriados no Brasil em 2024 que caem em dias de semana.\n\n")

# Q4.

# Aqui eu decidi não analisar o mês de Agosto quando fizer análises mensais, pois como extraímos dados apenas do dia 1º desse mês,
# as informações estariam gravemente incompletas, e a comparação com os outros meses seria irreal.

def get_temperatura_hora_em_hora(lat, long, data_inicio, data_fim):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Vou pegar dados de hora em hora, porque com o parâmetro "daily", a API só nos retorna a temperatura mínima e máxima de cada dia,
    # e fazer uma média entre essas 2 seria bem menos preciso do que fazer uma média das temperaturas nas 24 horas do dia.

    # API request parameters
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": long,
        "start_date": data_inicio,
        "end_date": data_fim,
        "hourly": "temperature_2m,weather_code",
        "temperature_unit": "celsius",
        "timezone": "America/Sao_Paulo",
        "cell_selection": "nearest"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Esse cell_selection está me jogando para Maria da Graça, foi o lugar que eu consegui no Rio.
    # Quando eu botava um ponto no Centro ele me jogava para Niterói, pelo jeito que o grid dessa API funciona.
    # Então, eu pensei, se não dá para colocar no Centro, que é o coração do Rio, vou tentar o ponto mais próximo, que foi esse.

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    with open('respostas_analise_api.md', 'a', encoding="utf-8") as f:
        f.write(f"Parâmetros do uso da Open-Meteo Historical Weather API:\n")
        f.write(f"* Coordenadas: {response.Latitude()}°N {response.Longitude()}°E\n")
        f.write(f"* Elevação: {response.Elevation()} m asl\n")
        f.write(f"* Fuso horário: {response.Timezone()}{response.TimezoneAbbreviation()}\n\n")

    # Process hourly data
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy() # temperatura a 2m do chão
    hourly_weather_code = hourly.Variables(1).ValuesAsNumpy() # weather_code

    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        ),
        "temperature_2m": hourly_temperature_2m,
        "weather_code": hourly_weather_code
    }

    hourly_dataframe = pd.DataFrame(data=hourly_data)

    # Converter a coluna de datas para o Horário de Brasília (GMT-3)
    hourly_dataframe["date"] = hourly_dataframe["date"].dt.tz_convert("America/Sao_Paulo")

    # Arredondando a temperatura para 2 casas decimais
    hourly_dataframe["temperature_2m"] = round(hourly_dataframe["temperature_2m"], 2)

    # Salvando em um CSV
    hourly_dataframe.to_csv("csvs/analise_api/4.1_temperaturas_hora_em_hora.csv", encoding="utf-8", index=False)

    return hourly_dataframe

# Calcular as médias diárias da temperatura
def media_diaria_temperatura(hourly_dataframe):
    df_media_temp_diaria = (
        hourly_dataframe.groupby(hourly_dataframe["date"].dt.date).agg({
            "temperature_2m": "mean",  # Média da Temperatura
            "weather_code": lambda x: x.mode()[0]  # Moda do weather_code (pega o mais frequente)
        })
        .reset_index()
        .rename(columns={"date": "Dia", "temperature_2m": "Temperatura Média"})
    )

    # Arredondando a temperatura para 2 casas decimais
    df_media_temp_diaria["Temperatura Média"] = round(df_media_temp_diaria["Temperatura Média"], 2)

    # Salvando em um CSV
    df_media_temp_diaria.to_csv("csvs/analise_api/4.2_temperaturas_diarias.csv", encoding="utf-8", index=False)
    return df_media_temp_diaria

def media_mensal_temperatura():
    df = pd.read_csv("csvs/analise_api/4.2_temperaturas_diarias.csv", parse_dates=["Dia"])

    # Agrupar por mês e calcular a média mensal
    df_media_temp_mensal = df.resample("ME", on="Dia").agg({
        "Temperatura Média": "mean",  # Média da Temperatura
        "weather_code": lambda x: x.mode()[0]  # Moda do weather_code (pega o mais frequente)
    }).reset_index()

    # Criar a coluna "Mês" com o formato Mês/Ano
    df_media_temp_mensal["Mês"] = df_media_temp_mensal["Dia"].dt.strftime('%m/%Y')

    # Eliminar a coluna "Dia"
    df_media_temp_mensal = df_media_temp_mensal.drop(columns=["Dia"])

    # Reordenar as colunas
    df_media_temp_mensal = df_media_temp_mensal[["Mês", "Temperatura Média", "weather_code"]]

    # Tirando Agosto, por só ter um dia
    df_media_temp_mensal = df_media_temp_mensal.iloc[:-1]

    # Arredondando a temperatura para 2 casas decimais
    df_media_temp_mensal["Temperatura Média"] = round(df_media_temp_mensal["Temperatura Média"], 2)

    # Salvar em um novo CSV
    df_media_temp_mensal.to_csv("csvs/analise_api/4.3_temperaturas_mensais.csv", index=False)

    return df_media_temp_mensal

hourly_dataframe = get_temperatura_hora_em_hora(-22.91, -43.22, "2024-01-01", "2024-08-01")
df_media_temp_diaria = media_diaria_temperatura(hourly_dataframe)
df_media_temp_mensal = media_mensal_temperatura()

with open('respostas_analise_api.md', 'a', encoding="utf-8") as f: 
    f.write(f"**Resposta Questão 4:** veja o arquivo csvs/analise_api/4.3_temperaturas_mensais.csv\n\n")

# Q5.

# Lembrar que pegamos só um dia de dados de Agosto, logo não devemos analisá-lo como mês junto com os outros meses.

def weather_code_pra_descricao(wc):
    # Carregar o JSON em um DataFrame
    df_codigos = pd.read_json('jsons/descriptions.json')

    # Pegar no JSON os dados do weather_code wc
    descricao_dia = df_codigos[wc]['day']['description']
    descricao_noite = df_codigos[wc]['night']['description']
    if descricao_dia == descricao_noite:
        return descricao_dia
    else:
        return f"{df_codigos[wc]['day']['description']}/{df_codigos[wc]['night']['description']}"

# Convertendo os weather_codes para suas descrições
df_media_temp_mensal["weather_code"] = df_media_temp_mensal["weather_code"].apply(weather_code_pra_descricao)

# Renomeando a coluna weather_code para "Tempo Predominante"
df_media_temp_mensal.rename(columns={'weather_code': 'Tempo Predominante'}, inplace=True)

df_media_temp_mensal.to_csv("csvs/analise_api/5_clima_mensal.csv", index=False)

with open('respostas_analise_api.md', 'a', encoding="utf-8") as f: 
    f.write(f"**Resposta Questão 5:** veja o arquivo csvs/analise_api/5_clima_mensal.csv\n\n")

# Q6.
clima_feriados = {
    "Feriados" : [],
    "Temperatura Média" : [],
    "Tempo" : []
}

# Pegando os dados de temperaturas diárias
df_diario = pd.read_csv("csvs/analise_api/4.2_temperaturas_diarias.csv", parse_dates=["Dia"])

# Iterando pelos feriados
for feriado in public_holidays:
    # Se for posterior a 01/08/2024, não queremos!
    if feriado['date'] > '2024-08-01':
        break
    clima_feriados["Feriados"].append(feriado['date'])
    linha_desse_dia = df_diario[df_diario.iloc[:, 0] == feriado['date']].values.tolist()[0]
    linha_desse_dia[0] = linha_desse_dia[0].date()
    clima_feriados["Temperatura Média"].append(float(linha_desse_dia[1]))
    clima_feriados["Tempo"].append(weather_code_pra_descricao(int(linha_desse_dia[2])))

# Criando DataFrame
df_clima_feriados = pd.DataFrame(clima_feriados)

# Salvando em um CSV
df_clima_feriados.to_csv("csvs/analise_api/6_clima_feriados.csv", encoding="utf-8", index=False)

with open('respostas_analise_api.md', 'a', encoding="utf-8") as f: 
    f.write(f"**Resposta Questão 6:** veja o arquivo csvs/analise_api/6_clima_feriados.csv\n\n")

# Q7.
df_feriados_nao_aprov = df_clima_feriados[(df_clima_feriados["Temperatura Média"] < 20) | (df_clima_feriados["Tempo"] == "Cloudy")]

df_feriados_nao_aprov.to_csv("csvs/analise_api/7_feriados_nao_aprov.csv", encoding="utf-8", index=False)

with open('respostas_analise_api.md', 'a', encoding="utf-8") as f: 
    f.write(f"**Resposta Questão 7:** veja o arquivo csvs/analise_api/7_feriados_nao_aprov.csv\n\n")

# Q8.
df_feriados_aprov = df_clima_feriados[(df_clima_feriados["Temperatura Média"] >= 20) & (df_clima_feriados["Tempo"] != "Cloudy")]

df_feriados_aprov.to_csv("csvs/analise_api/8_feriados_aprov.csv", encoding="utf-8", index=False)

# Os 3 feriados aproveitáveis têm o mesmo tempo (Sunny/Clear), logo vamos dizer que o mais aproveitável é o com a maior temperatura.
dia_feriado_aprov_maior_temp = df_feriados_aprov.loc[df_feriados_aprov["Temperatura Média"].idxmax(), "Feriados"]

with open('respostas_analise_api.md', 'a', encoding="utf-8") as f: 
    f.write(f"**Resposta Questão 8:** o dia de feriado mais aproveitável do ano foi {dia_feriado_aprov_maior_temp}, como visto em csvs/analise_api/8_feriados_aprov.csv")