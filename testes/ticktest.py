import pandas as pd

df7 = pd.read_csv('csvs/visualizacoes/chamados_eventos.csv')

ticktext=[evento.replace('*', '<br>') for evento in df7['evento']]

x2=[evento.replace('*', ' ') for evento in df7['evento']]

print(df7)
print()
print(ticktext)
print()
print(x2)