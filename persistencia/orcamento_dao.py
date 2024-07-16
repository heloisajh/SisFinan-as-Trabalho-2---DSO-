from persistencia.dao import DAO
from entidade.orcamento import Orcamento
from datetime import datetime
from persistencia.movimentacao_dao import MovimentacaoDAO
from persistencia.tipo_orcamento_dao import TipoOrcamentoDAO


class OrcamentoDAO(DAO):

    def __init__(self):
        super().__init__('orcamentos.pkl')

    def add(self, orcamento: Orcamento):
        if orcamento is not None and (isinstance(orcamento, Orcamento)
                                      and isinstance(orcamento.tipo.categoria, str) and
                                      isinstance(orcamento.mes_ano, datetime)):
            key = (orcamento.tipo.categoria, orcamento.mes_ano)
            super().add(key, orcamento)

    def load(self):
        super().load()
        movimentacao_dao = MovimentacaoDAO()
        tipo_orcamento_dao = TipoOrcamentoDAO()
        for orcamento in self.get_all():
            movimentacoes_sincronizadas = []
            for movimentacao in orcamento.movimentacoes:
                mov = movimentacao_dao.get(movimentacao.codigo)
                if mov is not None:
                    movimentacoes_sincronizadas.append(mov)
            orcamento.movimentacoes = movimentacoes_sincronizadas
            tipo = tipo_orcamento_dao.get(orcamento.tipo.categoria)
            if tipo is not None:
                orcamento.tipo = tipo

    def get(self, orcamento: Orcamento):
        if isinstance(orcamento, Orcamento):
            key = (orcamento.tipo.categoria, orcamento.mes_ano)
            return super().get(key)

    def remove(self, orcamento: Orcamento):
        if isinstance(orcamento, Orcamento):
            key = (orcamento.tipo.categoria, orcamento.mes_ano)
            return super().remove(key)

