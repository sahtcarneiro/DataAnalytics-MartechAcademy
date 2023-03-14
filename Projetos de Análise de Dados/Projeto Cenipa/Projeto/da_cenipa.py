# -*- coding: utf-8 -*-
"""da_cenipa.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uMeYSvdVRVu5yY6mE5HgmhhxSjbNk4Jv

# Analista    
Jonathas Carneiro

# Infra
"""

pip install gcsfs

pip install pandera

import pandas as pd
import pandera as pa
import numpy as np
import os
from google.cloud import storage

pd.set_option('display.max_columns',100)

#Configurações Google Cloud Storage
serviceAccount = '/content/total-bliss-377820-f1ed919eefd3.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = serviceAccount

#Configurações Google Cloud Storage
client = storage.Client()
bucket = client.get_bucket('jonathascarneiro01')
bucket.blob('ocorrenciass.csv')
path = 'gs://jonathascarneiro01/brutos/ocorrenciass.csv'

"""# Pandas"""

df = pd.read_csv(path,sep=';',encoding='ISO-8859-1',parse_dates=['ocorrencia_dia'],dayfirst=True)

"""##Pré análise

Visualizando de Maneira Geral o dataframe
"""

df

df.head(30)

df.tail()

df.dtypes

"""Os tipos parecem ok"""

df.shape

"""Setei a quantidade de dados padrão que devem haver em todas as colunas"""

df.info()

"""Aqui percebo que há colunas com dados faltando, essas são:   
ocorrencia_latitude           
ocorrencia_longitude           
investigacao_aeronave_liberada     
investigacao_status             
divulgacao_relatorio_numero     
divulgacao_dia_publicacao

##Backup
"""

dfback = df.copy()

"""##Transformações (limpeza, conversão, etc)  


"""

df

"""Checando se há valores repeditos no código de ocorrência ou se são valores únicos"""

df.codigo_ocorrencia.is_unique

"""Drop de colunas com informações repetidas repetidas"""

#Drop de colunas codigo de ocorrencia repetidas
df.drop(['codigo_ocorrencia1','codigo_ocorrencia2','codigo_ocorrencia3','codigo_ocorrencia4'],axis=1,inplace=True)

"""Decisão a cerca do drop ou não das colunas de investigação de aeronave e status da investigação"""

df['investigacao_aeronave_liberada'].unique()

df['investigacao_aeronave_liberada'].value_counts()

df['investigacao_aeronave_liberada'].isnull().sum()

df['investigacao_status'].unique()

df['investigacao_status'].value_counts()

df['investigacao_status'].isnull().sum()

"""Drop de colunas com problemas ou não utilizadas nas análises.   
Explicação: A cerca da latitude e longetide decidi dropar pois já contesta cidade e UF da ocorrência, e as demais colunas tem seus significados interligados, e como algumas tem imprecisões e valores faltantes em excesso decidi por não usá-las na análise e dropar elas
"""

# Drop de colunas com problemas e/ou não utilizadas na analise
df.drop(['ocorrencia_latitude','ocorrencia_longitude','investigacao_aeronave_liberada','investigacao_status','divulgacao_relatorio_numero','divulgacao_relatorio_publicado','divulgacao_dia_publicacao'],axis=1,inplace=True)

df

"""Rename das colunas simplificando"""

#Reneando colunas
df.rename(columns={'ocorrencia_classificacao':'classificacao','ocorrencia_cidade':'cidade','ocorrencia_uf':'uf','ocorrencia_pais':'pais','ocorrencia_aerodromo':'aerodromo','ocorrencia_dia':'data','ocorrencia_hora':'horario','total_aeronaves_envolvidas':'n_aeronaves','ocorrencia_saida_pista':'saida_pista'},inplace=True)

df.dtypes

df

"""Olhando o dataframe acima percebo inconsistências na coluna de aerodromos, e decido verificar a fundo"""

