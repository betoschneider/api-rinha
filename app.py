from flask import Flask, jsonify, request
import psycopg2
from psycopg2 import sql
import json
from credenciais import credencial

app = Flask(__name__)

# Função para estabelecer uma conexão com o banco de dados PostgreSQL
def conectar():
    try:
        conexao = psycopg2.connect(**credencial)
        return conexao
    except psycopg2.Error as e:
        print(f"Erro: Não foi possível conectar ao banco de dados\n{e}")
        return None

#listar todas as pessoas
@app.route('/pessoas', methods=['GET'])
def get_pessoas():
    conexao = conectar()
    if conexao:
        try:
            cursor = conexao.cursor()
            query_selecionar_todos = '''
                SELECT id, apelido, nome, TO_CHAR(nascimento, 'dd/mm/yyyy') as nascimento, stack FROM pessoas;
            '''
            cursor.execute(query_selecionar_todos)
            # Obtém os resultados
            results = cursor.fetchall()

            # Obtém os nomes das colunas
            columns = [desc[0] for desc in cursor.description]

            # Cria um dicionário para cada linha e converte para JSON
            json_result = []
            for row in results:
                row_dict = dict(zip(columns, row))
                json_result.append(row_dict)

            return json.dumps(json_result, indent=2, ensure_ascii=False)
        except psycopg2.Error as e:
            print(f"Erro: Não foi possível recuperar os dados\n{e}")
        finally:
            cursor.close()
            conexao.close()


#buscar por id
@app.route('/pessoas/<pessoa_id>', methods=['GET'])
def get_pessoaa(pessoa_id):
    conexao = conectar()
    if conexao:
        try:
            cursor = conexao.cursor()
            consulta = '''
                SELECT id, apelido, nome, TO_CHAR(nascimento, 'dd/mm/yyyy') as nascimento, stack 
                FROM pessoas
                WHERE id = '%s';
            ''' % (pessoa_id)
            cursor.execute(consulta, (pessoa_id,))
            # Obtém o resultado
            result = cursor.fetchone()

            # Se não houver resultado, retorna None
            if result is None:
                return None

            # Obtém os nomes das colunas
            columns = [desc[0] for desc in cursor.description]

            # Cria um dicionário para a linha e converte para JSON
            row_dict = dict(zip(columns, result))

            return json.dumps(row_dict, indent=2, ensure_ascii=False), 200
        except psycopg2.Error as e:
            return {"message": "pessoa nao encontrada"}, 404
        finally:
            cursor.close()
            conexao.close()


#criar pessoa
@app.route('/pessoas', methods=['POST'])
def create_pessoa():
    conexao = conectar()
    if conexao:
        try:
            cursor = conexao.cursor()
            query_inserir_dados = sql.SQL('''
                INSERT INTO pessoas (apelido, nome, nascimento, stack)
                VALUES (%s, %s, %s, %s) RETURNING id;
            ''')
            cursor.execute(query_inserir_dados, (request.json['apelido'], request.json['nome'], request.json['nascimento'], request.json['stack']))
            id_funcionario = cursor.fetchone()[0]
            conexao.commit()
            return {"id": id_funcionario}, 200
        except psycopg2.Error as e:
            return {"message": "nao foi possivel incluir"}, 500
        finally:
            cursor.close()
            conexao.close()


#atualizar pessoa
@app.route('/pessoas/<int:pessoa_id>', methods=['PUT'])
def update_pessoa(pessoa_id):
    for pessoa in bd_pessoas:
        if pessoa['id'] == pessoa_id:
            pessoa['apelido'] = request.json['apelido']
            pessoa['nome'] = request.json['nome']
            pessoa['nascimento'] = request.json['nascimento']
            return pessoa, 200
    return {"message": "pessoa nao encontrada"}, 404

#deletar pessoa
@app.route('/pessoas/<int:pessoa_id>', methods=['DELETE'])
def delete_pessoa(pessoa_id):
    for pessoa in bd_pessoas:
        if pessoa['id'] == pessoa_id:
            bd_pessoas.remove(pessoa)
            return {"message": "Pessoa removida com sucesso."}, 202
    return {"message": "pessoa nao encontrada"}, 404


#executar app
if __name__ == '__main__':
    app.run(debug=True)