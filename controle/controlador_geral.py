from limite.tela_geral import TelaGeral

class ControladorGeral:

    def __init__(self):
        from controle.controlador_tipo_orcamento import ControladorTipoOrcamento
        from controle.controlador_pessoa import ControladorPessoa
        from controle.controlador_orcamento import ControladorOrcamento
        from controle.controlador_usuario import ControladorUsuario
        from controle.controlador_movimentacao import ControladorMovimentacao
        self.__controlador_tipo_orcamento = ControladorTipoOrcamento(self)
        self.__controlador_pessoa = ControladorPessoa(self)
        self.__controlador_orcamento = ControladorOrcamento(self)
        self.__controlador_usuario = ControladorUsuario(self)
        self.__controlador_movimentacao = ControladorMovimentacao(self)
        self.__tela_geral = TelaGeral()
        self.usuario_logado = None

    @property
    def controlador_tipo_orcamento(self):
        return self.__controlador_tipo_orcamento

    @property
    def controlador_pessoa(self):
        return self.__controlador_pessoa

    @property
    def controlador_orcamento(self):
        return self.__controlador_orcamento

    @property
    def controlador_usuario(self):
        return self.__controlador_usuario

    @property
    def controlador_movimentacao(self):
        return self.__controlador_movimentacao

    def inicializar_sistema(self):
        self.__controlador_usuario.abrir_tela()

    def cadastrar_tipos_orcamento(self):
        self.__controlador_tipo_orcamento.abrir_tela()

    def cadastrar_orcamentos(self):
        self.__controlador_orcamento.abrir_tela()

    def cadastrar_pessoas(self):
        self.__controlador_pessoa.abrir_tela()

    def cadastrar_movimentacoes(self):
        self.__controlador_movimentacao.abrir_tela()

    def encerrar_sistema(self):
        exit(5)

    def abrir_tela(self):
        lista_opcoes = {1: self.cadastrar_orcamentos, 2: self.cadastrar_pessoas, 3: self.cadastrar_tipos_orcamento, 4: self.cadastrar_movimentacoes, 5: self.encerrar_sistema}

        while True:
            opcao_escolhida = self.__tela_geral.tela_opcoes()
            if opcao_escolhida is None:
                self.encerrar_sistema()
            funcao_escolhida = lista_opcoes[opcao_escolhida]
            funcao_escolhida()