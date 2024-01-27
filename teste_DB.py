import psycopg2
from psycopg2 import sql
from credenciais import credencial

# Função para estabelecer uma conexão com o banco de dados PostgreSQL
def conectar():
    try:
        conexao = psycopg2.connect(**credencial)
        return conexao
    except psycopg2.Error as e:
        print(f"Erro: Não foi possível conectar ao banco de dados\n{e}")
        return None

# Função para criar uma tabela
def criar_tabela():
    conexao = conectar()
    if conexao:
        try:
            cursor = conexao.cursor()
            query_criar_tabela = '''
                CREATE TABLE IF NOT EXISTS pessoas (
                    id UUID DEFAULT gen_random_uuid(),
                    apelido VARCHAR(32) CONSTRAINT APELIDO_PK PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    nascimento DATE NOT NULL,
                    stack VARCHAR[],
                    busca VARCHAR GENERATED ALWAYS AS (apelido || ' ' || nome || ' ' || stack) STORED
                );
            '''
            cursor.execute(query_criar_tabela)
            conexao.commit()
            print("Tabela criada com sucesso")
        except psycopg2.Error as e:
            print(f"Erro: Não foi possível criar a tabela\n{e}")
        finally:
            cursor.close()
            conexao.close()

# Função para inserir dados na tabela
def inserir_dados(apelido, nome, nascimento, stack=None):
    conexao = conectar()
    if conexao:
        try:
            cursor = conexao.cursor()
            query_inserir_dados = sql.SQL('''
                INSERT INTO pessoas (apelido, nome, nascimento, stack)
                VALUES (%s, %s, %s, %s) RETURNING id;
            ''')
            cursor.execute(query_inserir_dados, (apelido, nome, nascimento, stack))
            id_funcionario = cursor.fetchone()[0]
            conexao.commit()
            print(f"Dados inseridos com sucesso com ID: {id_funcionario}")
        except psycopg2.Error as e:
            print(f"Erro: Não foi possível inserir os dados\n{e}")
        finally:
            cursor.close()
            conexao.close()

# Função para recuperar todos os dados da tabela
def recuperar_dados():
    conexao = conectar()
    if conexao:
        try:
            cursor = conexao.cursor()
            query_selecionar_todos = '''
                SELECT id, apelido, nome, nascimento, stack FROM pessoas;
            '''
            cursor.execute(query_selecionar_todos)
            registros = cursor.fetchall()
            print("\nDados dos Pessoas:")
            for registro in registros:
                print(registro)
        except psycopg2.Error as e:
            print(f"Erro: Não foi possível recuperar os dados\n{e}")
        finally:
            cursor.close()
            conexao.close()

# Função para atualizar dados na tabela
def atualizar_dados(id_funcionario, nome_novo):
    conexao = conectar()
    if conexao:
        try:
            cursor = conexao.cursor()
            query_atualizar_dados = sql.SQL('''
                UPDATE pessoas SET nome = %s WHERE id = %s;
            ''')
            cursor.execute(query_atualizar_dados, (nome_novo, id_funcionario))
            conexao.commit()
            print("Dados atualizados com sucesso")
        except psycopg2.Error as e:
            print(f"Erro: Não foi possível atualizar os dados\n{e}")
        finally:
            cursor.close()
            conexao.close()

# Função para excluir dados da tabela
def excluir_dados(id_funcionario):
    conexao = conectar()
    if conexao:
        try:
            cursor = conexao.cursor()
            query_excluir_dados = sql.SQL('''
                DELETE FROM pessoas WHERE id = %s;
            ''')
            cursor.execute(query_excluir_dados, (id_funcionario,))
            conexao.commit()
            print("Dados excluídos com sucesso")
        except psycopg2.Error as e:
            print(f"Erro: Não foi possível excluir os dados\n{e}")
        finally:
            cursor.close()
            conexao.close()

if __name__ == "__main__":
    criar_tabela()

    # Inserindo dados
    inserir_dados("João", "João Silva", "1980-05-30", ["oracle"])
    inserir_dados("Maria", "Maria Oliveira", "01-01-1979", ["mongodb"])
    inserir_dados("João", "João Ribeiro", "1980-05-30", "['delphi']")
    inserir_dados("Maria", "Maria Cristina", "1995-09-30", "['cobol']")
    inserir_dados("JF", "João Francisco", "31-12-1990", ["mongodb", 'oracle'])

    # Recuperando dados
    recuperar_dados()

    # Atualizando dados
    atualizar_dados(1, "Desenvolvedor Sênior de Software")

    # Recuperando dados após a atualização
    recuperar_dados()

    # Excluindo dados
    excluir_dados(2)

    # Recuperando dados após a exclusão
    recuperar_dados()
