import streamlit as st
import duckdb
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração da página
st.set_page_config(layout="wide", page_title="Analisador de Qualidade de Dados")

st.title("🧪 Analisador de Qualidade de Dados - PostgreSQL")

# Função de conexão com PostgreSQL
def connect_to_postgres(host, port, user, password, dbname):
    conn = duckdb.connect()
    conn.execute("INSTALL postgres;")
    conn.execute("LOAD postgres;")
    conn.execute(f"ATTACH 'postgresql://{user}:{password}@{host}:{port}/{dbname}' AS postgres_db (TYPE postgres)")
    return conn

# Função para listar schemas
def get_schemas(conn):
    query = "SELECT schema_name FROM postgres_db.information_schema.schemata"
    schemas = conn.execute(query).fetchall()
    return [schema[0] for schema in schemas if schema[0] not in ('pg_catalog', 'information_schema')]

# Função para listar tabelas e views em um schema
def get_tables_with_types(conn, schema):
    query = f"SELECT table_name, table_type FROM postgres_db.information_schema.tables WHERE table_schema = '{schema}'"
    tables = conn.execute(query).fetchall()
    return tables

# Função para pegar detalhes das colunas de uma tabela
def get_table_details(conn, schema, table):
    query = f"""
    SELECT 
        c.column_name,
        c.is_nullable,
        c.data_type,
        pgd.description AS comment
    FROM postgres_db.information_schema.columns c
    LEFT JOIN postgres_db.pg_catalog.pg_description pgd
        ON pgd.objsubid = c.ordinal_position
        AND pgd.objoid = (
            SELECT oid FROM postgres_db.pg_catalog.pg_class 
            WHERE relname = '{table}' 
            AND relnamespace = (
                SELECT oid FROM postgres_db.pg_catalog.pg_namespace WHERE nspname = '{schema}'
            )
        )
    WHERE c.table_schema = '{schema}' AND c.table_name = '{table}'
    """
    return conn.execute(query).fetchdf()

# Função para listar os usuários e seus privilégios
def get_users_privileges(conn, schema, table):
    query = f"""
    SELECT 
        grantee,
        privilege_type
    FROM postgres_db.information_schema.role_table_grants
    WHERE table_schema = '{schema}' AND table_name = '{table}'
    """
    return conn.execute(query).fetchdf()

# Função para contar nulos
def get_null_counts(conn, schema, table):
    df_data = conn.execute(f"SELECT * FROM postgres_db.{schema}.{table}").fetchdf()
    null_counts = df_data.apply(lambda col: col.isnull().sum() + (col.astype(str).str.strip() == '').sum())
    null_counts = null_counts.reset_index()
    null_counts.columns = ['column_name', 'null_count']
    return null_counts, df_data

# Função para obter as chaves primárias
def get_primary_keys(conn, schema, table):
    query = f"""
    SELECT kcu.column_name
    FROM postgres_db.information_schema.table_constraints tc
    JOIN postgres_db.information_schema.key_column_usage kcu
      ON tc.constraint_name = kcu.constraint_name
     AND tc.table_schema = kcu.table_schema
     AND tc.table_name = kcu.table_name
    WHERE tc.constraint_type = 'PRIMARY KEY'
      AND tc.table_schema = '{schema}'
      AND tc.table_name = '{table}';
    """
    results = conn.execute(query).fetchall()
    return [row[0] for row in results]

# Função para verificar conformidade com regex
def check_regex_conformity(df_data, column_name, regex_pattern):
    regex = re.compile(regex_pattern)
    conformity = df_data[column_name].apply(lambda x: bool(regex.match(str(x)))).sum()
    total_rows = len(df_data)
    conformity_pct = (conformity / total_rows) * 100 if total_rows > 0 else 0
    non_conforming = df_data[~df_data[column_name].apply(lambda x: bool(regex.match(str(x))))]

    return conformity_pct, non_conforming

# Função para criar o histograma
def plot_histogram(df_data, column_name):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df_data[column_name], ax=ax, kde=True, bins=30, color='skyblue', edgecolor='black')
    ax.set_title(f"Distribuição da Coluna: {column_name}")
    ax.set_xlabel(column_name)
    ax.set_ylabel('Frequência')
    st.pyplot(fig)


