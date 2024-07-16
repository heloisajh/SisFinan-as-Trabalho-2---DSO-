from limite.tela_pessoa import TelaPessoa
from entidade.pessoa import Pessoa
from controle.controlador_geral import ControladorGeral
from persistencia.pessoa_dao import PessoaDAO
from exceptions.pessoaListaVaziaException import PessoaListaVaziaException


class ControladorPessoa:

    def __init__(self, controlador_geral):
        self.__pessoa_dao = PessoaDAO()
        if isinstance(controlador_geral, ControladorGeral):
            self.__controlador_geral = controlador_geral
        self.__tela_pessoa = TelaPessoa()

    def achar_pessoa(self, nome: str):
        for pessoa in self.__pessoa_dao.get_all():
            if(nome is not None and pessoa.nome == nome):
                return pessoa
        return None

    def listar_pessoa(self):
        try:
            dados_pessoa = self.listar_todas_pessoas()
            self.__tela_pessoa.mostrar_pessoa(dados_pessoa)
        except PessoaListaVaziaException:
            self.__tela_pessoa.mostrar_mensagem("Você só pode visualizar suas pessoas, "
                                                "se cadastrar ao menos uma pessoa.")

    def listar_todas_pessoas(self):
        if self.__pessoa_dao.get_all():
            return [{'nome': pessoa.nome} for pessoa in self.__pessoa_dao.get_all()]
        else:
            raise PessoaListaVaziaException

    def adicionar_pessoa(self):
        dados_pessoa = self.__tela_pessoa.pegar_pessoa()
        if dados_pessoa is None:
            return
        p = self.achar_pessoa(dados_pessoa["nome"])
        if p is None:
            pessoa = Pessoa(dados_pessoa["nome"])
            self.__pessoa_dao.add(pessoa)
            self.__tela_pessoa.mostrar_mensagem("Pessoa adicionada com sucesso.")
        else:
            self.__tela_pessoa.mostrar_mensagem("Não é possível adicionar uma pessoa já cadastrada.")

    def adicionar_fornecedor_pagador(self, nome): #Uso para controlador movimentação
        p = self.achar_pessoa(nome)
        if p is None:
            pessoa = Pessoa(nome)
            self.__pessoa_dao.add(pessoa)
            return pessoa
        return p

    def excluir_pessoa(self):
        try:
            dados_pessoa = self.listar_todas_pessoas()
        except PessoaListaVaziaException:
            self.__tela_pessoa.mostrar_mensagem("Você só pode visualizar suas pessoas, "
                                                "se cadastrar ao menos uma pessoa.")
            return
        pessoa_selecionada = self.__tela_pessoa.selecionar_pessoa(dados_pessoa)
        if pessoa_selecionada is None:
            return
        pessoa = self.achar_pessoa(pessoa_selecionada)

        if pessoa is not None:
            self.__pessoa_dao.remove(pessoa)
            self.__tela_pessoa.mostrar_mensagem("'Pessoa' excluída com sucesso.")
            self.listar_pessoa()
        else:
            self.__tela_pessoa.mostrar_mensagem("Não é possível excluir uma pessoa inexistente")

    def alterar_pessoa(self):
        try:
            dados_pessoa = self.listar_todas_pessoas()
        except PessoaListaVaziaException:
            self.__tela_pessoa.mostrar_mensagem("Você só pode visualizar suas pessoas, "
                                                "se cadastrar ao menos uma pessoa.")
            return
        pessoa_selecionada = self.__tela_pessoa.selecionar_pessoa(dados_pessoa)
        if pessoa_selecionada is None:
            return
        pessoa = self.achar_pessoa(pessoa_selecionada)

        if pessoa is not None:
            nova_pessoa = self.__tela_pessoa.pegar_pessoa()
            pessoa.nome = nova_pessoa["nome"]
            self.__tela_pessoa.mostrar_mensagem("Pessoa alterada com sucesso.")
            self.listar_pessoa()
        else:
            self.__tela_pessoa.mostrar_mensagem("Não é possível alterar uma pessoa inexistente.")

    def alterar_fornecedor_pagador(self, nome): #Uso para controlador movimentação
        pessoa = self.achar_pessoa(nome)
        if pessoa is None:
            nova_pessoa = Pessoa(nome)
            self.__pessoa_dao.add(nova_pessoa)
            return nova_pessoa
        else:
            return pessoa

    def retornar(self):
        self.__controlador_geral.abrir_tela()

    def abrir_tela(self):
        lista_opcoes = {1: self.listar_pessoa, 2: self.adicionar_pessoa, 3: self.alterar_pessoa,
                            4: self.excluir_pessoa, 5: self.retornar}
        continua = True
        while continua:
            opcao = self.__tela_pessoa.tela_opcoes()
            if opcao is None or opcao not in lista_opcoes:
                self.retornar()
                break
            lista_opcoes[opcao]()