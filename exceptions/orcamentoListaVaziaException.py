

class OrcamentoListaVaziaException(Exception):
    def __init__(self):
        super().__init__("Você só pode visualizar seus orçamentos, se cadastrar ao menos um.")
