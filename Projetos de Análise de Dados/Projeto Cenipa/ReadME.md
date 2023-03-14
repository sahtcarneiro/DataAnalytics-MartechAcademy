# Análise de Dados do Cenipa

Essa análise de usou como base dados do Cenipa, disponibilizado pelo bootcamp, onde continha dados dos acidentes e incidentes aéreos no Brasil.

## Projeto

### Estrutura

Eu dividi o código em 3 partes principais:  
Infra: Parte responsável por fazer conexão com a google cloud platform, por enviar e receber os dados.  
Pandas: Parte responsavél por verificar, tratar e explorar os dados.  
Conclusão: Parte final onde, com base nos dados, cheguei a conclusões e as apresentei.

### Infraestrutura

A infraestrutura se concentro em fazer as conexões com a google cloud platform e baixei o banco de dados de um bucket da google cloud platform.

### Pandas

Nessa parte fiz uso do numpy, pandas e os para exploração, tratamento e análise dos dados e pandera para verificação de dados.

##### Inconsistências

- Data de castrasdo dos clientes consta como tipo objeto
- Quase 10 mil dados faltando e inconsistentes
- Colunas com informações redundantes
- Valores registrados de maneira incorreta

#### Tratamentos

- Data de cadastro passada para o tipo datatime
- Drop de colunas redundantes
- Garanti que os valores que faltavam ou foram resgistrados incorretamente nas colunas estavam no tipo NaN para não criar conflito ao armazenar nos bancos de dados e apontei quais linhas as inconsistências apareciam
- Alteração no nome das colunas para simplificar visualização e mudança de ordem

#### Dificuldades Percebidas

- Em decidir como gerenciar a quantidade de dados que faltavam, mas como muitos eram redundantes ou dispensáveis para a análise acabei dropando boa parte das colunas que continham problema, reduzindo em quase 6mil inconcistências
- Entender as "regras do negócio" e precisar pesquisar mais sobre códigos de aerodromos pra só então saber quais códigos estavam corretos e quais foram registrados incorretamente.

#### Resultados das Análises e Conclusões

Classificação por tipo de Ocorrência:

- De maneira geral a maior parte de dá por incidentes, a segunda maior por acidentes e a menor por incidentes graves.

Local da Ocorrência:  
 - O maior número de ocorridos acontece na região sudeste, principalmente no estado de São Paulo;  
 - O menor número de ocorridos se dá ná região nordeste.

Quantidade de Aeronaves Envolvidas:  
 - A maior parte das ocorrências envolve apenas uma aeronave;  
 - A valor máximo de aeronaves envolvidas são 3;  
 - Considerando apenas as ocorrências que envolveram mais de uma aeronaves a quantidade de ocorridos por Uf muda um pouco e estados que era campeões de ocorrências descem bastantes posições, como é o caso do Mato Grosso.

Saída de Pista: - Mais de 90% das ocorrências não envolvem saída de pista;  
 - Os ocorridos que envolvem saída de pista(menos de 10% do total) seguem o mesmo padrão de quantidade de acidente pro Uf do total de ocorridos;  
 - Das ocorrências qe houveram saída de pista(menos de 10% do total) mudam o padrão de classificação de tipo de ocorrência, passando a ser a maior parte de acidentes, a segunda maior incidentes graves e a menor de incidentes.

Inconsistências da Coluna Aerodromo:  
 - Não foi visualizado nenhum padrão regional ou temporal qual ao registro inconsistente dos dados de aerodromo, porém for percebido que ele cresce proporcionalmente ao número de ocorrências, logo deve haver uma ligação diretamente proporcional entre o número de registros a serem feitos e o números de erros de nos resgistros.

#### Satisfações com o Projeto

- Neste caso aprendi muito sobre o tratamento de dados e encarei muitos desafios quanto a isso.

## Ferramentas

<a href = "https://colab.research.google.com/"> Google Colaboratory </a>  
<a href = "https://code.visualstudio.com/"> Visual Studio Code </a>  
<a href = "https://cloud.google.com/"> Google Cloud Platform </a>  
<a href = "https://github.com/sahtcarneiro/DataAnalytics-MartechAcademy"> Github </a>

## Observação

Eu fiz esse projeto em live, streamando na plataforma da Twitch ao vivo, mostrando toda minha progressão e linha de pensamento no decorrer das análises.  
Caso queira conferir, as gravações ficam salvas na plataforma.
<a href = "https://www.twitch.tv/sahtcarneirotv"> Twitch </a>
