
class Conquista(object):

    def __init__(self, idConquista=0, nomeConquista="", objetivoConquista=""):
        self.__idConquista= idConquista
        self.__nomeConquista = nomeConquista
        self.__objetivoConquista = objetivoConquista

    @property
    def id(self):
        return self.__idConquista
    
    @id.setter
    def id(self,novoIdConquista):
        self.__idConquista = novoIdConquista

    @property
    def nomeConquista(self):
        return self.__nomeConquista
    
    @nomeConquista.setter
    def nome(self,novoNomeConquista):
        self.__nomeConquista = novoNomeConquista
    
    @property
    def objetivo(self):
        return self.objetivoConquista
    
    @objetivo.setter
    def conquistas(self, novoObjetivo):
        self.objetivoConquista = novoObjetivo


    def toJson(self):
        return {
            "id": self.__idConquista,
            "nome": self.__nomeConquista,
            "objetivo": self.__objetivoConquista
        }