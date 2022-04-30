from Modelo.Jogador import Jogador
from Modelo.Jogo import Jogo
from Persistencia.JogoBD import JogoBD
import sqlite3

caminhoBancoDados = './BancoDeDados/Dados2.db'

class JogadorBD(object):
    
    def __init__(self):
        self.__conexao = sqlite3.connect(caminhoBancoDados)
        with self.__conexao as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS Jogador(
                    id integer not null primary key autoincrement,
                    nome text not null,
                    dataNasc text not null,
                    apelido text not null
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS Jogador_Jogo(
                    id_jogador integer not null,
                    id_jogo integer not null,
                    data_ultimo_acesso text,
                    PRIMARY KEY(id_jogador, id_jogo),
                    FOREIGN KEY (id_jogador) REFERENCES Jogador (id),
                    FOREIGN KEY (id_jogo) REFERENCES Jogo (id)
                )
            """)
            conn.commit()

    def incluir(self, jogador):
        if isinstance(jogador,Jogador):
            with self.__conexao as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO jogador(nome, dataNasc, apelido) 
                    values (?,?,?)
                """, (jogador.nome, jogador.dataNasc, jogador.apelido))
                jogador.id = cursor.lastrowid 
                for jogo in jogador.bibliotecaJogos:
                    self.adicionarJogo(jogador.id, jogo)
                conn.commit()

    def apagar(self, jogador):
        if isinstance(jogador, Jogador):
            with self.__conexao as conn:
                conn.execute("""
                    DELETE FROM jogador WHERE id = ?
                """,[jogador.id])
                self.limparBibliotecaJogos(jogador.id)
                conn.commit()    

    def atualizar(self, jogador):
        if isinstance(jogador,Jogador):
            with self.__conexao as conn:
                conn.execute("""
                    UPDATE jogador Set nome = ?, dataNasc = ?, apelido = ? 
                    WHERE jogador.id == ?
                """, (jogador.nome, jogador.dataNasc, jogador.apelido, jogador.id))
                self.limparBibliotecaJogos(jogador.id)
                for jogo in jogador.bibliotecaJogos:
                    self.adicionarJogo(jogador.id, jogo)
            conn.commit()
    
    def consultar(self, termo_busca):
        if isinstance(termo_busca, int):
            #A consulta deve ser pelo id
            with self.__conexao as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id,nome,dataNasc,apelido FROM jogador where id = ?
                """,[termo_busca])
                resultado = cursor.fetchone()
                if resultado:
                    jogador = Jogador(resultado[0], resultado[1], 
                    resultado[2], resultado[3])
                    jogador.bibliotecaJogos = self.obterJogosDoJogador(jogador.id)
                    return jogador
                else:
                    return None
        elif isinstance(termo_busca, str):
            with self.__conexao as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, nome, dataNasc, apelido FROM jogador WHERE nome like ?
                """, ["%" + termo_busca + "%"])
                resultados = cursor.fetchall()
                if resultados:
                    listaJogadores = []
                    for resultado in resultados:
                        jogador = Jogador(resultado[0], resultado[1], 
                        resultado[2], resultado[3])
                        jogador.bibliotecaJogos = self.obterJogosDoJogador(jogador.id)
                        listaJogadores.append(jogador)
                    return listaJogadores
                else:
                    return []
        else:
            return None


    def adicionarJogo(self, id_jogador, jogo):
       if isinstance(jogo, Jogo) and id_jogador:
           with self.__conexao as conn:
               conn.execute("""
                   INSERT INTO Jogador_Jogo(id_jogador, id_jogo)
                   VALUES (?,?)
               """, [id_jogador, jogo.id])
               conn.commit()

    def limparBibliotecaJogos(self, id_jogador):
        if isinstance(id_jogador, int):
            with self.__conexao as conn:
                conn.execute("""
                    DELETE FROM Jogador_Jogo WHERE id_jogador = ?
                """,[id_jogador])
            conn.commit()

    def obterJogosDoJogador(self, id_jogador):
        with self.__conexao as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_jogo FROM Jogador_Jogo WHERE id_jogador = ?
            """,[id_jogador])

        resultados = cursor.fetchall()

        jogoBD = JogoBD()
        listaJogos = []
        for resultado in resultados:
            jogoBD.consulta(resultado[0]) # resultado[0] é o id do jogo    
            listaJogos.append(jogo)
        
        return listaJogos


    def obterConquistasDoJogador(self, id_jogador):
        jogos = self.obterJogosDoJogador()
        conquistasDoJogador = []

        for jogo in jogos:
            for conquista in jogo.conquistas:
                conquistasDoJogador.append(conquista)
        
        return conquistasDoJogador
