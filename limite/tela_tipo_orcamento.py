import PySimpleGUI as sg
from limite.tela import Tela

class TelaTipoOrcamento(Tela):

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
            [sg.Text('CATEGORIAS DE ORÇAMENTO', font=('Century Gothic', 25))],
            [sg.Text("Escolha uma das opções abaixo:", font=("Open Sans", 15), justification='center', size=(30, 1))],
            [sg.Button("Listar categorias", font=("Open Sans", 15), size=(30, 1), key='1')],
            [sg.Button("Adicionar categoria", font=("Open Sans", 15), size=(30, 1), key='2')],
            [sg.Button("Alterar categoria", font=("Open Sans", 15), size=(30, 1), key='3')],
            [sg.Button("Excluir categoria", font=("Open Sans", 15), size=(30, 1), key='4')],
            [sg.Button("Retornar", font=("Open Sans", 15), size=(30, 1), key='5')]
        ]

        self.__window = sg.Window('Categorias orçamentárias', element_justification='c').Layout(layout)

    def pegar_tipo(self, nome_categoria=''):

        sg.ChangeLookAndFeel('DarkGray16')
        layout = [
            [sg.Text('Insira o novo nome da categoria', font=("Open Sans", 12))],
            [sg.InputText(nome_categoria, key='categoria')],
            [sg.Button('Confirmar'), sg.Cancel('Cancelar')]
        ]

        self.__window = sg.Window('Categorias orçamentárias', element_justification='c').Layout(layout)

        button, values = self.open()

        if button == 'Cancelar' or values['categoria'] is None:
            self.close()
            return None

        categoria = values['categoria']
        if isinstance(categoria, str) and categoria:
            self.close()
            return {"categoria": categoria}

    def mostrar_tipo(self, dados_tipo):
        categorias = [dado["categoria"] for dado in dados_tipo]
        dados_categoria = [[categoria] for categoria in categorias]

        sg.ChangeLookAndFeel('DarkGray16')
        layout = [
            [sg.Text('Categorias cadastradas no sistema:', font=("Open Sans", 12))],
            [sg.Table(values=dados_categoria, headings=['Categorias'], auto_size_columns=True,
                      display_row_numbers=False, justification='center',
                      num_rows=min(25, len(dados_categoria)), key='-TABLE-')],
            [sg.Button('Confirmar')]
        ]

        self.__window = sg.Window('Categorias Cadastradas', layout, element_justification='c')

        while True:
            event, values = self.__window.read()
            if event == sg.WIN_CLOSED or event == 'Confirmar':
                break

        self.__window.close()

    def selecionar_categoria(self, dados_tipos):

        sg.ChangeLookAndFeel('DarkGray16')

        categorias = [dado["categoria"] for dado in dados_tipos]
        data = [[categoria] for categoria in categorias]

        layout = [
            [sg.Text('Selecione a categoria que deseja alterar/excluir:', font=("Open Sans", 15))],
            [sg.Table(values=data, headings=['Categorias'], auto_size_columns=True,
                      display_row_numbers=False, justification='center',
                      num_rows=min(25, len(data)), key='TABLE', enable_events=True)],
            [sg.Cancel('Cancelar')]
        ]

        self.__window = sg.Window('Selecionar categoria', element_justification='c').Layout(layout)

        button, values = self.open()

        if button == 'Cancelar' or values['TABLE'] is None:
            self.close()
            return None

        selected_row_index = values['TABLE']
        if selected_row_index:
            categoria = data[selected_row_index[0]][0]
        else:
            categoria = None

        self.close()
        return categoria

    def close(self):
        self.__window.Close()

    def open(self):
        button, values = self.__window.Read()
        return button, values


