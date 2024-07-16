from persistencia.dao import DAO
from entidade.tipo_orcamento import TipoOrcamento


class TipoOrcamentoDAO(DAO):

    __instance = None

    def __init__(self):
        super().__init__('tipos.pkl')

    def __new__(cls):
        if TipoOrcamentoDAO.__instance is None:
            TipoOrcamentoDAO.__instance = object.__new__(cls)
        return TipoOrcamentoDAO.__instance

    def add(self, tipo: TipoOrcamento):
        if (isinstance(tipo.categoria, str) and (tipo is not None)
                and isinstance(tipo, TipoOrcamento)):
            super().add(tipo.categoria, tipo)

    def get(self, tipo: TipoOrcamento):
        if isinstance(tipo, TipoOrcamento):
            return super().get(tipo.categoria)

    def remove(self, tipo: TipoOrcamento):
        if isinstance(tipo, TipoOrcamento):
            super().remove(tipo.categoria)
