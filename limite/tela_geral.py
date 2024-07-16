import PySimpleGUI as sg
from limite.tela import Tela


class TelaGeral(Tela):

    def __init__(self):
        self.__window = None
        self.init_components()

    def tela_opcoes(self):
        self.init_components()
        button, values = self.__window.Read()
        opcao = 0
        if button == '1':
            opcao = 1
        if button == '2':
            opcao = 2
        if button == '3':
            opcao = 3
        if button == '4':
            opcao = 4
        if button in ('5', None):
            opcao = 5
        self.close()
        return opcao

    def close(self):
        self.__window.Close()

    def init_components(self):

        sg.ChangeLookAndFeel('DarkGray16')

        layout = [
                    [sg.Text('Olá, bem-vindo ao SisFinanças', font=("Century Gothic",25))],
                    [sg.Text('Escolha uma das opções abaixo:', font=("Open Sans",15))],
                    [sg.Button('Cadastrar orçamentos', font=("Open Sans", 15), size=(30,1), key='1')],
                    [sg.Button('Cadastrar pessoas', font=("Open Sans", 15), size=(30,1), key='2')],
                    [sg.Button('Cadastrar categorias orçamentárias', font=("Open Sans", 15), size=(30,1), key='3')],
                    [sg.Button('Registrar movimentações', font=("Open Sans", 15), size=(30,1), key='4')],
                    [sg.Button('Encerrar sistema', font=("Open Sans", 15), size=(30,1), key='5')],
        ]

        self.__window = sg.Window('SisFinanças', element_justification='c').Layout(layout)

