from limite.tela_usuario import TelaUsuario
from entidade.usuario import Usuario
from controle.controlador_geral import ControladorGeral
from persistencia.usuario_dao import UsuarioDAO


class ControladorUsuario:

    def __init__(self, controlador_geral):
        self.__usuario_dao = UsuarioDAO()
        if isinstance(controlador_geral, ControladorGeral):
            self.__controlador_geral = controlador_geral
        self.__tela_usuario = TelaUsuario()

    def achar_usuario(self, nome: str):
        if isinstance(nome, str):
            for usuario in self.__usuario_dao.get_all():
                if usuario.nome == nome:
                    return usuario
            return None

    def cadastrar_usuario(self):
        dados_usuario = self.__tela_usuario.pegar_usuario()
        if dados_usuario is None:
            return
        u = self.achar_usuario(dados_usuario["nome"])
        if u is None:
            usuario = Usuario(dados_usuario["nome"], dados_usuario["senha"])
            self.__usuario_dao.add(usuario)
            self.__tela_usuario.mostrar_mensagem("Cadastro realizado com sucesso!")
            self.login()
        else:
            self.__tela_usuario.mostrar_mensagem("Usuário já cadastrado no sistema, por favor, faça o login.")

    def login(self):
        dados_usuario = self.__tela_usuario.pegar_usuario()
        if dados_usuario is None:
            return
        usuario = self.achar_usuario(dados_usuario["nome"])

        if usuario is not None:
            if usuario.senha == dados_usuario["senha"]:
                self.__controlador_geral.usuario_logado = usuario
                self.__controlador_geral.abrir_tela()
            else:
                self.__tela_usuario.mostrar_mensagem("Senha incorreta, por favor, tente novamente")
        else:
            self.__tela_usuario.mostrar_mensagem("Usuário não cadastrado, por favor, primeiramente, realize o cadastro.")

    def alterar_senha(self):
        dados_usuario = self.__tela_usuario.pegar_senha()
        if dados_usuario is None:
            return
        usuario = self.achar_usuario(dados_usuario["nome"])
        if usuario is not None:
            nova_senha = dados_usuario["senha"]
            usuario.senha = nova_senha
            self.__tela_usuario.mostrar_mensagem("Senha alterada com sucesso.")
        else:
            self.__tela_usuario.mostrar_mensagem("Usuário não encontrado.")

    def encerrar_sistema(self):
        exit(4)

    def abrir_tela(self):
        lista_opcoes = {1: self.login, 2: self.alterar_senha, 3: self.cadastrar_usuario, 4: self.encerrar_sistema}
        continua = True
        while continua:
            opcao = self.__tela_usuario.tela_opcoes()
            if opcao is None or opcao not in lista_opcoes:
                self.encerrar_sistema()
                break
            lista_opcoes[opcao]()
