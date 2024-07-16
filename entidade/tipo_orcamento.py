

class TipoOrcamento:

    def __init__(self, categoria: str):
        if isinstance(categoria, str):
            self.__categoria = categoria

    @property
    def categoria(self):
        return self.__categoria

    @categoria.setter
    def categoria(self, categoria: str):
        if isinstance(categoria, str):
            self.__categoria = categoria