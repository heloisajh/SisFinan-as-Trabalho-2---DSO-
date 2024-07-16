from limite.tela_movimentacao import TelaMovimentacao
from entidade.movimentacao import Movimentacao
from controle.controlador_geral import ControladorGeral
from persistencia.movimentacao_dao import MovimentacaoDAO
from exceptions.movimentacaoListaVaziaException import MovimentacaoListaVaziaException
from exceptions.tipoListaVaziaException import TipoListaVaziaException


class ControladorMovimentacao:

    def __init__(self, controlador_geral: ControladorGeral):
        self.__tela_movimentacao = TelaMovimentacao()
        self.__movimentacao_dao = MovimentacaoDAO()
        if isinstance(controlador_geral, ControladorGeral):
            self.__controlador_geral = controlador_geral
        self.__saldo_total_atualizado = False
        self.saldo_categoria = 0
        self.saldo_total = 0
        self.calcular_saldo_total()

    def achar_movimentacao(self, codigo):
        if isinstance(codigo, int):
            for movimentacao in self.__movimentacao_dao.get_all():
                if movimentacao.codigo == codigo:
                    return movimentacao
            else:
                return None

    def listar_todas_movimentacoes(self):
        dados_movimentacoes = []
        if self.__movimentacao_dao.get_all():
            for movimentacao in self.__movimentacao_dao.get_all():
                dados_movimentacoes.append({'codigo': movimentacao.codigo, 'tipo': movimentacao.tipo_movimentacao,
                                            'data': movimentacao.data, 'valor': movimentacao.valor, 'categoria':
                                            movimentacao.categoria_movimentacao, 'fornecedor_pagador': movimentacao.fornecedor_pagador,
                                            'descricao': movimentacao.descricao, "saldo": self.saldo_total})
            return dados_movimentacoes
        else:
            raise MovimentacaoListaVaziaException

    def listar_movimentacao(self):
        try:
            dados_movimentacoes = self.listar_todas_movimentacoes()
            self.__tela_movimentacao.mostrar_movimentacao(dados_movimentacoes)
        except MovimentacaoListaVaziaException:
            self.__tela_movimentacao.mostrar_mensagem(
                "Você só pode visualizar suas movimentações, se registrar ao menos uma movimentação.")

    def adicionar_movimentacao(self):
        try:
            dados_tipos = self.__controlador_geral.controlador_tipo_orcamento.listar_todos_tipos()
        except TipoListaVaziaException:
            self.__tela_movimentacao.mostrar_mensagem("Cadastre ao menos uma categoria orçamentária.")
            return

        dados_movimentacao = self.__tela_movimentacao.pegar_movimentacao(dados_tipos)
        if dados_movimentacao is None:
            return
        codigo = self.__movimentacao_dao.gerar_codigo()
        dados_movimentacao["codigo"] = codigo
        categoria_usuario = dados_movimentacao["categoria"]
        categoria = self.__controlador_geral.controlador_tipo_orcamento.achar_categoria(categoria_usuario)
        if categoria is not None:
            usuario = self.__controlador_geral.usuario_logado
            pessoa = dados_movimentacao["fornecedor_pagador"]
            pes = self.__controlador_geral.controlador_pessoa.adicionar_fornecedor_pagador(pessoa)
            mov = Movimentacao(dados_movimentacao["codigo"], usuario, dados_movimentacao["valor"],
                               dados_movimentacao["data"], dados_movimentacao["descricao"],
                               dados_movimentacao["tipo"], categoria, pes)
            movimentacao_orcamento = self.__controlador_geral.controlador_orcamento.adicionar_movimentacoes(mov)

            if movimentacao_orcamento is not None:
                self.__movimentacao_dao.add(mov)
                self.__saldo_total_atualizado = False
                self.calcular_saldo_total()
                self.__tela_movimentacao.mostrar_mensagem(f"Movimentação {mov.codigo} adicionada com sucesso.")
                self.calcular_saldo_total()
            else:
                self.__tela_movimentacao.mostrar_mensagem("Por favor, cadastre um orçamento primeiro.")
        else:
            self.__tela_movimentacao.mostrar_mensagem(
                "Categoria não encontrada, por favor, cadastre-as no menu 'Cadastrar categorias orçamentárias'.")

    def excluir_movimentacao(self):
        try:
            dados_movimentacoes = self.listar_todas_movimentacoes()
        except MovimentacaoListaVaziaException:
            self.__tela_movimentacao.mostrar_mensagem(
                "Você só pode visualizar suas movimentações, se registrar ao menos uma movimentação.")
            return

        movimentacao_selecionada = self.__tela_movimentacao.selecionar_movimentacao(dados_movimentacoes)
        if movimentacao_selecionada is None:
            return
        codigo_movimentacao = movimentacao_selecionada['codigo']
        movimentacao = self.achar_movimentacao(codigo_movimentacao)
        if movimentacao is not None:
            movimentacao_orcamento = self.__controlador_geral.controlador_orcamento.excluir_movimentacoes(movimentacao)
            if movimentacao_orcamento is not None:
                self.__movimentacao_dao.remove(movimentacao)
                self.__saldo_total_atualizado = False
                self.calcular_saldo_total()
                self.__tela_movimentacao.mostrar_mensagem("Movimentação excluída com sucesso.")
                self.listar_movimentacao()
            else:
                self.__tela_movimentacao.mostrar_mensagem("Erro ao excluir movimentação do orçamento.")
        else:
            self.__tela_movimentacao.mostrar_mensagem("Não é possível excluir uma movimentação inexistente.")

    def alterar_movimentacao(self):
        try:
            dados_movimentacoes = self.listar_todas_movimentacoes()
        except MovimentacaoListaVaziaException:
            self.__tela_movimentacao.mostrar_mensagem(
                "Você só pode visualizar suas movimentações, se registrar ao menos uma movimentação.")
            return

        movimentacao_selecionada = self.__tela_movimentacao.selecionar_movimentacao(dados_movimentacoes)
        if movimentacao_selecionada is None:
            return

        codigo_movimentacao = movimentacao_selecionada['codigo']
        movimentacao = self.achar_movimentacao(codigo_movimentacao)

        if movimentacao is not None:
            try:
                dados_tipos = self.__controlador_geral.controlador_tipo_orcamento.listar_todos_tipos()
            except TipoListaVaziaException:
                self.__tela_movimentacao.mostrar_mensagem("Cadastre ao menos uma categoria orçamentária.")
                return

            dados_nova_movimentacao = self.__tela_movimentacao.pegar_movimentacao(
                dados_tipos, movimentacao.data.strftime("%d/%m/%Y"), movimentacao.valor,
                movimentacao.fornecedor_pagador.nome, movimentacao.descricao)

            if dados_nova_movimentacao is not None:
                # Atualiza os dados da movimentação
                movimentacao.valor = dados_nova_movimentacao['valor']
                movimentacao.data = dados_nova_movimentacao['data']
                movimentacao.descricao = dados_nova_movimentacao['descricao']
                movimentacao.tipo_movimentacao = dados_nova_movimentacao['tipo']

                nova_categoria = dados_nova_movimentacao['categoria']
                categoria = self.__controlador_geral.controlador_tipo_orcamento.achar_categoria(nova_categoria)
                if categoria is not None:
                    movimentacao.categoria_movimentacao = categoria

                novo_fornecedor_pagador = dados_nova_movimentacao['fornecedor_pagador']
                fornecedor_pagador = self.__controlador_geral.controlador_pessoa.alterar_fornecedor_pagador(
                    novo_fornecedor_pagador)
                movimentacao.fornecedor_pagador = fornecedor_pagador

                # Persiste a movimentação alterada no DAO de movimentações
                self.__movimentacao_dao.add(movimentacao)

                # Atualiza automaticamente no orçamento correspondente
                orcamento_contendo_movimentacao = self.__controlador_geral.controlador_orcamento.encontrar_orcamento_com_movimentacao(
                    movimentacao)
                if orcamento_contendo_movimentacao is not None:
                    self.__controlador_geral.controlador_orcamento.atualizar_movimentacao_no_orcamento(
                        orcamento_contendo_movimentacao, movimentacao)

                self.__saldo_total_atualizado = False
                self.calcular_saldo_total()

                self.__tela_movimentacao.mostrar_mensagem("A movimentação foi alterada com sucesso.")
            else:
                self.__tela_movimentacao.mostrar_mensagem("Os dados da nova movimentação são inválidos.")
        else:
            self.__tela_movimentacao.mostrar_mensagem("Não é possível alterar uma movimentação inexistente.")

    def calcular_saldo_total(self):
        if not self.__saldo_total_atualizado:
            # Limpe o saldo total antes de recalculá-lo
            self.saldo_total = 0
            for mov in self.__movimentacao_dao.get_all():
                if mov.tipo_movimentacao == "ENTRADA":
                    self.saldo_total += mov.valor
                elif mov.tipo_movimentacao == "SAIDA" or mov.tipo_movimentacao == "SAÍDA":
                    self.saldo_total -= mov.valor
            self.__saldo_total_atualizado = True

    def retornar(self):
        self.__controlador_geral.abrir_tela()

    def abrir_tela(self):
        lista_opcoes = {1: self.listar_movimentacao, 2: self.adicionar_movimentacao,
                            3: self.alterar_movimentacao, 4: self.excluir_movimentacao,
                            5: self.retornar}
        continua = True
        while continua:
            opcao = self.__tela_movimentacao.tela_opcoes()
            if opcao is None or opcao not in lista_opcoes:
                self.retornar()
                break
            lista_opcoes[opcao]()





