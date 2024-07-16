from entidade.pessoa import Pessoa
from entidade.usuario import Usuario
from entidade.tipo_orcamento import TipoOrcamento
from datetime import datetime

class Movimentacao:

    def __init__(self, codigo: int, usuario: Usuario, valor: float, data: datetime, descricao: str,
                    tipo_movimentacao: str, categoria_movimentacao: TipoOrcamento, fornecedor_pagador: Pessoa):
        if isinstance(codigo, int):
            self.__codigo = codigo
        if isinstance(usuario, Usuario):
            self.__usuario = usuario
        if isinstance(valor, float) or isinstance(valor, int):
            self.__valor = valor
        if isinstance(data, datetime):
            self.__data = data
        if isinstance(descricao, str):
            self.__descricao = descricao
        if isinstance(tipo_movimentacao, str):
            self.__tipo_movimentacao = tipo_movimentacao
        if isinstance(categoria_movimentacao, TipoOrcamento):
            self.__categoria_movimentacao = categoria_movimentacao
        if isinstance(fornecedor_pagador, Pessoa):
            self.__fornecedor_pagador = fornecedor_pagador

    def __eq__(self, other):
        if isinstance(other, Movimentacao):
            return self.codigo == other.codigo
        return False

    def __hash__(self):
        return hash(self.codigo)

    @property
    def codigo(self):
        return self.__codigo

    @codigo.setter
    def codigo(self, codigo):
        self.__codigo = codigo

    @property
    def usuario(self):
        return self.__usuario

    @usuario.setter
    def usuario(self, usuario):
        self.__usuario = usuario


    @property
    def valor(self):
        return self.__valor

    @valor.setter
    def valor(self, valor):
        if isinstance(valor, float) or isinstance(valor, int):
            self.__valor = valor

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        if isinstance(data, datetime):
            self.__data = data

    @property
    def descricao(self):
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao):
        if isinstance(descricao, str):
            self.__descricao = descricao

    @property
    def tipo_movimentacao(self):
        return self.__tipo_movimentacao

    @tipo_movimentacao.setter
    def tipo_movimentacao(self, tipo_movimentacao):
        if isinstance(tipo_movimentacao, str):
            self.__tipo_movimentacao = tipo_movimentacao

    @property
    def categoria_movimentacao(self):
        return self.__categoria_movimentacao

    @categoria_movimentacao.setter
    def categoria_movimentacao(self, categoria_movimentacao):
        if isinstance(categoria_movimentacao, TipoOrcamento):
            self.__categoria_movimentacao = categoria_movimentacao

    @property
    def fornecedor_pagador(self):
        return self.__fornecedor_pagador

    @fornecedor_pagador.setter
    def fornecedor_pagador(self, fornecedor_pagador):
        if isinstance(fornecedor_pagador, Pessoa):
            self.__fornecedor_pagador = fornecedor_pagador
