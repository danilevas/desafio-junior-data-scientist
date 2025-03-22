import pandas as pd

def weather_code_pra_descricao(wc):
    # Carregar o JSON em um DataFrame
    df_codigos = pd.read_json('jsons/descriptions.json')

    descricao_dia = df_codigos[wc]['day']['description']
    descricao_noite = df_codigos[wc]['night']['description']
    if descricao_dia == descricao_noite:
        return descricao_dia
    else:
        return f"{df_codigos[wc]['day']['description']}/{df_codigos[wc]['night']['description']}"

print(weather_code_pra_descricao(0))
print(weather_code_pra_descricao(1))
print(weather_code_pra_descricao(2))
print(weather_code_pra_descricao(3))
print(weather_code_pra_descricao(45))