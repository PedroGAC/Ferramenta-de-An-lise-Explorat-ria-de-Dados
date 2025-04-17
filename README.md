# Análise Exploratória de Dados com Streamlit

Esta aplicação foi desenvolvida como solução para o exercício 3 do processo seletivo de estágio da ESC Inovação. Ela permite realizar análise exploratória de dados através de uma interface gráfica intuitiva, utilizando as bibliotecas Streamlit e Pandas.

## Funcionalidades

### Carregamento de Dados
- **Upload de arquivos**: Suporte para formatos CSV e Excel
- **Datasets de exemplo**: Acesso imediato aos datasets Iris e Boston Housing

### Visualização de Dados
- **Tabela interativa**: Visualização dos dados em formato tabular
- **Controle de paginação**: Escolha o número de linhas a exibir

### Estatísticas Descritivas
- **Métricas básicas**: Média, mediana, desvio padrão, mínimo, máximo, quartis
- **Matriz de correlação**: Mapa de calor interativo mostrando correlações entre variáveis

### Visualizações Gráficas
- **Histogramas**: Análise da distribuição de variáveis individuais
- **Scatter plots**: Exploração de relações entre pares de variáveis
- **Box plots**: Identificação de outliers e distribuição dos dados
- **Gráficos 3D interativos**: Visualização da relação entre três variáveis simultaneamente

### Filtragem de Dados
- **Filtros numéricos**: Seleção de intervalos usando sliders
- **Filtros categóricos**: Seleção múltipla de valores
- **Visualização dos resultados**: Apresentação dos dados filtrados

## Requisitos

- Python 3.7 ou superior
- Bibliotecas Python (listadas em `requirements.txt`):
  - streamlit
  - pandas
  - numpy
  - matplotlib
  - seaborn
  - scikit-learn
  - plotly
  - openpyxl

## Instalação

1. Clone este repositório ou baixe os arquivos
2. Instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

## Execução

Para iniciar a aplicação, execute o seguinte comando no terminal:

```bash
streamlit run app.py
```

A aplicação será aberta automaticamente no seu navegador padrão. Caso isso não aconteça, acesse http://localhost:8501.

## Instruções de Uso

### Passo 1: Carregar um Dataset
- No menu lateral, escolha entre fazer upload de um arquivo ou usar um dataset de exemplo
- Para upload, clique no botão e selecione um arquivo CSV ou Excel
- Para dados de exemplo, selecione Iris ou Boston Housing no dropdown

### Passo 2: Explorar os Dados
- Na seção "Visão Geral dos Dados", confira as dimensões e primeiras linhas do dataset
- Em "Estatísticas Descritivas", selecione as colunas de interesse para análise
- Explore a matriz de correlação para identificar relações entre variáveis

### Passo 3: Criar Visualizações
- Na seção "Visualizações", navegue entre as abas para diferentes tipos de gráficos:
  - **Histogramas**: Selecione uma coluna para visualizar sua distribuição
  - **Scatter Plot**: Escolha variáveis para os eixos X e Y, com opção de colorir por categoria
  - **Box Plot**: Analise a distribuição e outliers, com opção de agrupar por categoria
  - **Gráfico 3D**: Explore relações tridimensionais entre variáveis, com rotação interativa

### Passo 4: Filtrar Dados
- Na seção "Filtragem de Dados", selecione as colunas para criar filtros
- Ajuste os parâmetros dos filtros (intervals para dados numéricos, valores para categóricos)
- Visualize imediatamente os resultados da filtragem na tabela abaixo

## Estrutura de Arquivos

- `app.py`: Código principal da aplicação Streamlit
- `README.md`: Esta documentação
- `requirements.txt`: Lista de dependências Python

## Recursos Adicionais

### Interagindo com o Gráfico 3D
- **Rotação**: Clique e arraste para girar o gráfico
- **Zoom**: Use o scroll do mouse ou gesto de pinça
- **Pan**: Pressione Shift + clique e arraste
- **Reset**: Clique duas vezes no gráfico

## Considerações Técnicas

- A aplicação utiliza cache para performance otimizada
- Tratamento de erro para diversos formatos de arquivo
- Interface responsiva adaptada a diferentes tamanhos de tela
- Suporte para tipos de dados numéricos e categóricos

---

Desenvolvido para o processo seletivo da ESC Inovação - 2025