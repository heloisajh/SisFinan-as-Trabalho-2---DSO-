from limite.tela import Tela
import PySimpleGUI as sg


class TelaPessoa(Tela):

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
        else:
            opcao = None

        self.close()
        return opcao

    def init_opcoes(self):

        sg.ChangeLookAndFeel('DarkGray16')
        layout = [
            [sg.Text('PESSOAS', font=('Century Gothic', 25))],
            [sg.Text("Escolha uma das opções abaixo:", font=("Open Sans", 15), justification='center', size=(30, 1))],
            [sg.Button("Listar pessoas", font=("Open Sans", 15), size=(30, 1), key='1')],
            [sg.Button("Adicionar pessoas", font=("Open Sans", 15), size=(30, 1), key='2')],
            [sg.Button("Alterar pessoas", font=("Open Sans", 15), size=(30, 1), key='3')],
            [sg.Button("Excluir pessoas", font=("Open Sans", 15), size=(30, 1), key='4')],
            [sg.Button("Retornar", font=("Open Sans", 15), size=(30, 1), key='5')]
        ]

        self.__window = sg.Window('Pessoas', element_justification='c').Layout(layout)


    def pegar_pessoa(self, nome_pessoa=''):

        sg.ChangeLookAndFeel('DarkGray16')
        layout = [
            [sg.Text('Insira o novo nome da pessoa', font=("Open Sans", 12))],
            [sg.InputText(nome_pessoa, key='nome')],
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]

        self.__window = sg.Window('Pessoas', element_justification='c').Layout(layout)

        button, values = self.open()

        if button == 'Cancelar' or values['nome'] is None:
            self.close()
            return None

        nome = values['nome']

        if isinstance(nome, str) and nome:
            self.close()
            return {"nome": nome}

    def mostrar_pessoa(self, dados_pessoa):
        nomes = [dado["nome"] for dado in dados_pessoa]
        dados_nomes = [[nome] for nome in nomes]

        sg.ChangeLookAndFeel('DarkGray16')
        layout = [
            [sg.Text('Pessoas cadastradas no sistema:', font=("Open Sans", 12))],
            [sg.Table(values=dados_nomes, headings=['Nomes'], auto_size_columns=True,
                      display_row_numbers=False, justification='center',
                      num_rows=min(25, len(dados_nomes)), key='-TABLE-')],
            [sg.Button('Confirmar')]
        ]

        self.__window = sg.Window('Pessoas Cadastradas', layout, element_justification='c')

        while True:
            event, values = self.__window.read()
            if event == sg.WIN_CLOSED or event == 'Confirmar':
                break

        self.__window.close()

    def selecionar_pessoa(self, dados_pessoa):

        nomes = [dado["nome"] for dado in dados_pessoa]
        dados_nomes = [[nome] for nome in nomes]

        sg.ChangeLookAndFeel('DarkGray16')
        layout = [
            [sg.Text('Selecione a pessoa que deseja alterar/excluir:', font=("Open Sans", 12))],
            [sg.Table(values=dados_nomes, headings=['Nomes'], auto_size_columns=True,
                      display_row_numbers=False, justification='center',
                      num_rows=min(25, len(dados_nomes)), key='TABLE', enable_events=True)],
            [sg.Cancel('Cancelar')]
        ]

        self.__window = sg.Window('Selecionar pessoa', element_justification='c').Layout(layout)

        button, values = self.open()

        if button == 'Cancelar' or values['TABLE'] is None:
            self.close()
            return None

        selected_row_index = values['TABLE']
        if selected_row_index:
            pessoa = dados_nomes[selected_row_index[0]][0]
        else:
            pessoa = None

        self.close()
        return pessoa

    def close(self):
        self.__window.Close()

    def open(self):
        button, values = self.__window.Read()
        return button, values












