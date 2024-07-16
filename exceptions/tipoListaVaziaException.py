

class TipoListaVaziaException(Exception):
    def __init__(self):
        super().__init__("Você só pode visualizar suas categorias orçamentárias, se cadastrar ao menos uma categoria.")
