# Data Quality Analyzer - Streamlit & DuckDB 

Este é um aplicativo criado para análise de qualidade de dados, utilizando **Streamlit**, **PostgreSQL** e **Docker**. O projeto permite analisar dados de um banco PostgreSQL, verificando aspectos como completude, unicidade, conformidade com expressões regulares e distribuição de valores. A aplicação utiliza o **DuckDB** para consultas e visualização dos dados.

## Funcionalidades

- **Conexão com PostgreSQL**: Conecta-se ao banco de dados PostgreSQL e permite explorar schemas, tabelas e visualizar dados.
- **Análise de Qualidade de Dados**: Exibe métricas como completude, unicidade e contagem de nulos.
- **Distribuição de Valores**: Gera gráficos para visualizar a distribuição de valores nas colunas numéricas.
- **Conformidade com Regex**: Permite verificar se os dados de uma coluna atendem a uma expressão regular fornecida.
- **Gerenciamento de Privilégios**: Exibe informações sobre os usuários e seus privilégios nas tabelas.

## Tecnologias Utilizadas

- **Streamlit**: Para criar a interface interativa.
- **DuckDB**: Para consultas SQL no PostgreSQL.
- **PostgreSQL**: Banco de dados utilizado para armazenar e consultar dados.
- **Docker**: Para facilitar a configuração do ambiente de desenvolvimento e produção.

## Pré-requisitos

Antes de executar o projeto, certifique-se de ter as seguintes ferramentas instaladas:

- Docker e Docker Compose
- Python 3.11+
- PostgreSQL (caso não utilize o Docker para inicializar o banco)

## Instruções de Instalação

### 1. Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/data-quality-analyzer.git
cd data-quality-analyzer
```
### 2. Construir e Subir os Containers com Docker Compose

```bash
docker-compose up --build -d
```

### 3. Acessar a Aplicação

```bash
http://localhost:8501
```
