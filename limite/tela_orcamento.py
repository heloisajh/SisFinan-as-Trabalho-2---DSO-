import datetime
from limite.tela import Tela
import PySimpleGUI as sg


class TelaOrcamento(Tela):

    def __init__(self):
        self.__window = None
        self.init_opcoes()

    def tela_opcoes(self):
        self.init_opcoes()
        button, values = self.open()
        if button == '1':
            opcao = 1
        elif button == '2':
            opcao = 2
        elif button == '3':
            opcao = 3
        elif button == '4':
            opcao = 4
        elif button == '5':
            opcao = 5
        elif button == '6':
            opcao = 6
        else:
            opcao = None

        self.close()
        return opcao

    def init_opcoes(self):

        sg.ChangeLookAndFeel('DarkGray16')
        layout = [
            [sg.Text('ORÇAMENTOS', font=('Century Gothic', 25))],
            [sg.Text("Escolha uma das opções abaixo:", font=("Open Sans", 15), justification='center', size=(30, 1))],
            [sg.Button("Listar orçamentos", font=("Open Sans", 15), size=(30, 1), key='1')],
            [sg.Button("Adicionar orçamento", font=("Open Sans", 15), size=(30, 1), key='2')],
            [sg.Button("Alterar orçamento", font=("Open Sans", 15), size=(30, 1), key='3')],
            [sg.Button("Excluir orçamento", font=("Open Sans", 15), size=(30, 1), key='4')],
            [sg.Button('Emitir relatório de metas de gastos', font=("Open Sans", 15), size=(30, 1), key='5')],
            [sg.Button("Retornar", font=("Open Sans", 15), size=(30, 1), key='6')]
        ]

        self.__window = sg.Window('Orçamentos', element_justification='c').Layout(layout)

    def pegar_orcamento(self, dados_tipos, mes_ano_anterior='', valor=''):
        categorias = [dado["categoria"] for dado in dados_tipos]

        sg.ChangeLookAndFeel('DarkGray16')
        layout = [
            [sg.Text('Insira as informações do orçamento abaixo:', font=('Open Sans', 12))],
            [sg.Text('Mês/Ano (formato mm/yyyy):', size=(30, 1)), sg.InputText(mes_ano_anterior, key='mes_ano', size=(30, 1))],
            [sg.Text('Valor: R$', size=(30, 1)), sg.InputText(valor, key='valor', size=(30, 1))],
            [sg.Text('Categoria', size=(30, 1)),
             sg.Combo(values=categorias, key='categoria', size=(28, 1,), readonly=True)],
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]

        self.__window = sg.Window('Orçamentos', element_justification='c').Layout(layout)

        while True:
            button, values = self.open()

            if button == 'Cancelar' or values['mes_ano'] is None:
                self.close()
                return None

            if button == 'Confirmar':
                try:
                    mes, ano = map(int, values['mes_ano'].split('/'))
                    if len(values['mes_ano']) != 7 or not (1 <= mes <= 12):
                        raise ValueError("Mês/Ano no formato incorreto.")
                    mes_ano = datetime.datetime(ano, mes, 1)
                except ValueError:
                    self.mostrar_mensagem("Por favor, digite o período no formato especificado (mm/yyyy).")
                    continue

                try:
                    valor = float(values['valor'])
                except ValueError:
                    self.mostrar_mensagem("Por favor, insira um valor numérico válido.")
                    continue

                tipo = values['categoria']
                self.close()
                return {"mes_ano": mes_ano, "valor": valor, "tipo": tipo}

    def mostrar_orcamento(self, dados_orcamento):
        orcamentos = []
        for orc in dados_orcamento:
            orcamentos.append([orc['mes_ano'].strftime("%m/%Y"), orc['valor'], orc['tipo'].categoria])

        sg.ChangeLookAndFeel('DarkGray16')
        layout = [
            [sg.Text('Orçamentos cadastrados no sistema:', font=("Open Sans", 15))],
            [sg.Table(values=orcamentos,
                      headings=['Mês/Ano', 'Valor', 'Categoria'],
                      auto_size_columns=True,
                      display_row_numbers=False,
                      justification='center',
                      num_rows=min(25, len(orcamentos)),
                      key='TABLE',
                      enable_events=True)],
            [sg.Button('Confirmar')]
        ]

        self.__window = sg.Window('Orçamentos Cadastradas', layout, element_justification='c')

        while True:
            event, values = self.__window.read()
            if event == sg.WIN_CLOSED or event == 'Confirmar':
                break

        self.__window.close()

    def mostrar_movimentacoes_orcamento(self, dados_movimentacoes):
        movimentacoes = []
        for mov in dados_movimentacoes:
            movimentacoes.append([
                mov['codigo'],
                mov['tipo'],
                mov['data'].strftime("%d/%m/%Y"),
                mov['valor'],
                mov['fornecedor_pagador'],
                mov['descricao']
            ])

        movimentacoes.append(['', '', '', '', 'Total Gasto', dados_movimentacoes[0]['saldo_total']])
        movimentacoes.append(['', '', '', '', 'Valor previsto', dados_movimentacoes[0]['valor_orcamento']])
        movimentacoes.append(['', '', '', '', 'Diferença', dados_movimentacoes[0]['saldo_comparado']])
        categoria = dados_movimentacoes[0]['categoria_orcamento']

        sg.ChangeLookAndFeel('DarkGray16')
        layout = [
            [sg.Text(f'Movimentações {categoria}:', font=("Open Sans", 15))],
            [sg.Table(
                values=movimentacoes,
                headings=['Código', 'Tipo', 'Data', 'Valor', 'Fornecedor/Pagador', 'Descrição'],
                auto_size_columns=True,
                display_row_numbers=False,
                justification='center',
                num_rows=min(25, len(movimentacoes)),
                key='TABLE',
                enable_events=True
            )],
            [sg.Button('Confirmar')]
        ]

        self.__window = sg.Window('Movimentações por orçamento', layout, element_justification='c')

        while True:
            event, values = self.__window.read()
            if event == sg.WIN_CLOSED or event == 'Confirmar':
                break

        self.__window.close()

    def selecionar_orcamento(self, dados_orcamento):

        orcamentos = []
        for orc in dados_orcamento:
            orcamentos.append([orc['mes_ano'].strftime("%m/%Y"), orc['valor'], orc['tipo'].categoria])

        sg.ChangeLookAndFeel('DarkGray16')
        layout = [
            [sg.Text('Orçamentos cadastrados no sistema:', font=("Open Sans", 15))],
            [sg.Table(values=orcamentos,
                      headings=['Mês/Ano', 'Valor', 'Categoria'],
                      auto_size_columns=True,
                      display_row_numbers=False,
                      justification='center',
                      num_rows=min(25, len(orcamentos)),
                      key='TABLE',
                      enable_events=True)],
            [sg.Cancel('Cancelar')]
        ]

        self.__window = sg.Window('Selecionar orçamento', layout, element_justification='c')

        button, values = self.open()

        if button == 'Cancelar' or values['TABLE'] is None:
            self.close()
            return None

        selected_row_index = values['TABLE']
        if selected_row_index:
            orcamento_selecionado = orcamentos[selected_row_index[0]]
            orcamento = {
                "mes_ano": orcamento_selecionado[0],
                "tipo": orcamento_selecionado[2]
            }
        else:
            orcamento = None

        self.close()
        return orcamento

    def close(self):
        self.__window.Close()

    def open(self):
        button, values = self.__window.Read()
        return button, values














