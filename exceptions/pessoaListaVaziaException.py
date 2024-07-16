

class PessoaListaVaziaException(Exception):
    def __init__(self):
        super().__init__("Você só pode visualizar suas pessoas, se cadastrar ao menos uma pessoa.")
