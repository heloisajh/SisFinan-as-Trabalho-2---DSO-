import PySimpleGUI as sg
import datetime
from limite.tela import Tela


class TelaMovimentacao(Tela):

    def __init__(self):
        self.__window = None
        self.init_opcoes()
        self.codigo = 0

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
        else:
            opcao = None

        self.close()
        return opcao

    def init_opcoes(self):

        sg.ChangeLookAndFeel('DarkGray16')
        layout = [
            [sg.Text('MOVIMENTAÇÕES', font=('Century Gothic', 25))],
            [sg.Text("Escolha uma das opções abaixo:", font=("Open Sans", 15), justification='center', size=(30, 1))],
            [sg.Button("Visualizar movimentações", font=("Open Sans", 15), size=(30, 1), key='1')],
            [sg.Button("Adicionar movimentação", font=("Open Sans", 15), size=(30, 1), key='2')],
            [sg.Button("Alterar movimentação", font=("Open Sans", 15), size=(30, 1), key='3')],
            [sg.Button("Excluir movimentação", font=("Open Sans", 15), size=(30, 1), key='4')],
            [sg.Button("Retornar", font=("Open Sans", 15), size=(30, 1), key='5')]
        ]

        self.__window = sg.Window('Movimentações', element_justification='c').Layout(layout)

    def pegar_movimentacao(self, dados_tipos, data_anterior='', valor='', nome_fornecedor_pagador='', descricao=''):
        categorias = [dado["categoria"] for dado in dados_tipos]
        tipo_mov = ['ENTRADA', 'SAIDA']

        sg.ChangeLookAndFeel('DarkGray16')
        layout = [
            [sg.Text('Insira as informações da movimentação abaixo:', font=('Open Sans', 12))],
            [sg.Text('Tipo', size=(30, 1)), sg.Combo(values=tipo_mov, key='tipo', size=(28, 1), readonly=True)],
            [sg.Text('Data (formato dd/mm/yyyy)', size=(30, 1)), sg.InputText(data_anterior, key='data', size=(30, 1))],
            [sg.Text('Valor: R$', size=(30, 1)), sg.InputText(valor, key='valor', size=(30, 1))],
            [sg.Text('Categoria', size=(30, 1)),
             sg.Combo(values=categorias, key='categoria', size=(28, 1,), readonly=True)],
            [sg.Text('Fornecedor/Pagador', size=(30, 1)),
             sg.InputText(nome_fornecedor_pagador, key='fornecedor_pagador', size=(30, 1))],
            [sg.Text('Descrição', size=(30, 1)), sg.InputText(descricao, key='descricao', size=(30, 1))],
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]

        self.__window = sg.Window('Movimentações', element_justification='c').Layout(layout)

        while True:
            button, values = self.open()

            if button == 'Cancelar' or values['data'] is None:
                self.close()
                return None

            try:
                dia, mes, ano = map(int, values['data'].split('/'))
                data = datetime.datetime(ano, mes, dia)
                if len(values['data']) != 10 or not (1 <= mes <= 12):
                    raise ValueError
            except (ValueError, IndexError):
                self.mostrar_mensagem("Por favor, digite a data no formato especificado (dd/mm/yyyy).")
                continue

            try:
                valor = float(values['valor'])
            except ValueError:
                self.mostrar_mensagem("Por favor, insira um valor numérico válido.")
                continue

            tipo = values['tipo']
            categoria = values['categoria']
            fornecedor_pagador = values['fornecedor_pagador']
            descricao = values['descricao']

            self.close()
            return {
                "valor": valor,
                "data": data,
                "descricao": descricao,
                "tipo": tipo,
                "categoria": categoria,
                "fornecedor_pagador": fornecedor_pagador
            }
    def mostrar_movimentacao(self, dados_movimentacoes):
        movimentacoes = []
        for mov in dados_movimentacoes:
            movimentacoes.append([mov['codigo'], mov['tipo'], mov['data'].strftime("%d/%m/%Y"), mov['valor'], mov['categoria'].categoria,
                         mov['fornecedor_pagador'].nome, mov['descricao']])

        movimentacoes.append(['', '', '', '', '', 'Total', dados_movimentacoes[0]['saldo']])

        sg.ChangeLookAndFeel('DarkGray16')
        layout = [
            [sg.Text('Movimentações cadastradas no sistema:', font=("Open Sans", 15))],
            [sg.Table(values=movimentacoes,
                      headings=['Código', 'Tipo', 'Data', 'Valor', 'Categoria', 'Fornecedor/Pagador', 'Descrição'],
                      auto_size_columns=True,
                      display_row_numbers=False,
                      justification='center',
                      num_rows=min(25, len(movimentacoes)),
                      key='TABLE',
                      enable_events=True)],
            [sg.Button('Confirmar')]
        ]

        self.__window = sg.Window('Movimentações registradas', layout, element_justification='c')

        while True:
            event, values = self.__window.read()
            if event == sg.WIN_CLOSED or event == 'Confirmar':
                break

        self.__window.close()

    def selecionar_movimentacao(self, dados_movimentacoes):
        movimentacoes = []
        for mov in dados_movimentacoes:
            movimentacoes.append(
                [mov['codigo'], mov['tipo'], mov['data'].strftime("%d/%m/%Y"), mov['valor'], mov['categoria'].categoria,
                 mov['fornecedor_pagador'].nome, mov['descricao']])

        sg.ChangeLookAndFeel('DarkGray16')
        layout = [
            [sg.Text('Selecione a movimentação que deseja alterar/excluir:', font=("Open Sans", 15))],
            [sg.Table(values=movimentacoes,
                      headings=['Código', 'Tipo', 'Data', 'Valor', 'Categoria', 'Fornecedor/Pagador', 'Descrição'],
                      auto_size_columns=True,
                      display_row_numbers=False,
                      justification='center',
                      num_rows=min(25, len(movimentacoes)),
                      key='TABLE',
                      enable_events=True)],
            [sg.Cancel('Cancelar')]
        ]

        self.__window = sg.Window('Selecionar movimentação', element_justification='c').Layout(layout)

        button, values = self.open()

        if button == 'Cancelar' or not values['TABLE']:
            self.close()
            return None

        selected_row_index = values['TABLE'][0]
        if selected_row_index < len(dados_movimentacoes):  # Verifica se não é a linha do saldo total
            movimentacao = {"codigo": dados_movimentacoes[selected_row_index]['codigo']}
        else:
            movimentacao = None

        self.close()
        return movimentacao

    def close(self):
        self.__window.Close()

    def open(self):
        button, values = self.__window.Read()
        return button, values

























