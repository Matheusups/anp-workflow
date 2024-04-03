# anp-workflow
Dados públicos (Open Data) do GOV.BR - Agência Nacional de Petróleo, Gás Natural e Biocombustíveis.

## Objetivo do Projeto

*Trazer uma solução não manual para criação de uma rotina de atualização dos dados da ANP (Agência Nacional do Petróleo, Gás Natural e Biocombustíveis)*. Atualmente o projeto possui 2 soluções de downloads possíveis, carga e unificação dos dados consolidados das últimas 4 semanas e carga e unificação dos dados históricos de Combustíveis Automotivos.

#### **download_dados_4_semanas**
- Faz uma captura no HTML da página do site que os dados são disponibilizados, obtem o url das bases que tem a atualização dos dados das últimas 4 semanas.
- Transforma o resultado da requisição em um dataframe
- Executa a unificação dos arquivos em um só e consolida como um .csv legível no diretório **./dados/**
<img width="538" alt="image" src="https://github.com/Matheusups/anp-workflow/assets/69797535/f8084826-2b94-43de-8acf-af833c835df2">



## Requirements
##### requests
```
pip install requests
```

##### polars
```
pip install polars
```
