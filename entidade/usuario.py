from entidade.pessoa import Pessoa


class Usuario(Pessoa):

    def __init__(self, nome: str, senha: str):
        super().__init__(nome)
        if isinstance(senha, str):
            self.__senha = senha

    @property
    def senha(self):
        return self.__senha

    @senha.setter
    def senha(self, senha):
        self.__senha = senha