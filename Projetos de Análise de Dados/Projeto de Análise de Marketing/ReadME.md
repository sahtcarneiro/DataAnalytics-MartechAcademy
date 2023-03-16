# Análise de Dados usando Pandas e MongoDB

Essa análise de usou como base dados de uma loja, disponibilizado pelo bootcamp, onde continha dados dos clientes e das campanhas de marketing.

## Projeto

### Estrutura

Eu dividi o código em 3 partes principais:  
Infra: Parte responsável por fazer conexão com a google cloud platform, com o mongoDB, por enviar e receber os dados.  
Pandas: Parte responsavél por verificar, tratar e explorar os dados.  
Conclusão/Sugestão: Parte final onde, com base nos dados, cheguei a conclusões a cerca dos clientes e campanhas de marketing da loja.

### Infraestrutura

A infraestrutura se concentro em fazer as conexões com a google cloud platform e baixei o banco de dados de um bucket da google cloud platform, e enviei os dados brutos e tratados para pastas diferentes de outro bucket da google cloud e também em coleções diferentes de um database do mongodb.

### Pandas

Nessa parte fiz uso do numpy, pandas e os para exploração, tratamento e análise dos dados e pandera para verificação de dados.

##### Inconsistências

- Data de castrasdo dos clientes consta como tipo objeto
- Anos de nascimento que apontavam para 3 pessoas com mais de 120 anos, sendo possívelmente errados
- 2 linhas possivelmente duplicadas, com todos os dados idênticos exceto o ID e a aceitação na ultimá campanha
- Valores faltando na coluna de renda dos clientes
- Precisaria traduzir linhas e colunas

#### Tratamentos

- Data de cadastro passada para o tipo datatime
- Criação da coluna idade para evidênciar o problema das idades, porém nenhuma alteração a mais feita, apenas apontadas as linhas em que essas idades "estranhas" apareciam
- As linhas possivelmente duplicadas não foram mexidas pois não consegui dectar se de fato eraam duplicadas ou não, então apontei quais são e não as alterei
- Garanti que os valores que faltavam na coluna renda estavam no tipo NaN para não criar conflito ao armazenar nos bancos de dados e apontei quais linhas as inconsistências apareciam
- Tradução de linhas e colunas que foram possíveis

#### Dificuldades Percebidas

- Senti dificuldade principalmente em discernir se as linhas eram duplicads ou não, e não consegui chegar a uma conclusão quanto a isso
- O que me gerou mais problemas não técnicos foi a questão das traduções, que cheguei a possíveis conclusões sobre o que seriam algumas palavras, mas por não ter certeza e não achar fontes confiáveis deixei como estavam

#### Resultados das Análises

Perfil de cliente:

- Em média 51 anos;
- Mais da metade dos gastos com produtos são com vinhos, e somando com o segundo lugar(carne), somam mais de 80% da receita da loja;
- Não há ligação direta entre a idade dos cliente e o quanto eles gastam na loja;
- A escolaridade está diretamente relacionada com a renda dos clientes, sendo aqueles formados no ensino superior com uma faixa de renda superior do que os que não se formaram;
- Há uma ligação direta entre os cliente que tem maior renda com os que gastam mais na loja, sendo os que mais gastam aqueles que tem renda superior a 50mil;
- Mais da metade dos clientes tem filhos, sendo eles 1602, e apenas 638 não tem;

Campanhas de Marketing:

- Sobre as 6 campanhas de marketing apenas a ultima teve uma conversão de mais de 10%, a 3, 4 e 5° tiverem taaxas de conversões muito próximas, em torno de 7%, e a 2° foi a mais baixa, com 1.3% de conversão.

#### Conclusões e Sugestões

- Avaliar o motivo das adesões das campanhas serem por padrão abaixo de 10%, e principalmente a razão da segunda ter apenas 1.3%;
- Investigar o que levou uma queda de conversão da primeira para a segunda campanha;
- Focar no cliente que faz o perfil médio da loja;
- Balancear os produtos de acordo com a demanda dos clientes.

#### Satisfações com o Projeto

- Principalmente no que tange a parte da exploração dos dados;
- Também me surpreendi a pensamentos prévios que eu tinha e percebi resultado diferentes com base nos dados, isso foi bem interessante.

## Ferramentas

<a href = "https://colab.research.google.com/"> Google Colaboratory </a>  
<a href = "https://cloud.google.com/"> Google Cloud Platform </a>  
<a href = "https://www.mongodb.com"> MongolDB </a>  
<a href = "https://github.com/sahtcarneiro/DataAnalytics-MartechAcademy"> Github </a>

## Observação

Eu fiz esse projeto em live, streamando na plataforma da Twitch ao vivo, mostrando toda minha progressão e linha de pensamento no decorrer das análises.  
Caso queira conferir, as gravações ficam salvas na plataforma.
<a href = "https://www.twitch.tv/sahtcarneirotv"> Twitch </a>
