from Modelo.Jogador import Jogador
from Modelo.Jogo import Jogo
from Modelo.Conquista import Conquista
import sqlite3

caminhoBancoDados = './BancoDeDados/Jogos.db'

class JogoBD(object):
    
    def __init__(self):
        self.__conexao = sqlite3.connect(caminhoBancoDados)
        with self.__conexao as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS Jogo(
                    id integer not null primary key autoincrement,
                    nome text not null,
                    horasJogadas text not null
                )
            """)
            conn.commit()

    def incluir(self, jogo):
        if isinstance(jogo,Jogador):
            with self.__conexao as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO jogo(nome, horasJogadas) 
                    values (?,?)
                """, (jogo.nome, jogo.horasJogadas))
                jogo.id = cursor.lastrowid        
                conn.commit()

    def apagar(self, jogo):
        if isinstance(jogo, Jogador):
            with self.__conexao as conn:
                conn.execute("""
                    DELETE FROM jogo WHERE id = ?
                """,[jogo.id])
                conn.commit()    

    def atualizar(self, jogo):
        if isinstance(jogo,Jogador):
            with self.__conexao as conn:
                conn.execute("""
                    UPDATE jogo Set nome = ?, horasjogadas = ? 
                    WHERE jogo.id == ?
                """, (jogo.nome, jogo.horasjogadas, jogo.id))
            conn.commit()
    
    def consultar(self, termo_busca):
        if isinstance(termo_busca, int):
            #A consulta deve ser pelo id
            with self.__conexao as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id,nome,horasjogadas FROM jogo where id = ?
                """,[termo_busca])
                resultado = cursor.fetchone()
                if resultado:
                    jogo = Jogador(resultado[0], resultado[1], 
                    resultado[2])
                    return jogo
                else:
                    return None
        elif isinstance(termo_busca, str):
            with self.__conexao as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, nome, horasjogadas FROM jogo WHERE nome like ?
                """, ["%" + termo_busca + "%"])
                resultados = cursor.fetchall()
                if resultados:
                    listaJogadores = []
                    for resultado in resultados:
                        jogo = Jogador(resultado[0], resultado[1], 
                        resultado[2])
                        listaJogadores.append(jogo)
                    return listaJogadores
                else:
                    return []
        else:
            return None

    
    def adicionarConquista(self, id_jogo, conquista):
        if isinstance(conquista, Conquista):
            with.self__conexao as conn:
                conn.execute("""
                    INSERT INTO Jogo_Coquista(id_jogo, id_conquista) WHERE id = ?
                    VALUES(?,?)
                """,[id_jogo, id_conquista])
            conn.commit()
    
    def limparBibliotecaConquista(self, id_jogo):
        if isinstance(id_jogo, int):
            with self.__conexao as conn:
                conn.execute("""
                    DELETE FROM Jogo_Conquista WHERE id_jogo
                """,[id_jogo])
            conn.commit()

    def obterConquistaJogo(self, id_jogo):
        with self.__conexao as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_conquista from Jogo_Conquista WHERE id_jogo = ?
            """, [id_jogo])
            resultados = cursor.fetchall()
            jogoBD = JogoBD()
            listaConquistas = []

            for resultado in resultados:
                conquista = jogoBD.consultar(resultado[0])
                listaConquistas.append(conquista)
            return listaConquistas