sorted(pd.unique(df['aerodromo']))

"""## Backup
Backup antes do tratamento de inconsistências
"""

df_backup2 = df.copy()

#inconsistencias encontradas, coluna aerodromo:  
'''
'***',
 '**NI'
'''
('***','**NI')

"""Usando o numpy para passar os dados inconsistentes para NaN, tipo de dados bem aceitos por bancos de dados, já que o pandas só poderia transforma em NA, um tipo que não é bem aceito."""

# Alteração 
df.replace(['***','**NI'],np.NaN,inplace=True)

"""Conferindo o rename"""

(pd.unique(df['aerodromo']))

df

df.dtypes

"""Checando quantos valores nulas há no dataframe"""

#Verificar dados nulos, ausentes, etc
df.isna().sum()

"""Aqui comparo com a quantidade de valores nulos que tinha com o dataframe antes do tratamento que fiz até então

Uma diferença de 6.997 dados inconsistêntes
"""

dfback.isna().sum()

#Verificando valores contidos
df.count()

"""Criando novo dataframe menor apenas com os dados que eu quero visualizar"""

df_estado_classificacao = df[['codigo_ocorrencia','uf','classificacao']]

df_estado_classificacao

"""##Schema 
validação de dados com pandera
"""

schema = pa.DataFrameSchema(
    columns = {
        'codigo_ocorrencia':pa.Column(pa.Int),
        'classificacao':pa.Column(pa.String),
        'cidade':pa.Column(pa.String),
        'uf':pa.Column(pa.String,pa.Check.str_length(2,2),nullable=True),
        'pais':pa.Column(pa.String),
        'aerodromo':pa.Column(pa.String,pa.Check.str_length(4,4),nullable=True),
        'data':pa.Column(pa.DateTime),
        'horario':pa.Column(pa.String,pa.Check.str_matches(r'^([0-1]?[0-9]|[2][0-3]):([0-5][0-9]):([0-5][0-9])?$'),nullable=True),
        'total_recomendacoes':pa.Column(pa.Int),
        'n_aeronaves':pa.Column(pa.Int),
        'saida_pista':pa.Column(pa.String,pa.Check.str_length(3,3)),
    }
)

df.dtypes

"""## Exploração de Dados

###Busca(Query)
"""

# O iloc busca apenas via indice, e não busca por valores(até vai mas n rola), então cuidado ao usar, apenas quando fizer a ordenação por indice
# Como é por indice ele aceita o -1 para buscar o último
#df.iloc[ ]

df.loc[0]

df.loc[1000:1002]

df.loc[1000,'aerodromo']

# Busca avançada
df.loc[[0,1000,2000],['classificacao','uf']]

df.loc[:,'horario']

"""Mudar especifico informação de certa coluna, geralmente utilizado para tradução de valores.  
Mais recomendado para valores especificos do que replace pois é mais especifico e descritivo a alteração, e mais fácil conserto.

Cuidado ao converter pois deve-se manter o mesmo tipo da coluna,  
se mudar o tipo de uma coluna com int ou float, vira objeto, msm voltando para int ou float continua objeto, precisa converter novamente
"""

df.loc[df.classificacao == 'INCIDENTE GRAVE']

"""## Análise de Dados

###Filtros, Agrupamentos e Plotagens
"""

#Filtro para valores nulos
filtronulo = df.aerodromo.isna()
df.loc[filtronulo]

filtronulo = df.uf.isna()
df.loc[filtronulo]

filtroacidente = df.classificacao == 'ACIDENTE'
df.loc[filtroacidente]
#dfacidentes = df.loc[filtroacidente]
#criar novo dv com infos que quero, assim povo mandar direto pra alguem

"""Filtro mais detalhado  
data.dt é o data time posso puxar pelo oq eu quiser, nesse caso pelo ano, qnd for igual a 2021
"""

