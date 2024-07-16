import PySimpleGUI as sg
from limite.tela import Tela

class TelaUsuario(Tela):

    def __init__(self):
        self.__window = None
        self.init_opcoes()

    def tela_opcoes(self):
        self.init_opcoes()
        button, values = self.__window.read()
        opcao = 0
        if button == '1':
            opcao = 1
        elif button == '2':
            opcao = 2
        elif button == '3':
            opcao = 3
        elif button == '4':
            opcao = 4

        self.close()
        return opcao

    def init_opcoes(self):
        sg.theme('DarkGray16')
        layout = [
            [sg.Text('SisFinanças', font=('Century Gothic', 25))],
            [sg.Button('Fazer login', size=(30, 1), key='1', font=("Century Gothic", 12))],
            [sg.Button('Esqueci a senha', size=(30, 1), key='2', font=("Century Gothic", 12))],
            [sg.Button('Sou novo usuário, quero me cadastrar', size=(30, 1), key='3', font=("Century Gothic", 12))],
            [sg.Button('Sair', size=(30,1), key='4', font=("Century Gothic", 12))]
        ]
        self.__window = sg.Window('Menu Usuário', layout, element_justification='c')

    def pegar_usuario(self):
        sg.theme('DarkGray16')
        layout = [
            [sg.Text('Nome', font=("Century Gothic", 12), size=(15, 1)), sg.InputText('', key='nome')],
            [sg.Text('Senha', font=("Century Gothic", 12), size=(15, 1)), sg.InputText('', key='senha', password_char='*')],
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]
        self.__window = sg.Window('Cadastro/Login', layout, element_justification='c')

        button, values = self.open()

        if button == 'Cancelar' or values['nome'] is None:
            self.close()
            return None

        nome = values.get('nome')
        senha = values.get('senha')
        self.close()
        return {"nome": nome, "senha": senha}

    def pegar_senha(self):
        sg.theme('DarkGray16')
        layout = [
            [sg.Text('Usuário:', font=("Century Gothic", 11), size=(15, 1)), sg.InputText('', key='nome')],
            [sg.Text('Nova Senha:', font=("Century Gothic", 11), size=(15, 1)), sg.InputText('', key='senha', password_char='*')],
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]
        self.__window = sg.Window('Nova Senha', layout, element_justification='c')

        button, values = self.open()

        if button == 'Cancelar' or values['nome'] is None:
            self.close()
            return None

        nome = values.get('nome')
        senha = values.get('senha')
        self.close()
        return {"nome": nome, "senha": senha}

    def close(self):
        if self.__window:
            self.__window.close()

    def open(self):
        button, values = self.__window.read()
        return button, values
