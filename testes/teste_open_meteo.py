import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

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
        "latitude": -22.91,
        "longitude": -43.22,
        "start_date": "2024-01-01",
        "end_date": "2024-08-01",
        "hourly": "temperature_2m",
        "temperature_unit": "celsius",
        "timezone": "America/Sao_Paulo",
        "cell_selection": "nearest"  # Está me jogando para Maria da Graça
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()}{response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process hourly data
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        ),
        "temperature_2m": hourly_temperature_2m
    }

    hourly_dataframe = pd.DataFrame(data=hourly_data)
    # print(hourly_dataframe.tail(48))

    # Converter a coluna de datas para o Horário de Brasília (GMT-3)
    hourly_dataframe["date"] = hourly_dataframe["date"].dt.tz_convert("America/Sao_Paulo")

    return hourly_dataframe

# Calcular as médias diárias da temperatura
def media_diaria_temperatura(hourly_dataframe):
    daily_temperature = (
        hourly_dataframe
        .groupby(hourly_dataframe["date"].dt.date)["temperature_2m"]
        .mean()
        .reset_index()
        .rename(columns={"date": "Dia", "temperature_2m": "Temperatura Média"})
    )

    # print(daily_temperature.tail(32).head(31))
    # print(daily_temperature.tail(32).head(31)["Temperatura Média"].mean()) teste julho

    daily_temperature.to_csv("csvs/analise_api/temperaturas_diarias.csv", encoding="utf-8", index=False)
    return daily_temperature

def media_mensal_temperatura():
    df = pd.read_csv("csvs/analise_api/temperaturas_diarias.csv", parse_dates=["Dia"])

    # Agrupar por mês e calcular a média mensal
    df_mensal = df.resample("ME", on="Dia").agg({"Temperatura Média": "mean"}).reset_index()

    # Criar a coluna "Mês" com o formato Mês/Ano
    df_mensal["Mês"] = df_mensal["Dia"].dt.strftime('%m/%Y')

    # Eliminar a coluna "Dia"
    df_mensal = df_mensal.drop(columns=["Dia"])

    # Reordenar as colunas
    df_mensal = df_mensal[["Mês", "Temperatura Média"]]

    # Salvar em um novo CSV
    df_mensal.to_csv("temperaturas_mensais.csv", index=False)

    return df_mensal