# Função para permitir download de CSV
def download_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# Função principal do Streamlit
def main():
    with st.expander("🔧 Configuração da Conexão PostgreSQL", expanded=True):
        host = st.text_input("Host", "db")
        port = st.text_input("Porta", "5432")
        user = st.text_input("Usuário", "postgres")
        password = st.text_input("Senha", type="password")
        dbname = st.text_input("Nome do Banco", "postgres")
        if st.button("Conectar"):
            try:
                st.session_state.conn = connect_to_postgres(host, port, user, password, dbname)
                st.success("Conectado com sucesso!")
            except Exception as e:
                st.error(f"Erro na conexão: {e}")

    if "conn" in st.session_state and st.session_state.conn:
        conn = st.session_state.conn

        # Seleção de Schema
        schemas = get_schemas(conn)
        schema = st.selectbox("📂 Escolha o Schema", schemas)

        if schema:
            tables = get_tables_with_types(conn, schema)
            table_options = [table[0] for table in tables]
            table_type_dict = {table[0]: table[1] for table in tables}  # Dicionário com tipo de cada item

            table = st.selectbox("📄 Escolha a Tabela ou View", table_options)

            if table:
                # Exibir o tipo do item escolhido
                table_type = table_type_dict.get(table, "Desconhecido")
                st.metric("Tipo de Objeto", table_type)

                # Layout das abas
                tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔎 Qualidade dos Dados", "👥 Usuários e Privilégios", "🔍 Conformidade com Regex", "📋 Registros", "📊 Distribuição de Valores"])

                with tab1:
                    df_colunas = get_table_details(conn, schema, table)
                    df_nulos, df_data = get_null_counts(conn, schema, table)
                    pk_cols = get_primary_keys(conn, schema, table)

                    # Adiciona coluna indicando se é PK
                    df_colunas["is_pk"] = df_colunas["column_name"].apply(lambda col: "✅" if col in pk_cols else "❌")

                    # Merge com contagem de nulos
                    df_final = pd.merge(df_colunas, df_nulos, how="left", on="column_name")

                    # Cálculo de métricas
                    total_linhas = len(df_data)
                    total_colunas = len(df_data.columns)
                    total_celulas = total_linhas * total_colunas
                    total_nulos = df_data.apply(lambda col: col.isnull().sum() + (col.astype(str).str.strip() == '').sum()).sum()
                    total_preenchidos = total_celulas - total_nulos
                    completude_pct = (total_preenchidos / total_celulas) * 100 if total_celulas > 0 else 0

                    unicidade_pct = None
                    if pk_cols:
                        df_pk = df_data[pk_cols].dropna()
                        registros_unicos = len(df_pk.drop_duplicates())
                        unicidade_pct = (registros_unicos / total_linhas) * 100 if total_linhas > 0 else 0

                    # Contagem de linhas duplicadas
                    total_duplicadas = df_data.duplicated().sum()

                    # Exibir cards
                    col1, col2, col3, col4, col5 = st.columns(5)
                    col1.metric("🔢 Total de Linhas", f"{total_linhas:,}")
                    col2.metric("📊 Total de Colunas", f"{total_colunas}")
                    col3.metric("✅ % Completude", f"{completude_pct:.2f}%")
                    if unicidade_pct is not None:
                        col4.metric("🔐 % Unicidade da PK", f"{unicidade_pct:.2f}%")
                    else:
                        col4.metric("🔐 % Unicidade da PK", "PK não encontrada")
                    col5.metric("⚠️ Linhas Duplicadas", f"{total_duplicadas}")

                    # Mostrar detalhes da tabela
                    st.subheader("📚 Detalhes")
                    df_final = df_final.rename(columns={
                        "column_name": "Coluna",
                        "is_nullable": "É Nulo?",
                        "data_type": "Tipo",
                        "comment": "Comentário",
                        "null_count": "Qtd Nulos",
                        "is_pk": "É PK?"
                    })
                    st.dataframe(df_final, use_container_width=True)

                with tab2:
                    st.subheader("🔒 Usuários e Privilégios")
                    df_privileges = get_users_privileges(conn, schema, table)
                    if df_privileges.empty:
                        st.write("Nenhum privilégio encontrado para a tabela selecionada.")
                    else:
                        df_privileges_grouped = df_privileges.groupby('grantee')['privilege_type'].apply(lambda x: ', '.join(x)).reset_index()
                        st.dataframe(df_privileges_grouped, use_container_width=True)

                with tab3:
                    st.subheader("🔍 Verificar Conformidade com Regex")

                    column_name = st.selectbox("📏 Selecione a coluna para verificar", df_data.columns)
                    regex_pattern = st.text_input("📝 Insira a expressão regex")

                    if regex_pattern:
                        conformity_pct, non_conforming = check_regex_conformity(df_data, column_name, regex_pattern)

                        st.metric(label="📊 Porcentagem de Conformidade", value=f"{conformity_pct:.2f}%", delta=None, delta_color="normal")

                        if not non_conforming.empty:
                            st.write("🚨 Registros que não atendem à conformidade definida:")
                            st.dataframe(non_conforming, use_container_width=True)
                        else:
                            st.write("✅ Todos os registros estão conformes com a expressão regex!")

                with tab4:
                    st.subheader("📋 Visualizar Todos os Registros")
                    st.write("Aqui estão todos os registros da tabela selecionada.")
                    st.dataframe(df_data, use_container_width=True)

                    # Botão para download
                    csv_data = download_csv(df_data)
                    st.download_button("Baixar Dados (CSV)", csv_data, file_name=f"{table}_dados.csv", mime="text/csv")

                with tab5:
                    st.subheader("📊 Visualizar Distribuição de Valores")
                    
                    numeric_columns = df_data.select_dtypes(include=['number']).columns
                    
                    if numeric_columns.size > 0:
                        column_name = st.selectbox("📏 Selecione a coluna para ver a distribuição", numeric_columns)

                        if column_name:
                            plot_histogram(df_data, column_name)
                    else:
                        st.write("Não há colunas numéricas para gerar o histograma.")

if __name__ == "__main__":
    main()
