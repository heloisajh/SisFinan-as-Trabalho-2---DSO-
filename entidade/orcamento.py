from entidade.tipo_orcamento import TipoOrcamento
from datetime import datetime


class Orcamento:

    def __init__ (self, mes_ano: datetime, valor: float, tipo: TipoOrcamento):
        if (isinstance(mes_ano, datetime) and isinstance (valor, float) or isinstance(valor, int)
                and isinstance(tipo, TipoOrcamento)):
            self.__mes_ano = mes_ano
            self.__valor = valor
            self.__tipo = tipo
            self.__movimentacoes = []

    @property
    def mes_ano (self):
        return self.__mes_ano

    @mes_ano.setter
    def mes_ano(self, mes_ano):
        if isinstance(mes_ano, datetime):
            self.__mes_ano = mes_ano

    @property
    def valor(self):
        return self.__valor

    @valor.setter
    def valor(self, valor):
        if isinstance(valor, float):
            self.__valor = valor

    @property
    def tipo (self):
        return self.__tipo

    @tipo.setter
    def tipo(self, tipo):
        if isinstance(tipo, TipoOrcamento):
            self.__tipo = tipo

    def adicionar_movimentacao(self, movimentacao):
        self.movimentacoes.append(movimentacao)

    @property
    def movimentacoes(self):
        return self.__movimentacoes

    @movimentacoes.setter
    def movimentacoes(self, movimentacoes):
        self.__movimentacoes = movimentacoes

