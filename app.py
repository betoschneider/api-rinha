from flask import Flask, jsonify, request

app = Flask(__name__)

#exemplo de pessoas
bd_pessoas = [
    {"id": 1, "apelido": "jose", "nome": "jose maria martins", "nascimento": "1995-05-30"},
    {"id": 2, "apelido": "jf", "nome": "joão francisco schneider", "nascimento": "2018-04-13"},
    {"id": 3, "apelido": "beto", "nome": "roberto schneider", "nascimento": "1979-01-01"},
    {"id": 4, "apelido": "buffe", "nome": "fernando buffe", "nascimento": "1999-03-06"}
]

#listar todas as pessoas
@app.route('/pessoas', methods=['GET'])
def get_pessoas():
    return bd_pessoas

#buscar por id
@app.route('/pessoas/<int:pessoa_id>', methods=['GET'])
def get_pessoa(pessoa_id):
    for pessoa in bd_pessoas:
        if pessoa['id'] == pessoa_id:
            return pessoa, 200
    return {"message": "pessoa nao encontrada"}, 404

#criar pessoa
@app.route('/pessoas', methods=['POST'])
def create_pessoa():
    nova_pessoa = {"id": len(bd_pessoas) + 1, "apelido": request.json['apelido'], "nome": request.json['nome'], "nascimento": request.json['nascimento']}
    bd_pessoas.append(nova_pessoa)
    return nova_pessoa

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