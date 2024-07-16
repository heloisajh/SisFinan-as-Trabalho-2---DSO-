from persistencia.dao import DAO
from entidade.usuario import Usuario

class UsuarioDAO(DAO):

    __instance = None

    def __init__(self):
        super().__init__('usuario.pkl')

    def __new__(cls):
        if UsuarioDAO.__instance is None:
            UsuarioDAO.__instance = object.__new__(cls)
        return UsuarioDAO.__instance

    def add(self, usuario: Usuario):
        if isinstance(usuario, Usuario):
            super().add(usuario.senha, usuario)

    def get(self, usuario: Usuario):
        if isinstance(usuario, Usuario):
            return super().get(usuario.senha)

    def remove(self, usuario: Usuario):
        if isinstance(usuario, Usuario):
            super().remove(usuario.senha)