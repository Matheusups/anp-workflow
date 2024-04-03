import requests
from io import StringIO
import polars as pl
import time
import zipfile
import glob

def extrair_zip(zip_file, path):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(path)

def get_url():
    url_site = 'https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/serie-historica-de-precos-de-combustiveis'
    response = requests.get(url_site)
    return response


def split_html():
    array_url = []
    
    get = get_url().text
    html_split = get.split('Combustíveis automotivos')[1].split('GLP P13')[0]
    html_final = html_split.split('href="')
    
    for texto in html_final:
        if texto.split('"')[0].startswith('https'):
           array_url.append(texto.split('"')[0])
    
    return array_url 


def get_array_persist():
    array = split_html()
    dataframes = []

    # Criação de lista contendo o schema do arquivo que será baixado
    headers = ['Regiao - Sigla'
               ,'Estado - Sigla'
               ,'Municipio'
               ,'Revenda'
               ,'CNPJ da Revenda'
               ,'Nome da Rua'
               ,'Numero Rua'
               ,'Complemento'
               ,'Bairro'
               ,'Cep'
               ,'Produto'
               ,'Data da Coleta'
               ,'Valor de Venda'
               ,'Valor de Compra'
               ,'Unidade de Medida'
               ,'Bandeira']
    
    qtd_itens = len(array)
    num_item = 0

    for url in array:

        num_item = num_item + 1
        percentual = (num_item/qtd_itens)*100
        print(percentual, f'% de Progresso. {num_item} de {qtd_itens} baixados.')
        
        if url.endswith('.csv'):
            # Leitura do arquivo como
            file = requests.get(url).content
            url_name = url.split('/')[-1]
            df_get = pl.read_csv(file,
                                separator=';',
                                infer_schema_length=10000,
                                new_columns=headers,
                                low_memory=False,
                                encoding='iso-8859-1')
            df_get.write_csv(f'./zip_extract/{url_name}', separator=';')

        elif url.endswith('.zip'):
            file = requests.get(url)
            url_name = url.split('/')[-1]
            with open(f'./zip_extract/{url_name}.zip', 'wb') as local:
                local.write(file.content)

            path_zip = f'./zip_extract/{url_name}.zip'
            path_sink = './zip_extract/'
            extrair_zip(path_zip, path_sink)
            

    arquivos = glob.glob("./zip_extract/*.csv")
    iter_arquivos = [pl.read_csv(arq,
                                separator=';',
                                infer_schema_length=10000,
                                new_columns=headers,
                                low_memory=False,
                                encoding='iso-8859-1') for arq in arquivos]
    
    df_final = pl.concat(iter_arquivos)
    df_final.write_csv('./dados/historico_combustivel_auto.csv')
    return 'Dados persistidos no diretório /Dados/'

get_array_persist()
    
    

