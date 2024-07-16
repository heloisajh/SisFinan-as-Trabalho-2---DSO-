import PySimpleGUI as sg
from abc import ABC, abstractmethod

class Tela(ABC):

    @abstractmethod
    def tela_opcoes(self):
        pass

    def ler_num_inteiro(self, mensagem: str = "", inteiros_validos: [] = None):
        while True:
            valor_lido = input(mensagem)
            try:
                inteiro = int(valor_lido)
                if inteiros_validos and inteiro not in inteiros_validos:
                    raise ValueError
                return inteiro
            except ValueError:
                print("O valor que você inseriu não é válido, por favor, digite novamente.")
                if inteiros_validos:
                    print("Por gentileza, digite apenas os números indicados no menu.")

    def mostrar_mensagem(self, msg):
        sg.popup("", msg)