#Filtro mais detalhado
ftcidade = df.cidade == 'SÃO PAULO'
ftpista = df.saida_pista == 'SIM'
ft2021 = df.data.dt.year == 2021
ftuf = df.uf == "SP"

df.loc[ftcidade & ftpista & ft2021 & ftuf]

ftabril = df.data.dt.month == 4
ftquinz = (df.data.dt.day > 0) & (df.data.dt.day < 16)
df.loc[ftabril & ftquinz]

# Filtro pra palavras terminadas em RIO, nome igual nos dados, se tiver tudo maiusculo =, se n = tb
# pra fazer diferente tem que fazer um for in com um .lower()
filtroletras = df.cidade.str[-3:] == 'RIO'
df.loc[filtroletras]

#Filto para letras dentro do valor
filtrointerno = df.cidade.str.contains('BO|MA')
df.loc[filtrointerno]

""">posso usar com .count() mas ta quase deprecated, melhor usar size()  
>padrão de ascending é true, colocando false fica do maior pro menos
"""

df.groupby(['classificacao']).size().sort_values(ascending=False)

#.plot() pra fazer plotagem

df.groupby(['aerodromo'],dropna=False).size().sort_values(ascending=False)

# plotagem .plot. tipo de plotagem (tem barra(bar), pizza (pie), linhas(line))
df.groupby(['uf'],dropna=False).size().sort_values(ascending=False).plot.bar(figsize=(12,8),xlabel='ESTADO',ylabel='N. Ocorrencias')

df.groupby('saida_pista',dropna=False).size().sort_values(ascending=False).plot.pie(figsize=(12,8),ylabel='Casos de Saída de Pista')

"""#### Análises por tipo de acidente"""

df.groupby(['classificacao']).size().sort_values(ascending=False)

df.groupby(['classificacao']).size().sort_values(ascending=False).plot.bar(figsize=(24,8))

df.groupby(['classificacao']).size().sort_values(ascending=False).plot.pie(figsize=(24,8))

"""#### Análise de quantidade de acidentes por UF"""

df.groupby(['uf'],dropna=False).size().sort_values(ascending=False)

df.groupby(['uf'],dropna=False).size().sort_values(ascending=False).plot.bar(figsize=(24,8),xlabel='ESTADO',ylabel='N. Ocorrencias')

"""##### Dividindo a análise de quantidade de acidentes por regiões"""

df_regioes = df.copy()
df_regioes.loc[df_regioes['uf'] == 'SP', 'regiao'] = 'SUDESTE'
df_regioes.loc[df_regioes['uf'] == 'MG', 'regiao'] = 'SUDESTE'
df_regioes.loc[df_regioes['uf'] == 'RJ', 'regiao'] = 'SUDESTE'
df_regioes.loc[df_regioes['uf'] == 'PR', 'regiao'] = 'SUL'
df_regioes.loc[df_regioes['uf'] == 'RS', 'regiao'] = 'SUL'
df_regioes.loc[df_regioes['uf'] == 'GO', 'regiao'] = 'CENTRO-OESTE'
df_regioes.loc[df_regioes['uf'] == 'MT', 'regiao'] = 'CENTRO-OESTE'
df_regioes.loc[df_regioes['uf'] == 'PA', 'regiao'] = 'NORTE'
df_regioes.loc[df_regioes['uf'] == 'AM', 'regiao'] = 'NORTE'
df_regioes.loc[df_regioes['uf'] == 'BA', 'regiao'] = 'NORDESTE'
df_regioes.loc[df_regioes['uf'] == 'SC', 'regiao'] = 'SUL'
df_regioes.loc[df_regioes['uf'] == 'MS', 'regiao'] = 'CENTRO-OESTE'
df_regioes.loc[df_regioes['uf'] == 'DF', 'regiao'] = 'CENTRO-OESTE'
df_regioes.loc[df_regioes['uf'] == 'PE', 'regiao'] = 'NORDESTE'
df_regioes.loc[df_regioes['uf'] == 'CE', 'regiao'] = 'NORDESTE'
df_regioes.loc[df_regioes['uf'] == 'ES', 'regiao'] = 'SUDESTE'
df_regioes.loc[df_regioes['uf'] == 'MA', 'regiao'] = 'NORDESTE'
df_regioes.loc[df_regioes['uf'] == 'RR', 'regiao'] = 'NORTE'
df_regioes.loc[df_regioes['uf'] == 'AC', 'regiao'] = 'NORTE'
df_regioes.loc[df_regioes['uf'] == 'TO', 'regiao'] = 'NORTE'
df_regioes.loc[df_regioes['uf'] == 'RO', 'regiao'] = 'NORTE'
df_regioes.loc[df_regioes['uf'] == 'PI', 'regiao'] = 'NORDESTE'
df_regioes.loc[df_regioes['uf'] == 'AL', 'regiao'] = 'NORDESTE'
df_regioes.loc[df_regioes['uf'] == 'PB', 'regiao'] = 'NORDESTE'
df_regioes.loc[df_regioes['uf'] == 'SE', 'regiao'] = 'NORDESTE'
df_regioes.loc[df_regioes['uf'] == 'RN', 'regiao'] = 'NORDESTE'
df_regioes.loc[df_regioes['uf'] == 'AP', 'regiao'] = 'NORTE'
df_regioes.loc[df_regioes['uf'].isnull(), 'regiao'] = "NaN"

