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

    # Descobrir o dia da semana (0 = Segunda, 6 = Domingo)
    return data.weekday()

response = requests.get('https://date.nager.at/api/v3/publicholidays/2024/BR')
public_holidays = json.loads(response.content)

# Teste
for feriado in public_holidays:
    print(feriado['date'])

# Q1.
print(f"Q1. Há {len(public_holidays)} feriados no Brasil em 2024")

# Q2.
meses = [f"{m:02d}" for m in range(1, 13)]
feriados_por_mes = {}
for feriado in public_holidays:
    mes = extrai_mes(feriado['date'])
    if mes not in feriados_por_mes.keys():
        feriados_por_mes[mes] = 1
    else:
        feriados_por_mes[mes] += 1

print(f"Q2. O mês com mais feriados no Brasil em 2024 é o mês {max(feriados_por_mes, key=feriados_por_mes.get)}")

# Q3.
feriados_em_dias_de_semana = 0
for feriado in public_holidays:
    dia_semana = extrai_dia_semana(feriado['date'])
    if dia_semana < 5:
        # É dia de semana
        feriados_em_dias_de_semana += 1

print(f"Q3. Há {feriados_em_dias_de_semana} feriados no Brasil em 2024 que caem em dias de semana.")

# Q4.

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
        "cell_selection": "nearest"  # Está me jogando para Maria da Graça
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"\nCoordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()}{response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

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
    # print(hourly_dataframe.tail(48))

    # Converter a coluna de datas para o Horário de Brasília (GMT-3)
    hourly_dataframe["date"] = hourly_dataframe["date"].dt.tz_convert("America/Sao_Paulo")
    hourly_dataframe.to_csv("csvs/analise_api/temperaturas_hora_em_hora.csv", encoding="utf-8", index=False)

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

    # print(df_media_temp_diaria.tail(32).head(31))
    # print(df_media_temp_diaria.tail(32).head(31)["Temperatura Média"].mean()) teste julho

    df_media_temp_diaria.to_csv("csvs/analise_api/temperaturas_diarias.csv", encoding="utf-8", index=False)
    return df_media_temp_diaria

def media_mensal_temperatura():
    df = pd.read_csv("csvs/analise_api/temperaturas_diarias.csv", parse_dates=["Dia"])

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
    df_media_temp_mensal = df_media_temp_mensal[["Mês", "Temperatura Média"]]

    # Salvar em um novo CSV
    df_media_temp_mensal.to_csv("csvs/analise_api/temperaturas_mensais.csv", index=False)

    return df_media_temp_mensal

hourly_dataframe = get_temperatura_hora_em_hora(-22.91, -43.22, "2024-01-01", "2024-08-01")
df_media_temp_diaria = media_diaria_temperatura(hourly_dataframe)
df_media_temp_mensal = media_mensal_temperatura()

# Q5.

def weather_code_pra_descricao(wc):
    