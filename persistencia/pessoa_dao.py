from persistencia.dao import DAO
from entidade.pessoa import Pessoa

class PessoaDAO(DAO):

    __instance = None

    def __init__(self):
        super().__init__('pessoa.pkl')

    def __new__(cls):
        if PessoaDAO.__instance is None:
            PessoaDAO.__instance = object.__new__(cls)
        return PessoaDAO.__instance

    def add(self, pessoa: Pessoa):
        if isinstance(pessoa, Pessoa):
            super().add(pessoa.nome, pessoa)

    def get(self, pessoa: Pessoa):
        if isinstance(pessoa, Pessoa):
            return super().get(pessoa.nome)

    def remove(self, pessoa: Pessoa):
        if isinstance(pessoa, Pessoa):
            super().remove(pessoa.nome)