df_regioes.replace(["NaN"],np.NaN,inplace=True)

df_regioes.groupby(['regiao'],dropna=False).size().sort_values(ascending=False)

df_regioes.groupby(['regiao'],dropna=False).size().sort_values(ascending=False).plot.bar(figsize=(24,8))

"""Fica claro que a região sudente concentra o maior número de ocorridos.

#### Análise de número de aeronaves envolvidas nos acidentes
"""

df['n_aeronaves'].value_counts()

df.groupby(['n_aeronaves']).size().sort_values(ascending=False).plot.bar(figsize=(12,8))

"""É perceptível que a maioria esmagadora das ocorrências se dá com uma única aeronave, será que os ocorridos com mais de uma revela algum padrão? ocorre em um mesmo estado? em um mesmo periodo do ano? ou em um mesmo aerodromo?"""

df_mais1_aeronave = df.loc[df['n_aeronaves'] >= 2]

df_mais1_aeronave

"""Agora verifico novamente o número de acidentes por Uf para comparar com a análise anterior"""

df_mais1_aeronave.groupby(['uf'],dropna=False).size().sort_values(ascending=False)

df_mais1_aeronave.groupby(['uf'],dropna=False).size().sort_values(ascending=False).plot.bar(figsize=(24,8),xlabel='ESTADO',ylabel='N. Ocorrencias')

"""Conclusões:"""

df.groupby(['uf'],dropna=False).size().sort_values(ascending=False)

"""#### Análise por saída de pista"""

df.groupby(['saida_pista']).size().sort_values(ascending=False)

df.groupby(['saida_pista']).size().sort_values(ascending=False).plot.pie()

"""Percebe-se que menos de 10% incorre em saída de pista, então vale analisar em detalhes apenas os que isso ocorreu em vez de analisar todos.

##### Análise apenas dos acidentes que saíram da pista
"""

df_saida_pista = df.loc[df['saida_pista'] == "SIM"]

"""Em quais estados ocorreram essa saída de pista?"""

df_saida_pista.groupby(['uf'],dropna=False).size().sort_values(ascending=False)

df_saida_pista.groupby(['uf'],dropna=False).size().sort_values(ascending=False).plot.bar(figsize=(24,8))

"""Parece seguir o padrão de acidentes por estado

Os acidentes que incorrem saida de pista costumam envolver mais de uma aeronave?
"""

