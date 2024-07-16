from entidade.orcamento import Orcamento
from exceptions.tipoListaVaziaException import TipoListaVaziaException
from limite.tela_orcamento import TelaOrcamento
from entidade.tipo_orcamento import TipoOrcamento
from datetime import datetime
from controle.controlador_geral import ControladorGeral
from persistencia.orcamento_dao import OrcamentoDAO
from exceptions.orcamentoListaVaziaException import OrcamentoListaVaziaException



class ControladorOrcamento:

    def __init__(self, controlador_geral):
        self.__tela_orcamento = TelaOrcamento()
        self.__orcamento_dao = OrcamentoDAO()
        if isinstance(controlador_geral, ControladorGeral):
            self.__controlador_geral = controlador_geral

    def achar_orcamento(self, mes_ano: datetime, tipo: TipoOrcamento):
        if isinstance(mes_ano, datetime) and isinstance(tipo, TipoOrcamento):
            print(f"Procurando orçamento para Mês/Ano: {mes_ano}, Categoria: {tipo.categoria}")
            for orcamento in self.__orcamento_dao.get_all():
                print(f"Comparando com: Mês/Ano: {orcamento.mes_ano}, Categoria: {orcamento.tipo.categoria}")
                if orcamento.mes_ano == mes_ano and orcamento.tipo.categoria == tipo.categoria:
                    return orcamento
        return None

    def listar_todos_orcamentos(self):
        dados_orcamentos = []
        if self.__orcamento_dao.get_all():
            for orcamento in self.__orcamento_dao.get_all():
                print(orcamento)
                dados_orcamentos.append({'mes_ano': orcamento.mes_ano, 'tipo': orcamento.tipo,
                                         'valor': orcamento.valor})
            return dados_orcamentos
        else:
            raise OrcamentoListaVaziaException

    def listar_orcamento(self):
        try:
            dados_orcamentos = self.listar_todos_orcamentos()
            self.__tela_orcamento.mostrar_orcamento(dados_orcamentos)
        except OrcamentoListaVaziaException:
            self.__tela_orcamento.mostrar_mensagem(
                "Você só pode visualizar seus orçamentos, se cadastrar ao menos um orçamento."
            )

    def listar_movimentacoes_orcamento(self):
        try:
            dados_orcamentos = self.listar_todos_orcamentos()
        except OrcamentoListaVaziaException:
            self.__tela_orcamento.mostrar_mensagem(
                "Você só pode visualizar seus orçamentos, se cadastrar ao menos um orçamento.")
            return

        orcamento_selecionado = self.__tela_orcamento.selecionar_orcamento(dados_orcamentos)
        if orcamento_selecionado is None:
            return

        mes_ano_selecionado = orcamento_selecionado["mes_ano"]
        tipo_selecionado = orcamento_selecionado["tipo"]

        # Convertendo mes_ano_selecionado para datetime
        mes, ano = map(int, mes_ano_selecionado.split('/'))
        mes_ano = datetime(ano, mes, 1)

        tipo_orcamento = self.__controlador_geral.controlador_tipo_orcamento.achar_tipo(tipo_selecionado)
        orcamento = self.achar_orcamento(mes_ano, tipo_orcamento)

        if orcamento is None:
            self.__tela_orcamento.mostrar_mensagem("Orçamento não encontrado.")
            return

        dados_saldos = self.comparar_saldos(orcamento)
        saldo_categoria = dados_saldos["saldo_categoria"]
        saldo_comparado = dados_saldos["saldo_comparado"]
        movimentacoes_orcamento = orcamento.movimentacoes

        if movimentacoes_orcamento:
            dados_movimentacoes = []
            for movimentacao in movimentacoes_orcamento:
                dados_movimentacoes.append({
                    "codigo": movimentacao.codigo,
                    "valor": movimentacao.valor,
                    "data": movimentacao.data,
                    "descricao": movimentacao.descricao,
                    "tipo": movimentacao.tipo_movimentacao,
                    "fornecedor_pagador": movimentacao.fornecedor_pagador.nome,
                    "saldo_total": saldo_categoria,
                    "valor_orcamento": orcamento.valor,
                    "saldo_comparado": saldo_comparado,
                    "categoria_orcamento": orcamento.tipo.categoria
                })

            self.__tela_orcamento.mostrar_movimentacoes_orcamento(dados_movimentacoes)

            if saldo_comparado >= 0:
                self.__tela_orcamento.mostrar_mensagem("Meta cumprida com sucesso!")
            else:
                self.__tela_orcamento.mostrar_mensagem(
                    "Parece que a meta esperada não foi alcançada..."
                    "Que tal olhar as suas movimentações "
                    "para uma visão mais detalhada sobre o que aconteceu?"
                    "A responsabilidade financeira é "
                    "um dos pilares para a qualidade de vida e para um futuro próspero!")
        else:
            self.__tela_orcamento.mostrar_mensagem(
                "Parece que não há nenhuma movimentação registrada para esta categoria..."
                "Por gentileza, primeiramente, registre-as no menu 'Registrar movimentações'.")

    def adicionar_orcamento(self):
        try:
            dados_tipos = self.__controlador_geral.controlador_tipo_orcamento.listar_todos_tipos()
        except TipoListaVaziaException:
            self.__tela_orcamento.mostrar_mensagem("Cadastre ao menos uma categoria orçamentária.")
            return

        dados_orcamento = self.__tela_orcamento.pegar_orcamento(dados_tipos)
        if dados_orcamento is None:
            return
        tipo = dados_orcamento["tipo"]
        t = self.__controlador_geral.controlador_tipo_orcamento.adicionar_categoria(tipo)
        if t is None:
            self.__tela_orcamento.mostrar_mensagem("Tipo de orçamento inválido.")
            return
        o = self.achar_orcamento(dados_orcamento["mes_ano"], t)
        if o is None:
            orc = Orcamento(dados_orcamento["mes_ano"], dados_orcamento["valor"], t)
            self.__orcamento_dao.add(orc)
            print(orc)
            print(self.__orcamento_dao.get_all())
            self.__tela_orcamento.mostrar_mensagem("Orçamento adicionado com sucesso.")
        else:
            self.__tela_orcamento.mostrar_mensagem("Não é possível adicionar mais um orçamento para esta categoria.")

    def excluir_orcamento(self):
        try:
            dados_orcamentos = self.listar_todos_orcamentos()
        except OrcamentoListaVaziaException:
            self.__tela_orcamento.mostrar_mensagem(
                "Você só pode visualizar seus orçamentos, se cadastrar ao menos um orçamento.")
            return

        orcamento_selecionado = self.__tela_orcamento.selecionar_orcamento(dados_orcamentos)
        if orcamento_selecionado is None:
            return

        mes_ano_selecionado = orcamento_selecionado["mes_ano"]
        tipo_selecionado = orcamento_selecionado["tipo"]

        # Convertendo mes_ano_selecionado para datetime
        mes, ano = map(int, mes_ano_selecionado.split('/'))
        mes_ano = datetime(ano, mes, 1)

        tipo_orcamento = self.__controlador_geral.controlador_tipo_orcamento.achar_tipo(tipo_selecionado)
        orcamento = self.achar_orcamento(mes_ano, tipo_orcamento)

        if orcamento is not None:
            self.__orcamento_dao.remove(orcamento)
            self.__tela_orcamento.mostrar_mensagem("Orçamento excluído com sucesso.")
            self.listar_orcamento()
        else:
            self.__tela_orcamento.mostrar_mensagem("Não é possível excluir um orçamento inexistente.")

    def excluir_orcamento_associado_categoria(self, tipo):
        if isinstance(tipo, TipoOrcamento):
            orcamentos_para_remover = []

            for orcamento in self.__orcamento_dao.get_all():
                if orcamento.tipo.categoria == tipo.categoria:
                    orcamentos_para_remover.append(orcamento)

            for orcamento in orcamentos_para_remover:
                self.__orcamento_dao.remove(orcamento)

    def alterar_orcamento(self):
        try:
            dados_orcamentos = self.listar_todos_orcamentos()
        except OrcamentoListaVaziaException:
            self.__tela_orcamento.mostrar_mensagem(
                "Você só pode visualizar seus orçamentos, se cadastrar ao menos um orçamento.")
            return

        orcamento_selecionado = self.__tela_orcamento.selecionar_orcamento(dados_orcamentos)
        if orcamento_selecionado is None:
            return

        mes_ano_selecionado = orcamento_selecionado["mes_ano"]
        tipo_selecionado = orcamento_selecionado["tipo"]

        # Convertendo mes_ano_selecionado para datetime
        mes, ano = map(int, mes_ano_selecionado.split('/'))
        mes_ano = datetime(ano, mes, 1)

        tipo_orcamento = self.__controlador_geral.controlador_tipo_orcamento.achar_tipo(tipo_selecionado)
        orcamento = self.achar_orcamento(mes_ano, tipo_orcamento)

        if orcamento is not None:
            try:
                dados_tipos = self.__controlador_geral.controlador_tipo_orcamento.listar_todos_tipos()
            except TipoListaVaziaException:
                self.__tela_orcamento.mostrar_mensagem("Cadastre ao menos uma categoria orçamentária.")
                return

            dados_novo_orcamento = self.__tela_orcamento.pegar_orcamento(dados_tipos, orcamento.mes_ano,
                                                                         orcamento.valor)
            if dados_novo_orcamento is not None:
                orcamento.valor = dados_novo_orcamento['valor']
                orcamento.mes_ano = dados_novo_orcamento['mes_ano']
                novo_tipo = dados_novo_orcamento['tipo']
                tipo = self.__controlador_geral.controlador_tipo_orcamento.achar_categoria(novo_tipo)
                if tipo is not None:
                    orcamento.tipo = tipo
                self.__orcamento_dao.add(orcamento)  # Salva o orçamento atualizado
                self.__tela_orcamento.mostrar_mensagem("Orçamento alterado com sucesso.")
        else:
            self.__tela_orcamento.mostrar_mensagem("Não é possível alterar um orçamento inexistente.")

    def adicionar_movimentacoes(self, movimentacao):
        print(
            f"Tentando adicionar movimentação: {movimentacao.codigo} para {movimentacao.data} e {movimentacao.categoria_movimentacao.categoria}")
        for orcamento in self.__orcamento_dao.get_all():
            print(f"Verificando orçamento: {orcamento.tipo.categoria} para {orcamento.mes_ano}")
            if (movimentacao.data.year == orcamento.mes_ano.year and
                    movimentacao.data.month == orcamento.mes_ano.month and
                    orcamento.tipo.categoria == movimentacao.categoria_movimentacao.categoria):

                ids_movimentacoes_adicionadas = {m.codigo for m in orcamento.movimentacoes}
                if movimentacao.codigo not in ids_movimentacoes_adicionadas:
                    orcamento.adicionar_movimentacao(movimentacao)
                    self.__orcamento_dao.add(orcamento)  # Salva o orçamento atualizado
                    print("Movimentação adicionada com sucesso.")
                    return movimentacao
        print("Nenhum orçamento encontrado correspondente.")
        return None

    def excluir_movimentacoes(self, movimentacao):
        print("Iniciando a exclusão da movimentação do orçamento...")
        for orcamento in self.__orcamento_dao.get_all():
            print(f"Verificando orçamento: {orcamento}")
            if movimentacao.data.year == orcamento.mes_ano.year and movimentacao.data.month == orcamento.mes_ano.month and orcamento.tipo.categoria == movimentacao.categoria_movimentacao.categoria:
                print(f"Orçamento correspondente encontrado: {orcamento}")
                for mov in orcamento.movimentacoes:
                    print(f"Comparando movimentação: {mov.codigo} com {movimentacao.codigo}")
                    if mov == movimentacao:
                        print(f"Movimentação encontrada no orçamento: {movimentacao}")
                        orcamento.movimentacoes.remove(mov)
                        self.__orcamento_dao.add(orcamento)  # Salva o orçamento atualizado
                        print("Movimentação removida e orçamento atualizado.")
                        return movimentacao
                print("Movimentação não encontrada no orçamento.")
        print("Movimentação não encontrada em nenhum orçamento.")
        return None

    def encontrar_orcamento_com_movimentacao(self, movimentacao):
        for orcamento in self.__orcamento_dao.get_all():
            if movimentacao in orcamento.movimentacoes:
                return orcamento
        return None

    def atualizar_movimentacao_no_orcamento(self, orcamento, movimentacao):
        print("Iniciando a atualização da movimentação no orçamento...")
        print(f"Verificando orçamento: {orcamento}")
        for mov in orcamento.movimentacoes:
            print(f"Comparando movimentação: {mov.codigo} com {movimentacao.codigo}")
            if mov.codigo == movimentacao.codigo:
                print(f"Movimentação encontrada no orçamento: {movimentacao}")
                mov.valor = movimentacao.valor
                mov.data = movimentacao.data
                mov.descricao = movimentacao.descricao
                mov.tipo_movimentacao = movimentacao.tipo_movimentacao
                mov.categoria_movimentacao = movimentacao.categoria_movimentacao
                mov.fornecedor_pagador = movimentacao.fornecedor_pagador
                self.__orcamento_dao.add(orcamento)  # Salva o orçamento atualizado
                print("Movimentação atualizada no orçamento.")
                return True
        print("Movimentação não encontrada no orçamento.")
        return False

    def comparar_saldos(self, orcamento):
        movimentacoes_orcamento = orcamento.movimentacoes
        saldo_categoria = 0
        for m in movimentacoes_orcamento:
            if m.tipo_movimentacao == 'ENTRADA':
                saldo_categoria += m.valor
            else:
                saldo_categoria -= m.valor
        saldo_comparado = orcamento.valor - abs(saldo_categoria)
        return {"saldo_categoria": saldo_categoria, "saldo_comparado": saldo_comparado}

    def retornar(self):
        self.__controlador_geral.abrir_tela()

    def abrir_tela(self):
        lista_opcoes = {1: self.listar_orcamento, 2: self.adicionar_orcamento,
                            3: self.alterar_orcamento, 4: self.excluir_orcamento,
                            5: self.listar_movimentacoes_orcamento, 6: self.retornar}
        continua = True
        while continua:
            opcao = self.__tela_orcamento.tela_opcoes()
            if opcao is None or opcao not in lista_opcoes:
                self.retornar()
                break
            lista_opcoes[opcao]()















