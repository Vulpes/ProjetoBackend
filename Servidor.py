from flask import Flask, request, jsonify
from Persistencia.JogadorBD import JogadorBD
from Persistencia.JogoBD import JogoBD
from Modelo.Jogador import Jogador
from Modelo.Jogo import Jogo
from flask_basicauth import BasicAuth 

app = Flask(__name__)

app.secret_key = 'A0B1C2D34E4F5G6H7I8J9'
app.config['BASIC_AUTH_USERNAME'] = 'Renato'
app.config['BASIC_AUTH_PASSWORD'] = '123456'

basic_auth = BasicAuth(app)

#parâmetro id é do tipo inteiro
#exemplo: http://endereçoServidor/jogador/10

@app.route("/jogadores", methods=["GET","POST","PUT","DELETE"])
@app.route("/jogadores/<int:id>", methods=["GET","POST","PUT","DELETE"])
@basic_auth.required
def jogador(id=None):
    if request.method == "GET":
        jogadorBD = JogadorBD()
        jogadores = []
        if id: # recebemos um id?
            jogador = jogadorBD.consultar(id)
            if jogador: 
                jogadores.append(jogador)
        else:
            jogadores = jogadorBD.consultar("")
        return jsonify([jogador.toJson() for jogador in jogadores])
        

    elif request.method == "POST":
        if id:
            return {"status" : "Método POST não permitido para /" + str(id)}
        else:
            if request.is_json:
                dados = request.get_json()
                pNome     = dados.get("nome")
                pDataNasc = dados.get("dataNasc")
                pApelido  = dados.get("apelido")
                pJogos    = dados.get("jogos")
                jogador = Jogador(id=0,nome=pNome,dataNasc=pDataNasc,apelido=pApelido,bibliotecaJogos=validarJogos(pJogos))
                jogadorBD = JogadorBD()
                jogadorBD.incluir(jogador)
                return {"id": jogador.id}
            else:
                return {"status":"O servidor aceita apenas dados no formato JSON."}

    elif request.method == "PUT":
        if id:
           if request.is_json:
               #transformação de JSON para dicionário Python via get_json()
               dados = request.get_json()
               nome     = dados.get("nome")
               dataNasc = dados.get("dataNasc")
               apelido  = dados.get("apelido")
               jogos    = dados.get("jogos")
               
               if (nome and dataNasc and apelido and jogos):
                           
                   jogador = Jogador(id=id, nome=nome, dataNasc=dataNasc, apelido=apelido, bibliotecaJogos=validarJogos(jogos))
                   jogadorBD = JogadorBD()
                   jogadorBD.atualizar(jogador)
                   return {"status":True}
               else:
                   return {"status":"Especifique o nome, a dataNasc e o apelido!"}
           else:
               return {"status":"Somente o formato JSON é aceito pelo servidor!"} 
        else:
            return {"status":"Especifique o id do recurso que deseja atualizar!"}
    elif request.method == "DELETE":
        if id:
            jogadorBD = JogadorBD()
            jogador = jogadorBD.consultar(id)
            if jogador:
                jogadorBD.apagar(jogador)
                return {"status":True}
            else:
                return {"status":"Jogador não encontrado no servidor!"}
        else:
            return {"status":"Especifique o id na url!"}
    else:
        pass
    
def validarJogos(jogos):
    listaJogos = []
    jogoBD = JogoBD()
    for jogo in jogos:
        retornoJogo = jogoBD.consultar(jogo["id"])
        if isinstance(retornoJogo, Jogo):
            listaJogos.append(retornoJogo)
    return listaJogos


@app.route("/jogos", methods=["GET", "POST", "DELETE", "PUT"])
@app.route("/jogos/<int:id>", methods=["GET", "POST", "DELETE", "PUT"])

def jogo(id=None):
    if request.method == "GET":
        jogoBD = JogoBD()
        jogos = []

        if id:
            jogo = jogoBD.consultar(id)

            if jogo:
                jogos.append(jogo)
        else:
            jogos = jogoBD.consultar("")

        return jsonify([jogo.toJson() for jogo in jogos])
    
    elif request.method == "POST":
        if id:
            return {"status" : "Erro! Utilize o metodo POST somente para cadastros."}
        else:
            if request.is_json:
                data = request.get_json()
                nome = data.get("nome")
                horasJogadas = data.get("horasJogadas")
                jogo = Jogo(nomeJogo=nome,conquistas=[], HorasJogadas=horasJogadas)
                print(jogo.toJson())
                jogoBD = JogoBD()
                jogoBD.incluir(jogo)
                return {"id": jogo.id}
    
    elif request.method == "DELETE":
        if id:
            jogoBD = JogoBD()
            jogo = jogoBD.consultar(id)

            if jogo: 
                jogoBD.apagar(jogo)
                return {"status" : "Jogo Excluído!"} 
            else:
                return {"status" : "Jogo não encontrado no servidor!"}
        else:
            return {"status" : "Não foi possível ler o id, verifique as informações e tente novamente."}        
    else:
        pass

if __name__ == "__main__":
    app.run('0.0.0.0', port=5000)