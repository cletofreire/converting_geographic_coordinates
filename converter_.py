# -*- coding: utf-8 -*-
"""Converter_.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FnpjmMNrwADAPHllWR1F2NoSfYnl1TI8

TUTORIAL PARA CONVERTER ESCALAS
"""

import pandas as pd

!pip install dms2dec -q

from dms2dec.dms_convert import dms2dec

dados = pd.read_excel('https://raw.githubusercontent.com/cletofreire/converting_geographic_coordinates/main/data_convert.xlsx',header=0)
dados2 = pd.read_excel('https://raw.githubusercontent.com/cletofreire/converting_geographic_coordinates/main/data_convert.xlsx',header=0)

dados.info()

#criando um id
dados.reset_index(inplace = True)
dados = dados.rename(columns ={'index':'id'})

# id para os dados2
dados2.reset_index(inplace = True)
dados2 = dados.rename(columns ={'index':'id'})

#Observando se há vazio
print(dados.isnull().sum())

#Observando as linhas que possuem dados vazios
linhas_vazias = dados[dados.isnull().any(axis=1)]
print(linhas_vazias)

dados2.info()

#Selecionando apenas os dados que estão em grau_minuto_segundo
#Latitude
dados['Latitude_GMS'] = dados['Latitude'].astype(str)
dados= dados[dados['Latitude_GMS'].str.contains("[°'\"']", regex=True)]

#Longitude
dados['Longitude_GMS'] = dados['Longitude'].astype(str)
dados= dados[dados['Longitude_GMS'].str.contains("[°'\"']", regex=True)]

# Criei uma função onde substitui os valores desejados para ficar no formato limpo
def remover_os_simbolos(remover):
    return remover.replace('°', ' ').replace ('\'', ' ').replace('\"', ' ')

dados['Latitude_GMS'] = dados['Latitude_GMS'].apply(remover_os_simbolos)
dados['Longitude_GMS'] = dados['Longitude_GMS'].apply(remover_os_simbolos)

# convertendo para Graus_decimaism
dados['Latitude_GD'] = dados['Latitude_GMS'].apply(dms2dec)
dados['Longitude_GD'] = dados['Longitude_GMS'].apply(dms2dec)

dados.head(3)

def adicionar_sinal(valor):
    if valor < 0:
        return valor
    else:
        return '-' + str(valor)

# aplicar a função lambda para adicionar um sinal de menos na frente de todos os valores em 'Latitude_GD' e 'Longitude_GD' que não possuem um sinal de menos
dados['Latitude_GD'] = dados['Latitude_GD'].apply(lambda x: adicionar_sinal(x))
dados['Longitude_GD'] = dados['Longitude_GD'].apply(lambda x: adicionar_sinal(x))

dados.head(3)

# Unindo os dois dataframes usando a coluna 'id' como chave e uma junção externa
dados_unidos = dados2.merge(dados, on='id', how='outer')

# Preenchendo os valores faltantes de Latitude_GD com os valores correspondentes de Latitude
dados_unidos['Latitude_GD'] = dados_unidos['Latitude_GD'].fillna(dados_unidos['Latitude_x'])

# Preenchendo os valores faltantes de Longitude_GD com os valores correspondentes de Longitude
dados_unidos['Longitude_GD'] = dados_unidos['Longitude_GD'].fillna(dados_unidos['Longitude_x'])

# Descartando as colunas 'Latitude' e 'Longitude' se desejado
dados_unidos = dados_unidos.drop(['Latitude_x', 'Longitude_x'], axis=1)

# Mostrando o dataframe unido
dados_unidos.info()

dados_unidos.head()

# Save
dados_unidos.to_excel('dados_convertidos.xlsx', index=False)