

class MovimentacaoListaVaziaException(Exception):
    def __init__(self):
        super().__init__("Você só pode visualizar suas movimentações, se registrar ao menos uma movimentação.")