df_saida_pista['n_aeronaves'].value_counts()

"""Aqui percebo que todos envolvem apenas 1 aeronave

Qual a classificação desses acidentes que saem da pista?
"""

df_saida_pista.groupby(['classificacao']).size().sort_values(ascending=False)

df_saida_pista.groupby(['classificacao']).size().sort_values(ascending=False).plot.bar(figsize=(24,8))

"""Comparação com a classificação de acidentes total"""

df.groupby(['classificacao']).size().sort_values(ascending=False)

"""Percebe-se que no total de acidente a maior quantidade se dá aos incidentes, em segundo lugar aos acidentes e em terceiro os incidentes graves, mas no que tange os que envolve aeronaves que sairam da pista o maior número é de acidentes, em segundo lugar de incidentes graves e em terceiro incidentes

#### Análisando os dados que constam sem aerodromo
Será que os problemas vieram de uma mesma cidade? mesmo estado? mesma período do ano?
"""

df

df_aerodromo_inconsistente = df.loc[df['aerodromo'].isnull()]

df_aerodromo_inconsistente

df_aerodromo_inconsistente.groupby(['uf'],dropna=False).size().sort_values(ascending=False)

df_aerodromo_inconsistente.groupby(['uf'],dropna=False).size().sort_values(ascending=False).plot.bar(figsize=(24,8))

"""não parece haver um padrão de Uf para os dados inconsistêntes no aerodromo"""

df_aerodromo_inconsistente.groupby(['data'],dropna=False).size()

df_aerodromo_inconsistente.groupby(['data'],dropna=False).size().plot.bar(figsize=(60,20))

"""aparentemente não há um padrão temporal para o registro de aerodromo inconsistentes

Será que categorizando as inconcistências por região algum padrão surge?
"""

df_aerodromo_inconsistente = df_regioes.loc[df['aerodromo'].isnull()]

df_aerodromo_inconsistente.groupby(['regiao'],dropna=False).size().sort_values(ascending=False)

df_aerodromo_inconsistente.groupby(['regiao'],dropna=False).size().sort_values(ascending=False).plot.bar(figsize=(24,8))

"""Aparentemente não, segue o mesmo padrão de número de acidentes, o que me leve a acreditar que quanto maior o número de registros de ocorrências cresce também o número de inconssistências nos registros

# Conclusões das Análises

Classificação de Ocorrência:    
    *   De maneira geral a maior parte se dá por incidentes, a segunda maior por acidentes e a menor parte por incidentes graves.    
        
Local da Ocorrência:    
    *   O maior número de ocorridos se dá na região sudeste, principalmente no estado de São Paulo    
    *   O menor número de ocorrências ocorre na região nordeste.    
    
Quantidade de Aeronaves:     
    *   A maior parte dos ocorridos envolvem apenas uma aeronave    
    *   Quando consideramos apenas os ocorridos que envolvem apenas mais de uma aeronave alguns estados que eram campeões de ocorrências descem bastantes posições, como é o caso do Mato Grosso.        

Saída de Pista:    
    *   Mais de 90% dos ocorridos não envolvem saída de pista    
    *   Os ocorridos que envolvem saída de pista(menos de 10% do total) seguem o mesmo padrão de quantidade de acidente pro Uf do total de ocorridos.    
    *   Das ocorrências qe houveram saída de pista(menos de 10% do total) mudam o padrão de classificação de tipo de ocorrência, passando a ser a maior parte de acidentes, a segunda maior incidentes graves e a menor de incidentes   
     
Inconsistências da Coluna Aerodromo:    
    *   Não foi visualizado nenhum padrão regional ou temporal qual ao registro inconsistente dos dados de aerodromo, porém for percebido que ele cresce proporcionalmente ao número de ocorrências, logo deve haver uma ligação diretamente proporcional entre o número de registros a serem feitos e o números de erros de nos resgistros.
"""