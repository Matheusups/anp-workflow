import requests
from io import StringIO
import polars as pl
import time

#Lista de dataframes
frame_list = []

# Dados de Diesel-GNV
url_diesel_gnv = 'https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/qus/ultimas-4-semanas-diesel-gnv.csv'

# Dados de Etanol-Gasolina
url_etanol_gasolina = 'https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/qus/ultimas-4-semanas-gasolina-etanol.csv'

# Dados de GLP
url_glp = 'https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/qus/ultimas-4-semanas-glp.csv'

# Fazendo uma solicitação GET para obter o conteúdo do arquivo
response_gnv = requests.get(url_diesel_gnv)
response_gasol = requests.get(url_etanol_gasolina)
response_glp = requests.get(url_glp)

# Armazenamento dos dados em dataframe caso a requisição retorne 200
if response_gnv.status_code == 200:
    file_gnv = response_gnv.content
    df_gnv = pl.read_csv(file_gnv,separator=';')
    frame_list.append(df_gnv)

if response_gasol.status_code == 200:
    file_gasol = response_gasol.content
    df_gasol = pl.read_csv(file_gasol,separator=';')
    frame_list.append(df_gasol)

if response_glp.status_code == 200:
    file_glp = response_glp.content
    df_glp = pl.read_csv(file_glp,separator=';')
    frame_list.append(df_glp)

# Unificação dos dataframes
# Gravação do arquivo no diretório do ambiente
df_consolidado = pl.concat(frame_list)
df_consolidado.write_csv('./dados/dados_consolidados_combustivel.csv')
